"""Leitura IFC2x3 da H03: associacao por Tag, materiais e malhas; sem gravar IFC/RVT.

O conjunto Structural usa os nomes portugueses observados no exportador desta
instalacao. Nao constitui um validador universal de todos os esquemas/psets IFC.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys
import time

FIELDS = {
    'compressionMPa': ('Compressão do concreto', 'concreteCompression', 1e-6),
    'youngMPa': ('Módulo de elasticidade', 'youngModulus', 1e-6),
    'densityKgM3': ('Densidade', 'density', 1),
    'poisson': ('Relação de Poisson', 'poissonRatio', 1),
}
CLASSES = {'IfcColumn': 'Pilares estruturais', 'IfcBeam': 'Framing estrutural', 'IfcSlab': 'Pisos'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def material_leaves(material):
    if material is None:
        return []
    if material.is_a('IfcMaterial'):
        return [material]
    if material.is_a('IfcMaterialLayerSetUsage'):
        return material_leaves(material.ForLayerSet)
    if material.is_a('IfcMaterialLayerSet'):
        return [m for layer in material.MaterialLayers for m in material_leaves(layer.Material)]
    if material.is_a('IfcMaterialList'):
        return list(material.Materials)
    raise ValueError('Associacao de material fora do escopo: '+material.is_a())


def numeric_property(model, prop, target):
    from ifcopenshell.util.unit import get_property_unit
    if prop is None or prop.NominalValue is None:
        return {'status': 'absent', 'value': None}
    nominal = prop.NominalValue
    required = {'compressionMPa': 'IfcPressureMeasure', 'youngMPa': 'IfcPressureMeasure',
                'densityKgM3': 'IfcMassDensityMeasure', 'poisson': 'IfcReal'}[target]
    if nominal.is_a() != required:
        return {'status': 'unexpected_measure_type', 'value': None, 'measure': nominal.is_a()}
    raw = nominal.wrappedValue
    if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not math.isfinite(raw):
        return {'status': 'invalid_value', 'value': None}
    unit = get_property_unit(prop, model)
    if target != 'poisson' and unit is None:
        return {'status': 'missing_unit', 'value': None, 'raw': raw}
    expected = {'compressionMPa': 'PRESSUREUNIT', 'youngMPa': 'PRESSUREUNIT',
                'densityKgM3': 'MASSDENSITYUNIT'}.get(target)
    if unit is not None and (expected is None or unit.UnitType != expected):
        return {'status': 'unexpected_unit', 'value': None, 'raw': raw, 'unit': str(unit)}
    factor = 1 if unit is None else scale_to_si(unit)
    return {'status': 'read', 'value': raw*factor*FIELDS[target][2], 'raw': raw,
            'measure': nominal.is_a(), 'unit': None if unit is None else str(unit)}


def scale_to_si(unit):
    """Normaliza massa em kg, inclusive dentro da unidade derivada de densidade.

    IfcSIUnit nomeia GRAM, enquanto o destino SI de massa e kg. Na dependencia
    0.9.0post1, get_unit_scale(KILO GRAM) retorna 1000; evita-se aplicar esse
    fator como se a unidade de destino fosse kg.
    """
    from ifcopenshell.util.unit import get_unit_scale
    if unit.is_a('IfcSIUnit'):
        return get_unit_scale(unit)*(0.001 if unit.Name == 'GRAM' else 1)
    if unit.is_a('IfcDerivedUnit'):
        return math.prod(scale_to_si(e.Unit)**e.Exponent for e in unit.Elements)
    if unit.is_a('IfcConversionBasedUnit'):
        conversion = unit.ConversionFactor
        return conversion.ValueComponent.wrappedValue*scale_to_si(conversion.UnitComponent)
    raise ValueError('Unidade fora do escopo de conversao: '+str(unit))


def inspect_model(model, native):
    from ifcopenshell.util.element import get_material
    if model.schema != 'IFC2X3':
        raise ValueError('Este auditor delimita o ensaio ao IFC2X3')
    native_by_id = {e['id']: e for e in native['elements']}
    if len(native_by_id) != len(native['elements']):
        raise ValueError('ID nativo duplicado')
    materials = {m['id']: m for m in native['materials']}
    rows, seen = [], set()
    for cls in CLASSES:
        for obj in model.by_type(cls):
            tag = obj.Tag
            if not tag or tag in seen or tag not in native_by_id:
                raise ValueError('Tag ausente, repetida ou nao associada: '+str(tag))
            seen.add(tag)
            source = native_by_id[tag]
            expected_category = {'IfcColumn': '-2001330', 'IfcBeam': '-2001320', 'IfcSlab': '-2000032'}[cls]
            if source['categoryId'] != expected_category:
                raise ValueError('Classe IFC difere da categoria nativa: '+tag)
            mat = materials.get(source['structuralMaterialId'])
            leaves = material_leaves(get_material(obj))
            match = mat is not None and len(leaves) == 1 and leaves[0].Name == mat['name']
            row = dict(revitId=tag, guid=obj.GlobalId, ifcClass=cls,
                       nativeMaterialId=source['structuralMaterialId'],
                       nativeMaterialName=None if mat is None else mat['name'],
                       ifcMaterialNames=[m.Name for m in leaves], singleMaterialNameMatches=match,
                       properties={})
            props = {}
            if match:
                for pset in model.get_inverse(leaves[0]):
                    if pset.is_a('IfcExtendedMaterialProperties') and pset.Name == 'Structural':
                        for prop in pset.ExtendedProperties:
                            if prop.is_a('IfcPropertySingleValue'):
                                if prop.Name in props:
                                    raise ValueError('Propriedade Structural repetida: '+prop.Name)
                                props[prop.Name] = prop
            for key, (label, native_key, _) in FIELDS.items():
                read = numeric_property(model, props.get(label), key)
                n = {} if mat is None else mat.get('asset', {}).get(native_key, {})
                expected = n.get('converted') if n.get('status') == 'read' else None
                if isinstance(expected, list):
                    expected = expected[0] if expected and all(v == expected[0] for v in expected) else None
                read['nativeValue'] = expected
                read['matchesNative'] = (match and read['status'] == 'read' and expected is not None
                                         and math.isclose(read['value'], expected, rel_tol=1e-9, abs_tol=1e-8))
                row['properties'][key] = read
            rows.append(row)
    unmatched = sorted(set(native_by_id)-seen)
    return dict(schema=model.schema, elementCount=len(rows),
                countsByClass=dict(Counter(r['ifcClass'] for r in rows)),
                unmatchedNativeIds=unmatched,
                materialPropertiesEntityCount=len(model.by_type('IfcMaterialProperties')),
                materialPropertyEntityTypes=dict(Counter(p.is_a() for p in model.by_type('IfcMaterialProperties'))),
                singleMaterialNameMatches=sum(r['singleMaterialNameMatches'] for r in rows),
                matchingPropertyCounts={k: sum(r['properties'][k]['matchesNative'] for r in rows) for k in FIELDS},
                rows=rows)


def inspect_geometry(model):
    import ifcopenshell.geom as geom
    import numpy as np
    settings = geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    rows = {}
    for cls in CLASSES:
        for obj in model.by_type(cls):
            shape = geom.create_shape(settings, obj)
            v = np.array(shape.geometry.verts).reshape(-1, 3)
            f = np.array(shape.geometry.faces).reshape(-1, 3)
            if not np.isfinite(v).all() or not len(f):
                raise ValueError('Malha ausente ou nao finita: '+obj.Tag)
            edges, orientation = Counter(), Counter()
            for a, b, c in f:
                for start, end in ((a,b),(b,c),(c,a)):
                    edge = tuple(sorted((int(start), int(end))))
                    edges[edge] += 1
                    orientation[edge] += 1 if start < end else -1
            if any(n != 2 for n in edges.values()) or any(orientation.values()):
                raise ValueError('Malha nao fechada/orientada: '+obj.Tag)
            shifted = v-v.mean(axis=0)
            volume = abs(float(np.einsum('ij,ij->i', shifted[f[:,0]],
                               np.cross(shifted[f[:,1]],shifted[f[:,2]])).sum()/6))
            triangles = sorted(tuple(sorted(tuple(round(float(n), 9) for n in v[i]) for i in tri)) for tri in f)
            rows[obj.Tag] = dict(meshVolumeM3=volume, triangleCount=len(f),
                                canonicalTrianglesSha256=hashlib.sha256(repr(triangles).encode()).hexdigest())
    return dict(worldCoordinates=True, unit='m', coordinateDecimals=9, closedOrientedMeshes=True,
                sumSeparateMeshVolumesM3=sum(r['meshVolumeM3'] for r in rows.values()),
                unionVolumeCalculated=False, rows=rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--deps', type=Path)
    p.add_argument('--native', type=Path, required=True)
    p.add_argument('--folder', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    if args.deps:
        sys.path.insert(0, str(args.deps))
    import ifcopenshell
    started, tick = datetime.now(timezone.utc).isoformat(), time.perf_counter()
    native = json.loads(args.native.read_text(encoding='utf-8-sig'))
    sources = [args.native]
    hashes = {str(args.native): sha(args.native)}
    result = dict(revision='H03/R94', startedAtUtc=started, ifcopenshellVersion=ifcopenshell.version,
                  geometryEngine='IfcOpenShell tessellation', outputs={}, structuralApproval=False,
                  receiverVerified=False, wholeFlowTotalMeasured=False,
                  limits=['Ensaio de exportacao da mesma autoria; nao mede recepcao/calculo no Eberick.',
                          'Mapeamento por Tag e material unico; nomes nao comprovam identidade universal.',
                          'Numeros sao propriedades cadastradas; Young nao e automaticamente Eci/Ecs.',
                          'Malha igual entre arquivos nao verifica modelo analitico, armaduras ou normas.',
                          'Nao se calculou uniao de solidos nem quantitativo executivo.'])
    for label in ('CONTROLE', 'MATERIAIS', 'MATERIAIS-CV'):
        path = args.folder/('H03-R93-'+label+'.ifc')
        hashes[str(path)] = sha(path)
        sources.append(path)
        model = ifcopenshell.open(str(path))
        data = inspect_model(model, native)
        data['geometry'] = inspect_geometry(model)
        data['viewDescription'] = list(model.header.file_description.description)
        result['outputs'][label] = data
    control = result['outputs']['CONTROLE']['geometry']['rows']
    for data in result['outputs'].values():
        rows = data['geometry']['rows']
        data['geometry']['sameTagsAsControl'] = set(rows) == set(control)
        data['geometry']['triangleMismatchIds'] = [k for k in rows if k not in control or
            rows[k]['canonicalTrianglesSha256'] != control[k]['canonicalTrianglesSha256']]
    result['sources'] = [dict(path=str(path), sha256=hashes[str(path)], bytes=path.stat().st_size) for path in sources]
    if any(sha(path) != hashes[str(path)] for path in sources):
        raise ValueError('Fonte mudou durante a leitura')
    result['sourcesUnchangedAfterRead'] = True
    result['endedAtUtc'] = datetime.now(timezone.utc).isoformat()
    result['auditScriptSeconds'] = time.perf_counter()-tick
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({k: dict(elements=v['elementCount'], materialNames=v['singleMaterialNameMatches'],
        matches=v['matchingPropertyCounts'], separateMeshVolumesM3=v['geometry']['sumSeparateMeshVolumesM3'],
        triangleMismatchIds=v['geometry']['triangleMismatchIds']) for k,v in result['outputs'].items()}))


if __name__ == '__main__':
    main()

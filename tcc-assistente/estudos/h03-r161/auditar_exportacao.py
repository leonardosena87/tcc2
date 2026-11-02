"""Auditoria somente leitura da exportação nativa R161; sem reparar o IFC.

Compara identidades/classes e informações explicitamente lidas no Revit.
Usa IfcOpenShell 0.9.0.post1; geometria em metros, atributos na unidade IFC.
Não dimensiona, não aprova apoios e não mede o fluxo BIM completo.
"""
import hashlib
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import sys
import time

sys.path.insert(0, 'D:/TCC/work/ifc/deps')
import ifcopenshell
import ifcopenshell.geom
from ifcopenshell.util.element import get_material, get_psets
from ifcopenshell.util.unit import calculate_unit_scale, get_property_unit
import numpy as np
from leitor_propriedades_r94 import FIELDS, material_leaves, numeric_property

OUT = Path('D:/TCC/outputs/Intercambio-H03-R161-R160-NAO-EXECUTAR')
IFC = OUT/'H03-R160-Revit-SOMENTE-VIGA-PATAMAR-NAO-EXECUTAR.ifc'
NATIVE = Path('D:\\TCC\\outputs\\Escada-H03-R160-SOMENTE-VIGA-NAO-EXECUTAR\\R160-releitura-nativa-20261102-163548.json')
RVT = Path('D:\\TCC\\outputs\\Escada-H03-R160-SOMENTE-VIGA-NAO-EXECUTAR\\H03-R160-Revit-SOMENTE-VIGA-PATAMAR-NAO-EXECUTAR.rvt')
EXPECTED_RVT_SHA = 'b491460fb73deddf6e9552fc15fc6708254dce15733eb5b528e8a7fbc3fbcb6c'
EXPECTED_NATIVE_SHA = 'fd43fd25e3665bfe6fc3b9eaa14892b9d7446b19809efaae6e278a0aad3f3a18'
CLASSES = {'column': 'IfcColumn', 'beam': 'IfcBeam', 'slab': 'IfcSlab'}
SPEC = 'https://standards.buildingsmart.org/IFC/RELEASE/IFC2x3/FINAL/HTML/ifcsharedbldgelements/lexical/ifcstairflight.htm'


def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))


def compare_length(raw, scale, expected):
    value = None if raw is None else raw*scale
    return dict(raw=raw, interpretedM=value, nativeM=expected,
                matchesNative=value is not None and math.isclose(value, expected, abs_tol=1e-8, rel_tol=1e-8))


def by_native_tag(objects, native):
    """Não confunde o patamar agregado da escada com uma laje da edificação."""
    wanted = {str(e['Id']): e for e in native}
    if len(wanted) != len(native):
        raise ValueError('ID nativo duplicado')
    found = {}
    extras = []
    for obj in objects:
        tag = obj.Tag
        if tag not in wanted:
            extras.append(obj)
            continue
        if tag in found:
            raise ValueError('Tag IFC nativa duplicada: '+tag)
        if obj.is_a() != CLASSES[wanted[tag]['Kind']]:
            raise ValueError('Classe IFC divergente: '+tag)
        found[tag] = obj
    return wanted, found, extras


def require_complete_identity(wanted, found, objects):
    missing = sorted(set(wanted)-set(found))
    if missing:
        raise ValueError('Elementos nativos ausentes no IFC: '+', '.join(missing))
    removed = {'473797', '473798'}
    retained_removed = removed & {str(getattr(o, 'Tag', None)) for o in objects}
    if retained_removed:
        raise ValueError('Pilar rejeitado ainda presente: '+', '.join(sorted(retained_removed)))


def mesh(obj, settings):
    shape = ifcopenshell.geom.create_shape(settings, obj)
    v = np.asarray(shape.geometry.verts).reshape(-1, 3)
    f = np.asarray(shape.geometry.faces).reshape(-1, 3)
    if not len(v) or not len(f) or not np.isfinite(v).all():
        raise ValueError('Malha vazia ou não finita: '+str(obj.Tag))
    return dict(minM=v.min(0).tolist(), maxM=v.max(0).tolist(), vertices=len(v), triangles=len(f))


def material_names(obj):
    mat = get_material(obj)
    if mat is None:
        return []
    if mat.is_a('IfcMaterial'):
        return [mat.Name]
    if mat.is_a('IfcMaterialLayerSetUsage'):
        mat = mat.ForLayerSet
    if mat.is_a('IfcMaterialLayerSet'):
        return [layer.Material.Name for layer in mat.MaterialLayers if layer.Material]
    if mat.is_a('IfcMaterialList'):
        return [m.Name for m in mat.Materials]
    raise ValueError('Associação de material não prevista: '+mat.is_a())


def material_properties(model,obj,native_fck):
    """Lê o conjunto Structural observado na R94; não converte ausência em zero."""
    materials=material_leaves(get_material(obj));props={}
    if len(materials)==1:
        for pset in model.get_inverse(materials[0]):
            if pset.is_a('IfcExtendedMaterialProperties') and pset.Name=='Structural':
                for prop in pset.ExtendedProperties:
                    if prop.is_a('IfcPropertySingleValue'):
                        if prop.Name in props:raise ValueError('Propriedade material repetida: '+prop.Name)
                        props[prop.Name]=prop
    result={key:numeric_property(model,props.get(label),key) for key,(label,_,_) in FIELDS.items()}
    compression=result['compressionMPa'];compression['nativeValue']=native_fck
    compression['matchesNative']=(compression['status']=='read' and math.isclose(compression['value'],native_fck,abs_tol=1e-8))
    for key in ('youngMPa','densityKgM3','poisson'):result[key]['nativeCurrentValueNotRead']=True
    return result


def pset_length(model, obj, label, expected):
    for rel in obj.IsDefinedBy:
        if not rel.is_a('IfcRelDefinesByProperties'):
            continue
        pset = rel.RelatingPropertyDefinition
        if not pset.is_a('IfcPropertySet') or pset.Name != 'Pset_StairFlightCommon':
            continue
        for prop in pset.HasProperties:
            if prop.Name != label or not prop.is_a('IfcPropertySingleValue'):
                continue
            unit = get_property_unit(prop, model)
            if unit is None or not unit.is_a('IfcSIUnit') or unit.Name != 'METRE' or unit.UnitType != 'LENGTHUNIT':
                raise ValueError('Unidade de comprimento não prevista: '+str(unit))
            from ifcopenshell.util.unit import get_unit_scale
            result = compare_length(prop.NominalValue.wrappedValue, get_unit_scale(unit), expected)
            result.update(unit=str(unit), measure=prop.NominalValue.is_a())
            return result
    return compare_length(None, 1, expected)


def main():
    t0 = time.perf_counter()
    sources = [IFC, NATIVE, RVT, OUT/'R161-configuracao-IFC-CV.json', OUT/'R161-configuracao-IFC-releitura-nativa.json']
    before = {str(p): sha(p) for p in sources}
    if before[str(RVT)] != EXPECTED_RVT_SHA:
        raise ValueError('RVT não corresponde à cópia fechada/reaberta auditada')
    if before[str(NATIVE)] != EXPECTED_NATIVE_SHA:
        raise ValueError('Releitura nativa diverge da referencia R160 preservada')
    native = read(NATIVE)
    assert len(native['Elements']) == 63
    assert Counter(e['Kind'] for e in native['Elements']) == {'column':22,'beam':30,'slab':11}
    model = ifcopenshell.open(str(IFC))
    assert model.schema == 'IFC2X3'
    prepared = read(sources[-2]); config = read(sources[-1])
    config_diff = [k for k in prepared if k != 'Name' and prepared[k] != config.get(k)]
    assert not config_diff
    assert config['IFCVersion'] == 10 and config['ExportMaterialPsets'] is True
    assert config['VisibleElementsOfCurrentView'] is False and config['UseActiveViewGeometry'] is False and config['StoreIFCGUID'] is False
    settings = ifcopenshell.geom.settings(); settings.set(settings.USE_WORLD_COORDS, True)
    unit_scale = calculate_unit_scale(model)
    objects = [o for cls in CLASSES.values() for o in model.by_type(cls)]
    wanted, found, extras = by_native_tag(objects, native['Elements'])
    require_complete_identity(wanted, found, model.by_type('IfcProduct'))
    stair_source = native['Stair']
    stair = [o for o in model.by_type('IfcStair') if o.Tag == str(stair_source['Id'])]
    assert len(stair) == 1
    children = [o for rel in stair[0].IsDecomposedBy for o in rel.RelatedObjects]
    assert all(o in children and o.is_a('IfcSlab') and o.PredefinedType == 'LANDING' for o in extras)
    assert len(extras) == 1
    rows = []
    for tag, obj in sorted(found.items()):
        src = wanted[tag]
        rows.append(dict(revitId=tag, mark=src['Mark'], ifcGuid=obj.GlobalId, ifcClass=obj.is_a(),
                         nativeMaterialId=src['MaterialId'], nativeFckMPa=src['MaterialFckMPa'],
                         ifcMaterialNames=material_names(obj), materialProperties=material_properties(model,obj,src['MaterialFckMPa']), geometry=mesh(obj, settings)))
    run_rows = []
    for src in stair_source['Runs']:
        matches = [o for o in children if o.is_a('IfcStairFlight') and o.Tag == str(src['Id'])]
        assert len(matches) == 1
        obj = matches[0]
        geom = mesh(obj, settings)
        run_rows.append(dict(revitId=str(src['Id']), guid=obj.GlobalId,
            numberOfRisers=obj.NumberOfRiser, nativeNumberOfRisers=src['Risers'],
            numberOfTreads=obj.NumberOfTreads, nativeNumberOfTreads=src['Treads'],
            attributeRiserHeight=compare_length(obj.RiserHeight, unit_scale, stair_source['RiserM']),
            attributeTreadLength=compare_length(obj.TreadLength, unit_scale, stair_source['TreadM']),
            psetRiserHeight=pset_length(model, obj, 'RiserHeight', stair_source['RiserM']),
            psetTreadLength=pset_length(model, obj, 'TreadLength', stair_source['TreadM']),
            meshWidthM=geom['maxM'][0]-geom['minM'][0], nativeWidthM=src['WidthM'],
            geometry=geom, ifcMaterialNames=material_names(obj)))
    levels = []
    for lev in model.by_type('IfcBuildingStorey'):
        contained = [o for rel in lev.ContainsElements for o in rel.RelatedElements]
        levels.append(dict(guid=lev.GlobalId, name=lev.Name, elevationM=lev.Elevation*unit_scale,
                           directlyContainedCount=len(contained), containedTags=[getattr(o, 'Tag', None) for o in contained],
                           emptyDirectContainment=len(contained) == 0, removed=False))
    material_props = model.by_type('IfcMaterialProperties')
    assert before == {str(p): sha(p) for p in sources}
    result = dict(revision='H03/R161', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        ifcopenshellVersion=ifcopenshell.version, schema=model.schema, projectLengthUnitScaleToM=unit_scale,
        configurationReadbackMatchesPreparedExceptSavedName=True, configurationNameReadback=config['Name'],
        fileDescription=list(model.header.file_description.description), sources=before,
        sourceHashesUnchangedAfterRead=True, rawNativeExportUnmodified=True, nativeRevitFileUnchanged=True,
        expectedBuildingElementCount=len(wanted), foundBuildingElementCount=len(found),
        missingNativeIds=sorted(set(wanted)-set(found)), countsByClass=dict(Counter(r['ifcClass'] for r in rows)),
        extraSlabIsStairLanding=True, totalIfcSlabCount=len(model.by_type('IfcSlab')),
        buildingElementsWithNamedMaterial=sum(bool(r['ifcMaterialNames']) for r in rows),
        materialPropertiesEntityCount=len(material_props),
        buildingElementsWithReadableCompressionMatchingNative=sum(r['materialProperties']['compressionMPa']['matchesNative'] for r in rows),
        nativeMaterialNamesNotReadInCurrentReadback=True,
        currentNativeYoungDensityPoissonNotRead=True,
        stairGuid=stair[0].GlobalId, stairRuns=run_rows,
        stairCountsPreserved=all(r['numberOfRisers'] == r['nativeNumberOfRisers'] and r['numberOfTreads'] == r['nativeNumberOfTreads'] for r in run_rows),
        stairDimensionalAttributeDiscrepancy=any(not r[k]['matchesNative'] for r in run_rows for k in ('attributeRiserHeight','attributeTreadLength')),
        stairDiscrepancyScope='Atributos e Pset_StairFlightCommon comparados separadamente por unidade; não se inferiu o comportamento do receptor.',
        stairSchemaReference=SPEC,
        landing=dict(revitTagObservedInIfc=extras[0].Tag, tagIndependentlyConfirmedInNativeAudit=False,
                     ifcGuid=extras[0].GlobalId, geometry=mesh(extras[0], settings), nativeConcreteTopM=stair_source['ConcreteLandingM']),
        landingBeam=next(r for r in rows if r['mark'] == 'V16-ESC-PAT'),
        levels=levels, rows=rows,
        meshReadabilityIsNotProofOfGeometricEquivalenceOrClosedSolid=True,
        nativeBuildingIdentitiesPreserved=len(found) == 63, eberickReceptionVerified=False,
        removedColumnTagsAbsent=True,
        fullCompatibilityReviewCompleted=False, structuralApproval=False,
        usableForPairedFlowRanking=False, auditScriptSeconds=time.perf_counter()-t0)
    (OUT/'R161-IFC-auditoria.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['foundBuildingElementCount','countsByClass','materialPropertiesEntityCount','stairCountsPreserved','stairDimensionalAttributeDiscrepancy','sourceHashesUnchangedAfterRead','auditScriptSeconds']}))


if __name__ == '__main__':
    main()

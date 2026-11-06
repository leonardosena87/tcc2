"""Reconstitui seções e eixos nominais de 15 peças para um ensaio IFC4."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

STUDIES = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(STUDIES / 'h03-r229'))
from preparar_niveis import (OUT as R229, TARGET as INPUT, SOURCE, direct_containers,
                              materials, shapes, storeys)
from preparar_derivado import (ifcopenshell, nominal_box, read, schema_issues,
                               sha, target_item as beam_item)
from geometria_nominal_r95 import nominal_geometry

sys.path.insert(0, str(STUDIES / 'h03-r164'))
from preparar_colunas import target_item as column_item
from ifcopenshell.api.pset import edit_pset, remove_pset
from ifcopenshell.util.element import get_psets, get_type
from ifcopenshell.util.unit import calculate_unit_scale


OUT = R229.parent / 'H03-R230-IFC4-SECOES-NOMINAIS-NAO-EXECUTAR'
TARGET = OUT / 'H03-R230-IFC4-DERIVADO-SECOES-NOMINAIS-NAO-EXECUTAR.ifc'
NATIVE = SOURCE / 'R225-exportacao-ifc.json'
CLASSES = {'beam': 'IfcBeam', 'column': 'IfcColumn'}
OLD_CUT_FIELDS = {'Comprimento do corte', 'Volume'}
UPPER_COLUMNS = {'P5-N2', 'P11-N2'}


def semantic_snapshot(model):
    return {o.GlobalId: dict(
        cls=o.is_a(), tag=o.Tag, name=o.Name, objectType=o.ObjectType,
        psets=get_psets(o, psets_only=True, should_inherit=False),
        qtos=get_psets(o, qtos_only=True),
        associations=sorted(str(r) for r in o.HasAssociations),
        typeId=get_type(o).GlobalId if get_type(o) else None,
    ) for o in model.by_type('IfcElement')}


def remove_cut_quantities(model, obj, expected):
    qto_name = f'Qto_{obj.is_a()[3:]}BaseQuantities'
    occurrence_qtos = get_psets(obj, qtos_only=True, should_inherit=False)
    if set(expected['qtos']) != {qto_name} or expected['qtos'] != occurrence_qtos:
        raise ValueError(f'Quantitativos fora do escopo em {obj.Tag}')
    qto = model.by_id(occurrence_qtos[qto_name]['id'])
    if any(set(r.RelatedObjects) != {obj} for r in qto.DefinesOccurrence):
        raise ValueError(f'Quantitativo compartilhado em {obj.Tag}')
    remove_pset(model, product=obj, pset=qto)
    expected['qtos'].clear()
    dimensions = expected['psets']['Cotas']
    removed = {k: dimensions.pop(k) for k in dimensions.keys() & OLD_CUT_FIELDS}
    pset = model.by_id(dimensions['id'])
    if any(set(r.RelatedObjects) != {obj} for r in pset.DefinesOccurrence):
        raise ValueError(f'Cotas compartilhadas em {obj.Tag}')
    edit_pset(model, pset=pset, properties=dict.fromkeys(removed))
    return dict(quantitySet=qto_name, obsoleteCutFields=removed)


def expected_box(item):
    if item['kind'] == 'beam':
        return nominal_box(item)
    x, y, b, h = (item[k] for k in ('x', 'y', 'b', 'h'))
    return [x-b/2, y-h/2, item['z0']], [x+b/2, y+h/2, item['z1']]


def main():
    t0 = time.perf_counter()
    if TARGET.exists():
        raise FileExistsError(TARGET)
    prior = read(R229 / 'R229-auditoria.json')
    frozen = {p: sha(p) for p in (INPUT, NATIVE)}
    if (frozen[INPUT] != prior['preparation']['derivedSha256']
            or frozen[NATIVE] != read(SOURCE / 'R225-IFC-auditoria.json')['nativeSha256']):
        raise ValueError('Arquivos de entrada diferentes das revisões auditadas')
    beams = set(prior['sectionDifferenceMarksAfter'])
    if len(beams) != 13 or set(prior['axialBoxGapsAfter']) != UPPER_COLUMNS | {'V2-N2'}:
        raise ValueError('O conjunto de ocorrências difere da R229')
    expected_marks = {'beam': beams, 'column': UPPER_COLUMNS}
    items = {str(e['Id']): (beam_item if e['Kind'] == 'beam' else column_item)(e)
             for e in read(NATIVE)['Readback']['Elements']
             if e['Kind'] in expected_marks and e['Mark'] in expected_marks[e['Kind']]}
    if {e['id'] for e in items.values()} != beams | UPPER_COLUMNS or len(items) != 15:
        raise ValueError('Peças nominais ausentes ou duplicadas')

    model = ifcopenshell.open(str(INPUT))
    if model.schema != 'IFC4':
        raise ValueError('Esperado IFC4')
    objects = {o.Tag: o for cls in CLASSES.values() for o in model.by_type(cls) if o.Tag in items}
    if set(objects) != set(items):
        raise ValueError('Identificadores R225 não encontrados no IFC derivado')
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    before_shapes = shapes(model, settings)
    before_psets = semantic_snapshot(model)
    before_levels = {z: s.GlobalId for z, s in storeys(model).items()}
    before_containers = direct_containers(model)
    before_materials = materials(model)
    before_issues = schema_issues(model)
    changes = []
    for tag, item in items.items():
        obj = objects[tag]
        if obj.is_a() != CLASSES[item['kind']] or obj.ObjectPlacement.ReferencedByPlacements:
            raise ValueError(f'Classe ou colocação imprevista em {tag}')
        removed = remove_cut_quantities(model, obj, before_psets[obj.GlobalId])
        nominal_geometry(model, obj, item, calculate_unit_scale(model))
        changes.append(dict(nativeId=tag, mark=item['id'], kind=item['kind'], guid=obj.GlobalId,
                            expectedBoundsM=expected_box(item), removed=removed))

    model.header.file_description.description = [
        *model.header.file_description.description,
        'TCC R230 IFC4 DERIVADO SECOES NOMINAIS PARA RECEPCAO NAO EXECUTAR',
    ]
    model.header.file_name.name = TARGET.name
    serialized = model.to_string()
    reopened = ifcopenshell.file.from_string(serialized)
    if (semantic_snapshot(reopened) != before_psets or direct_containers(reopened) != before_containers
            or materials(reopened) != before_materials or schema_issues(reopened) != before_issues
            or {z: s.GlobalId for z, s in storeys(reopened).items()} != before_levels):
        raise ValueError('Metadados, associações, níveis ou esquema mudaram fora do escopo')
    after_shapes = shapes(reopened, settings)
    for row in changes:
        guid = row['guid']
        old, new = before_shapes.pop(guid), after_shapes.pop(guid)
        if max(abs(a-b) for key, target in zip(('minM', 'maxM'), row['expectedBoundsM'])
               for a, b in zip(new[key], target)) > 1e-7 or old == new:
            raise ValueError(f'Prisma nominal divergente em {row["mark"]}')
        row['sourceBody'] = old
        row['derivedBody'] = new
    if before_shapes != after_shapes or frozen != {p: sha(p) for p in frozen}:
        raise ValueError('Corpo fora do escopo ou insumo alterado')

    OUT.mkdir(parents=True, exist_ok=True)
    with TARGET.open('x', encoding='utf-8') as handle:
        handle.write(serialized)
    result = dict(
        revision='H03/R230', preparedUtc=datetime.now(timezone.utc).isoformat(),
        inputSha256=frozen[INPUT], nativeReadbackSha256=frozen[NATIVE], outputSha256=sha(TARGET),
        originalInputsUnchanged=True, keptStoreysM=list(before_levels),
        restoredBeamBodies=len(beams), restoredColumnBodies=len(UPPER_COLUMNS),
        unchangedOtherBodies=len(after_shapes), schemaIssueCount=len(before_issues),
        prismaticGeometryForReceptionOnly=True, quantitySetsRemoved=len(changes),
        nativeRevitExport=False, structuralApproval=False, elapsedSeconds=time.perf_counter()-t0,
        changes=changes,
    )
    (OUT / 'R230-preparacao.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n',
                                             encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'changes'}, ensure_ascii=False))


if __name__ == '__main__':
    main()

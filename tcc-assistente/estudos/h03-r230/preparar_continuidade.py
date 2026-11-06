"""Complementa o ensaio com três pilares inferiores recortados no IFC bruto."""
from datetime import datetime, timezone
import json
import time

from preparar_geometria import (OUT as R230, TARGET as INPUT, NATIVE, column_item,
    direct_containers, expected_box, ifcopenshell, materials, nominal_geometry, read,
    remove_cut_quantities, schema_issues, semantic_snapshot, sha, shapes, storeys,
    calculate_unit_scale)

OUT = R230.parent / 'H03-R231-IFC4-CONTINUIDADE-NAO-EXECUTAR'
TARGET = OUT / 'H03-R231-IFC4-DERIVADO-CONTINUIDADE-NAO-EXECUTAR.ifc'
MARKS = {'P5-N1', 'P11-N1', 'P12-N1'}


def main():
    t0 = time.perf_counter()
    if TARGET.exists():
        raise FileExistsError(TARGET)
    prior = read(R230 / 'R230-preparacao.json')
    frozen = {p: sha(p) for p in (INPUT, NATIVE)}
    if frozen[INPUT] != prior['outputSha256'] or frozen[NATIVE] != prior['nativeReadbackSha256']:
        raise ValueError('Entrada diferente da R230')
    model = ifcopenshell.open(str(INPUT))
    items = {str(e['Id']): column_item(e) for e in read(NATIVE)['Readback']['Elements']
             if e['Kind'] == 'column' and e['Mark'] in MARKS}
    if {e['id'] for e in items.values()} != MARKS or len(items) != 3:
        raise ValueError('Pilares inferiores ausentes ou duplicados')
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    old_shapes = shapes(model, settings)
    old_semantics = semantic_snapshot(model)
    old_materials = materials(model)
    old_containers = direct_containers(model)
    old_levels = {z: s.GlobalId for z, s in storeys(model).items()}
    old_issues = schema_issues(model)
    changes = []
    for obj in model.by_type('IfcColumn'):
        if obj.Tag not in items:
            continue
        item = items[obj.Tag]
        if obj.ObjectPlacement.ReferencedByPlacements:
            raise ValueError('Colocação compartilhada com filho')
        removed = remove_cut_quantities(model, obj, old_semantics[obj.GlobalId])
        nominal_geometry(model, obj, item, calculate_unit_scale(model))
        changes.append(dict(guid=obj.GlobalId, mark=item['id'], nativeId=obj.Tag,
                            expectedBoundsM=expected_box(item), removed=removed))
    if len(changes) != 3:
        raise ValueError('Conjunto de pilares IFC divergente')
    model.header.file_description.description = [
        *model.header.file_description.description,
        'TCC R231 IFC4 DERIVADO CONTINUIDADE DE TRES PILARES INFERIORES NAO EXECUTAR',
    ]
    model.header.file_name.name = TARGET.name
    serialized = model.to_string()
    checked = ifcopenshell.file.from_string(serialized)
    if (semantic_snapshot(checked) != old_semantics or materials(checked) != old_materials
            or direct_containers(checked) != old_containers or schema_issues(checked) != old_issues
            or {z: s.GlobalId for z, s in storeys(checked).items()} != old_levels):
        raise ValueError('Informação fora do escopo alterada')
    new_shapes = shapes(checked, settings)
    for row in changes:
        old = old_shapes.pop(row['guid'])
        new = new_shapes.pop(row['guid'])
        if max(abs(a-b) for key, values in zip(('minM', 'maxM'), row['expectedBoundsM'])
               for a, b in zip(new[key], values)) > 1e-7:
            raise ValueError('Geometria nominal divergente')
        row.update(sourceBody=old, derivedBody=new)
    if old_shapes != new_shapes or frozen != {p: sha(p) for p in frozen}:
        raise ValueError('Corpo fora do escopo ou arquivo de entrada alterado')
    OUT.mkdir(parents=True, exist_ok=True)
    with TARGET.open('x', encoding='utf-8') as handle:
        handle.write(serialized)
    result = dict(revision='R231', preparedUtc=datetime.now(timezone.utc).isoformat(),
                  inputSha256=frozen[INPUT], nativeReadbackSha256=frozen[NATIVE],
                  outputSha256=sha(TARGET), changedColumnBodies=3, unchangedOtherBodies=len(new_shapes),
                  removedCutQuantitySets=3, schemaIssueCount=len(old_issues), changes=changes,
                  elapsedSeconds=time.perf_counter()-t0, structuralApproval=False)
    (OUT / 'R231-preparacao.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n',
                                             encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'changes'}, ensure_ascii=False))


if __name__ == '__main__':
    main()

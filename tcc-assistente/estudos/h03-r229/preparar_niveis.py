"""Cria um IFC4 experimental com quatro níveis, preservando os corpos R225."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'h03-r162'))
from preparar_derivado import cloud, ifcopenshell, read, schema_issues, sha
from ifcopenshell.api.root.remove_product import remove_product
from ifcopenshell.api.spatial.assign_container import assign_container
from ifcopenshell.util.element import get_container, get_material, get_psets
from ifcopenshell.util.unit import calculate_unit_scale


OUTPUTS = Path('D:/TCC/outputs')
SOURCE = OUTPUTS / 'H03-R225-AUTORIA-COORDENACAO-NAO-EXECUTAR'
INPUT = SOURCE / 'H03-R225-Revit-COORDENACAO-NAO-EXECUTAR.ifc'
OUT = OUTPUTS / 'H03-R229-IFC4-QUATRO-NIVEIS-NAO-EXECUTAR'
TARGET = OUT / 'H03-R229-IFC4-DERIVADO-QUATRO-NIVEIS-NAO-EXECUTAR.ifc'
KEEP_ELEVATIONS = (0.20, 1.77411765, 3.20, 6.39)
REMOVE_ELEVATIONS = (0.0, 0.17, 0.22, 3.0, 3.25)


def products(model):
    return {o.GlobalId: (o.is_a(), o.Tag, o.Name, get_psets(o), str(get_material(o)))
            for o in model.by_type('IfcElement')}


def materials(model):
    return sorted(str(p) for p in model.by_type('IfcMaterialProperties'))


def shapes(model, settings):
    return {o.GlobalId: cloud(o, settings)
            for o in model.by_type('IfcElement') if o.Representation}


def direct_containers(model):
    return {o.GlobalId: tuple(r.RelatingStructure.GlobalId for r in o.ContainedInStructure)
            for o in model.by_type('IfcElement')}


def storeys(model):
    unit = calculate_unit_scale(model)
    rows = model.by_type('IfcBuildingStorey')
    by_elevation = {round(s.Elevation * unit, 8): s for s in rows}
    if len(rows) != len(by_elevation):
        raise ValueError('Níveis distintos com a mesma cota')
    return by_elevation


def main():
    t0 = time.perf_counter()
    if TARGET.exists():
        raise FileExistsError(TARGET)
    expected = read(SOURCE / 'R225-IFC-auditoria.json')['ifcSha256']
    if sha(INPUT) != expected:
        raise ValueError('Entrada diferente do IFC4 congelado da R225')
    model = ifcopenshell.open(str(INPUT))
    if model.schema != 'IFC4':
        raise ValueError('Esperado IFC4')
    before = storeys(model)
    if set(before) != set(KEEP_ELEVATIONS + REMOVE_ELEVATIONS):
        raise ValueError('Conjunto de cotas inesperado')
    before_names = {z: s.Name for z, s in before.items()}
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    old_products = products(model)
    old_shapes = shapes(model, settings)
    old_materials = materials(model)
    old_issues = schema_issues(model)
    expected_containers = direct_containers(model)
    stairs = model.by_type('IfcStair')
    if len(stairs) != 1 or get_container(stairs[0]) != before[0.17]:
        raise ValueError('Escada ausente ou fora do nível da base virtual')
    stair_guid = stairs[0].GlobalId
    expected_containers[stair_guid] = (before[0.20].GlobalId,)
    assign_container(model, products=stairs, relating_structure=before[0.20])
    for z in REMOVE_ELEVATIONS:
        obj = before[z]
        if obj.ContainsElements or obj.IsDecomposedBy:
            raise ValueError(f'Nível {z} m ainda contém objetos')
        remove_product(model, product=obj)
    model.header.file_description.description = [
        *model.header.file_description.description,
        'TCC R229 IFC4 DERIVADO QUATRO NIVEIS NAO EXECUTAR',
    ]
    model.header.file_name.name = TARGET.name
    OUT.mkdir(parents=True, exist_ok=True)
    reopened = ifcopenshell.file.from_string(model.to_string())
    after_names = {z: s.Name for z, s in storeys(reopened).items()}
    if after_names != {z: before_names[z] for z in KEEP_ELEVATIONS}:
        raise ValueError('As cotas estruturais devem permanecer iguais')
    if (products(reopened) != old_products or materials(reopened) != old_materials
            or direct_containers(reopened) != expected_containers
            or shapes(reopened, settings) != old_shapes or schema_issues(reopened) != old_issues):
        raise ValueError('Uma informação fora do escopo da normalização mudou')
    if sha(INPUT) != expected:
        raise ValueError('Arquivo de origem alterado')
    with TARGET.open('x', encoding='utf-8') as handle:
        handle.write(reopened.to_string())
    result = dict(
        revision='H03/R229', preparedUtc=datetime.now(timezone.utc).isoformat(),
        sourceIfc=INPUT.name, sourceSha256=expected, derivedIfc=TARGET.name, derivedSha256=sha(TARGET),
        originalUnchanged=True, storeysBeforeM=before_names, storeysAfterM=after_names,
        preservedElementMetadataCount=len(old_products), preservedWorldPointClouds=len(old_shapes),
        preservedMaterialPropertySets=len(old_materials), schemaIssuesBeforeAndAfter=len(old_issues),
        stairContainerRemap=dict(guid=stair_guid, fromM=0.17, toM=0.20, worldShapeChanged=False),
        scriptSeconds=time.perf_counter()-t0, nativeRevitExport=False, eberickReceptionVerified=False,
        nominalBeamGeometryCorrected=False, structuralApproval=False,
    )
    (OUT / 'R229-preparacao.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n',
                                             encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()

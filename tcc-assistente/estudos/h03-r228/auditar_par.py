"""Compara o primeiro salvamento do IFC4 e dos DWGs R225 no Eberick."""
from collections import Counter
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'h03-r163'))
from auditar_cobertura import beam_frame, coverage, ifcopenshell, mesh, read, sha
from auditar_recepcao import parse_report
from ifcopenshell.util.element import get_container, get_materials, get_psets
from ifcopenshell.util.unit import calculate_unit_scale


OUT = Path('D:/TCC/outputs')
SOURCE = OUT / 'H03-R225-AUTORIA-COORDENACAO-NAO-EXECUTAR'
RESULT = OUT / 'H03-R228-RECEPCAO-R225-NAO-EXECUTAR'
BIM = RESULT / 'R228-BIM-IFC4-BRUTO-NAO-EXECUTAR'
CAD = RESULT / 'R228-CAD-DWG-BRUTO-NAO-EXECUTAR'
REPORT = BIM / 'Arquivos do projeto/Documentos/Eberick/Relatorio_de_importacao_de_elementos_IFC.docx'
SOURCE_IFC = SOURCE / 'H03-R225-Revit-COORDENACAO-NAO-EXECUTAR.ifc'
MODELS = {p: p / 'Arquivos do projeto/Modelo 3D.IFC' for p in (CAD, BIM)}
LEVELS = {'N0': 20, 'PATAMAR': 177.41, 'N1': 320, 'N2': 639}
TOL = 0.0002  # 0,2 mm, para comparação computacional, sem significado normativo
CLASSES = {'beam': 'IfcBeam', 'column': 'IfcColumn'}
GROUPS = {'beam': 'Vigas', 'column': 'Pilares'}


def project_file(root):
    return root / 'Projeto Eberick' / (root.name + '.prj')


def read_model(path):
    model = ifcopenshell.open(str(path))
    if model.schema != 'IFC4':
        raise ValueError(f'Esquema inesperado em {path}: {model.schema}')
    return model


def storeys(model):
    unit = calculate_unit_scale(model)
    return {s.Name: round(s.Elevation * unit, 8) for s in model.by_type('IfcBuildingStorey')}


def counts(model):
    return dict(Counter(e.is_a() for e in model.by_type('IfcElement')))


def level_of(obj):
    return get_container(obj).Name


def overlap(a, b, c, d):
    return min(b, d) - max(a, c)


def candidates(geometry, sources, kind):
    """Cruza a projeção e a cota do corpo IFC de origem, sem usar a marca receptora."""
    lo, hi = geometry['minM'], geometry['maxM']
    for e in sources:
        ref = e['body']
        a, b = ref['min'], ref['max']
        if kind == 'column':
            match = (all(abs(p[i] - q[i]) <= TOL for p, q in ((a, lo), (b, hi)) for i in (0, 1))
                     and overlap(lo[2], hi[2], a[2], b[2]) > TOL)
        else:
            along, cross, *_ = beam_frame(e)
            match = (abs((lo[cross] + hi[cross] - a[cross] - b[cross]) / 2) <= TOL
                     and abs(hi[2] - b[2]) <= TOL
                     and overlap(lo[along], hi[along], a[along], b[along]) > TOL)
        if match:
            yield e['Id']


def collect_parts(model, sources):
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    parts = []
    for kind, cls in CLASSES.items():
        wanted = [e for e in sources if e['Kind'] == kind]
        for obj in model.by_type(cls):
            body = mesh(obj, settings)
            ids = list(candidates(body, wanted, kind))
            props = get_psets(obj)
            section = props['AltoQi_Eberick_Elemento']
            concrete = props.get('Pset_ConcreteElementGeneral', {})
            materials = get_materials(obj)
            parts.append(dict(
                guid=obj.GlobalId, name=obj.Name, kind=kind, level=level_of(obj),
                sourceTag=obj.Tag, candidates=ids, geometry=body,
                sectionCm=[section['Seção_bw' if kind == 'beam' else 'Seção_b'], section['Seção_h']],
                concreteClass=concrete.get('StrengthClass'), coverCm=concrete.get('ConcreteCover'),
                exposureClass=concrete.get('ExposureClass'),
                materialNames=[m.Name for m in materials],
                materialPropertySets=sorted({s.Name for m in materials for s in m.HasProperties}),
            ))
    return parts


def compare_origins(sources, parts):
    results = []
    for e in sources:
        hits = [p for p in parts if p['candidates'] == [e['Id']]]
        axis = 2 if e['Kind'] == 'column' else beam_frame(e)[0]
        projected = [(p['geometry']['minM'][axis], p['geometry']['maxM'][axis]) for p in hits]
        target = e['body']
        nominal = [round(e[k] * 100, 6) for k in ('BM', 'HM')]
        mismatches = [p['sectionCm'] for p in hits
                      if any(abs(a - b) > TOL * 100 for a, b in zip(p['sectionCm'], nominal))]
        results.append(dict(
            id=e['Id'], mark=e['Mark'], kind=e['Kind'], inputLevel=e['level'],
            parts=[p['guid'] for p in hits], sourceNominalSectionCm=nominal,
            sourceBoundingBoxM=target,
            beamTopNominalM=e['AxisM'][2] if e['Kind'] == 'beam' else None,
            receiverSectionsDifferingFromNominalCm=mismatches,
            axialCoverageOfInputBoundingBox=coverage(
                projected, target['min'][axis], target['max'][axis], TOL),
        ))
    return results


def main():
    dwgs = {level: SOURCE / f'R225-CAD-{level}-COORDENACAO-NAO-EXECUTAR.dwg' for level in LEVELS}
    rvt = SOURCE / 'H03-R225-REVIT-COORDENACAO-NAO-EXECUTAR.rvt'
    native = SOURCE / 'R225-exportacao-ifc.json'
    input_audit = SOURCE / 'R225-IFC-auditoria.json'
    timings = {mode: RESULT / f'R228-{mode}-tempo-observado.json' for mode in ('CAD', 'BIM')}
    input_files = [rvt, SOURCE_IFC, native, input_audit, *dwgs.values()]
    observed = [*input_files, *MODELS.values(), REPORT, project_file(BIM), project_file(CAD),
                *timings.values()]
    hashes = {p: sha(p) for p in observed}
    manifest = {r['path']: r['sha256'] for r in read(SOURCE / 'R225-manifesto-final.json')['files']}
    if any(hashes[p] != manifest[p.name] for p in input_files):
        raise ValueError('O insumo R225 diverge da versão congelada')

    source, bim, cad = map(read_model, (SOURCE_IFC, MODELS[BIM], MODELS[CAD]))
    bodies = {r['nativeId']: r['bodyBoundsM'] for r in read(input_audit)['elements']}
    source_objects = {o.Tag: o for cls in CLASSES.values() for o in source.by_type(cls)}
    origins = [dict(e, body=bodies[str(e['Id'])], level=level_of(source_objects[str(e['Id'])]))
               for e in read(native)['Readback']['Elements'] if e['Kind'] in CLASSES]
    rows = parse_report(REPORT)
    expected = Counter((str(e['Id']), GROUPS[e['Kind']], e['level']) for e in origins)
    observed_rows = Counter((r['revId'], r['group'], r['level']) for r in rows)
    if expected != observed_rows:
        raise ValueError(f'Identidades, tipos ou níveis divergentes: {expected - observed_rows}, '
                         f'{observed_rows - expected}')

    parts = collect_parts(bim, origins)
    geometry = compare_origins(origins, parts)
    drawings = {level: RESULT / f'R228-CAD-reaberto-{level}.png' for level in LEVELS}
    if not all(p.is_file() for p in drawings.values()) or counts(cad):
        raise ValueError('Evidência CAD divergente da recepção como desenhos de referência')
    if hashes != {p: sha(p) for p in observed}:
        raise ValueError('Arquivo alterado durante a auditoria')

    result = dict(
        revision='H03/R228', sourceRevision='H03/R225', sourceCounts=counts(source),
        sourceStoreysM=storeys(source), bimControlStoreysM=storeys(bim),
        bimControlCounts=counts(bim), cadControlCounts=counts(cad),
        cadReferenceLevelsCm=LEVELS, cadReferenceReopenEvidence={k: p.name for k, p in drawings.items()},
        timings={k: read(p) for k, p in timings.items()}, fullFlowTimesMeasured=False,
        matchedScopeBetweenTimers=False, nativeReportCounts=dict(Counter(r['group'] for r in rows)),
        reportIdsClassesAndSourceLevelsMatch=True, reportRows=rows,
        uniquePartMatches=dict(Counter(p['kind'] for p in parts if len(p['candidates']) == 1)),
        originsWithNominalSectionDifferences=[r['mark'] for r in geometry
                                              if r['receiverSectionsDifferingFromNominalCm']],
        originsWithProjectionGaps=[r['mark'] for r in geometry
                                   if not r['axialCoverageOfInputBoundingBox']['noGapAboveTolerance']],
        columnShortSegmentsUpTo5Cm=sum(
            p['kind'] == 'column' and p['geometry']['maxM'][2] - p['geometry']['minM'][2] <= .05 + TOL
            for p in parts),
        concreteCoverExposureTuples=[dict(values=list(k), parts=n) for k, n in Counter(
            (p['concreteClass'], p['coverCm'], p['exposureClass']) for p in parts).items()],
        materialAssociationsInBimControl=sum(bool(p['materialNames']) for p in parts),
        bimControlPartsWithMaterialPropertySets=sum(bool(p['materialPropertySets']) for p in parts),
        bimCriteriaCopiedFromLastProject='CAD R227', cadCriteriaCopiedFromLastProject='BIM R228',
        materialTransferIsolated=False, analyticalConnectivityVerified=False,
        rawModelsRecalculated=False, structuralApproval=False, comparisonToleranceM=TOL,
        hashes={p.relative_to(OUT).as_posix(): value for p, value in hashes.items()},
        origins=geometry, parts=parts,
    )
    (RESULT / 'R228-auditoria.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n',
                                              encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('hashes', 'parts', 'origins', 'reportRows')}, ensure_ascii=False))


if __name__ == '__main__':
    main()

"""Compara os IFCs de controle do Eberick antes e depois de normalizar níveis."""
from collections import Counter
import json
from pathlib import Path
import sys

from preparar_niveis import INPUT, OUT, SOURCE, TARGET

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'h03-r228'))
from auditar_par import (CLASSES, GROUPS, RESULT, TOL, collect_parts, compare_origins,
                         counts, level_of, parse_report, project_file, read, read_model, sha, storeys)


def main():
    baseline_path = RESULT / 'R228-auditoria.json'
    prep_path = OUT / 'R229-preparacao.json'
    project = OUT / 'R229-BIM-QUATRO-NIVEIS-NAO-EXECUTAR'
    control = project / 'Arquivos do projeto/Modelo 3D.IFC'
    report = project / 'Arquivos do projeto/Documentos/Eberick/Relatorio_de_importacao_de_elementos_IFC.docx'
    timing = OUT / 'R229-tempo-observado.json'
    paths = (INPUT, TARGET, project_file(project), control, report, timing, prep_path, baseline_path)
    before = {p: sha(p) for p in paths}
    baseline = read(baseline_path)
    prep = read(prep_path)
    if before[INPUT] != prep['sourceSha256'] or before[TARGET] != prep['derivedSha256']:
        raise ValueError('Hash do IFC de entrada divergente')
    for relative, digest in baseline['hashes'].items():
        if sha(RESULT.parent / relative) != digest:
            raise ValueError(f'Controle R228 alterado: {relative}')
    source = read_model(TARGET)
    received = read_model(control)
    source_objects = {obj.Tag: obj for cls in CLASSES.values() for obj in source.by_type(cls)}
    bodies = {r['nativeId']: r['bodyBoundsM'] for r in read(SOURCE / 'R225-IFC-auditoria.json')['elements']}
    origins = [dict(e, body=bodies[str(e['Id'])], level=level_of(source_objects[str(e['Id'])]))
               for e in read(SOURCE / 'R225-exportacao-ifc.json')['Readback']['Elements']
               if e['Kind'] in CLASSES]
    rows = parse_report(report)
    expected = Counter((str(e['Id']), GROUPS[e['Kind']], e['level']) for e in origins)
    observed = Counter((r['revId'], r['group'], r['level']) for r in rows)
    if expected != observed:
        raise ValueError(f'Diferenças no relatório: {expected - observed}, {observed - expected}')
    parts = collect_parts(received, origins)
    geometry = compare_origins(origins, parts)
    short = [p['guid'] for p in parts if p['kind'] == 'column'
             and p['geometry']['maxM'][2] - p['geometry']['minM'][2] <= .05 + TOL]
    bad = [r['mark'] for r in geometry if r['receiverSectionsDifferingFromNominalCm']]
    gaps = [r['mark'] for r in geometry if not r['axialCoverageOfInputBoundingBox']['noGapAboveTolerance']]
    native_reopened = (OUT / 'R229-reaberto.png').is_file()
    if before != {p: sha(p) for p in paths} or not native_reopened:
        raise ValueError('Conferência sem reabertura documentada ou arquivo alterado')
    result = dict(
        revision='H03/R229', preparation=prep, eberickReceptionVerified=True,
        nativeReopened=native_reopened, receptionTiming=read(timing),
        criteria='Configuração do último projeto aberto, CAD R227',
        reportIdsClassesAndSourceLevelsMatch=True, reportCounts=dict(Counter(r['group'] for r in rows)),
        inputStoreysM=storeys(source), controlStoreysM=storeys(received),
        controlCountsBefore=baseline['bimControlCounts'], controlCountsAfter=counts(received),
        shortColumnPartsBefore=baseline['columnShortSegmentsUpTo5Cm'], shortColumnPartsAfter=len(short),
        sectionDifferenceMarksBefore=baseline['originsWithNominalSectionDifferences'],
        sectionDifferenceMarksAfter=bad, axialBoxGapsBefore=baseline['originsWithProjectionGaps'],
        axialBoxGapsAfter=gaps,
        uniquePartMatches=dict(Counter(p['kind'] for p in parts if len(p['candidates']) == 1)),
        controlCoverAndConcrete=[dict(values=list(k), parts=n) for k, n in Counter(
            (p['concreteClass'], p['coverCm'], p['exposureClass']) for p in parts).items()],
        originalR225AndReceiversR228Unchanged=True, structuralConnectivityVerified=False,
        structuralApproval=False, fullBimFlowTimeMeasured=False,
        hashes={p.relative_to(OUT.parent).as_posix(): h for p, h in before.items()},
        origins=geometry, parts=parts,
    )
    (OUT / 'R229-auditoria.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n',
                                             encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('origins', 'parts', 'preparation', 'hashes')}, ensure_ascii=False))


if __name__ == '__main__':
    main()

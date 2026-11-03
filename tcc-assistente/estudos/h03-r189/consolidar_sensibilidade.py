"""Consolida ensaio nativo unilateral; nao promove a hipotese a apoio fisico."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys
import zipfile

HERE = Path(__file__).resolve().parent
OUT = Path('D:/TCC/outputs/Escada-H03-R189-SENSIBILIDADE-APOIO-NAO-EXECUTAR')
sys.path.insert(0, str(HERE.parent / 'h03-r182'))
from consolidar_diagnostico import text_docx, parse_report


def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))


def write(p, data):
    Path(p).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    prep = read(OUT / 'R189-preparacao.json')
    if sha(prep['sourceProjectPath']) != prep['sourceProjectSha256']:
        raise ValueError('Controle R188 CAD alterado')
    prj = Path(prep['projectPath'])
    if sha(prj) == prep['sourceProjectSha256']:
        raise ValueError('Copia experimental nao gravada')
    with zipfile.ZipFile(prj) as z:
        if z.testzip():
            raise ValueError('PRJ experimental corrompido')
    for name, expected in [('CAD-barra-antes-AX.txt', '0'),
                           ('CAD-barra-20cm-retido-AX.txt', '20'),
                           ('CAD-barra-poscalculo-AX.txt', '20')]:
        if f'Largura Value: {expected} ID: 803' not in (OUT / name).read_text(encoding='utf-8'):
            raise ValueError('Largura nao confirmada: ' + name)
    ax = (OUT / 'CAD-LE3-A11-AX.txt').read_text(encoding='utf-8')
    if ax.count('Erro A11 - Largura do apoio insuficiente.') != 5:
        raise ValueError('Faltam resultados por bitola')
    if 'Laje LE3 Erro D31' not in ax:
        raise ValueError('D31 de LE3 nao confirmado')
    if 'Estrutura processada com avisos' not in (OUT / 'CAD-processamento-concluido-AX.txt').read_text(encoding='utf-8'):
        raise ValueError('Conclusao do processamento nao confirmada')
    report_path = OUT / 'CAD-mensagens.docx'
    report = parse_report(text_docx(report_path))
    timing = read(OUT / 'CAD-tempo-observado.json')
    elapsed = (datetime.fromisoformat(timing['firstCompletionScreenshotConfirmedAtUtc']) -
               datetime.fromisoformat(timing['startedAtUtc'])).total_seconds()
    refs = read(HERE.parent / 'h03-r183/R183-inicio.json')['sourceProjects']
    for ref in refs.values():
        if sha(ref['path']) != ref['sha256']:
            raise ValueError('Controle R182 alterado')
    result = dict(revision='H03/R189', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        branch='CAD', experimentalProjectPath=str(prj), experimentalProjectSha256=sha(prj),
        experimentalProjectZipValid=True, sourceProjectPath=prep['sourceProjectPath'],
        sourceProjectSha256=prep['sourceProjectSha256'], sourceProjectUnchanged=True,
        R182ReferenceProjectHashesPreserved=True,
        intervention=dict(applied=True, target='Barra ordinaria horizontal do bordo inferior de LE3 no N0',
            initialWidthCm=0, experimentalWidthCm=20, retainedAfterRecalculation=True,
            inheritedAnchorageCriterion='gancho no controle R188',
            newPhysicalMemberDefined=False, foundationDesigned=False,
            supportingMemberCapacityVerified=False),
        reportPath=str(report_path), reportSha256=sha(report_path), nativeReport=report,
        stairsPositiveTable=dict(LE1='calculado', LE2='calculado', LE3='D31'),
        LE3DiameterErrors={str(d): 'A11' for d in (6.3, 8.0, 10.0, 12.5, 16.0)},
        supplementalVisualReadings=dict(source='CAD-LE3-secao-0.png / CAD-LE3-esforcos-0.png',
            method='Transcricao visual da planilha nativa, sem OCR',
            LE3=dict(waistCm=14, type='Fundo plano', treadCm=28, riserDisplayedCm=17.82,
                MdxKnMPerM=5.46, MdyKnMPerM=1.91, NdxKn=87.97, RdxKn=-1.71,
                displayedDeflectionCm=-0.05),
            displayedDeflectionIsNotACompletedSlabELSCheck=True,
            localXMappingToGlobalCoordinatesNotYetVerified=True),
        observedTiming=dict(**timing, elapsedSeconds=elapsed,
            includesToolObservationAndConfirmationLatency=True,
            completionTimestampRecordedAfterReviewingReturnedScreenshot=True,
            isNativeProcessingTime=False, isActiveWorkTime=False, completeFlowMeasured=False),
        interpretation='A largura hipotetica de 20 cm dessa barra, isoladamente, nao eliminou D31/A11. O ensaio nao identifica qual bordo governa e nao comprova uma solucao fisica de apoio.',
        comparisonIsPaired=False, BIMReplicatePerformed=False,
        freshGeometryAndLoadExportAudited=False, allStructuralElementsSuccessfullyDesigned=False,
        thresholdsRaisedToSuppressError=False, structuralApproval=False,
        fullPairedFlowComparisonFinished=False, wholeFlowProductivityRankingPermitted=False)
    write(OUT / 'R189-sensibilidade-barra.json', result)
    pointer = Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    if not (OUT / 'R189-ponteiro-anterior.json').exists():
        shutil.copy2(pointer, OUT / 'R189-ponteiro-anterior.json')
    current = read(pointer)
    current.update(latestSupportWidthExperimentRevision='H03/R189',
        latestSupportWidthExperimentPath=str(OUT / 'R189-sensibilidade-barra.json'),
        latestSupportWidthExperimentSha256=sha(OUT / 'R189-sensibilidade-barra.json'),
        lowerLE3Bar20CmAloneResolvesA11=False,
        allStructuralElementsSuccessfullyDesigned=False)
    write(pointer, current)
    write(OUT / 'R189-ponteiro-atualizado.json', current)
    for p in OUT.iterdir():
        if p.is_file() and (p.name.startswith('CAD-') or p.name in (
                'R189-preparacao.json', 'R189-sensibilidade-barra.json', 'R189-ponteiro-atualizado.json')):
            shutil.copy2(p, HERE / p.name)
    shutil.copy2(HERE / 'LEIA-ME-R189.md', OUT / 'LEIA-ME-R189.md')
    files = [p for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'R189-manifesto.json']
    manifest = dict(revision='H03/R189', files=[dict(relativePath=p.name,
        bytes=p.stat().st_size, sha256=sha(p)) for p in files])
    write(HERE / 'R189-manifesto.json', manifest)
    shutil.copy2(HERE / 'R189-manifesto.json', OUT / 'R189-manifesto.json')
    print(json.dumps(dict(evidenceFiles=len(files), nativeTotalSeconds=report['nativeTotalSeconds'],
        LE3='D31/A11', observedSeconds=elapsed, referencesPreserved=True)))


if __name__ == '__main__':
    main()

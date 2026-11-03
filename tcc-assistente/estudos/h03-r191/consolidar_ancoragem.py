"""Consolida evidencia nativa do ensaio CAD; nao constitui aprovacao estrutural."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys
import zipfile

HERE = Path(__file__).resolve().parent
OUT = Path('D:/TCC/outputs/Escada-H03-R191-ANCORAGEM-ADJACENTE-NAO-EXECUTAR')
sys.path.insert(0, str(HERE.parent / 'h03-r182'))
from consolidar_diagnostico import parse_report, text_docx


def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))


def write(p, value):
    Path(p).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    prep = read(OUT / 'R191-preparacao.json')
    assert sha(prep['sourceProjectPath']) == prep['sourceProjectSha256'], 'Fonte R189 alterada'
    prj = Path(prep['projectPath'])
    assert sha(prj) == '3df555df637fad8e4754711baff22a978ebb5dca8197107bbdb5a2983bd85d48', 'Arquivo salvo mudou'
    with zipfile.ZipFile(prj) as z:
        assert z.testzip() is None, 'PRJ com CRC invalido'
    for ref in read(HERE.parent / 'h03-r183/R183-inicio.json')['sourceProjects'].values():
        assert sha(ref['path']) == ref['sha256'], 'Controle R182 alterado'
    stages = {}
    for stage in ('controle', 'ensaio'):
        ax = (OUT / f'CAD-{stage}-LE3-A11-AX.txt').read_text(encoding='utf-8')
        assert ax.count('Erro A11 - Largura do apoio insuficiente.') == 5
        assert 'Laje LE3 Erro D31' in ax
        assert 'Estrutura processada com avisos' in (OUT / f'CAD-{stage}-fim-AX.txt').read_text(encoding='utf-8')
        report_file = OUT / f'CAD-{stage}-mensagens.docx'
        report = parse_report(text_docx(report_file))
        timing = read(OUT / f'CAD-{stage}-tempo.json')
        elapsed = (datetime.fromisoformat(timing['firstConfirmedUtc']) - datetime.fromisoformat(timing['startUtc'])).total_seconds()
        stages[stage] = dict(reportSha256=sha(report_file), nativeReport=report,
            observedTiming=dict(**timing, elapsedSeconds=elapsed,
                includesObservationLatency=True, isActiveWorkTime=False, completeFlowMeasured=False),
            LE3='D31/A11', failingDiametersMm=[6.3, 8, 10, 12.5, 16])
    ax = (OUT / 'CAD-LE3-reaberto-AX.txt').read_text(encoding='utf-8')
    assert ax.count('Erro A11 - Largura do apoio insuficiente.') == 5
    stale = OUT / 'CAD-controle-apos-integridade.prj'
    assert sha(stale) == prep['initialProjectSha256']
    result = dict(revision='H03/R191', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        branch='CAD', projectPath=str(prj), projectSha256=sha(prj), zipCrcValid=True,
        sourceProjectUnchanged=True, R182ControlHashesPreserved=True,
        intervention=dict(adjacentSlabAnchorageEnabled=True, retainedAfterSaveAndReopen=True,
            stateEvidence='Capturas CAD-ancoragem-adjacente-confirmada-2.png e CAD-ancoragem-adjacente-reaberto-1.png; AX nao informa estado do checkbox',
            inheritedLowerOrdinaryBarHypotheticalWidthCm=20, inheritedAnchorage='gancho',
            geometryEdited=False, newPhysicalColumns=False, supportingConcreteDetailVerified=False,
            thresholdsRaisedToSuppressError=False),
        integrity=dict(openingWarningObserved=True, nativeVerificationPerformed=True,
            recalculatedBeforeIntervention=True, nativeControlSaveConfirmed=False,
            excludedStaleControlCopy=str(stale), excludedStaleCopySha256=sha(stale),
            staleCopyExplanation='Ctrl+S nao persistiu o controle recalculado. A copia tem bytes da fonte R189; nao e prova de salvamento do controle. Relatorio e AX registram o controle efetivamente processado.',
            finalSaveMethod='Botao de disco, alteracao de hash e reabertura conferidas'),
        stages=stages, nativeReportsEqual=stages['controle']['nativeReport']==stages['ensaio']['nativeReport'],
        LE3ErrorRetainedAfterReopen=True, LE3A11Resolved=False,
        interpretation='Habilitar ancoragem adjacente nesta configuracao nao eliminou D31/A11. Nao identifica o bordo governante nem valida a ancoragem fisica.',
        inheritedShearCheckWaiverRequiresReview=True, BIMReplicatePerformed=False,
        freshGeometryAndLoadExportAudited=False, fullAnalyticalEquivalenceVerified=False,
        allStructuralElementsSuccessfullyDesigned=False, structuralApproval=False,
        fullPairedFlowComparisonFinished=False, wholeFlowProductivityRankingPermitted=False)
    write(OUT / 'R191-resultado.json', result)
    pointer = Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    if not (OUT / 'R191-ponteiro-anterior.json').exists():
        shutil.copy2(pointer, OUT / 'R191-ponteiro-anterior.json')
    current = read(pointer)
    current.update(latestAdjacentAnchorageExperimentRevision='H03/R191',
        latestAdjacentAnchorageExperimentPath=str(OUT / 'R191-resultado.json'),
        adjacentAnchorageExperimentResolvesA11=False, allStructuralElementsSuccessfullyDesigned=False)
    write(pointer, current)
    write(OUT / 'R191-ponteiro-atualizado.json', current)
    excluded = {'CAD-controle-gravacao.json', 'CAD-reabertura-AX.txt'}
    for p in OUT.iterdir():
        if p.is_file() and p.suffix != '.prj' and p.name not in excluded and (
                p.name.startswith('CAD-') or p.name in ('R191-preparacao.json', 'R191-resultado.json', 'R191-ponteiro-atualizado.json')):
            shutil.copy2(p, HERE / p.name)
    shutil.copy2(HERE / 'LEIA-ME-R191.md', OUT / 'LEIA-ME-R191.md')
    files = [p for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'R191-manifesto.json']
    manifest = dict(revision='H03/R191', files=[dict(relativePath=p.name, bytes=p.stat().st_size, sha256=sha(p)) for p in files])
    write(HERE / 'R191-manifesto.json', manifest)
    shutil.copy2(HERE / 'R191-manifesto.json', OUT / 'R191-manifesto.json')
    print(json.dumps(dict(files=len(files), nativeSeconds=[v['nativeReport']['nativeTotalSeconds'] for v in stages.values()],
        observedSeconds=[v['observedTiming']['elapsedSeconds'] for v in stages.values()], LE3='D31/A11', referencesPreserved=True)))


if __name__ == '__main__':
    main()

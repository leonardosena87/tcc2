"""Audita o ensaio nativo R192 sem promover a copia a projeto aprovado."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys
import zipfile

HERE = Path(__file__).resolve().parent
OUT = Path('D:/TCC/outputs/Escada-H03-R192-ENCONTRO-PATAMAR-NAO-EXECUTAR')
sys.path.insert(0, str(HERE.parent / 'h03-r182'))
from consolidar_diagnostico import parse_report, text_docx


def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))


def write(p, value):
    Path(p).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    prep = read(OUT / 'R192-preparacao.json')
    assert sha(prep['sourceProjectPath']) == prep['sourceProjectSha256'], 'Fonte R191 alterada'
    prj = Path(prep['projectPath'])
    assert sha(prj) == 'f99b160413d4fb2416df7ec9a66ef5c810a44cfe62638c940c849113de74ce83'
    control = OUT / 'CAD-controle-recalculado.prj'
    assert sha(control) == read(OUT / 'CAD-controle-gravacao.json')['sha256']
    assert sha(control) != prep['initialProjectSha256']
    for path in (prj, control):
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None
    for ref in read(HERE.parent / 'h03-r183/R183-inicio.json')['sourceProjects'].values():
        assert sha(ref['path']) == ref['sha256'], 'Controle R182 alterado'
    for file, expected in [('CAD-barra-encontro-antes-AX.txt', '0'),
                           ('CAD-barra-encontro-20cm-AX.txt', '20'),
                           ('CAD-barra-encontro-poscalculo-AX.txt', '20')]:
        assert f'Largura Value: {expected} ID:' in (OUT / file).read_text(encoding='utf-8')
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
    assert [s['nativeReport']['nativeTotalSeconds'] for s in stages.values()] == [6, 7]
    assert stages['controle']['nativeReport']['levels'] == stages['ensaio']['nativeReport']['levels']
    result = dict(revision='H03/R192', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        branch='CAD', projectPath=str(prj), projectSha256=sha(prj), zipCrcValid=True,
        sourceProjectUnchanged=True, R182ControlHashesPreserved=True,
        intervention=dict(upperOrdinaryBarAtLE3LE1WidthBeforeCm=0, upperOrdinaryBarWidthAfterCm=20,
            widthConfirmedAfterProcessing=True, savedProjectHashChanged=True,
            postReopenVerificationPerformed=False, inheritedLowerOrdinaryBarHypotheticalWidthCm=20,
            inheritedAnchorage='gancho', inheritedAdjacentSlabAnchorageEnabled=True,
            newPhysicalBeam=False, newPhysicalColumns=False, supportingConcreteDetailVerified=False,
            thresholdsRaisedToSuppressError=False),
        integrity=dict(openingWarningObserved=True, nativeVerificationPerformed=True,
            recalculatedBeforeIntervention=True, savedRecalculatedControlSha256=sha(control),
            savedRecalculatedControlPath=str(control), finalSaveMethod='Botao de disco; hash alterado'),
        stages=stages, reportedCategoryCountsEqual=True, LE3A11Resolved=False,
        displayedLE3Summary=dict(Mdx_kNmPerM=5.46, Mdy_kNmPerM=1.91, Ndx_kN=87.97,
            Rdx_kN=-1.71, maxDeflectionCm=-0.05, evidence='CAD-ensaio-esforcos.png',
            isIdentificationOfGoverningSupport=False, isCompleteELSVerification=False),
        interpretation='A largura hipotetica de 20 cm no encontro LE3/LE1 nao eliminou D31/A11 nesta configuracao. O bordo governante e o comprimento fisico de ancoragem continuam por determinar.',
        inheritedShearCheckWaiverRequiresReview=True, BIMReplicatePerformed=False,
        freshGeometryAndLoadExportAudited=False, fullAnalyticalEquivalenceVerified=False,
        allStructuralElementsSuccessfullyDesigned=False, structuralApproval=False,
        fullPairedFlowComparisonFinished=False, wholeFlowProductivityRankingPermitted=False)
    write(OUT / 'R192-resultado.json', result)
    pointer = Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    if not (OUT / 'R192-ponteiro-anterior.json').exists():
        shutil.copy2(pointer, OUT / 'R192-ponteiro-anterior.json')
    current = read(pointer)
    current.update(latestLandingEncounterWidthExperimentRevision='H03/R192',
        latestLandingEncounterWidthExperimentPath=str(OUT / 'R192-resultado.json'),
        landingEncounter20CmResolvesA11=False, allStructuralElementsSuccessfullyDesigned=False)
    write(pointer, current)
    write(OUT / 'R192-ponteiro-atualizado.json', current)
    for p in OUT.iterdir():
        if p.is_file() and p.suffix != '.prj' and (p.name.startswith('CAD-') or p.name in (
                'R192-preparacao.json', 'R192-resultado.json', 'R192-ponteiro-atualizado.json')):
            shutil.copy2(p, HERE / p.name)
    shutil.copy2(HERE / 'LEIA-ME-R192.md', OUT / 'LEIA-ME-R192.md')
    files = [p for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'R192-manifesto.json']
    manifest = dict(revision='H03/R192', files=[dict(relativePath=p.name, bytes=p.stat().st_size, sha256=sha(p)) for p in files])
    write(HERE / 'R192-manifesto.json', manifest)
    shutil.copy2(HERE / 'R192-manifesto.json', OUT / 'R192-manifesto.json')
    print(json.dumps(dict(files=len(files), nativeSeconds=[v['nativeReport']['nativeTotalSeconds'] for v in stages.values()],
        observedSeconds=[v['observedTiming']['elapsedSeconds'] for v in stages.values()], LE3='D31/A11', referencesPreserved=True)))


if __name__ == '__main__':
    main()

"""Consolida o ensaio nativo de agrupamento, sem declarar causalidade integral."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys
import zipfile

HERE = Path(__file__).resolve().parent
OUT = Path('D:/TCC/outputs/Comparacao-H03-R187-CONTINUIDADE-V2-NAO-EXECUTAR')
sys.path.insert(0, str(HERE.parent / 'h03-r182'))
from consolidar_diagnostico import text_docx, parse_report
sys.path.insert(0, str(HERE.parent / 'h03-r186'))
from consolidar_leitura import compare_displayed


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    prep = read(OUT / 'R187-preparacao.json')
    refs = read(HERE.parent / 'h03-r183/R183-inicio.json')['sourceProjects']
    preserved = {}
    for branch, ref in refs.items():
        current = sha(ref['path'])
        if current != ref['sha256']:
            raise ValueError('Projeto de referencia alterado: ' + branch)
        preserved[branch] = dict(path=ref['path'], sha256=current, unchanged=True)
    native = Path(prep['projectPath'])
    with zipfile.ZipFile(native) as z:
        if z.testzip():
            raise ValueError('PRJ experimental corrompido')
    if sha(native) == prep['sourceProject']['sha256']:
        raise ValueError('Copia experimental ainda identica a fonte')
    report = OUT / 'CAD-mensagens.docx'
    text = text_docx(report)
    parsed = parse_report(text)
    (OUT / 'CAD-mensagens.txt').write_text(text, encoding='utf-8')
    if parsed['levels']['N1']['reportedCategories']['Vigas'] != dict(reportedSuccess=14, reportedError=1):
        raise ValueError('Contagem nativa diferente da observada')
    obs = read(HERE / 'observacoes.json')
    baseline = read(HERE.parent / 'h03-r186/observacoes.json')
    comparisons = []
    for old_name, new_span in [('V2', 'span1'), ('V14', 'span2')]:
        comparisons.append(dict(baselineGroup=old_name, experimentalSpan=new_span,
            **compare_displayed(baseline['CAD'][old_name]['envelope'], obs['V2'][new_span], False)))
    if obs['V2']['sectionsCmInNativeOrder'] != [baseline['CAD']['V2']['sectionCm'], baseline['CAD']['V14']['sectionCm']]:
        raise ValueError('Secoes diferentes da referencia')
    ax = (OUT / 'CAD-V2-A07-AX.txt').read_text(encoding='utf-8')
    if 'Erro D16 - Erro na armadura negativa (nó 2)' not in ax or ax.count('Erro A07') != 5:
        raise ValueError('Diagnostico D16/A07 nao sustentado pela leitura nativa')
    timing = read(OUT / 'R187-tempo-observado.json')
    start = datetime.fromisoformat(timing['startUtc'])
    end = datetime.fromisoformat(timing['firstConfirmedUtc'])
    if abs((end - start).total_seconds() - timing['elapsedSeconds']) > 0.0001:
        raise ValueError('Intervalo observado inconsistente')
    result = dict(revision='H03/R187', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        referenceProjects=preserved, experimentalProjectPath=str(native), experimentalProjectSha256=sha(native),
        preparationPath=str(OUT / 'R187-preparacao.json'), nativeIntegrityCheckOnOpening=True,
        reportPath=str(report), reportSha256=sha(report), nativeReport=parsed,
        observationPath=str(HERE / 'observacoes.json'), observationSha256=sha(HERE / 'observacoes.json'),
        displayedEnvelopeComparisons=comparisons,
        displayedEnvelopeScalarsUnchanged=10 if all(x['equalAtDisplayedPrecision'] for x in comparisons) else None,
        sectionsRetainedAtDisplayedPrecision=True, nativeErrorReproduced='V2 N1 D16 / A07 no 2',
        stairLE3StillD31=True, sourceR182CADGroupsN1=16, experimentalCADGroupsN1=15,
        baselineBIMGroupsN1=12, onlyOneCADGroupPairTested=True,
        timing=dict(nativeTotalSeconds=parsed['nativeTotalSeconds'],
            nativeDimensioningSecondsIncludedInTotal=parsed['nativeDimensioningSeconds'],
            observedInterval=timing, completeFlowMeasured=False, wholeFlowRankingPermitted=False),
        interpretation='O erro D16/A07 tambem aparece no CAD ao agrupar V2/V14. Sustenta a influencia do agrupamento neste caso, sem provar identidade integral dos modelos ou a causa interna do dimensionador.',
        freshGeometryAndLoadExportsAvailable=False, fullAnalyticalEquivalenceVerified=False,
        directComparisonOfRawBeamErrorRatesValid=False, structuralApproval=False)
    write(OUT / 'R187-ensaio-continuidade.json', result)
    pointer = Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    old_pointer = OUT / 'R187-ponteiro-anterior.json'
    if not old_pointer.exists():
        shutil.copy2(pointer, old_pointer)
    current = read(pointer)
    current.update(latestBeamGroupingExperimentRevision='H03/R187',
        latestBeamGroupingExperimentPath=str(OUT / 'R187-ensaio-continuidade.json'),
        latestBeamGroupingExperimentSha256=sha(OUT / 'R187-ensaio-continuidade.json'),
        CADUnifiedV2AlsoHasD16A07=True, fullPairedFlowComparisonFinished=False,
        allStructuralElementsSuccessfullyDesigned=False)
    write(pointer, current)
    write(OUT / 'R187-ponteiro-atualizado.json', current)
    selected = ['R187-preparacao.json', 'R187-ensaio-continuidade.json', 'R187-ponteiro-atualizado.json',
        'R187-tempo-observado.json', 'CAD-mensagens.docx', 'CAD-mensagens.txt',
        'CAD-processamento-AX.txt', 'CAD-resumo-AX.txt', 'CAD-V2-A07-AX.txt']
    selected += [p.name for p in OUT.glob('CAD-*-0.png')]
    for name in selected:
        shutil.copy2(OUT / name, HERE / name)
    for name in ('LEIA-ME-R187.md', 'observacoes.json'):
        shutil.copy2(HERE / name, OUT / name)
    files = [p for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'R187-manifesto.json']
    manifest = dict(revision='H03/R187', files=[dict(relativePath=p.name,
        bytes=p.stat().st_size, sha256=sha(p)) for p in files])
    write(HERE / 'R187-manifesto.json', manifest)
    shutil.copy2(HERE / 'R187-manifesto.json', OUT / 'R187-manifesto.json')
    print(json.dumps(dict(evidenceFiles=len(files), CADV2='D16/A07',
        unchangedDisplayedEnvelopeScalars=result['displayedEnvelopeScalarsUnchanged'],
        nativeSeconds=parsed['nativeTotalSeconds'], sourceProjectHashesPreserved=True)))


if __name__ == '__main__':
    main()

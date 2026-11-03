"""Registra o controle real e a alternativa de gancho ainda nao executada."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys
import zipfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'h03-r182'))
from consolidar_diagnostico import text_docx, parse_report

OUT = Path('D:/TCC/outputs/Escada-H03-R184-ENSAIO-GANCHO-NAO-EXECUTAR')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    prep = json.loads((OUT / 'R184-preparacao.json').read_text(encoding='utf-8'))
    refs = json.loads(Path('D:/TCC/outputs/Escada-H03-R183-LEITURA-APOIOS-NAO-EXECUTAR/R183-inicio.json').read_text(encoding='utf-8'))
    for b, ref in refs['sourceProjects'].items():
        if sha(ref['path']) != ref['sha256']:
            raise ValueError('PRJ de referencia alterado: ' + b)
    report = OUT / 'CAD-controle-reta-mensagens.docx'
    text = text_docx(report)
    parsed = parse_report(text)
    (OUT / 'CAD-controle-reta-mensagens.txt').write_text(text, encoding='utf-8')
    start = json.loads((OUT / 'CAD-controle-reta-inicio.json').read_text(encoding='utf-8'))
    end = json.loads((OUT / 'CAD-controle-reta-fim.json').read_text(encoding='utf-8'))
    if 'Estrutura processada com avisos' not in end['state']:
        raise ValueError('Termino nativo nao confirmado')
    interval = (datetime.fromisoformat(end['observedAtUtc']) - datetime.fromisoformat(start['startedAtUtc'])).total_seconds()
    baseline = OUT / 'CAD-controle-reta.prj'
    for path in (baseline, Path(prep['branches']['CAD']['projectPath'])):
        with zipfile.ZipFile(path) as z:
            if z.testzip():
                raise ValueError('PRJ ilegivel: ' + str(path))
    untouched_bim = prep['branches']['BIM']
    if sha(untouched_bim['projectPath']) != untouched_bim['initialProjectSha256']:
        raise ValueError('Copia BIM deveria permanecer sem ensaio')
    result = dict(revision='H03/R184', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        sourceR182ProjectHashesPreserved=True,
        CAD=dict(nativeIntegrityCheckPerformed=True, baselineAnchorage='reta',
            reportPath=str(report), reportSha256=sha(report), nativeReport=parsed,
            baselineSavedProjectPath=str(baseline), baselineSavedProjectSha256=sha(baseline),
            currentExperimentalProjectPath=prep['branches']['CAD']['projectPath'],
            currentExperimentalProjectSha256=sha(prep['branches']['CAD']['projectPath']),
            LE1='calculado', LE2='calculado', LE3='D31 / A11',
            LE3TestedDiametersMm=[6.3, 8, 10, 12.5, 16],
            observedIntervalSeconds=interval, observedIntervalIncludesToolAndObservationLatency=True,
            accidentalLapOptionChangeDuringSelectionAttempt=True,
            lapOptionRestoredUncheckedBeforeLastSave=True,
            noReprocessingWithAccidentalLapOption=True,
            finalObservedAnchorage='reta', hookRecalculationExecuted=False),
        BIM=dict(projectPath=untouched_bim['projectPath'], copyUnchanged=True,
            nativeProcessingThisRevision=False, nativeSeconds=None, hookRecalculationExecuted=False),
        hookTestStatus='Pendente: a lista perdeu foco nas tentativas automaticas; nenhuma selecao de gancho confirmada',
        nativeFolderNameContainsIntendedTestNotProvenExecution=True,
        fullPairedTestCompleted=False, fullFlowMeasured=False, structuralApproval=False,
        sourceExportsAreInheritedNotFreshR184=True,
        timing=dict(CADNativeControlSeconds=parsed['nativeTotalSeconds'],
            CADNativeSizingSecondsIncluded=parsed['nativeDimensioningSeconds'],
            BIMNativeControlSeconds=None, hookTestSeconds=None, rankWholeFlows=False))
    write(OUT / 'R184-controle-e-pendencia.json', result)
    pointer = Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    if not (OUT / 'R184-ponteiro-anterior.json').exists():
        shutil.copy2(pointer, OUT / 'R184-ponteiro-anterior.json')
    current = json.loads(pointer.read_text(encoding='utf-8-sig'))
    current.update(latestAnchorageControlRevision='H03/R184',
        latestAnchorageControlPath=str(OUT / 'R184-controle-e-pendencia.json'),
        latestAnchorageControlSha256=sha(OUT / 'R184-controle-e-pendencia.json'),
        hookAnchorageTestCompleted=False, allStructuralElementsSuccessfullyDesigned=False)
    write(pointer, current)
    write(OUT / 'R184-ponteiro-atualizado.json', current)
    selected = ['R184-preparacao.json', 'R184-controle-e-pendencia.json', 'R184-ponteiro-atualizado.json',
        'CAD-controle-reta-mensagens.docx', 'CAD-controle-reta-mensagens.txt',
        'CAD-controle-reta-inicio.json', 'CAD-controle-reta-fim.json']
    selected += [p.name for p in OUT.glob('CAD-controle-reta-*-0.png')]
    selected += ['CAD-configuracao-restaurada-reta-0.png', 'CAD-aviso-abertura-0.png']
    for name in selected:
        shutil.copy2(OUT / name, HERE / name)
    shutil.copy2(HERE / 'LEIA-ME-R184.md', OUT / 'LEIA-ME-R184.md')
    files = [p for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'R184-manifesto.json']
    manifest = dict(revision='H03/R184', files=[dict(relativePath=p.name, bytes=p.stat().st_size,
        sha256=sha(p)) for p in files])
    write(HERE / 'R184-manifesto.json', manifest)
    shutil.copy2(HERE / 'R184-manifesto.json', OUT / 'R184-manifesto.json')
    print(json.dumps(dict(files=len(files), CADNativeSeconds=parsed['nativeTotalSeconds'], hookTestExecuted=False)))


if __name__ == '__main__':
    main()

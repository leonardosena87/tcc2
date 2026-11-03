from pathlib import Path
from datetime import datetime,timezone
import json,shutil
from consolidar_diagnostico import OUT,HERE,sha


def write(p,value):
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')


def main():
    result_path=OUT/'R182-diagnostico.json'
    r=json.loads(result_path.read_text(encoding='utf-8'))
    for b,entry in r['branches'].items():
        if sha(entry['projectPath'])!=entry['projectSha256']:
            raise ValueError('Projeto de diagnostico mudou: '+b)
    pointer=Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    backup=OUT/'R182-ponteiro-anterior.json'
    if not backup.exists():
        shutil.copy2(pointer,backup)
    current=json.loads(pointer.read_text(encoding='utf-8-sig'))
    current.update(latestNativeSuperstructureSizingDiagnosticRevision='H03/R182',
        latestNativeSuperstructureSizingDiagnosticPath=str(result_path),
        latestNativeSuperstructureSizingDiagnosticSha256=sha(result_path),
        latestNativeSizingDiagnosticProjectPaths={b:x['projectPath'] for b,x in r['branches'].items()},
        experimentalLowerStairFlightSizingErrorBothBranches='D31 / A11',
        experimentalBimV2SizingError='D16 / A07 no 2',
        diagnosticNativeProcessingSecondsEach={'CAD':7,'BIM':7},
        diagnosticNativeProcessingTimeIsNotFullFlowTime=True,
        allStructuralElementsSuccessfullyDesigned=False,fullPairedFlowComparisonFinished=False,
        fullAnalyticalEquivalenceVerified=False,finalReinforcementReviewed=False)
    write(pointer,current)
    shutil.copy2(pointer,OUT/'R182-ponteiro-atualizado.json')
    timings=dict(revision='H03/R182',recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        scope='Processamento ELU e dimensionamento selecionado da superestrutura; deslocamentos do portico com rigidez configurada',
        nativeProcessingSeconds={b:x['nativeDimensioningReport']['nativeTotalSeconds'] for b,x in r['branches'].items()},
        nativeSizingSecondsIncludedInProcessing={b:x['nativeDimensioningReport']['nativeDimensioningSeconds'] for b,x in r['branches'].items()},
        observedClickToFirstConfirmedCompletionSeconds={b:x['observedClickToFirstConfirmedCompletionSeconds'] for b,x in r['branches'].items()},
        observedIntervalsIncludeToolLatencyAndObservationDelay=True,observedIntervalsAreNotActiveWorkTimes=True,
        nativeProcessingSingleObservationEach=True,fullFlowMeasured=False,rankEntireWorkflows=False,
        historicalR178ObservationsNotReplaced=True,doNotAddNestedSizingToNativeTotal=True)
    write(OUT/'R182-tempos.json',timings)
    selected=['R182-preparacao.json','R182-diagnostico.json','R182-tempos.json','R182-ponteiro-atualizado.json']
    for b in ('CAD','BIM'):
        selected += [f'{b}-{s}' for s in ('mensagens-analise.docx','mensagens-analise.txt',
            'resultados-analise.txt','opcoes-analise-AX.txt','processamento-inicio.json',
            'processamento-primeira-observacao.json','processamento-observacao-final.json')]
    selected += [p.name for p in sorted(OUT.glob('*-0.png'))]
    for name in selected:
        shutil.copy2(OUT/name,HERE/name)
    shutil.copy2(HERE/'LEIA-ME-R182.md',OUT/'LEIA-ME-R182.md')
    files=[p for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='R182-manifesto.json']
    write(HERE/'R182-manifesto.json',dict(revision='H03/R182',files=[dict(relativePath=p.name,bytes=p.stat().st_size,sha256=sha(p)) for p in files]))
    shutil.copy2(HERE/'R182-manifesto.json',OUT/'R182-manifesto.json')
    print(json.dumps(dict(files=len(files),resultSha256=sha(result_path))))


if __name__=='__main__':
    main()

"""Registra a tentativa R98 interrompida sem promover o plano a carga aplicada."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
from conferir_qt import read, sha, build_plan, check_native


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,required=True)
    args=ap.parse_args()
    root=args.root
    target=root/'R98-estado-interrompido.json'
    if target.exists(): raise SystemExit('Registro existente; nao sobrescrever')
    prep=read(root/'R98-preparacao.json')
    studies=Path(__file__).resolve().parent.parent
    plan=build_plan(studies/'h03-r65/R65-plano-Q.json',studies/'h03-r64/R64-leituras-CAD.json',studies/'h03-r64/R64-leituras-BIM.json')
    rows=[]
    for b in prep['copies']:
        for f in b['sourceFiles']:
            source=Path(b['source'])/f['relativePath']
            copy=Path(b['copy'])/f['relativePath']
            actual=sha(source) if source.is_file() else None
            copied=sha(copy) if copy.is_file() else None
            rows.append(dict(branch=b['branch'],relativePath=f['relativePath'],
                             sourceSha256=actual,expectedSourceSha256=f['sha256'],
                             sourcePreserved=actual==f['sha256'],copySha256=copied,
                             copyMissing=not copy.is_file(),copyMatchesSourceSnapshot=copied==f['sha256']))
    if not all(r['sourcePreserved'] for r in rows):
        raise ValueError('Origem R97 mudou; investigar antes de consolidar')
    prjs=[r for r in rows if r['relativePath'].lower().endswith('.prj')]
    if len(prjs)!=2 or not all(r['copyMatchesSourceSnapshot'] for r in prjs):
        raise ValueError('PRJ R98 divergiu do cadastro R97; investigar')
    gfile=root/'BIM-RC01-G-antes-UI.txt'
    gtext=gfile.read_text(encoding='utf-8-sig')
    actual_g=check_native(gtext,plan['rows'][0],'G','BIM')
    try:
        check_native(gtext,plan['rows'][0],'QT','BIM')
    except ValueError as error:
        negative=dict(passed=True,reason=str(error),source=gfile.name,sha256=sha(gfile),
                      scope='Leitura real G deve ser recusada como evidencia QT; nao ensaio de QT inserida')
    else:
        raise ValueError('Auditor aceitou G como QT')
    result=dict(revision='H03/R98',recordedAtUtc=datetime.now(timezone.utc).isoformat(),
                status='interrompido_sem_QT_nativa_confirmada',
                sourceFilesChecked=len(rows),allR97SourceFilesPreserved=True,
                nativePRJsByteIdenticalToR97=True,fileChecks=rows,
                nativePreEditGRead=actual_g,nativePreEditGEvidence=dict(file=gfile.name,sha256=sha(gfile)),
                actualEvidenceNegativeControl=negative,
                qtZeroObservation=dict(branch='BIM',point='RC01',action='Q_TELHADO_MANUTENCAO',
                                       fzKN=0,source='Leitura da ferramenta get_window_state nesta sessao',
                                       rawAccessibilityFileSaved=False,
                                       status='Observacao anterior a tentativa, nao prova persistencia'),
                attemptedFzKN=-1.0725,successfulNativeFzEdits=0,
                savedQTLoadCount=0,qtPostReopenVerifiedCount=0,
                programReportedNotResponding=True,programWindowLaterAbsent=True,
                automatedRelaunchError='accessibility window-opened handler did not become ready',
                humanReopenRequested=True,humanActionConfirmed=False,
                completedStage=False,structuralProcessingPerformed=False,
                structuralApproval=False,sourceRvtDwgEdited=False,monographEdited=False,
                transferDefectProven=False,wholeFlowTotal=False,rankingAllowed=False,
                timing=read(root/'R98-tempo-BIM-interrompido.json'))
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('fileChecks','timing')},ensure_ascii=False))


if __name__=='__main__': main()

"""Preserva as evidências locais; interrompe se algum PRJ de controle divergir."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

EXPECTED={
    'CAD':'1bb22b8316417a11f53d9506483910593aad11f26d8db2548c72c969d651ca53',
    'BIM':'84ce9482e16afdeac95c3301fbbae63c52dc2555e069c3c7b4a239b0618348b2',
}


def sha(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('root',type=Path)
    ap.add_argument('backup',type=Path)
    args=ap.parse_args()
    root=args.root.resolve()
    if args.backup.exists() or (root/'R217-integridade.json').exists():
        raise FileExistsError('Não substituir a auditoria ou o backup finalizado')
    protected=[]
    for branch,expected in EXPECTED.items():
        files=list((root/branch/'Projeto Eberick').glob('*.prj'))
        if len(files)!=1:
            raise ValueError(f'PRJ ambíguo: {branch}')
        file=files[0]
        actual=sha(file)
        if actual!=expected:
            raise ValueError(f'PRJ divergente: {branch}')
        with ZipFile(file) as z:
            if z.testzip() is not None:
                raise ValueError(f'CRC do PRJ: {branch}')
        protected.append(dict(branch=branch,path=str(file),sha256=actual,crc='OK'))
    # Fontes da grelha usadas neste estudo são guardadas junto do resultado, sem modificá-las.
    exports=root/'fontes-grelha-R214'
    exports.mkdir(exist_ok=True)
    source=root.parent/'H03-R214-INERCIA-BIM-NAO-EXECUTAR'
    for branch in EXPECTED:
        files=list((source/(branch+'-generico')).glob('*escada*'))
        if len(files)!=1:
            raise ValueError(f'Grelha ambígua: {branch}')
        shutil.copy2(files[0],exports/(branch+'-'+files[0].name))
    data=json.loads((root/'R217-resultados.json').read_text(encoding='utf-8'))
    now=datetime.now(timezone.utc)
    start=datetime(2026,11,4,22,33,6,tzinfo=timezone.utc)
    timing=dict(inicio=start.isoformat(),fim=now.isoformat(),
                intervalo_observado_s=(now-start).total_seconds(),
                descricao='Recorte observado de testes, analise e documentacao R217; exclui trabalho anterior a 22:33:06Z e posterior a este registro.',
                pairedExperiment=False,nativeCalculationExecuted=False,
                humanVsAiActiveTimeSeparated=False,includesToolWaits=True,
                tokens=None,inferenceSeconds=None,cost=None)
    (root/'R217-tempo-recorte.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    audit=dict(createdAt=now.isoformat(),nativeProjects=protected,nativeModelChanged=False,
               fullVerificationComplete=False,classification='Correcao estrutural comum aos dois fluxos; nao e perda exclusiva de interoperabilidade.',
               testResult=dict(auxiliaryAnalyticalTestsPassed=10,timingInventoryTestsPassed=8),
               maxNativeReportDifference=data['max_difference_printed_CAD_BIM'],
               detailing=data['detailing'],
               controls={b:data[b]['controls'] for b in EXPECTED},
               results={b:{k:data[b]['governing'][k] for k in ('combination','mv_bound','mh_bound','utilization','with_native_min')} for b in EXPECTED},
               files=[dict(path=str(f.relative_to(root)),bytes=f.stat().st_size,sha256=sha(f))
                      for f in sorted(root.rglob('*')) if f.is_file()])
    (root/'R217-integridade.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with ZipFile(args.backup,'x',ZIP_DEFLATED,compresslevel=6) as z:
        for f in sorted(root.rglob('*')):
            if f.is_file():
                z.write(f,str(f.relative_to(root)))
    with ZipFile(args.backup) as z:
        if z.testzip() is not None:
            raise ValueError('Backup com CRC divergente')
        for p in protected:
            name=str(Path(p['path']).relative_to(root)).replace('\\','/')
            if hashlib.sha256(z.read(name)).hexdigest()!=p['sha256']:
                raise ValueError('PRJ no backup diverge')
    final=dict(path=str(args.backup.resolve()),bytes=args.backup.stat().st_size,sha256=sha(args.backup),crc='OK',
               projectHashesVerified=True,verificationComplete=False)
    (root/'R217-backup.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(final,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()

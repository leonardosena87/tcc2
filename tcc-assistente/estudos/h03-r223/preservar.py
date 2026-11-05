"""Backup local das copias R223 fechadas; originais R222 verificados por hash."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main(root,backup):
    if backup.exists():raise FileExistsError(backup)
    source=root.parent/'H03-R222-CONTINUIDADE-PILARES-NAO-EXECUTAR'
    expected=dict(CAD='c062f09b695ce34590fdd72e3e18eecd040316b44a404fe1f996cf318b9f59cb',
                  BIM='7af11ff076becd265037624c63986b304372f844d2131f47e8f62744b0beec64')
    projects=[]
    for b,digest in expected.items():
        before,=(source/b/'Projeto Eberick').glob('*.prj')
        after,=(root/b/'Projeto Eberick').glob('*.prj')
        if sha(before)!=digest:raise ValueError('Original R222 alterado')
        with ZipFile(after) as z:
            if z.testzip() is not None:raise ValueError('PRJ corrompido')
        projects.append(dict(branch=b,path=after.relative_to(root).as_posix(),sha256=sha(after),
                             sourceR222Preserved=True,sourceSha256=digest,crc='OK'))
    audit=dict(revision='R223',recordedAt=datetime.now(timezone.utc).isoformat(),projects=projects,
               appliedNative=['V1 N0: 30x30 cm, topo +0,20 m',
                   'AE1A/AE1B: B=H=30 cm, altura20 cm, elevacao0, engastados; apoios idealizados',
                   'ELU/dimensionamento geral e ELS com rigidez fissurada nos dois fluxos'],
               nativeDetail=dict(upper='3 fi8 com gancho projetado27cm',lower='4 fi8 com gancho10cm',
                                 skin='2x2 fi8',stirrup='8 fi6,3 c15'),
               pillarContinuityObserved=dict(CAD=['P2','P9'],BIM=['P3','P4'],
                                             reinforcement='6 fi10 em L3/L2/L1'),
               timings=dict(CADNativeSeconds=10,BIMNativeSeconds=11,
                            fullWorkflowSeconds=None,tokenUsage=None,inferenceSeconds=None),
               automaticNativeSizingMessages='Superestrutura: Com sucesso; sapatas:14 com erro em cada fluxo',
               nativeSizingSuccessIsApproval=False,fullVerificationComplete=False,
               drawingExternalOnly=True,externalHookAppliedToNative=False,
               externalDXFImported=False,authoringRevitCADSynchronized=False,
               staleItems=['Diagnostico_estrutura.docx herdado da R222',
                           'Desenhos R218 herdados: secao20x30 e complemento c9; somente historico'],
               files=[dict(path=p.relative_to(root).as_posix(),bytes=p.stat().st_size,sha256=sha(p))
                      for p in sorted(root.rglob('*')) if p.is_file() and not p.name.startswith('~$')
                      and not p.name.endswith(('.tmp','-tmp')) and p.name not in ('R223-integridade.json','R223-backup.json')])
    (root/'R223-integridade.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with ZipFile(backup,'x',ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file() and not p.name.startswith('~$') and not p.name.endswith(('.tmp','-tmp')):
                z.write(p,p.relative_to(root).as_posix())
    with ZipFile(backup) as z:
        if z.testzip() is not None:raise ValueError('Backup corrompido')
        for p in projects:
            if hashlib.sha256(z.read(p['path'])).hexdigest()!=p['sha256']:raise ValueError('PRJ divergente no backup')
        for p in audit['files']:
            if hashlib.sha256(z.read(p['path'])).hexdigest()!=p['sha256']:raise ValueError('Arquivo divergente no backup')
    result=dict(path=str(backup),bytes=backup.stat().st_size,sha256=sha(backup),crc='OK',
                allIncludedFilesHashesVerified=True,originalsR222Preserved=True)
    (root/'R223-backup.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('backup',type=Path)
    args=ap.parse_args();main(args.root,args.backup)

"""Preserva copias R224 fechadas, verificando a referencia R223 e o backup inteiro."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main(root, backup):
    if backup.exists(): raise FileExistsError(backup)
    source = root.parent/'H03-R223-V1-30X30-ENSAIO-NAO-EXECUTAR'
    source_audit = json.loads((source/'R223-integridade.json').read_text(encoding='utf-8'))
    for row in source_audit['files']:
        if sha(source/row['path']) != row['sha256']:
            raise ValueError('Arquivo R223 alterado: '+row['path'])
    projects=[]
    for b in ('CAD','BIM'):
        p, = (root/b/'Projeto Eberick').glob('*.prj')
        with ZipFile(p) as z:
            if z.testzip(): raise ValueError('PRJ com CRC invalido')
        projects.append(dict(branch=b,path=p.relative_to(root).as_posix(),sha256=sha(p),crc='OK'))
    comparison=json.loads((root/'R224-cobertura-comparacao.json').read_text(encoding='utf-8'))
    audit=dict(revision='R224',recordedAt=datetime.now(timezone.utc).isoformat(),projects=projects,
        originalsR223FilesVerified=len(source_audit['files']), originalsR223Preserved=True,
        V1ExternalDrawingImportedBoth=True,V1ExternalReinforcementAppliedToSizing=False,
        coverWarning08Resolved=False,nativeReinforcementModified=False,
        newFullProcessingPerformed=False,newFullProcessingTimeSeconds=None,
        authoringRevitCADSynchronized=False,fullVerificationComplete=False,
        coverComparison={k:v for k,v in comparison['comparison'].items() if k!='differences'},
        files=[dict(path=p.relative_to(root).as_posix(),bytes=p.stat().st_size,sha256=sha(p))
               for p in sorted(root.rglob('*')) if p.is_file() and not p.name.startswith('~$')
               and not p.name.endswith(('.tmp','-tmp'))
               and p.name not in ('R224-integridade.json','R224-backup.json')])
    (root/'R224-integridade.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with ZipFile(backup,'x',ZIP_DEFLATED) as z:
        for row in audit['files']: z.write(root/row['path'],row['path'])
        z.write(root/'R224-integridade.json','R224-integridade.json')
    with ZipFile(backup) as z:
        if z.testzip(): raise ValueError('Backup com CRC invalido')
        for row in audit['files']:
            if hashlib.sha256(z.read(row['path'])).hexdigest()!=row['sha256']:
                raise ValueError('Backup diverge: '+row['path'])
    result=dict(path=str(backup),bytes=backup.stat().st_size,sha256=sha(backup),crc='OK',
                allIncludedFilesHashesVerified=True,originalsR223Preserved=True)
    (root/'R224-backup.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('backup',type=Path)
    args=ap.parse_args();main(args.root,args.backup)

"""Empacota evidencias R226 e verifica todos os bytes incluidos; sem PRJ novo."""
import argparse
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main(root,target):
    if target.exists():raise FileExistsError(target)
    control=json.loads((root/'R226-consolidacao.json').read_text(encoding='utf-8'))
    for item in control['nativeProjects']:
        if sha(Path(item['path']))!=item['sha256']:raise ValueError('PRJ fonte alterado')
    files=[p for p in sorted(root.rglob('*')) if p.is_file() and not p.name.startswith('~$')
           and not p.name.endswith(('.tmp','-tmp')) and p.name not in ('R226-manifesto.json','R226-backup.json')]
    rows=[dict(path=p.relative_to(root).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in files]
    manifest=dict(revision='R226',recordedUtc=datetime.now(timezone.utc).isoformat(),files=rows,
        nativeProjectsIncluded=False,sourceProjects=control['nativeProjects'],
        fullNativeProjectBackup='D:/TCC/outputs/Salvamento-R224-2026-11-05.zip',
        fullVerificationComplete=False)
    (root/'R226-manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with ZipFile(target,'x',ZIP_DEFLATED) as z:
        for row in rows:z.write(root/row['path'],row['path'])
        z.write(root/'R226-manifesto.json','R226-manifesto.json')
    with ZipFile(target) as z:
        if z.testzip():raise ValueError('CRC do backup invalido')
        for row in rows:
            if hashlib.sha256(z.read(row['path'])).hexdigest()!=row['sha256']:raise ValueError('Backup divergente')
    result=dict(path=str(target),bytes=target.stat().st_size,sha256=sha(target),crc='OK',
        allIncludedFilesHashesVerified=True,sourceNativeProjectsUnchanged=True,nativeProjectsIncluded=False)
    (root/'R226-backup.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('target',type=Path)
    a=ap.parse_args();main(a.root,a.target)

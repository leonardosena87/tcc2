"""Registra os resultados públicos e verifica o backup local da R235."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile
from auditar import audit, OUT, sha


def consolidate():
    result=audit()
    if not result['persistedAfterReopen']:
        raise ValueError('Persistência não conferida')
    here=Path(__file__).resolve().parent
    public={k:v for k,v in result.items() if k not in ('parts','origins')}
    (here/'R235-resultados.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    shutil.copyfile(here/'README.md',OUT/'LEIA-PRIMEIRO-R235.md')
    target=OUT.parent/'Salvamento-R235-CAD-VIGAS-ESCADA-2026-11-06.zip'
    paths=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='R235-backup.json')
    hashes={p.relative_to(OUT).as_posix():sha(p) for p in paths}
    if not target.exists():
        with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED) as archive:
            for p in paths:
                archive.write(p,p.relative_to(OUT).as_posix())
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ValueError('Falha CRC')
        contents={n:hashlib.sha256(archive.read(n)).hexdigest() for n in archive.namelist()}
    if hashes!=contents or hashes!={p.relative_to(OUT).as_posix():sha(p) for p in paths}:
        raise ValueError('Backup difere da origem')
    result=dict(path=str(target),sha256=sha(target),bytes=target.stat().st_size,
                files=len(paths),allHashesAndCrcVerified=True)
    (OUT/'R235-backup.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':
    consolidate()

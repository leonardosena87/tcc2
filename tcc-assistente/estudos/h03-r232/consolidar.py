"""Consolida evidência textual pública e backup local verificado da R232."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

from auditar_pilares import audit, OUT, sha


def consolidate():
    result = audit()
    if not result['persistedAfterReopen'] or not result['nativeReopened']:
        raise ValueError('Persistência nativa ainda não conferida')
    origin = json.loads((OUT/'R232-preparacao.json').read_text(encoding='utf-8-sig'))
    source_prj, = (Path(origin['source'])/'Projeto Eberick').glob('*.prj')
    if sha(source_prj) != origin['sourcePrjSha256']:
        raise ValueError('PRJ original R228 alterado')
    public = {k:v for k,v in result.items() if k not in ('parts','origins')}
    public['sourceR228PrjUnchanged'] = True
    here = Path(__file__).resolve().parent
    (here/'R232-resultados.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    shutil.copyfile(here/'README.md',OUT/'LEIA-PRIMEIRO-R232.md')
    target = OUT.parent/'Salvamento-R232-CAD-PILARES-2026-11-06.zip'
    paths = sorted(p for p in OUT.rglob('*') if p.is_file() and p.name != 'R232-backup.json')
    hashes = {p.relative_to(OUT).as_posix():sha(p) for p in paths}
    if not target.exists():
        with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED) as archive:
            for p in paths:
                archive.write(p,p.relative_to(OUT).as_posix())
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ValueError('CRC inválido no backup')
        restored = {n:hashlib.sha256(archive.read(n)).hexdigest() for n in archive.namelist()}
    if hashes != restored or hashes != {p.relative_to(OUT).as_posix():sha(p) for p in paths}:
        raise ValueError('Backup difere dos arquivos salvos')
    backup = dict(path=str(target),sha256=sha(target),bytes=target.stat().st_size,
                  files=len(paths),crcAndAllFileHashesVerified=True,sourceR228PrjUnchanged=True)
    (OUT/'R232-backup.json').write_text(json.dumps(backup,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(backup))


if __name__ == '__main__':
    consolidate()

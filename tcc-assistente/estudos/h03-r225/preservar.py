"""Backup verificavel da autoria; distingue geometria salva e cobrimentos pendentes."""
import argparse
import hashlib
import json
import re
from datetime import datetime,timezone
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main(root,target,partial=False):
    if target.exists():raise FileExistsError(target)
    cfg=json.loads((root/'R225-config.json').read_text(encoding='utf-8-sig'))
    if sha(Path(cfg['SourcePath']))!=cfg['SourceSha256']:raise ValueError('R195 original alterada')
    if sha(Path(cfg['CandidatePath']))!=cfg['CandidateSha256']:raise ValueError('Candidato mudou')
    if not partial:
        audit=json.loads((root/'R225-IFC-auditoria.json').read_text(encoding='utf-8-sig'))
        if audit['summary']['coverThreeFieldsMatchCount']!=66:raise ValueError('Cobrimentos finais nao conferidos')
        native=root/'H03-R225-REVIT-COORDENACAO-NAO-EXECUTAR.rvt'
    else:
        native=root/'Antes-correcao-cobrimentos/H03-R225-REVIT-ANTES-COBRIMENTOS.rvt'
        closed=json.loads((root/'R225-fechado-apos-aplicacao.json').read_text(encoding='utf-8-sig'))
        if sha(native).lower()!=closed['SavedCopySha256'].lower():raise ValueError('Copia geometrica anterior mudou')
    rows=[]
    for p in sorted(root.rglob('*')):
        if not p.is_file() or p.name.startswith('~$') or p.suffix.lower() in ('.tmp','.dwl','.dwl2'):continue
        if p.name in ('R225-manifesto-geometria.json','R225-backup-geometria.json','R225-manifesto-final.json','R225-backup-final.json'):continue
        if p.suffix.lower()=='.rvt' and p.parent==root:
            if partial or re.search(r'\.\d{4}\.rvt$',p.name,re.I):continue
        rows.append(dict(path=p.relative_to(root).as_posix(),bytes=p.stat().st_size,sha256=sha(p)))
    phase='geometria' if partial else 'final'
    manifest=dict(revision='R225',phase=phase,recordedUtc=datetime.now(timezone.utc).isoformat(),
        originalR195Preserved=True,sourceOriginalSha256=cfg['SourceSha256'],
        includedNativeRvt=native.relative_to(root).as_posix(),includedNativeRvtSha256=sha(native),
        liveMainRvtExcluded=partial,coverCorrectionFinalized=not partial,
        EberickIncluded=False,EberickNativeBackup='D:/TCC/outputs/Salvamento-R224-2026-11-05.zip',
        fullVerificationComplete=False,files=rows)
    name=f'R225-manifesto-{phase}.json'
    (root/name).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with ZipFile(target,'x',ZIP_DEFLATED) as z:
        for row in rows:z.write(root/row['path'],row['path'])
        z.write(root/name,name)
    with ZipFile(target) as z:
        if z.testzip():raise ValueError('CRC do backup invalido')
        for row in rows:
            if hashlib.sha256(z.read(row['path'])).hexdigest()!=row['sha256']:raise ValueError('Conteudo do backup divergente')
    result=dict(path=str(target),bytes=target.stat().st_size,sha256=sha(target),crc='OK',
        allIncludedFilesHashesVerified=True,originalR195Preserved=True,
        liveMainRvtExcluded=partial,coverCorrectionFinalized=not partial)
    (root/f'R225-backup-{phase}.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('target',type=Path)
    ap.add_argument('--partial-geometry',action='store_true');a=ap.parse_args();main(a.root,a.target,a.partial_geometry)

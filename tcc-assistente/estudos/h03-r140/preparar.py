"""Cópias de consulta dos controles R138; não edita o PRJ."""
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('D:/TCC/outputs')
OUT = ROOT/'Reacoes-Grelha-H03-R140-CONSULTA-NAO-EXECUTAR'
PAIRS = [
    ('CAD', '62-H03-R138-CAD-L3-SEM-W20-NAO-EXECUTAR', '66-H03-R140-CAD-CONTROLE-CONSULTA-NAO-EXECUTAR'),
    ('BIM', '63-H03-R138-BIM-L3-SEM-W20-NAO-EXECUTAR', '67-H03-R140-BIM-CONTROLE-CONSULTA-NAO-EXECUTAR'),
]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    target = OUT/'R140-preparacao.json'
    if target.exists() or any((ROOT/d).exists() for _, _, d in PAIRS):
        raise FileExistsError('Cópias ou registro já existentes')
    OUT.mkdir(exist_ok=True)
    rows = []
    for branch, origin, destination in PAIRS:
        src, dst = ROOT/origin, ROOT/destination
        before = [(p.relative_to(src), sha(p)) for p in src.rglob('*') if p.is_file()]
        shutil.copytree(src, dst)
        for rel, digest in before:
            if sha(dst/rel) != digest:
                raise ValueError('Cópia divergente')
            rows.append({'branch':branch,'source':str(src/rel),'copy':str(dst/rel),'sha256':digest})
        prjs = list((dst/'Projeto Eberick').glob('*.prj'))
        if len(prjs) != 1:
            raise ValueError('PRJ não único')
        ini = dst/'_DADOS_/EdificacaoEberick.ini'
        raw, n = re.subn(r'(?m)^Arquivo=.*$', lambda _: 'Arquivo='+str(prjs[0])+'\r', ini.read_bytes().decode('cp1252'))
        if n != 1:
            raise ValueError('INI sem endereço único')
        ini.write_bytes(raw.encode('cp1252'))
    target.write_text(json.dumps({'createdAtUtc':datetime.now(timezone.utc).isoformat(),'files':rows,
        'onlyPreparationChange':'INI Arquivo aponta ao PRJ da cópia; PRJs inicialmente idênticos'},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'copiedFiles':len(rows)}))

if __name__ == '__main__':
    main()

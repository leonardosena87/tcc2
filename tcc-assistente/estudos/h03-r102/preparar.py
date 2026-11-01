"""Cria copias independentes dos receptores fechados, sem editar o PRJ."""
import hashlib
import json
import re
import shutil
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('D:/TCC/outputs')
OUT = ROOT / 'Analise-H03-R102-QT-VERTICAL-NAO-EXECUTAR'
PAIRS = [('CAD', '14-H03-R98-CAD-QT-NAO-EXECUTAR', '16-H03-R102-CAD-QT-VERTICAL-NAO-EXECUTAR'), ('BIM', '15-H03-R98-BIM-QT-NAO-EXECUTAR', '17-H03-R102-BIM-QT-VERTICAL-NAO-EXECUTAR')]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if OUT.exists() or any((ROOT / d).exists() for _, _, d in PAIRS):
        raise FileExistsError('Destino ja existente; nao sobrescrever')
    OUT.mkdir()
    rows = []
    for branch, origin, destination in PAIRS:
        src, dst = ROOT / origin, ROOT / destination
        before = [(p.relative_to(src).as_posix(), sha(p)) for p in src.rglob('*') if p.is_file()]
        shutil.copytree(src, dst)
        for rel, expected in before:
            actual = sha(dst / rel)
            assert actual == expected
            rows.append({'branch': branch, 'source': str(src / rel), 'copy': str(dst / rel), 'sha256Before': expected, 'copyInitiallyIdentical': True})
        prjs = list((dst / 'Projeto Eberick').glob('*.prj'))
        assert len(prjs) == 1
        ini = dst / '_DADOS_/EdificacaoEberick.ini'
        raw = ini.read_bytes().decode('cp1252')
        changed, n = re.subn(r'(?m)^Arquivo=.*$', lambda _: 'Arquivo=' + str(prjs[0]) + '\r', raw)
        assert n == 1
        ini.write_bytes(changed.encode('cp1252'))
        assert sha(prjs[0]) == next(h for p, h in before if p.endswith('.prj'))
    data = {'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'files': rows, 'onlyPreparationChange': 'ProjetoRecente/Arquivo no INI aponta para PRJ da propria copia; PRJs copiados sem alteracoes', 'processingPerformed': False}
    (OUT / 'R102-preparacao.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'copiedFilesVerified': len(rows), 'destinations': [d for _, _, d in PAIRS]}))

if __name__ == '__main__':
    main()

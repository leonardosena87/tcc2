"""Verifica a releitura real das combinacoes e preservacao das origens."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('D:/TCC/outputs')
OUT = ROOT / 'Analise-H03-R102-QT-VERTICAL-NAO-EXECUTAR'
EXPECTED = {'1017': '1.4G1+1.4G2+1.4Q+1.1A+1.4QT', '1016': 'G1+G2+Q+A+QT'}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read_combinations(text):
    result = {}
    for line in text.splitlines():
        m = re.search(r'\d+ text (.*?) ID: (1016|1017)$', line)
        if m:
            if m[2] in result and result[m[2]] != m[1]:
                raise ValueError('Leitura contraditoria')
            result[m[2]] = m[1]
    if result != EXPECTED:
        raise ValueError(f'Combinacoes inesperadas: {result}')
    return result

def main():
    prep = json.loads((OUT / 'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = []
    for row in prep['files']:
        protected.append({'path': row['source'], 'sha256': sha(Path(row['source'])), 'expected': row['sha256Before']})
    assert all(r['sha256'] == r['expected'] for r in protected)
    branches = {}
    for branch, folder in [('CAD', '16-H03-R102-CAD-QT-VERTICAL-NAO-EXECUTAR'), ('BIM', '17-H03-R102-BIM-QT-VERTICAL-NAO-EXECUTAR')]:
        text = (OUT / f'{branch}-analise-apos-reabrir-UI.txt').read_text(encoding='utf-8')
        assert folder in text
        combinations = read_combinations(text)
        prjs = list((ROOT / folder / 'Projeto Eberick').glob('*.prj'))
        assert len(prjs) == 1
        branches[branch] = {'path': str(prjs[0]), 'sha256': sha(prjs[0]), 'combinationsAfterReopening': combinations, 'time': json.loads((OUT / f'{branch}-tempo.json').read_text(encoding='utf-8'))}
    result = {'revision': 'H03/R102', 'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'branches': branches, 'protectedSources': protected, 'nativeReadbacks': 4, 'allMatched': True, 'processingPerformed': False, 'classification': 'Correcao comum de configuracao no receptor; nao defeito de transferencia comprovado', 'limits': ['Leitura das expressoes nativas regeneradas e persistidas; grade de coeficientes nao exposta pela UIA.', 'Combinacoes verticais auxiliares de PDelta e desaprumo; nao envoltoria completa ELU/ELS.', 'Tempos exploratorios incluem registro/interrupcoes; sem ranking CAD/BIM.', 'Cargas restantes, apoios efetivos, vento e dimensionamento pendentes.']}
    dest = OUT / 'R102-resultado.json'
    if dest.exists():
        raise FileExistsError(dest)
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'readbacksMatched': 4, 'protectedSourceFiles': len(protected), 'branches': {b: v['sha256'] for b, v in branches.items()}}))

if __name__ == '__main__':
    main()

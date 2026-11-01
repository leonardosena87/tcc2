"""Compara cadastros nativos de apoio; nao valida o calculo estrutural."""
import hashlib
import json
import re
from pathlib import Path
from datetime import datetime, timezone

OUT = Path('D:/TCC/outputs/Apoios-H03-R103-CONSULTA-NAO-EXECUTAR')
IDS = '801 828 1014 803 821 826 809 810 811 802 820'.split()
# Correspondencia visual no mesmo croqui N0; os nomes nativos diferem.
PAIRS = [(1, 8), (2, 4), (3, 1), (4, 9), (5, 5), (6, 2), (7, 11), (8, 7), (9, 3), (10, 10), (11, 6)]

def read_fields(text):
    values = {}
    for line in text.splitlines():
        m = re.search(r'(?:editar|caixa de combinação) \([^\n]+\).*?Value: (.*?) ID: (\d+)$', line)
        if m and m[2] in IDS:
            if m[2] in values and values[m[2]] != m[1]:
                raise ValueError('Leitura contraditoria')
            values[m[2]] = m[1]
    if set(values) != set(IDS):
        raise ValueError('Leitura incompleta')
    return values

def main():
    branches = {}
    for branch in ['CAD', 'BIM']:
        branches[branch] = {}
        for number in range(1, 12):
            name = f'{branch}-N0-P{number}'
            raw = (OUT / f'{name}-UI.txt').read_text(encoding='utf-8')
            assert 'diálogo Pilar de fundação' in raw
            assert ('16-H03-R102-CAD' if branch == 'CAD' else '17-H03-R102-BIM') in raw
            values = read_fields(raw)
            assert values['801'] == f'P{number}'
            assert (OUT / f'{name}.png').is_file()
            branches[branch][str(number)] = values
    comparisons = []
    for cad, bim in PAIRS:
        for field in IDS[1:]:
            a, b = branches['CAD'][str(cad)][field], branches['BIM'][str(bim)][field]
            comparisons.append({'cad': f'P{cad}', 'bim': f'P{bim}', 'controlId': field, 'CAD': a, 'BIM': b, 'equal': a == b})
    previous = json.loads((OUT.parent / 'Analise-H03-R102-QT-VERTICAL-NAO-EXECUTAR/R102-resultado.json').read_text(encoding='utf-8'))
    protected = []
    for b, v in previous['branches'].items():
        actual = hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()
        assert actual == v['sha256']
        protected.append({'branch': b, 'path': v['path'], 'sha256': actual, 'unchanged': True})
    result = {'revision': 'H03/R103', 'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'nativeDialogsRead': 22, 'fields': branches, 'pairingMethod': 'Posicao visual correspondente no croqui N0, documentada nas capturas; nao pareamento por nome nem nova auditoria numerica de coordenadas', 'pairs': PAIRS, 'comparisons': comparisons, 'equalFields': sum(x['equal'] for x in comparisons), 'totalComparedFields': len(comparisons), 'protectedPrjs': protected, 'processingPerformed': False, 'limits': ['Cadastro fundacao/sapata e condicao de contorno exploratoria, nao dimensionamento de fundacao.', 'Vinculos das vigas, pilares superiores e continuidade analitica global continuam pendentes.', 'Sem verificacao de estabilidade, equilibrio ou adequacao normativa final.', 'Radios/checkboxes observados visualmente; parser nao deduz estado de selecao.'], 'times': {b: json.loads((OUT / f'{b}-tempo.json').read_text()) for b in branches}}
    target = OUT / 'R103-resultado.json'
    if target.exists():
        raise FileExistsError(target)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'nativeDialogs': 22, 'equalFields': result['equalFields'], 'total': len(comparisons), 'prjsUnchanged': True}))

if __name__ == '__main__':
    main()

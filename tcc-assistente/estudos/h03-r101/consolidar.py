"""Consolida leituras nativas; nao calcula nem aprova a estrutura."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('D:/TCC/outputs')
OUT = ROOT / 'Analise-H03-R101-CONSULTA-NAO-EXECUTAR'
SOURCES = {
    'CAD': ('14-H03-R98-CAD-QT-NAO-EXECUTAR/Projeto Eberick/H03_CAD_R49_LAJES_NAO_EXECUTAR.prj', 'e2dc1d91fda030a981e8562d7c3d46318b8e6c262f9c4300415d4078027ca122'),
    'BIM': ('15-H03-R98-BIM-QT-NAO-EXECUTAR/Projeto Eberick/H03_BIM_R46_IFC_NAO_EXECUTAR.prj', '41735ed0fdd0e2c0424dd84ef0b272418947b5c8bdb0cd1abcfa62c852917ccf'),
}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def controls(path, ids):
    text = path.read_text(encoding='utf-8')
    result = {}
    for line in text.splitlines():
        m = re.search(r'(?:editar|caixa de combinação) \([^\n]+\) (.*?) Value: (.*?) ID: (\d+)$', line)
        if m and m[3] in ids:
            key, value = m[3], (m[1], m[2])
            if key in result and result[key] != value:
                raise ValueError(f'Controle contraditorio: {path.name}/{key}')
            result[key] = value
    if set(result) != set(ids):
        raise ValueError(f'Controles ausentes: {path.name}/{set(ids)-set(result)}')
    return result

def main():
    groups = {
        'analise-geral': '1001 1011 1023 1061 1025 1201 1008 1009 1010 1045 1064 1046 1020 1021 1029'.split(),
        'apoio-elastico-padrao': '138 141 145 148 103 109 104 110 105 111 106 112 107 113 108 114'.split(),
    }
    comparisons = []
    for name, ids in groups.items():
        values = {b: controls(OUT / f'{b}-{name}-UI.txt', ids) for b in SOURCES}
        for key in ids:
            comparisons.append({'dialog': name, 'id': key, 'CAD': values['CAD'][key], 'BIM': values['BIM'][key], 'equal': values['CAD'][key] == values['BIM'][key]})
    protected = []
    for branch, (path, expected) in SOURCES.items():
        actual = sha(ROOT / path)
        protected.append({'branch': branch, 'path': path, 'expectedSha256': expected, 'sha256': actual, 'unchanged': actual == expected})
    if not all(x['unchanged'] for x in protected):
        raise ValueError('PRJ consultado foi alterado')
    visual = [{'branch': b, 'combination': c, 'action': 'Q_TELHADO_MANUTENCAO', 'displayedCoefficient': 0.0, 'method': 'Leitura visual da linha 19; grade nao exposta pela UIA', 'screenshot': f'{b}-{c}-QT-zero-0.png'} for b in SOURCES for c in ['PDelta', 'desaprumo']]
    for item in visual:
        assert (OUT / item['screenshot']).is_file()
    result = {'revision': 'H03/R101', 'atUtc': datetime.now(timezone.utc).isoformat(), 'comparisons': comparisons, 'equal': sum(x['equal'] for x in comparisons), 'total': len(comparisons), 'protected': protected, 'visualObservations': visual, 'finding': 'QT com coeficiente zero nas duas combinacoes verticais em ambos os ramos. Correcao comum no receptor; nao perda DWG/IFC demonstrada.', 'limits': ['Apoio elastico padrao nao comprova vinculos efetivos dos pilares.', 'Nao houve processamento, alteracao nativa ou verificacao normativa final.', '31 comparacoes incluem parametros de fundacoes fora do escopo; igualdade nao significa adequacao.', 'Checkboxes e radios conferidos visualmente: PDelta ativo, grelhas+portico espacial, flexibilizacao ativa, salvar apos processamento desativado.']}
    target = OUT / 'R101-resultado.json'
    if target.exists():
        raise FileExistsError(target)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'equal': result['equal'], 'total': result['total'], 'nativePrjUnchanged': True}))

if __name__ == '__main__':
    main()

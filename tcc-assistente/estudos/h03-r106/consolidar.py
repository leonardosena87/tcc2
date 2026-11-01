"""Preserva o ensaio ELS parcial e a divergencia de direcao critica."""
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('D:/TCC/outputs')
OUT = ROOT / 'Deslocamentos-H03-R106-EXPLORATORIO-NAO-EXECUTAR'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary(text):
    values = set(re.findall(r'editar Value: (Cargas verticais: [^\n]+)', text))
    if len(values) != 1:
        raise ValueError('Resumo ausente ou contraditorio')
    raw = values.pop()
    if any(marker not in raw for marker in ['Q_TELHADO_MANUTENCAO =', 'Gama-Z', 'Processo P-Delta']):
        raise ValueError('Resumo incompleto')
    if 'Os deslocamentos horizontais não foram verificados' in raw:
        raise ValueError('Deslocamentos nao verificados neste resumo')
    horizontal = re.search(r'Deslocamento horizontal máximo do centro de massa \(Vento\): (.*?) Deslocamento relativo', raw)
    relative = re.search(r'Deslocamento relativo máximo do centro de massa \(Vento\): (.+?) - ([XY][+-]) = ([\d.]+) cm \(limite ([\d.]+)\)', raw)
    if not horizontal or not relative:
        raise ValueError('Deslocamentos ausentes')
    values = re.findall(r'([XY][+-]) = ([\d.]+) cm \(limite ([\d.]+)\)', horizontal[1])
    if len(values) != 4 or {r[0] for r in values} != {'X+', 'X-', 'Y+', 'Y-'}:
        raise ValueError('Direcoes horizontais ausentes ou duplicadas')
    return {'raw': raw, 'horizontalCm': {d: {'value': float(v), 'displayedLimit': float(l)} for d, v, l in values},
            'relative': {'floorNative': relative[1], 'direction': relative[2], 'valueCm': float(relative[3]), 'displayedLimitCm': float(relative[4])}}


def comparison(cad, bim):
    return {'horizontalValuesAndDisplayedLimitsEqual': cad['horizontalCm'] == bim['horizontalCm'],
            'relativeValueAndDisplayedLimitEqual': (cad['relative']['valueCm'], cad['relative']['displayedLimitCm']) == (bim['relative']['valueCm'], bim['relative']['displayedLimitCm']),
            'relativeCriticalDirectionEqual': cad['relative']['direction'] == bim['relative']['direction'],
            'rawSummariesEqual': cad['raw'] == bim['raw'],
            'directionDiscrepancyCause': None, 'transferDefectDemonstrated': False}


def main():
    if (OUT / 'R106-resultado.json').exists():
        raise FileExistsError('Nao substituir resultado anterior')
    prep = json.loads((OUT / 'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = [{'path': r['source'], 'sha256': sha(Path(r['source'])), 'expected': r['sha256Before']} for r in prep['files']]
    if not all(r['sha256'] == r['expected'] for r in protected):
        raise ValueError('Origem alterada')
    frozen = OUT / 'congelados-apos-processamento'
    frozen.mkdir()
    branches = {}
    for branch, folder in [('CAD', '20-H03-R106-CAD-DESLOCAMENTOS-NAO-EXECUTAR'), ('BIM', '21-H03-R106-BIM-DESLOCAMENTOS-NAO-EXECUTAR')]:
        text = (OUT / f'{branch}-resumo-analise-UI.txt').read_text(encoding='utf-8')
        if folder not in text:
            raise ValueError('Projeto incorreto no resumo')
        parsed = summary(text)
        src, dst = ROOT / folder, frozen / branch
        shutil.copytree(src, dst)
        hashes = []
        for path in src.rglob('*'):
            if path.is_file():
                rel = path.relative_to(src)
                h = sha(path)
                if sha(dst / rel) != h:
                    raise ValueError('Copia congelada divergente')
                hashes.append({'relativePath': rel.as_posix(), 'sha256': h})
        prjs = list((src / 'Projeto Eberick').glob('*.prj'))
        if len(prjs) != 1:
            raise ValueError('Projeto ambiguo')
        branches[branch] = {'projectPath': str(prjs[0]), 'prjSha256': sha(prjs[0]), 'summary': parsed,
                            'frozenFiles': hashes,
                            'processingTimeObservation': json.loads((OUT / f'{branch}-processamento-tempo.json').read_text()),
                            'sessionTime': json.loads((OUT / f'{branch}-sessao-tempo.json').read_text())}
    result = {'revision': 'H03/R106', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Portico ELS-DEF, adotar rigidez configurada. Sem dimensionamento, flechas de lajes ou vibracoes.',
              'branches': branches, 'comparison': comparison(branches['CAD']['summary'], branches['BIM']['summary']),
              'sourceFilesProtected': protected, 'processingPerformed': True, 'finalStructuralApproval': False,
              'finalRankingAllowed': False,
              'limits': ['Cargas restantes e vento local ainda incompletos; resultados parciais.',
                         'Limites sao valores exibidos, nao confirmacao da adequacao normativa de cada parametro.',
                         'Rigidez configurada nao equivale ao calculo de rigidez fissurada.',
                         'Direcao critica relativa difere e sua causa ainda nao foi estabelecida.',
                         'Igualdade de valores arredondados nao comprova equivalencia dos casos criticos ou da estrutura.',
                         'Tempos incluem observacao, registro e intervalos; nao medem solver isolado nem produtividade final.']}
    (OUT / 'R106-resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'comparison': result['comparison'], 'protectedFiles': len(protected), 'frozenFiles': {b: len(v['frozenFiles']) for b, v in branches.items()}}))


if __name__ == '__main__':
    main()

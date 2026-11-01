"""Consolida o diagnostico nativo parcial, sem aprovar estrutura ou ranking."""
import hashlib
import json
import re
import shutil
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('D:/TCC/outputs')
OUT = ROOT / 'Diagnostico-H03-R104-EXPLORATORIO-NAO-EXECUTAR'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def summary(text):
    values = set(re.findall(r'editar Value: (Cargas verticais: [^\n]+)', text))
    if len(values) != 1:
        raise ValueError('Resumo ausente ou contraditorio')
    value = values.pop()
    for marker in ['Q_TELHADO_MANUTENCAO =', 'Gama-Z', 'Processo P-Delta', 'Os deslocamentos horizontais não foram verificados']:
        if marker not in value:
            raise ValueError('Resumo incompleto')
    return value

def main():
    if (OUT / 'R104-resultado.json').exists():
        raise FileExistsError('Nao substituir resultado anterior')
    prep = json.loads((OUT / 'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = [{'path': r['source'], 'sha256': sha(Path(r['source'])), 'expected': r['sha256Before']} for r in prep['files']]
    assert all(r['sha256'] == r['expected'] for r in protected)
    branches = {}
    frozen = OUT / 'congelados-apos-processamento'
    frozen.mkdir()
    for branch, folder in [('CAD', '18-H03-R104-CAD-DIAGNOSTICO-NAO-EXECUTAR'), ('BIM', '19-H03-R104-BIM-DIAGNOSTICO-NAO-EXECUTAR')]:
        text = (OUT / f'{branch}-resumo-analise-UI.txt').read_text(encoding='utf-8')
        assert folder in text
        raw = summary(text)
        src, dst = ROOT / folder, frozen / branch
        shutil.copytree(src, dst)
        hashes = []
        for p in src.rglob('*'):
            if p.is_file():
                rel = p.relative_to(src)
                h = sha(p)
                assert sha(dst / rel) == h
                hashes.append({'relativePath': rel.as_posix(), 'sha256': h})
        prjs = list((src / 'Projeto Eberick').glob('*.prj'))
        assert len(prjs) == 1
        branches[branch] = {'projectPath': str(prjs[0]), 'prjSha256': sha(prjs[0]), 'summary': raw, 'frozenFiles': hashes, 'processingTimeObservation': json.loads((OUT / f'{branch}-processamento-tempo.json').read_text()), 'sessionTime': json.loads((OUT / f'{branch}-sessao-tempo.json').read_text())}
    result = {'revision': 'H03/R104', 'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'scope': 'Analise estatica exploratoria, dimensionamento/ELSDEF/ELSVE desmarcados nas opcoes observadas', 'branches': branches, 'summariesExactlyEqualAtDisplayedPrecision': branches['CAD']['summary'] == branches['BIM']['summary'], 'sourceFilesProtected': protected, 'processingPerformed': True, 'finalStructuralApproval': False, 'finalRankingAllowed': False, 'limits': ['Cargas restantes e vento local ainda incompletos; resultados parciais.', 'Resumo exibe zero no bloco de deslocamentos nao verificados; nao usar como deslocamento estrutural nulo ou aprovacao ELS.', 'GamaZ apresentado nao aprova estabilidade final com cargas incompletas.', 'Igualdade do resumo nao comprova igualdade de todos os esforcos, ligacoes ou dimensionamento.', 'Tempos de observacao incluem latencia e intervalos entre capturas; nao medem solver isolado.']}
    (OUT / 'R104-resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'equalSummary': result['summariesExactlyEqualAtDisplayedPrecision'], 'protectedFiles': len(protected), 'frozenFiles': {b: len(v['frozenFiles']) for b, v in branches.items()}}))

if __name__ == '__main__':
    main()

"""Congela o processamento parcial com varanda e conserva a divergencia de direcao."""
import hashlib
import importlib.util
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('D:/TCC/outputs')
OUT = ROOT / 'Analise-H03-R111-VARANDA-NAO-EXECUTAR'
spec = importlib.util.spec_from_file_location('r106', Path(__file__).parents[1] / 'h03-r106/consolidar.py')
r106 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r106)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract(text):
    result = r106.summary(text)
    labels = ['Peso próprio', 'Adicional', 'Acidental', 'Q_TELHADO_MANUTENCAO', 'Total']
    loads = {}
    for label in labels:
        values = re.findall(re.escape(label) + r' = (\d+\.\d+) tf', result['raw'])
        if len(values) != 1:
            raise ValueError('Parcela vertical ausente ou duplicada: ' + label)
        loads[label] = float(values[0])
    gamma = re.search(r'Verificação de estabilidade \(Gama-Z\): (.*?) Análise de 2ª ordem:', result['raw'])
    if not gamma:
        raise ValueError('Gama-Z ausente')
    rows = re.findall(r'([XY][+-]) = (\d+\.\d+) \(limite (\d+\.\d+)\)', gamma[1])
    if len(rows) != 4 or {r[0] for r in rows} != {'X+', 'X-', 'Y+', 'Y-'}:
        raise ValueError('Direcoes Gama-Z ausentes ou duplicadas')
    result['verticalLoadsDisplayedTf'] = loads
    result['gammaZDisplayed'] = {d: {'value': float(v), 'displayedLimit': float(l)} for d, v, l in rows}
    return result


def main():
    if (OUT / 'R111-resultado.json').exists():
        raise FileExistsError('Nao substituir resultado anterior')
    prep = json.loads((OUT / 'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = [{**r, 'afterSha256': sha(Path(r['source']))} for r in prep['files']]
    if any(r['afterSha256'] != r['sha256Before'] for r in protected):
        raise ValueError('Fonte R109 alterada')
    baseline_path = ROOT / 'Deslocamentos-H03-R106-EXPLORATORIO-NAO-EXECUTAR/R106-resultado.json'
    baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
    frozen = OUT / 'congelados-apos-processamento'
    frozen.mkdir()
    branches = {}
    for branch, folder in [('CAD', '24-H03-R111-CAD-VARANDA-NAO-EXECUTAR'),
                           ('BIM', '25-H03-R111-BIM-VARANDA-NAO-EXECUTAR')]:
        evidence = OUT / f'{branch}-resumo-analise-UI.txt'
        text = evidence.read_text(encoding='utf-8')
        if folder not in text:
            raise ValueError('Resumo de projeto incorreto')
        summary = extract(text)
        previous = extract('editar Value: ' + baseline['branches'][branch]['summary']['raw'])
        src, dst = ROOT / folder, frozen / branch
        shutil.copytree(src, dst)
        hashes = [{'path': p.relative_to(src).as_posix(), 'sha256': sha(p)}
                  for p in sorted(src.rglob('*')) if p.is_file()]
        if not all(sha(dst / r['path']) == r['sha256'] for r in hashes):
            raise ValueError('Congelamento divergente')
        prjs = list(src.rglob('*.prj'))
        if len(prjs) != 1:
            raise ValueError('PRJ ambiguo')
        branches[branch] = {'projectPath': str(prjs[0]), 'prjSha256': sha(prjs[0]), 'summary': summary,
                            'frozenFiles': hashes, 'evidenceSha256': sha(evidence),
                            'deltaDisplayedVerticalLoadsTfFromOwnR106': {
                                k: round(v-previous['verticalLoadsDisplayedTf'][k], 6)
                                for k, v in summary['verticalLoadsDisplayedTf'].items()},
                            'horizontalAndRelativeSummaryUnchangedFromOwnR106':
                                (summary['horizontalCm'], summary['relative']) == (previous['horizontalCm'], previous['relative']),
                            'sessionTime': json.loads((OUT / f'{branch}-sessao-tempo.json').read_text(encoding='utf-8')),
                            'processingTimeObservation': json.loads((OUT / f'{branch}-processamento-tempo.json').read_text(encoding='utf-8'))}
    cad, bim = [branches[b]['summary'] for b in ['CAD', 'BIM']]
    result = {'revision': 'H03/R111', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Sensibilidade VP1-A; analise estatica e ELS-DEF com rigidez configurada, sem dimensionamento.',
              'branches': branches, 'comparison': {**r106.comparison(cad, bim),
                'verticalDisplayedValuesEqual': cad['verticalLoadsDisplayedTf'] == bim['verticalLoadsDisplayedTf'],
                'gammaZDisplayedValuesAndLimitsEqual': cad['gammaZDisplayed'] == bim['gammaZDisplayed']},
              'baselineR106Path': str(baseline_path), 'baselineR106Sha256': sha(baseline_path),
              'protectedSourceR109Files': protected, 'sourceR109FilesUnchanged': True,
              'processingPerformed': True, 'finalStructuralApproval': False, 'finalRankingAllowed': False,
              'limits': ['Cargas ainda parciais; nao dimensionou concreto, armaduras, metal ou ancoragens.',
                         'Mesmos valores arredondados nao demonstram ausencia de alteracao dos esforcos.',
                         'Diferenca da direcao relativa permanece sem causa esclarecida.',
                         'Delta de totais arredondados nao e verificacao integral de equilibrio global.',
                         'Limites apresentados sao os exibidos, sem validacao final de sua adequacao.',
                         'Intervalos incluem observacao/interface; nao sao solver ou produtividade final.']}
    (OUT / 'R111-resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'comparison': result['comparison'], 'sourceFilesUnchanged': len(protected),
                      'frozenFiles': {b: len(v['frozenFiles']) for b, v in branches.items()},
                      'deltasTf': {b: v['deltaDisplayedVerticalLoadsTfFromOwnR106'] for b, v in branches.items()}}))


if __name__ == '__main__':
    main()

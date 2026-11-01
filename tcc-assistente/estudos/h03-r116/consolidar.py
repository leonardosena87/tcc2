"""Consolida sensibilidade P2 sem mascarar diferencas exibidas dos resumos."""
import importlib.util
import json
import math
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('D:/TCC/outputs')
OUT = ROOT / 'Analise-H03-R116-P2-NAO-EXECUTAR'
spec = importlib.util.spec_from_file_location('r111', Path(__file__).parents[1] / 'h03-r111/consolidar.py')
r111 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r111)
sha = r111.sha


def extract(text):
    parsed = r111.extract(text)
    tail = parsed['raw'].split('Deslocamentos no topo da edificação: ', 1)
    if len(tail) != 2:
        raise ValueError('Resultados de topo ausentes')
    rows = re.findall(r'(Acidental|Vento [XY][+-]|Desaprumo [XY][+-]): (\d+\.\d+) »» (\d+\.\d+) \(([+-]\d+\.\d+)%\)', tail[1])
    if len(rows) != 9 or len({r[0] for r in rows}) != 9:
        raise ValueError('Casos do topo ausentes ou duplicados')
    parsed['topDisplacementsRawUnitNotExplicit'] = {
        name: {'first': float(a), 'second': float(b), 'displayedIncreasePercent': float(p)}
        for name, a, b, p in rows}
    return parsed


def check_time(session, command):
    for row, field in [(session, 'wallMs'), (command, 'durationMs')]:
        v = row[field]
        if not math.isfinite(v) or v <= 0:
            raise ValueError('Duracao invalida')
    if not (session['start']['mono'] <= command['start']['mono'] < command['end']['mono'] <= session['end']['mono']):
        raise ValueError('Intervalo de processamento fora da sessao')


def main():
    if (OUT / 'R116-resultado.json').exists():
        raise FileExistsError('Nao substituir resultado anterior')
    prep = json.loads((OUT / 'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = [{**r, 'afterSha256': sha(Path(r['source']))} for r in prep['files']]
    if any(r['afterSha256'] != r['sha256Before'] for r in protected):
        raise ValueError('Fonte R115 alterada')
    baseline_path = ROOT / 'Analise-H03-R111-VARANDA-NAO-EXECUTAR/R111-resultado.json'
    baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
    branches = {}
    for branch, folder in [('CAD', '30-H03-R116-CAD-P2-NAO-EXECUTAR'), ('BIM', '31-H03-R116-BIM-P2-NAO-EXECUTAR')]:
        evidence = OUT / f'{branch}-resumo-analise-UI.txt'
        text = evidence.read_text(encoding='utf-8')
        if folder not in text:
            raise ValueError('Projeto incorreto')
        summary = extract(text)
        status = (OUT / f'{branch}-processamento-estado-UI.txt').read_text(encoding='utf-8')
        if folder not in status or 'Estrutura processada com avisos' not in status:
            raise ValueError('Termino com avisos nao confirmado')
        previous = extract('editar Value: ' + baseline['branches'][branch]['summary']['raw'])
        session = json.loads((OUT / f'{branch}-sessao-tempo.json').read_text(encoding='utf-8'))
        command = json.loads((OUT / f'{branch}-processamento-tempo.json').read_text(encoding='utf-8'))
        check_time(session, command)
        src = ROOT / folder
        prjs = list(src.rglob('*.prj'))
        if len(prjs) != 1:
            raise ValueError('PRJ ambiguo')
        branches[branch] = {'projectPath': str(prjs[0]), 'projectSha256': sha(prjs[0]),
                            'summary': summary, 'evidenceSha256': sha(evidence),
                            'deltaDisplayedVerticalLoadsTfFromOwnR111': {
                                k: round(v - previous['verticalLoadsDisplayedTf'][k], 6)
                                for k, v in summary['verticalLoadsDisplayedTf'].items()},
                            'sessionTime': session, 'processingTimeObservation': command}
    frozen = OUT / 'congelados-apos-processamento'
    frozen.mkdir()
    for branch, values in branches.items():
        src = Path(values['projectPath']).parents[1]
        dst = frozen / branch
        shutil.copytree(src, dst)
        hashes = [{'path': p.relative_to(src).as_posix(), 'sha256': sha(p)}
                  for p in sorted(src.rglob('*')) if p.is_file()]
        if not all(sha(dst / r['path']) == r['sha256'] for r in hashes):
            raise ValueError('Congelamento divergente')
        values['frozenFiles'] = hashes
    cad, bim = [branches[b]['summary'] for b in ['CAD', 'BIM']]
    top_differences = []
    for case, a in cad['topDisplacementsRawUnitNotExplicit'].items():
        b = bim['topDisplacementsRawUnitNotExplicit'][case]
        for field in a:
            if a[field] != b[field]:
                top_differences.append({'case': case, 'field': field, 'CAD': a[field], 'BIM': b[field],
                                        'deltaBIMminusCAD': round(b[field] - a[field], 6)})
    result = {'revision': 'H03/R116', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Sensibilidade P2-GRAV-A somada a VP1-A; estatica e ELS-DEF portico com rigidez configurada.',
              'branches': branches, 'comparison': {**r111.r106.comparison(cad, bim),
                  'verticalDisplayedValuesEqual': cad['verticalLoadsDisplayedTf'] == bim['verticalLoadsDisplayedTf'],
                  'gammaZDisplayedValuesAndLimitsEqual': cad['gammaZDisplayed'] == bim['gammaZDisplayed'],
                  'topDisplayedDifferences': top_differences},
              'baselineR111Path': str(baseline_path), 'baselineR111Sha256': sha(baseline_path),
              'protectedSourceR115Files': protected, 'sourceR115FilesUnchanged': True,
              'processingPerformed': True, 'dimensioningPerformed': False, 'slabDeflectionPerformed': False,
              'crackedStiffnessCalculationPerformed': False, 'finalStructuralApproval': False,
              'finalRankingAllowed': False,
              'limits': ['Cargas parciais: tanque, demais cargas e vento/combinacoes nao encerrados.',
                         'Nao dimensionou concreto, armaduras, metal ou ancoragens.',
                         'Diferenca de direcao relativa persiste; causa e defeito de transferencia nao demonstrados.',
                         'Duas diferencas de 0,01 ponto percentual no topo devem ser preservadas; causa desconhecida.',
                         'Deslocamentos de topo preservados como exibidos: unidade nao explicitada nesse trecho.',
                         'Delta de totais arredondados nao e verificacao integral de equilibrio ou calibracao de unidades.',
                         'Tempos de comando incluem latencia/captura, estao contidos nas sessoes e nao devem ser somados.',
                         'Sessao CAD inclui intervalo de retomada; nao compara produtividade com a sessao BIM.']}
    (OUT / 'R116-resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'comparison': result['comparison'], 'protectedFiles': len(protected),
                      'frozenFiles': {b: len(v['frozenFiles']) for b, v in branches.items()},
                      'deltasTf': {b: v['deltaDisplayedVerticalLoadsTfFromOwnR111'] for b, v in branches.items()}}))


if __name__ == '__main__':
    main()

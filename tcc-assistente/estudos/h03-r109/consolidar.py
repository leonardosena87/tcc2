"""Consolida a releitura nativa VP1-A; nao processa ou modifica os PRJs."""
import hashlib
import json
import math
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('D:/TCC/outputs')
OUT = ROOT / 'Varanda-H03-R109-SENSIBILIDADE-NAO-EXECUTAR'
TARGETS = {'CAD': [('VP1-01', 'P8'), ('VP1-02', 'P9')],
           'BIM': [('VP1-01', 'P7'), ('VP1-02', 'P3')]}
EXPECTED = {'G': {'Fx': 0, 'Fy': 0, 'Fz': -0.521164, 'Mx': 0, 'My': 0.260582, 'Mz': 0},
            'QT': {'Fx': 0, 'Fy': 0, 'Fz': -0.393750, 'Mx': 0, 'My': 0.196875, 'Mz': 0}}
ACTIONS = {'G': 'Adicional', 'QT': 'Q_TELHADO_MANUTENCAO'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vector(text, action):
    names = set(re.findall(r'caixa de combina[^\r\n]* Ação Value: (.+?) ID:', text))
    if names != {ACTIONS[action]}:
        raise ValueError('Acao ausente ou ambigua na releitura')
    result = {}
    for component in ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']:
        values = {float(v) for v in re.findall(r'editar \(settable, string\) ' + component + r' Value: (\S+) ID:', text)}
        if len(values) != 1 or not all(math.isfinite(v) for v in values):
            raise ValueError('Componente ausente, invalida ou ambigua: ' + component)
        result[component] = values.pop()
    return result


def verify_expected(values, action):
    if any(abs(values[c] - v) > 1e-9 for c, v in EXPECTED[action].items()):
        raise ValueError('Vetor relido diferente do planejado para ' + action)


def main():
    if (OUT / 'R109-resultado.json').exists():
        raise FileExistsError('Nao substituir resultado anterior')
    preparation = json.loads((OUT / 'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = [{**r, 'afterSha256': sha(Path(r['source']))} for r in preparation['files']]
    if any(r['afterSha256'] != r['sha256Before'] for r in protected):
        raise ValueError('Arquivo fonte R102 alterado')
    branches = {}
    frozen = OUT / 'congelados-apos-releitura'
    frozen.mkdir()
    for branch, targets in TARGETS.items():
        readings = []
        for support, pillar in targets:
            identity_file = OUT / f'{branch}-{support}-{pillar}-apos-reabrir-UI.txt'
            text = identity_file.read_text(encoding='utf-8')
            identity = set(re.findall(r'editar \(settable, string\) Nome Value: (\S+) ID:', text))
            if identity != {pillar}:
                raise ValueError('Identidade nativa inesperada')
            for action in ['G', 'QT']:
                evidence = OUT / f'{branch}-{support}-{action}-apos-reabrir-UI.txt'
                values = vector(evidence.read_text(encoding='utf-8'), action)
                verify_expected(values, action)
                readings.append({'support': support, 'pillarNative': pillar, 'action': action, 'components': values,
                                 'identityEvidence': str(identity_file), 'vectorEvidence': str(evidence),
                                 'vectorEvidenceSha256': sha(evidence)})
        own_rows = [r for r in preparation['files'] if r['branch'] == branch]
        src = Path(own_rows[0]['copy']).parents[1]
        dst = frozen / branch
        shutil.copytree(src, dst)
        hashes = [{'path': p.relative_to(src).as_posix(), 'sha256': sha(p)}
                  for p in sorted(src.rglob('*')) if p.is_file()]
        if not all(sha(dst / r['path']) == r['sha256'] for r in hashes):
            raise ValueError('Congelamento divergente')
        first = json.loads((OUT / f'{branch}-primeira-gravacao-hashes.json').read_text(encoding='utf-8'))
        changes = [{'path': r['path'], 'beforeSha256': r['sha256'], 'afterSha256': sha(src / r['path'])}
                   for r in first if sha(src / r['path']) != r['sha256']]
        if any(r['path'].endswith('.prj') for r in changes):
            raise ValueError('PRJ mudou durante consulta')
        prj = next(p for p in src.rglob('*.prj'))
        branches[branch] = {'projectPath': str(prj), 'projectSha256': sha(prj), 'readings': readings,
                            'frozenFiles': hashes, 'auxiliaryChangesDuringConsultation': changes,
                            'prjUnchangedDuringConsultation': True,
                            'sessionTime': json.loads((OUT / f'{branch}-sessao-tempo.json').read_text())}
    comparisons = []
    for cad, bim in zip(branches['CAD']['readings'], branches['BIM']['readings']):
        assert (cad['support'], cad['action']) == (bim['support'], bim['action'])
        for c in EXPECTED[cad['action']]:
            comparisons.append({'support': cad['support'], 'action': cad['action'], 'component': c,
                                'CAD': cad['components'][c], 'BIM': bim['components'][c],
                                'equal': cad['components'][c] == bim['components'][c]})
    result = {'revision': 'H03/R109', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
              'hypothesisId': 'VP1-A', 'branches': branches, 'pairedComponentComparisons': comparisons,
              'protectedSourceR102Files': protected, 'sourceR102FilesUnchanged': True,
              'nativeLoadApplicationPerformed': True, 'saveCloseReopenReadbackPerformed': True,
              'processingPerformed': False, 'finalStructuralApproval': False, 'finalTimeRankingAllowed': False,
              'other13RoofNodesReauditedInR109': False,
              'limits': ['Sensibilidade de cargas da varanda; perfis e ligacoes nao dimensionados.',
                         'Nao encerra P2, reservatorio, paredes, escada, vento ou combinacoes.',
                         'Nao houve reprocessamento; resultados antigos nao representam cargas R109.',
                         'Tempos de sessao incluem aprendizagem, interface e retomada; nao medem produtividade pura.',
                         'Demais13 nos A1/A2 nao foram selecionados para lancamento; nao foram todos relidos nesta etapa.']}
    (OUT / 'R109-resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'sourceFilesUnchanged': len(protected), 'pairedComponents': len(comparisons),
                      'equal': sum(r['equal'] for r in comparisons),
                      'frozenFiles': {b: len(v['frozenFiles']) for b, v in branches.items()}}))


if __name__ == '__main__':
    main()

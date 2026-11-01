"""Confere registros nativos P2 antes/depois; preserva fontes e congela copias fechadas."""
import hashlib
import importlib.util
import json
import math
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('D:/TCC/outputs')
OUT = ROOT / 'Telhado-P2-H03-R115-SENSIBILIDADE-NAO-EXECUTAR'
TARGETS = {'CAD': ['P10', 'P7', 'P11', 'P8'], 'BIM': ['P10', 'P11', 'P6', 'P7']}
COMPONENTS = ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']
ACTION_NAMES = {'G': 'Adicional', 'QT': 'Q_TELHADO_MANUTENCAO'}
spec = importlib.util.spec_from_file_location('r109_readback', Path(__file__).parents[1] / 'h03-r109/consolidar.py')
extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extractor)
vector = extractor.vector
sha = extractor.sha


def expected(support, action, before=False):
    result = dict.fromkeys(COMPONENTS, 0.0)
    if support == 'RP2-04':
        result.update(Fz=-0.521164 if action == 'G' else -0.39375,
                      My=0.260582 if action == 'G' else 0.196875)
    if not before:
        result['Fz'] += -1.000138 if action == 'G' else -0.755625
    return result


def verify(values, support, action, before=False):
    target = expected(support, action, before)
    # O dialogo reaberto mostra seis algarismos significativos, e nao seis casas.
    # A tolerancia cobre a meia unidade da ultima casa EXIBIDA neste intervalo.
    for c, v in target.items():
        tolerance = 5.000001e-6 if c == 'Fz' and not before else 1e-9
        if not math.isfinite(values[c]) or abs(values[c] - v) > tolerance:
            raise ValueError(f'Vetor divergente {support}/{action}/{c}: {values[c]} esperado {v}')


def main():
    if (OUT / 'R115-resultado.json').exists():
        raise FileExistsError('Nao substituir resultado existente')
    prep = json.loads((OUT / 'R102-preparacao.json').read_text(encoding='utf-8-sig'))
    protected = [{**r, 'afterSha256': sha(Path(r['source']))} for r in prep['files']]
    if any(r['afterSha256'] != r['sha256Before'] for r in protected):
        raise ValueError('Fonte R109 alterada')
    branches = {}
    # Validar integralmente antes de criar congelados ou resultado.
    for branch, pillars in TARGETS.items():
        readings = []
        for number, pillar in enumerate(pillars, 1):
            support = f'RP2-{number:02d}'
            identity_files = {}
            for phase in ['antes', 'apos-reabrir']:
                p = OUT / f'{branch}-{support}-{pillar}-{phase}-UI.txt'
                names = set(re.findall(r'editar \(settable, string\) Nome Value: (\S+) ID:', p.read_text(encoding='utf-8')))
                if names != {pillar}:
                    raise ValueError(f'Identidade inesperada: {p.name}')
                identity_files[phase] = {'path': str(p), 'sha256': sha(p)}
            for action in ['G', 'QT']:
                evidence = {}
                for phase in ['antes', 'preparado', 'apos-reabrir']:
                    p = OUT / f'{branch}-{support}-{action}-{phase}-UI.txt'
                    values = vector(p.read_text(encoding='utf-8'), action)
                    verify(values, support, action, phase == 'antes')
                    evidence[phase] = {'path': str(p), 'sha256': sha(p), 'components': values}
                readings.append({'support': support, 'pillarNative': pillar, 'action': action,
                                 'identityEvidence': identity_files, 'evidence': evidence,
                                 'components': evidence['apos-reabrir']['components'],
                                 'plannedTotal': expected(support, action)})
        rows = [r for r in prep['files'] if r['branch'] == branch]
        src = Path(rows[0]['copy']).parents[1]
        first = json.loads((OUT / f'{branch}-primeira-gravacao-hashes.json').read_text(encoding='utf-8-sig'))
        changes = [{'path': r['path'], 'beforeSha256': r['sha256'], 'afterSha256': sha(src / r['path'])}
                   for r in first if sha(src / r['path']) != r['sha256']]
        if any(r['path'].lower().endswith('.prj') for r in changes):
            raise ValueError('PRJ alterado durante consulta')
        prj = next(src.rglob('*.prj'))
        session = json.loads((OUT / f'{branch}-sessao-tempo.json').read_text(encoding='utf-8-sig'))
        if session['wallMs'] <= 0:
            raise ValueError('Duracao invalida')
        branches[branch] = {'projectPath': str(prj), 'projectSha256': sha(prj), 'readings': readings,
                            'auxiliaryChangesDuringConsultation': changes,
                            'prjUnchangedDuringConsultation': True, 'sessionTime': session}
    comparisons = []
    for cad, bim in zip(branches['CAD']['readings'], branches['BIM']['readings']):
        assert (cad['support'], cad['action']) == (bim['support'], bim['action'])
        for component in COMPONENTS:
            comparisons.append({'support': cad['support'], 'action': cad['action'], 'component': component,
                                'CAD': cad['components'][component], 'BIM': bim['components'][component],
                                'equalDisplayed': cad['components'][component] == bim['components'][component]})
    if not all(r['equalDisplayed'] for r in comparisons):
        raise ValueError('Ramos divergem na releitura')
    frozen = OUT / 'congelados-apos-releitura'
    frozen.mkdir()
    for branch in branches:
        src = Path(branches[branch]['projectPath']).parents[1]
        dst = frozen / branch
        shutil.copytree(src, dst)
        hashes = [{'path': p.relative_to(src).as_posix(), 'sha256': sha(p)}
                  for p in sorted(src.rglob('*')) if p.is_file()]
        if not all(sha(dst / r['path']) == r['sha256'] for r in hashes):
            raise ValueError('Congelamento divergente')
        branches[branch]['frozenFiles'] = hashes
    result = {'revision': 'H03/R115', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
              'hypothesisId': 'P2-GRAV-A', 'branches': branches, 'pairedComponentComparisons': comparisons,
              'protectedSourceR109Files': protected, 'sourceR109FilesUnchanged': True,
              'nativeLoadApplicationPerformed': True, 'saveCloseReopenReadbackPerformed': True,
              'processingPerformed': False, 'finalStructuralApproval': False, 'finalTimeRankingAllowed': False,
              'comparisonPrecision': 'Valores exibidos na interface: Fz reaberto arredondado a seis algarismos significativos neste ensaio; nao afirmar igualdade binaria interna dos valores.',
              'otherRoofNodesReauditedInR115': False,
              'limits': ['Hipotese gravitacional parcial; metal e ligacoes nao dimensionados.',
                         'Agua, tara e apoio do reservatorio excluidos; nao assumir ausencias como zero fisico.',
                         'RP2-04 conserva My da varanda e soma Fz P2; demais nos nao foram todos relidos.',
                         'Sem processamento nesta revisao; resultados antigos nao representam R115.',
                         'Tempos de sessao incluem interface e evidencias; nao medem inferencia IA ou produtividade pura.',
                         'Vento/succao, caso localizado de manutencao e demais cargas e combinacoes nao encerrados.']}
    (OUT / 'R115-resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'protectedFiles': len(protected), 'pairedComponents': len(comparisons),
                      'equalDisplayed': sum(r['equalDisplayed'] for r in comparisons),
                      'frozenFiles': {b: len(v['frozenFiles']) for b, v in branches.items()}}))


if __name__ == '__main__':
    main()

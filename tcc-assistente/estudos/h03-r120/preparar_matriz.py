"""Matriz geométrica de paredes: conserva lacunas e não edita modelo nativo."""
import csv
import hashlib
import json
import math
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
STUDIES = HERE.parent
OUT = Path('D:/TCC/outputs/Paredes-H03-R120-MATRIZ-NAO-APLICADO')
INPUTS = {
    'walls': STUDIES / 'h03-r55/R55-paredes-referencia.json',
    'segments': STUDIES / 'h03-r56/R56-paredes-trechos.json',
    'geometry': STUDIES / 'h03-r56/R56-geometria-exportada.json',
    'openings': STUDIES / 'h03-r67/R67-aberturas-e-massas-condicionais.json',
    'doorCorrection': STUDIES / 'h03-r68/R68-resultado.json',
    'stairFacade': STUDIES / 'h03-r70/R70-W08-J4.json',
    'materialHypothesis': STUDIES / 'h03-r97/R97-base-materiais-paredes.json',
}
SURFACE = 1.565  # Hipótese acadêmica R55/R97, não produto aferido.
EPS = 1e-7


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def overlap(a, b, c, d): return max(0.0, min(b, d) - max(a, c))


def resolve_support(segment, geometry, branch):
    """Em cruzamentos, prioriza viga paralela; não prova contato analítico."""
    if segment['route'] != 'viga':
        return None
    p1, p2 = segment['p1'], segment['p2']
    axis = 0 if abs(p1[1] - p2[1]) < EPS else 1
    mid = [(a + b) / 2 for a, b in zip(p1, p2)]
    names = segment['lowerNativeNames' if branch == 'CAD' else 'lowerNativeNamesBIM']
    candidates = [r for r in geometry[branch] if r['type'] == 'IfcBeam' and r['name'] in names
                  and abs(r['max'][2] - 3.2) < EPS
                  and all(r['min'][i] - EPS <= mid[i] <= r['max'][i] + EPS for i in [0, 1])]
    parallel = [r for r in candidates if (0 if r['max'][0] - r['min'][0] > r['max'][1] - r['min'][1] else 1) == axis]
    chosen = parallel or candidates
    if len(chosen) != 1:
        raise ValueError(f'Apoio não unívoco {segment["wallId"]}/{branch}: {len(chosen)}')
    r = chosen[0]
    return {'name': r['name'], 'guidR56': r['guid'], 'minR56': r['min'], 'maxR56': r['max'],
            'parallelToWall': bool(parallel), 'otherIntersectingBeamNames': sorted(set(names) - {r['name']}),
            'selectionIsGeometricOnly': True}


def prepare(walls, segments, geometry, old, correction):
    if len(walls) != 20 or len(segments) != 59:
        raise ValueError('Conjunto de referência incompleto')
    openings = [dict(o) for o in old['openings']]
    if len(openings) != len({o['id'] for o in openings}):
        raise ValueError('Abertura repetida')
    updated = next(o for o in openings if o['id'] == correction['openingId'])
    updated['nominalStartM'], updated['nominalEndM'] = correction['updatedNominalLocalIntervalM']
    updated['positionSource'] = 'R68, largura nominal centrada na leitura vetorial do vão claro'
    updated['nominalColumnOverlapWidthM'] = correction['updatedNominalClearOverlapM']
    for wall in walls:
        oo = [o for o in openings if o['wallId'] == wall['id']]
        for i, a in enumerate(oo):
            for b in oo[i + 1:]:
                if overlap(a['nominalStartM'], a['nominalEndM'], b['nominalStartM'], b['nominalEndM']) > EPS:
                    raise ValueError('Vãos sobrepostos exigem união explícita')
    matrix, summaries, simple = [], [], []
    for index, segment in enumerate(segments, 1):
        s = dict(segment)
        wall = next(w for w in walls if w['id'] == s['wallId'])
        oo = [o for o in openings if o['wallId'] == s['wallId']]
        column = s['route'] == 'coluna-sem-alvenaria'
        height = s['grossHeightReferenceM']
        gross = s['lengthM'] * height if height is not None and not column else (0.0 if column else None)
        deductions = []
        if gross is not None and not column:
            for o in oo:
                if o['heightM'] > height + EPS:
                    raise ValueError('Vão excede faixa de alvenaria')
                width = overlap(s['fromM'], s['toM'], o['nominalStartM'], o['nominalEndM'])
                if width > EPS:
                    deductions.append({'openingId': o['id'], 'widthOverMasonryM': width,
                                       'conditionalAreaM2': width * o['heightM'],
                                       'verticalFitKnown': o['verticalFitFromAvailableData'],
                                       'openingPositionSource': o.get('positionSource', 'R34/R67, aproximada')})
        deduction = sum(d['conditionalAreaM2'] for d in deductions)
        net = gross - deduction if gross is not None else None
        if net is not None and net < -EPS:
            raise ValueError('Área negativa')
        supports = {b: resolve_support(s, geometry, b) for b in ['CAD', 'BIM']} if s['route'] == 'viga' else None
        if supports:
            if supports['CAD']['minR56'] != supports['BIM']['minR56'] or supports['CAD']['maxR56'] != supports['BIM']['maxR56']:
                raise ValueError('Caixas dos apoios não correspondem')
        reasons = ['Hipótese de composição sem ensaio/fabricante; conferir faces e encontros.',
                   'Geometria R56 preservada em R57; não se exportou IFC dos receptores atuais nesta etapa.']
        if oo: reasons.append('Transferência ao redor dos vãos, vergas e tara de esquadrias não resolvidas.')
        if s['route'] == 'laje': reasons.append('Carga de linha sobre laje; não espalhar como G2 uniforme sem justificar o caminho.')
        if supports and not supports['CAD']['parallelToWall']:
            reasons.append('Contato com viga transversal no encontro; partilha com laje não definida.')
        if s['wallId'] == 'W08': reasons.append('Fachada contínua J4; suporte e parcela transmitida à superestrutura indefinidos, conforme R70.')
        record = {**s, 'segmentId': f'R120-S{index:02d}', 'supportSelectionR120': supports,
                  'grossMasonryAreaM2': gross, 'openingDeductions': deductions,
                  'conditionalNetMasonryAreaM2': net,
                  'conditionalNetMasonryWeightMagnitudeKN': None if net is None else net * SURFACE,
                  'fullHeightLineWeightMagnitudeKNm': None if column or height is None else height * SURFACE,
                  'allWallOpeningIds': [o['id'] for o in oo],
                  'extraWeightOfJoineryLintelsFinishesOnConcreteKN': None,
                  'analyticalLoadPathVerified': False, 'nativeSignedInputValue': None,
                  'nativeLinearSignConventionVerified': False, 'applicationBlockReasons': reasons,
                  'readyForNativeApplication': False, 'appliedToNative': False}
        matrix.append(record)
    for wall in walls:
        rows = [r for r in matrix if r['wallId'] == wall['id']]
        if not math.isclose(sum(r['lengthM'] for r in rows), wall['lengthBetweenAxesM'], abs_tol=1e-6):
            raise ValueError('Partição não fecha')
        known = all(r['grossMasonryAreaM2'] is not None for r in rows)
        gross = sum(r['grossMasonryAreaM2'] for r in rows) if known else None
        net = sum(r['conditionalNetMasonryAreaM2'] for r in rows) if known else None
        previous = next(r for r in old['walls'] if r['wallId'] == wall['id'])
        row = {'wallId': wall['id'], 'name': wall['name'], 'openingIds': [o['id'] for o in openings if o['wallId'] == wall['id']],
               'routes': sorted(set(r['route'] for r in rows if r['route'] != 'coluna-sem-alvenaria')),
               'grossMasonryAreaM2': gross, 'conditionalNetMasonryAreaM2': net,
               'conditionalWeightMagnitudeKN': net * SURFACE if net is not None else None,
               'previousConditionalNetAreaR67M2': previous['conditionalNetMasonryAreaM2'],
               'deltaConditionalAreaFromR67M2': net - previous['conditionalNetMasonryAreaM2'] if net is not None else None,
               'readyForNativeApplication': False}
        summaries.append(row)
        active = [r for r in rows if r['route'] != 'coluna-sem-alvenaria']
        if not row['openingIds'] and known and all(r['route'] == 'viga' and r['supportSelectionR120']['CAD']['parallelToWall'] for r in active):
            simple.append({'wallId': wall['id'], 'segments': [r['segmentId'] for r in active],
                           'pointsXYM': [active[0]['p1'], active[-1]['p2']],
                           'weightMagnitudeKN': sum(r['conditionalNetMasonryWeightMagnitudeKN'] for r in active),
                           'lineWeightMagnitudeKNm': active[0]['fullHeightLineWeightMagnitudeKNm'],
                           'supports': active[0]['supportSelectionR120'], 'proposedAction': 'Adicional',
                           'requiresNodesOrExactSegmentDefinition': True, 'nativeSignedInputValue': None,
                           'isPriorityCandidateOnly': True, 'readyForNativeApplication': False})
    return {'segments': matrix, 'walls': summaries, 'openingsWithR68Position': openings,
            'priorityUnopenedParallelBeamWalls': simple,
            'segmentRouteCounts': dict(Counter(r['route'] for r in matrix)),
            'ambiguousCrossingsGeometricallyResolved': sum(bool(r['supportSelectionR120'] and r['supportSelectionR120']['CAD']['otherIntersectingBeamNames']) for r in matrix),
            'unknownWallIds': [r['wallId'] for r in summaries if r['conditionalNetMasonryAreaM2'] is None]}


def figure(walls, segments, target):
    sys.path.insert(0, 'D:/TCC/work/plot-deps')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    fig, ax = plt.subplots(figsize=(10, 7.5))
    for w in walls:
        if w['id'] == 'W08': color = '#b42318'
        elif any(s['route'] == 'laje' for s in segments if s['wallId'] == w['id']): color = '#7a3e9d'
        elif w['openingReferencesR34']: color = '#b45b00'
        else: color = '#066a9b'
        ax.plot([w['x'], w['x2']], [w['y'], w['y2']], color=color, lw=5, solid_capstyle='butt')
        mid = [(w['x'] + w['x2']) / 2, (w['y'] + w['y2']) / 2]
        dx, dy = (0.2, 0) if w['x'] == w['x2'] else (0, 0.18)
        ax.text(mid[0]+dx, mid[1]+dy, w['id'], fontsize=9, color=color, weight='bold',
                bbox={'facecolor': 'white', 'alpha': 0.85, 'edgecolor': 'none', 'pad': 1})
    for s in segments:
        if s['route'] == 'coluna-sem-alvenaria':
            ax.plot([s['p1'][0], s['p2'][0]], [s['p1'][1], s['p2'][1]], color='#555555', lw=5)
    labels = [('Sem vão na referência / sobre viga', '#066a9b'), ('Com abertura na referência', '#b45b00'),
              ('Contém trecho sobre laje', '#7a3e9d'), ('W08: apoio indefinido', '#b42318'), ('Trecho de pilar excluído da alvenaria', '#555555')]
    ax.legend(handles=[Line2D([0], [0], color=c, lw=4, label=l) for l,c in labels], loc='upper left', bbox_to_anchor=(1.02,1), frameon=False, fontsize=9)
    ax.set(xlabel='X nominal (m)', ylabel='Y nominal (m)', title='H03/R120 — paredes superiores e tipos de apoio\nReferência R56/R57; triagem, sem lançamento de cargas')
    ax.set_aspect('equal'); ax.set_xlim(-0.6, 10.3); ax.set_ylim(-0.65, 7.65)
    ax.grid(alpha=0.2); fig.tight_layout(); fig.savefig(target, dpi=170, bbox_inches='tight'); plt.close(fig)


def main():
    if OUT.exists(): raise FileExistsError('Não substituir estudo')
    start = time.perf_counter(); utc = datetime.now(timezone.utc).isoformat()
    source_hashes = {k: sha(p) for k,p in INPUTS.items()}
    data = {k: json.loads(p.read_text(encoding='utf-8-sig')) for k,p in INPUTS.items()}
    result = prepare(data['walls']['walls'], data['segments']['segments'], data['geometry'], data['openings'], data['doorCorrection'])
    result.update({'revision': 'H03/R120', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
                   'sources': [{'key': k, 'path': str(p), 'sha256': source_hashes[k]} for k,p in INPUTS.items()],
                   'geometrySource': 'R56 com preservação verificada na R57; não nova exportação atual.',
                   'areaWeightHypothesisKNm2': SURFACE, 'wallCompositionManufacturerConfirmed': False,
                   'nativeFilesEdited': False, 'loadsApplied': False, 'processingPerformed': False,
                   'monographEdited': False, 'structuralApproval': False, 'finalWholeBuildingWeightKN': None,
                   'priorityCandidateSubtotalMagnitudeKN': sum(r['weightMagnitudeKN'] for r in result['priorityUnopenedParallelBeamWalls']),
                   'notes': ['Áreas líquidas condicionadas ao encaixe vertical dos vãos; peitoris J1 desconhecidos não foram inventados.',
                             'Não inclui tara/vergas, acabamentos sobre concreto, correção volumétrica dos encontros, paredes térreas ou platibandas.',
                             'Prioridade geométrica em cruzamento não comprova repartição de reações ou vínculo analítico.',
                             'Não converter massa de parede com vão em carga uniforme: verga e ombreiras redistribuem ações.',
                             'Não lançar sobre a extensão integral da viga: intervalos livres de pilares exigem nós/trechos exatos.',
                             'Não aplicar a convenção de Fz nodal negativo a cargas lineares sem conferir o diálogo.',
                             'Não se validou vigência normativa por catálogo nesta etapa.']})
    for k,p in INPUTS.items():
        if sha(p) != source_hashes[k]: raise ValueError('Fonte modificada')
    OUT.mkdir()
    (OUT / 'R120-matriz.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    with (OUT / 'R120-paredes-resumo.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer=csv.DictWriter(f, fieldnames=list(result['walls'][0]), delimiter=';')
        writer.writeheader(); writer.writerows(result['walls'])
    figure(data['walls']['walls'], result['segments'], OUT / 'R120-mapa-paredes.png')
    (OUT / 'R120-tempo-script.json').write_text(json.dumps({'startedAtUtc': utc, 'endedAtUtc': datetime.now(timezone.utc).isoformat(),
        'elapsedMs': (time.perf_counter()-start)*1000, 'scope': 'Somente execução do script e renderização da figura; não tempo de autoria, IA total ou fluxo CAD/BIM.',
        'branch': None, 'allowsFinalFlowRanking': False}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'walls': len(result['walls']), 'segments': len(result['segments']),
        'crossingsResolved': result['ambiguousCrossingsGeometricallyResolved'],
        'priority': [r['wallId'] for r in result['priorityUnopenedParallelBeamWalls']],
        'prioritySubtotalKN': result['priorityCandidateSubtotalMagnitudeKN'],
        'updatedW18': next(w for w in result['walls'] if w['wallId']=='W18')}, ensure_ascii=False))


if __name__ == '__main__': main()

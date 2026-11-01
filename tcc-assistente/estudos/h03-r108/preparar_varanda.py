"""Hipotese de sensibilidade para P1: transferencia excentrica sem omitir momentos."""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

ROOT = Path('D:/TCC')
OUT = ROOT / 'outputs/Varanda-H03-R108-HIPOTESE-NAO-EXECUTAR'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transferred_load(load_per_area, x0=9.65, x1=10.65, y0=3.9, y1=7.05):
    """Duas resultantes iguais na borda interna; momento transportado r x F."""
    if not all(math.isfinite(v) for v in [load_per_area, x0, x1, y0, y1]) or load_per_area <= 0 or x1 <= x0 or y1 <= y0:
        raise ValueError('Carga e geometria invalidas')
    area = (x1-x0)*(y1-y0)
    force = load_per_area*area/2
    eccentricity = (x1-x0)/2
    return [{'xM': x0, 'yM': y, 'FxKN': 0, 'FyKN': 0, 'FzKN': -force,
             'MxKNm': 0, 'MyKNm': force*eccentricity, 'MzKNm': 0} for y in [y0, y1]]


def total_effect(nodes):
    # Momento da forca vertical em torno da origem + binario transportado.
    return {'FzKN': sum(n['FzKN'] for n in nodes),
            'MxKNm': sum(n['yM']*n['FzKN'] + n['MxKNm'] for n in nodes),
            'MyKNm': sum(-n['xM']*n['FzKN'] + n['MyKNm'] for n in nodes)}


def main():
    start = perf_counter()
    OUT.mkdir(exist_ok=False)
    roof_path = ROOT / 'outputs/Cobertura-H03-R59-MEMORIA-ESTUDO-NAO-EXECUTAR/R59-memoria-cobertura.json'
    geometry_path = ROOT / 'outputs/Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR/R56-geometria-exportada.json'
    arrangement_path = ROOT / 'outputs/Cobertura-H03-R60-REACOES-PARCIAIS-NAO-EXECUTAR/R60-arranjo-reacoes.json'
    roof = json.loads(roof_path.read_text(encoding='utf-8-sig'))
    geometry = json.loads(geometry_path.read_text(encoding='utf-8-sig'))
    arrangement = json.loads(arrangement_path.read_text(encoding='utf-8-sig'))
    if sha(geometry_path) != arrangement['geometrySource']['sha256']:
        raise ValueError('Geometria historica divergente')
    planes = {p['id']: p for p in arrangement['planes']}
    if planes['P1']['box'] != [9.65, 3.9, 10.65, 7.05]:
        raise ValueError('P1 diferente do recorte esperado')
    loads = {'G_ADICIONAL': roof['loads']['roofPermanentHorizontalKNm2'],
             'Q_TELHADO_MANUTENCAO': roof['loads']['roofMaintenanceHorizontalKNm2']}
    actions = {}
    for name, value in loads.items():
        nodes = transferred_load(value)
        for i, n in enumerate(nodes, 1):
            n['id'] = f'VP1-{i:02d}'
            n['targetsHistoricalR56'] = {}
            for branch, elements in geometry.items():
                candidates = [e for e in elements if e['type'] == 'IfcColumn' and abs(e['max'][2]-6.39) < 1e-6
                              and e['min'][0] <= n['xM'] <= e['max'][0] and e['min'][1] <= n['yM'] <= e['max'][1]]
                if len(candidates) != 1:
                    raise ValueError('Alvo historico nao unico')
                n['targetsHistoricalR56'][branch] = candidates[0]
        total = value*3.15
        analytic = {'FzKN': -total, 'MxKNm': -total*5.475, 'MyKNm': total*10.15}
        effect = total_effect(nodes)
        if any(abs(effect[k]-analytic[k]) > 1e-9 for k in analytic):
            raise ValueError('Equilibrio global de forca/momentos divergente')
        actions[name] = {'loadHorizontalKNm2': value, 'nodes': nodes, 'equivalentResultantAtRoofCentroid': analytic,
                         'transportedResultant': effect, 'equilibriumPassed': True}
    result = {'revision': 'H03/R108', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
              'hypothesisId': 'VP1-A', 'status': 'Alternativa de sensibilidade; nao solucao dimensionada ou aprovada',
              'roofAreaP1M2': 3.15, 'roofBoxM': [9.65, 3.9, 10.65, 7.05],
              'concept': 'Dois bracos metalicos em balanco X, nas extremidades Y3,90/7,05, recebem uma barra longitudinal Y no centro X10,15 da faixa. Resultantes transportadas aos nos X9,65.',
              'actions': actions, 'forcesAreLoadsOnConcreteNotSupportReactionsOnSteel': True,
              'supportTopReferenceM': 6.39, 'referenceIsExistingConcreteTopNotNewRoofAbsoluteLevel': True,
              'sources': [{'path': str(p), 'sha256': sha(p)} for p in [roof_path, geometry_path, arrangement_path]],
              'operationalSource': 'https://suporte.altoqi.com.br/hc/pt-br/articles/115003467013',
              'geometryMustBeCheckedInCurrentNativeCopy': True, 'nativeApplicationPerformed': False,
              'p2RoofAndReservoirIncluded': False, 'steelWeightAllowanceKNm2': 0.15,
              'steelWeightAllowanceIsNotMemberTakeoff': True, 'metalAndAnchorsDesigned': False,
              'finalStructuralApproval': False,
              'limits': ['Nao aumentar a area A1/A2 nem substituir suas13 cargas; VP1 e parcela adicional distinta.',
                         'Nao omitir My ao transportar carga excentrica. Nao inverter sinal confundindo carga no concreto com reacao sobre metal.',
                         'Momentos sao em eixos globais, em kN.m; confirmar unidades no receptor instalado.',
                         'Barras, ancoragens, estabilidade lateral, vento/succao e compatibilidade altimetrica nao dimensionados.',
                         'Nao declarou viavel o sistema metalico nem a capacidade dos nos de concreto.',
                         'P2, reservatorio, paredes, escada e demais cargas continuam separados e pendentes.']}
    (OUT/'R108-plano-varanda.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT/'R108-tempo-script.json').write_text(json.dumps({'recordedAtUtc': result['createdAtUtc'], 'durationMs': (perf_counter()-start)*1000,
                                                       'scope': 'Somente script aritmetico; nao tempo de autoria ou esforco total IA'}, indent=2), encoding='utf-8')
    print(json.dumps({'areaM2': 3.15, 'actions': {k: {'eachFzKN': v['nodes'][0]['FzKN'], 'eachMyKNm': v['nodes'][0]['MyKNm']} for k,v in actions.items()}, 'nativeApplicationPerformed': False}))


if __name__ == '__main__':
    main()

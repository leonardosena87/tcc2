"""Conferencia offline de entradas QT. Nao edita PRJ nem valida a estrutura."""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import argparse
import csv
import hashlib
import json
import re

Q_HASH = '60f7b24d363808ccaf3cad5243a39cda7913034f8bc038d31be2305b0c04999a'
TOL = Decimal('0.0000051')  # precisao da leitura nativa, nao tolerancia estrutural
ACTION = 'Q_TELHADO_MANUTENCAO'
FIELDS = ('X', 'Y', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dec(value):
    d = Decimal(str(value))
    if not d.is_finite():
        raise ValueError('Valor nao finito')
    return d


def build_plan(qpath, gcad_path, gbim_path):
    if sha(qpath) != Q_HASH:
        raise ValueError('O plano R65 nao corresponde ao exemplar congelado')
    q, cad, bim = map(read, (qpath, gcad_path, gbim_path))
    if cad['branch'] != 'CAD' or bim['branch'] != 'BIM':
        raise ValueError('Identificacao de ramo G incorreta')
    gids = {b: {r['id']: r for r in data['rows']} for b, data in [('CAD', cad), ('BIM', bim)]}
    ids = [r['id'] for r in q['nodes']]
    if len(ids) != 13 or len(set(ids)) != 13:
        raise ValueError('Esperados 13 pontos distintos')
    coords = [(r['xCm'], r['yCm']) for r in q['nodes']]
    if len(set(coords)) != 13 or any(set(gids[b]) != set(ids) for b in gids):
        raise ValueError('Pontos Q/G incompletos ou coordenadas duplicadas')
    rows = []
    for n in q['nodes']:
        a, b = (gids[k][n['id']] for k in ('CAD', 'BIM'))
        if (not a['passed'] or not b['passed'] or a['observed'] != b['observed']
                or a['expected'] != b['expected']):
            raise ValueError('G historico divergente entre ramos: ' + n['id'])
        for r in (a, b):
            if r['observed']['X'] != n['xCm'] or r['observed']['Y'] != n['yCm']:
                raise ValueError('Coordenadas Q/G divergentes: ' + n['id'])
            if r['expected']['action'] != 'Adicional':
                raise ValueError('Acao G de origem inesperada')
            if abs(dec(r['observed']['Fz']) - dec(r['expected']['fzKN'])) > TOL:
                raise ValueError('G historico fora da precisao de leitura')
            if any(dec(r['observed'][f]) != 0 for f in ('Fx','Fy','Mx','My','Mz')):
                raise ValueError('G historico tem componente adicional')
        force, entered = dec(n['proposedFzKN']), dec(n['proposedInputFzKN'])
        if force >= 0 or force.quantize(Decimal('.000001'), rounding=ROUND_HALF_UP) != entered:
            raise ValueError('Sinal ou arredondamento QT divergente')
        rows.append(dict(id=n['id'], xCm=n['xCm'], yCm=n['yCm'], action=ACTION,
                         qtFzKN=float(entered), gAction='Adicional',
                         gFzKN=a['expected']['fzKN'],
                         historicalDisplayedGFzKN=a['observed']['Fz'],
                         nativeTargets=n['nativeTargets'], currentQTVerified=False,
                         currentGPreservationVerified=False))
    down = -sum(dec(n['proposedFzKN']) for n in q['nodes'])
    mx = -sum(dec(n['proposedFzKN']) * dec(n['xCm']) / 100 for n in q['nodes'])
    my = -sum(dec(n['proposedFzKN']) * dec(n['yCm']) / 100 for n in q['nodes'])
    entered_down = -sum(dec(r['qtFzKN']) for r in rows)
    if abs(down - dec(q['qHorizontalKNm2']) * dec(q['areaNominalAxesM2'])) > Decimal('1e-10'):
        raise ValueError('Desequilibrio entre resultante e integral de area')
    for actual, name in ((down, 'downKN'), (mx, 'firstMomentXKNm'), (my, 'firstMomentYKNm')):
        if abs(actual - dec(q['equilibrium'][name])) > Decimal('1e-10'):
            raise ValueError('Integral divergente: ' + name)
    return dict(schema='tcc-qt-check-plan/1', revision='H03/R98', rows=rows,
                sourceHashes=dict(q=sha(qpath), gCAD=sha(gcad_path), gBIM=sha(gbim_path)),
                analyticalDownKN=float(down), enteredDownKN=float(entered_down),
                roundingDeltaKN=float(entered_down-down), firstMomentXKNm=float(mx),
                firstMomentYKNm=float(my), nativeReadToleranceKN=float(TOL),
                excludedRoofPlanes=q['excludedRoofPlanes'],
                nativeLoadsAppliedByThisScript=False, structuralProcessingPerformed=False,
                completeRoofCase=False, structuralApproval=False, fullFlowRankingAllowed=False)


def parse_native(text):
    """Duplicacao identica na arvore e permitida; valores conflitantes sao recusados."""
    values = {}
    for field in FIELDS:
        hits = re.findall(r'\b' + field + r' Value: ([^\s]+)', text)
        if not hits:
            raise ValueError('Campo nativo ausente: ' + field)
        numbers = {dec(x.replace(',', '.')) for x in hits}
        if len(numbers) != 1:
            raise ValueError('Leitura ambigua: ' + field)
        values[field] = numbers.pop()
    actions = {m.strip() for m in re.findall(r'Ação Value: ([^\r\n]+)', text)}
    actions = {re.sub(r' ID: [^\s]+$', '', m) for m in actions}
    if len(actions) != 1:
        raise ValueError('Acao ausente ou ambigua')
    # Vincula cada unidade a linha imediatamente posterior ao seu controle.
    for field in ('Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'):
        unit = 'kN' if field.startswith('F') else 'kN.m'
        pattern = r'\b' + field + r' Value: [^\r\n]+\r?\n[^\r\n]*\btext ([^\s]+) ID:'
        units = set(re.findall(pattern, text))
        if units != {unit}:
            raise ValueError('Unidade nao comprovada para ' + field)
    return values, actions.pop()


def check_native(text, point, phase, branch):
    if phase not in ('G', 'QT') or branch not in ('CAD', 'BIM'):
        raise ValueError('Fase/ramo invalido')
    title = f'{14 if branch == "CAD" else 15}-H03-R98-{branch}-QT-NAO-EXECUTAR'
    if title not in text:
        raise ValueError('Leitura nao identifica a copia R98 esperada')
    values, action = parse_native(text)
    wanted_action = point['gAction'] if phase == 'G' else point['action']
    if action != wanted_action:
        raise ValueError('Acao divergente: ' + action)
    if values['X'] != dec(point['xCm']) or values['Y'] != dec(point['yCm']):
        raise ValueError('Coordenadas divergentes')
    wanted_fz = point['gFzKN'] if phase == 'G' else point['qtFzKN']
    if abs(values['Fz'] - dec(wanted_fz)) > TOL:
        raise ValueError('Fz divergente')
    if any(values[f] != 0 for f in ('Fx', 'Fy', 'Mx', 'My', 'Mz')):
        raise ValueError('Componente adicional nao prevista')
    return dict(id=point['id'], branch=branch, phase=phase, action=action,
                observed={k: float(v) for k, v in values.items()}, matched=True)


def audit_reads(plan, root):
    """Usa somente arquivos *-apos-reabrir-UI.txt; ausencia nunca vira aprovacao."""
    rows = []
    for branch in ('CAD', 'BIM'):
        for p in plan['rows']:
            for phase in ('G', 'QT'):
                path = Path(root) / f'{branch}-{p["id"]}-{phase}-apos-reabrir-UI.txt'
                row = dict(branch=branch, id=p['id'], phase=phase, evidence=path.name)
                if not path.is_file():
                    row.update(status='pending', matched=False)
                else:
                    row['sha256'] = sha(path)
                    try:
                        row.update(check_native(path.read_text(encoding='utf-8-sig'), p, phase, branch), status='matched')
                    except (ValueError, ArithmeticError) as error:
                        row.update(status='rejected', matched=False, reason=str(error))
                rows.append(row)
    return dict(rows=rows, expectedReadings=52, matchedReadings=sum(r['matched'] for r in rows),
                pendingReadings=sum(r['status']=='pending' for r in rows),
                rejectedReadings=sum(r['status']=='rejected' for r in rows),
                allReadingsMatched=all(r['matched'] for r in rows),
                saveReopenSequenceProvenByTextAlone=False, structuralApproval=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True, help='Nova pasta; nao sobrescreve saidas')
    ap.add_argument('--reads', type=Path, help='Pasta de leituras reais, opcional')
    args = ap.parse_args()
    studies = Path(__file__).resolve().parent.parent
    plan = build_plan(studies/'h03-r65/R65-plano-Q.json', studies/'h03-r64/R64-leituras-CAD.json',
                      studies/'h03-r64/R64-leituras-BIM.json')
    if args.out.exists():
        raise SystemExit('Saida existente; escolha nova pasta')
    args.out.mkdir(parents=True)
    (args.out/'R98-plano-conferencia.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    with (args.out/'R98-roteiro-conferencia.csv').open('w', encoding='utf-8-sig', newline='') as f:
        cols = ['ramo','ponto','x_cm','y_cm','acao_qt','fz_qt_kN','acao_g','fz_g_kN','qt_relido','g_relido','evidencias']
        writer = csv.writer(f, delimiter=';'); writer.writerow(cols)
        for branch in ('CAD','BIM'):
            for p in plan['rows']:
                writer.writerow([branch,p['id'],p['xCm'],p['yCm'],p['action'],p['qtFzKN'],p['gAction'],p['gFzKN'],'PENDENTE','PENDENTE',''])
    if args.reads:
        result = audit_reads(plan, args.reads)
        (args.out/'R98-auditoria-leituras.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
    print(json.dumps({k:v for k,v in plan.items() if k!='rows'}, ensure_ascii=False))


if __name__ == '__main__':
    main()

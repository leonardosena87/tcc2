"""Reconcilia prismas IFC fechados e preserva a diferenca de agrupamento."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter, defaultdict
import hashlib
import json
import math
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'h03-r182'))
from consolidar_diagnostico import prism_signature

OUT = Path('D:/TCC/outputs/Comparacao-H03-R185-AGRUPAMENTO-VIGAS-NAO-EXECUTAR')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def normalize_level(name):
    match = re.search(r'(N[012])$', name or '')
    if not match:
        raise ValueError('Pavimento nao identificado: ' + str(name))
    return match[1]


def group(row):
    return row['level'], row['name']


def validate_rows(rows):
    guids = set()
    signatures = set()
    for row in rows:
        sig = row['signature']
        if not row.get('closedPrismValidated'):
            raise ValueError('Bounding box sem validacao de prisma')
        if len(sig) != 6 or not all(math.isfinite(x) for x in sig):
            raise ValueError('Assinatura invalida')
        if any(sig[k+3] <= sig[k] for k in range(3)):
            raise ValueError('Dimensao nula ou negativa')
        if not row['name'] or row['level'] not in ('N0', 'N1', 'N2'):
            raise ValueError('Grupo sem identificacao')
        if row['guid'] in guids or sig in signatures:
            raise ValueError('Correspondencia ambigua: GUID ou prisma duplicado')
        guids.add(row['guid'])
        signatures.add(sig)


def reconcile(cad, bim):
    validate_rows(cad)
    validate_rows(bim)
    by_cad = {x['signature']: x for x in cad}
    by_bim = {x['signature']: x for x in bim}
    pairs = []
    adjacency = defaultdict(set)
    for sig in sorted(by_cad.keys() & by_bim.keys()):
        a, b = by_cad[sig], by_bim[sig]
        node_a = ('CAD', *group(a))
        node_b = ('BIM', *group(b))
        adjacency[node_a].add(node_b)
        adjacency[node_b].add(node_a)
        pairs.append(dict(cadGuid=a['guid'], bimGuid=b['guid'], cadName=a['name'],
            bimName=b['name'], cadLevel=a['level'], bimLevel=b['level'],
            levelsMatch=a['level'] == b['level'], minM=list(sig[:3]), maxM=list(sig[3:]),
            equalClosedPrismAt1eMinus7M=True,
            volumeM3=math.prod(sig[k+3]-sig[k] for k in range(3))))
    components = []
    visited = set()
    for node in sorted(adjacency):
        if node in visited:
            continue
        stack = [node]
        nodes = set()
        while stack:
            current = stack.pop()
            if current in nodes:
                continue
            nodes.add(current)
            stack.extend(adjacency[current] - nodes)
        visited.update(nodes)
        ag = sorted([x[1:] for x in nodes if x[0] == 'CAD'])
        bg = sorted([x[1:] for x in nodes if x[0] == 'BIM'])
        members = [p for p in pairs if (p['cadLevel'], p['cadName']) in ag]
        components.append(dict(cadGroups=ag, bimGroups=bg, matchedPhysicalPieces=len(members),
            groupingRelation=('one_to_one' if len(ag) == len(bg) == 1 else
                'multiple_CAD_to_one_BIM' if len(bg) == 1 else
                'one_CAD_to_multiple_BIM' if len(ag) == 1 else 'many_to_many')))
    cad_only = [by_cad[k] for k in sorted(by_cad.keys() - by_bim.keys())]
    bim_only = [by_bim[k] for k in sorted(by_bim.keys() - by_cad.keys())]
    return dict(pairs=pairs, unmatchedCAD=cad_only, unmatchedBIM=bim_only,
        components=components, uniqueOneToOnePhysicalPairing=True,
        allExportedBeamPrismsMatched=not cad_only and not bim_only,
        allMatchedLevelsAgree=all(p['levelsMatch'] for p in pairs))


def read_beams(path):
    sys.path.insert(0, 'D:/TCC/work/ifc/deps')
    import ifcopenshell
    import ifcopenshell.geom
    import numpy as np
    model = ifcopenshell.open(str(path))
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    rows = []
    for element in model.by_type('IfcBeam'):
        # Manter model e shape vivos enquanto se le a geometria nativa.
        shape = ifcopenshell.geom.create_shape(settings, element)
        vertices = np.asarray(shape.geometry.verts).reshape(-1, 3)
        faces = np.asarray(shape.geometry.faces).reshape(-1, 3)
        signature = prism_signature(vertices, faces)
        containers = [x.RelatingStructure for x in element.ContainedInStructure]
        if len(containers) != 1:
            raise ValueError('Viga sem pavimento unico: ' + element.GlobalId)
        rows.append(dict(guid=element.GlobalId, name=element.Name,
            nativeLevelName=containers[0].Name, level=normalize_level(containers[0].Name),
            signature=signature, closedPrismValidated=True))
    validate_rows(rows)
    return rows


def main():
    control = json.loads((HERE.parent / 'h03-r178/R178-comparacao-CAD-BIM.json').read_text(encoding='utf-8'))
    sources, branches = {}, {}
    OUT.mkdir(exist_ok=True)
    for b in ('CAD', 'BIM'):
        entry = control['branches'][b]
        path = Path(entry['ifcPath'])
        if sha(path) != entry['ifcSha256']:
            raise ValueError('IFC fonte alterado: ' + b)
        sources[b] = dict(path=str(path), sha256=sha(path), baselineRevision='H03/R178')
        rows = read_beams(path)
        groups = sorted(set(group(x) for x in rows))
        branches[b] = dict(pieces=rows, exportedPhysicalPieces=len(rows), nativeNameLevelGroups=len(groups),
            groupsPerLevel=dict(Counter(level for level, name in groups)),
            physicalPiecesPerLevel=dict(Counter(x['level'] for x in rows)),
            exportedPrismVolumeSumM3=sum(math.prod(x['signature'][k+3]-x['signature'][k] for k in range(3)) for x in rows),
            volumeIsSumOfPiecesNotUnion=True)
    result = dict(revision='H03/R185', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        sources=sources, branches=branches,
        reconciliation=reconcile(branches['CAD']['pieces'], branches['BIM']['pieces']),
        sourceFilesUnchangedAfterRead=all(sha(x['path']) == x['sha256'] for x in sources.values()),
        closedPrismMethod='8 cantos, 12 triangulos, arestas fechadas, faces planas e areas completas; permite diagonais diferentes',
        coordinateRoundingM=1e-7, roundingIsComputationalNotConstructionTolerance=True,
        exportsAreBaselineR178NotFreshR182OrR184=True,
        fullNativeAnalyticalEquivalence=False, causalAttributionOfD16ToGroupingProven=False,
        correctionRankingValid=False, structuralApproval=False,
        timing=dict(newNativeProcessing=False, nativeSeconds=None, fullFlowMeasured=False))
    (OUT / 'R185-reconciliacao-vigas.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    rows = ['# Correspondência das peças de viga — R178 / auditoria R185', '',
        'Estudo preliminar, não executar. Correspondência geométrica nos IFCs de referência, sem equivalência analítica integral.', '',
        '| Nível CAD | Nome CAD | Nível BIM | Nome BIM | Mínimo X/Y/Z (m) | Máximo X/Y/Z (m) |',
        '|---|---|---|---|---|---|']
    for p in result['reconciliation']['pairs']:
        lo = ' / '.join(f'{x:.7f}'.rstrip('0').rstrip('.') for x in p['minM'])
        hi = ' / '.join(f'{x:.7f}'.rstrip('0').rstrip('.') for x in p['maxM'])
        rows.append(f"| {p['cadLevel']} | {p['cadName']} | {p['bimLevel']} | {p['bimName']} | {lo} | {hi} |")
    rows += ['', '## Agrupamentos conectados', '', '| Grupos CAD | Grupos BIM | Peças correspondentes |', '|---|---|---:|']
    for c in result['reconciliation']['components']:
        ca = ', '.join('/'.join(x) for x in c['cadGroups'])
        bi = ', '.join('/'.join(x) for x in c['bimGroups'])
        rows.append(f"| {ca} | {bi} | {c['matchedPhysicalPieces']} |")
    (OUT / 'R185-correspondencia-vigas.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')
    print(json.dumps(dict(branches={b:{k:v for k,v in r.items() if k != 'pieces'} for b,r in branches.items()},
        pairedPieces=len(result['reconciliation']['pairs']),
        unmatchedCAD=len(result['reconciliation']['unmatchedCAD']), unmatchedBIM=len(result['reconciliation']['unmatchedBIM']),
        relationCounts=dict(Counter(c['groupingRelation'] for c in result['reconciliation']['components']))), ensure_ascii=False))


if __name__ == '__main__':
    main()

"""Classifica ordem I/J sem transformar cargas ou declarar equivalência mecânica."""
import json
from collections import defaultdict, Counter
from comparar import SOURCE, OUT, r122, encode, normalize_value


def groups(model):
    result = defaultdict(list)
    sections = {r['Frame']: r['AnalSect'] for r in model['tables']['FRAME SECTION ASSIGNMENTS']}
    for key, ends in model['frames'].items():
        clean = tuple(tuple(0.0 if v == 0 else v for v in point) for point in ends)
        result[tuple(sorted(clean))].append({'id': key, 'ends': clean, 'section': sections[key]})
    return result


def diagnose(a, b):
    aa, bb = groups(a), groups(b)
    if aa.keys() != bb.keys():
        raise ValueError('Geometrias diferentes; não classificar como mera orientação')
    counts = Counter()
    examples = []
    for ends in sorted(aa):
        left, right = aa[ends], bb[ends]
        if len(left) != 1 or len(right) != 1:
            counts['ambiguousParallelGroups'] += 1
            counts['CADBarsInAmbiguousGroups'] += len(left)
            counts['BIMBarsInAmbiguousGroups'] += len(right)
            continue
        x, y = left[0], right[0]
        same = x['ends'] == y['ends']
        reverse = x['ends'] == tuple(reversed(y['ends']))
        if not same and not reverse:
            raise ValueError('Ordem não corresponde aos mesmos extremos')
        counts['uniquePairs'] += 1
        counts['sameOrder' if same else 'reversedOrder'] += 1
        counts['sectionNameEqualAtSameGeometricPair' if x['section'] == y['section'] else 'differentSectionName'] += 1
        if reverse and len(examples) < 3:
            examples.append({'CAD': x, 'BIM': y})
    return {'counts': dict(counts), 'reversedExamples': examples,
            'loadsTransformed': False, 'localAxesTransformed': False,
            'mechanicalEquivalenceProved': False,
            'causeOfRelativeDisplacementDirectionProved': False}


def main():
    target = OUT / 'R123-orientacao.json'
    if target.exists():
        raise FileExistsError('Diagnóstico já existente')
    models = {}
    for branch in ['CAD', 'BIM']:
        models[branch] = {}
        for p in (SOURCE / ('SAP-' + branch)).glob('*.$2k'):
            kind = 'portico' if p.name.startswith('portico') else ('N1' if '-N1.' in p.name or '_N1.' in p.name else 'N2')
            models[branch][kind] = r122.parse(p.read_text(encoding='cp1252'))
    data = {'revision': 'H03/R123', 'strictComparisonSha256': r122.sha(OUT / 'R123-resultado-final.json'),
            'models': {kind: diagnose(models['CAD'][kind], models['BIM'][kind]) for kind in ['portico', 'N1', 'N2']}}
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({kind: row['counts'] for kind, row in data['models'].items()}))


if __name__ == '__main__':
    main()

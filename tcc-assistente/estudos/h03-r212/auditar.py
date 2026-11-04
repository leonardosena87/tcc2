"""Compara quatro exportações nativas por fluxo; não executa SAP ou dimensiona."""
import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('compare176', HERE.parent / 'h03-r176/comparar_receptores.py')
comp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(comp)


def load_models(root, branch):
    result = {}
    for path in sorted((root / f'{branch}-exportacao').glob('*.$2k')):
        kind = ('portico' if path.name.startswith('portico_') else
                'escada' if path.name.startswith('grelha_SAP2000_escada_') else
                'N1' if path.name.endswith('N1.$2k') else
                'N2' if path.name.endswith('N2.$2k') else None)
        if kind is None or kind in result:
            raise ValueError('Exportação desconhecida ou repetida: ' + path.name)
        result[kind] = (path, comp.sap.parse(path.read_text(encoding='cp1252')))
    if set(result) != {'portico', 'escada', 'N1', 'N2'}:
        raise ValueError('Exportação incompleta: ' + branch)
    return result


def p12_evidence(model):
    xy = (355., 390.)
    joints = {key: point for key, point in model['joints'].items() if point[:2] == xy}
    vertical = [(key, ends) for key, ends in model['frames'].items()
                if ends[0][:2] == ends[1][:2] == xy]
    intervals = sorted((min(a[2], b[2]), max(a[2], b[2])) for _, (a, b) in vertical)
    if intervals != [(0., 20.), (20., 177.4), (177.4, 320.)]:
        raise ValueError('Continuidade P12 inesperada')
    fixed = [r for r in model['tables']['JOINT RESTRAINT ASSIGNMENTS']
             if r['Joint'] in joints]
    if len(fixed) != 1 or joints[fixed[0]['Joint']] != (355., 390., 0.):
        raise ValueError('Apoio P12 ausente ou ambíguo')
    if any(fixed[0][key] != 'YES' for key in ('U1', 'U2', 'U3', 'R1', 'R2', 'R3')):
        raise ValueError('Vínculo P12 diferente do engaste idealizado')
    if any(p[2] > 320 for p in joints.values()):
        raise ValueError('P12 prolongado acima do N1')
    return dict(jointsCm=joints, verticalFramesCm=vertical, restraint=fixed[0],
                continuousAtIntermediateLevel=True, noColumnAboveN1=True,
                geotechnicalValidation=False, baseRestraintIsStudyIdealization=True)


def run(root):
    branches = {b: load_models(root, b) for b in ('CAD', 'BIM')}
    summary = {}
    for kind in ('portico', 'escada', 'N1', 'N2'):
        a, b = [branches[branch][kind][1] for branch in ('CAD', 'BIM')]
        result = comp.compare(a, b)
        differences = result['nodalLoadDifferences']
        delta = dict(
            rows=len(differences),
            unmatched=sum(row['bimMinusCad'] is None for row in differences),
            maxForceDifferenceKgf=max((abs(row['bimMinusCad'][key]) for row in differences
                if row['bimMinusCad'] is not None for key in ('F1', 'F2', 'F3')), default=0),
            maxMomentDifferenceKgfCm=max((abs(row['bimMinusCad'][key]) for row in differences
                if row['bimMinusCad'] is not None for key in ('M1', 'M2', 'M3')), default=0))
        (root / f'R212-comparacao-{kind}.json').write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        summary[kind] = {k: v for k, v in result.items() if k not in ('tables', 'nodalLoadDifferences')}
        summary[kind]['nodalDifferences'] = delta
        summary[kind]['tableCountsAndEquality'] = {
            name: {k: value[k] for k in ('equal', 'cadRows', 'bimRows')}
            for name, value in result['tables'].items()}
        summary[kind]['exports'] = {branch: dict(name=branches[branch][kind][0].name,
            sha256=comp.sha(branches[branch][kind][0])) for branch in branches}
        if kind == 'N1':
            summary[kind]['differentSectionProperties'] = result['tables'][
                'FRAME SECTION PROPERTIES 01 - GENERAL']
    evidence = {branch: p12_evidence(branches[branch]['portico'][1]) for branch in branches}
    output = dict(revision='H03-R212', comparisons=summary, P12=evidence,
                  nativeSAPSolverExecuted=False, fullNativeEquivalenceVerified=False,
                  localAxesReversalsNotSilentlyEquated=True, structuralApproval=False)
    (root / 'R212-auditoria-resumo.json').write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({kind: dict(counts=entry['counts'],
        geometry=entry['frameUndirectedEndpointMultisetsEqual'],
        sections=entry['sectionPropertiesByUndirectedSegmentEqual'],
        nodalDifferences=entry['nodalDifferences']) for kind, entry in summary.items()}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    run(parser.parse_args().folder)

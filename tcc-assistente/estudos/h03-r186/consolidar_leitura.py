"""Compara valores exibidos, sem confundir envoltorias com historicos de esforcos."""
from pathlib import Path
from decimal import Decimal
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys

HERE = Path(__file__).resolve().parent
OUT = Path('D:/TCC/outputs/Comparacao-H03-R186-NOS-V2-NAO-EXECUTAR')
KEYS = ('initialShearMagnitudeKn', 'finalShearMagnitudeKn', 'positiveMdKnM',
        'negativeMdKnM', 'torsionEnvelopeMagnitudeKnM')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def compare_displayed(cad, bim, reverse):
    if set(cad) != set(KEYS) or set(bim) != set(KEYS):
        raise ValueError('Campos ausentes ou inesperados')
    a, b = {k: Decimal(v) for k, v in cad.items()}, {k: Decimal(v) for k, v in bim.items()}
    if not all(x.is_finite() for x in (*a.values(), *b.values())):
        raise ValueError('Valor nao finito')
    if reverse:
        b[KEYS[0]], b[KEYS[1]] = b[KEYS[1]], b[KEYS[0]]
    return dict(equalAtDisplayedPrecision=all(a[k] == b[k] for k in KEYS),
        differencesAtDisplayedPrecision={k: str(a[k] - b[k]) for k in KEYS},
        comparisonIsOfDisplayedMagnitudesAndExtremaNotSignedForceVectors=True,
        exactInternalEqualityOrControllingCombinationNotVerified=True)


def read_reference_supports():
    sys.path.insert(0, 'D:/TCC/work/ifc/deps')
    sys.path.insert(0, str(HERE.parent / 'h03-r182'))
    import ifcopenshell
    import ifcopenshell.geom
    import numpy as np
    from consolidar_diagnostico import prism_signature
    ref = json.loads((HERE.parent / 'h03-r178/R178-comparacao-CAD-BIM.json').read_text(encoding='utf-8'))
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    rows = {}
    sources = {}
    for branch in ('CAD', 'BIM'):
        entry = ref['branches'][branch]
        path = Path(entry['ifcPath'])
        if sha(path) != entry['ifcSha256']:
            raise ValueError('IFC de referencia alterado')
        sources[branch] = dict(path=str(path), sha256=sha(path), revision='H03/R178')
        model = ifcopenshell.open(str(path))
        wanted = {'P2', 'P5', 'P11'} if branch == 'CAD' else {'P4', 'P5', 'P6'}
        selected = {}
        for element in model.by_type('IfcColumn'):
            if element.Name not in wanted:
                continue
            shape = ifcopenshell.geom.create_shape(settings, element)
            vertices = np.asarray(shape.geometry.verts).reshape(-1, 3)
            faces = np.asarray(shape.geometry.faces).reshape(-1, 3)
            if vertices.max(0)[2] > 3.2000001:
                continue
            signature = prism_signature(vertices, faces)
            if element.Name in selected:
                raise ValueError('Pilar de referencia ambiguo')
            selected[element.Name] = dict(guid=element.GlobalId, signature=signature)
        if set(selected) != wanted:
            raise ValueError('Pilar de referencia nao encontrado')
        rows[branch] = selected
    pairs = []
    for cad, bim in (('P2', 'P4'), ('P5', 'P5'), ('P11', 'P6')):
        a, b = rows['CAD'][cad], rows['BIM'][bim]
        if a['signature'] != b['signature']:
            raise ValueError('Pilares correspondentes divergentes')
        pairs.append(dict(cadName=cad, bimName=bim, cadGuid=a['guid'], bimGuid=b['guid'],
            minM=list(a['signature'][:3]), maxM=list(a['signature'][3:]),
            equalClosedPrismInR178Reference=True))
    return dict(pairs=pairs, sources=sources, currentNativeNodePositionsNotIndependentlyExported=True)


def main():
    start = json.loads((OUT / 'R186-inicio.json').read_text(encoding='utf-8'))
    observations = json.loads((HERE / 'observacoes.json').read_text(encoding='utf-8'))
    for b, x in start['sourceProjects'].items():
        if sha(x['path']) != x['sha256']:
            raise ValueError('PRJ mudou durante leitura: ' + b)
    matches = []
    for p in observations['pairing']:
        a = observations['CAD'][p['cadGroup']]['envelope']
        b = observations['BIM'][p['bimGroup']][p['bimSpan']]
        matches.append(dict(p, **compare_displayed(a, b, p['nativeDirectionsReversed'])))
    result = dict(revision='H03/R186', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        sourceProjects=start['sourceProjects'], sourceProjectHashesUnchanged=True,
        observations=observations, displayedEnvelopeComparison=matches,
        supportNamesInR178Reference=read_reference_supports(),
        allTenDisplayedEnvelopeScalarsMatch=all(x['equalAtDisplayedPrecision'] for x in matches),
        nodeTableAggregationDiffers=True, failureMechanismInDetailingNotProven=True,
        newNativeProcessing=False, nativeSeconds=None, fullFlowTimeMeasured=False,
        completeNativeModelEquivalence=False, finalReinforcementReviewed=False,
        structuralApproval=False, fullPairedFlowComparisonFinished=False)
    write(OUT / 'R186-nos-e-envoltorias.json', result)
    pointer = Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    if not (OUT / 'R186-ponteiro-anterior.json').exists():
        shutil.copy2(pointer, OUT / 'R186-ponteiro-anterior.json')
    current = json.loads(pointer.read_text(encoding='utf-8-sig'))
    current.update(latestBeamNodeReadRevision='H03/R186',
        latestBeamNodeReadPath=str(OUT / 'R186-nos-e-envoltorias.json'),
        latestBeamNodeReadSha256=sha(OUT / 'R186-nos-e-envoltorias.json'),
        matchedV2V14DisplayedEnvelopeScalars=10,
        beamNodeAggregationDiffers=True, completeNativeModelEquivalence=False,
        finalReinforcementReviewed=False, fullPairedFlowComparisonFinished=False)
    write(pointer, current)
    write(OUT / 'R186-ponteiro-atualizado.json', current)
    for p in OUT.glob('*-0.png'):
        shutil.copy2(p, HERE / p.name)
    for name in ('R186-inicio.json', 'R186-nos-e-envoltorias.json', 'R186-ponteiro-atualizado.json'):
        shutil.copy2(OUT / name, HERE / name)
    shutil.copy2(HERE / 'LEIA-ME-R186.md', OUT / 'LEIA-ME-R186.md')
    files = [p for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'R186-manifesto.json']
    manifest = dict(revision='H03/R186', files=[dict(relativePath=p.name, bytes=p.stat().st_size,
        sha256=sha(p)) for p in files])
    write(HERE / 'R186-manifesto.json', manifest)
    shutil.copy2(HERE / 'R186-manifesto.json', OUT / 'R186-manifesto.json')
    print(json.dumps(dict(files=len(files), matchedDisplayedScalars=10,
        sourceProjectHashesUnchanged=True, structuralApproval=False)))


if __name__ == '__main__':
    main()

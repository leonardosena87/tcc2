"""Cobertura axial observada no IFC receptor R162, sem editar os controles.

Associa por eixo, topo, seção e limites geométricos dos apoios de extremidade.
Não usa o nome renumerado como identidade e não infere conectividade analítica.
Limitado aos prismas ortogonais deste experimento, explicitamente verificados.
"""
from datetime import datetime, timezone
from itertools import product
import json
import math
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'h03-r161'))
from auditar_exportacao import read, sha, mesh, ifcopenshell
import ifcopenshell.geom

OUT = Path('D:/TCC/outputs/Intercambio-H03-R163-COBERTURA-GEOMETRICA-NAO-EXECUTAR')
R162 = Path('D:/TCC/outputs/Intercambio-H03-R162-SECOES-NOMINAIS-NAO-EXECUTAR')
TOL = 1e-4  # m: 0,1 mm, cobre a precisão observada no receptor; não tolerância normativa


def merge_intervals(intervals, tolerance=TOL):
    merged = []
    for a, b in sorted(intervals):
        if b < a:
            raise ValueError('Intervalo invertido')
        if not merged or a > merged[-1][1] + tolerance:
            merged.append([a, b])
        else:
            merged[-1][1] = max(merged[-1][1], b)
    return merged


def coverage(intervals, start, end, tolerance=TOL):
    """União de projeções, incluindo lacunas; nunca soma trechos sobrepostos."""
    if end <= start:
        raise ValueError('Vão de referência não positivo')
    clipped = [(max(a, start), min(b, end)) for a, b in intervals
               if min(b, end) > max(a, start)]
    merged = merge_intervals(clipped, tolerance)
    cursor = start
    gaps = []
    for a, b in merged:
        if a - cursor > tolerance:
            gaps.append([cursor, a])
        cursor = max(cursor, b)
    if end - cursor > tolerance:
        gaps.append([cursor, end])
    return dict(referenceIntervalM=[start, end], mergedIntervalsM=merged,
                uncoveredIntervalsM=gaps, coveredLengthM=sum(b-a for a, b in merged),
                referenceLengthM=end-start, noGapAboveTolerance=not gaps)


def subtract_intervals(intervals, exclusions, tolerance=TOL):
    result = merge_intervals(intervals, tolerance)
    for lo, hi in merge_intervals(exclusions, tolerance):
        remaining = []
        for a, b in result:
            if hi <= a or lo >= b:
                remaining.append([a,b])
            else:
                if lo-a > tolerance:remaining.append([a,min(lo,b)])
                if b-hi > tolerance:remaining.append([max(hi,a),b])
        result = remaining
    return result


def beam_frame(src):
    a = src['AxisM']
    along = 0 if abs(a[3]-a[0]) > abs(a[4]-a[1]) else 1
    cross = 1-along
    if abs(a[cross+3]-a[cross]) > 1e-8 or abs(a[5]-a[2]) > 1e-8:
        raise ValueError('Viga não horizontal e ortogonal: '+src['Mark'])
    return along, cross, *sorted((a[along], a[along+3]))


def column_box(src):
    """Caixa de coluna retangular ortogonal; não generaliza rotação oblíqua."""
    angle = src.get('RotationRad', 0)
    if abs(math.sin(2*angle)) > 1e-8:
        raise ValueError('Pilar oblíquo exige interseção poligonal: '+src['Mark'])
    c, s = abs(math.cos(angle)), abs(math.sin(angle))
    dx = (c*src['BM']+s*src['HM'])/2
    dy = (s*src['BM']+c*src['HM'])/2
    x, y, z0, z1 = src['AxisM']
    return dict(minM=[x-dx, y-dy, z0], maxM=[x+dx, y+dy, z1])


def endpoint_supports(src, elements):
    along, cross, start, end = beam_frame(src)
    line, top = src['AxisM'][cross], src['AxisM'][2]
    result = []
    for endpoint in (start, end):
        found = []
        for e in elements:
            if e['Kind'] != 'column':
                continue
            box = column_box(e); lo, hi = box['minM'], box['maxM']
            # Exige envolvimento vertical de toda a seção da viga, não mero toque.
            if (lo[along]-TOL <= endpoint <= hi[along]+TOL and
                    lo[cross]-TOL <= line <= hi[cross]+TOL and
                    lo[2] <= top-src['HM']+TOL and hi[2] >= top-TOL):
                found.append(dict(kind='column', nativeId=e['Id'], nativeMark=e['Mark'],
                                  alongIntervalM=[lo[along], hi[along]], box=box))
        if not found:
            # Apenas compatibilidade geométrica de viga secundária apoiada em transversal.
            for e in elements:
                if e['Kind'] != 'beam' or e['Id'] == src['Id']:
                    continue
                ea, ec, es, ee = beam_frame(e)
                axis = e['AxisM']
                if (ea == cross and es-TOL <= line <= ee+TOL and
                        abs(endpoint-axis[ec]) <= e['BM']/2+TOL and
                        axis[2] >= top-TOL and axis[2]-e['HM'] <= top-src['HM']+TOL):
                    found.append(dict(kind='beam', nativeId=e['Id'], nativeMark=e['Mark'],
                                      alongIntervalM=[axis[ec]-e['BM']/2, axis[ec]+e['BM']/2]))
        result.append(found)
    return result


def column_intervals(src, elements):
    """Projeções dos apoios intermediários e de extremidade na linha da viga."""
    along, cross, start, end = beam_frame(src)
    line, top = src['AxisM'][cross], src['AxisM'][2]
    found = []
    for e in elements:
        if e['Kind'] != 'column':
            continue
        box = column_box(e); lo, hi = box['minM'], box['maxM']
        if (lo[cross]-TOL <= line <= hi[cross]+TOL and
                lo[2] <= top-src['HM']+TOL and hi[2] >= top-TOL and
                min(hi[along], end)-max(lo[along], start) > TOL):
            found.append(dict(nativeId=e['Id'], nativeMark=e['Mark'],
                              alongIntervalM=[lo[along], hi[along]]))
    return found


def rectangular_mesh(obj, settings):
    """Exige oito cantos, faces nos planos da caixa e arestas fechadas orientadas."""
    shape = ifcopenshell.geom.create_shape(settings, obj)
    verts = [tuple(shape.geometry.verts[i:i+3]) for i in range(0, len(shape.geometry.verts), 3)]
    faces = [tuple(shape.geometry.faces[i:i+3]) for i in range(0, len(shape.geometry.faces), 3)]
    lo = [min(v[i] for v in verts) for i in range(3)]
    hi = [max(v[i] for v in verts) for i in range(3)]
    corners = {tuple(round(x, 8) for x in v) for v in product(*zip(lo, hi))}
    if len(verts) != 8 or len(faces) != 12 or {tuple(round(x, 8) for x in v) for v in verts} != corners:
        raise ValueError('Sólido não é caixa ortogonal: '+obj.GlobalId)
    directed = {}
    for face in faces:
        if not any(max(verts[v][i] for v in face)-min(verts[v][i] for v in face) < 1e-8 for i in range(3)):
            raise ValueError('Face não está no plano da caixa: '+obj.GlobalId)
        for a,b in zip(face, face[1:]+face[:1]):
            directed[a,b] = directed.get((a,b), 0)+1
    if any(count != 1 or directed.get((b,a)) != 1 for (a,b),count in directed.items()):
        raise ValueError('Malha não fechada/orientada: '+obj.GlobalId)
    return dict(minM=lo, maxM=hi, vertices=len(verts), triangles=len(faces), rectangularClosedMeshVerified=True)


def candidate(part, src, supports):
    along, cross, start, end = beam_frame(src)
    lo, hi = part['geometry']['minM'], part['geometry']['maxM']
    if (abs((lo[cross]+hi[cross])/2-src['AxisM'][cross]) > TOL or
            abs(hi[2]-src['AxisM'][2]) > TOL or
            abs(hi[2]-lo[2]-src['HM']) > TOL or
            abs(hi[cross]-lo[cross]-src['BM']) > TOL or
            min(hi[along], end)-max(lo[along], start) <= TOL):
        return None
    allowed_start = min([start]+[s['alongIntervalM'][0] for s in supports[0]])
    allowed_end = max([end]+[s['alongIntervalM'][1] for s in supports[1]])
    if lo[along] < allowed_start-TOL or hi[along] > allowed_end+TOL:
        return None
    return dict(nativeId=src['Id'], nativeMark=src['Mark'],
                receiverIntervalM=[lo[along], hi[along]], nativeAxisIntervalM=[start, end],
                extensionBeforeAxisM=max(0, start-lo[along]),
                extensionAfterAxisM=max(0, hi[along]-end),
                topDeltaM=hi[2]-src['AxisM'][2],
                widthDeltaM=hi[cross]-lo[cross]-src['BM'],
                heightDeltaM=hi[2]-lo[2]-src['HM'])


def main():
    started = time.perf_counter()
    previous = read(R162/'R162-recepcao-auditoria.json')
    paths = [Path(p) for p in previous['sourceHashes']]
    before = {str(p): sha(p) for p in paths}
    assert before == previous['sourceHashes'], 'Controle R162 mudou desde a auditoria'
    native = read(next(p for p in paths if 'releitura' in p.name))
    source = [e for e in native['Elements'] if e['Kind'] == 'beam']
    supports = {e['Id']: endpoint_supports(e, native['Elements']) for e in source}
    model = ifcopenshell.open(str(next(p for p in paths if p.name == 'Modelo 3D.IFC')))
    input_model = ifcopenshell.open(str(next(p for p in paths if 'DERIVADO' in p.name)))
    settings = ifcopenshell.geom.settings(); settings.set(settings.USE_WORLD_COORDS, True)
    parts = []
    for obj in model.by_type('IfcBeam'):
        box = rectangular_mesh(obj, settings)
        part = dict(receiverName=obj.Name, receiverGuid=obj.GlobalId, geometry=box)
        found = [r for e in source if (r := candidate(part, e, supports[e['Id']]))]
        part['candidates'] = found
        part['uniqueAssociation'] = found[0] if len(found) == 1 else None
        parts.append(part)
    rows = []
    for e in source:
        along, cross, start, end = beam_frame(e)
        ends = supports[e['Id']]
        intervals = [p['uniqueAssociation']['receiverIntervalM'] for p in parts
                     if p['uniqueAssociation'] and p['uniqueAssociation']['nativeId'] == e['Id']]
        # Face interna do volume de apoio identificado na autoria (não vão de cálculo).
        free_start = max([start]+[s['alongIntervalM'][1] for s in ends[0]])
        free_end = min([end]+[s['alongIntervalM'][0] for s in ends[1]])
        exclusions = column_intervals(e, native['Elements'])
        rows.append(dict(nativeId=e['Id'], nativeMark=e['Mark'], nativeAxisM=e['AxisM'],
                         widthM=e['BM'], heightM=e['HM'], endpointSupportCandidates=ends,
                         endpointSupportsAreGeometricOnly=True, partIntervalsM=intervals,
                         coverageBetweenAuthoringSupportFaces=coverage(intervals, free_start, free_end),
                         excludedAuthoringColumnFootprints=exclusions,
                         coverageOutsideAuthoringColumnFootprints=coverage(
                             intervals+[s['alongIntervalM'] for s in exclusions], free_start, free_end)))
    # Verifica a cobertura vertical das 22 colunas, permitindo segmentação nos níveis IFC.
    column_parts = [dict(receiverName=o.Name, receiverGuid=o.GlobalId, geometry=mesh(o, settings))
                    for o in model.by_type('IfcColumn')]
    column_rows = []
    input_columns = {o.Tag: o for o in input_model.by_type('IfcColumn')}
    for e in native['Elements']:
        if e['Kind'] != 'column':
            continue
        box = column_box(e)
        associated = [p for p in column_parts if all(
            abs(p['geometry'][side][i]-box[side][i]) <= TOL
            for side in ('minM', 'maxM') for i in (0, 1)) and
            min(p['geometry']['maxM'][2], box['maxM'][2])-
            max(p['geometry']['minM'][2], box['minM'][2]) > TOL]
        vertical = coverage([(p['geometry']['minM'][2], p['geometry']['maxM'][2]) for p in associated],
                            box['minM'][2], box['maxM'][2])
        input_box = mesh(input_columns[str(e['Id'])], settings)
        relative_to_input = coverage([(p['geometry']['minM'][2], p['geometry']['maxM'][2]) for p in associated],
                                     input_box['minM'][2], input_box['maxM'][2])
        column_rows.append(dict(nativeId=e['Id'], nativeMark=e['Mark'], nominalBox=box,
                                partGuids=[p['receiverGuid'] for p in associated], coverage=vertical,
                                inputIfcBox=input_box, coverageRelativeToInputIfcZExtent=relative_to_input,
                                inputIfcTopDeltaFromNominalM=input_box['maxM'][2]-box['maxM'][2]))
    assert before == {str(p): sha(p) for p in paths}, 'Arquivo de controle alterado durante leitura'
    missing = [p for p in parts if not p['uniqueAssociation']]
    result = dict(revision='H03/R163', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
                  inputRevision='H03/R162', inputWasExplicitDerivedIfc=True,
                  sourceHashes=before, sourceHashesUnchangedAfterRead=True,
                  geometricToleranceM=TOL, geometricToleranceIsNotNormative=True,
                  receiverBeamPartCount=len(parts), uniquelyAssociatedParts=len(parts)-len(missing),
                  beamOriginCount=len(source), beamOriginsWithObservedFreeSpanCoverage=sum(
                      r['coverageOutsideAuthoringColumnFootprints']['noGapAboveTolerance'] for r in rows),
                  columnOriginCount=len(column_rows), columnOriginsWithObservedVerticalCoverage=sum(
                      r['coverage']['noGapAboveTolerance'] for r in column_rows),
                  receiverColumnPartCount=len(column_parts),
                  columnOriginsWithInputIfcVerticalExtentCovered=sum(
                      r['coverageRelativeToInputIfcZExtent']['noGapAboveTolerance'] for r in column_rows),
                  columnOriginsWithInputTopBelowNominal=sum(
                      r['inputIfcTopDeltaFromNominalM'] < -TOL for r in column_rows),
                  partsWithAxisEndExtensions=sum(bool(p['uniqueAssociation'] and
                      max(p['uniqueAssociation']['extensionBeforeAxisM'],
                          p['uniqueAssociation']['extensionAfterAxisM']) > TOL) for p in parts),
                  unmatchedOrAmbiguousParts=missing,
                  ifcRelConnectsElementsCount=len(model.by_type('IfcRelConnectsElements')),
                  analyticalConnectivityVerified=False, columnAndBeamContactIsNotStructuralApproval=True,
                  nativeNodeTopologyNotRead=True, sourceSectionSizingNotApproved=True,
                  sourceOrReceiverModelChanged=False, loadsApplied=False,
                  structuralCalculationPerformed=False, pairedFlowComparisonFinished=False,
                  auditElapsedMs=(time.perf_counter()-started)*1000,
                  auditTimeIsNotOperatorOrFullFlowTime=True, beamParts=parts, beamOrigins=rows,
                  columnOrigins=column_rows, receiverColumnParts=column_parts)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'R163-cobertura-geometrica.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,(list,dict))}, ensure_ascii=False))


if __name__ == '__main__':
    main()

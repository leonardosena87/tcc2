"""Audita sólidos nativos H02, conciliando partes de viga e recortes em pilares."""
from pathlib import Path
import json,hashlib,math
root=Path(__file__).parent
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
proposal_path=root.parent/'Alternativa-H02-R12-NAO-EXECUTAR/H02-R12-proposta.json'
p=load(proposal_path);native=load(root/'R17-geometria-nativa.json')
TOL=1e-5
close=lambda a,b:abs(a-b)<=TOL
same=lambda a,b:len(a)==len(b) and all(close(x,y) for x,y in zip(a,b))
columns=[e for e in p['elements'] if e['kind']=='column']
beams=[e for e in p['elements'] if e['kind']=='beam']
def merge(intervals):
    out=[]
    for lo,hi in sorted(intervals):
        if hi-lo<=TOL:continue
        if out and lo<=out[-1][1]+TOL:out[-1][1]=max(out[-1][1],hi)
        else:out.append([lo,hi])
    return out
def expected_intervals(e):
    axis=0 if close(e['y'],e['y2']) else 1;cross=1-axis
    lo,hi=sorted((e['x'],e['x2']) if axis==0 else (e['y'],e['y2']))
    c=e['y'] if cross==1 else e['x'];cuts=[]
    for col in columns:
        if close(col['z1'],e['z']) and close(col['y'] if cross==1 else col['x'],c):
            center=col['x'] if axis==0 else col['y'];half=(col['b'] if axis==0 else col['h'])/2
            if center+half>lo+TOL and center-half<hi-TOL:cuts.append([max(lo,center-half),min(hi,center+half)])
    cursor=lo;intervals=[]
    for a,b in merge(cuts):
        if a>cursor+TOL:intervals.append([cursor,a])
        cursor=max(cursor,b)
    if cursor<hi-TOL:intervals.append([cursor,hi])
    return axis,cross,intervals,merge(cuts)
def audit(rows):
    colrows=[];unmatched=[];groups={e['id']:[] for e in beams}
    for r in rows:
        if r['class']=='IfcColumn':
            matches=[]
            for c in columns:
                lo=[c['x']-c['b']/2,c['y']-c['h']/2,c['z0']]
                hi=[c['x']+c['b']/2,c['y']+c['h']/2,c['z1']]
                if same(r['min'],lo) and same(r['max'],hi):matches.append(c['id'])
            colrows.append({'nativeGuid':r['guid'],'nativeName':r['name'],'matchedSourceIds':matches,'boundsMatchUnique':len(matches)==1})
        elif r['class']=='IfcBeam':
            matches=[]
            for e in beams:
                axis,cross,intervals,cuts=expected_intervals(e)
                s,t=sorted((e['x'],e['x2']) if axis==0 else (e['y'],e['y2']))
                center=e['y'] if cross==1 else e['x']
                if close((r['min'][cross]+r['max'][cross])/2,center) and close(r['max'][2],e['z']) and r['min'][axis]>=s-TOL and r['max'][axis]<=t+TOL and r['max'][axis]-r['min'][axis]>TOL:
                    matches.append(e['id'])
            if len(matches)==1:groups[matches[0]].append(r)
            else:unmatched.append({'nativeGuid':r['guid'],'nativeName':r['name'],'matches':matches,'bbox':{'min':r['min'],'max':r['max']}})
    beamrows=[]
    for e in beams:
        parts=groups[e['id']];axis,cross,wanted,cuts=expected_intervals(e)
        actual=merge([[r['min'][axis],r['max'][axis]] for r in parts])
        total=sum(r['max'][axis]-r['min'][axis] for r in parts)
        union=sum(b-a for a,b in actual)
        checks={'partsPresent':bool(parts),'width':bool(parts) and all(close(r['max'][cross]-r['min'][cross],e['b']) for r in parts),
        'height':bool(parts) and all(close(r['max'][2]-r['min'][2],e['h']) for r in parts),
        'topElevation':bool(parts) and all(close(r['max'][2],e['z']) for r in parts),
        'coverageOutsideColumnFaces':len(actual)==len(wanted) and all(same(a,b) for a,b in zip(actual,wanted)),
        'noDuplicatedAxialOverlap':close(total,union)}
        beamrows.append({'sourceId':e['id'],'nativeNames':sorted({r['name'] for r in parts}),'nativePartGuids':[r['guid'] for r in parts],
        'exportedParts':len(parts),'expectedSolidIntervalsM':wanted,'columnCutsM':cuts,'observedSolidIntervalsM':actual,'checks':checks})
    colIds=[r['matchedSourceIds'][0] for r in colrows if r['boundsMatchUnique']]
    return {'columnSegments':colrows,'columnSegmentsMatching':sum(r['boundsMatchUnique'] for r in colrows),
      'missingColumnIds':sorted({c['id'] for c in columns}-set(colIds)),
      'duplicateColumnIds':sorted({x for x in colIds if colIds.count(x)>1}),
      'beams':beamrows,'matchedLogicalBeams':sum(r['exportedParts']>0 for r in beamrows),
      'logicalBeamsPassing':sum(all(r['checks'].values()) for r in beamrows),'unmatchedBeamParts':unmatched,
      'geometryPass':len(colrows)==20 and len(set(colIds))==20 and all(r['boundsMatchUnique'] for r in colrows) and not unmatched and all(all(r['checks'].values()) for r in beamrows)}
result=audit(native['geometry'])
# Controles sintéticos em memória: não alteram resultados empíricos/arquivos IFC.
removed=next(r for r in native['geometry'] if r['class']=='IfcBeam')
missing=audit([r for r in native['geometry'] if r is not removed])
altered=json.loads(json.dumps(native['geometry']));b=next(r for r in altered if r['class']=='IfcBeam');b['min'][2]-=.01
changed=audit(altered)
duplicated=audit(native['geometry']+[removed])
assert not missing['geometryPass'] and not changed['geometryPass'] and not duplicated['geometryPass']
result.update({'sourceIfc':native['source'],'sourceSha256':native['sha256'],'proposalRunId':p['runId'],
 'proposalSha256':hashlib.sha256(proposal_path.read_bytes()).hexdigest(),'comparisonToleranceM':TOL,
 'exportedCounts':native['counts'],'slabsNativeMissing':10-native['counts']['IfcSlab'],
 'schemaValidationMessageCount':len(native['schemaValidationMessages']),
 'sensitivityControls':{'missingBeamPartDetected':True,'changedBeamHeightDetected':True,'duplicatedBeamPartDetected':True},
 'limits':['Equivalência nominal de caixas envolventes e cobertura axial dos sólidos de vigas, descontando faces de pilares da proposta. Não comprova eixo analítico, apoios ou estabilidade.',
 'Correspondência espacial, independente de numeração nativa; não preservação de IDs semânticos Revit no IFC do Eberick.',
 'Viga com pilar intermediário pode apresentar lacuna de sólido ocupada pelo pilar; isso não é perda do vão nem prova de conectividade analítica.',
 'Não comprova inexistência de alteração em outros parâmetros entre os arquivos binários históricos.',
 'Materiais, cargas, apoios, lajes, armaduras e cálculo estrutural ainda pendentes. Tolerância computacional, não normativa.'],
 'structuralCalculationPerformed':False})
(root/'R17-auditoria-geometria-H02.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('geometryPass','columnSegmentsMatching','missingColumnIds','duplicateColumnIds','matchedLogicalBeams','logicalBeamsPassing','unmatchedBeamParts','exportedCounts','schemaValidationMessageCount')},ensure_ascii=True,indent=2))
assert result['geometryPass'],'Investigar discrepâncias antes de aceitar geometria nominal.'

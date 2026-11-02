"""Compara geometrias corrigidas dos receptores, sem equiparar tempo/calculo."""
from collections import Counter
from datetime import datetime,timezone
import json
from pathlib import Path
from auditar_receptor import (read,sha,ifcopenshell,rectangular_mesh,mesh,beam_frame,
    endpoint_supports,column_intervals,column_box,coverage,NATIVE,OUT,ROOT,association,XY_TOL,Z_TOL)
from auditar_cobertura import subtract_intervals
import ifcopenshell.geom

CAD=Path('D:/TCC/outputs/Intercambio-H03-R165-CAD-GEOMETRIA-NAO-EXECUTAR/IFC-CAD-Eberick/Modelo 3D.IFC')


def main():
    paths=[CAD,ROOT/'Arquivos do projeto/Modelo 3D.IFC',NATIVE]
    hashes={str(p):sha(p) for p in paths};native=read(NATIVE);elements=native['Elements']
    sources=[e for e in elements if e['Kind']=='beam'];branches={}
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    for branch,path in zip(('CAD_R165','BIM_R166'),paths):
        model=ifcopenshell.open(str(path));parts=[]
        for obj in model.by_type('IfcBeam'):
            p=dict(name=obj.Name,guid=obj.GlobalId,geometry=rectangular_mesh(obj,settings))
            found=[r for e in sources if (r:=association(p,e,endpoint_supports(e,elements)))]
            if len(found)!=1:raise ValueError('Associação ausente/ambígua: '+branch+':'+obj.Name)
            p['origin']=found[0];parts.append(p)
        origins={}
        for e in sources:
            a,c,start,end=beam_frame(e);ends=endpoint_supports(e,elements)
            start=max([start]+[s['alongIntervalM'][1] for s in ends[0]])
            end=min([end]+[s['alongIntervalM'][0] for s in ends[1]])
            exclusion=[x['alongIntervalM'] for x in column_intervals(e,elements)]
            intervals=[p['origin']['receiverIntervalM'] for p in parts if p['origin']['nativeId']==e['Id']]
            clipped=[(max(a,start),min(b,end)) for a,b in intervals if min(b,end)>max(a,start)]
            origins[str(e['Id'])]=dict(nativeMark=e['Mark'],coverageOutsideColumns=coverage(intervals+exclusion,start,end),
                observedIntervalsOutsideColumnsM=subtract_intervals(clipped,exclusion))
        columns=[dict(name=o.Name,guid=o.GlobalId,geometry=mesh(o,settings)) for o in model.by_type('IfcColumn')]
        column_rows={}
        for e in elements:
            if e['Kind']!='column':continue
            box=column_box(e)
            found=[p for p in columns if all(abs(p['geometry'][s][i]-box[s][i])<XY_TOL for s in ('minM','maxM') for i in (0,1)) and min(p['geometry']['maxM'][2],box['maxM'][2])-max(p['geometry']['minM'][2],box['minM'][2])>XY_TOL]
            column_rows[str(e['Id'])]=dict(nativeMark=e['Mark'],coverage=coverage([(p['geometry']['minM'][2],p['geometry']['maxM'][2]) for p in found],box['minM'][2],box['maxM'][2]))
        branches[branch]=dict(productCounts={c:len(model.by_type(c)) for c in ('IfcBeam','IfcColumn','IfcSlab','IfcStair','IfcStairFlight')},
            matchedBeamParts=len(parts),matchedBeamOrigins=len({p['origin']['nativeId'] for p in parts}),
            beams=origins,columnOrigins=column_rows,beamParts=parts)
    comparison=[]
    for e in sources:
        cad=branches['CAD_R165']['beams'][str(e['Id'])];bim=branches['BIM_R166']['beams'][str(e['Id'])]
        a=cad['observedIntervalsOutsideColumnsM'];b=bim['observedIntervalsOutsideColumnsM']
        same=len(a)==len(b) and all(abs(x-y)<=XY_TOL for ra,rb in zip(a,b) for x,y in zip(ra,rb))
        comparison.append(dict(nativeId=e['Id'],nativeMark=e['Mark'],cadIntervalsM=a,bimIntervalsM=b,
            projectionOutsideColumnsEqualWithinTolerance=same,
            cadCovered=cad['coverageOutsideColumns']['noGapAboveTolerance'],bimCovered=bim['coverageOutsideColumns']['noGapAboveTolerance']))
    assert hashes=={str(p):sha(p) for p in paths}
    result=dict(revision='H03/R166',recordedAtUtc=datetime.now(timezone.utc).isoformat(),sourceHashes=hashes,
        sourcesUnchanged=True,scope='Geometrias corrigidas CAD R165 versus BIM derivado R166; nao intercambios brutos nem calculo final',
        xyAndSectionToleranceM=XY_TOL,topToleranceM=Z_TOL,commonBeamOrigins=30,
        beamOriginsWithEqualFreeSpanProjections=sum(r['projectionOutsideColumnsEqualWithinTolerance'] for r in comparison),
        allBeamOriginsCoveredInBoth=all(r['cadCovered'] and r['bimCovered'] for r in comparison),
        columnOriginsCoveredByBranch={k:sum(r['coverage']['noGapAboveTolerance'] for r in b['columnOrigins'].values()) for k,b in branches.items()},
        segmentationCountsAreNotPhysicalElementCounts=True,slabAndStairParityNotEstablished=True,
        analyticalConnectivityVerified=False,loadsAndConfigurationEqualityVerified=False,
        fullFlowTimesCompared=False,structuralCalculationCompared=False,structuralApproval=False,
        branches=branches,beamComparison=comparison)
    (OUT/'R166-comparacao-geometrica-CAD-BIM.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('branches','beamComparison')},ensure_ascii=False))


if __name__=='__main__':main()

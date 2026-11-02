"""Compara 11 lajes relançadas; não equipara cargas de vigas/vínculos/calculo."""
from collections import Counter
from datetime import datetime,timezone
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'h03-r166'))
from auditar_receptor import read,sha,ifcopenshell,rectangular_mesh,mesh
from preparar_niveis import cloud
from auditar_exportacao import get_psets
import ifcopenshell.geom
import numpy as np

OUT=Path('D:/TCC/outputs/Intercambio-H03-R167-LAJES-BIM-NAO-EXECUTAR')
ROOT=Path('D:/TCC/outputs/R167-BIM-LAJES-NAO-EXECUTAR')
IFC=ROOT/'Arquivos do projeto/Modelo 3D.IFC'
CAD=Path('D:/TCC/outputs/Intercambio-H03-R165-CAD-GEOMETRIA-NAO-EXECUTAR/IFC-CAD-Eberick/Modelo 3D.IFC')
PRIOR=Path('D:/TCC/outputs/R166-R160-3NIVEIS-CONFIG-CAD-NAO-EXECUTAR/Arquivos do projeto/Modelo 3D.IFC')
PRJ=ROOT/'Projeto Eberick/R166-R160-3NIVEIS-CONFIG-CAD-NAO-EXECUTAR.prj'
POINT_TOL=1e-4  # m; precisão computacional, não tolerância normativa


def properties(obj):
    return {k:{n:v for n,v in values.items() if n!='id'} for k,values in get_psets(obj).items()}


def points(obj,settings):
    shape=ifcopenshell.geom.create_shape(settings,obj)
    return np.unique(np.asarray(shape.geometry.verts).reshape(-1,3),axis=0)


def compare_points(a,b,tolerance=POINT_TOL):
    if len(a)!=len(b) or not len(a):return dict(matches=False,maxNearestDistanceM=None)
    d=np.linalg.norm(np.asarray(a)[:,None,:]-np.asarray(b)[None,:,:],axis=2)
    maximum=float(max(d.min(axis=0).max(),d.min(axis=1).max()))
    unique=len(set(d.argmin(axis=0)))==len(a) and len(set(d.argmin(axis=1)))==len(b)
    return dict(matches=maximum<=tolerance and unique,maxNearestDistanceM=maximum,uniqueNearestCorrespondence=unique)


def main():
    prep=read(OUT/'R167-preparacao-copia.json')
    preserved={e['relativePath']:sha(Path(prep['sourceRoot'])/e['relativePath'])==e['sha256'] for e in prep['sourceFiles']}
    assert all(preserved.values())
    paths=[IFC,CAD,PRIOR,PRJ];hashes={str(p):sha(p) for p in paths}
    assert hashes[str(PRJ)]=='936da7d187905771b918a906481f5d4149887928083a618fec6eb59dfc106e24'
    reopened=read(OUT/'R167-reabertura-observacao.json')
    assert reopened['closedAndReopened'] and reopened['firstSavedProjectSha256']==hashes[str(PRJ)]
    models=[ifcopenshell.open(str(p)) for p in paths[:3]];bim,cad,prior=models
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    cad_slabs=[dict(name=o.Name,guid=o.GlobalId,box=mesh(o,settings),cloud=cloud(o,settings),points=points(o,settings),properties=properties(o)) for o in cad.by_type('IfcSlab')]
    rows=[]
    for obj in bim.by_type('IfcSlab'):
        box=mesh(obj,settings);shape=cloud(obj,settings)
        candidates=[r for r in cad_slabs if all(abs(box[side][i]-r['box'][side][i])<1e-5 for side in ('minM','maxM') for i in range(3))]
        if len(candidates)!=1:raise ValueError('Laje sem correspondência espacial única: '+obj.Name)
        match=candidates[0];psets=properties(obj)
        rows.append(dict(bimName=obj.Name,bimGuid=obj.GlobalId,cadName=match['name'],cadGuid=match['guid'],
            geometry=box,pointCloudEqual=shape['pointsSha256']==match['cloud']['pointsSha256'],
            pointCloudComparison=compare_points(points(obj,settings),match['points']),
            exportedPropertySetsEqual=psets==match['properties'],exportedPropertySets=psets))
    assert len(rows)==11 and len({r['cadGuid'] for r in rows})==11
    assert all(r['pointCloudComparison']['matches'] and r['exportedPropertySetsEqual'] for r in rows)
    unchanged={}
    for cls in ('IfcBeam','IfcColumn'):
        def sig(model):
            return Counter((o.Name,cloud(o,settings)['pointsSha256']) for o in model.by_type(cls))
        unchanged[cls]=sig(bim)==sig(prior)
    assert all(unchanged.values())
    assert hashes=={str(p):sha(p) for p in paths}
    result=dict(revision='H03/R167',recordedAtUtc=datetime.now(timezone.utc).isoformat(),sourceHashes=hashes,
        readOnlyAuditSourcesPreserved=True,previousR166FilesPreserved=preserved,
        nativeProject=str(PRJ),nativeProjectClosedAndReopened=True,nativeSlabsPlaced=11,nativeSlabCountByFloor={'N1':6,'N2':5},
        receiverProductCounts={c:len(bim.by_type(c)) for c in ('IfcBeam','IfcColumn','IfcSlab','IfcStair','IfcStairFlight')},
        slabPairsUniquelyAssociatedByGeometry=len(rows),slabPointCloudsExactlyEqualToCad=sum(r['pointCloudEqual'] for r in rows),
        slabPointCloudsWithinToleranceToCad=sum(r['pointCloudComparison']['matches'] for r in rows),
        slabPointComparisonToleranceM=POINT_TOL,slabExportedPropertySetsEqualToCad=11,
        priorBeamAndColumnGeometriesUnchanged=unchanged,slabBoundingToleranceM=1e-5,
        propertyComparisonUsesRawIfcValuesWithoutUnitConversion=True,
        nativeInputValues=dict(N1Main=dict(accidentalKnM2=1.5,finishKnM2=1.25),
            N1StairArrivalAndBalcony=dict(accidentalKnM2=2.5,finishKnM2=1),N2=dict(accidentalKnM2=1,finishKnM2=.25),thicknessCm=14),
        nativeInputsWereMatchedToExistingCadReference=True,loadsNormativelyApprovedByThisAudit=False,
        balconyContourBarsAdded=3,balconyContourWidthCm=0,balconyOuterLimitsM=dict(x=10.725,yMin=3.8,yMax=7.1),
        newColumnsAdded=False,newPhysicalBeamsAdded=False,
        nativeStairStillMissing=True,beamLoadsAndBoundaryRestraintsEqualityNotVerified=True,
        gridAnglesNotComparedForAllSlabs=True,analyticalConnectivityVerified=False,
        newStructuralCalculationPerformed=False,structuralApproval=False,fullPairedComparisonFinished=False,
        partialSlabPlacementElapsedMs=read(OUT/'R167-lancamento-observacao.json')['elapsedMs'],
        subintervalsOverlapWholeInterval=True,fullBimFlowTime=False,slabPairs=rows)
    (OUT/'R167-lajes-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('sourceHashes','previousR166FilesPreserved','slabPairs')},ensure_ascii=False))


if __name__=='__main__':main()

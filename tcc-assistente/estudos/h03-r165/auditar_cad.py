"""Releitura somente leitura da revisão geométrica CAD R165.

Associação da laje por posição, cota e espessura, não pela coincidência do nome.
Caixas de faces livres do Eberick não são áreas nominais do perfil do Revit.
"""
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'h03-r161'))
from auditar_exportacao import read, sha, mesh, ifcopenshell, NATIVE, EXPECTED_NATIVE_SHA
from auditar_cad_eberick import check_landing_beam
from planejar_revisao_cad import unique_slab_candidate

OUT=Path('D:/TCC/outputs/Intercambio-H03-R165-CAD-GEOMETRIA-NAO-EXECUTAR')
PRIOR=Path('D:/TCC/outputs/Intercambio-H03-R161-R160-NAO-EXECUTAR/IFC-CAD-Eberick/Modelo 3D.IFC')
IFC=OUT/'IFC-CAD-Eberick/Modelo 3D.IFC'
TOL=1e-4  # m; apenas precisão computacional da comparação, não limite normativo


def rows(path):
    model=ifcopenshell.open(str(path))
    assert model.schema=='IFC4'
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    result=[]
    for cls in ('IfcBeam','IfcColumn','IfcSlab'):
        for obj in model.by_type(cls):
            result.append(dict(ifcClass=cls,name=obj.Name,guid=obj.GlobalId,geometry=mesh(obj,settings)))
    return model,result


def signature(row):
    box=row['geometry']
    return (row['ifcClass'],row['name'],*(round(v,5) for v in box['minM']+box['maxM']))


def main():
    t0=time.perf_counter();prep=read(OUT/'R165-preparacao-copia.json')
    prj=Path(prep['workingProject']);reopen=read(OUT/'R165-reabertura-observacao.json')
    files=[prj,IFC,PRIOR,NATIVE,OUT/'R165-L5-parametros.txt',OUT/'R165-L5-parametros-depois.txt',
           OUT/'R165-L5-grelha-antes.txt',OUT/'R165-L5-grelha-depois.txt',
           OUT/'R165-reabertura-V15.txt',OUT/'R165-reabertura-L5.txt']
    hashes={str(p):sha(p) for p in files}
    assert hashes[str(NATIVE)]==EXPECTED_NATIVE_SHA
    assert hashes[str(prj)]==reopen['projectSha256']
    preserved={e['relativePath']:sha(Path(prep['sourceRoot'])/e['relativePath'])==e['sha256'] for e in prep['sourceFiles']}
    assert all(preserved.values())
    native=read(NATIVE);model,current=rows(IFC);_,previous=rows(PRIOR)
    source=next(e for e in native['Elements'] if e['Mark']=='V15-N1')
    targets=[r for r in current if r['ifcClass']=='IfcBeam' and r['name']=='V15'];assert len(targets)==1
    beam=targets[0];lo,hi=beam['geometry']['minM'],beam['geometry']['maxM']
    delta=(lo[1]+hi[1])/2-source['AxisM'][1]
    assert abs(delta)<=TOL and abs(hi[2]-source['AxisM'][2])<=TOL
    assert abs(hi[2]-lo[2]-source['HM'])<=TOL and abs(hi[1]-lo[1]-source['BM'])<=TOL
    source_slab=next(e for e in native['Elements'] if e['Mark']=='L6-N1')
    slab=unique_slab_candidate([r for r in current if r['ifcClass']=='IfcSlab'],source_slab)
    old_slab=unique_slab_candidate([r for r in previous if r['ifcClass']=='IfcSlab'],source_slab)
    gap=slab['geometry']['minM'][1]-hi[1]
    assert abs(gap)<=TOL and slab['geometry']['minM'][1]>old_slab['geometry']['minM'][1]
    # Registra as diferenças de caixas; não equipara diferenças de segmentação a novos elementos.
    old_counter=Counter(signature(r) for r in previous);new_counter=Counter(signature(r) for r in current)
    removed=list((old_counter-new_counter).elements());added=list((new_counter-old_counter).elements())
    assert all(r[0]!='IfcColumn' for r in removed+added)
    assert all(r[0]!='IfcSlab' or r[1]=='L5' for r in removed+added)
    assert Counter(signature(r) for r in previous if r['ifcClass']=='IfcColumn')==Counter(signature(r) for r in current if r['ifcClass']=='IfcColumn')
    column_counts=Counter(r['name'] for r in current if r['ifcClass']=='IfcColumn')
    assert column_counts==Counter({'P'+str(i):2 for i in range(1,12)})
    landing_source=next(e for e in native['Elements'] if e['Mark']=='V16-ESC-PAT')
    supports={}
    for r in current:
        g=r['geometry']
        if r['ifcClass']=='IfcColumn' and g['minM'][2]<=landing_source['AxisM'][2]<=g['maxM'][2]:
            supports.setdefault(r['name'],[]).append(g)
    landing=next(r for r in current if r['ifcClass']=='IfcBeam' and r['name']=='V16')
    landing_check=check_landing_beam(landing['geometry'],supports,landing_source)
    assert landing_check['matchesWithinDeclaredTolerance']
    texts={p.name:p.read_text(encoding='utf-8-sig') for p in files if p.suffix=='.txt'}
    for name in ('R165-L5-parametros.txt','R165-L5-parametros-depois.txt','R165-reabertura-L5.txt'):
        assert all(s in texts[name] for s in ('Nome Value: L5','Acidental Value: 2.5','Revestimento Value: 1','Espessura Value: 14','Elevação Value: 0'))
    for name in ('R165-L5-grelha-antes.txt','R165-L5-grelha-depois.txt'):
        assert 'Ângulo Value: 90' in texts[name]
    assert all(s in texts['R165-reabertura-V15.txt'] for s in ('Nome Value: V15','bw Value: 20','h Value: 16'))
    assert hashes=={str(p):sha(p) for p in files}
    result=dict(revision='H03/R165',recordedAtUtc=datetime.now(timezone.utc).isoformat(),sourceHashes=hashes,
        originalR161CadFilesPreserved=preserved,readOnlyAuditSourcesPreserved=True,nativeClosedAndReopened=True,
        project=str(prj),productCounts={c:len(model.by_type(c)) for c in ('IfcBeam','IfcColumn','IfcSlab','IfcStair','IfcStairFlight')},
        distinctColumnPositions=11,columnParts=22,columnGeometricBoxesPreserved=True,
        beam=dict(revitId=source['Id'],revitMark=source['Mark'],nativeEberickName='V15',geometry=beam['geometry'],
            sourceAxisM=source['AxisM'],centerYDeltaM=delta,sectionCm=[20,16],sectionIsPreliminary=True),
        slab=dict(revitId=source_slab['Id'],revitMark=source_slab['Mark'],nativeEberickName=slab['name'],
            oldClearSolid=old_slab['geometry'],newClearSolid=slab['geometry'],nominalRevitProfileM=source_slab['ProfileM'],
            clearFaceToBeamFaceGapM=gap,independentIdentityProved=False,
            comparisonIsSpatialAndNotNominalAreaEquality=True,removedAndRelaunched=True,
            recordedLoadsMaintained=dict(accidentalKnM2=2.5,finishKnM2=1,extraKnM2=0),
            gridAngleDeg=90,gridAdoptsConfiguredSpacing=True,boundaryRestraintsNotCompletelyAudited=True),
        changedBoundingBoxSignatures=dict(beforeOnly=removed,afterOnly=added),
        landingBeam=landing_check,geometricToleranceM=TOL,
        correctionLog=['V15 altura 30 para 16 cm','Dois nos Y=285 para 303.5783333333 cm',
            'L5 removida e relancada no novo contorno, com parametros registrados reaplicados'],
        earlierTextOnlyMoveIncludedInObservedTime=True,tccVigasLayerHiddenInWorkingCopy=True,
        partialCorrectionElapsedMs=read(OUT/'R165-correcao-contorno-observacao.json')['elapsedMs'],
        partialTimeIncludesAttemptsResearchAndAudit=True,earlierOverlappingIntervalsNotAdditive=True,fullCadFlowTime=False,
        nativeStairPlacementInEberickPending=True,lowerStairSupportPending=True,windowJ4ConflictPending=True,
        newStructuralCalculationPerformed=False,inheritedCalculationResultsNotCurrent=True,
        fullPairedFlowComparisonFinished=False,structuralApproval=False,auditElapsedMs=(time.perf_counter()-t0)*1000)
    (OUT/'R165-CAD-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('productCounts','distinctColumnPositions','partialCorrectionElapsedMs','auditElapsedMs')}))
    print(json.dumps(result['changedBoundingBoxSignatures'],ensure_ascii=False))


if __name__=='__main__':main()

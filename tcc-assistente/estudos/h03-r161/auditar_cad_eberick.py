"""Leitura independente do IFC4 de controle da copia CAD R161.

Confere a V16 e a existencia geometrica dos pilares P1-P11. Nao confunde
solidos segmentados com novos pilares fisicos. Nao aprova ligacoes ou calculo.
"""
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import time

from auditar_exportacao import OUT, NATIVE, EXPECTED_NATIVE_SHA, read, sha, mesh, ifcopenshell, get_psets

PRJ = Path('D:/TCC/outputs/R161-CAD-REVISAO-R160-NAO-EXECUTAR/Projeto Eberick/H03_CAD_R49_LAJES_NAO_EXECUTAR.prj')
IFC = OUT/'IFC-CAD-Eberick/Modelo 3D.IFC'
AX = OUT/'R161-CAD-V16-releitura-AX.txt'
LEVEL_AX = OUT/'R161-CAD-nivel-releitura-AX.txt'
SNAPSHOT = OUT/'R161-copias-receptores-preparadas.json'
Z_TOLERANCE_M = 0.0002  # 0,2 mm: registra-se tambem a diferenca efetiva.
XY_TOLERANCE_M = 1e-6


def check_landing_beam(box, supports, native):
    lo, hi = box['minM'], box['maxM']
    axis = native['AxisM']
    if abs(axis[1]-axis[4]) > XY_TOLERANCE_M:
        raise ValueError('Auditoria delimitada a viga horizontal em X')
    if len(supports['P4']) != 1 or len(supports['P10']) != 1:
        raise ValueError('Apoios geometricos ambiguos na altura da viga')
    left, right = supports['P4'][0], supports['P10'][0]
    expected_lo = [left['maxM'][0], axis[1]-native['BM']/2, axis[2]-native['HM']]
    expected_hi = [right['minM'][0], axis[1]+native['BM']/2, axis[2]]
    deltas = [lo[i]-expected_lo[i] for i in range(3)]+[hi[i]-expected_hi[i] for i in range(3)]
    tolerances = [XY_TOLERANCE_M, XY_TOLERANCE_M, Z_TOLERANCE_M]*2
    return dict(expectedClearSolidMinM=expected_lo, expectedClearSolidMaxM=expected_hi,
                actualMinM=lo, actualMaxM=hi, signedDeltasM=deltas,
                matchesWithinDeclaredTolerance=all(abs(d)<=t for d,t in zip(deltas,tolerances)),
                topDeltaM=hi[2]-axis[2], widthM=hi[1]-lo[1], heightM=hi[2]-lo[2],
                clearLengthM=hi[0]-lo[0], nominalAxisLengthM=axis[3]-axis[0],
                xyToleranceM=XY_TOLERANCE_M,zToleranceM=Z_TOLERANCE_M,
                supportFaceAlignmentIsNotAnalyticalConnectivity=True)


def main():
    t0=time.perf_counter()
    files=[PRJ,IFC,NATIVE,AX,LEVEL_AX,SNAPSHOT]
    before={str(p):sha(p) for p in files}
    assert before[str(NATIVE)]==EXPECTED_NATIVE_SHA
    native=read(NATIVE)
    target=next(e for e in native['Elements'] if e['Mark']=='V16-ESC-PAT')
    model=ifcopenshell.open(str(IFC))
    assert model.schema=='IFC4'
    settings=ifcopenshell.geom.settings(); settings.set(settings.USE_WORLD_COORDS,True)
    beams=[o for o in model.by_type('IfcBeam') if o.Name=='V16']
    assert len(beams)==1
    columns=[dict(name=o.Name,guid=o.GlobalId,geometry=mesh(o,settings)) for o in model.by_type('IfcColumn')]
    counts=Counter(c['name'] for c in columns)
    assert set(counts)=={'P'+str(i) for i in range(1,12)} and all(n==2 for n in counts.values())
    by_name={}
    for col in columns:
        box=col['geometry']
        if box['minM'][2]<=target['AxisM'][2]<=box['maxM'][2]:
            by_name.setdefault(col['name'],[]).append(box)
    geometry=check_landing_beam(mesh(beams[0],settings),by_name,target)
    assert geometry['matchesWithinDeclaredTolerance']
    text=AX.read_text(encoding='utf-8-sig')
    assert all(s in text for s in ('Nome Value: V16','bw Value: 20','h Value: 30','/ Value: 0','Croqui (altura 157.4)'))
    level_text=LEVEL_AX.read_text(encoding='utf-8-sig')
    assert 'Altura Value: 157.4' in level_text and 'Nível Value: 177.4' in level_text
    copies=read(SNAPSHOT)
    original_checks={}
    for branch,entry in copies['branches'].items():
        original_checks[branch]=sha(entry['sourceProject'])==entry['sourceProjectSha256']
    assert all(original_checks.values())
    bim=copies['branches']['BIM']
    bim_unchanged=sha(bim['workingProject'])==bim['initialWorkingProjectSha256']
    assert bim_unchanged
    assert before=={str(p):sha(p) for p in files}
    result=dict(revision='H03/R161',commonAuthoringRevision='H03/R160',
        recordedAtUtc=datetime.now(timezone.utc).isoformat(),sources=before,
        sourceHashesUnchangedAfterRead=True,sourceR148ProjectsPreserved=original_checks,
        cadWorkingProject=str(PRJ),cadClosedAndReopened=True,nativeBeamReadbackConfirmed=True,
        nativeLevelReadbackConfirmed=True,intermediateHeightCm=157.4,intermediateAbsoluteLevelCm=177.4,
        requestedIntermediateHeightCm=157.4117647,
        ifcSchema=model.schema,ifcProfile='IFC4',propertySetsEnabled=True,completeBuildingSelected=True,
        productCounts={cls:len(model.by_type(cls)) for cls in ('IfcBeam','IfcColumn','IfcSlab','IfcStair','IfcStairFlight')},
        columnPartsByNativeName=dict(counts),distinctColumnNames=11,
        addedRejectedP12P13Present=False,columnCountIsSegmentCount=True,
        landingBeam=dict(nativeName='V16',sourceRevitId=target['Id'],guid=beams[0].GlobalId,
                         geometry=geometry,psets=get_psets(beams[0])),
        dwgR160ImportCompleted=False,
        dwgImportBlocker='Seletor em QiCadViewer.exe fora das superficies enumeradas; cancelado com Escape. V16 lancada pelos nos P4/P10 existentes.',
        commonRevisionFullyAppliedToCad=False,upperFloorV15L6RevisionApplied=False,
        stairNativeElementsLaunched=False,stairLoadsApplied=False,
        inheritedCalculationResultsInvalidated=True,newStructuralCalculationPerformed=False,
        bimWorkingCopyStillUnmodified=bim_unchanged,currentR160RevitIfcExportProduced=False,
        fullFlowComparisonCompleted=False,structuralApproval=False,
        windowJ4CompatibilityPending=True,auditScriptSeconds=time.perf_counter()-t0,columns=columns)
    (OUT/'R161-CAD-Eberick-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('productCounts','distinctColumnNames','cadClosedAndReopened','sourceR148ProjectsPreserved','auditScriptSeconds')}))


if __name__=='__main__':main()

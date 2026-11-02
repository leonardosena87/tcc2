"""Releitura R166; distingue normalização IFC, recepção e configuração CAD."""
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'h03-r163'))
from auditar_cobertura import (read,sha,ifcopenshell,rectangular_mesh,mesh,beam_frame,
    endpoint_supports,column_intervals,column_box,coverage)
from auditar_recepcao import parse_report
from auditar_exportacao import NATIVE,EXPECTED_NATIVE_SHA
from preparar_niveis import OUT,TARGET
import ifcopenshell.geom

ROOT=Path('D:/TCC/outputs/R166-R160-3NIVEIS-CONFIG-CAD-NAO-EXECUTAR')
PRJ=ROOT/'Projeto Eberick'/(ROOT.name+'.prj')
XY_TOL=1e-4
Z_TOL=2e-4  # 0,2 mm cobre arredondamento observado de -142,6 cm; não tolerância normativa


def association(part,source,supports):
    along,cross,start,end=beam_frame(source);lo,hi=part['geometry']['minM'],part['geometry']['maxM']
    if (abs((lo[cross]+hi[cross])/2-source['AxisM'][cross])>XY_TOL or
        abs(hi[2]-source['AxisM'][2])>Z_TOL or
        abs(hi[2]-lo[2]-source['HM'])>XY_TOL or
        abs(hi[cross]-lo[cross]-source['BM'])>XY_TOL or
        min(hi[along],end)-max(lo[along],start)<=XY_TOL):return None
    lower=min([start]+[s['alongIntervalM'][0] for s in supports[0]])
    upper=max([end]+[s['alongIntervalM'][1] for s in supports[1]])
    if lo[along]<lower-XY_TOL or hi[along]>upper+XY_TOL:return None
    return dict(nativeId=source['Id'],nativeMark=source['Mark'],receiverIntervalM=[lo[along],hi[along]],
        topDeltaM=hi[2]-source['AxisM'][2],heightDeltaM=hi[2]-lo[2]-source['HM'],widthDeltaM=hi[cross]-lo[cross]-source['BM'])


def main():
    t0=time.perf_counter();plan=read(OUT/'R166-derivado-conferencia.json')
    prior_path=Path('D:/TCC/outputs/Intercambio-H03-R164-CONTINUIDADE-PILARES-NAO-EXECUTAR/R164-recepcao-auditoria.json')
    prior=read(prior_path)
    assert all(sha(p)==h for p,h in prior['sourceHashes'].items())
    ifc=ROOT/'Arquivos do projeto/Modelo 3D.IFC'
    report=ROOT/'Arquivos do projeto/Documentos/Eberick/Relatorio_de_importacao_de_elementos_IFC.docx'
    files=[TARGET,PRJ,ifc,report,NATIVE,OUT/'R166-viga-patamar-nativa.txt',OUT/'R166-materiais-nativos.txt']
    hashes={str(p):sha(p) for p in files}
    assert hashes[str(NATIVE)]==EXPECTED_NATIVE_SHA and hashes[str(TARGET)]==plan['targetSha256']
    assert hashes[str(PRJ)]=='babfb4a5777e72f02957fc74d1123ec7776ceafd76b320c403daabd84712038f'
    reopen=read(OUT/'R166-reabertura-observacao.json')
    assert reopen['closedAndReopened'] and reopen['firstSavedProjectSha256']==hashes[str(PRJ)]
    native=read(NATIVE);elements=native['Elements'];beams=[e for e in elements if e['Kind']=='beam']
    rows=parse_report(report);ids=Counter(r['revId'] for r in rows)
    assert ids==Counter({str(e['Id']):1 for e in elements if e['Kind'] in ('column','beam')})
    model=ifcopenshell.open(str(ifc));assert model.schema=='IFC4'
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    parts=[]
    for obj in model.by_type('IfcBeam'):
        p=dict(receiverName=obj.Name,receiverGuid=obj.GlobalId,geometry=rectangular_mesh(obj,settings))
        candidates=[r for e in beams if (r:=association(p,e,endpoint_supports(e,elements)))]
        p['candidates']=candidates;p['uniqueAssociation']=candidates[0] if len(candidates)==1 else None;parts.append(p)
    origins=[]
    for e in beams:
        a,c,start,end=beam_frame(e);ends=endpoint_supports(e,elements)
        start=max([start]+[s['alongIntervalM'][1] for s in ends[0]])
        end=min([end]+[s['alongIntervalM'][0] for s in ends[1]])
        intervals=[p['uniqueAssociation']['receiverIntervalM'] for p in parts if p['uniqueAssociation'] and p['uniqueAssociation']['nativeId']==e['Id']]
        origins.append(dict(nativeId=e['Id'],nativeMark=e['Mark'],coverageOutsideColumns=coverage(intervals+[x['alongIntervalM'] for x in column_intervals(e,elements)],start,end)))
    columns=[dict(receiverName=o.Name,receiverGuid=o.GlobalId,geometry=mesh(o,settings)) for o in model.by_type('IfcColumn')]
    column_origins=[]
    for e in elements:
        if e['Kind']!='column':continue
        box=column_box(e)
        found=[p for p in columns if all(abs(p['geometry'][s][i]-box[s][i])<XY_TOL for s in ('minM','maxM') for i in (0,1)) and min(p['geometry']['maxM'][2],box['maxM'][2])-max(p['geometry']['minM'][2],box['minM'][2])>XY_TOL]
        column_origins.append(dict(nativeId=e['Id'],nativeMark=e['Mark'],verticalCoverage=coverage([(p['geometry']['minM'][2],p['geometry']['maxM'][2]) for p in found],box['minM'][2],box['maxM'][2])))
    landing=[p for p in parts if p['uniqueAssociation'] and p['uniqueAssociation']['nativeId']==473802];assert len(landing)==1
    ax=(OUT/'R166-viga-patamar-nativa.txt').read_text(encoding='utf-8-sig')
    assert all(x in ax for x in ('Nome Value: V6','bw Value: 20','h Value: 30','Value: -142.6'))
    mat=(OUT/'R166-materiais-nativos.txt').read_text(encoding='utf-8-sig')
    assert 'Classe de agressividade Value: II (moderada)' in mat and 'Dimensão do agregado Value: 25' in mat and mat.count('Value: C-25')>=3
    assert hashes=={str(p):sha(p) for p in files}
    assert all(p['uniqueAssociation'] for p in parts)
    assert all(r['coverageOutsideColumns']['noGapAboveTolerance'] for r in origins)
    assert all(r['verticalCoverage']['noGapAboveTolerance'] for r in column_origins)
    result=dict(revision='H03/R166',recordedAtUtc=datetime.now(timezone.utc).isoformat(),sourceHashes=hashes,
        readOnlyAuditSourcesPreserved=True,previousR164SourcesPreserved=True,firstSavedProjectSha256=hashes[str(PRJ)],
        nativeProjectClosedAndReopened=True,
        receiverRoot=str(ROOT),receiverProject=str(PRJ),inputIsExplicitDerivedIfc=True,
        importedOriginCount=len(rows),importedByClass=dict(Counter(r['group'] for r in rows)),
        receiverProductCounts={c:len(model.by_type(c)) for c in ('IfcBeam','IfcColumn','IfcSlab','IfcStair','IfcStairFlight')},
        nativeWizardStructuralStoreys=3,nativeWizardStructuralLevelsCm=[20,320,639],
        exportedIfcStoreyCount=len(model.by_type('IfcBuildingStorey')),
        exportedIfcStoreys=[dict(name=s.Name,elevationRaw=s.Elevation) for s in model.by_type('IfcBuildingStorey')],
        exportedIfcStoreyElevationUnit='centimeter',
        firstStoreyHasNoProductsInControlIfc=True,
        beamPartsAssociated=len(parts),beamOriginsWithFreeSpanCoverage=len(origins),columnOriginsWithNominalVerticalCoverage=len(column_origins),
        xyAndSectionToleranceM=XY_TOL,beamTopToleranceM=Z_TOL,tolerancesAreComputationalNotNormative=True,
        landingBeam=landing[0],landingNativeName='V6',landingNativeElevationCm=-142.6,
        materialConfigObserved=dict(concrete='C25',environmentClass='II',aggregateMm=25,source='Configuracao do ultimo projeto CAD R165; nao propriedades mecanicas transferidas pelo IFC'),
        sourceMaterialPsetsStillAbsent=True,allConfigurationsComparedFieldByField=False,
        experimentChangedBothLevelOrganisationAndConfigSource=True,isolatedCausalEffectOfLevelChangeClaimed=False,
        firstStoreyWizardHeightCm=100,firstStoreyWizardHeightIsNotFoundationDesign=True,
        partialReceptionElapsedMs=read(OUT/'R166-recepcao-observacao.json')['elapsedMs'],fullBimFlowTime=False,
        nativeSlabsAndStairPending=True,lowerStairSupportPending=True,windowJ4ConflictPending=True,
        analyticalConnectivityVerified=False,ifcRelConnectsElementsCount=len(model.by_type('IfcRelConnectsElements')),
        newStructuralCalculationPerformed=False,pairedComparisonFinished=False,structuralApproval=False,
        auditElapsedMs=(time.perf_counter()-t0)*1000,beamParts=parts,beamOrigins=origins,columnParts=columns,columnOrigins=column_origins)
    (OUT/'R166-recepcao-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,(dict,list))},ensure_ascii=False))


if __name__=='__main__':main()

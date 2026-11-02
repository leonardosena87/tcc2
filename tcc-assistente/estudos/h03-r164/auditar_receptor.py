"""Confere o ensaio R164 sem sobrescrever nem promover os controles anteriores."""
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'h03-r163'))
from auditar_cobertura import (read, sha, ifcopenshell, mesh, rectangular_mesh,
    candidate, endpoint_supports, beam_frame, column_intervals, column_box, coverage, subtract_intervals, TOL)
from auditar_recepcao import parse_report
from preparar_colunas import OUT, TARGET
import ifcopenshell.geom

ROOT = Path('D:/TCC/outputs/R164-R160-CONTINUIDADE-PILARES-NAO-EXECUTAR')


def main():
    t0=time.perf_counter()
    plan=read(OUT/'R164-derivado-conferencia.json');native_path=Path(plan['nativeReadbackPath'])
    assert sha(plan['priorAuditPath'])==plan['priorAuditSha256']
    prj=ROOT/'Projeto Eberick'/(ROOT.name+'.prj')
    receiver=ROOT/'Arquivos do projeto/Modelo 3D.IFC'
    report=ROOT/'Arquivos do projeto/Documentos/Eberick/Relatorio_de_importacao_de_elementos_IFC.docx'
    files=[TARGET,native_path,prj,receiver,report]
    before={str(p):sha(p) for p in files}
    assert before[str(TARGET)]==plan['targetSha256'] and before[str(native_path)]==plan['nativeReadbackSha256']
    frozen=read(OUT/'R164-receptor-congelamento.json')
    assert before[str(prj)]==next(e['sha256'] for e in frozen['entries'] if e['relativePath'].endswith('.prj'))
    native=read(native_path)
    source=[e for e in native['Elements'] if e['Kind']=='beam']
    rows=parse_report(report);counts=Counter(r['revId'] for r in rows)
    assert set(counts)=={str(e['Id']) for e in native['Elements'] if e['Kind'] in ('beam','column')}
    assert all(v==1 for v in counts.values())
    model=ifcopenshell.open(str(receiver));assert model.schema=='IFC4'
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    parts=[]
    for obj in model.by_type('IfcBeam'):
        part=dict(receiverName=obj.Name,receiverGuid=obj.GlobalId,geometry=rectangular_mesh(obj,settings))
        matches=[r for e in source if (r:=candidate(part,e,endpoint_supports(e,native['Elements'])))]
        part['candidates']=matches;part['uniqueAssociation']=matches[0] if len(matches)==1 else None
        parts.append(part)
    beam_rows=[]
    for e in source:
        along,cross,start,end=beam_frame(e)
        intervals=[p['uniqueAssociation']['receiverIntervalM'] for p in parts
                   if p['uniqueAssociation'] and p['uniqueAssociation']['nativeId']==e['Id']]
        exclusions=column_intervals(e,native['Elements'])
        endpoints=endpoint_supports(e,native['Elements'])
        start=max([start]+[s['alongIntervalM'][1] for s in endpoints[0]])
        end=min([end]+[s['alongIntervalM'][0] for s in endpoints[1]])
        beam_rows.append(dict(nativeId=e['Id'],nativeMark=e['Mark'],receiverIntervalsM=intervals,
            coverageOutsideAuthoringColumnFootprints=coverage(intervals+[r['alongIntervalM'] for r in exclusions],start,end)))
    columns=[dict(receiverName=o.Name,receiverGuid=o.GlobalId,geometry=mesh(o,settings)) for o in model.by_type('IfcColumn')]
    column_rows=[]
    for e in native['Elements']:
        if e['Kind']!='column':continue
        box=column_box(e)
        found=[p for p in columns if all(abs(p['geometry'][side][i]-box[side][i])<=TOL
            for side in ('minM','maxM') for i in (0,1)) and
            min(p['geometry']['maxM'][2],box['maxM'][2])-max(p['geometry']['minM'][2],box['minM'][2])>TOL]
        column_rows.append(dict(nativeId=e['Id'],nativeMark=e['Mark'],partGuids=[p['receiverGuid'] for p in found],
            nominalVerticalCoverage=coverage([(p['geometry']['minM'][2],p['geometry']['maxM'][2]) for p in found],box['minM'][2],box['maxM'][2])))
    previous=read(plan['priorAuditPath'])
    def signatures(parts):
        return Counter((p['uniqueAssociation']['nativeId'],*tuple(round(x,5) for x in p['geometry']['minM']+p['geometry']['maxM']))
                       for p in parts if p['uniqueAssociation'])
    beam_solid_signatures_equal=signatures(parts)==signatures(previous['beamParts'])
    changed_beam_extents=[]
    for e in source:
        old=[p['uniqueAssociation']['receiverIntervalM'] for p in previous['beamParts']
             if p['uniqueAssociation'] and p['uniqueAssociation']['nativeId']==e['Id']]
        new=[p['uniqueAssociation']['receiverIntervalM'] for p in parts
             if p['uniqueAssociation'] and p['uniqueAssociation']['nativeId']==e['Id']]
        rounded=lambda rows:sorted([[round(v,5) for v in r] for r in rows])
        if rounded(old)!=rounded(new):
            excluded=[r['alongIntervalM'] for r in column_intervals(e,native['Elements'])]
            old_outside=subtract_intervals(old,excluded);new_outside=subtract_intervals(new,excluded)
            changed_beam_extents.append(dict(nativeId=e['Id'],nativeMark=e['Mark'],beforeIntervalsM=old,
                afterIntervalsM=new,columnFootprintIntervalsM=excluded,
                beforeOutsideColumnsM=old_outside,afterOutsideColumnsM=new_outside,
                projectionsOutsideColumnFootprintsEqual=rounded(old_outside)==rounded(new_outside)))
    preserved_controls={p:sha(p)==h for p,h in previous['sourceHashes'].items()}
    assert all(preserved_controls.values())
    assert before=={str(p):sha(p) for p in files}
    reopened=read(OUT/'R164-reabertura-observacao.json')
    assert reopened['projectSha256']==before[str(prj)]
    assert sha(reopened['nativeN1CroquisAfterReopen'])==reopened['nativeN1CroquisSha256']
    result=dict(revision='H03/R164',recordedAtUtc=datetime.now(timezone.utc).isoformat(),sourceHashes=before,
        sourcesUnchangedAfterRead=True,firstSavedReceiverPrjPreserved=True,previousR162ControlsPreserved=preserved_controls,
        receiverRoot=str(ROOT),receiverProject=str(prj),inputIsExplicitDerivedIfc=True,
        importedOriginCount=len(rows),importedOriginsByNativeReport=dict(Counter(r['group'] for r in rows)),
        receiverProductCounts={c:len(model.by_type(c)) for c in ('IfcBeam','IfcColumn','IfcSlab','IfcStair','IfcStairFlight')},
        uniquelyAssociatedBeamParts=sum(p['uniqueAssociation'] is not None for p in parts),
        beamOriginsWithObservedFreeSpanCoverage=sum(r['coverageOutsideAuthoringColumnFootprints']['noGapAboveTolerance'] for r in beam_rows),
        columnOriginsWithNominalVerticalExtentCovered=sum(r['nominalVerticalCoverage']['noGapAboveTolerance'] for r in column_rows),
        previousColumnOriginsWithNominalVerticalExtentCovered=previous['columnOriginsWithObservedVerticalCoverage'],
        receiverBeamSolidAssociationsAndBoxesUnchangedFromR162=beam_solid_signatures_equal,
        beamOriginsWithChangedAxialIntervals=len(changed_beam_extents),
        changedAxialIntervalsLimitedToColumnFootprints=all(r['projectionsOutsideColumnFootprintsEqual'] for r in changed_beam_extents),
        changedAxialIntervals=changed_beam_extents,
        beamBoxComparisonRoundingDecimalsM=5,geometricToleranceM=TOL,
        nativeCroquisBirthIndicationsBefore=['P12(NASCE)','P13(NASCE)'],
        nativeCroquisSameLocationsAfter=['P5','P6'],nativeCroquisObservationIsNotFullNodeTopology=True,
        nativeP5SectionCm=[20,30],nativeP5ElevationCm=0,
        nativeReceiverClosedAndReopened=reopened['closedAndReopened'],
        nativePostReopenCroquisEvidence=reopened,
        ifcRelConnectsElementsCount=len(model.by_type('IfcRelConnectsElements')),
        analyticalConnectivityVerified=False,sourceRevitJoinCauseNotIsolated=True,
        mechanicalMaterialTransferStillNotProved=True,levelsStillRequireReview=True,
        nativeSlabsAndStairStillRequirePlacement=True,structuralCalculationPerformed=False,
        structuralApproval=False,pairedFlowComparisonFinished=False,
        partialReceptionElapsedMs=read(OUT/'R164-recepcao-observacao.json')['savedObservation']['elapsedMs'],
        fullFlowTime=False,auditElapsedMs=(time.perf_counter()-t0)*1000,
        reportRows=rows,beamParts=parts,beamOrigins=beam_rows,columnParts=columns,columnOrigins=column_rows)
    (OUT/'R164-recepcao-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,(dict,list))},ensure_ascii=False))


if __name__=='__main__':main()

"""Audita receptor da variante; mantem os resultados R161 sem sobrescrever."""
from collections import Counter
from datetime import datetime,timezone
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'h03-r161'))
from auditar_recepcao import parse_report,beam_candidates
from auditar_exportacao import mesh,get_psets
from preparar_derivado import OUT,TARGET,read,sha,ifcopenshell
import ifcopenshell.geom

ROOT=Path('D:/TCC/outputs/R162-R160-VIGAS-NOMINAIS-NAO-EXECUTAR')


def main():
    plan=read(OUT/'R162-derivado-conferencia.json');native_path=Path(plan['nativeReadbackPath']);native=read(native_path)
    prj=ROOT/'Projeto Eberick'/(ROOT.name+'.prj');receiver=ROOT/'Arquivos do projeto/Modelo 3D.IFC'
    report=ROOT/'Arquivos do projeto/Documentos/Eberick/Relatorio_de_importacao_de_elementos_IFC.docx'
    files=[TARGET,native_path,prj,receiver,report];before={str(p):sha(p) for p in files}
    assert before[str(TARGET)]==plan['targetSha256'] and before[str(native_path)]==plan['nativeReadbackSha256']
    frozen=read(OUT/'R162-receptor-congelamento.json')
    assert before[str(prj)]==next(e['sha256'] for e in frozen['entries'] if e['relativePath'].endswith('.prj'))
    rows=parse_report(report);expected={str(e['Id']) for e in native['Elements'] if e['Kind'] in ('beam','column')}
    counts=Counter(r['revId'] for r in rows)
    assert set(counts)==expected and all(v==1 for v in counts.values())
    model=ifcopenshell.open(str(receiver));assert model.schema=='IFC4'
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    beams=[]
    for o in model.by_type('IfcBeam'):
        box=mesh(o,settings);beams.append(dict(name=o.Name,guid=o.GlobalId,geometry=box,psets=get_psets(o),
            nominalBeamAssociation=beam_candidates(box,native['Elements'])))
    matched=[b['nominalBeamAssociation'] for b in beams if b['nominalBeamAssociation']]
    assert before=={str(p):sha(p) for p in files}
    original_checks={}
    copies=read(Path(__file__).resolve().parent.parent/'h03-r161/R161-copias-receptores-preparadas.json')
    for branch,e in copies['branches'].items():original_checks[branch]=sha(e['sourceProject'])==e['sourceProjectSha256']
    assert all(original_checks.values())
    raw=read(Path(__file__).resolve().parent.parent/'h03-r161/R161-Eberick-recepcao-auditoria.json')
    assert sha(raw['receiverProject'])==raw['sourceHashes'][raw['receiverProject']]
    result=dict(revision='H03/R162',recordedAtUtc=datetime.now(timezone.utc).isoformat(),sourceHashes=before,
        sourceHashesUnchangedAfterRead=True,receiverProject=str(prj),receiverRoot=str(ROOT),
        receiverInputWasExplicitlyDerived=True,replacedNativeRevitOrCadFiles=False,
        expectedOriginCount=len(expected),importedOriginCount=len(rows),importedOriginsByReport=dict(Counter(r['group'] for r in rows)),
        originalR148Preserved=original_checks,rawR161ReceiverPrjPreserved=True,
        receiverCounts={c:len(model.by_type(c)) for c in ('IfcBeam','IfcColumn','IfcSlab','IfcStair','IfcStairFlight')},
        beamPartCount=len(beams),spatiallyAssociatedParts=len(matched),distinctAssociatedBeamOrigins=len({r['nativeId'] for r in matched}),
        unmatchedBeamParts=[b for b in beams if b['nominalBeamAssociation'] is None],
        associatedPartsWithTopDifference=sum(abs(r['topDeltaM'])>1e-5 for r in matched),
        associatedPartsWithHeightDifference=sum(abs(r['heightDeltaM'])>1e-5 for r in matched),
        associatedPartsWithWidthDifference=sum(abs(r['receiverWidthM']-r['nativeWidthM'])>1e-5 for r in matched),
        beforeRawReceiver=dict(distinctAssociatedBeamOrigins=raw['distinctBeamOriginsSpatiallyAssociated'],
            associatedPartsWithTopDifference=raw['beamPartsWithDifferentTop'],associatedPartsWithHeightDifference=raw['beamPartsWithDifferentHeight']),
        valuesAreObservedGeometryNotApproval=True,beamAxialCoverageAndConnectionsNotVerified=True,
        mechanicalMaterialPropertiesNotRepaired=True,stairAndSlabNativeConversionNotResolved=True,
        levelsNotSimplified=True,loadsNotApplied=True,newStructuralCalculationPerformed=False,
        nativeProjectClosedReopened=False,completeCadBimComparisonFinished=False,structuralApproval=False,reportRows=rows,beams=beams)
    (OUT/'R162-recepcao-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('importedOriginCount','receiverCounts','distinctAssociatedBeamOrigins','associatedPartsWithTopDifference','associatedPartsWithHeightDifference','associatedPartsWithWidthDifference')}))


if __name__=='__main__':main()

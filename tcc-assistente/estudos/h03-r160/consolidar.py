"""Consolida provas nativas R160; não promove aprovação de arquitetura/cálculo."""
from collections import Counter
from datetime import datetime,timezone
import hashlib
import json
import math
from pathlib import Path
import shutil

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R160-SOMENTE-VIGA-NAO-EXECUTAR')


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))


def main():
    prep=read(OUT/'R160-preparacao.json');created=read(OUT/'R160-criacao-nativa.json')
    path=sorted(OUT.glob('R160-releitura-nativa-*.json'))[-1];reread=read(path)
    assert reread==created['Readback']
    old=read(Path(prep['sourcePath']).parent/'R159-releitura-nativa-20261102-134930.json')
    before={r['Mark']:r for r in old['Elements']};after={r['Mark']:r for r in reread['Elements']}
    assert set(before)-set(after)=={'P12-ESC-N1','P13-ESC-N1'} and not set(after)-set(before)
    assert sorted(created['DeletedIds'])==[473797,473798]
    assert old['Stair']==reread['Stair']
    for key,row in after.items():
        if key!='V16-ESC-PAT':assert row==before[key],key
    beam=after['V16-ESC-PAT'];previous=before['V16-ESC-PAT']
    for key in beam:
        if key!='AxisM':assert beam[key]==previous[key],key
    assert all(math.isclose(a,b,abs_tol=1e-8,rel_tol=0) for a,b in zip(beam['AxisM'],[4.4,0.0,previous['AxisM'][2],6.55,0.0,previous['AxisM'][5]]))
    assert abs(beam['AxisM'][2]-(.22+9*3.03/17-.05))<1e-8
    assert Counter(e['Kind'] for e in reread['Elements'])==dict(column=22,beam=30,slab=11)
    assert all(e['MaterialFckMPa']==25 for e in reread['Elements'])
    assert sha(prep['sourcePath'])==prep['sourceSha256']
    closed=read(OUT/'R160-fechado-apos-criacao.json');assert sha(prep['copyPath'])==closed['copySha256']
    cad=read(OUT/'R160-CAD-formas-conferidas.json');assert cad['uniqueBuildingElementCount']==63 and cad['allThreeSavedClosedReopened']
    for f in cad['files']:assert sha(f['dwgPath'])==f['dwgSha256']
    result=dict(revision='H03/R160',recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        nativeRevitPath=prep['copyPath'],nativeRevitSha256=sha(prep['copyPath']),sourceR159Preserved=True,
        nativeCreatedSavedClosedReopenedExactReadbackMatch=True,readbackPath=str(path),readbackSha256=sha(path),
        removedColumnMarks=['P12-ESC-N1','P13-ESC-N1'],removedIds=created['DeletedIds'],
        unchangedBuildingElementsComparedToR159=62,stairReadbackExactlyPreserved=True,
        countsByKind=dict(column=22,beam=30,slab=11),oneAddedBeamRelativeTo62ElementBase=True,
        beamMark='V16-ESC-PAT',beamIdPreserved=True,beamAxisM=beam['AxisM'],beamWidthM=beam['BM'],beamHeightM=beam['HM'],
        nativeCommandMs=created['CommandMs'],commandTimeIsNotFlowTime=True,
        nativeStairVisibilityEnabledManuallyInNewView=True,warnings=created['Warnings'],
        cadFormsVerified=True,cadFiles=cad['files'],cadTiming=read(OUT/'R160-CAD-formas-fim.json'),
        revitApplicationObservation=read(OUT/'R160-Revit-aplicacao-observacao.json'),
        windowJ4ConflictUnderRecordedArchitectureInterpretation=True,architectureWindowChanged=False,
        allStructuralSupportsOrConnectionsVerified=False,structuralDimensioningOrApproval=False,
        ifcR160Exported=False,eberickR160Applied=False,pairedFlowRankingCompleted=False)
    target=OUT/'R160-resultado.json';target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    pointer=Path('D:/TCC/dados-pesquisa/escada-h03-atual.json');current=read(pointer)
    previous_pointer=OUT/'R160-apontador-antes.json'
    if not previous_pointer.exists():shutil.copyfile(pointer,previous_pointer)
    current.update(nativeRevitRevision='H03/R160',nativeRevitCopyPath=prep['copyPath'],nativeRevitReadbackEvidence=str(target),nativeRevitReadbackEvidenceSha256=sha(target),
        nativeRevitCreatedSavedReopened=True,landingBeamCandidatePath=str(OUT/'R160-candidato-comum.json'),
        latestCandidateImplementationEvidencePath=str(target),latestCandidateImplementationEvidenceSha256=sha(target),
        latestVisualEvidencePath=str(target),latestVisualEvidenceSha256=sha(target),
        latestCandidateCadForms=[f['dwgPath'] for f in cad['files']],
        landingBeamRevitR160PlacementConfirmed=True,extraLandingColumnsRemoved=True,
        currentBeamUsesExistingP4P10=True,currentBeamWindowJ4ConflictPending=True,
        latestNativeIfcRevision='H03/R159',currentNativeRevisionHasExportedIFC=False,
        landingBeamEberickPlacementConfirmed=False,stairIntegratedInCalculationModel=False,fullCompatibilityReviewCompleted=False,finalApproval=False)
    pointer.write_text(json.dumps(current,ensure_ascii=False,indent=2),encoding='utf-8');shutil.copyfile(pointer,OUT/'R160-apontador-apos.json')
    for name in ('LEIA-ME-R160.md','CONTINUAR-AQUI-H03-R160.md'):
        if (HERE/name).exists():shutil.copyfile(HERE/name,OUT/name)
    for p in OUT.iterdir():
        if p.is_file() and p.suffix.lower() in ('.json','.dxf','.scr','.png','.addin') and 'manifesto' not in p.name:shutil.copyfile(p,HERE/p.name)
    manifest=[dict(path=p.name,sha256=sha(p)) for p in sorted(HERE.iterdir()) if p.is_file() and 'manifesto' not in p.name]
    for folder in (OUT,HERE):(folder/'R160-manifesto.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(dict(reopenedMatch=True,removed=2,retained=62,buildingElements=63,stairPreserved=True,sourceR159Preserved=True,nativeCommandMs=created['CommandMs'])))


if __name__=='__main__':main()

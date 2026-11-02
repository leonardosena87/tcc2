"""Preserva evidências desta etapa sem promover candidato a projeto aprovado."""
import hashlib
import json
import shutil
from datetime import datetime,timezone
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R159-IMPLANTACAO-NAO-EXECUTAR')
CAD=Path('D:/TCC/outputs/Escada-H03-R158-CANDIDATO-COMUM-NAO-EXECUTAR')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))

def main():
    if (OUT/'R159-criacao-nativa.json').exists():raise RuntimeError('Há criação Revit: consolidar com releitura, não como pendência.')
    prep=read(OUT/'R159-preparacao.json');copy=Path(prep['copyPath']);source=Path(prep['sourcePath'])
    assert sha(copy)==sha(source)==prep['sourceSha256']==prep['copySha256Before']
    assert sha(Path(prep['candidatePath']))==prep['candidateSha256']
    forms=read(OUT/'R159-CAD-formas-conferidas.json');partial=read(OUT/'R159-CAD-conferencia.json')
    assert forms['allThreeSavedClosedReopened'] and forms['uniqueBuildingElementCount']==65
    for f in forms['files']:assert sha(Path(f['dwgPath']))==f['dwgSha256'] and sha(Path(f['returnPath']))==f['returnSha256']
    assert sha(Path(partial['dwgPath']))==partial['dwgSha256']
    failures=[read(p) for p in sorted(OUT.glob('R159-falha-*.json'))]
    assert failures and all(f['Saved'] is False for f in failures)
    result=dict(revision='H03/R159',recordedAtUtc=datetime.now(timezone.utc).isoformat(),sourceR157PreservedByteIdentical=True,r159CopyStillBaselineByteIdentical=True,
        revitCandidateApplied=False,firstRevitFailureBeforeTransactions=True,revitFirstCommandFailureMs=failures[0]['CommandMs'],revitHashReadCorrected=True,
        revitFailedAttemptCount=len(failures),revitFailedAttempts=[dict(error=f['Error'],commandMs=f['CommandMs'],saved=f['Saved'],warnings=f['Warnings']) for f in failures],
        revitSketchProfileLookupCorrected=True,geometryUnchangedAfterRollback=True,softwareFailuresAreNotGeometryOrIfcImportDefects=True,
        revitRestartWaitingForVisibleTrustDialog=True,securityPolicyChanged=False,revitCorrectedDllPath=prep['dllPath'],revitCorrectedDllSha256=sha(Path(prep['dllPath'])),
        originalBuildDllSha256=prep['dllSha256'],candidateSha256=prep['candidateSha256'],candidateElementCount=65,
        cadPartialSavedClosedReopened=True,cadFormsSavedClosedReopened=True,cadFormsUniqueBuildingElementCount=65,
        cadPartialEvidencePath=str(OUT/'R159-CAD-conferencia.json'),cadFormsEvidencePath=str(OUT/'R159-CAD-formas-conferidas.json'),
        materialAnalyticalDataTransferredToEberick=False,stairResistantVolumeCalculated=False,completeCompatibilityReview=False,
        pairedFlowComparisonCompleted=False,structuralApproval=False,activeStairGeometryPromoted=False,
        preservedSession=read(OUT/'R159-preservacao-R157.json'))
    target=OUT/'R159-resultado-parcial.json';target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    current=Path('D:/TCC/dados-pesquisa/escada-h03-atual.json');j=read(current)
    assert j['activeRevision']=='H03/R153' and j['nativeRevitRevision']=='H03/R157'
    backup=OUT/'R159-apontador-anterior.json'
    if not backup.exists():shutil.copyfile(current,backup)
    j.update(latestCandidateImplementationEvidencePath=str(target),latestCandidateImplementationEvidenceSha256=sha(target),
        latestCandidateCadForms=[f['dwgPath'] for f in forms['files']],landingBeamRevitR159PlacementConfirmed=False,landingBeamEberickPlacementConfirmed=False)
    current.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding='utf-8');shutil.copyfile(current,OUT/'R159-apontador-atual.json')
    shutil.copyfile(HERE/'LEIA-ME-R159.md',OUT/'LEIA-ME-R159.md')
    allowed={'.json','.png','.dxf','.scr','.addin'}
    for p in OUT.iterdir():
        if p.is_file() and p.suffix.lower() in allowed and 'manifesto' not in p.name:shutil.copyfile(p,HERE/p.name)
    for name in ('R158-CAD-salvo.png','R158-CAD-reaberto.png','CAD-retomada-inicio.json','CAD-retomada-fim.json'):
        shutil.copyfile(CAD/name,HERE/name)
    entries=[dict(path=p.name,sha256=sha(p)) for p in sorted(HERE.iterdir()) if p.is_file() and 'manifesto' not in p.name]
    for folder in (OUT,HERE):(folder/'R159-manifesto.json').write_text(json.dumps(entries,indent=2),encoding='utf-8')
    print(json.dumps(dict(revitApplied=False,cadFormsVerified=3,uniqueElements=65,sourcePreserved=True,archivedFiles=len(entries))))

if __name__=='__main__':main()

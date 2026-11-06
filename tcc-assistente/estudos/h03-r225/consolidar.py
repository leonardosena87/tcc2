"""Consolida autoria salva e auditorias IFC antes/depois dos cobrimentos."""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime,timezone


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main(root):
    first=root/'Antes-correcao-cobrimentos'
    before=read(first/'R225-primeiro-IFC-auditoria.json');after=read(root/'R225-IFC-auditoria.json')
    original=read(first/'R225-primeira-exportacao-ifc.json');exported=read(root/'R225-exportacao-ifc.json')
    native=read(root/'R225-aplicacao-nativa.json');cad=read(root/'R225-CAD-conferencia.json')
    cfg=read(root/'R225-config.json')
    if sha(Path(cfg['SourcePath']))!=cfg['SourceSha256']:raise ValueError('R195 original alterada')
    if exported['Readback']!=original['Readback']:raise ValueError('Cadastro geometrico ou escada mudou')
    a={r['nativeId']:r for r in before['elements']};b={r['nativeId']:r for r in after['elements']}
    if a.keys()!=b.keys():raise ValueError('Identidades alteradas')
    boxes=0;ids=0;delta=0.
    for key in a:
        maximum=max(abs(x-y) for side in ('min','max') for x,y in zip(a[key]['bodyBoundsM'][side],b[key]['bodyBoundsM'][side],strict=True))
        if maximum<=1e-8:boxes+=1
        delta=max(delta,maximum);ids+=a[key]['globalId']==b[key]['globalId']
    if after['summary']['coverThreeFieldsMatchCount']!=66:raise ValueError('Cobrimentos ainda divergentes')
    rvt=root/'H03-R225-REVIT-COORDENACAO-NAO-EXECUTAR.rvt'
    result=dict(revision='R225',recordedUtc=datetime.now(timezone.utc).isoformat(),
        nativeRevitAppliedSavedClosedReopened=True,geometries=66,stair17Preserved=True,
        coverCorrectionReportedByUser=True,coverCorrectionVerifiedInIFC=True,
        coverFieldsCorrected=198,coverElementsCorrected=66,
        correctionOrigin='Cadastro padrao de autoria; nao demonstrado como perda do exportador',
        manualEditingOperationCount=None,exclusiveHumanEditingSeconds=None,
        nativeGeometryAndStairReadbackUnchangedDuringCoverCorrection=True,
        ifcGlobalIdsPreserved=ids,ifcBodyBoundingBoxesPreserved=boxes,maxBoundingBoxDeltaM=delta,
        boundingBoxMatchIsNotCompleteSolidGeometryVerification=True,
        revitPath=str(rvt),revitSha256=sha(rvt),originalR195Preserved=True,
        ifcPath=exported['File'],ifcSha256=sha(Path(exported['File'])),ifcAudit=after['summary'],
        cadUniqueElements=cad['uniqueElements'],cadSavedClosedReopened=True,
        timings=dict(revitCorrectionCommandMs=native['CommandMs'],
            firstIfcExportCommandMs=original['CommandMs'],finalIfcExportCommandMs=exported['CommandMs'],
            cadEightProcessesSeconds=read(root/'R225-CAD-nativo.json')['sequentialProcessWallSeconds'],
            totalWorkflowSeconds=None,paidApiTokens=None,exclusiveAiInferenceSeconds=None,pairedRankingComplete=False),
        eberickReceptionOfUpdatedSourcesTested=False,
        fullStructuralVerificationComplete=False,structuralApproval=False)
    (root/'R225-resultado-autoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('coverCorrectionVerifiedInIFC','ifcGlobalIdsPreserved','ifcBodyBoundingBoxesPreserved','maxBoundingBoxDeltaM','revitSha256')}))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);a=ap.parse_args();main(a.root)

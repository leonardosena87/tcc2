"""Prepara cópia isolada R160; a alteração nativa só ocorre pelo comando Revit."""
import copy
from collections import Counter
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
from xml.etree import ElementTree as ET

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R160-SOMENTE-VIGA-NAO-EXECUTAR')
SOURCE=Path('D:/TCC/outputs/Escada-H03-R159-IMPLANTACAO-NAO-EXECUTAR/H03-R159-Revit-VIGA-PATAMAR-NAO-EXECUTAR.rvt')
PREVIOUS=Path('D:/TCC/outputs/Escada-H03-R158-CANDIDATO-COMUM-NAO-EXECUTAR/R158-candidato-comum.json')
PIN='165d3b0cd163ffcc79b2f1df5344c17201ab7023d728a7d2f388450280a24d85'
DLL=Path('D:/TCC/ferramentas/RevitStairSupport-R160/TccAssistente.RevitStairSupportR160.dll')
IMAGE=Path('C:/Users/leona/AppData/Local/Temp/codex-clipboard-ba11c4b2-123e-407e-a0e9-fbddc1cc5c4e.png')


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def revise(previous):
    p=copy.deepcopy(previous)
    beam=next(e for e in p['addedElements'] if e['kind']=='beam')
    beam.update(y=0,y2=0,role='viga-frontal-patamar-marcacao-usuario')
    p.update(revision='H03/R160',addedElements=[beam],proposedElementCount=63,
        countsByKind=dict(column=22,beam=30,slab=11),
        removedR159ColumnMarks=['P12-ESC-N1','P13-ESC-N1'],existingBeamMovedFromR159=True,
        userRequest='Retirar os dois pilares adicionais e manter somente uma viga no local vermelho da imagem, entre os pilares existentes P4/P10.',
        noNewColumns=True,originalStairGeometryPreserved=True,
        facadeBeamCrossesWindow=True,windowJ4Changed=False,
        windowJ4InterferenceRequiresArchitectureReview=True,
        nativeStairAlreadyExistsInSource=True,nativeAuthoringApplied=False,
        modelIntegratedInEberick=False,structuralCapacityVerified=False,supportAndAnchorageVerified=False,
        supportSchemeCandidate='V16-ESC-PAT entre P4/P10, eixo Y=0; sem P12/P13. Seção 20x30cm herdada como hipótese, sem cálculo.',
        createdAtUtc=datetime.now(timezone.utc).isoformat())
    for k in ('rejectedFacadeBeam','nominalHorizontalSurfaceOverlaps','zeroNominalSurfaceOverlapsIsNotSolidClashClearance'):
        p.pop(k,None)
    p['solidClashReviewAfterPlacementPending']=True
    p['limitations']=['Seção e ligações da viga ainda não dimensionadas.','Conflito com faixa da janela J4 sob interpretação arquitetônica registrada; janela não foi alterada.','Apoio inferior, continuidade, cargas e ELU/ELS pendentes.']
    rows=sum((p[k] for k in ('retainedExistingElements','changedExistingElements','addedElements')),[])
    assert len(rows)==63 and len({e['id'] for e in rows})==63
    assert Counter(e['kind'] for e in rows)==p['countsByKind']
    assert not any(e['id'] in p['removedR159ColumnMarks'] for e in rows)
    assert beam['x']==4.4 and beam['x2']==6.55 and beam['z']==p['concreteLandingM']
    return p


def main():
    if OUT.exists():raise FileExistsError(OUT)
    assert sha(SOURCE)==PIN and DLL.is_file()
    assert sha(PREVIOUS)=='a0dec2b713ea8ea945207c366b0c31ad2c7a0bd1be41dd6a7f196adc752764eb'
    manifest=Path(os.environ['APPDATA'])/'Autodesk/Revit/Addins/2027/TccAssistente.StairSupportR160.addin'
    if manifest.exists():raise FileExistsError(manifest)
    OUT.mkdir();p=revise(json.loads(PREVIOUS.read_text(encoding='utf-8')))
    candidate=OUT/'R160-candidato-comum.json';candidate.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
    target=OUT/'H03-R160-Revit-SOMENTE-VIGA-PATAMAR-NAO-EXECUTAR.rvt';shutil.copyfile(SOURCE,target)
    assert sha(target)==PIN
    shutil.copyfile(IMAGE,OUT/'R160-marcacao-usuario.png')
    config=dict(CandidateSha256=sha(candidate),CopySha256Before=PIN)
    (OUT/'R160-config.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
    root=ET.Element('RevitAddIns')
    for label,guid,cls in [('TCC - somente viga patamar R160','9cbda03e-2f63-49c7-baf7-789780e31a3e','ApplyRevision'),('TCC - conferir somente viga R160','601264f0-0a6a-4080-b9ec-f7b90199ef9e','AuditRevision')]:
        a=ET.SubElement(root,'AddIn',Type='Command')
        for key,value in dict(Name=label,Text=label,Assembly=str(DLL),AddInId=guid,FullClassName='TccAssistente.RevitStairSupportR160.'+cls,VendorId='TCC2',VendorDescription='Copia R160: retirar P12/P13 e mover V16 conforme marcacao do usuario. Nao dimensiona.').items():ET.SubElement(a,key).text=value
    raw=ET.tostring(root,encoding='utf-8',xml_declaration=True);manifest.write_bytes(raw);(OUT/manifest.name).write_bytes(raw)
    result=dict(preparedAtUtc=datetime.now(timezone.utc).isoformat(),sourcePath=str(SOURCE),sourceSha256=PIN,copyPath=str(target),copySha256Before=sha(target),candidatePath=str(candidate),candidateSha256=sha(candidate),userImageSha256=sha(IMAGE),dllPath=str(DLL),dllSha256=sha(DLL),dependencyR159Sha256=sha(DLL.parent/'TccAssistente.RevitStairSupport.dll'),manifestPath=str(manifest),nativeApplied=False,structuralApproval=False)
    (OUT/'R160-preparacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(prepared=True,copy=str(target),expectedStructuralCount=63,nativeApplied=False)))


if __name__=='__main__':main()

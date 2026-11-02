"""Prepara cópia e manifesto; não executa o Revit nem modifica os projetos-fonte."""
import hashlib
import json
import os
import shutil
from datetime import datetime,timezone
from pathlib import Path
from xml.etree import ElementTree as ET

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R159-IMPLANTACAO-NAO-EXECUTAR')
SOURCE=Path('D:/TCC/outputs/Escada-H03-R157-VISUAL-NAO-EXECUTAR/H03-R157-Revit-ESCADA17-VISUAL-NAO-EXECUTAR.rvt')
CANDIDATE=Path('D:/TCC/outputs/Escada-H03-R158-CANDIDATO-COMUM-NAO-EXECUTAR/R158-candidato-comum.json')
REQUIREMENT=CANDIDATE.parent/'R158-orientacao-viga-patamar.json'
DLL=Path('D:/TCC/ferramentas/RevitStairSupport-R159/TccAssistente.RevitStairSupport.dll')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if OUT.exists():raise FileExistsError(OUT)
    current=json.loads(Path('D:/TCC/dados-pesquisa/escada-h03-atual.json').read_text(encoding='utf-8'))
    frozen=json.loads((SOURCE.parent/'R157-resultado.json').read_text(encoding='utf-8'))
    requirement=json.loads(REQUIREMENT.read_text(encoding='utf-8'))
    assert current['landingBeamRequired'] and requirement['landingBeamRequired']
    assert sha(SOURCE)==frozen['copySha256'] and sha(CANDIDATE)==requirement['existingCandidateSha256']
    assert DLL.is_file()
    candidate=json.loads(CANDIDATE.read_text(encoding='utf-8'))
    assert len(candidate['retainedExistingElements'])==60 and candidate['countsByKind']==dict(column=24,beam=30,slab=11)
    manifest=Path(os.environ['APPDATA'])/'Autodesk/Revit/Addins/2027/TccAssistente.StairSupport.addin'
    if manifest.exists():raise FileExistsError(manifest)
    OUT.mkdir();copy=OUT/'H03-R159-Revit-VIGA-PATAMAR-NAO-EXECUTAR.rvt';shutil.copyfile(SOURCE,copy)
    assert sha(copy)==sha(SOURCE)
    config=dict(CandidatePath=str(CANDIDATE),CandidateSha256=sha(CANDIDATE),CopySha256Before=sha(copy))
    (OUT/'R159-config.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
    root=ET.Element('RevitAddIns')
    for name,label,guid,cls in [
        ('TCC Viga Patamar','TCC - aplicar viga patamar R159','035e8989-6f3a-43f5-bc8b-c54ac0e95e33','ApplyCandidate'),
        ('TCC Conferir Viga Patamar','TCC - conferir viga patamar R159','90475041-9d67-45b4-bce1-e09de5ec4489','AuditCandidate')]:
        e=ET.SubElement(root,'AddIn',Type='Command')
        for tag,value in dict(Name=name,Text=label,Assembly=str(DLL),AddInId=guid,FullClassName='TccAssistente.RevitStairSupport.'+cls,VendorId='TCC2',VendorDescription='Candidato comum em copia R159; nao dimensiona; nao executar.').items():ET.SubElement(e,tag).text=value
    raw=ET.tostring(root,encoding='utf-8',xml_declaration=True)
    assert all(Path(a.text).is_file() for a in ET.fromstring(raw).iter('Assembly'))
    (OUT/manifest.name).write_bytes(raw);manifest.write_bytes(raw)
    record=dict(preparedAtUtc=datetime.now(timezone.utc).isoformat(),sourcePath=str(SOURCE),sourceSha256=sha(SOURCE),copyPath=str(copy),copySha256Before=sha(copy),candidatePath=str(CANDIDATE),candidateSha256=sha(CANDIDATE),requirementPath=str(REQUIREMENT),requirementSha256=sha(REQUIREMENT),dllPath=str(DLL),dllSha256=sha(DLL),manifestPath=str(manifest),manifestSha256=sha(manifest),nativeExecutionPerformed=False,structuralApproval=False)
    (OUT/'R159-preparacao.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(copyPath=str(copy),prepared=True,nativeExecutionPerformed=False)))

if __name__=='__main__':main()

"""Prepara cópia isolada e comando explícito; não executa a API do Revit."""
import hashlib
import json
import os
import shutil
from datetime import datetime,timezone
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R155-Revit-17-NAO-EXECUTAR')
DLL=Path('D:/TCC/ferramentas/RevitStairs-R155/TccAssistente.RevitStairs.dll')
SOURCE=Path('D:/TCC/outputs/Materiais-H03-R93-ALINHAMENTO-NAO-EXECUTAR/H03-R93-Revit.rvt')
PLAN=Path('D:/TCC/outputs/Escada-H03-R153-17-9MAIS8-NAO-EXECUTAR/R153-geometria9mais8.json')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if OUT.exists():raise FileExistsError(OUT)
    assert DLL.is_file() and SOURCE.is_file()
    current=json.loads(Path('D:/TCC/dados-pesquisa/escada-h03-atual.json').read_text(encoding='utf-8'))
    assert current['activeRevision']=='H03/R153' and current['definitionSha256']==sha(PLAN)
    OUT.mkdir();copy=OUT/'H03-R155-Revit-ESCADA17-NAO-EXECUTAR.rvt';shutil.copyfile(SOURCE,copy)
    assert sha(copy)==sha(SOURCE)
    (OUT/'R155-config.json').write_text(json.dumps(dict(PlanPath=str(PLAN),PlanSha256=sha(PLAN)),indent=2),encoding='utf-8')
    manifest=r'''<?xml version="1.0" encoding="utf-8"?>
<RevitAddIns>
 <AddIn Type="Command"><Name>TCC Escada17</Name><Text>TCC - lançar escada17 R155</Text><Assembly>D:\TCC\ferramentas\RevitStairs-R155\TccAssistente.RevitStairs.dll</Assembly><AddInId>6e3ce892-99ac-4c35-9f35-b878ccdd13da</AddInId><FullClassName>TccAssistente.RevitStairs.CreateStair</FullClassName><VendorId>TCC2</VendorId><VendorDescription>Estudo local17espelhos; somente cópia R155; não dimensiona.</VendorDescription></AddIn>
 <AddIn Type="Command"><Name>TCC Conferir Escada17</Name><Text>TCC - conferir escada17 R155</Text><Assembly>D:\TCC\ferramentas\RevitStairs-R155\TccAssistente.RevitStairs.dll</Assembly><AddInId>d23fa1c9-7a89-44bf-80e9-cb1edb1d2b81</AddInId><FullClassName>TccAssistente.RevitStairs.AuditStair</FullClassName><VendorId>TCC2</VendorId><VendorDescription>Leitura nativa da escada na cópia R155.</VendorDescription></AddIn>
</RevitAddIns>'''
    target=Path(os.environ['APPDATA'])/'Autodesk/Revit/Addins/2027/TccAssistente.Stairs17.addin'
    if target.exists():raise FileExistsError(target)
    (OUT/'TccAssistente.Stairs17.addin').write_text(manifest,encoding='utf-8');target.write_text(manifest,encoding='utf-8')
    data=dict(createdAtUtc=datetime.now(timezone.utc).isoformat(),sourcePath=str(SOURCE),sourceSha256=sha(SOURCE),copyPath=str(copy),copySha256Before=sha(copy),
        planPath=str(PLAN),planSha256=sha(PLAN),dllPath=str(DLL),dllSha256=sha(DLL),addinPath=str(target),addinSha256=sha(target),
        codeBuildSucceeded=True,notNativeExecution=True,structuralDepthHypothesisM=.14,structuralApproval=False)
    (OUT/'R155-preparacao.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(copyPath=str(copy),sourceHash=sha(SOURCE),codeReady=True)))
if __name__=='__main__':main()

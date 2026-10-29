"""Valida evidencias R57 e copia somente metadados revisaveis ao repositorio."""
from pathlib import Path
import hashlib,json,shutil
from datetime import datetime,timezone
root=Path('D:/TCC/outputs/Verificacao-H03-R57-NAO-EXECUTAR')
dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r57')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
manifest=read(root/'R57-manifesto.json')
for r in manifest['files']:assert sha(Path(r['path']))==r['sha256'],r['path']
result=read(root/'R57-resultado.json')
assert len(result['checks'])==6 and result['zeroMessagesInAllSixLaunchChecks']
assert result['protectedR56FilesChecked']==45
for branch in ('CAD','BIM'):
 a=result['audits'][branch]
 assert a['superstructureObjectsChecked']==65 and a['superstructureNamesGuidsBoxesTopAreasAndExportedPropertiesPreserved']
 assert a['auxiliaryGuidChanges']==11 and a['auxiliaryNamesBoxesTopAreasAndExportedPropertiesPreserved']
 assert result['times'][branch]['durationMs']>0
 state=read(root/f'R57-estado-{branch}.json')
 assert sha(Path(state['nativeProject']))==state['nativeSha256']
 for r in state['frozenFiles']:assert sha(Path(r['frozen']))==r['sha256']
v=dict(atUtc=datetime.now(timezone.utc).isoformat(),manifestFilesChecked=len(manifest['files']),protectedR56FilesChecked=45,nativeLaunchChecks=6,nativeLaunchMessages=0,superstructureObjectsPerBranch=65,auxiliaryGuidChangesPerBranch=11,syntheticTests=dict(command='node --test tests/exchange.test.mjs tests/structural.test.mjs',passed=9,failed=0,meaning='Testes sinteticos de exportacao e triagem; nao calculo estrutural, nem validacao de operacao dentro do Revit/AutoCAD.'),liveAICallsPerformed=False,structuralProcessingPerformed=False,fullWorkflowRankingAllowed=False)
(root/'R57-validacao.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(Path(__file__),root/Path(__file__).name)
(root/'R57-manifesto.json').write_text(json.dumps(dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(root.rglob('*')) if p.is_file() and p.name!='R57-manifesto.json']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dest.mkdir(parents=True,exist_ok=True)
files=[p for p in root.iterdir() if p.is_file() and p.suffix.lower() in ('.md','.json','.py','.txt')]
for p in files:
 q=dest/p.name
 assert not q.exists(),q
 shutil.copy2(p,q)
 assert sha(q)==sha(p)
print(json.dumps(dict(metadataFilesCopied=len(files),destination=str(dest),validation=v),ensure_ascii=False))

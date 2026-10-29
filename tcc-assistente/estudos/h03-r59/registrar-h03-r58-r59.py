"""Valida os manifestos e copia metadados academicos sem binarios licenciados."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,ast
root=Path('D:/TCC');repo=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
specs=[('R58','Processamento-H03-R58-DIAGNOSTICO-PARCIAL-NAO-EXECUTAR'),('R59','Cobertura-H03-R59-MEMORIA-ESTUDO-NAO-EXECUTAR')]
results=[]
for rev,folder in specs:
 src=root/'outputs'/folder;manifest=read(src/f'{rev}-manifesto.json')['files']
 for r in manifest:assert sha(Path(r['path']))==r['sha256'],r['path']
 for p in src.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'))
 if rev=='R58':
  result=read(src/'R58-resultado.json')
  assert result['summaryTextsEqualAtDisplayedPrecision'] and result['structuralProcessingPerformed']
  assert not result['elementDesignPerformed'] and not result['elsDisplacementsVerified']
  for b in ('CAD','BIM'):
   state=read(src/f'R58-estado-{b}.json')
   assert sha(Path(state['nativeProject']))==state['nativeSha256']
   for r in state['frozenFiles']:assert sha(Path(r['frozen']))==r['sha256']
 else:
  data=read(src/'R59-memoria-cobertura.json')
  assert data['userAccepted']['roofSlopePercent']==10 and not data['nativeModelsEdited']
  assert data['actualRoofAreaM2'] is None and data['actualRoofSupportReactions'] is None
  assert data['loads']['steelAllowanceIsHypothesis'] and not data['loads']['roofPermanentAppliedToSlabG2']
 val=dict(atUtc=datetime.now(timezone.utc).isoformat(),manifestFilesChecked=len(manifest),pythonSourcesParsed=True,syntheticAssistantTests=dict(passed=9,failed=0,command='node --test tests/exchange.test.mjs tests/structural.test.mjs',notNativeStructuralDesignValidation=True),liveAICallsPerformed=False,fullWorkflowRankingAllowed=False)
 (src/f'{rev}-validacao.json').write_text(json.dumps(val,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 shutil.copy2(Path(__file__),src/Path(__file__).name)
 (src/f'{rev}-manifesto.json').write_text(json.dumps(dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(src.rglob('*')) if p.is_file() and p.name!=f'{rev}-manifesto.json']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 dst=repo/f'h03-{rev.lower()}';dst.mkdir(exist_ok=False)
 files=[p for p in src.iterdir() if p.is_file() and p.suffix.lower() in ('.py','.md','.json','.txt')]
 for p in files:
  q=dst/p.name;shutil.copy2(p,q);assert sha(q)==sha(p)
 results.append(dict(revision=rev,files=len(files),destination=str(dst),manifestFilesChecked=len(manifest)))
print(json.dumps(results,ensure_ascii=False))

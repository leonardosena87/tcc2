"""Copias independentes R64 para conferir acoes e preparar Q telhado."""
from pathlib import Path
import hashlib,json,shutil
root=Path('D:/TCC');prior=root/'outputs/Cargas-H03-R64-CONFERENCIA-INDIVIDUAL-NAO-EXECUTAR'
out=root/'outputs/Acoes-H03-R66-Q-TELHADO-NAO-EXECUTAR'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not out.exists()
protected=[]
for manifest in [prior/'R64-manifesto.json',root/'outputs/Cobertura-H03-R65-PLANO-Q-NAO-APLICADO/R65-manifesto.json']:
 for r in read(manifest)['files']:
  assert sha(Path(r['path']))==r['sha256'],r['path']
  protected.append(r)
out.mkdir()
(out/'R66-protegidos-R64-R65.json').write_text(json.dumps(protected,ensure_ascii=False,indent=2),encoding='utf-8')
for branch in ('CAD','BIM'):
 state=read(prior/f'R64-estado-{branch}.json')
 dest=root/f'outputs/H03_{branch}_R66_Q_TELHADO_NAO_EXECUTAR'
 dest.mkdir(exist_ok=False)
 for r in state['frozenFiles']:
  p=Path(r['frozen']);assert sha(p)==r['sha256']
  q=dest/p.relative_to(prior/f'congelado-{branch}')
  q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==r['sha256']
 (out/f'R66-preparacao-{branch}.json').write_text(json.dumps(dict(branch=branch,nativeProject=str(dest/'Projeto Eberick'/Path(state['nativeProject']).name),sourceState=str(prior/f'R64-estado-{branch}.json')),ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
print(json.dumps(dict(out=str(out),protected=len(protected))))

"""Prepara copias independentes para ler as treze cargas, sem alterar R63."""
from pathlib import Path
import hashlib,json,shutil
root=Path('D:/TCC')
source=root/'outputs/Cargas-H03-R63-AUDITORIA-G-NAO-EXECUTAR'
out=root/'outputs/Cargas-H03-R64-CONFERENCIA-INDIVIDUAL-NAO-EXECUTAR'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
protected=read(source/'R63-manifesto.json')['files']
for row in protected:assert sha(Path(row['path']))==row['sha256'],row['path']
out.mkdir(exist_ok=False)
(out/'R64-protegidos-R63.json').write_text(json.dumps(protected,ensure_ascii=False,indent=2),encoding='utf-8')
for branch in ('CAD','BIM'):
 state=read(source/f'R63-estado-{branch}.json')
 dest=root/f'outputs/H03_{branch}_R64_CONFERENCIA_INDIVIDUAL_NAO_EXECUTAR'
 dest.mkdir(exist_ok=False)
 for row in state['frozenFiles']:
  p=Path(row['frozen']);assert sha(p)==row['sha256']
  q=dest/p.relative_to(source/f'congelado-{branch}')
  q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==row['sha256']
 (out/f'R64-preparacao-{branch}.json').write_text(json.dumps(dict(branch=branch,nativeProject=str(dest/'Projeto Eberick'/Path(state['nativeProject']).name),sourceState=str(source/f'R63-estado-{branch}.json')),ensure_ascii=False,indent=2),encoding='utf-8')
nodes=[('RC01',110,0,1.419551),('RC02',330,0,1.419551),('RC03',547.5,0,1.387289),('RC04',110,390,2.566112),('RC05',330,390,2.566112),('RC06',547.5,390,2.507791),('RC07',732.5,390,.807804),('RC08',887.5,390,.807804),('RC09',110,705,1.146561),('RC10',330,705,1.146561),('RC11',547.5,705,1.120503),('RC12',732.5,705,.807804),('RC13',887.5,705,.807804)]
(out/'R64-plano.json').write_text(json.dumps([dict(id=n,xCm=x,yCm=y,action='Adicional',fzKN=-f) for n,x,y,f in nodes],ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
print(json.dumps(dict(out=str(out),protected=len(protected),plannedReads=26)))

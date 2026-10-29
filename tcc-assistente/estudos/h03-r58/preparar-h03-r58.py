"""Copia os estados R57 congelados para diagnostico parcial independente."""
from pathlib import Path
import json,hashlib,shutil
root=Path('D:/TCC');src=root/'outputs/Verificacao-H03-R57-NAO-EXECUTAR';out=root/'outputs/Processamento-H03-R58-DIAGNOSTICO-PARCIAL-NAO-EXECUTAR'
out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((src/'R57-manifesto.json').read_text(encoding='utf-8'))['files']
for r in manifest:assert sha(Path(r['path']))==r['sha256'],r['path']
(out/'R58-protegidos-R57.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
for b in ('CAD','BIM'):
 state=json.loads((src/f'R57-estado-{b}.json').read_text(encoding='utf-8'))
 dst=root/f'outputs/H03_{b}_R58_DIAGNOSTICO_PARCIAL_NAO_EXECUTAR';dst.mkdir(exist_ok=False);files=[]
 for r in state['frozenFiles']:
  p=Path(r['frozen']);assert sha(p)==r['sha256'];q=dst/p.relative_to(src/f'congelado-{b}');q.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(p,q);assert sha(q)==r['sha256']
  files.append(dict(source=str(p),copy=str(q),sha256=sha(q)))
 prep=dict(branch=b,nativeProject=str(dst/'Projeto Eberick'/Path(state['nativeProject']).name),files=files,scope='Diagnostico de processamento com cargas parciais; sem validacao normativa ou projeto executivo',plannedEngineeringChanges=False)
 (out/f'R58-preparacao-{b}.json').write_text(json.dumps(prep,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
print(out)

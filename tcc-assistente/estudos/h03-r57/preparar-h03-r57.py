"""Cria copias independentes R57 para verificacao nativa de lancamento."""
from pathlib import Path
import json,hashlib,shutil
root=Path('D:/TCC');src=root/'outputs/Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR';out=root/'outputs/Verificacao-H03-R57-NAO-EXECUTAR';out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((src/'R56-manifesto.json').read_text(encoding='utf-8'))['files']
for r in manifest:assert sha(Path(r['path']))==r['sha256'],r['path']
(out/'R57-protegidos-R56.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
for b in ('CAD','BIM'):
 d=json.loads((src/f'R56-estado-{b}.json').read_text(encoding='utf-8'));dst=root/f'outputs/H03_{b}_R57_VERIFICACAO_NAO_EXECUTAR';dst.mkdir(exist_ok=False);files=[]
 for r in d['frozenFiles']:
  p=Path(r['frozen']);assert sha(p)==r['sha256'];q=dst/p.relative_to(src/f'congelado-{b}');q.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(p,q);assert sha(q)==r['sha256'];files.append(dict(source=str(p),copy=str(q),sha256=sha(q)))
 (out/f'R57-preparacao-{b}.json').write_text(json.dumps(dict(branch=b,nativeProject=str(dst/'Projeto Eberick'/Path(d['nativeProject']).name),files=files,plannedFloors=['N2','N1','N0'],scope='Somente verificacao de lancamento; nao dimensionamento/calculo'),ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
print(out)

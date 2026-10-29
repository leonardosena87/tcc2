"""Copias de ensaio para lancamento de reacoes permanentes parciais R60."""
from pathlib import Path
import json,hashlib,shutil
root=Path('D:/TCC');src=root/'outputs/Processamento-H03-R58-DIAGNOSTICO-PARCIAL-NAO-EXECUTAR';out=root/'outputs/Cargas-H03-R61-TELHADO-G-PARCIAL-NAO-EXECUTAR';out.mkdir(exist_ok=False)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(src/'R58-manifesto.json')['files']
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
(out/'R61-protegidos-R58.json').write_text(json.dumps(protected,indent=2),encoding='utf-8')
for b in ('CAD','BIM'):
 state=read(src/f'R58-estado-{b}.json');dst=root/f'outputs/H03_{b}_R61_TELHADO_G_PARCIAL_NAO_EXECUTAR';dst.mkdir(exist_ok=False);files=[]
 for r in state['frozenFiles']:
  p=Path(r['frozen']);assert sha(p)==r['sha256'];q=dst/p.relative_to(src/f'congelado-{b}');q.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(p,q);assert sha(q)==r['sha256'];files.append(dict(source=str(p),copy=str(q),sha256=sha(q)))
 (out/f'R61-preparacao-{b}.json').write_text(json.dumps(dict(branch=b,nativeProject=str(dst/'Projeto Eberick'/Path(state['nativeProject']).name),files=files,planned='Ensaio G descendente R60: 13 pontos, soma18.511248004822kN. Q do telhado nao aplicado; etapas precisam verificacao nativa e de persistencia.'),ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
print(out)

"""Copias independentes da tentativa R62 para auditoria das cargas nodais."""
from pathlib import Path
import hashlib,json,shutil
root=Path('D:/TCC');src=root/'outputs/Cargas-H03-R62-TELHADO-G-PARCIAL-NAO-EXECUTAR';out=root/'outputs/Cargas-H03-R63-AUDITORIA-G-NAO-EXECUTAR'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(src/'R62-manifesto.json')['files']
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
out.mkdir(exist_ok=False)
(out/'R63-protegidos-R62.json').write_text(json.dumps(protected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for b in ('CAD','BIM'):
    state=read(src/f'R62-estado-{b}.json');dst=root/f'outputs/H03_{b}_R63_AUDITORIA_G_NAO_EXECUTAR';dst.mkdir(exist_ok=False)
    for r in state['frozenFiles']:
        p=Path(r['frozen']);assert sha(p)==r['sha256'];q=dst/p.relative_to(src/f'congelado-{b}');q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==r['sha256']
    (out/f'R63-preparacao-{b}.json').write_text(json.dumps(dict(branch=b,nativeProject=str(dst/'Projeto Eberick'/Path(state['nativeProject']).name),sourceState=str(src/f'R62-estado-{b}.json'),status='Copia para auditoria; cargas ainda nao validadas'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
print(out)

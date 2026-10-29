"""Prepara copia independente para parametros, mantendo as evidencias geométricas."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,sys,time
branch=sys.argv[1];assert branch in ('BIM','CAD')
start=time.perf_counter();root=Path('D:/TCC')
if branch=='BIM':
    source=root/'outputs/Complementacao-H03-R50-LAJES-BIM-NAO-EXECUTAR'
    state=json.loads((source/'R50-estado-atual.json').read_text(encoding='utf-8-sig'))
else:
    source=root/'outputs/Complementacao-H03-R49-LAJES-CAD-NAO-EXECUTAR'
    state=json.loads((source/'R49-estado-parcial.json').read_text(encoding='utf-8-sig'))
dst=root/f'outputs/H03_{branch}_R51_PARAMETROS_NAO_EXECUTAR'
out=root/'outputs/Conferencia-H03-R51-PARAMETROS-NAO-EXECUTAR';out.mkdir(exist_ok=True)
target=dst/'Projeto Eberick';target.mkdir(parents=True,exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for row in state['frozenFiles']:
    a=Path(row['frozen']);parts=a.parts
    if 'Projeto Eberick' not in parts or a.suffix.lower()=='.errlog':continue
    assert sha(a)==row['sha256'],str(a)
    rel=Path(*parts[parts.index('Projeto Eberick')+1:]);b=target/rel
    b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
    assert sha(b)==sha(a);rows.append(dict(source=str(a),copy=str(b),sha256=sha(b)))
prj=target/Path(state['nativeProject']).name;assert prj.exists()
result=dict(branch=branch,atUtc=datetime.now(timezone.utc).isoformat(),nativeProject=str(prj),files=rows,
    elapsedScriptMs=(time.perf_counter()-start)*1000,status='Copia preparada; parametros ainda nao conferidos.',
    limits=['Preserva nome-base para recursos relativos; pasta identifica R51.',
            'Copia do estado congelado proprio de cada ramo; nao transplanta CAD para BIM ou vice-versa.',
            'Tempo de script separado do intervalo assistido, que pode inclui-lo.'])
(out/f'R51-preparacao-{branch}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(branch=branch,nativeProject=str(prj),files=len(rows))))

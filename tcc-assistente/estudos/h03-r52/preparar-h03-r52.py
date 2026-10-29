"""Copia estados proprios R51 para estudo de vinculos, sem misturar os fluxos."""
from pathlib import Path
import json,hashlib,shutil
root=Path('D:/TCC');src=root/'outputs/Conferencia-H03-R51-PARAMETROS-NAO-EXECUTAR'
out=root/'outputs/Conferencia-H03-R52-VINCULOS-NAO-EXECUTAR';out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for branch in ('CAD','BIM'):
    data=json.loads((src/f'R51-parametros-{branch}.json').read_text(encoding='utf-8-sig'))
    native=root/f'outputs/H03_{branch}_R52_VINCULOS_NAO_EXECUTAR';native.mkdir(exist_ok=False)
    rows=[]
    for row in data['frozenFiles']:
        a=Path(row['frozen']);assert sha(a)==row['sha256']
        rel=a.relative_to(src/f'congelado-{branch}');b=native/rel
        b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
        assert sha(a)==sha(b);rows.append(dict(source=str(a),copy=str(b),sha256=sha(b)))
    result=dict(branch=branch,nativeProject=str(native/'Projeto Eberick'/Path(data['nativeProject']).name),files=rows,status='Copia preparada; vinculos ainda nao verificados.')
    (out/f'R52-preparacao-{branch}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(branch=branch,files=len(rows),nativeProject=result['nativeProject'])))
shutil.copy2(Path(__file__),out/Path(__file__).name)

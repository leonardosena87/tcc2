import json
import shutil
from pathlib import Path
from altimetria import HERE,OUT,sha

if __name__=='__main__':
    r=json.loads((OUT/'R142-altimetria.json').read_text(encoding='utf-8'))
    for s in [r['architecture'],r['r112Source'],*r['structuralReferenceExports']]:
        if sha(s['path'])!=s['sha256']:raise ValueError('Fonte alterada')
    for p in OUT.iterdir():
        if not p.is_file() or p.name=='R142-manifesto.json':continue
        if p.suffix not in ['.json','.md']:raise ValueError('Arquivo fora da lista pública')
        target=HERE/p.name
        if target.exists() and sha(target)!=sha(p):raise ValueError('Registro divergente')
        shutil.copyfile(p,target)
    (HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    entries=[{'path':p.name,'sha256':sha(p)} for p in sorted(HERE.iterdir())
        if p.is_file() and p.name!='R142-manifesto.json']
    for base in [HERE,OUT]:
        (base/'R142-manifesto.json').write_text(json.dumps({'revision':'H03/R142','publicFiles':entries},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'manifestedFiles':len(entries),'sourceHashesVerified':4}))

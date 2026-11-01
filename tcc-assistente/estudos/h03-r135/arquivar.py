import json
import shutil
from auditar import HERE, OUT, sha

if __name__=='__main__':
    # Somente evidências válidas e consolidações; não copiar quarentena ou binários.
    for p in OUT.iterdir():
        if not p.is_file():
            continue
        if p.name.startswith(('CAD-recuperado-croqui','CAD-recuperado-W20','CAD-recuperado-acoes',
                              'BIM-recuperado-croqui','BIM-recuperado-W20','BIM-recuperado-acoes')) or p.suffix=='.dxf' or (
                p.suffix=='.json' and not p.name.endswith('-captura.json')) or p.name=='LEIA-ME-R135.md':
            target = HERE/p.name
            if target.exists() and sha(target)!=sha(p):
                raise ValueError('Evidência divergente')
            shutil.copyfile(p,target)
    (HERE/'.gitattributes').write_text('* -text\n*.dxf whitespace=-blank-at-eol\n',encoding='utf-8')
    data = {'revision':'H03/R135','publicFiles':[
        {'path':p.relative_to(HERE).as_posix(),'sha256':sha(p)}
        for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and 'manifesto' not in p.name]}
    for base in [HERE,OUT]:
        (base/'R135-manifesto.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'publicFiles':len(data['publicFiles'])}))

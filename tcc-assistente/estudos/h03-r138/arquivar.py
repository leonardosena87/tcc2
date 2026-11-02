import json
import shutil
from auditar import HERE,OUT,sha

if __name__=='__main__':
    for p in OUT.rglob('*'):
        if not p.is_file() or 'congelados-apos-processamento' in p.parts or 'manifesto' in p.name:continue
        if p.suffix not in {'.json','.jpg','.txt','.md', '.$2k'}:continue
        target=HERE/p.relative_to(OUT)
        target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() and sha(target)!=sha(p):raise ValueError('Evidência divergente')
        shutil.copyfile(p,target)
    (HERE/'.gitattributes').write_text('* -text\n*.$2k whitespace=-blank-at-eol\n',encoding='utf-8')
    data={'revision':'H03/R138','publicFiles':[{'path':p.relative_to(HERE).as_posix(),'sha256':sha(p)} for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and 'manifesto' not in p.name]}
    for base in [HERE,OUT]:(base/'R138-manifesto.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'publicFiles':len(data['publicFiles'])}))

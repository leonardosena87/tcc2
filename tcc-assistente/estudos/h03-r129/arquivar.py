import json
import shutil
from pathlib import Path
from consolidar import OUT,sha
HERE=Path(__file__).parent
if __name__=='__main__':
    for p in OUT.iterdir():
        if p.is_file() and p.suffix in {'.json','.jpg','.txt','.md'} and 'manifesto' not in p.name:
            target=HERE/p.name
            if target.exists() and sha(target)!=sha(p):raise ValueError('Evidência divergente')
            shutil.copyfile(p,target)
    (HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    data={'revision':'H03/R129','publicFiles':[{'path':p.relative_to(HERE).as_posix(),'sha256':sha(p)} for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and 'manifesto' not in p.name]}
    for base in [HERE,OUT]:(base/'R129-manifesto.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'publicFiles':len(data['publicFiles'])}))

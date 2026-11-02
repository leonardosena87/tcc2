import json
import shutil
from consolidar import HERE,OUT,sha


if __name__=='__main__':
    for p in OUT.iterdir():
        if p.is_file() and p.suffix in {'.json','.txt','.jpg'} and 'manifesto' not in p.name:
            dest=HERE/p.name
            if dest.exists() and sha(dest)!=sha(p):raise ValueError('Evidência divergente: '+p.name)
            shutil.copyfile(p,dest)
    (HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    shutil.copyfile(HERE/'LEIA-ME-R148.md',OUT/'LEIA-ME-R148.md')
    m=dict(revision='H03/R148',nativeBinariesRemainLocalOnly=True,
        publicFiles=[dict(path=p.relative_to(HERE).as_posix(),sha256=sha(p)) for p in sorted(HERE.rglob('*'))
                     if p.is_file() and '__pycache__' not in p.parts and 'manifesto' not in p.name])
    for base in (HERE,OUT):(base/'R148-manifesto.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'publicFiles':len(m['publicFiles'])}))

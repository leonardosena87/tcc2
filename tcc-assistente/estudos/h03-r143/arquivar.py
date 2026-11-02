"""Arquiva somente evidências públicas do ensaio; nativos ficam em D:/TCC."""
import json
import shutil
from auditar import HERE,OUT,sha

if __name__=='__main__':
    result=json.loads((OUT/'R143-resultado.json').read_text(encoding='utf-8'))
    for r in result['sourceR116FilesPreserved']:
        if sha(__import__('pathlib').Path(r['path']))!=r['sha256']:raise ValueError('Fonte mudou')
    for p in OUT.iterdir():
        if not p.is_file() or p.suffix not in {'.json','.md','.txt','.jpg'} or p.name=='R143-manifesto.json':continue
        dst=HERE/p.name
        if dst.exists() and sha(dst)!=sha(p):raise ValueError('Arquivo público divergente')
        shutil.copyfile(p,dst)
    shutil.copytree(OUT/'SAP-CAD',HERE/'SAP-CAD',dirs_exist_ok=True)
    (HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    entries=[{'path':p.relative_to(HERE).as_posix(),'sha256':sha(p)} for p in sorted(HERE.rglob('*'))
        if p.is_file() and '__pycache__' not in p.parts and p.name!='R143-manifesto.json']
    for base in [HERE,OUT]:
        (base/'R143-manifesto.json').write_text(json.dumps({'revision':'H03/R143','publicFiles':entries},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'publicFiles':len(entries),'nativeFilesIncluded':False}))

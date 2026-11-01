import hashlib
import json
import shutil
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Resultados-H03-R128-PARCIAIS-NAO-EXECUTAR')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
    for name in ['R128-resultados-parciais.json','LEIA-ME-R128.md']:
        src,dst=OUT/name,HERE/name
        if dst.exists() and sha(dst)!=sha(src):raise ValueError('Resultado existente divergente')
        shutil.copyfile(src,dst)
    data={'revision':'H03/R128','publicFiles':[{'path':p.relative_to(HERE).as_posix(),'sha256':sha(p)} for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and 'manifesto' not in p.name]}
    for base in [HERE,OUT]:(base/'R128-manifesto.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'publicFiles':len(data['publicFiles'])}))

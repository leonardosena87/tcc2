import json
import shutil
from comparar import HERE, OUT, r122


if __name__ == '__main__':
    for name in ['R123-resultado-final.json', 'R123-orientacao.json']:
        src, dst = OUT / name, HERE / name
        if dst.exists() and r122.sha(src) != r122.sha(dst):
            raise ValueError('Evidência existente divergente')
        shutil.copyfile(src, dst)
    shutil.copyfile(HERE / 'LEIA-ME-R123.md', OUT / 'LEIA-ME-R123.md')
    rows = [{'path': p.relative_to(HERE).as_posix(), 'sha256': r122.sha(p)} for p in sorted(HERE.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and 'manifesto' not in p.name]
    manifest = {'revision': 'H03/R123', 'publicFiles': rows, 'nativeBinariesIncluded': False}
    for base in [HERE, OUT]:
        (base / 'R123-manifesto.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'publicFiles': len(rows)}))

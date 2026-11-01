import hashlib
import json
import shutil
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Armadura-H03-R118-CONSULTA-NAO-EXECUTAR')


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


if __name__ == '__main__':
    for p in OUT.iterdir():
        if p.is_file() and p.suffix in {'.json', '.txt', '.jpg'} and 'manifesto' not in p.name:
            target = HERE / p.name
            if target.exists() and sha(target) != sha(p): raise ValueError('Evidencia divergente: ' + p.name)
            shutil.copyfile(p, target)
    for name in ['LEIA-ME-R118.md', 'transcricao-visual.json']: shutil.copyfile(HERE / name, OUT / name)
    manifest = {'revision': 'H03/R118', 'nativeBinariesRemainLocalOnly': True,
                'publicFiles': [{'path': p.relative_to(HERE).as_posix(), 'sha256': sha(p)}
                                for p in sorted(HERE.rglob('*')) if p.is_file()
                                and '__pycache__' not in p.parts and 'manifesto' not in p.name]}
    for base in [HERE, OUT]:
        (base / 'R118-manifesto.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'publicFiles': len(manifest['publicFiles'])}))

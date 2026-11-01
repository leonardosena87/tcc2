"""Copia evidencias textuais e imagens; mantem PRJ/SAV locais."""
import hashlib
import json
import shutil
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Analise-H03-R116-P2-NAO-EXECUTAR')


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    for p in OUT.iterdir():
        if p.is_file() and p.suffix in {'.txt', '.jpg', '.json'} and 'manifesto' not in p.name:
            target = HERE / p.name
            if target.exists() and sha(target) != sha(p):
                raise ValueError('Evidencia divergente: ' + p.name)
            shutil.copyfile(p, target)
    shutil.copyfile(HERE / 'LEIA-ME-R116.md', OUT / 'LEIA-ME-R116.md')
    result = json.loads((OUT / 'R116-resultado.json').read_text(encoding='utf-8'))
    manifest = {'revision': 'H03/R116', 'nativeBinariesRemainLocalOnly': True,
                'publicFiles': [{'path': p.relative_to(HERE).as_posix(), 'sha256': sha(p)}
                                for p in sorted(HERE.rglob('*')) if p.is_file()
                                and '__pycache__' not in p.parts and 'manifesto' not in p.name],
                'nativeProjects': {b: {'path': v['projectPath'], 'sha256': v['projectSha256'],
                                       'frozenFiles': v['frozenFiles']} for b, v in result['branches'].items()}}
    for base in [HERE, OUT]:
        (base / 'R116-manifesto.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'publicFiles': len(manifest['publicFiles'])}))


if __name__ == '__main__':
    main()

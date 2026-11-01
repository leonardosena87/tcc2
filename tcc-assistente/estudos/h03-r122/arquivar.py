"""Arquiva evidências e exportações textuais; PRJ e demais binários ficam em D:/TCC."""
import json
import shutil
from pathlib import Path
from consolidar import HERE, OUT, sha


def main():
    sources = [p for p in OUT.iterdir() if p.is_file() and p.suffix in {'.json', '.txt', '.jpg'} and 'manifesto' not in p.name]
    sources += list(OUT.glob('SAP-*/*.$2k'))
    for src in sources:
        target = HERE / src.relative_to(OUT)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and sha(target) != sha(src):
            raise ValueError('Não substituir evidência divergente: ' + str(target))
        shutil.copyfile(src, target)
    shutil.copyfile(HERE / 'LEIA-ME-R122.md', OUT / 'LEIA-ME-R122.md')
    rows = [{'path': p.relative_to(HERE).as_posix(), 'sha256': sha(p)} for p in sorted(HERE.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and 'manifesto' not in p.name]
    manifest = {'revision': 'H03/R122', 'nativeBinariesRemainLocalOnly': True,
                'nativeTextExportsIncluded': True, 'publicFiles': rows}
    for base in [HERE, OUT]:
        (base / 'R122-manifesto.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'publicFiles': len(rows)}))


if __name__ == '__main__':
    main()

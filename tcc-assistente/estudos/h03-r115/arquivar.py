"""Arquiva evidencias e manifestos; nao copia binarios nativos para o repositorio publico."""
import hashlib
import json
import shutil
from pathlib import Path

REPO = Path(__file__).parent
ROOT = Path('D:/TCC/outputs')


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def archive(revision, folder):
    out = ROOT / folder
    repo = REPO.parent / f'h03-r{revision}'
    for p in sorted(out.iterdir()):
        if p.is_file() and p.suffix.lower() in {'.json', '.txt', '.jpg'} and 'manifesto' not in p.name:
            target = repo / p.name
            if target.exists() and sha(target) != sha(p):
                raise ValueError('Evidencia divergente ja existente: ' + str(target))
            shutil.copyfile(p, target)
    shutil.copyfile(repo / f'LEIA-ME-R{revision}.md', out / f'LEIA-ME-R{revision}.md')
    public = [{'path': p.relative_to(repo).as_posix(), 'sha256': sha(p)} for p in sorted(repo.rglob('*'))
              if p.is_file() and '__pycache__' not in p.parts and 'manifesto' not in p.name]
    manifest = {'revision': f'H03/R{revision}', 'publicFiles': public,
                'nativeBinariesRemainLocalOnly': True}
    if revision == 115:
        result = json.loads((out / 'R115-resultado.json').read_text(encoding='utf-8'))
        manifest['nativeProjects'] = {b: {'path': v['projectPath'], 'sha256': v['projectSha256'],
                                         'frozenFiles': v['frozenFiles']} for b, v in result['branches'].items()}
    body = json.dumps(manifest, ensure_ascii=False, indent=2)
    for base in [repo, out]:
        (base / f'R{revision}-manifesto.json').write_text(body, encoding='utf-8')
    print(json.dumps({'revision': revision, 'publicFiles': len(public)}))


if __name__ == '__main__':
    archive(114, 'Cobertura-H03-R114-P2-HIPOTESE-NAO-EXECUTAR')
    archive(115, 'Telhado-P2-H03-R115-SENSIBILIDADE-NAO-EXECUTAR')

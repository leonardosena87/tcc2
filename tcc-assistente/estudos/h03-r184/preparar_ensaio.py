"""Copia receptores R182 para ensaio isolado; nao opera a interface."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

OUT = Path('D:/TCC/outputs/Escada-H03-R184-ENSAIO-GANCHO-NAO-EXECUTAR')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    reference = json.loads(Path('D:/TCC/outputs/Escada-H03-R183-LEITURA-APOIOS-NAO-EXECUTAR/R183-leitura-apoios.json').read_text(encoding='utf-8'))
    destinations = {b: Path(f'D:/TCC/outputs/R184-{b}-ENSAIO-GANCHO-NAO-EXECUTAR') for b in ('CAD', 'BIM')}
    for b, dest in destinations.items():
        if dest.exists():
            raise FileExistsError(dest)
        p = Path(reference['sourceProjects'][b]['path'])
        if sha(p) != reference['sourceProjects'][b]['sha256']:
            raise ValueError('Fonte alterada: ' + b)
    OUT.mkdir(exist_ok=False)
    branches = {}
    for b, dest in destinations.items():
        p = Path(reference['sourceProjects'][b]['path'])
        root = p.parent.parent
        files = [dict(relativePath=str(x.relative_to(root)), sha256=sha(x))
                 for x in sorted(root.rglob('*')) if x.is_file()]
        shutil.copytree(root, dest, ignore=shutil.ignore_patterns('~$*', '*.lck', '*.lock'))
        copy = dest / p.relative_to(root)
        if sha(copy) != sha(p):
            raise ValueError('Copia divergente: ' + b)
        branches[b] = dict(sourceRoot=str(root), sourceFiles=files,
            projectPath=str(copy), initialProjectSha256=sha(copy))
    result = dict(revision='H03/R184', preparedAtUtc=datetime.now(timezone.utc).isoformat(),
        plannedChange='Somente Detalhamento Lajes: reta -> gancho; recalculo experimental de escadas',
        geometryChangePlanned=False, supportWidthChangePlanned=False,
        forceThresholdChangePlanned=False, originalReferencesPreserved=True, branches=branches,
        inheritedExportsAreNotNewEvidence=True, fullSizingApproval=False)
    (OUT / 'R184-preparacao.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({b:x['projectPath'] for b,x in branches.items()}))


if __name__ == '__main__':
    main()

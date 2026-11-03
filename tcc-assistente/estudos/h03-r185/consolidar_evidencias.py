from pathlib import Path
import json
import shutil
from reconciliar_vigas import HERE, OUT, sha


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    result_path = OUT / 'R185-reconciliacao-vigas.json'
    r = json.loads(result_path.read_text(encoding='utf-8'))
    for source in r['sources'].values():
        if sha(source['path']) != source['sha256']:
            raise ValueError('Fonte alterada apos auditoria')
    pointer = Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    backup = OUT / 'R185-ponteiro-anterior.json'
    if not backup.exists():
        shutil.copy2(pointer, backup)
    current = json.loads(pointer.read_text(encoding='utf-8-sig'))
    current.update(latestBeamGroupingAuditRevision='H03/R185',
        latestBeamGroupingAuditPath=str(result_path), latestBeamGroupingAuditSha256=sha(result_path),
        baselineR178MatchedBeamPhysicalPieces=len(r['reconciliation']['pairs']),
        baselineR178BeamGroups={b:x['nativeNameLevelGroups'] for b,x in r['branches'].items()},
        baselineBeamPrismEqualityIsNotFullAnalyticalEquivalence=True,
        correctionRankingValid=False, fullPairedFlowComparisonFinished=False)
    write(pointer, current)
    write(OUT / 'R185-ponteiro-atualizado.json', current)
    for name in ('R185-reconciliacao-vigas.json', 'R185-correspondencia-vigas.md', 'R185-ponteiro-atualizado.json'):
        shutil.copy2(OUT / name, HERE / name)
    shutil.copy2(HERE / 'LEIA-ME-R185.md', OUT / 'LEIA-ME-R185.md')
    files = [p for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'R185-manifesto.json']
    manifest = dict(revision='H03/R185', files=[dict(relativePath=p.name, bytes=p.stat().st_size,
        sha256=sha(p)) for p in files])
    write(HERE / 'R185-manifesto.json', manifest)
    shutil.copy2(HERE / 'R185-manifesto.json', OUT / 'R185-manifesto.json')
    print(json.dumps(dict(files=len(files), matchedPieces=len(r['reconciliation']['pairs']))))


if __name__ == '__main__':
    main()

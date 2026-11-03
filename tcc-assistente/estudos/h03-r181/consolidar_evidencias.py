"""Publica apenas evidencias locais selecionadas e preserva o ponteiro anterior."""
from pathlib import Path
from datetime import datetime,timezone
import json,shutil
from conferir_ligacao import OUT,HERE,sha


def write(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')


def main():
    result=OUT/'R181-ligacao-patamar.json'
    data=json.loads(result.read_text(encoding='utf-8'))
    if not data['frontDifferenceIsNotAnUnsupportedGapAtCheckedBeamFace']:
        raise ValueError('Contato local nao confirmado')
    for row in data['sourceFilesPreserved']:
        if sha(row['path'])!=row['sha256']:
            raise ValueError('Fonte mudou antes da consolidacao')
    pointer=Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    backup=OUT/'R181-ponteiro-anterior.json'
    if not backup.exists():
        shutil.copy2(pointer,backup)
    current=json.loads(pointer.read_text(encoding='utf-8-sig'))
    current.update(latestLandingBeamFaceAuditRevision='H03/R181',
        latestLandingBeamFaceAuditPath=str(result),latestLandingBeamFaceAuditSha256=sha(result),
        landingFrontDifferenceReclassifiedAsRepresentationAtCheckedFace=True,
        unsupportedGapAtCheckedV16FaceObserved=False,
        landingBeamFaceSectionAreaM2=0.273,
        exportedLandingGridBeamSharedNodeCountEachBranch=4,
        experimentalStairLandingContourNeedsReconciliation=True,
        experimentalStairUniformityStrictAuditPassed=False,
        nativeLandingSupportRotationAndReinforcementReviewed=False,
        fullPairedFlowComparisonFinished=False,fullAnalyticalEquivalenceVerified=False)
    write(pointer,current)
    shutil.copy2(pointer,OUT/'R181-ponteiro-atualizado.json')
    for name in ['R181-ligacao-patamar.json','R181-ligacao-patamar.png',
                 'R181-ponteiro-atualizado.json','CAD-grelha-patamar-0.png','CAD-grelha-patamar-AX.txt']:
        shutil.copy2(OUT/name,HERE/name)
    shutil.copy2(HERE/'LEIA-ME-R181.md',OUT/'LEIA-ME-R181.md')
    files=[p for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='R181-manifesto.json']
    manifest=dict(revision='H03/R181',createdAtUtc=datetime.now(timezone.utc).isoformat(),
        files=[dict(relativePath=p.name,bytes=p.stat().st_size,sha256=sha(p)) for p in files])
    write(HERE/'R181-manifesto.json',manifest)
    shutil.copy2(HERE/'R181-manifesto.json',OUT/'R181-manifesto.json')
    print(json.dumps(dict(files=len(files),resultSha256=sha(result))))


if __name__=='__main__':
    main()

"""Incorpora a decisão que substituiu a retomada original durante a interrupção."""
import hashlib
import json
import shutil
from datetime import datetime,timezone
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R154-RETOMADA-ORIGINAL-NAO-EXECUTAR')
CURRENT=Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    decision=OUT/'R154-decisao-final17.json'
    if decision.exists():raise FileExistsError(decision)
    previous=json.loads(CURRENT.read_text(encoding='utf-8'))
    assert previous['activeRevision']=='H03/R154'
    restored=json.loads((OUT/'R154-definicao-anterior.json').read_text(encoding='utf-8'))
    assert restored['activeRevision']=='H03/R153'
    source=Path(restored['definitionPath']);data=json.loads(source.read_text(encoding='utf-8'))
    assert sha(source)==restored['definitionSha256']
    g=data['geometry'];assert (g['totalRisers'],g['lowerFlightRisers'],g['upperFlightRisers'])==(17,9,8)
    assert abs(g['finishedGroundM']+17*g['uniformRiserM']-g['finishedUpperM'])<1e-12
    shutil.copyfile(CURRENT,OUT/'R154-estado-interrompido.json')
    record=dict(createdAtUtc=datetime.now(timezone.utc).isoformat(),
        exactUserInstruction='deixe com 17 mesmo. temos que adiantar',
        supersedes='Retomada original solicitada anteriormente na R154',
        restoredDefinitionPath=str(source),restoredDefinitionSha256=sha(source),
        totalRisers=17,lowerFlightRisers=9,upperFlightRisers=8,
        finishedLandingM=g['proposedFinishedLandingM'],uniformRiserM=g['uniformRiserM'],treadM=g['treadHypothesisM'],
        concentratedTwoRiserCorrectionAdopted=False,nativeProjectsEdited=False,structuralApproval=False)
    decision.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    restored.update(activeChoice='17 espelhos; 9+8, U com patamar; desenvolvimento retomado',
        latestDecisionPath=str(decision),latestDecisionSha256=sha(decision),
        interruptedOriginalReferencePreservedAt=str(OUT/'R154-estado-interrompido.json'))
    CURRENT.write_text(json.dumps(restored,ensure_ascii=False,indent=2),encoding='utf-8')
    reread=json.loads(CURRENT.read_text(encoding='utf-8'))
    assert reread['activeRevision']=='H03/R153' and sha(Path(reread['definitionPath']))==reread['definitionSha256']
    for p in OUT.iterdir():
        if p.is_file() and 'manifesto' not in p.name and p.name!='LEIA-ME-R154.md':shutil.copyfile(p,HERE/p.name)
    shutil.copyfile(HERE/'LEIA-ME-R154.md',OUT/'LEIA-ME-R154.md')
    manifest=[dict(path=p.name,sha256=sha(p)) for p in sorted(HERE.iterdir()) if p.is_file() and 'manifesto' not in p.name]
    for folder in (HERE,OUT):(folder/'R154-manifesto.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('Definição ativa restabelecida:17 espelhos,9+8, patamar acabado+1,824118m; correção concentrada não aplicada.')

if __name__=='__main__':main()

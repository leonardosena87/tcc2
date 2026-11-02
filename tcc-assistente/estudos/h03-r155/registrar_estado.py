"""Registra o estado verificado sem promover a escada ao modelo de cálculo."""
import json
import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from consolidar import OUT,archive,sha

def main():
    result=json.loads((OUT/'R155-resultado.json').read_text(encoding='utf-8'))
    assert result['nativeCreatedSavedReopenedReadbackMatched']
    start=json.loads((OUT/'Revit-inicio.json').read_text(encoding='utf-8'))
    end=json.loads((OUT/'Revit-sessao-observada-fim.json').read_text(encoding='utf-8'))
    parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
    duration=end['mono']-start['mono']
    utc_duration=(parse(end['utc'])-parse(start['utc'])).total_seconds()*1000
    assert duration>0 and utc_duration>0
    timing=dict(start=start,end=end,elapsedMonotonicMs=duration,elapsedUtcMs=utc_duration,
        monotonicMinusUtcMs=duration-utc_duration,commandMs=result['commandMs'],
        commandIncludedInSession=True,sessionIncludesWaitingBuildFixAndUiFailures=True,
        humanActiveTimeUnknown=True,aiInferenceTimeUnknown=True,pairedCadMeasurementAvailable=False,
        usableForFlowRanking=False,doNotSumNestedIntervals=True)
    (OUT/'R155-tempos.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf-8')
    current=Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    previous=json.loads(current.read_text(encoding='utf-8'))
    assert previous['activeRevision']=='H03/R153'
    assert sha(Path(previous['definitionPath']))==previous['definitionSha256']
    backup=OUT/'R155-apontador-anterior.json'
    if backup.exists():raise FileExistsError(backup)
    shutil.copyfile(current,backup)
    previous.update(nativeRevitRevision='H03/R155',nativeRevitCopyPath=result['copyPath'],
        nativeRevitReadbackEvidence=str(OUT/'R155-resultado.json'),
        nativeRevitReadbackEvidenceSha256=sha(OUT/'R155-resultado.json'),
        nativeRevitCreatedSavedReopened=True,nativePlacementResolved=False,
        nativeProjectsUpdated=False,stairIntegratedInCalculationModel=False,
        stairCadStructuralGeometryEquivalent=False,visualStairInspectionCompleted=False,finalApproval=False)
    current.write_text(json.dumps(previous,ensure_ascii=False,indent=2),encoding='utf-8')
    shutil.copyfile(current,OUT/'R155-apontador-atual.json')
    archive()
    print(json.dumps(dict(sessionMinutes=duration/60000,commandMs=result['commandMs'],flowRanking=False)))

if __name__=='__main__':main()

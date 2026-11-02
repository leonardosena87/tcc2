"""Exige leitura nativa de criação e após reabertura para aceitar a gravação."""
import hashlib
import json
import math
import shutil
from datetime import datetime
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R155-Revit-17-NAO-EXECUTAR')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def validate(row):
    if row['TotalRisers']!=17 or [r['Risers'] for r in row['Runs']]!=[9,8] or len(row['Landings'])!=1:
        raise ValueError('Contagem incorreta')
    for key,value in [('BaseM',.22),('TopM',3.25),('RiserM',3.03/17),('TreadM',.28)]:
        x=row[key]
        if not isinstance(x,(int,float)) or not math.isfinite(x) or abs(x-value)>1e-6:raise ValueError('Dimensão incorreta:'+key)
    if abs(row['Landings'][0]['FinishedM']-(.22+9*3.03/17))>1e-6:raise ValueError('Patamar incorreto')
    if row['StructuralApproval'] or row['SupportAndGuardDesignCompleted']:raise ValueError('Aprovação indevida')
    return row

def main():
    target=OUT/'R155-resultado.json'
    if target.exists():raise FileExistsError(target)
    prep=json.loads((OUT/'R155-preparacao.json').read_text(encoding='utf-8'))
    created=json.loads((OUT/'R155-criacao-nativa.json').read_text(encoding='utf-8'));a=validate(created['Readback'])
    rereads=sorted(OUT.glob('R155-releitura-nativa-*.json'))
    if not rereads:raise ValueError('Sem releitura nativa após reabrir')
    b=validate(json.loads(rereads[-1].read_text(encoding='utf-8')))
    closed=json.loads((OUT/'Revit-fechado-para-reabrir.json').read_text(encoding='utf-8'))
    reopened=json.loads((OUT/'Revit-reaberto-observado.json').read_text(encoding='utf-8'))
    parse=lambda value:datetime.fromisoformat(value.replace('Z','+00:00'))
    assert parse(created['EndedUtc'])<parse(closed['utc'])<parse(reopened['utc']),'Cronologia de fechamento/reabertura inválida'
    assert closed['mono']<reopened['mono'],'Relógio monotônico de fechamento/reabertura inválido'
    assert a==b,'Releitura difere da criação; revisar'
    assert a['ProtectedGeometryHash']==created['BeforeProtectedHash']
    assert sha(Path(prep['sourcePath']))==prep['sourceSha256']
    assert sha(Path(prep['planPath']))==prep['planSha256']
    result=dict(revision='H03/R155',nativeCreatedSavedReopenedReadbackMatched=True,
        readback=a,protectedGeometryHashUnchanged=True,originalR93Preserved=True,
        sourcePath=prep['sourcePath'],sourceSha256=prep['sourceSha256'],
        copyPath=prep['copyPath'],copySha256After=sha(Path(prep['copyPath'])),
        warningsAndErrors=created['WarningsAndErrors'],stairIntegratedInCalculationModel=False,
        structuralDepthM=.14,structuralDepthIsHypothesis=True,structuralApproval=False,
        commandMs=created['CommandMs'],commandTimeIsNotFlowTime=True,
        rereadSource=rereads[-1].name,visualStairInspectionCompleted=False,
        visualPendingReason='Vista herdou disciplina Estrutural; lista fecha durante automacao; alteracao para Coordenacao pendente',
        supportingClosedObservation=closed,supportingReopenedObservation=reopened)
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');archive()
    print(json.dumps(dict(nativeReadbackMatched=True,originalR93Preserved=True,warnings=len(created['WarningsAndErrors']))))

def archive():
    for p in OUT.iterdir():
        if p.is_file() and p.suffix.lower() in {'.json','.jpg','.png','.addin','.md'} and 'manifesto' not in p.name and p.name!='LEIA-ME-R155.md':shutil.copyfile(p,HERE/p.name)
    if (HERE/'LEIA-ME-R155.md').exists():shutil.copyfile(HERE/'LEIA-ME-R155.md',OUT/'LEIA-ME-R155.md')
    (HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    manifest=[dict(path=p.name,sha256=sha(p)) for p in sorted(HERE.iterdir()) if p.is_file() and 'manifesto' not in p.name]
    for folder in (HERE,OUT):(folder/'R155-manifesto.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

if __name__=='__main__':main()

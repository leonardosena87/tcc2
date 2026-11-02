"""Sensibilidade L3/W20: evidência de exportação, sem aprovação estrutural."""
import importlib.util
import json
import shutil
import zipfile
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Grelha-W20-H03-R137-SENSIBILIDADE-NAO-EXECUTAR')
spec=importlib.util.spec_from_file_location('r136',HERE.parent/'h03-r136/auditar.py')
r136=importlib.util.module_from_spec(spec)
spec.loader.exec_module(r136)
sha=r136.sha

def time_check(session,process):
    stamps=[session['inicio_utc'],process['inicio_utc'],process['fim_primeira_observacao_utc'],session['fim_utc']]
    dates=[datetime.fromisoformat(v.replace('Z','+00:00')) for v in stamps]
    if not dates[0]<=dates[1]<dates[2]<=dates[3]:raise ValueError('Processamento fora da sessão')
    for row,a,b in [(session,dates[0],dates[3]),(process,dates[1],dates[2])]:
        if abs(row['duracao_ms']-(b-a).total_seconds()*1000)>0.01:raise ValueError('Duração inconsistente')

def validate_fine(before,after):
    changes={k:r136.compare(before[k]['data'],after[k]['data']) for k in before}
    if changes['N2']['changedTables']:raise ValueError('N2 alterado')
    if not changes['portico']['sameJointIdsCoordinates'] or not changes['portico']['sameFrameIdsOrderedEndpoints']:
        raise ValueError('Geometria ordenada do pórtico alterada')
    if changes['N1']['jointCounts'][1]<=changes['N1']['jointCounts'][0]:raise ValueError('Malha não refinada')
    rows=r136.r132.nodal(after['N1']['data'])
    result=r136.resultant(rows)
    # Não exigir coincidência do centro como condição para registrar o ensaio.
    # Um resultado divergente também é resultado e deve permanecer visível.
    return changes,rows,result

def main():
    target=OUT/'R137-resultado.json'
    if target.exists():raise FileExistsError(target)
    prep=json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected=[]
    for row in prep['files']:
        if sha(Path(row['source']))!=row['sha256Before']:raise ValueError('Fonte R136 alterada')
        protected.append({'path':row['source'],'sha256':row['sha256Before']})
    historic=json.loads((HERE.parent/'h03-r136/R136-resultado.json').read_text(encoding='utf-8'))
    branches={}
    for branch in ['CAD','BIM']:
        coarse=r136.models(HERE.parent/'h03-r136'/f'SAP-{branch}')
        fine=r136.models(OUT/f'SAP-{branch}')
        for k,row in coarse.items():
            if row['sha256']!=historic['branches'][branch]['wallExports'][k]['sha256']:raise ValueError('Exportação R136 alterada')
        comparisons,loads,result=validate_fine(coarse,fine)
        session=json.loads((OUT/f'{branch}-sessao-tempo.json').read_text(encoding='utf-8'))
        process=json.loads((OUT/f'{branch}-processamento-tempo.json').read_text(encoding='utf-8'))
        time_check(session,process)
        text=(OUT/f'{branch}-reaberto-grelha-UI.txt').read_text(encoding='utf-8')
        for field in ['Espaçamento X Value: 10','Espaçamento Y Value: 10','Ângulo Value: 0']:
            if field not in text:raise ValueError('Conferência nativa ausente: '+field)
        prj=Path(next(r['copy'] for r in prep['files'] if r['branch']==branch and r['copy'].endswith('.prj')))
        if sha(prj)==next(r['sha256Before'] for r in prep['files'] if r['copy']==str(prj)):raise ValueError('PRJ não mudou')
        with zipfile.ZipFile(prj) as z:
            if z.testzip():raise ValueError('PRJ inválido')
        source=prj.parent.parent
        frozen=OUT/'congelados-apos-processamento'/branch
        if frozen.exists():raise FileExistsError(frozen)
        shutil.copytree(source,frozen)
        files=[{'path':p.relative_to(source).as_posix(),'sha256':sha(p)} for p in sorted(source.rglob('*')) if p.is_file()]
        if not all(sha(frozen/r['path'])==r['sha256'] for r in files):raise ValueError('Congelamento divergente')
        branches[branch]={'projectPath':str(prj),'projectSha256':sha(prj),'frozenFiles':files,
            'coarseExports':{k:{t:v[t] for t in ['path','sha256']} for k,v in coarse.items()},
            'fineExports':{k:{t:v[t] for t in ['path','sha256']} for k,v in fine.items()},
            'modelComparisonsToOwnR136':{k:{**c,'changedTables':{n:{side+'Count':len(rows) for side,rows in delta.items()} for n,delta in c['changedTables'].items()}} for k,c in comparisons.items()},
            'nodalG2N1':loads,'resultantN1':result,
            'coarseResultantR136':historic['branches'][branch]['resultantN1'],
            'session':session,'processingObservation':process}
    paired=branches['CAD']['nodalG2N1']==branches['BIM']['nodalG2N1']
    if not paired:raise ValueError('Distribuição nodal pareada divergente')
    data={'revision':'H03/R137','createdAtUtc':datetime.now(timezone.utc).isoformat(),
        'scope':'Somente malha L3/N1 50x50 para individual 10x10 cm, ângulo 0; W20/S58 mantida.',
        'protectedR136Files':protected,'sourceFilesUnchanged':True,'branches':branches,
        'pairedNodalLoadsIncludingIdsEqual':paired,'gridReadbackAfterReopeningBothCopies':True,
        'forceAndOriginFirstMomentsEqualToNominalInWrittenN1Export':all(D(v)==0 for b in branches.values() for v in b['resultantN1']['originMomentDeltaKgfCm'].values()) and all(D(b['resultantN1']['signedForceDeltaKgf'])==0 for b in branches.values()),
        'fineMeshWithoutW20ControlPerformed':False,'isolatedPorticoIncrementDetermined':False,
        'localReactionsVerified':False,'meshConvergenceDemonstrated':False,'W20AcceptedAsFinal':False,
        'internalModelIdenticalToExportProven':False,'processingPerformed':True,
        'dimensioningPerformed':False,'slabDeflectionPerformed':False,'SAP2000Executed':False,
        'CADorBIMTransferDefectProven':False,'finalProductivityRankingAllowed':False,
        'monographEdited':False,'authorshipRVTorDWGEdited':False,'finalStructuralApproval':False,
        'nextStep':'Criar controles próprios sem W20 com L3 10x10/0 graus; comparar diferenças e transmissão ao pórtico antes de aceitar modelo local.'}
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'paired':paired,'protected':len(protected),'N1':branches['CAD']['resultantN1'],
        'nodes':branches['CAD']['modelComparisonsToOwnR136']['N1']['jointCounts']},ensure_ascii=False))

if __name__=='__main__':main()

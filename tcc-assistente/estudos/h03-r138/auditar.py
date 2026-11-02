"""Controle de mesma malha L3 para isolar W20; pórtico sob hipótese explícita de eixos."""
import importlib.util
import json
import shutil
import zipfile
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Controle-L3-H03-R138-SEM-W20-NAO-EXECUTAR')
spec=importlib.util.spec_from_file_location('r137',HERE.parent/'h03-r137/auditar.py')
r137=importlib.util.module_from_spec(spec)
spec.loader.exec_module(r137)
r136=r137.r136
sha=r136.sha

def isolated(control,wall):
    comparisons={k:r136.compare(control[k]['data'],wall[k]['data']) for k in control}
    for k,c in comparisons.items():
        if not c['sameJointIdsCoordinates'] or not c['sameFrameIdsOrderedEndpoints']:
            raise ValueError('Geometria ordenada divergente: '+k)
    if comparisons['N2']['changedTables']:raise ValueError('N2 mudou')
    if r136.r132.nodal(control['N1']['data']):raise ValueError('Controle contém G2 nodal')
    changes=comparisons['N1']['changedTables']
    if set(changes)!={'JOINT LOADS - FORCE'} or changes['JOINT LOADS - FORCE']['removed']:
        raise ValueError('N1 não é adição exclusiva de cargas nodais')
    rows=r136.r132.nodal(wall['N1']['data'])
    if len(rows)!=len(changes['JOINT LOADS - FORCE']['added']):raise ValueError('Outra ação mudou')
    result=r136.resultant(rows)
    portico=r136.r134.portico_increment(control['portico']['data'],wall['portico']['data'],comparisons['portico']['changedTables'])
    portico['differenceFromN1Forces']={'FzKgf':str(D(portico['signedTotals']['Fz'])-D(result['signedFzKgf'])),
        **{k+'KgfCm':str(D(portico['signedTotals'][k])-D(result['originMomentFromForcesKgfCm'][k])) for k in ['Mx','My']}}
    return comparisons,rows,result,portico

def main():
    target=OUT/'R138-resultado.json'
    if target.exists():raise FileExistsError(target)
    prep=json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected=[]
    for row in prep['files']:
        if sha(Path(row['source']))!=row['sha256Before']:raise ValueError('Fonte R116 alterada')
        protected.append({'path':row['source'],'sha256':row['sha256Before']})
    old=json.loads((HERE.parent/'h03-r137/R137-resultado.json').read_text(encoding='utf-8'))
    protected_wall=[]
    for branch,data in old['branches'].items():
        base=Path(data['projectPath']).parent.parent
        for row in data['frozenFiles']:
            if sha(base/row['path'])!=row['sha256']:raise ValueError('Cópia R137 alterada')
            protected_wall.append({'path':str(base/row['path']),'sha256':row['sha256']})
    branches={}
    for branch in ['CAD','BIM']:
        control=r136.models(OUT/f'SAP-{branch}')
        wall=r136.models(HERE.parent/'h03-r137'/f'SAP-{branch}')
        for k,row in wall.items():
            if row['sha256']!=old['branches'][branch]['fineExports'][k]['sha256']:raise ValueError('Exportação R137 alterada')
        comparisons,loads,result,portico=isolated(control,wall)
        text=(OUT/f'{branch}-reaberto-grelha-UI.txt').read_text(encoding='utf-8')
        for v in ['Espaçamento X Value: 10','Espaçamento Y Value: 10','Ângulo Value: 0']:
            if v not in text:raise ValueError('Releitura nativa ausente: '+v)
        session=json.loads((OUT/f'{branch}-sessao-tempo.json').read_text(encoding='utf-8'))
        process=json.loads((OUT/f'{branch}-processamento-tempo.json').read_text(encoding='utf-8'))
        r137.time_check(session,process)
        prj=Path(next(r['copy'] for r in prep['files'] if r['branch']==branch and r['copy'].endswith('.prj')))
        with zipfile.ZipFile(prj) as z:
            if z.testzip():raise ValueError('PRJ inválido')
        source=prj.parent.parent
        frozen=OUT/'congelados-apos-processamento'/branch
        if frozen.exists():raise FileExistsError(frozen)
        shutil.copytree(source,frozen)
        files=[{'path':p.relative_to(source).as_posix(),'sha256':sha(p)} for p in sorted(source.rglob('*')) if p.is_file()]
        if not all(sha(frozen/r['path'])==r['sha256'] for r in files):raise ValueError('Congelamento divergente')
        branches[branch]={'projectPath':str(prj),'projectSha256':sha(prj),'frozenFiles':files,
            'controlExports':{k:{t:v[t] for t in ['path','sha256']} for k,v in control.items()},
            'wallExports':{k:{t:v[t] for t in ['path','sha256']} for k,v in wall.items()},
            'comparisons':{k:{**c,'changedTables':{n:{side+'Count':len(rows) for side,rows in delta.items()} for n,delta in c['changedTables'].items()}} for k,c in comparisons.items()},
            'addedNodalG2N1':loads,'resultantN1':result,'conditionalPorticoIncrement':portico,
            'session':session,'processingObservation':process}
    paired=branches['CAD']['addedNodalG2N1']==branches['BIM']['addedNodalG2N1']
    paired_portico=branches['CAD']['conditionalPorticoIncrement']==branches['BIM']['conditionalPorticoIncrement']
    if not paired or not paired_portico:raise ValueError('Incrementos pareados divergentes')
    data={'revision':'H03/R138','createdAtUtc':datetime.now(timezone.utc).isoformat(),
        'scope':'Controles L3/N1 10x10 cm/0 graus sem W20, comparados com R137 com W20/S58.',
        'protectedR116Files':protected,'protectedR137Files':protected_wall,'sourceFilesUnchanged':True,
        'branches':branches,'pairedNodalLoadsIncludingIdsEqual':paired,'pairedConditionalPorticoIncrementsEqual':paired_portico,
        'fineMeshWithoutW20ControlPerformed':True,'sameOrderedGeometryConfirmed':True,
        'forceAndFirstMomentsRetainedInN1WrittenExport':all(D(v)==0 for b in branches.values() for v in b['resultantN1']['originMomentDeltaKgfCm'].values()),
        'porticoFirstMomentsExactlyEqualToN1UnderConditionalInterpretation':all(D(v)==0 for b in branches.values() for k,v in b['conditionalPorticoIncrement']['differenceFromN1Forces'].items() if k!='FzKgf'),
        'localSupportReactionsVerified':False,'meshConvergenceDemonstrated':False,'W20AcceptedAsFinal':False,
        'SAP2000Executed':False,'internalAxesProvenEquivalentToSAPDefault':False,
        'processingPerformed':True,'dimensioningPerformed':False,'slabDeflectionPerformed':False,
        'finalStructuralApproval':False,'CADorBIMTransferDefectProven':False,
        'finalProductivityRankingAllowed':False,'monographEdited':False,'authorshipRVTorDWGEdited':False,
        'axisReferences':json.loads((HERE.parent/'h03-r134/R134-resultado.json').read_text(encoding='utf-8'))['axisReferences'],
        'nextStep':'Examinar momentos/transmissão local e rigidez de apoios, mantendo carga nominal; não compensar valor nem deslocar linha para forçar coincidência.'}
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'pairedNodal':paired,'pairedPorticoConditional':paired_portico,'protected':[len(protected),len(protected_wall)],
        'resultant':branches['CAD']['resultantN1'],'portico':branches['CAD']['conditionalPorticoIncrement']},ensure_ascii=False))

if __name__=='__main__':main()

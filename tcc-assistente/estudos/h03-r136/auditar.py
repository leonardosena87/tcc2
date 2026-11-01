"""Incremento isolado W20 em exportações nativas; sem executar SAP2000."""
import importlib.util
import json
import shutil
import zipfile
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Analise-W20-H03-R136-ESTUDO-NAO-EXECUTAR')

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    value=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

r132=module('r132audit',HERE.parent/'h03-r132/auditar.py')
r134=module('r134audit',HERE.parent/'h03-r134/auditar.py')
sha=r132.sha

def models(folder):
    files=sorted(folder.glob('*.$2k'))
    if len(files)!=3:raise ValueError('Exportação incompleta')
    data={}
    for p in files:
        kind='N1' if p.stem.endswith('N1') else 'N2' if p.stem.endswith('N2') else 'portico'
        if kind in data:raise ValueError('Modelo duplicado')
        data[kind]={'path':str(p),'sha256':sha(p),'data':r132.r122.parse(p.read_text(encoding='cp1252'))}
    return data

def compare(a,b):
    return {'sameJointIdsCoordinates':a['joints']==b['joints'],
        'sameFrameIdsOrderedEndpoints':a['frames']==b['frames'],
        'jointCounts':[len(a['joints']),len(b['joints'])],
        'frameCounts':[len(a['frames']),len(b['frames'])],
        'changedTables':r134.differences(a,b)}

def resultant(rows,expected_force=D('-1742.9405'),center=(D(810),D(195))):
    force=sum((D(r['forceKgf'][2]) for r in rows),D(0))
    # Cada F3 foi escrito com quatro casas. O limite descreve a incerteza
    # possível da escrita arredondada, não tolerância física nem prova da causa.
    if any(D(r['forceKgf'][2]).as_tuple().exponent!=-4 for r in rows):
        raise ValueError('Precisão de F3 inesperada')
    rounding_bound=D(len(rows))*D('0.00005')
    if not force or abs(force-expected_force)>rounding_bound:
        raise ValueError('Integral incompatível com precisão da escrita sob convenção R125')
    x=sum(D(r['xyzCm'][0])*D(r['forceKgf'][2]) for r in rows)/force
    y=sum(D(r['xyzCm'][1])*D(r['forceKgf'][2]) for r in rows)/force
    mx=sum(D(r['xyzCm'][1])*D(r['forceKgf'][2]) for r in rows)
    my=sum(-D(r['xyzCm'][0])*D(r['forceKgf'][2]) for r in rows)
    dx,dy=x-center[0],y-center[1]
    return {'signedFzKgf':str(force),'nominalSignedFzUnderR125Kgf':str(expected_force),
        'signedForceDeltaKgf':str(force-expected_force),
        'possibleRoundingBoundKgf':str(rounding_bound),
        'forceExactlyEqualToNominal':force==expected_force,
        'compatibleWithFourDecimalExport':True,'roundingProvenAsCause':False,
        'centroidXYCm':[str(x),str(y)],
        'idealCentroidXYCm':[str(v) for v in center],'centroidDeltaXYCm':[str(dx),str(dy)],
        'centroidDistanceCm':str((dx*dx+dy*dy).sqrt()),
        'originMomentFromForcesKgfCm':{'Mx':str(mx),'My':str(my)},
        'idealOriginMomentKgfCm':{'Mx':str(center[1]*expected_force),'My':str(-center[0]*expected_force)},
        'originMomentDeltaKgfCm':{'Mx':str(mx-center[1]*expected_force),'My':str(my+center[0]*expected_force)}}

def main():
    target=OUT/'R136-resultado.json'
    if target.exists():raise FileExistsError(target)
    prep=json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected=[]
    for row in prep['files']:
        if sha(Path(row['source']))!=row['sha256Before']:raise ValueError('Fonte R135 alterada')
        protected.append({'path':row['source'],'sha256':row['sha256Before']})
    old=json.loads((HERE.parent/'h03-r132/R132-resultado.json').read_text(encoding='utf-8'))
    branches={}
    for b in ['CAD','BIM']:
        control=models(HERE.parent/'h03-r132'/f'SAP-{b}-BASE')
        wall=models(OUT/f'SAP-{b}')
        for name,row in control.items():
            historic=next(r for r in old['exports'] if r['branch']==b and r['state']=='BASE' and r['model']==name)
            if row['sha256']!=historic['sha256']:raise ValueError('Exportação controle R132 alterada')
        comparisons={name:compare(control[name]['data'],wall[name]['data']) for name in wall}
        for name,c in comparisons.items():
            if not c['sameJointIdsCoordinates'] or not c['sameFrameIdsOrderedEndpoints']:
                raise ValueError('Malha mudou: '+b+'/'+name)
        n1=comparisons['N1']['changedTables']
        if set(n1)!={'JOINT LOADS - FORCE'} or n1['JOINT LOADS - FORCE']['removed']:
            raise ValueError('Mudança N1 não é apenas adição nodal')
        if comparisons['N2']['changedTables']:raise ValueError('N2 mudou')
        if r132.nodal(control['N1']['data']):raise ValueError('Controle com G2 nodal')
        loads=r132.nodal(wall['N1']['data'])
        if len(loads)!=len(n1['JOINT LOADS - FORCE']['added']):raise ValueError('Mudança fora de G2')
        result=resultant(loads)
        portico=r134.portico_increment(control['portico']['data'],wall['portico']['data'],comparisons['portico']['changedTables'])
        portico['differenceFromN1Forces']={
            'FzKgf':str(D(portico['signedTotals']['Fz'])-D(result['signedFzKgf'])),
            **{k+'KgfCm':str(D(portico['signedTotals'][k])-D(result['originMomentFromForcesKgfCm'][k])) for k in ['Mx','My']}}
        prj=Path(next(r['copy'] for r in prep['files'] if r['branch']==b and r['copy'].endswith('.prj')))
        with zipfile.ZipFile(prj) as archive:
            if archive.testzip():raise ValueError('PRJ inválido')
        source=prj.parent.parent
        frozen=OUT/'congelados-apos-processamento'/b
        if frozen.exists():raise FileExistsError(frozen)
        shutil.copytree(source,frozen)
        files=[{'path':p.relative_to(source).as_posix(),'sha256':sha(p)} for p in sorted(source.rglob('*')) if p.is_file()]
        if not all(sha(frozen/r['path'])==r['sha256'] for r in files):raise ValueError('Congelamento divergente')
        session=json.loads((OUT/f'{b}-sessao-tempo.json').read_text(encoding='utf-8'))
        process=json.loads((OUT/f'{b}-processamento-tempo.json').read_text(encoding='utf-8'))
        if not session['inicio_utc']<=process['inicio_utc']<=process['fim_primeira_observacao_utc']<=session['fim_utc']:
            raise ValueError('Tempos fora da sessão')
        branches[b]={'projectPath':str(prj),'projectSha256':sha(prj),'frozenFiles':files,
            'controlExports':{k:{t:v[t] for t in ['path','sha256']} for k,v in control.items()},
            'wallExports':{k:{t:v[t] for t in ['path','sha256']} for k,v in wall.items()},
            'comparisons':comparisons,'addedNodalG2N1':loads,'resultantN1':result,
            'conditionalPorticoIncrement':portico,'session':session,'processingObservation':process}
    paired=branches['CAD']['addedNodalG2N1']==branches['BIM']['addedNodalG2N1']
    if not paired:raise ValueError('Distribuição pareada diferente')
    data={'revision':'H03/R136','createdAtUtc':datetime.now(timezone.utc).isoformat(),
        'scope':'Análise isolada W20/S58 na malha original; controles próprios R116 exportados na R132.',
        'protectedR135Files':protected,'sourceFilesUnchanged':True,'branches':branches,
        'pairedNodalLoadsIncludingIdsEqual':paired,'processingPerformed':True,
        'dimensioningPerformed':False,'slabDeflectionPerformed':False,'SAP2000Executed':False,
        'forceIntegralCompatibleWithExportPrecisionUnderR125Convention':True,
        'firstMomentsRetained':all(D(v)==0 for v in branches['CAD']['resultantN1']['originMomentDeltaKgfCm'].values()),
        'localSupportReactionsVerified':False,'meshConvergenceDemonstrated':False,
        'W20AcceptedAsFinal':False,'finalStructuralApproval':False,'finalProductivityRankingAllowed':False,
        'CADorBIMTransferDefectProven':False,'monographEdited':False,'authorshipRVTorDWGEdited':False,
        'warnings':'Ambos processados com avisos; resumo visual e limites da sua precisão documentados no relatório.',
        'axisAssumptionReferences':json.loads((HERE.parent/'h03-r134/R134-resultado.json').read_text(encoding='utf-8'))['axisReferences']}
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'paired':paired,'protected':len(protected),
        'resultant':branches['CAD']['resultantN1'],
        'changes':{b:{k:{t:{s:len(v[s]) for s in ['added','removed']} for t,v in c['changedTables'].items()} for k,c in r['comparisons'].items()} for b,r in branches.items()}},ensure_ascii=False))

if __name__=='__main__':main()

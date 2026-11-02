"""Ensaio nativo W05: dados de parede e faixa distribuída exportada, sem SAP."""
import hashlib
import importlib.util
import json
import re
import shutil
import zipfile
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Paredes-Vigas-H03-R143-NAO-EXECUTAR')
spec = importlib.util.spec_from_file_location('r122', HERE.parent/'h03-r122/consolidar.py')
r122 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r122)


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def number(s): return D(s.replace(',', '.'))


def distributed(model):
    rows = [r for r in model['tables']['FRAME LOADS - DISTRIBUTED'] if r['LoadPat']=='G2']
    if len(rows)!=1: raise ValueError('Ensaio não contém uma única carga G2 distribuída')
    r=rows[0]
    if (r['CoordSys'],r['Type'],r['Dir'],r['DistType'])!=('LOCAL','Force','2','RelDist'):
        raise ValueError('Convenção de carga diferente')
    a,b=model['frames'][r['Frame']]
    if (a,b)!=((965.,3.,320.),(965.,387.,320.)):
        raise ValueError('Extremos ordenados da barra diferentes')
    ra,rb,qa,qb=[number(r[k]) for k in ['RelDistA','RelDistB','FOverLA','FOverLB']]
    if not D(0)<=ra<rb<=D(1): raise ValueError('Intervalo relativo inválido')
    length=D(str(b[1]))-D(str(a[1]))
    start=D(str(a[1]))+ra*length
    end=D(str(a[1]))+rb*length
    integral=(qa+qb)/2*(end-start)
    return {'raw':r,'frameEndpointsCm':[a,b], 'loadedYStartEndCm':[str(start),str(end)],
            'loadedLengthCm':str(end-start),'signedIntegralLocal2Kgf':str(integral),
            'physicalFreeYStartEndCm':['15','375'],'physicalFreeLengthCm':'360',
            'matchesPhysicalFreeInterval':start==D(15) and end==D(375),
            'overrunAtEachEndCm':[str(D(15)-start),str(end-D(375))],
            'notTotalGlobalActionOrSupportReactions':True}


def changed_tables(a,b):
    enc=lambda r:json.dumps(r,sort_keys=True)
    result={}
    for k in sorted(set(a['tables'])|set(b['tables'])):
        ca,cb=[Counter(map(enc,x['tables'].get(k,[]))) for x in [a,b]]
        removed=[json.loads(r) for r in (ca-cb).elements()]
        added=[json.loads(r) for r in (cb-ca).elements()]
        if removed or added:result[k]={'removed':removed,'added':added}
    return result


def main():
    target=OUT/'R143-resultado.json'
    if target.exists():raise FileExistsError(target)
    prep=json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected=[]
    for r in prep['files']:
        if sha(Path(r['source']))!=r['sha256Before']:raise ValueError('Fonte R116 alterada')
        if r['branch']=='BIM':
            if Path(r['copy']).name=='EdificacaoEberick.ini':
                bimprj=next(x['copy'] for x in prep['files'] if x['branch']=='BIM' and x['copy'].endswith('.prj'))
                expected=re.sub(r'(?m)^Arquivo=.*$',lambda _: 'Arquivo='+bimprj+'\r',Path(r['source']).read_bytes().decode('cp1252')).encode('cp1252')
                if Path(r['copy']).read_bytes()!=expected:raise ValueError('INI BIM alterado além do ponteiro')
            elif sha(Path(r['copy']))!=r['sha256Before']:
                raise ValueError('Cópia BIM mudou sem ensaio')
        protected.append({'path':r['source'],'sha256':r['sha256Before']})
    prj=Path(next(r['copy'] for r in prep['files'] if r['branch']=='CAD' and r['copy'].endswith('.prj')))
    saved=json.loads((OUT/'CAD-prj-antes-releitura.json').read_text(encoding='utf-8'))
    end=json.loads((OUT/'CAD-sessao-fim.json').read_text(encoding='utf-8'))
    if sha(prj)!=saved['sha256'] or not end['retomadaSemAlterarPrj']:raise ValueError('PRJ mudou na releitura')
    with zipfile.ZipFile(prj) as z:
        if z.testzip():raise ValueError('PRJ inválido')
    wall=(OUT/'CAD-W05-parede-reaberta-UI.txt').read_text(encoding='utf-8')
    for value in ['68-H03-R143-CAD','Altura Value: 285','Espessura Value: 15','Peso Value: 10.4333','Carga Value: 4.46']:
        if value not in wall:raise ValueError('Releitura ausente: '+value)
    before=(OUT/'CAD-V8-dados-sem-carga-UI.txt').read_text(encoding='utf-8')
    after=(OUT/'CAD-V8-reaberto-UI.txt').read_text(encoding='utf-8')
    for value in ['Nome Value: V8','bw Value: 20','h Value: 40','/ Value: 0','Carga extra Value: 0']:
        if value not in before or value not in after:raise ValueError('Seção/extra alterado: '+value)
    exports={}
    for file in sorted((OUT/'SAP-CAD').glob('*.$2k')):
        kind='portico' if file.name.startswith('portico') else 'N1' if '_N1.' in file.name else 'N2'
        if kind in exports:raise ValueError('Exportação ambígua')
        exports[kind]={'path':str(file),'sha256':sha(file),'data':r122.parse(file.read_text(encoding='cp1252'))}
    if set(exports)!={'portico','N1','N2'}:raise ValueError('Exportação incompleta')
    diagnostic=distributed(exports['portico']['data'])
    control_root=HERE.parent/'h03-r132/SAP-CAD-BASE'
    comparisons={}
    for kind,item in exports.items():
        cf=next(p for p in control_root.glob('*.$2k') if ('portico' if p.name.startswith('portico') else 'N1' if '_N1.' in p.name else 'N2')==kind)
        control=r122.parse(cf.read_text(encoding='cp1252'))
        if control['joints']!=item['data']['joints'] or control['frames']!=item['data']['frames']:
            raise ValueError('Geometria difere do controle R116/R132: '+kind)
        comparisons[kind]={'controlPath':str(cf),'controlSha256':sha(cf),
            'orderedGeometryEqual':True,'changedTables':changed_tables(control,item['data'])}
    start=json.loads((OUT/'CAD-sessao-inicio.json').read_text(encoding='utf-8'))
    elapsed=(datetime.fromisoformat(end['fim_utc'].replace('Z','+00:00'))-datetime.fromisoformat(start['inicio_utc'].replace('Z','+00:00'))).total_seconds()
    if elapsed<=0:raise ValueError('Intervalo temporal inválido')
    frozen=OUT/'congelado-CAD'
    if frozen.exists():raise FileExistsError(frozen)
    source=prj.parent.parent
    shutil.copytree(source,frozen)
    freeze=[{'path':p.relative_to(source).as_posix(),'sha256':sha(p)} for p in sorted(source.rglob('*')) if p.is_file()]
    if any(sha(frozen/r['path'])!=r['sha256'] for r in freeze):raise ValueError('Congelamento divergente')
    result={'revision':'H03/R143','createdAtUtc':datetime.now(timezone.utc).isoformat(),
        'scope':'Ensaio CAD de parede nativa W05/V8; não aceito como lançamento físico definitivo.',
        'projectPath':str(prj),'projectSha256':sha(prj),'prjUnchangedOnReadback':True,
        'sourceR116FilesPreserved':protected,'frozenCadFiles':freeze,
        'BIMCopyPreparedButNotOpenedOrTested':True,'BIMTimingOrEqualityNotAsserted':True,
        'nodeAttempt':{'typedCoordinatesCm':[965,15],'nativeMessage':'Já existe um nó nesta posição no pavimento.',
            'newNodeNotConfirmed':True,'snapStateNotProvedByToggle':True,'causeNotIdentified':True},
        'nativeWall':{'heightCm':'285','finishedThicknessCm':'15','typedEquivalentWeightKNm3':'10.433333333',
            'reopenedWeightDisplayedKNm3':'10.4333','displayedLineLoadKNm':'4.46','extraDisplayedKNm':'0',
            'nominalCompositionWeightKNm2':'1.565','nominalQKNm':'4.46025',
            'compositionIsStudyHypothesisNotManufacturerSpecification':True,'sectionCm':[20,40],'elevationCm':0},
        'distributedExportDiagnostic':diagnostic,'controlComparison':comparisons,
        'exports':{k:{a:v[a] for a in ['path','sha256']} for k,v in exports.items()},
        'time':{'startUtc':start['inicio_utc'],'endUtc':end['fim_utc'],'elapsedWallSeconds':elapsed,
            'minutes':elapsed/60,'scope':end['inclui'],'humanIntervention':False,
            'includesResearchToolLatencyAndReadback':True,'notPureAiInferenceOrSolverTime':True,
            'processingIntervalNested':True,'finalFlowTotal':None,'rankingAllowed':False},
        'processing':json.loads((OUT/'CAD-processamento-tempo.json').read_text(encoding='utf-8')),
        'fullELUELSPerformed':False,'finalWallAccepted':False,'structuralApproval':False,
        'monographOrAuthoringRvtDwgChanged':False,
        'technicalSources':['https://suporte.altoqi.com.br/hc/pt-br/articles/360058309854',
            'https://suporte.altoqi.com.br/hc/pt-br/articles/360046158854'],
        'next':'Não repetir a mesma tentativa junto ao pilar nem estender esta representação às demais paredes; resolver a faixa carregada antes da incorporação final. Avançar em paralelo nas outras frentes independentes sem declarar cargas/ELU/ELS completos.'}
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'protectedFiles':len(protected),'timeMinutes':elapsed/60,'diagnostic':diagnostic,
        'changes':{k:{t:{c:len(rows) for c,rows in v.items()} for t,v in x['changedTables'].items()} for k,x in comparisons.items()}}))

if __name__=='__main__':main()

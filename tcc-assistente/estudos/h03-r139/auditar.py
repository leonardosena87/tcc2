"""Consulta sem editar PRJ; inventário de vínculos, não solução de reações."""
import importlib.util
import json
import re
from collections import Counter
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Diagnostico-Transmissao-H03-R139-CONSULTA-NAO-EXECUTAR')
spec=importlib.util.spec_from_file_location('r138',HERE.parent/'h03-r138/auditar.py')
r138=importlib.util.module_from_spec(spec)
spec.loader.exec_module(r138)
r136=r138.r136
sha=r136.sha

def inventory(model):
    tables=model['tables']
    springs=[]
    for row in tables.get('JOINT SPRING ASSIGNMENTS 1 - UNCOUPLED',[]):
        if row['CoordSys']!='GLOBAL':raise ValueError('Mola em eixo não global exige transformação')
        if row['Joint'] not in model['joints']:raise ValueError('Mola sem nó')
        springs.append({'joint':row['Joint'],'xyzCm':model['joints'][row['Joint']],
            'rawStiffness':{k:row[k] for k in ['U1','U2','U3','R1','R2','R3']},
            'nonzeroComponents':[k for k in ['U1','U2','U3','R1','R2','R3'] if D(row[k].replace(',','.'))!=0]})
    restraints=tables.get('JOINT RESTRAINT ASSIGNMENTS',[])
    counts=Counter(tuple(sorted((k,v) for k,v in r.items() if k!='Joint')) for r in restraints)
    restraint_ids={r['Joint'] for r in restraints}
    return {'jointCount':len(model['joints']),'springRows':springs,'springCount':len(springs),
        'restraintRows':len(restraints),'restraintPatterns':[{'values':dict(k),'count':v} for k,v in counts.items()],
        'jointIdsWithoutExplicitRestraintRow':sorted(set(model['joints'])-restraint_ids,key=int),
        'partialFixityRows':tables.get('FRAME RELEASE ASSIGNMENTS 2 - PARTIAL FIXITY',[]),
        'generalReleaseCount':len(tables.get('FRAME RELEASE ASSIGNMENTS 1 - GENERAL',[])),
        'offsetOrInsertionTablesPresent':[k for k in tables if 'OFFSET' in k or 'INSERT' in k],
        'reactionResultTablesPresent':[k for k in tables if 'REACTION' in k],
        'programControl':tables['PROGRAM CONTROL']}

def fields(text):
    return dict(re.findall(r'editar .*?\) (.*?) Value: (.*?) ID:',text))

def main():
    target=OUT/'R139-resultado.json'
    if target.exists():raise FileExistsError(target)
    prep=json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected=[];copies=[]
    for row in prep['files']:
        if sha(Path(row['source']))!=row['sha256Before']:raise ValueError('Fonte R137 alterada')
        protected.append({'path':row['source'],'sha256':row['sha256Before']})
        if row['copy'].endswith('.prj'):
            if sha(Path(row['copy']))!=row['sha256Before']:raise ValueError('PRJ da consulta alterado')
            copies.append({'branch':row['branch'],'path':row['copy'],'sha256':row['sha256Before'],'unchanged':True})
    old137=json.loads((HERE.parent/'h03-r137/R137-resultado.json').read_text(encoding='utf-8'))
    old138=json.loads((HERE.parent/'h03-r138/R138-resultado.json').read_text(encoding='utf-8'))
    branches={}
    for branch in ['CAD','BIM']:
        wall=r136.models(HERE.parent/'h03-r137'/f'SAP-{branch}')
        control=r136.models(HERE.parent/'h03-r138'/f'SAP-{branch}')
        for kind in wall:
            if wall[kind]['sha256']!=old137['branches'][branch]['fineExports'][kind]['sha256']:raise ValueError('Arquivo R137 alterado')
            if control[kind]['sha256']!=old138['branches'][branch]['controlExports'][kind]['sha256']:raise ValueError('Arquivo R138 alterado')
        i=inventory(wall['N1']['data']);j=inventory(control['N1']['data'])
        if i!=j:raise ValueError('Vínculos diferentes no controle')
        configurations={}
        for kind in ['analise-configurada','paineis-configurados','analise-avancada']:
            configurations[kind]=fields((OUT/f'{branch}-{kind}-UI.txt').read_text(encoding='utf-8'))
        diff=r136.compare(control['portico']['data'],wall['portico']['data'])['changedTables']['JOINT LOADS - FORCE']
        session=json.loads((OUT/f'{branch}-sessao-tempo.json').read_text(encoding='utf-8'))
        branches[branch]={'N1SupportInventory':i,'nativeNumericFields':configurations,'porticoG2JointDifferences':diff,
            'session':session,'tablesRead':{state:{k:{'path':v['path'],'sha256':v['sha256']} for k,v in data.items()} for state,data in [('R137',wall),('R138',control)]}}
    if branches['CAD']['N1SupportInventory']!=branches['BIM']['N1SupportInventory']:raise ValueError('Inventário pareado diferente')
    if branches['CAD']['nativeNumericFields']!=branches['BIM']['nativeNumericFields']:raise ValueError('Campos numéricos pareados diferentes')
    visual={'method':'Transcrição visual das capturas, pois a árvore informa radios/checkboxes sem estado marcado confiável.',
        'bothBranches':{'process':'Grelhas + pórtico espacial','PDeltaChecked':True,'flexibleBeamColumnConnectionChecked':True,
            'autoSaveAfterProcessingChecked':False,'panelDimensioningModel':'Completo','globalSolidSlabSpacingCm':'50',
            'L3IndividualSpacingSource':'R137/R138:10x10 cm/0 graus, conferido após reabertura',
            'grillageTorsionReductionPercent':'40','numericalEstimatedMaximumErrorPercent':'2',
            'numericalMinimumAbsoluteValueRaw':'200','numericalAbsoluteValueUnitShown':False,
            'treatNumericalSettingsAsStructuralAcceptanceTolerance':False}}
    d={'revision':'H03/R139','createdAtUtc':datetime.now(timezone.utc).isoformat(),'protectedR137Files':protected,
        'copyPRJs':copies,'sourceFilesUnchanged':True,'consultedPRJsUnchanged':True,'branches':branches,
        'pairedNativeNumericFieldsEqual':True,'pairedN1SupportInventoryEqual':True,'visualObservations':visual,
        'concreteCauseOfMomentResidualProven':False,'springRotationsOrReactionsCalculated':False,
        'offsetAbsenceInInternalEberickModelProven':False,'missingRestraintRowsClassifiedAsDefect':False,
        'analysisProcessChanged':False,'processingPerformed':False,'newSAPExportsMade':False,'SAP2000Executed':False,
        'W20AcceptedAsFinal':False,'finalStructuralApproval':False,'finalProductivityRankingAllowed':False,
        'monographEdited':False,'authorshipRVTorDWGEdited':False,
        'primaryReferences':[{'url':'https://suporte.altoqi.com.br/hc/pt-br/articles/360001391833','use':'Diferença entre grelha separada e modelo integrado; não prova causa deste caso.'},
            {'url':'https://suporte.altoqi.com.br/hc/pt-br/articles/360002163594','use':'Graus de liberdade e formulação; não valida a estrutura estudada.'},
            {'url':'https://suporte.altoqi.com.br/hc/pt-br/articles/360000302893','use':'Possibilidade de offsets/vinculação semirrígida; não prova sua participação no resíduo.'}],
        'nextStep':'Obter rotações/reações G2 das grelhas com e sem W20, incluindo momentos nos vínculos, antes de atribuir a causa ou alterar o processo.'}
    target.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'PRJsUnchanged':len(copies),'protected':len(protected),'pairedFields':True,
        'springs':branches['CAD']['N1SupportInventory']['springCount'],
        'explicitRestraints':branches['CAD']['N1SupportInventory']['restraintRows'],
        'noRestraintRow':len(branches['CAD']['N1SupportInventory']['jointIdsWithoutExplicitRestraintRow'])}))

if __name__=='__main__':main()

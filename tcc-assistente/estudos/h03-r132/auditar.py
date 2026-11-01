"""Audita cargas nodais exportadas sem executar SAP2000 ou mudar o modelo."""
import importlib.util
import json
from collections import Counter
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Distribuicao-W15-H03-R132-CONSULTA-NAO-EXECUTAR')
spec=importlib.util.spec_from_file_location('r122',HERE.parent/'h03-r122/consolidar.py')
r122=importlib.util.module_from_spec(spec)
spec.loader.exec_module(r122)
sha=r122.sha
D=Decimal

def encode(row):return json.dumps(row,sort_keys=True,ensure_ascii=False)

def nodal(model):
    rows=[]
    for r in model['tables'].get('JOINT LOADS - FORCE',[]):
        if r['LoadPat']!='G2':continue
        if r['CoordSys']!='GLOBAL':raise ValueError('Carga não global')
        row={'jointId':r['Joint'],'xyzCm':[str(D(str(v))) for v in model['joints'][r['Joint']]],
             'forceKgf':[str(D(r[k].replace(',','.'))) for k in ['F1','F2','F3']],
             'momentKgfCm':[str(D(r[k].replace(',','.'))) for k in ['M1','M2','M3']]}
        if any(D(v)!=0 for v in row['forceKgf'][:2]+row['momentKgfCm']):
            raise ValueError('Há componente adicional; não resumir como força vertical pura')
        rows.append(row)
    return rows

def resultant(rows):
    f=sum((D(r['forceKgf'][2]) for r in rows),D(0))
    if f==0:raise ValueError('Resultante nula')
    x=sum(D(r['xyzCm'][0])*D(r['forceKgf'][2]) for r in rows)/f
    y=sum(D(r['xyzCm'][1])*D(r['forceKgf'][2]) for r in rows)/f
    expected=(D('497.5'),D(495))
    dx,dy=x-expected[0],y-expected[1]
    return {'signedFzKgf':str(f),'centroidXYCm':[str(x),str(y)],
      'expectedWallCentroidXYCm':[str(v) for v in expected],
      'centroidDeltaXYCm':[str(dx),str(dy)],'centroidDistanceCm':str((dx*dx+dy*dy).sqrt()),
      'originMomentFromNodalForcesKgfCm':{'Mx':str(y*f),'My':str(-x*f)},
      'originMomentForIdealUniformWallKgfCm':{'Mx':str(expected[1]*f),'My':str(-expected[0]*f)},
      'originMomentDifferenceKgfCm':{'Mx':str(dy*f),'My':str(-dx*f)}}

def main():
    if (OUT/'R132-resultado.json').exists():raise FileExistsError('Resultado existente')
    prep=json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected=[];copies=[]
    for row in prep['files']:
        digest=sha(Path(row['source']))
        if digest!=row['sha256Before']:raise ValueError('Fonte alterada')
        protected.append({'path':row['source'],'sha256':digest})
        if row['copy'].endswith('.prj'):
            if sha(Path(row['copy']))!=digest:raise ValueError('PRJ de consulta alterado')
            copies.append({'branch':row['branch'],'path':row['copy'],'sha256':digest})
    exports=[];branches={}
    for b in ['CAD','BIM']:
        models={}
        for state in ['BASE','W15']:
            folder=OUT/f'SAP-{b}-{state}'
            files=sorted(folder.glob('*.$2k'))
            if len(files)!=3:raise ValueError('Faltam exportações')
            models[state]={}
            for p in files:
                name='N1' if p.stem.endswith('N1') else 'N2' if p.stem.endswith('N2') else 'portico'
                if name in models[state]:raise ValueError('Modelo ambíguo')
                models[state][name]=r122.parse(p.read_text(encoding='cp1252'))
                exports.append({'branch':b,'state':state,'model':name,'file':p.relative_to(OUT).as_posix(),'sha256':sha(p)})
        comparisons={}
        for name in ['N1','N2','portico']:
            a,c=[models[s][name] for s in ['BASE','W15']]
            tables={}
            for t in sorted(set(a['tables'])|set(c['tables'])):
                ca=Counter(encode(r) for r in a['tables'].get(t,[]));cc=Counter(encode(r) for r in c['tables'].get(t,[]))
                tables[t]={'equalIncludingIdsAndOrderOfEndpoints':ca==cc,
                    'added':[json.loads(s) for s in (cc-ca).elements()],
                    'removed':[json.loads(s) for s in (ca-cc).elements()]}
            comparisons[name]={'geometry':r122.geometry_comparison(a,c),
                'jointCounts':{'BASE':len(a['joints']),'W15':len(c['joints'])},
                'frameCounts':{'BASE':len(a['frames']),'W15':len(c['frames'])},
                'changedTables':{t:v for t,v in tables.items() if not v['equalIncludingIdsAndOrderOfEndpoints']},
                'unchangedTableCount':sum(v['equalIncludingIdsAndOrderOfEndpoints'] for v in tables.values())}
        a,c=[models[s]['N1'] for s in ['BASE','W15']]
        before=nodal(a);after=nodal(c)
        if before or len(after)!=2:raise ValueError('Diferença nodal não é apenas a W15 esperada')
        if set(comparisons['N1']['changedTables'])!={'JOINT LOADS - FORCE'}:
            raise ValueError('Outras mudanças na grelha N1 exigem investigação')
        force=resultant(after)
        if D(force['signedFzKgf'])!=D('-446.0250'):raise ValueError('Integral nodal inesperada')
        branches[b]={'modelComparisonsToOwnR116':comparisons,'W15AddedNodalLoadsN1':after,'resultant':force,
            'sessions':{s:json.loads((OUT/f'{b}-{s}-sessao-tempo.json').read_text(encoding='utf-8')) for s in ['BASE','W15']}}
    paired=branches['CAD']['W15AddedNodalLoadsN1']==branches['BIM']['W15AddedNodalLoadsN1']
    if not paired:raise ValueError('Distribuição diferente entre CAD/BIM')
    data={'revision':'H03/R132','createdAtUtc':datetime.now(timezone.utc).isoformat(),
      'scope':'Comparação de exportações textuais nativas R116/R131; somente leitura de cópias, sem execução SAP2000.',
      'protectedSourceFiles':protected,'copyPrjs':copies,'sourceFilesUnchanged':True,'copyPrjsUnchanged':True,
      'exports':exports,'branches':branches,'pairedN1AddedNodalLoadsEqual':paired,
      'forceIntegralRetainedUnderObservedDisplayConvention':True,'firstMomentsOfIdealWallRetainedInN1Export':False,
      'graphicalWallPositionR130Changed':False,'nativeLineWasEnteredAfterImport':True,
      'CADorBIMTransferDefectProven':False,'causeOfNodalMappingProven':False,
      'W15AcceptedAsFinalLocalModel':False,'newProcessingPerformed':False,'SAP2000Executed':False,
      'monographEdited':False,'finalStructuralApproval':False,'finalProductivityRankingAllowed':False,
      'nextStep':'Ensaiar discretização mais fina ou alinhada à W15 e conferir forças, primeiros momentos e efeitos antes de ampliar cargas semelhantes.'}
    (OUT/'R132-resultado.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'protectedFiles':len(protected),'copyPrjsUnchanged':len(copies),'exports':len(exports),'pairedNodalLoadsEqual':paired,'resultant':branches['CAD']['resultant'],
        'changedTables':{b:{n:list(v['changedTables']) for n,v in branches[b]['modelComparisonsToOwnR116'].items()} for b in branches}},ensure_ascii=False))

if __name__=='__main__':main()

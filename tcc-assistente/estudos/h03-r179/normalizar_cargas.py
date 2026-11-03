"""Auditoria somente leitura das cargas locais exportadas na R178.

Converte componentes para referencia global e inverte estacoes ao ordenar I/J.
Nao executa SAP2000, nao altera PRJs e nao verifica dimensionamento.
Convencao: https://docs.csiamerica.com/help-files/sap/Menus/Assign/Frame/Frame_Local_Axes.htm
"""
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
import math, sys, json
HERE = Path(__file__).parent
sys.path.insert(0,str(HERE.parent/'h03-r177'))
from comparar_escada import module, model_kind
from auditar_escada import sha

SOURCE = Path('D:/TCC/outputs/Escada-H03-R178-CONTORNO-PATAMAR-NAO-EXECUTAR')
OUT = Path('D:/TCC/outputs/Analise-H03-R179-CARGAS-REFERENCIA-COMUM-NAO-EXECUTAR')


def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(a):
    n=math.sqrt(dot(a,a))
    if n <= 1e-12 or not math.isfinite(n): raise ValueError('Barra nula ou nao finita')
    return tuple(x/n for x in a)


def local_axes(i,j,angle_degrees=0):
    e1=unit(tuple(b-a for a,b in zip(i,j)))
    # Regra de verticalidade do manual CSI: seno menor que 10^-3.
    if math.hypot(e1[0],e1[1]) < 1e-3:
        e2=unit(tuple(x-dot((1,0,0),e1)*y for x,y in zip((1,0,0),e1)))
    else:
        e2=unit(tuple(x-e1[2]*y for x,y in zip((0,0,1),e1)))
    e3=cross(e1,e2)
    angle=math.radians(angle_degrees)
    c,s=math.cos(angle),math.sin(angle)
    rotated2=tuple(c*x+s*y for x,y in zip(e2,e3))
    rotated3=tuple(-s*x+c*y for x,y in zip(e2,e3))
    return e1,rotated2,rotated3


def number(value):
    v=float(str(value).replace(',','.'))
    if not math.isfinite(v): raise ValueError('Numero nao finito')
    return v


def canonical_load(model,row,table):
    if row.get('CoordSys')!='LOCAL' or row.get('Type')!='Force' or row.get('DistType')!='RelDist':
        raise ValueError('Tipo de carga ainda nao suportado: '+str(row))
    if row.get('Dir') not in ('1','2','3'): raise ValueError('Direcao local invalida')
    if any(rows for name,rows in model['tables'].items()
           if name.startswith('FRAME LOCAL AXES ASSIGNMENTS')
           and name!='FRAME LOCAL AXES ASSIGNMENTS 1 - TYPICAL'):
        raise ValueError('Eixos avancados exigem leitura especifica')
    angle_rows=model['tables'].get('FRAME LOCAL AXES ASSIGNMENTS 1 - TYPICAL',[])
    matches=[r for r in angle_rows if r['Frame']==row['Frame']]
    if len(matches)>1: raise ValueError('Angulo duplicado')
    if matches and any(k not in ('Frame','Angle') for k in matches[0]):
        raise ValueError('Atributos de eixo nao suportados')
    i,j=model['frames'][row['Frame']]
    vector=local_axes(i,j,number(matches[0]['Angle']) if matches else 0)[int(row['Dir'])-1]
    reverse=i>j
    segment=tuple(sorted((tuple(i),tuple(j))))
    if table=='FRAME LOADS - POINT':
        t=number(row['RelDist'])
        if not 0 <= t <= 1: raise ValueError('Estacao fora da barra')
        key=(segment,row['LoadPat'],round(1-t if reverse else t,8))
        return key,tuple(number(row['Force'])*x for x in vector)
    if table!='FRAME LOADS - DISTRIBUTED': raise ValueError('Tabela nao suportada')
    a,b=number(row['RelDistA']),number(row['RelDistB'])
    if not 0 <= a < b <= 1: raise ValueError('Intervalo de carga invalido')
    qa,qb=number(row['FOverLA']),number(row['FOverLB'])
    if reverse: a,b,qa,qb=1-b,1-a,qb,qa
    key=(segment,row['LoadPat'],round(a,8),round(b,8))
    return key,tuple(qa*x for x in vector)+tuple(qb*x for x in vector)


def aggregate(model,table):
    result={}; count=defaultdict(int)
    for row in model['tables'].get(table,[]):
        key,vector=canonical_load(model,row,table)
        if key not in result: result[key]=[0.0]*len(vector)
        result[key]=[a+b for a,b in zip(result[key],vector)]
        count[key]+=1
    return result,dict(count)


def compare_rows(a,b):
    differences=[]
    for key in sorted(a.keys()|b.keys()):
        av,bv=a.get(key),b.get(key)
        # Arredondamento declarado so elimina residuo trigonometrico de maquina.
        if av is None or bv is None or tuple(round(x,8) for x in av)!=tuple(round(x,8) for x in bv):
            differences.append(dict(key=key,cad=av,bim=bv,
                bimMinusCad=[y-x for x,y in zip(av,bv)] if av is not None and bv is not None else None))
    return dict(cadGroups=len(a),bimGroups=len(b),positionPatternKeysEqual=a.keys()==b.keys(),
                equalAtDeclaredRounding=not differences,differences=differences,
                maxAbsoluteComponentDifference=max((abs(x) for d in differences
                    for x in (d['bimMinusCad'] or [])),default=0))


def main():
    OUT.mkdir(exist_ok=True)
    control=json.loads((SOURCE/'R178-comparacao-CAD-BIM.json').read_text(encoding='utf-8'))
    sap=module('sap179',HERE.parent/'h03-r122/consolidar.py')
    models={}; before={}
    for branch,entry in control['branches'].items():
        paths=[entry['projectPath'],entry['ifcPath']]+[r['path'] for r in entry['exports'].values()]
        before[branch]={p:sha(p) for p in paths}
        expected={entry['projectPath']:entry['projectSha256'],entry['ifcPath']:entry['ifcSha256']}
        expected.update({r['path']:r['sha256'] for r in entry['exports'].values()})
        if before[branch]!=expected:
            raise ValueError('Fonte mudou depois da auditoria R178')
        models[branch]={model_kind(Path(r['path']).name):sap.parse(Path(r['path']).read_text(encoding='cp1252'))
                        for r in entry['exports'].values()}
    results={}
    for kind in ('portico','escada','N1','N2'):
        results[kind]={}
        for table in ('FRAME LOADS - DISTRIBUTED','FRAME LOADS - POINT'):
            a,ac=aggregate(models['CAD'][kind],table)
            b,bc=aggregate(models['BIM'][kind],table)
            compared=compare_rows(a,b)
            compared['inputRows']={branch:len(models[branch][kind]['tables'].get(table,[])) for branch in ('CAD','BIM')}
            compared['groupsWithMultipleInputRows']={'CAD':sum(v>1 for v in ac.values()),'BIM':sum(v>1 for v in bc.values())}
            results[kind][table]=compared
    if any(sha(p)!=value for branch in before.values() for p,value in branch.items()):
        raise ValueError('Fonte alterada durante a leitura')
    result=dict(revision='H03/R179',recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        sourceR178Sha256=sha(SOURCE/'R178-comparacao-CAD-BIM.json'),sourceHashes=before,
        sourcesUnchangedAfterRead=True,scope='Cargas locais de forca de barras com distancias relativas; somente leitura',
        exportUnits='Kgf, cm, C',exportUnitsVerifiedByParser=True,
        distributedGlobalVectorUnits='kgf/cm',pointGlobalVectorUnits='kgf',
        globalComponentRoundingDigits=8,relativeStationRoundingDigits=8,
        distributedComponentsAggregatedOnlyAtIdenticalSegmentPatternAndInterval=True,
        pointComponentsAggregatedOnlyAtIdenticalSegmentPatternAndStation=True,
        csiLocalAxisConventionImplemented=True,sourceLocalAxesAnglePrecisionPreserved=True,
        sourceRelativeStationPrecisionPreserved=True,results=results,
        frameForceResultDiagramsCompared=False,jointLoadResidualsRemainInR178=True,
        allNativeStiffnessEffectsVerified=False,fullNativeModelEquivalenceVerified=False,
        structuralApproval=False)
    (OUT/'R179-cargas-globais.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:{t:{a:r[a] for a in ('cadGroups','bimGroups','equalAtDeclaredRounding','maxAbsoluteComponentDifference')}
                        for t,r in v.items()} for k,v in results.items()},indent=2))


if __name__=='__main__': main()

"""Reacoes gravitacionais de sensibilidade do telhado P2, separado do tanque."""
import hashlib
import json
import math
from datetime import datetime,timezone
from pathlib import Path
from time import perf_counter

ROOT=Path('D:/TCC/outputs')
OUT=ROOT/'Cobertura-H03-R114-P2-HIPOTESE-NAO-EXECUTAR'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def corner_loads(g,box):
    x0,y0,x1,y1=box
    if not all(math.isfinite(v) for v in [g,*box]) or g<=0 or x1<=x0 or y1<=y0:raise ValueError('Carga/geometria invalida')
    force=g*(x1-x0)*(y1-y0)/4
    return [{'id':f'RP2-{i:02d}','xM':x,'yM':y,'FxKN':0,'FyKN':0,'FzKN':-force,
             'MxKNm':0,'MyKNm':0,'MzKNm':0} for i,(x,y) in enumerate([(x0,y0),(x1,y0),(x0,y1),(x1,y1)],1)]


def main():
    start=perf_counter();start_utc=datetime.now(timezone.utc).isoformat()
    if OUT.exists():raise FileExistsError('Nao sobrescrever plano')
    sources=[ROOT/'Cobertura-H03-R59-MEMORIA-ESTUDO-NAO-EXECUTAR/R59-memoria-cobertura.json',
             ROOT/'Cobertura-H03-R60-REACOES-PARCIAIS-NAO-EXECUTAR/R60-arranjo-reacoes.json',
             ROOT/'Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR/R56-geometria-exportada.json',
             ROOT/'Altimetria-H03-R113-CONSULTA-NAO-EXECUTAR/R113-resultado.json']
    roof,arrangement,geometry,levels=[json.loads(p.read_text(encoding='utf-8-sig')) for p in sources]
    if sha(sources[2])!=arrangement['geometrySource']['sha256']:raise ValueError('Geometria historica divergente')
    p2=next(p for p in arrangement['planes'] if p['id']=='P2')
    if p2['box']!=[6.55,0,9.65,3.9]:raise ValueError('P2 diferente')
    actions={}
    for action,value in {'G_ADICIONAL':roof['loads']['roofPermanentHorizontalKNm2'],
                          'Q_TELHADO_MANUTENCAO':roof['loads']['roofMaintenanceHorizontalKNm2']}.items():
        nodes=corner_loads(value,p2['box'])
        for n in nodes:
            n['targetsHistoricalR56']={}
            for branch,elements in geometry.items():
                candidates=[e for e in elements if e['type']=='IfcColumn' and abs(e['max'][2]-6.39)<1e-6
                            and e['min'][0]<=n['xM']<=e['max'][0] and e['min'][1]<=n['yM']<=e['max'][1]]
                if len(candidates)!=1:raise ValueError('Alvo historico nao unico')
                n['targetsHistoricalR56'][branch]=candidates[0]
            n['overlapsVP1']=(n['xM'],n['yM'])==(9.65,3.9)
        total=value*12.09
        effect={'FzKN':sum(n['FzKN'] for n in nodes),
                'MxKNm':sum(n['yM']*n['FzKN'] for n in nodes),
                'MyKNm':sum(-n['xM']*n['FzKN'] for n in nodes)}
        expected={'FzKN':-total,'MxKNm':-total*1.95,'MyKNm':total*8.1}
        if any(abs(effect[k]-expected[k])>1e-9 for k in expected):raise ValueError('Equilibrio divergente')
        actions[action]={'loadHorizontalKNm2':value,'nodes':nodes,'resultant':effect,'equilibriumPassed':True}
    result={'revision':'H03/R114','createdAtUtc':datetime.now(timezone.utc).isoformat(),'hypothesisId':'P2-GRAV-A',
            'areaM2':12.09,'boxM':p2['box'],'actions':actions,
            'concept':'Dois quadros transversais X em Y0/3,90 recebem as tercas longitudinais Y da cobertura de caimento-X. Quatro montantes alinhados aos nos de concreto N2. Esquema gravitacional articulado idealizado, sem atribuicao de resistencia/rigidez ao metal.',
            'equalQuartersRequireSymmetricUniformLoadingAndArticulatedIdealization':True,
            'absoluteRoofAndSteelNodeGeometryFinalized':False,
            'relativeTankBaseFromR113M':levels['architecturalGraphicRegistration']['derivedLevelsM']['raisedTankBase'],
            'tankLoadsIncluded':False,'nativeApplicationPerformed':False,'finalStructuralApproval':False,
            'sources':[{'path':str(p),'sha256':sha(p)} for p in sources],
            'loadAccumulationRule':'Somar incremento P2 aos valores existentes por acao; RP2-04 coincide com VP1-01 e deve preservar Fz e My anteriores. Nao substituir vetor total por incremento.',
            'limits':['G conserva reserva de0,15kN/m2 para metal, sem levantamento de perfis/montantes.',
                      'A area nominal por eixos nao e medicao liquida da telha ou volume de material.',
                      'Quatro forcas equilibradas nao dimensionam perfis, ancoragens, quadro ou nos de concreto.',
                      'Metal nao modelado: nao acrescentar rigidez lateral ficticia ao concreto.',
                      'Sem vento/succao, caso localizado de manutencao, deformacoes do metal, acesso ao tanque ou ligacoes.',
                      'Altimetria dos perfis deve respeitar o contorno R112/R113; nao elevar cobertura para encaixar.',
                      'A soma das parcelas A1/A2/P1/P2 representa apenas a hipotese distribuida gravitacional do telhado.',
                      'Nao inclui policarbonato, platibandas/calhas, agua, tara ou plataforma do tanque.']}
    OUT.mkdir()
    (OUT/'R114-plano-P2.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'R114-tempo-script.json').write_text(json.dumps({'startUtc':start_utc,'endUtc':datetime.now(timezone.utc).isoformat(),
        'durationMs':(perf_counter()-start)*1000,'scope':'Somente aritmetica e identificacao historica; nao autoria ou inferencia IA'},indent=2),encoding='utf-8')
    print(json.dumps({a:{'eachFzKN':v['nodes'][0]['FzKN'],'totalKN':v['resultant']['FzKN']} for a,v in actions.items()}))


if __name__=='__main__':main()

"""Gera plantas 2D separadas, sem deslocar a origem, do candidato comum R158.

O DXF fornece desenho de referência, não elementos de cálculo do Eberick.
"""
import hashlib
import json
import math
import sys
import time
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path

START=time.perf_counter()
START_UTC=datetime.now(timezone.utc).isoformat()
sys.path.insert(0,'D:/TCC/work/dxf-deps')
import ezdxf

OUT=Path('D:/TCC/outputs/Escada-H03-R159-IMPLANTACAO-NAO-EXECUTAR')
PLAN=Path('D:/TCC/outputs/Escada-H03-R158-CANDIDATO-COMUM-NAO-EXECUTAR/R158-candidato-comum.json')
PIN='a0dec2b713ea8ea945207c366b0c31ad2c7a0bd1be41dd6a7f196adc752764eb'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def draw(e,ms,prefix):
    kind=e['kind'];layer=prefix+'_'+dict(column='PILARES',beam='VIGAS',slab='LAJES')[kind]
    if kind=='column':
        x,y=e['x'],e['y'];b,h=e['b'],e['h'];pts=[(x-b/2,y-h/2),(x+b/2,y-h/2),(x+b/2,y+h/2),(x-b/2,y+h/2)]
    elif kind=='beam':
        x,y,x2,y2=e['x'],e['y'],e['x2'],e['y2'];length=math.hypot(x2-x,y2-y)
        if length<=0:raise ValueError('Viga sem comprimento')
        dx,dy=-(y2-y)*e['b']/(2*length),(x2-x)*e['b']/(2*length)
        pts=[(x+dx,y+dy),(x2+dx,y2+dy),(x2-dx,y2-dy),(x-dx,y-dy)]
    elif kind=='slab':pts=[(e['x'],e['y']),(e['x2'],e['y']),(e['x2'],e['y2']),(e['x'],e['y2'])]
    else:raise ValueError(kind)
    poly=ms.add_lwpolyline(pts,close=True,dxfattribs={'layer':layer})
    raw=json.dumps(e,separators=(',',':'),ensure_ascii=True)
    # Os valores pequenos deste contrato cabem em um registro XDATA de 255 bytes.
    assert len(raw.encode('ascii'))<=255
    poly.set_xdata('TCC_R159',[(1000,e['id']),(1000,raw)])
    x=sum(p[0] for p in pts)/4;y=sum(p[1] for p in pts)/4
    size=f"{e['h']*100:g}cm" if kind=='slab' else f"{e['b']*100:g}x{e['h']*100:g}cm"
    ms.add_text(e['id']+' '+size,dxfattribs={'height':.065,'insert':(x+.03,y+.03,0),'layer':prefix+'_TEXTO'})
    if kind=='beam':ms.add_line((e['x'],e['y'],0),(e['x2'],e['y2'],0),dxfattribs={'layer':prefix+'_EIXOS'})
    return poly

def main():
    target=OUT/'R159-formas-CAD-geradas.json'
    if target.exists():raise FileExistsError(target)
    assert sha(PLAN)==PIN
    p=json.loads(PLAN.read_text(encoding='utf-8'));rows=sum((p[k] for k in ('retainedExistingElements','changedExistingElements','addedElements')),[])
    assert len(rows)==65 and len({e['id'] for e in rows})==65
    files=[];represented=set()
    for name,z in [('N1',3.20),('N2',6.39),('PATAMAR',p['concreteLandingM'])]:
        path=OUT/f'R159-CAD-{name}-FORMA-CANDIDATA.dxf'
        if path.exists():raise FileExistsError(path)
        d=ezdxf.new('R2013');d.units=6;d.appids.new('TCC_R159');ms=d.modelspace()
        for suffix,color in [('PILARES',1),('VIGAS',2),('LAJES',4),('TEXTO',7),('EIXOS',3),('CONTEXTO',8),('AVISOS',1)]:d.layers.new(name+'_'+suffix,dxfattribs={'color':color})
        selected=[e for e in rows if abs(e.get('z',e.get('z1'))-z)<1e-8]
        for e in selected:draw(e,ms,name);represented.add(e['id'])
        if name=='PATAMAR':
            # Pilares passantes não são novos segmentos no nível intermediário.
            for e in rows:
                if e['kind']=='column' and e['z0']<z<e['z1']:
                    poly=draw(e,ms,name);poly.dxf.layer=name+'_CONTEXTO'
            landing=next(f for f in p['concreteTopSurfaces'] if f['kind']=='landing')
            ms.add_lwpolyline([v[:2] for v in landing['vertices']],close=True,dxfattribs={'layer':name+'_CONTEXTO'})
        for i,text in enumerate([f'R159 - {name} - TOPO DO CONCRETO +{z:.6f} m',
            'CANDIDATO COMUM - SEM DIMENSIONAMENTO - NAO EXECUTAR',
            'UNIDADE: METRO | ORIGEM XY PRESERVADA | GEOMETRIA 2D Z=0',
            'C25/CA-50: PREMISSAS; DXF NAO CRIA MATERIAL OU ELEMENTO ANALITICO',
            'ESCADA17: APOIO INFERIOR/CONTINUIDADE/ANCORAGEM/CARGAS PENDENTES']):
            ms.add_text(text,dxfattribs={'height':.10,'insert':(-.5,-1-i*.20,0),'layer':name+'_AVISOS'})
        d.saveas(path);check=ezdxf.readfile(path);assert not check.audit().has_errors and check.units==6
        actual=[]
        for entity in check.modelspace().query('LWPOLYLINE'):
            if entity.has_xdata('TCC_R159'):
                tags=[t.value for t in entity.get_xdata('TCC_R159') if t.code==1000];assert len(tags)==2
                assert tags[0]==json.loads(tags[1])['id'];actual.append(tags[0]);assert entity.closed and entity.dxf.elevation==0
        assert set(e['id'] for e in selected).issubset(actual)
        files.append(dict(path=str(path),sha256=sha(path),level=name,concreteTopM=z,selectedElementIds=[e['id'] for e in selected],selectedCount=len(selected),
            countsByKind=dict(Counter(e['kind'] for e in selected)),includesPassingColumnsAsContext=name=='PATAMAR',units='m',allCoordinatesProjectedWithoutXYTranslation=True,nativeAutoCadVerified=False,eberickImported=False))
    assert represented=={e['id'] for e in rows}
    result=dict(candidatePath=str(PLAN),candidateSha256=PIN,files=files,uniqueBuildingElementCount=65,stairsResistantVolumeIncluded=False,
        analyticalObjectsCreated=False,materialTransferredToEberick=False,structuralApproval=False,startedUtc=START_UTC,endedUtc=datetime.now(timezone.utc).isoformat(),scriptElapsedMs=(time.perf_counter()-START)*1000,
        scriptTimeIsNotFlowTime=True,pairedRankingCompleted=False)
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(files=len(files),uniqueElements=65,scriptElapsedMs=result['scriptElapsedMs'])))

if __name__=='__main__':main()

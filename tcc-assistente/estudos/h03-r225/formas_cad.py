"""Plantas 2D da hipotese R225; conversao e retorno pela CLI nativa AutoCAD 2027."""
import argparse
import hashlib
import json
import math
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy  # Carrega a extensao compilada antes das dependencias DXF locais.
sys.path.append('D:/TCC/work/dxf-deps')
import ezdxf

ROOT=Path('D:/TCC/outputs/H03-R225-AUTORIA-COORDENACAO-NAO-EXECUTAR')
ENGINE=Path('D:/AutoCAD 2027/accoreconsole.exe')
APP='TCC_R225'
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'h03-r160'))
from verificar_cad import compare


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def write(name,data): (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def draw(e,ms,prefix,context=False):
    kind=e['kind'];layer=prefix+('_CONTEXTO' if context else '_'+dict(column='PILARES',beam='VIGAS',slab='LAJES')[kind])
    if kind=='column':
        x,y,b,h=(e[k] for k in ('x','y','b','h'))
        pts=[(x-b/2,y-h/2),(x+b/2,y-h/2),(x+b/2,y+h/2),(x-b/2,y+h/2)]
    elif kind=='beam':
        x,y,x2,y2=(e[k] for k in ('x','y','x2','y2'));length=math.hypot(x2-x,y2-y)
        if length<=0: raise ValueError('Viga sem comprimento')
        dx,dy=-(y2-y)*e['b']/(2*length),(x2-x)*e['b']/(2*length)
        pts=[(x+dx,y+dy),(x2+dx,y2+dy),(x2-dx,y2-dy),(x-dx,y-dy)]
    else:pts=[(e['x'],e['y']),(e['x2'],e['y']),(e['x2'],e['y2']),(e['x'],e['y2'])]
    poly=ms.add_lwpolyline(pts,close=True,dxfattribs={'layer':layer})
    raw=json.dumps({k:e[k] for k in ('id','kind','level','x','y','x2','y2','z','z0','z1','b','h') if k in e},separators=(',',':'),ensure_ascii=True)
    if len(raw.encode())>255: raise ValueError('Metadados nao cabem no XDATA')
    poly.set_xdata(APP,[(1000,e['id']),(1000,raw)])
    x=sum(p[0] for p in pts)/4;y=sum(p[1] for p in pts)/4
    size=f"h={e['h']*100:g}cm" if kind=='slab' else f"{e['b']*100:g}x{e['h']*100:g}cm"
    ms.add_text(e['id']+' '+size,dxfattribs={'height':.065,'insert':(x+.03,y+.03,0),'layer':prefix+'_TEXTO'})
    if kind=='beam':ms.add_line((e['x'],e['y'],0),(e['x2'],e['y2'],0),dxfattribs={'layer':prefix+'_EIXOS'})


def generate():
    timer=time.perf_counter();started=datetime.now(timezone.utc).isoformat()
    if (ROOT/'R225-formas-geradas.json').exists(): raise FileExistsError('Plantas ja geradas')
    plan_path=ROOT/'R225-candidato-comum.json';plan=json.loads(plan_path.read_text(encoding='utf-8'))
    entries=sum((plan[k] for k in ('retainedExistingElements','changedExistingElements','addedElements')),[])
    if len(entries)!=66 or len({e['id'] for e in entries})!=66: raise ValueError('Contagem divergente')
    stair=json.loads((HERE.parent/'h03-r160/R160-candidato-comum.json').read_text(encoding='utf-8'))
    files=[];represented=set()
    for name,z in [('N0',.2),('PATAMAR',stair['concreteLandingM']),('N1',3.2),('N2',6.39)]:
        path=ROOT/f'R225-CAD-{name}-COORDENACAO-NAO-EXECUTAR.dxf'
        if path.exists(): raise FileExistsError(path)
        d=ezdxf.new('R2013');d.units=6;d.appids.new(APP);ms=d.modelspace()
        for suffix,color in [('PILARES',1),('VIGAS',2),('LAJES',4),('TEXTO',7),('EIXOS',3),('CONTEXTO',8),('AVISOS',1)]:
            d.layers.new(name+'_'+suffix,dxfattribs={'color':color})
        selected=[e for e in entries if abs(e.get('z',e.get('z1'))-z)<1e-8]
        for e in selected:draw(e,ms,name);represented.add(e['id'])
        if name in ('PATAMAR','N0'):
            for e in entries:
                if e['kind']=='column' and e['z0']<=z<e['z1']: draw(e,ms,name,context=True)
        if name in ('PATAMAR','N0','N1'):
            for face in stair['concreteTopSurfaces']:
                pts=[tuple(p[:2]) for p in face['vertices']]
                # Espelhos projetados degeneram em uma linha: nao se criam faces invalidas.
                distinct=list(dict.fromkeys(pts))
                if len(distinct)>=3:ms.add_lwpolyline(distinct,close=True,dxfattribs={'layer':name+'_CONTEXTO'})
                elif len(distinct)==2:ms.add_line(distinct[0],distinct[1],dxfattribs={'layer':name+'_CONTEXTO'})
        for i,text in enumerate([f'R225 - {name} - TOPO CONCRETO +{z:.6f} m',
            'COORDENACAO DA HIPOTESE EBERICK R223/R224 - NAO EXECUTAR',
            'UNIDADE: METRO | ORIGEM XY PRESERVADA | DESENHO 2D Z=0',
            'C25/CA-50: PREMISSAS | SEM ARMADURA OU OBJETO ANALITICO',
            'ESCADA17 PRESERVADA | V1 BASE30x30 | APOIOS IDEALIZADOS SEM FUNDACOES',
            'LIGACOES, AVISOS08/19, W08 E INTERFACES ARQUITETONICAS PENDENTES']):
            ms.add_text(text,dxfattribs={'height':.10,'insert':(-.5,-1-i*.20,0),'layer':name+'_AVISOS'})
        d.saveas(path);r=ezdxf.readfile(path)
        if r.audit().has_errors or r.units!=6: raise ValueError('DXF gerado invalido')
        files.append(dict(path=str(path),sha256=sha(path),level=name,topM=z,
            selectedElementIds=[e['id'] for e in selected],countsByKind=dict(Counter(e['kind'] for e in selected)),
            nativeAutoCadVerified=False,eberickImported=False))
    if represented!={e['id'] for e in entries}: raise ValueError('Elemento ausente nas plantas')
    result=dict(candidateSha256=sha(plan_path),files=files,uniqueElements=66,
        startedUtc=started,endedUtc=datetime.now(timezone.utc).isoformat(),generationMs=(time.perf_counter()-timer)*1000,
        generationTimeIsNotFlowTime=True,pairedRankingComplete=False)
    write('R225-formas-geradas.json',result)
    return result


def native():
    source=json.loads((ROOT/'R225-formas-geradas.json').read_text(encoding='utf-8'))
    if (ROOT/'R225-CAD-nativo.json').exists(): raise FileExistsError('Conversao ja registrada')
    records=[];overall=time.perf_counter();overall_start=datetime.now(timezone.utc).isoformat()
    for item in source['files']:
        p=Path(item['path']);dwg=p.with_suffix('.dwg');returned=p.with_name(p.stem+'-retorno.dxf')
        if sha(p)!=item['sha256'] or dwg.exists() or returned.exists(): raise ValueError('Entrada alterada ou saida existente')
        for stage in ('salvar','reabrir'):
            script=ROOT/f"R225-{item['level']}-{stage}.scr"
            if stage=='salvar':
                lines=['_.FILEDIA','0','_.DXFIN',str(p),'_.ZOOM','_Extents','_.SAVEAS','2018',str(dwg),'_.QUIT']
                args=[str(ENGINE),'/s',str(script),'/l','en-US']
            else:
                lines=['_.FILEDIA','0','_.DXFOUT',str(returned),'16','_.QUIT']
                args=[str(ENGINE),'/i',str(dwg),'/s',str(script),'/l','en-US']
            script.write_text('\n'.join(lines)+'\n',encoding='ascii')
            start=datetime.now(timezone.utc).isoformat();timer=time.perf_counter()
            process=subprocess.run(args,cwd=ROOT,capture_output=True,timeout=180)
            elapsed=time.perf_counter()-timer
            # O motor Windows escreve UTF-16LE em pipe.
            log=(process.stdout+process.stderr).decode('utf-16le',errors='replace')
            (ROOT/f"R225-{item['level']}-{stage}.log").write_text(log,encoding='utf-8')
            records.append(dict(level=item['level'],stage=stage,startedUtc=start,
                endedUtc=datetime.now(timezone.utc).isoformat(),processSeconds=elapsed,exitCode=process.returncode,
                scope='Inicializacao e script do CoreConsole; nao tempo total do fluxo'))
            write('R225-CAD-nativo-parcial.json',dict(records=records,complete=False))
            if process.returncode!=0: raise RuntimeError('Falha nativa: '+item['level']+' '+stage)
            if stage=='salvar' and (not dwg.exists() or dwg.read_bytes()[:6]!=b'AC1032'):
                raise ValueError('DWG nativo ausente ou formato inesperado')
            if stage=='reabrir' and not returned.exists(): raise ValueError('DXF de retorno ausente')
    result=dict(records=records,startedUtc=overall_start,endedUtc=datetime.now(timezone.utc).isoformat(),
        sequentialProcessWallSeconds=time.perf_counter()-overall,nativeEngine=str(ENGINE),complete=True,
        inputIsSharedCandidate=True,interoperabilityToEberickTested=False,fullWorkflowTimeMeasured=False)
    write('R225-CAD-nativo.json',result)
    return result


def read(path):
    d=ezdxf.readfile(path)
    if d.units!=6 or d.audit().has_errors: raise ValueError('DXF invalido ou unidade mudou')
    rows=[];data={};anonymous=0
    for e in d.modelspace().query('LWPOLYLINE'):
        if not e.closed or e.dxf.elevation!=0: raise ValueError('Face aberta ou nao 2D')
        if e.has_xdata(APP):
            tags=[t.value for t in e.get_xdata(APP) if t.code==1000]
            if len(tags)!=2 or tags[0] in data: raise ValueError('Identidade ausente ou duplicada')
            key=tags[0];data[key]=json.loads(tags[1])
        else:key='contexto-'+str(anonymous);anonymous+=1
        rows.append(dict(id=key,layer=e.dxf.layer,vertices=[[p[0],p[1],0] for p in e.get_points('xy')]))
    texts=Counter(e.dxf.text for e in d.modelspace().query('TEXT'))
    lines=Counter((e.dxf.layer,tuple(e.dxf.start),tuple(e.dxf.end)) for e in d.modelspace().query('LINE'))
    return rows,data,texts,lines


def compare_axes(before,after,tolerance=1e-9):
    """Compara multiconjuntos sem exigir igualdade binaria de floats do DXF."""
    pending=list(after.elements());maximum=0.
    for layer,start,end in before.elements():
        choices=[]
        for i,(other_layer,a,b) in enumerate(pending):
            if layer!=other_layer: continue
            for p,q in ((a,b),(b,a)):
                values=[abs(x-y) for s,t in ((start,p),(end,q)) for x,y in zip(s,t,strict=True)]
                if any(not math.isfinite(v) for v in values):raise ValueError('Eixo nao finito')
                delta=max(values)
                choices.append((delta,i))
        if not choices: raise ValueError('Eixo ausente')
        delta,index=min(choices)
        if delta>tolerance:raise ValueError('Eixo deslocado')
        maximum=max(maximum,delta);pending.pop(index)
    if pending: raise ValueError('Eixos adicionais')
    return maximum


def verify():
    generated=json.loads((ROOT/'R225-formas-geradas.json').read_text(encoding='utf-8'))
    native=json.loads((ROOT/'R225-CAD-nativo.json').read_text(encoding='utf-8'))
    if not native['complete']: raise ValueError('Conversao incompleta')
    result=[];unique=set()
    for item in generated['files']:
        p=Path(item['path']);dwg=p.with_suffix('.dwg');ret=p.with_name(p.stem+'-retorno.dxf')
        if sha(p)!=item['sha256']: raise ValueError('DXF fonte alterado')
        a,b=read(p),read(ret);delta=compare(a[0],b[0])
        if a[1:3]!=b[1:3]: raise ValueError('Metadados ou textos divergentes')
        axis_delta=compare_axes(a[3],b[3])
        if not set(item['selectedElementIds']).issubset(b[1]): raise ValueError('Elemento perdido')
        unique.update(item['selectedElementIds'])
        result.append(dict(level=item['level'],dwg=str(dwg),sha256=sha(dwg),returnSha256=sha(ret),
            maxCoordinateDeltaM=delta,maxAxisCoordinateDeltaM=axis_delta,
            coordinateToleranceM=1e-9,xdataTextAndAxesRetained=True,selectedCount=len(item['selectedElementIds'])))
    if len(unique)!=66: raise ValueError('Contagem total divergente')
    out=dict(files=result,uniqueElements=66,nativeSavedAndReopened=True,
        eberickImported=False,structuralApproval=False,fullWorkflowComparisonComplete=False)
    write('R225-CAD-conferencia.json',out);return out


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['gerar','nativo','conferir']);args=ap.parse_args()
    action={'gerar':generate,'nativo':native,'conferir':verify}[args.stage]
    print(json.dumps(action(),ensure_ascii=True,indent=2))

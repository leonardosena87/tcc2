"""Candidato comum da escada: geometria de estudo, sem aprovação resistente."""
import copy
import hashlib
import importlib.util
import json
import math
import shutil
import sys
from datetime import datetime,timezone
from pathlib import Path
from time import perf_counter

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R158-CANDIDATO-COMUM-NAO-EXECUTAR')
PROPOSAL=Path('D:/TCC/outputs/Autoria-H03-R83-SINCRONIZACAO-GEOMETRICA-NAO-EXECUTAR/H03-R83-proposta.json')
PLAN=HERE.parent/'h03-r153/R153-geometria9mais8.json'
REF=HERE.parent/'h03-r68/R68-referencia-arquitetonica-estudo.json'
PDF=Path('D:/TCC/PROJETO ARQUITETONICO-A0.pdf')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def bounds(e):
    k=e['kind']
    if k=='column':return [e['x']-e['b']/2,e['y']-e['h']/2,e['z0'],e['x']+e['b']/2,e['y']+e['h']/2,e['z1']]
    if k=='slab':return [e['x'],e['y'],e['z']-e['h'],e['x2'],e['y2'],e['z']]
    if k!='beam':raise ValueError(k)
    if abs(e['y']-e['y2'])<1e-9:return [min(e['x'],e['x2']),e['y']-e['b']/2,e['z']-e['h'],max(e['x'],e['x2']),e['y']+e['b']/2,e['z']]
    if abs(e['x']-e['x2'])<1e-9:return [e['x']-e['b']/2,min(e['y'],e['y2']),e['z']-e['h'],e['x']+e['b']/2,max(e['y'],e['y2']),e['z']]
    raise ValueError('Viga obliqua nao suportada')

def volume_overlap(a,b):return all(min(a[i+3],b[i+3])-max(a[i],b[i])>1e-9 for i in range(3))

def horizontal_surface_overlaps(f,b):
    ps=f['vertices'];z=ps[0][2]
    assert all(abs(p[2]-z)<1e-9 for p in ps)
    return b[2]+1e-9<z<b[5]-1e-9 and all(min(max(p[i] for p in ps),b[i+3])-max(min(p[i] for p in ps),b[i])>1e-9 for i in range(2))

def build(proposal,plan,ref):
    old={e['id']:e for e in proposal['elements']};env=plan['clearEnvelope'];g=plan['geometry']
    # Mantem as posicoes longitudinais R153; reserva a faixa entre faces de pilares.
    xl=4.50;xr=6.45;width=.90;finish=.05
    changed=[copy.deepcopy(old[i]) for i in ('V15-N1','L6-N1')]
    changed[0].update(y=env['upperArrivalYM']+.10,y2=env['upperArrivalYM']+.10,h=.16)
    changed[1]['y']=env['upperArrivalYM']
    ys=env['landingNorthM']-.10
    landingConcrete=g['proposedFinishedLandingM']-finish
    added=[dict(id='P12-ESC-N1',kind='column',x=4.4,y=ys,z0=.2,z1=3.2,b=.2,h=.3,levelReference='N0/N1',role='candidato-apoio-escada'),
           dict(id='P13-ESC-N1',kind='column',x=6.55,y=ys,z0=.2,z1=3.2,b=.2,h=.3,levelReference='N0/N1',role='candidato-apoio-escada'),
           dict(id='V16-ESC-PAT',kind='beam',x=4.4,y=ys,x2=6.55,y2=ys,z=landingConcrete,b=.2,h=.3,levelReference='ESC-INTERMEDIARIO',role='candidato-apoio-patamar')]
    finished=[]
    for f in plan['finishedSurfaceFaces']:
        nf=copy.deepcopy(f)
        if f['kind']=='landing':
            for p in nf['vertices']:p[0]=xl if abs(p[0]-env['xMinM'])<1e-8 else xr
        else:
            isLower=f['number']<=9
            x0=xl if isLower else xr-width
            oldx0=env['xMinM'] if isLower else env['xMaxM']-env['flightWidthGraphicalM']
            for p in nf['vertices']:p[0]=x0 if abs(p[0]-oldx0)<1e-8 else x0+width
        finished.append(nf)
    concrete=copy.deepcopy(finished)
    for f in concrete:
        for p in f['vertices']:p[2]-=finish
    proposed=[copy.deepcopy(e) for e in proposal['elements'] if e['id'] not in ('V15-N1','L6-N1')]+changed+added
    # Teste nominal de SUPERFICIES. Nao inclui o fundo resistente da escada.
    intersections=[]
    for f in concrete:
        if f['kind'] not in ('tread','landing'):continue
        for e in proposed:
            if horizontal_surface_overlaps(f,bounds(e)):intersections.append(dict(face=f.get('number',f['kind']),element=e['id']))
    assert not intersections,intersections
    # A janela alta impede a viga na fachada; seu peitoril e relativo ao piso.
    opening=next(o for floor in ref['floors'] if floor['id']=='T' for o in floor['openings'] if o['id']=='T-J4-01')
    window=[min(opening['x'],opening['x2']),-.075,.22+.20,max(opening['x'],opening['x2']),.075,.22+.20+3.20]
    rejected=dict(id='V-FACHADA-DESCARTADA',kind='beam',x=4.4,y=0,x2=6.55,y2=0,z=landingConcrete,b=.2,h=.3)
    assert volume_overlap(bounds(rejected),window)
    assert all(not volume_overlap(bounds(e),window) for e in added)
    assert abs(changed[0]['y']-.1-env['upperArrivalYM'])<1e-9
    assert abs(added[2]['y']+.1-env['landingNorthM'])<1e-9
    assert abs(concrete[-1]['vertices'][2][2]-3.2)<1e-9
    return dict(schema='tcc-stair-compatibility/1',revision='H03/R158',units='m',status='CANDIDATO COMUM - NAO DIMENSIONADO - NAO EXECUTAR',
        finishedGeometry=copy.deepcopy(g),finishedSurfaces=finished,concreteTopSurfaces=concrete,
        constantFinishHypothesisM=finish,finishDensityAndPermanentLoadNotDefined=True,
        virtualConcreteStartM=.17,virtualStartIsNotLowerFloorConcreteTop=True,existingLowerFloorConcreteTopM=.20,
        lowerSupportElevationDifferenceM=-.03,lowerSupportInterfaceUnresolved=True,
        concreteLandingM=landingConcrete,concreteUpperM=3.20,
        nominalFlightWidthM=width,nominalOuterFacesXM=[xl,xr],centralGapM=(xr-width)-(xl+width),
        widthIsNotVerifiedClearWidthAfterGuards=True,waistAndLandingThicknessHypothesisM=.14,
        noClosedNativeStairVolumeOrSelfWeightDefined=True,
        changedExistingElements=changed,addedElements=added,retainedExistingElements=[e for e in proposed if e['id'] not in {x['id'] for x in changed+added}],
        proposedElementCount=len(proposed),countsByKind={k:sum(e['kind']==k for e in proposed) for k in ('column','beam','slab')},
        nominalHorizontalSurfaceOverlaps=intersections,zeroNominalSurfaceOverlapsIsNotSolidClashClearance=True,
        nominalUpperBeamSoffitM=changed[0]['z']-changed[0]['h'],architectureGroundCeilingHypothesisM=3.02,
        ceilingGapM=changed[0]['z']-changed[0]['h']-3.02,ceilingConstructionAndToleranceUnverified=True,
        rejectedFacadeBeam=rejected,windowJ4BoxInterpretedM=window,facadeBeamCrossesWindow=True,
        windowSource='Tabela da prancha: J4 1.60x3.20m fixa, peitoril0.20m; posicaoR68. Peitoril relativo ao piso terreo+.22m como hipotese explicita.',
        newColumnDoorPlanIntersections=door_intersections(added[:2],ref),
        architectureWallsDoorsAndFacadeMoved=False,stairFinishedLevelsAndLongitudinalPositionsPreserved=True,
        supportSchemeCandidate='Dois pilares laterais e viga interna no bordo norte do patamar; patamar avanca para fachada. Ligacoes/torcao/engaste/balanco a calcular.',
        supportAndAnchorageVerified=False,structuralCapacityVerified=False,modelIntegratedInEberick=False,
        nativeAuthoringApplied=False,activeGeometryReplaced=False,
        modelVersionWarning='Instalado Eberick2025-04; nao pressupor recurso de apoio em viga interior de painel anunciado em2025-11.',
        limitations=['Fundo da escada e contatos volumetricos nao testados; nao minimizar relatorio de interferencia apenas por contagem.',
        'Ancoragem da escada na viga rasa de chegada, cisalhamento/torcao do patamar e ELU/ELS pendentes.',
        'Apoio inferior e rebaixo virtual3cm precisam de tratamento no receptor, sem introduzir fundacao real.',
        'Novos pilares precisam de continuidade ate apoios idealizados N0 e conferencias de vao/circulacao; sem sondagem ou fundacoes dimensionadas.'])

def door_intersections(columns,ref):
    hits=[]
    for floor in ref['floors']:
        for door in floor['openings']:
            b=[min(door['x'],door['x2'])-.05,min(door['y'],door['y2'])-.05,0,max(door['x'],door['x2'])+.05,max(door['y'],door['y2'])+.05,4]
            for c in columns:
                if volume_overlap(bounds(c),b):hits.append(dict(column=c['id'],opening=door['id'],floor=floor['id']))
    return hits

def box_faces(e):
    x,y,z,X,Y,Z=bounds(e)
    v=[[x,y,z],[X,y,z],[X,Y,z],[x,Y,z],[x,y,Z],[X,y,Z],[X,Y,Z],[x,Y,Z]]
    return [[v[i] for i in ids] for ids in ((0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7))]

def export(d):
    sys.path.insert(0,'D:/TCC/work/dxf-deps');import ezdxf
    doc=ezdxf.new('R2013');doc.units=6;doc.header['$MEASUREMENT']=1;doc.appids.new('TCC_R158')
    ms=doc.modelspace()
    for name,color in [('TCC_R158_ACABADO',3),('TCC_R158_CONCRETO_TOPO',8),('TCC_R158_APOIOS',2),('TCC_R158_REVISADOS',4),('TCC_R158_AVISO',1)]:doc.layers.new(name,dxfattribs={'color':color})
    faces=[]
    for key,layer in [('finishedSurfaces','TCC_R158_ACABADO'),('concreteTopSurfaces','TCC_R158_CONCRETO_TOPO')]:
        for i,f in enumerate(d[key]):faces.append(dict(id=f'{key}-{i}',layer=layer,vertices=f['vertices']))
    for key,layer in [('addedElements','TCC_R158_APOIOS'),('changedExistingElements','TCC_R158_REVISADOS')]:
        for e in d[key]:
            for i,f in enumerate(box_faces(e)):faces.append(dict(id=e['id']+f'-face{i}',layer=layer,vertices=f))
    for f in faces:
        entity=ms.add_3dface(f['vertices'],dxfattribs={'layer':f['layer']});entity.set_xdata('TCC_R158',[(1000,f['id']),(1000,'CANDIDATO - NAO EXECUTAR')])
    ms.add_text('R158 - CANDIDATO PARCIAL ESCADA/APOIOS - SEM CALCULO - NAO EXECUTAR',dxfattribs={'height':.10,'insert':(4.2,4.5,0),'layer':'TCC_R158_AVISO'})
    path=OUT/'R158-escada-apoios-CANDIDATO.dxf';doc.saveas(path)
    checked=ezdxf.readfile(path);audit=checked.audit();assert not audit.has_errors and len(checked.modelspace().query('3DFACE'))==96
    (OUT/'R158-dxf-gerado.json').write_text(json.dumps(dict(faceCount=len(faces),parser='ezdxf',version=ezdxf.__version__,units=checked.units,errors=len(audit.errors),nativeAutoCadOpened=False,representsCompleteStructuralBuilding=False,noClosedWaistVolume=True,faces=faces),ensure_ascii=False,indent=2),encoding='utf-8')

def plot(d):
    sys.path.insert(0,'D:/TCC/work/plot-deps');import matplotlib
    matplotlib.use('Agg');import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig,(ax,bx)=plt.subplots(1,2,figsize=(13,7))
    for f in d['finishedSurfaces']:
        if f['kind'] not in ('tread','landing'):continue
        v=f['vertices']+[f['vertices'][0]];ax.plot([p[0] for p in v],[p[1] for p in v],c='#26705e',lw=1)
    for e in d['addedElements']+d['changedExistingElements']:
        b=bounds(e);ax.add_patch(Rectangle((b[0],b[1]),b[3]-b[0],b[4]-b[1],color='#e4b658' if e in d['addedElements'] else '#7ea4bf',alpha=.55))
        ax.text((b[0]+b[3])/2,(b[1]+b[4])/2,e['id'],fontsize=7,rotation=90 if e['kind']=='column' else 0,ha='center',va='center')
    b=d['windowJ4BoxInterpretedM'];ax.plot([b[0],b[3]],[0,0],color='#2d9abc',lw=5,label='J4: manter livre')
    ax.set(xlim=(4.1,6.85),ylim=(-.15,4.05),aspect='equal',xlabel='X local (m)',ylabel='Y local (m)',title='Candidato: pilares laterais e apoio interno')
    ax.legend(loc='upper left',fontsize=8);ax.grid(alpha=.15)
    arr=[f for f in d['finishedSurfaces'] if f['kind']=='tread' and f['number']>=10]
    for f in arr:
        ys=[p[1] for p in f['vertices']];z=f['vertices'][0][2]
        bx.plot([min(ys),max(ys)],[z,z],color='#26705e',lw=2)
        bx.plot([min(ys),max(ys)],[z-.05,z-.05],color='#ba762d',lw=2)
    for e in d['changedExistingElements']:
        b=bounds(e);bx.add_patch(Rectangle((b[1],b[2]),b[4]-b[1],b[5]-b[2],color='#7ea4bf',alpha=.55))
    bx.axhline(3.25,c='#26705e',ls='--',label='Piso acabado +3,25')
    bx.axhline(3.20,c='#ba762d',ls=':',label='Concreto +3,20')
    bx.set(xlim=(2.1,3.35),ylim=(2.6,3.45),xlabel='Y local (m)',ylabel='Cota (m)',title='Chegada: acabamento hipotético de 5 cm')
    bx.text(2.12,2.63,'Fundo da escada e ancoragem ainda não verificados',fontsize=8)
    bx.legend(loc='upper left',fontsize=8);bx.grid(alpha=.15)
    fig.suptitle('H03/R158 — 17 espelhos (9 + 8): candidato comum CAD/BIM\nNão implantado no receptor; não dimensionado',fontsize=14)
    fig.text(.5,.02,'Faixas nominais de 90 cm antes de guardas | Novos pilares 20x30 e vigas são hipóteses | NÃO EXECUTAR',ha='center',fontsize=10)
    fig.tight_layout(rect=(0,.05,1,.91));fig.savefig(OUT/'R158-candidato-comum.png',dpi=160);plt.close(fig)

def main():
    tick=perf_counter();start=datetime.now(timezone.utc).isoformat()
    if OUT.exists():raise FileExistsError(OUT)
    sources=[dict(path=str(p),sha256=sha(p)) for p in (PROPOSAL,PLAN,REF,PDF)]
    d=build(json.loads(PROPOSAL.read_text(encoding='utf-8')),json.loads(PLAN.read_text(encoding='utf-8')),json.loads(REF.read_text(encoding='utf-8')))
    assert d['proposedElementCount']==65 and not d['newColumnDoorPlanIntersections']
    d.update(createdAtUtc=datetime.now(timezone.utc).isoformat(),sources=sources,
        officialSources=['https://suporte.altoqi.com.br/hc/pt-br/articles/115004562614','https://suporte.altoqi.com.br/hc/pt-br/articles/115002281074','https://suporte.altoqi.com.br/hc/pt-br/articles/360000143334'])
    OUT.mkdir();(OUT/'R158-candidato-comum.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    export(d);plot(d)
    assert all(sha(Path(r['path']))==r['sha256'] for r in sources)
    (OUT/'R158-tempo-script.json').write_text(json.dumps(dict(startUtc=start,endUtc=datetime.now(timezone.utc).isoformat(),durationMs=(perf_counter()-tick)*1000,isFlowTimeOrWholeAiEffort=False),indent=2),encoding='utf-8')
    archive();print(json.dumps(dict(nominalHorizontalSurfaceOverlaps=len(d['nominalHorizontalSurfaceOverlaps']),elements=65,facadeBeamRejected=True,newColumnOpeningHits=0,nativePlacement=False)))

def archive():
    shutil.copyfile(HERE/'LEIA-ME-R158.md',OUT/'LEIA-ME-R158.md')
    for p in OUT.iterdir():
        if p.is_file() and p.suffix.lower() in ('.json','.png','.txt','.dxf') and 'manifesto' not in p.name:shutil.copyfile(p,HERE/p.name)
    (HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    m=[dict(path=p.name,sha256=sha(p)) for p in sorted(HERE.iterdir()) if p.is_file() and 'manifesto' not in p.name]
    for folder in (OUT,HERE):(folder/'R158-manifesto.json').write_text(json.dumps(m,indent=2),encoding='utf-8')

if __name__=='__main__':main()

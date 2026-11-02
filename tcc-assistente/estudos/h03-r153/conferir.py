"""Conferência 9+8: geometria acabada e triagem condicional, sem dimensionamento."""
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
OUT=Path('D:/TCC/outputs/Escada-H03-R153-17-9MAIS8-NAO-EXECUTAR')
CURRENT=Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
spec=importlib.util.spec_from_file_location('r144',HERE.parent/'h03-r144/estudar_escada.py')
r144=importlib.util.module_from_spec(spec);spec.loader.exec_module(r144)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def build(ref,m):
    a=r144.alternative(17,9);scale=ref['coordinateSystem']['pdfUnitsPerM'];origin=ref['coordinateSystem']['upperOriginPdf']
    xl=(801.84-origin['x'])/scale;xr=(915.36-origin['x'])/scale;w=m['flightStripWidth']
    south=(origin['y']-1494.80)/scale;land_n=south+m['landingDepth']
    upper_arrival=land_n+a['upperTreadRunM'];lower_start=land_n+a['lowerTreadRunM']
    # Hipótese explícita de sentido: inferior à esquerda, superior à direita.
    faces=[];treads=[];risers=[];e=a['uniformRiserM'];p=a['treadHypothesisM']
    for i in range(1,10):
        y=lower_start-(i-1)*p;z=.22+i*e;z0=.22+(i-1)*e
        risers.append(dict(number=i,flight='lower',yM=y,zTopM=z))
        faces.append(dict(kind='riser',number=i,vertices=[[xl,y,z0],[xl+w,y,z0],[xl+w,y,z],[xl,y,z]]))
        if i<9:
            tread=dict(number=i,flight='lower',yMinM=y-p,yMaxM=y,zM=z)
            treads.append(tread);faces.append(dict(kind='tread',number=i,vertices=[[xl,y-p,z],[xl+w,y-p,z],[xl+w,y,z],[xl,y,z]]))
    z=a['proposedFinishedLandingM']
    faces.append(dict(kind='landing',vertices=[[xl,south,z],[xr,south,z],[xr,land_n,z],[xl,land_n,z]]))
    for j in range(1,9):
        i=9+j;y=land_n+(j-1)*p;z=.22+i*e;z0=.22+(i-1)*e
        risers.append(dict(number=i,flight='upper',yM=y,zTopM=z))
        faces.append(dict(kind='riser',number=i,vertices=[[xr-w,y,z0],[xr,y,z0],[xr,y,z],[xr-w,y,z]]))
        if j<8:
            treads.append(dict(number=i,flight='upper',yMinM=y,yMaxM=y+p,zM=z))
            faces.append(dict(kind='tread',number=i,vertices=[[xr-w,y,z],[xr,y,z],[xr,y+p,z],[xr-w,y+p,z]]))
    return dict(geometry=a,clearEnvelope=dict(xMinM=xl,xMaxM=xr,ySouthM=south,landingNorthM=land_n,
        upperArrivalYM=upper_arrival,lowerStartYM=lower_start,flightWidthGraphicalM=w,
        upperArrivalReferenceYM=(origin['y']-1332.56)/scale),
        planSenseHypothesis='Lance inferior à esquerda desce em Y ao subir; superior à direita sobe em Y. Hipótese de redesenho explícita, não reprodução automática de setas contraditórias entre plantas.',
        finishedSurfaceFaces=faces,treads=treads,risers=risers,
        noWaistThicknessOrVolume=True,loadApplied=False,nativeModelsEdited=False)

def headroom(treads,opening_edge,soffit,tolerance=.05):
    # Tol. representa incerteza de triagem da borda, não tolerância de execução.
    under=[t for t in treads if t['flight']=='lower' and t['yMaxM']>=opening_edge-tolerance]
    if not under:raise ValueError('Sem sobreposição para a hipótese')
    rows=[dict(tread=t['number'],clearanceM=soffit-t['zM']) for t in under]
    return dict(openingEdgeYM=opening_edge,soffitAssumedM=soffit,edgeUncertaintyM=tolerance,
        overlappedTreads=rows,minimumConditionalClearanceM=min(x['clearanceM'] for x in rows),
        actual3DObstructionSurveyOrComplianceVerified=False)

def main():
    if OUT.exists():raise FileExistsError(OUT)
    tick=perf_counter();start=datetime.now(timezone.utc).isoformat()
    sources=[HERE.parent/'h03-r147/R147-planta.json',HERE.parent/'h03-r68/R68-referencia-arquitetonica-estudo.json',
             HERE.parent/'h03-r152/R152-escada17.json',HERE.parent/'h03-r145/R145-resultado.json']
    base,ref=json.loads(sources[0].read_text(encoding='utf-8')),json.loads(sources[1].read_text(encoding='utf-8'))
    m=base['graphicalMeasurementsM'];d=build(ref,m);env=d['clearEnvelope']
    sg=next(f for f in ref['floors'] if f['id']=='S');tg=next(f for f in ref['floors'] if f['id']=='T')
    p3=next(o for o in sg['openings'] if o['id']=='S-P3-01');tp2=next(o for o in tg['openings'] if o['id']=='T-P2-01')
    d.update(revision='H03/R153',createdAtUtc=datetime.now(timezone.utc).isoformat(),
        sources=[dict(path=str(p),sha256=sha(p)) for p in sources],
        userScope='Continuação da escolha de17; distribuição9+8 estudada para preservar paredes/portas e chegada superior.',
        fitScreening=dict(upperHallDepthGraphicallyPreservedM=m['hallDepth'],landingDepthGraphicallyPreservedM=m['landingDepth'],
            upperArrivalToP3OpeningStartGapM=min(p3['y'],p3['y2'])-env['upperArrivalYM'],
            lowerFirstRiserToGroundP2OpeningStartGapM=min(tp2['y'],tp2['y2'])-env['lowerStartYM'],
            doorScreeningMeans='Distâncias longitudinais, sem simulação de folhas, guardas, mobiliário ou largura de circulação.',
            groundApproachClosedHallDepthNotInferred=True,
            groundLowerFlightStartsBeyondOldOpeningByM=env['lowerStartYM']-env['upperArrivalReferenceYM'],
            detailedCirculationApproved=False),
        headroomScenarios=[headroom(d['treads'],env['upperArrivalReferenceYM'],s) for s in (3.02,3.06,2.75)],
        headroomAssumptions=dict(ceilingPlaneM=3.02,ceilingBasis='Piso térreo acabado+.22 e pé-direito arquitetônico2.80, leitura visual corteAA.',
            slabUndersideScenarioM=3.06,slabBasis='PlanoN1+3.20 menos espessura14cm registrada em L5/R145; não levantamento físico da borda.',
            beamUndersideSensitivityM=2.75,beamBasis='Sensibilidade a altura45cm sob plano3.20; não afirma viga existente nesta posição.',
            clearanceBenchmarkM=2.10,benchmarkStatus='Triagem geométrica, não declaração de enquadramento normativo.',
            excluded=['obstruções locais reais','inclinação de forro','guarda/corrimão','toda a circulação sob patamar','faces/espessuras finais de apoio']),
        preferredGeometricCandidateForNextChecks=True,finalStructuralOrNormativeApproval=False,
        comparisonProtocol='Mesma geometria deverá alimentar ambos os fluxos; esta revisão não é ensaio de importação nem ranking temporal.')
    OUT.mkdir();(OUT/'R153-geometria9mais8.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    export_dxf(d);plot(d,ref,m)
    for row in d['sources']:assert sha(Path(row['path']))==row['sha256']
    shutil.copyfile(CURRENT,OUT/'R153-definicao-anterior.json')
    CURRENT.write_text(json.dumps(dict(activeRevision='H03/R153',activeChoice='17 espelhos; candidato geométrico9+8, U com patamar',
        definitionPath=str(OUT/'R153-geometria9mais8.json'),definitionSha256=sha(OUT/'R153-geometria9mais8.json'),
        previousDefinitionPreservedAt=str(OUT/'R153-definicao-anterior.json'),
        nativePlacementResolved=False,nativeProjectsUpdated=False,finalApproval=False),ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'R153-tempo-script.json').write_text(json.dumps(dict(startUtc=start,endUtc=datetime.now(timezone.utc).isoformat(),
        durationMs=(perf_counter()-tick)*1000,scope='cálculo/exportação/render inicial; não esforço total de IA ou tempo de fluxo'),ensure_ascii=False,indent=2),encoding='utf-8')
    archive()
    print(json.dumps(dict(landing=d['geometry']['proposedFinishedLandingM'],fit=d['fitScreening'],
        headroomMinima=[r['minimumConditionalClearanceM'] for r in d['headroomScenarios']])))

def export_dxf(d):
    sys.path.insert(0,'D:/TCC/work/dxf-deps');import ezdxf
    doc=ezdxf.new('R2013');doc.units=6;doc.header['$MEASUREMENT']=1
    for name,color in [('TCC_PISADAS_ESTUDO',3),('TCC_ESPELHOS_ESTUDO',4),('TCC_PATAMAR_ESTUDO',2),('TCC_AVISO',1)]:doc.layers.new(name,dxfattribs={'color':color})
    ms=doc.modelspace()
    layers={'tread':'TCC_PISADAS_ESTUDO','riser':'TCC_ESPELHOS_ESTUDO','landing':'TCC_PATAMAR_ESTUDO'}
    for f in d['finishedSurfaceFaces']:ms.add_3dface(f['vertices'],dxfattribs={'layer':layers[f['kind']]})
    ms.add_text('17 ESPELHOS 9+8 - SUPERFICIES ACABADAS - SEM ESPESSURA - NAO EXECUTAR',dxfattribs={'height':.09,'insert':(4.45,4.6,0),'layer':'TCC_AVISO'})
    path=OUT/'R153-escada17-superficies3D.dxf';doc.saveas(path)
    reread=ezdxf.readfile(path);audit=reread.audit()
    count=len(reread.modelspace().query('3DFACE'))
    assert not audit.has_errors and count==33
    (OUT/'R153-auditoria-dxf.json').write_text(json.dumps(dict(parser='ezdxf',version=ezdxf.__version__,faces=count,
        nativeAutoCadOpened=False,errors=len(audit.errors),fixes=len(audit.fixes),units=reread.units,sha256=sha(path)),indent=2),encoding='utf-8')

def plot(d,ref,m):
    sys.path.insert(0,'D:/TCC/work/plot-deps');import matplotlib
    matplotlib.use('Agg');import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig=plt.figure(figsize=(14,8),facecolor='#f3f6f8');fig.suptitle('Escada de 17 espelhos: candidato com 9 no primeiro lance e 8 no segundo',fontsize=17,x=.5,y=.97)
    ax=fig.add_subplot(121);env=d['clearEnvelope'];xl=env['xMinM'];xr=env['xMaxM'];yn=env['landingNorthM'];ys=env['ySouthM'];w=env['flightWidthGraphicalM']
    ax.add_patch(Rectangle((xl,ys),xr-xl,m['landingDepth'],facecolor='#ffe7ba',edgecolor='#906f39'))
    for t in d['treads']:
        x=xl if t['flight']=='lower' else xr-w
        ax.add_patch(Rectangle((x,t['yMinM']),w,t['yMaxM']-t['yMinM'],facecolor='#d9eee7' if t['flight']=='lower' else '#dce8f4',edgecolor='#355f6b',linewidth=.8))
        ax.text(x+w/2,(t['yMinM']+t['yMaxM'])/2,str(t['number']),ha='center',va='center',fontsize=8)
    edge=env['upperArrivalReferenceYM'];ax.axhline(edge,color='#ac602f',linestyle='--',linewidth=1)
    ax.text(xr+.08,edge-.02,'Chegada superior\nna posição gráfica original',fontsize=9,va='top')
    for fl,oid,color in [('S','S-P3-01','#c64242'),('T','T-P2-01','#864696')]:
        o=next(o for f in ref['floors'] if f['id']==fl for o in f['openings'] if o['id']==oid)
        ax.plot([o['x'],o['x2']],[o['y'],o['y2']],color=color,linewidth=4)
        ax.text(o['x']+(.08 if fl=='S' else -.08),(o['y']+o['y2'])/2,oid,fontsize=9,rotation=90,ha='left' if fl=='S' else 'right')
    ax.text((xl+xr)/2,ys+.43,f"Patamar acabado\n+{d['geometry']['proposedFinishedLandingM']:.3f} m",ha='center',fontsize=11)
    ax.annotate('',xy=(xl+.75*w,1.15),xytext=(xl+.75*w,3.02),arrowprops={'arrowstyle':'->','color':'#16785f','lw':2})
    ax.annotate('',xy=(xr-.15*w,2.75),xytext=(xr-.15*w,1.2),arrowprops={'arrowstyle':'->','color':'#275e92','lw':2})
    ax.set(xlim=(4.1,7.6),ylim=(-.1,4.85),aspect='equal',xlabel='X local (m)',ylabel='Y local (m)',title='Plantas sobrepostas para triagem; setas indicam subida')
    ax.grid(alpha=.15)
    bx=fig.add_subplot(122,projection='3d');colors={'tread':'#5aa68e','riser':'#a4cebe','landing':'#eac782'}
    for kind in colors:
        polys=[f['vertices'] for f in d['finishedSurfaceFaces'] if f['kind']==kind]
        bx.add_collection3d(Poly3DCollection(polys,facecolors=colors[kind],edgecolors='#315b58',linewidths=.6,alpha=.98))
    bx.set(xlim=(xl-.1,xr+.1),ylim=(ys-.1,3.5),zlim=(0,3.5),xlabel='X (m)',ylabel='Y (m)',zlabel='Cota acabada (m)',title='Superfícies acabadas; sem espessura resistente')
    bx.view_init(elev=55,azim=135);bx.set_box_aspect((2,3.5,3.5))
    bx.set_xticks([4.5,5.5,6.5]);bx.set_yticks([0,1,2,3]);bx.set_zticks([0,1,2,3])
    fig.text(.04,.075,'17 espelhos iguais de 17,8235 cm | pisadas de 28 cm | patamar +1,8241 m',fontsize=12,weight='bold')
    fig.text(.04,.042,'Encaixe e altura livre em triagem. Guardas, corrimãos, apoios e dimensionamento pendentes. NÃO EXECUTAR.',fontsize=11,color='#98431d')
    fig.subplots_adjust(left=.06,right=.95,bottom=.15,top=.88,wspace=.24)
    fig.savefig(OUT/'R153-planta-e-superficies.png',dpi=150);plt.close(fig)

def archive():
    for p in OUT.iterdir():
        if p.is_file() and p.suffix.lower() in {'.json','.png','.jpg','.dxf','.svg','.md'} and 'manifesto' not in p.name:shutil.copyfile(p,HERE/p.name)
    shutil.copyfile(HERE/'LEIA-ME-R153.md',OUT/'LEIA-ME-R153.md');(HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    manifest=[dict(path=p.name,sha256=sha(p)) for p in sorted(HERE.iterdir()) if p.is_file() and 'manifesto' not in p.name]
    for folder in (HERE,OUT):(folder/'R153-manifesto.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

if __name__=='__main__':main()

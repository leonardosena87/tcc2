"""Hipótese geométrica independente: U com transição compensada, sem editar modelos."""
import hashlib
import json
import math
import shutil
import sys
from datetime import datetime,timezone
from pathlib import Path
from time import perf_counter

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R151-CAIXA-PRESERVADA-NAO-EXECUTAR')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def rail(radius,a,s):
    if s<=a:return (-radius,a-s)
    if s<=a+math.pi*radius:
        t=math.pi+(s-a)/radius
        return radius*math.cos(t),radius*math.sin(t)
    return radius,s-a-math.pi*radius

def outer_intersection(inner,walk,R,a):
    x,y=inner;dx,dy=walk[0]-x,walk[1]-y
    hits=[]
    if abs(dx)>1e-12:
        for xx in (-R,R):
            t=(xx-x)/dx;yy=y+t*dy
            if t>=1-1e-8 and -1e-8<=yy<=a+1e-8:hits.append((t,(xx,yy)))
    aa=dx*dx+dy*dy;bb=2*(x*dx+y*dy);cc=x*x+y*y-R*R
    det=bb*bb-4*aa*cc
    if det>=0:
        for t in ((-bb-math.sqrt(det))/(2*aa),(-bb+math.sqrt(det))/(2*aa)):
            xx,yy=x+t*dx,y+t*dy
            if t>=1-1e-8 and yy<=1e-8:hits.append((t,(xx,yy)))
    if not hits:raise ValueError('Reta não alcança o contorno externo permitido')
    return min(hits)[1]

def station(radius,a,point):
    x,y=point
    if y>=-1e-9:return a-y if x<0 else a+math.pi*radius+y
    angle=math.atan2(y,x)
    if angle<math.pi:angle+=2*math.pi
    return a+radius*(angle-math.pi)

def candidate(width,flight,a=.77,offset=.50,compensated=11):
    R=width/2;r=R-flight;rw=r+offset
    if not 0<r<rw<R or a<=0:raise ValueError('Contornos inválidos')
    if compensated not in (7,9,11,13,15):raise ValueError('Contagem de transição inválida')
    half=(compensated-1)//2;straight=(17-compensated)//2
    # Um intervalo central e igual número de divisões em cada bordo interno reto.
    inner=[(-r,a-i*a/half) for i in range(half+1)]+[(r,i*a/half) for i in range(half+1)]
    pitch=(2*a+math.pi*rw)/compensated
    walk=[rail(rw,a,i*pitch) for i in range(compensated+1)]
    outer=[outer_intersection(ip,wp,R,a) for ip,wp in zip(inner,walk)]
    outer_s=[station(R,a,q) for q in outer]
    if any(b<=aa for aa,b in zip(outer_s,outer_s[1:])):raise ValueError('Ordem dos espelhos externos invertida')
    edges=[dict(index=i+straight+1,inner=ip,walk=wp,outer=op) for i,(ip,wp,op) in enumerate(zip(inner,walk,outer))]
    inner_chords=[math.dist(x,y) for x,y in zip(inner,inner[1:])]
    walking_chords=[math.dist(x,y) for x,y in zip(walk,walk[1:])]
    return dict(outerRadiusM=R,innerRadiusM=r,walklineRadiusM=rw,
        walklineOffsetFromInnerRailM=offset,transitionStraightExtensionM=a,
        totalRisers=18,totalTreadIntervals=17,lowerStraightTreadIntervals=straight,
        compensatedTreadIntervals=compensated,upperStraightTreadIntervals=straight,
        finishedFloorLevelsM=[.22,3.25],riserM=3.03/18,
        walkingPitchAlongCurveM=pitch,twoRisersPlusPitchM=2*3.03/18+pitch,
        innerBoundaryChordLengthsM=inner_chords,minimumInnerBoundaryChordM=min(inner_chords),
        walkingChordLengthsM=walking_chords,
        contourOrderVerified=True,outerBoundaryStationsM=outer_s,transitionRiserSegments=edges,
        requiredStairLengthM=straight*pitch+a+R,graphicalFlightWidthBeforeHandrailsM=flight,
        headroomVerified=False,openingsAndDoorSwingsVerified=False,
        structuralSupportVerified=False,legalApproval=False,nativeApplied=False)

def main():
    tick=perf_counter();start=datetime.now(timezone.utc).isoformat()
    if OUT.exists():raise FileExistsError(OUT)
    basep=HERE.parent/'h03-r147/R147-planta.json'
    base=json.loads(basep.read_text(encoding='utf-8'));m=base['graphicalMeasurementsM']
    c=candidate(m['stairwellWidth'],m['flightStripWidth'])
    available=m['upperTreadRun']+m['landingDepth']
    c['availableLengthWithoutHallM']=available
    c['southGraphicalReserveM']=available-c['requiredStairLengthM']
    c['envelopeFitsGraphicalBox']=c['southGraphicalReserveM']>=0
    decision=dict(exactText='Preservar as paredes e portas; estudar outra configuração de escada',
        effect='Ampliação R149 descartada para aplicação; estudar compensados dentro da caixa existente.',
        preserves=['paredes','portas','fachada','pisos +0,22 e +3,25','limite norte de chegada desenhado'],
        notAuthorizationForFinalConstruction=True)
    data=dict(revision='H03/R151',createdAtUtc=datetime.now(timezone.utc).isoformat(),userDecision=decision,
        sources=[dict(path=str(basep),sha256=sha(basep))],candidate=c,
        benchmarks=dict(innerBoundaryChordM=.15,walklineOffsetM=.50,
            status='HIPOTESES DE TRIAGEM; não se declara mínimo legal aplicável à escada privada.'),
        referenceUrls=['https://www.pmvc.ba.gov.br/wp-content/uploads/Lei_1481-2007_Anexos.pdf',
            'https://suporte.altoqi.com.br/hc/pt-br/articles/115001824894',
            'https://www.ba.gov.br/bombeiros/normas-tecnicas'],
        limitations=['Contorno curvo reduz área útil nos cantos; guardas e corrimãos não modelados.',
            'Largura gráfica não equivale a largura útil acabada após guardas/corrimãos.',
            'Pisada constante medida por comprimento da linha curva adotada; cordas variam e precisam de conferência normativa.',
            'Não foi resolvida altura livre nem a união à laje/hall e estrutura de apoio.',
            'Não há patamar horizontal em +1,735 m nesta hipótese; não reaproveitar cotas/cargas de R149.',
            'Critérios do anexo municipal para uso coletivo não foram impostos automaticamente à unidade unifamiliar.',
            'Página oficial CBMBA consultada, mas não forneceu texto da instrução aplicável; sem atestado legal.'],
        monographOrAuthoringModelsEdited=False,newLoadsApplied=False,finalApproval=False)
    OUT.mkdir()
    (OUT/'R151-estudo.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    draw(c,m)
    (OUT/'R151-tempo-script.json').write_text(json.dumps(dict(startUtc=start,endUtc=datetime.now(timezone.utc).isoformat(),
        durationMs=(perf_counter()-tick)*1000,notFlowOrWholeAiEffort=True),indent=2),encoding='utf-8')
    print(json.dumps({k:c[k] for k in ['walkingPitchAlongCurveM','minimumInnerBoundaryChordM','requiredStairLengthM','southGraphicalReserveM','envelopeFitsGraphicalBox']}))

def draw(c,m,stem='R151-compensada'):
    R=c['outerRadiusM'];r=c['innerRadiusM'];a=c['transitionStraightExtensionM'];p=c['walkingPitchAlongCurveM']
    straight=c['lowerStraightTreadIntervals'];wind=c['compensatedTreadIntervals']
    k=115;cx=250;top=245;center_y=top+(straight*p+a)*k
    def xy(q):return cx+q[0]*k,center_y-q[1]*k
    def points(qs):return ' '.join(f'{x:.3f},{y:.3f}' for x,y in map(xy,qs))
    s=['<svg xmlns="http://www.w3.org/2000/svg" width="1220" height="790" viewBox="0 0 1220 790">',
       '<rect width="1220" height="790" fill="#f3f6f8"/><g font-family="Arial,sans-serif" fill="#173246">',
       '<text x="28" y="38" font-size="26" font-weight="bold">Escada · hipótese em U com degraus compensados</text>',
       '<text x="28" y="70" font-size="18">18 espelhos · paredes e portas preservadas como restrição · estudo geométrico independente</text>',
       '<rect x="28" y="98" width="445" height="576" rx="12" fill="white" stroke="#c6d3dc"/>']
    stairheight=m['upperTreadRun']+m['landingDepth'];hall=m['hallDepth']
    s += [f'<rect x="{cx-R*k}" y="{top-hall*k}" width="{2*R*k}" height="{hall*k}" fill="#dbe9f3" stroke="#40617a"/>',
          f'<text x="{cx-80}" y="{top-30}" font-size="15">Hall existente</text>',
          f'<rect x="{cx-R*k}" y="{top}" width="{2*R*k}" height="{stairheight*k}" fill="none" stroke="#af5b24" stroke-dasharray="6 4"/>']
    for rad,color in ((R,'#236e67'),(r,'#236e67'),(c['walklineRadiusM'],'#368ac0')):
        qs=[(-rad,a+straight*p),(-rad,a),(-rad,0)]+[(rad*math.cos(math.pi+j*math.pi/80),rad*math.sin(math.pi+j*math.pi/80)) for j in range(81)]+[(rad,a),(rad,a+straight*p)]
        s.append(f'<polyline points="{points(qs)}" fill="none" stroke="{color}" stroke-width="2" '+('stroke-dasharray="5 4"' if color=='#368ac0' else '')+'/>')
    for edge in c['transitionRiserSegments']:
        s.append(f'<polyline points="{points([edge["inner"],edge["outer"]])}" fill="none" stroke="#236e67" stroke-width="1.5"/>')
        x,y=xy(edge['walk']);s.append(f'<text x="{x+5}" y="{y-4}" font-size="11">{edge["index"]}</text>')
    for side in (-1,1):
        for j in range(1,straight+1):
            q=[(side*r,a+j*p),(side*R,a+j*p)]
            s.append(f'<polyline points="{points(q)}" fill="none" stroke="#236e67" stroke-width="1.5"/>')
    s += ['<text x="48" y="628" font-size="14">Contorno laranja: limite gráfico original</text>',
          f'<text x="48" y="651" font-size="14">Azul: percurso adotado a {100*c["walklineOffsetFromInnerRailM"]:.0f} cm do bordo</text>']
    labels=[('Encaixe em planta',f'Caixa disponível: {stairheight:.3f} × {2*R:.3f} m',f'Envoltória proposta: {c["requiredStairLengthM"]:.3f} × {2*R:.3f} m',f'Reserva ao sul: ≈ {100*c["southGraphicalReserveM"]:.1f} cm'),
        ('Distribuição dos degraus',f'{straight} pisadas retas + {wind} compensadas + {straight} retas','17 intervalos de pisada / 18 espelhos','Não há patamar horizontal intermediário'),
        ('Medidas de estudo',f'Espelho: {100*c["riserM"]:.3f} cm',f'Pisada na linha curva: {100*p:.3f} cm',f'Menor corda no bordo interno: {100*c["minimumInnerBoundaryChordM"]:.1f} cm')]
    for i,(title,*lines) in enumerate(labels):
        y=105+i*176;s.append(f'<rect x="500" y="{y}" width="686" height="157" rx="10" fill="white" stroke="#c6d3dc"/>')
        s.append(f'<text x="518" y="{y+28}" font-size="20" font-weight="bold">{title}</text>')
        for j,line in enumerate(lines):s.append(f'<text x="518" y="{y+58+j*29}" font-size="18">{line}</text>')
    s += ['<text x="28" y="716" font-size="21" font-weight="bold" fill="#9f4720">CABE NA ENVOLTÓRIA GRÁFICA · AINDA NÃO APROVADA</text>',
          '<text x="28" y="747" font-size="17">Pendentes: altura livre, largura útil, portas/guardas, critérios aplicáveis, apoios e dimensionamento.</text>',
          '<text x="28" y="775" font-size="16">Nenhuma alteração nos modelos Revit/CAD/Eberick. Não executar.</text></g></svg>']
    raw='\n'.join(s);(OUT/(stem+'.svg')).write_text(raw,encoding='utf-8')
    sys.path.insert(0,'D:/TCC/work/pdf-deps');import pymupdf
    pymupdf.open(stream=raw.encode(),filetype='svg')[0].get_pixmap().save(str(OUT/(stem+'.png')))

def archive():
    for p in OUT.iterdir():
        if p.is_file() and 'manifesto' not in p.name:shutil.copyfile(p,HERE/p.name)
    shutil.copyfile(HERE/'LEIA-ME-R151.md',OUT/'LEIA-ME-R151.md')
    (HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    manifest=[dict(path=p.name,sha256=sha(p)) for p in sorted(HERE.iterdir()) if p.is_file() and 'manifesto' not in p.name]
    for folder in (HERE,OUT):(folder/'R151-manifesto.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

if __name__=='__main__':main();archive()

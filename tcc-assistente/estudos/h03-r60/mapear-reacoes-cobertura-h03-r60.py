"""Arranjo parcial de estudo: reacoes de cobertura, equilibrio e correspondencia CAD/BIM."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,shutil,math,time
sys.path.insert(0,'D:/TCC/work/plot-deps')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
start=time.perf_counter();root=Path('D:/TCC');out=root/'outputs/Cobertura-H03-R60-REACOES-PARCIAIS-NAO-EXECUTAR';out.mkdir(exist_ok=False)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
src=root/'outputs/Cobertura-H03-R59-MEMORIA-ESTUDO-NAO-EXECUTAR';protected=read(src/'R59-manifesto.json')['files']
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
write('R60-protegidos-R59.json',protected)
mem=read(src/'R59-memoria-cobertura.json');g=mem['loads']['roofPermanentHorizontalKNm2'];q=mem['loads']['roofMaintenanceHorizontalKNm2']
geometryPath=root/'outputs/Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR/R56-geometria-exportada.json';geometry=read(geometryPath)
beams={b:[r for r in rows if r['type']=='IfcBeam' and abs(r['max'][2]-6.39)<1e-6] for b,rows in geometry.items()}
vectors=read(root/'work/r60-cobertura-vetores.json')
# Eixos centrais das paredes de 15 cm na planta 1:100, revisados contra os contornos vetoriais.
origin=(2040.48,710.36);scale=72/.0254/100
references=[dict(axis='x',pdf=2226.24,nominalM=6.55),dict(axis='x',pdf=2314.08,nominalM=9.65),dict(axis='x',pdf=2342.4,nominalM=10.65),dict(axis='y',pdf=599.84,nominalM=3.9),dict(axis='y',pdf=510.56,nominalM=7.05)]
for r in references:
 r['measuredM']=(r['pdf']-origin[0])/scale if r['axis']=='x' else (origin[1]-r['pdf'])/scale
 r['residualM']=r['measuredM']-r['nominalM'];assert abs(r['residualM'])<.005
planes=[dict(id='A1',name='Agua inferior esquerda',box=[0,0,6.55,3.9],slopeDirection=[0,-1],status='Arranjo metalico hipotetico e reacoes calculadas nesta R60'),dict(id='A2',name='Agua superior sobre corpo principal',box=[0,3.9,9.65,7.05],slopeDirection=[0,1],status='Parcela parcial da agua superior; exclui avanco da varanda'),dict(id='P1',name='Avanco da agua superior sobre varanda',box=[9.65,3.9,10.65,7.05],slopeDirection=[0,1],status='Pendente: sem viga N2 sob borda externa; projetar suporte/balanco e ligacoes'),dict(id='P2',name='Agua elevada do abrigo do reservatorio',box=[6.55,0,9.65,3.9],slopeDirection=[-1,0],status='Pendente: cotas, abrigo, caminho das reacoes e apoio do tanque')]
for p in planes:p['nominalProjectedAreaM2']=(p['box'][2]-p['box'][0])*(p['box'][3]-p['box'][1])
rafters=[];nodeMap={}
for plane,xcuts,ys in [('A1',[0,2.2,4.4,6.55],[0,3.9]),('A2',[0,2.2,4.4,6.55,8.1,9.65],[3.9,7.05])]:
 for i,(a,b) in enumerate(zip(xcuts,xcuts[1:]),1):
  x=(a+b)/2;width=b-a;span=ys[1]-ys[0];area=width*span;ident=f'{plane}-M{i:02}'
  r=dict(id=ident,plane=plane,xM=x,yStartM=ys[0],yEndM=ys[1],tributaryX=[a,b],tributaryWidthM=width,horizontalSpanM=span,inclinedSpanM=span*math.sqrt(1.01),tributaryProjectedAreaM2=area,gTotalKN=g*area,qTotalKN=q*area,gEachEndKN=g*area/2,qEachEndKN=q*area/2,model='Barra metalica inclinada biapoiada, carga vertical uniforme em projecao horizontal, sem empuxo horizontal idealizado',designVerified=False)
  rafters.append(r)
  for y in ys:
   k=(round(x,6),y);n=nodeMap.setdefault(k,dict(xM=x,yM=y,zConcreteBeamTopM=6.39,gDownKN=0,qRoofDownKN=0,sourceRafters=[]))
   n['gDownKN']+=r['gEachEndKN'];n['qRoofDownKN']+=r['qEachEndKN'];n['sourceRafters'].append(ident)
nodes=[]
for i,(key,n) in enumerate(sorted(nodeMap.items(),key=lambda kv:(kv[0][1],kv[0][0])),1):
 n['id']=f'RC{i:02}';n['nativeTargets']={}
 for branch,rows in beams.items():
  matches=[r for r in rows if r['min'][0]-1e-6<n['xM']<r['max'][0]+1e-6 and r['min'][1]-1e-6<n['yM']<r['max'][1]+1e-6]
  assert len(matches)==1,(branch,n,matches)
  r=matches[0];n['nativeTargets'][branch]=dict(name=r['name'],guid=r['guid'],min=r['min'],max=r['max'])
 assert n['nativeTargets']['CAD']['min']==n['nativeTargets']['BIM']['min']
 assert n['nativeTargets']['CAD']['max']==n['nativeTargets']['BIM']['max']
 n['appliedToNative']=False;n['forceZConventionKN']=-n['gDownKN'];nodes.append(n)
assert len(rafters)==8 and len(nodes)==13
partialArea=sum(p['nominalProjectedAreaM2'] for p in planes[:2]);pendingArea=sum(p['nominalProjectedAreaM2'] for p in planes[2:])
for action,load in [('gDownKN',g),('qRoofDownKN',q)]:assert abs(sum(n[action] for n in nodes)-load*partialArea)<1e-10
# Equilibrio global de momento das reacoes verticais, em relacao a x e y.
for action,load in [('gDownKN',g),('qRoofDownKN',q)]:
 for coord,indices in [('xM',(0,2)),('yM',(1,3))]:
  target=sum(p['nominalProjectedAreaM2']*load*(p['box'][indices[0]]+p['box'][indices[1]])/2 for p in planes[:2])
  assert abs(sum(n[action]*n[coord] for n in nodes)-target)<1e-9
purlins=[dict(plane='A1',yRowsM=[0,1.3,2.6,3.9],maxSheetSpanAlongSlopeM=1.3*math.sqrt(1.01)),dict(plane='A2',yRowsM=[3.9,5.475,7.05],maxSheetSpanAlongSlopeM=1.575*math.sqrt(1.01))]
data=dict(revision='H03/R60',atUtc=datetime.now(timezone.utc).isoformat(),scope='Arranjo de estudo e mapa parcial de reacoes, sem dimensionamento metalico ou lancamento nativo',geometrySource=dict(path=str(geometryPath),sha256=sha(geometryPath),meaning='Geometria R56 conferida em R57 antes do processamento R58; nao nova exportacao R60'),roofCalibration=dict(originPdfTopLeftCoordinates=origin,pointsPerMeter=scale,sourceScale='1:100',references=references,method='Eixos nominais de paredes identificados visualmente entre contornos PDF; calibracao da escala nao torna cotas ausentes em cotas executivas'),planes=planes,roofPlanesAreNominalAxisAreas=True,netSheetAreaClaimed=False,partialProjectedAreaM2=partialArea,pendingProjectedAreaM2=pendingArea,gHorizontalKNm2=g,qRoofHorizontalKNm2=q,rafters=rafters,purlins=purlins,reactionNodes=nodes,equilibrium=dict(verticalGKN=sum(n['gDownKN'] for n in nodes),verticalQRoofKN=sum(n['qRoofDownKN'] for n in nodes),verticalAndFirstMomentsPassed=True),partialCoverageOnly=True,pointReactionsAreProposedNotMeasured=True,metalMembersSized=False,steelWeightAllowanceStillHypothesis=True,roofVariableSimultaneityWithSlabUnresolved=True,nativeModelsEdited=False,excluded=['Varanda P1','Abrigo elevado P2','Policarbonato','Platibandas/calhas/arremates ainda nao quantificados','Reservatorio 1000 L, tara, base e apoio','Vento, succao, ancoragens e combinacoes'],pending=['Definir apoios elevados com articulacao/deslizamento e contraventamento para a hipotese sem empuxo horizontal.','Conferir altimetria e espaco dos perfis sob o telhado, preservando a arquitetura.','Dimensionar metal/ancoragens e avaliar efeitos locais nas vigas de concreto.','Nao equiparar area nominal por eixos a quantidade liquida de telhas.','Tratar P1/P2 separadamente e completar acoes antes da verificacao ELU/ELS.'])
write('R60-arranjo-reacoes.json',data)
# Fonte vetorial reduzida: somente contornos de referencia, sem reproduzir prancha/norma.
selected=[o for o in vectors if o['color']==[0,0,0] and ((o['x0'] in (2038.32,2042.64,2224.08,2228.4,2311.92,2316.24,2340.24,2344.56)) and (o['x1']-o['x0']>45 or o['bottom']-o['top']>35))]
write('R60-contornos-PDF-referencia.json',selected)
fig,ax=plt.subplots(figsize=(12,8.7));colors=['#d9eef7','#def1e0','#fce4bf','#f5d4d4']
for p,c in zip(planes,colors):
 x,y,x2,y2=p['box'];ax.add_patch(Rectangle((x,y),x2-x,y2-y,facecolor=c,edgecolor='#4b5563',lw=1.2))
 ax.text((x+x2)/2,(y+y2)/2,p['id'],fontsize=16,ha='center',va='center',alpha=.65)
for b in beams['CAD']:
 a=b['min'];z=b['max'];ax.add_patch(Rectangle((a[0],a[1]),z[0]-a[0],z[1]-a[1],facecolor='#576574',alpha=.65))
for r in rafters:ax.plot([r['xM']]*2,[r['yStartM'],r['yEndM']],color='#226797',lw=1.6)
for p in purlins:
 xmax=6.55 if p['plane']=='A1' else 9.65
 for y in p['yRowsM']:ax.plot([0,xmax],[y,y],color='#508b7c',ls=':',lw=1)
for n in nodes:
 ax.plot(n['xM'],n['yM'],'o',color='#a12f24',ms=5)
 ax.annotate(n['id'],(n['xM'],n['yM']),xytext=(4,5),textcoords='offset points',fontsize=8)
ax.set(xlim=(-.4,11.2),ylim=(-.5,7.7),xlabel='X nominal H03 (m)',ylabel='Y nominal H03 (m)');ax.set_aspect('equal');ax.grid(alpha=.15)
ax.set_title('H03/R60 - arranjo parcial proposto e pontos de reacao\nESTUDO NAO DIMENSIONADO - NAO EXECUTAR',loc='left',fontsize=13)
fig.text(.12,.12,'A1: inferior esquerda; A2: superior sobre corpo principal.\nP1: avanco sobre varanda sem suporte definido; P2: abrigo elevado do tanque.\nAzul: 8 barras metalicas propostas; pontos vermelhos: 13 reacoes agregadas em vigas N2.\nSem vento, dimensionamento ou cargas do tanque. Areas por eixos; nao sao telhas liquidas.',fontsize=9)
fig.subplots_adjust(bottom=.24,top=.89)
fig.savefig(out/'R60-arranjo-reacoes.png',dpi=150);fig.savefig(out/'R60-arranjo-reacoes.svg');plt.close(fig)
svg=out/'R60-arranjo-reacoes.svg';svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
table='\n'.join(f"| {n['id']} | {n['xM']:.3f}; {n['yM']:.3f} | {n['gDownKN']:.6f} | {n['qRoofDownKN']:.6f} | {n['nativeTargets']['CAD']['name']} | {n['nativeTargets']['BIM']['name']} |" for n in nodes)
report=f'''# H03/R60 - arranjo proposto e reacoes parciais da cobertura

ESTUDO NAO DIMENSIONADO - NAO EXECUTAR. Esta etapa define um caminho gravitacional de estudo para duas regioes da cobertura. Nao alterou PRJ/RVT/DWG ou monografia e nao aplicou cargas automaticamente. Usa g={g:.9f} kN/m2 e q_telhado={q:.2f} kN/m2 da R59; a reserva metalica de 0,15 kN/m2 continua sem levantamento de perfis.

## Leitura geometrica e limites

Revisaram-se a prancha completa, o recorte da planta de cobertura e os contornos vetoriais do PDF. A origem PDF (2040,48;710,36), coordenadas com Y para baixo, foi associada ao encontro nominal (0;0) da H03. Escala 1:100: {scale:.9f} pontos/m. Compararam-se cinco eixos de referencia (x6,55/x9,65/x10,65/y3,90/y7,05); residuos inferiores a 5 mm. Trata-se de leitura nominal por eixos centrais de paredes de 15 cm, nao levantamento executivo de faces/beirais/calhas. As areas seguintes sao idealizadas por esses eixos, sem desconto de arremates ou acrescimos de recobrimento.

A1 ocupa x0..6,55/y0..3,90, caimento -Y; A2 ocupa x0..9,65/y3,90..7,05, caimento +Y. Area parcial nominal={partialArea:.6f} m2. A agua superior se prolonga ate x10,65 sobre a varanda: P1 possui 3,15 m2 nominais e nao possui viga N2 na borda externa nesse conjunto exportado. O abrigo elevado P2 ocupa x6,55..9,65/y0..3,90, 12,09 m2 nominais, caimento -X. P1 e P2 ({pendingArea:.6f} m2 nominais) permanecem SEM reacoes nativas definidas; cargas desconhecidas nao foram substituidas por zero. Tambem nao se incluiu o policarbonato.

## Hipotese de caminho gravitacional

Propoem-se 3 barras metalicas biapoiadas no sentido Y em A1, e 5 em A2. Cada barra fica no meio da propria faixa tributaria em X, com faixas explicitamente definidas no JSON. A faixa inferior tem vao horizontal3,90m e a superior3,15m; larguras tributarias entre1,55 e2,20m. Terças propostas em A1 nas ordenadas0/1,30/2,60/3,90; em A2,3,90/5,475/7,05. Os perfis e ligacoes nao foram dimensionados. As alturas dos apoios metalicos e a compatibilidade dos perfis sob os planos de telhado continuam pendentes. Nao se declarou viavel construtivamente esse arranjo.

As barras recebem carga vertical uniforme na projecao horizontal. Pela hipotese de dois apoios, cada extremidade transmite g*b*L/2 e q*b*L/2. Adotou-se ausencia de empuxo horizontal apenas no esquema gravitacional idealizado; isto exige detalhar apoio articulado/deslizante e contraventamento. Vento, succao, excentricidade e ancoragens nao estao nesse calculo. Reacoes no mesmo ponto foram somadas: 8 barras resultam em 13 pontos, todos com correspondencia unica nas caixas de vigas N2 dos ramos CAD e BIM. Isso e correspondencia geometrica, nao validacao das ligacoes analiticas locais.

| Ponto | X;Y (m) | G descendente (kN) | Q do telhado (kN) | Viga CAD | Viga BIM |
|---|---:|---:|---:|---|---|
{table}

Soma G={sum(n['gDownKN'] for n in nodes):.9f} kN; soma Q_telhado={sum(n['qRoofDownKN'] for n in nodes):.9f} kN. Conferiram-se equilibrio vertical e primeiros momentos em X/Y das duas acoes, em relacao as areas tributarias parciais. Isso valida a aritmetica do esquema escolhido, nao sua capacidade resistente. Forcas nodais na convencao Fz positiva para cima devem receber sinal negativo para gravidade; confirmar unidades no dialogo do Eberick instalado antes de lancar. Preservar a identificacao por ponto/coordenada/GUID: os nomes BIM V1/V2 aparecem em mais de um solido.

![Arranjo parcial](R60-arranjo-reacoes.png)

## Aplicacao e continuidade

O mapa e concreto e revisavel para as duas regioes. A aplicacao deve ocorrer em novas copias independentes, com cargas permanentes e variaveis separadas. A simultaneidade com Q_laje=1,00 kN/m2 continua pendente, portanto nao aumentar Q das lajes nem apagar G2_forro=0,25. Registrar cada no/carga introduzido e o tempo, salvar/reabrir e confrontar o acrescimo global com a soma esperada. A discretizacao adicional pertence a mesma concepcao nos dois ramos, sem contar como defeito de transferencia.

O avanco P1 requer suporte/balanco metalico com efeitos locais; o abrigo P2 requer altimetria/apoio independente e nao recebe, por associacao, a carga do reservatorio. Permanecem paredes, platibandas, calhas, tanque1000L/tara/base, escada, bordas, vento/combinacoes e verificacoes ELU/ELS. Preservados os {len(protected)} arquivos protegidos R59. A base limpa segue R57 congelada; R58 conserva o diagnostico parcial. Nao se mediu tempo de autoria CAD/BIM nesta R60: o tempo do script exclui pesquisa, decisao e revisao.
'''
(out/'LEIA-ME-R60.md').write_text(report,encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
write('R60-execucao-script.json',dict(durationMs=(time.perf_counter()-start)*1000,scope='Somente execucao de script; nao esforco total nem tempo comparativo'))
write('R60-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='R60-manifesto.json']))
print(json.dumps(dict(rafters=len(rafters),nodes=len(nodes),partialAreaM2=partialArea,pendingAreaM2=pendingArea,gTotalKN=sum(n['gDownKN'] for n in nodes),qRoofTotalKN=sum(n['qRoofDownKN'] for n in nodes),output=str(out))))

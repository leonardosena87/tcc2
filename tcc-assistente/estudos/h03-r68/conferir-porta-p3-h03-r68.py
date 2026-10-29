"""Confronta S-P3-02 aproximada com vetores da prancha; preserva historico."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter
import sys,json,hashlib,shutil,ast
sys.path.insert(0,'D:/TCC/work/pdf-deps')
import pymupdf as pdf
sys.path.insert(0,'D:/TCC/work/plot-deps')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path('D:/TCC');out=root/'outputs/Compatibilizacao-H03-R68-PORTA-P3-ESTUDO'
dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r68')
assert not out.exists() and not dest.exists()
tick=perf_counter();started=datetime.now(timezone.utc).isoformat()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prior=root/'outputs/Paredes-H03-R67-ABERTURAS-NAO-APLICADO';protected=read(prior/'R67-manifesto.json')['files']
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
arch=root/'PROJETO ARQUITETONICO-A0.pdf';refpath=root/'outputs/Concepcao-H03-R34-ESTUDO-NAO-ADOTADO/R34-referencia-arquitetonica.json'
ref=read(refpath);assert sha(arch)==ref['sourceSha256']
page=pdf.open(arch)[0];crop=pdf.Rect(1035,1255,1115,1335)
lines=[]
for drawing in page.get_drawings():
    if drawing['color']!=(0.,0.,0.):continue
    for item in drawing['items']:
        if item[0]!='l':continue
        a,b=item[1:];r=pdf.Rect(min(a.x,b.x)-.01,min(a.y,b.y)-.01,max(a.x,b.x)+.01,max(a.y,b.y)+.01)
        if r.intersects(crop):lines.append(dict(a=[a.x,a.y],b=[b.x,b.y]))
def line_exists(a,b):return any((all(abs(x-y)<.001 for x,y in zip(l['a']+l['b'],a+b)) or all(abs(x-y)<.001 for x,y in zip(l['a']+l['b'],b+a))) for l in lines)
clearPdf=[1051.44,1085.28];outerPdf=[1049.04,1087.68];y0=1273.52;y1=1282.16
for x in clearPdf+outerPdf:assert line_exists([x,y0],[x,y1]),x
origin=ref['coordinateSystem']['upperOriginPdf']['x'];scale=ref['coordinateSystem']['pdfUnitsPerM']
raw=[(x-origin)/scale for x in clearPdf];outer=[(x-origin)/scale for x in outerPdf]
center=sum(raw)/2;nominal=[center-.30,center+.30]
newref=json.loads(json.dumps(ref))
op=next(o for f in newref['floors'] if f['id']=='S' for o in f['openings'] if o['id']=='S-P3-02')
oldop=json.loads(json.dumps(op))
op.update(x=nominal[0],x2=nominal[1],source='R68: largura nominal0,60m centralizada na abertura vetorial P3 direita da prancha; limites claros PDF1051,44..1085,28pt; eixo nominaly3,90m preservado',coordinateUncertaintyM=.05)
newref.update(scope='Referencia de estudo R68; corrige apenas posicao X da porta S-P3-02. Demais lacunas R34 preservadas; nao arquitetura executiva.',parentReferencePath=str(refpath),parentReferenceSha256=sha(refpath))
geoPath=root/'outputs/Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR/R56-geometria-exportada.json';geo=read(geoPath)
columns={b:[c for c in rr if c['type']=='IfcColumn' and abs(c['max'][2]-6.39)<1e-5 and c['min'][1]<=3.9<=c['max'][1] and c['min'][0]>9] for b,rr in geo.items()}
assert all(len(c)==1 for c in columns.values())
assert columns['CAD'][0]['min']==columns['BIM'][0]['min'] and columns['CAD'][0]['max']==columns['BIM'][0]['max']
col=columns['CAD'][0];left=col['min'][0];right=col['max'][0]
over=lambda ab:max(0,min(ab[1],right)-max(ab[0],left))
gap=left-nominal[1];outergap=left-outer[1]
assert over([oldop['x'],oldop['x2']])>.09 and over(nominal)==0 and gap>.05
out.mkdir()
def write(n,v):(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write('R68-protegidos-R67.json',protected);write('R68-referencia-arquitetonica-estudo.json',newref)
write('R68-vetores-P3.json',dict(source=str(arch),sha256=sha(arch),pageIndex=0,cropPdfPoints=list(crop),coordinateUnits='PDF point; top-left PyMuPDF',selectedBlackLines=lines))
result=dict(revision='H03/R68',atUtc=datetime.now(timezone.utc).isoformat(),openingId='S-P3-02',wallId='W18',pdfClearXPoints=clearPdf,pdfOuterFrameXPoints=outerPdf,originXPdfPoints=origin,pdfPointsPerM=scale,clearRawLocalIntervalM=raw,clearRawWidthM=raw[1]-raw[0],nominalClearWidthM=.60,updatedNominalLocalIntervalM=nominal,oldApproximateIntervalM=[oldop['x'],oldop['x2']],centerCorrectionM=center-(oldop['x']+oldop['x2'])/2,outerFrameLocalIntervalM=outer,columnGeometryByBranch=columns,oldNominalColumnOverlapM=over([oldop['x'],oldop['x2']]),updatedNominalClearOverlapM=over(nominal),updatedClearGapToColumnM=gap,updatedClearGapRangeStudyM=[gap-.05,gap+.05],outerFrameGapToColumnM=outergap,outerFrameGapRangeStudyM=[outergap-.05,outergap+.05],clearOpeningTriagedWithoutOverlap=True,outerFrameStillNeedsFaceCheck=outergap<.05,structuralColumnMoved=False,originalArchitectureEdited=False,geometrySource=dict(path=str(geoPath),sha256=sha(geoPath),revision='R56 geometry preserved in R57; no new R68 export'),nativeRvtDwgPrjEdited=False,loadsApplied=False,fullCompatibilityApproved=False,interpretation='R67 aparente conflito do vao claro decorre da referencia aproximada; contorno externo/folgas e posicoes executivas continuam a conferir')
write('R68-resultado.json',result)
# Esquema derivado dos intervalos, sem copiar a prancha para o repositorio publico.
fig,ax=plt.subplots(figsize=(9.5,4.2));fig.subplots_adjust(left=.25,bottom=.2,top=.80,right=.97)
ax.axvspan(left,right,color='#bdc4cc',alpha=.8,label='Pilar exportado')
series=[('R34/R67: aproximação',[oldop['x'],oldop['x2']],3,'#ba3d35'),('R68: vão claro nominal',nominal,2,'#216d9d'),('R68: contorno externo',outer,1,'#ad7718')]
for label,ab,y,color in series:ax.plot(ab,[y,y],lw=9,color=color,solid_capstyle='butt');ax.text(ab[0]-.02,y,label,ha='right',va='center',fontsize=10)
ax.set_xlim(8.65,9.83);ax.set_ylim(.5,3.5);ax.set_yticks([]);ax.set_xlabel('Coordenada X local (m)');ax.grid(axis='x',alpha=.2);fig.suptitle('Porta P3 direita / W18: revisão da referência em planta',y=.98,fontsize=13)
fig.text(.25,.9,'Triagem de estudo. Não representa tolerância executiva ou aprovação estrutural.',fontsize=9)
ax.legend(loc='lower right',fontsize=9);fig.savefig(out/'R68-intervalos-P3.png',dpi=160);fig.savefig(out/'R68-intervalos-P3.svg');plt.close(fig)
# Recorte original permanece SOMENTE em work, fora do pacote versionado.
page.get_pixmap(matrix=pdf.Matrix(6,6),clip=crop).save(root/'work/r68-P3-direita-conferida.png')
(out/'LEIA-ME-R68.md').write_text(f'''# H03/R68 — conferência vetorial da porta P3 direita

ESTUDO, NÃO EXECUTAR. A sobreposição nominal de10cm indicada na R67 para S-P3-02/W18 foi recalculada após consultar visualmente e extrair os vetores da mesma prancha arquitetônica original. A referência R34 aproximava esse vão por X9,05..9,65m. A conferência mostrou que essa aproximação não deve orientar o deslocamento de um pilar.

Os contornos claros da abertura estão em PDF X1051,44..1085,28pt e os limites externos do conjunto gráfico em1049,04..1087,68pt. As quatro linhas verticais dos dois contornos foram verificadas no arquivo vetorial em Y1273,52..1282,16pt. A transformação usa a origem X{origin:g}pt e escala{scale:.9f}pt/m herdadas R34. O vão claro desenhado mede{raw[1]-raw[0]:.6f}m; essa diferença em relação a0,60m decorre da representação gráfica e não foi tratada como medição executiva.

Adotou-se apenas para a referência de estudo a largura nominal0,60m centralizada no intervalo vetorial, resultando em X{nominal[0]:.6f}..{nominal[1]:.6f}m. A correção do centro é{result['centerCorrectionM']:.6f}m. Preservaram-se Y nominal3,90m, identificador, etiqueta, demais aberturas e margem de posição±0,05m da triagem. Criou-se nova referência R68; R34/R67 e a prancha original não foram substituídas.

O pilar correspondente possui X{left:.2f}..{right:.2f}m, com caixas coincidentes CAD/BIM na geometria exportada R56 e preservada R57. A nova referência de vão claro não o intercepta: folga nominal{gap*100:.2f}cm e faixa de estudo{(gap-.05)*100:.2f}..{(gap+.05)*100:.2f}cm. Isso retira o conflito nominal do vão claro encontrado pela aproximação anterior. Não prova folga executiva do conjunto: o contorno externo chega a{outer[1]:.6f}m, deixando apenas{outergap*100:.2f}cm nominais; com±5cm de posição, essa faixa ainda permite contato. Esquadria, acabamento e faces reais continuam exigindo compatibilização.

![Esquema dos intervalos](R68-intervalos-P3.png)

A figura é um esquema derivado de coordenadas, não cópia nem alteração da prancha. Os vetores selecionados e as transformações acompanham o JSON. O recorte visual original ficou apenas em D:/TCC/work. Não se alterou, deslocou ou dimensionou pilar. A ocorrência é revisão de uma referência interpretada manualmente, sem atribuição a defeito DWG/IFC.

As massas condicionais R67 continuam históricas e não são cargas prontas: a parcela nominal de0,10m de vão que intersectava pilar deve ser recalculada antes de qualquer desconto de alvenaria nessa parede. Para0,60m por2,10m, a diferença potencial na retirada geométrica é0,21m², ou0,32865kN na composição hipotética1,565kN/m²; isso não inclui esquadria/verga nem autoriza aplicação de uma carga. As outras dez aberturas não foram refinadas vetorialmente nesta revisão. S-P3-01/W19 permanece outra porta.

Nenhum PRJ/RVT/DWG ou monografia foi editado. Q do telhado e ajuste dos fatores continuam pendentes na interface. Mantém-se a restrição à superestrutura e a necessidade de fechar cargas/combinações e ELU/ELS. O registro do script é somente duração computacional e não tempo do fluxo ou esforço integral da IA.
''',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name);ast.parse(Path(__file__).read_text(encoding='utf-8'))
write('R68-validacao.json',dict(sourceArchitectureHashPassed=True,selectedVectorEdgesVerified=True,matchingColumnBoxesCADBIM=True,protectedR67FilesChecked=len(protected),nativeFilesEdited=False,startedUtc=started,endUtc=datetime.now(timezone.utc).isoformat(),scriptElapsedSeconds=perf_counter()-tick,scriptDurationIsFlowTime=False))
write('R68-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file()]))
dest.mkdir()
for p in out.iterdir():shutil.copy2(p,dest/p.name);assert sha(p)==sha(dest/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
guide.write_text('''# Atualizacao R68 — referencia da porta P3 direita refinada

Consulta vetorial da prancha corrige S-P3-02/W18 aproximada R34/R67: largura nominal0,60m centralizada no vao claro extraido, sem mover pilar. Ver R68-resultado.json e R68-referencia-arquitetonica-estudo.json em outputs/Compatibilizacao-H03-R68-PORTA-P3-ESTUDO. Vao claro agora sem sobreposicao na triagem; contorno externo e tolerancias ainda exigem conferencia. R67historica com desconto condicional desatualizado nessa parede; nao aplicar. Outros10vaos nao refinados. Nenhum nativo/monografia/original alterado. Nativo final permanece R64, Q_R65 e configuracaoR66 pendentes. NAO EXECUTAR.

---
Historico anterior:

'''+old,encoding='utf-8')
print(json.dumps({k:result[k] for k in ['openingId','updatedNominalLocalIntervalM','centerCorrectionM','updatedClearGapToColumnM','outerFrameGapToColumnM']},ensure_ascii=False))

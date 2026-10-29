"""Figura cientifica de evidencias R72; sem ranking ou tempos inventados."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,sys,ast
sys.path.insert(0,'D:/TCC/work/plot-deps')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
root=Path('D:/TCC');out=root/'outputs/Resultados-H03-R75-FIGURA-PARCIAL'
dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r75')
assert not out.exists() and not dest.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(root/'outputs/Normativa-H03-R74-TRIAGEM-NAO-DIMENSIONADO/R74-manifesto.json')['files']
for p in protected:assert sha(Path(p['path']))==p['sha256'],p['path']
src=root/'outputs/Resultados-H03-R72-PARCIAIS-NAO-FINAIS/R72-resultados-parciais.json';r=read(src)
assert r['initialTypedAggregate']['denominatorLogicalElements']==62 and r['initialTypedAggregate']['BIM_native']==51
assert r['complementedLogicalElements']['CAD']==62 and r['complementedLogicalElements']['BIM']==11
out.mkdir()
fig,ax=plt.subplots(figsize=(13,9.2));fig.patch.set_facecolor('white');ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
blue='#1D4E89';teal='#087F8C';ink='#132D46';gray='#53687B'
def box(x,y,w,h,title,body,color,fs=11):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.012',linewidth=1.3,edgecolor=color,facecolor=color+'0D',zorder=2))
 ax.text(x+w/2,y+h*.74,title,ha='center',va='center',fontsize=12,fontweight='bold',color=color,zorder=3)
 ax.text(x+w/2,y+h*.33,body,ha='center',va='center',fontsize=fs,color=ink,linespacing=1.5,zorder=3)
def arrow(a,b,color=gray):ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=13,linewidth=1.4,color=color,zorder=1))
ax.text(.5,.98,'Dois fluxos automatizados: o que já foi observado',ha='center',va='top',fontsize=18,fontweight='bold',color=ink)
ax.text(.5,.943,'Estudo de caso H03 · resultados exploratórios · sem ranking de produtividade',ha='center',va='top',fontsize=11,color=gray)
box(.235,.825,.53,.085,'Proposta comum — 62 unidades lógicas','22 trechos de pilares + 29 vigas lógicas + 11 lajes',ink)
box(.035,.655,.425,.10,'AutoCAD 2027 → DWG 2D','Representação gráfica gerada por automação',blue)
box(.54,.655,.425,.10,'Revit 2027.2 → IFC adaptado','Tratamento explícito: 17 registros e 2 níveis vazios',teal)
arrow((.36,.813),(.2475,.765),blue);arrow((.64,.813),(.7525,.765),teal)
box(.035,.47,.425,.12,'Chegada CAD ao Eberick — R45','62/62 contornos e 66/66 conteúdos de texto\nSem lançamento estrutural nativo nessa etapa',blue)
box(.54,.47,.425,.12,'Chegada BIM ao Eberick — R46','22/22 trechos de pilares + 29/29 vigas lógicas\n0/11 lajes nativas; 51/62 unidades tipadas',teal)
arrow((.2475,.643),(.2475,.602),blue);arrow((.7525,.643),(.7525,.602),teal)
box(.035,.305,.425,.10,'Complementação CAD — R47 a R49','22 trechos de pilares + 29 vigas + 11 lajes\n62 unidades lógicas complementadas',blue)
box(.54,.305,.425,.10,'Complementação BIM — R50','11 lajes\n11 unidades lógicas complementadas',teal)
arrow((.2475,.458),(.2475,.417),blue);arrow((.7525,.458),(.7525,.417),teal)
box(.115,.105,.77,.13,'Receptores complementados e revisados — R56/R57','65 pares geométricos: 22 pilares + 32 partes de viga + 11 lajes\n32 sólidos de viga representam 29 vigas lógicas\nEquivalência limitada a classes, caixas e áreas superiores',ink,fs=11)
arrow((.2475,.293),(.35,.247),blue);arrow((.7525,.293),(.65,.247),teal)
ax.text(.5,.057,'Unidades complementadas não são contagem de erros, cliques ou minutos.',ha='center',va='center',fontsize=11,fontweight='bold',color=ink)
ax.text(.5,.025,'Tempos finais pareados, conectividade analítica e aprovação ELU/ELS ainda não demonstrados.',ha='center',va='center',fontsize=10.5,color=gray)
fig.subplots_adjust(left=.025,right=.975,top=.98,bottom=.025)
fig.savefig(out/'R75-fluxos-resultados-parciais.png',dpi=180,facecolor='white')
fig.savefig(out/'R75-fluxos-resultados-parciais.svg',facecolor='white')
plt.close(fig)
p=out/'R75-fluxos-resultados-parciais.svg';p.write_text('\n'.join(line.rstrip() for line in p.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
(out/'R75-origem-dados.json').write_text(json.dumps(dict(revision='H03/R75',atUtc=datetime.now(timezone.utc).isoformat(),source=str(src),sha256=sha(src),figureContainsPartialHistoricalResults=True,fullFlowRankingAllowed=False,fullTimesAvailable=False,structuralApproval=False,visualQAStatus='pendente'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'LEIA-ME-R75.md').write_text('''# H03/R75 — figura de resultados parciais

PNG em180dpi e SVG vetorial, derivados de R72. A figura distingue desenho CAD recebido, elementos nativos BIM após adaptador e complementação posterior em cada ramo. Não representa geração final, taxa de erro, número de operações ou tempo dos fluxos. Contém as limitações na própria imagem.

Legenda sugerida: Figura — Recepção e complementação dos elementos da H03 nos dois fluxos automatizados, com checkpoint geométrico dos receptores. Fonte: elaboração do estudo, com evidências R43–R57 consolidadas em R72. Os32 sólidos de vigas representam29 vigas lógicas. Valores de complementação não equivalem a defeitos ou duração de trabalho.

Os65 pares no checkpoint R56/R57 não incluem11 apoios auxiliares exportados como IfcFooting por ramo. Nenhuma fundação foi dimensionada. Não se insere esta figura na monografia automaticamente. A revisão visual e os hashes finais são registrados antes da entrega.
''',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name);ast.parse(Path(__file__).read_text(encoding='utf-8'))
(out/'R75-protegidos-R74.json').write_text(json.dumps(protected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(str(out/'R75-fluxos-resultados-parciais.png'))

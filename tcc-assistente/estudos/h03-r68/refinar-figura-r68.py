from pathlib import Path
import sys,json
sys.path.insert(0,'D:/TCC/work/plot-deps')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path('D:/TCC/outputs/Compatibilizacao-H03-R68-PORTA-P3-ESTUDO')
r=json.loads((out/'R68-resultado.json').read_text(encoding='utf-8'))
col=r['columnGeometryByBranch']['CAD'][0];left=col['min'][0];right=col['max'][0]
fig,ax=plt.subplots(figsize=(9.5,4.2));fig.subplots_adjust(left=.25,bottom=.2,top=.80,right=.97)
ax.axvspan(left,right,color='#bdc4cc',alpha=.8,label='Pilar exportado')
series=[('R34/R67: aproximação',r['oldApproximateIntervalM'],3,'#ba3d35'),('R68: vão claro nominal',r['updatedNominalLocalIntervalM'],2,'#216d9d'),('R68: contorno externo',r['outerFrameLocalIntervalM'],1,'#ad7718')]
for label,ab,y,color in series:ax.plot(ab,[y,y],lw=9,color=color,solid_capstyle='butt');ax.text(ab[0]-.02,y,label,ha='right',va='center',fontsize=10)
ax.set_xlim(8.65,9.83);ax.set_ylim(.5,3.5);ax.set_yticks([]);ax.set_xlabel('Coordenada X local (m)');ax.grid(axis='x',alpha=.2)
fig.suptitle('Porta P3 direita / W18: revisão da referência em planta',y=.98,fontsize=13)
fig.text(.25,.90,'Triagem de estudo. Não representa tolerância executiva ou aprovação estrutural.',fontsize=9)
ax.legend(loc='lower right',fontsize=9);fig.savefig(out/'R68-intervalos-P3.png',dpi=160);fig.savefig(out/'R68-intervalos-P3.svg');plt.close(fig)

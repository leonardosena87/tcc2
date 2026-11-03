"""Figura do contorno medido nos IFCs; nao e desenho de execucao."""
from pathlib import Path
import json, sys
sys.path.insert(0, 'D:/TCC/work/plot-deps')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from auditar_contorno import OUT


def main():
    data = json.loads((OUT/'R178-comparacao-CAD-BIM.json').read_text(encoding='utf-8'))
    old = json.loads((OUT.parent/'Escada-H03-R177-INTEGRACAO-EBERICK-NAO-EXECUTAR/R177-comparacao-CAD-BIM.json').read_text(encoding='utf-8'))
    before = old['branches']['CAD']['elements']['LE1']
    after = data['branches']['CAD']['elements']['LE1']
    fig, (ax, zoom) = plt.subplots(1, 2, figsize=(12,6), facecolor='#f7f8fa')
    for item, label, color, style in [(before,'Eberick R177 — 2,15 m','#a66b25','--'),
                                       (after,'Eberick R178 CAD/BIM — 1,95 m','#216c9c','-')]:
        lo, hi = item['minM'], item['maxM']
        ax.add_patch(Rectangle((lo[0],lo[1]),hi[0]-lo[0],hi[1]-lo[1],
                              fill=False,edgecolor=color,linestyle=style,linewidth=2,label=label))
    for name in ('LE3','LE2'):
        e = data['branches']['CAD']['elements'][name]
        lo,hi = e['minM'],e['maxM']
        ax.add_patch(Rectangle((lo[0],.9758),hi[0]-lo[0],hi[1]-.9758,
                              facecolor='#cddde8',edgecolor='#216c9c',alpha=.7))
        ax.text((lo[0]+hi[0])/2,2.1,name,ha='center')
    ax.set(xlim=(4.15,6.8),ylim=(-.2,3.45),xlabel='X (m)',ylabel='Y (m)',
           title='Correção lateral do patamar')
    ax.set_aspect('equal'); ax.grid(alpha=.2)
    ax.legend(loc='upper center',bbox_to_anchor=(.5,-.15),fontsize=9,frameon=False)
    for y,label,color,ls in [(.1,'Frente Eberick R178: Y = 10,00 cm','#216c9c','-'),
                              (.0740833333,'Referência Revit R160: Y = 7,4083 cm','#218767','--')]:
        zoom.plot([4.5,6.45],[y,y],color=color,linestyle=ls,linewidth=2,label=label)
    zoom.annotate('',xy=(5.48,.1),xytext=(5.48,.0740833333),arrowprops=dict(arrowstyle='<->',color='#a53c28'))
    zoom.text(5.53,.087,'2,59 cm\npendentes',va='center',color='#a53c28')
    zoom.set(xlim=(4.4,6.55),ylim=(.045,.13),xlabel='X (m)',ylabel='Y (m)',
             title='Ampliação da borda junto à viga')
    zoom.grid(alpha=.2); zoom.legend(loc='upper center',bbox_to_anchor=(.5,-.15),fontsize=9,frameon=False)
    fig.suptitle('H03/R178 — patamar corrigido lateralmente nos dois receptores',fontsize=15,fontweight='bold')
    fig.text(.5,.035,'ESTUDO PRELIMINAR — NÃO EXECUTAR | Mesma triangulação das cinco peças comparadas; vínculo e dimensionamento pendentes.',
             ha='center',fontsize=9,color='#8b3526')
    fig.subplots_adjust(left=.07,right=.97,bottom=.25,top=.86,wspace=.35)
    fig.savefig(OUT/'R178-contorno-patamar.png',dpi=150)
    plt.close(fig)


if __name__ == '__main__':
    main()

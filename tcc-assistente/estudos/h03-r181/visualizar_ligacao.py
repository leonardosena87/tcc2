"""Secao XZ medida nas malhas; sem inferir dimensionamento ou armadura."""
from pathlib import Path
import json,sys
sys.path.insert(0,'D:/TCC/work/plot-deps')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon
from conferir_ligacao import OUT


def main():
    data=json.loads((OUT/'R181-ligacao-patamar.json').read_text(encoding='utf-8'))
    fig,axs=plt.subplots(1,2,figsize=(12,5.8),facecolor='#f7f8fa')
    for ax,key,title in zip(axs,['Revit','CAD'],['Revit R160 — IFC R161','Eberick R178 — CAD e BIM']):
        r=data['branches'][key];beam=r['beamMinM'],r['beamMaxM'];landing=r['landingMinM'],r['landingMaxM']
        # Corte local antes da uniao com os lances; espessura medida na secao.
        polys=r['sectionAtBeamFace']['polygonsXZ']
        zmin=min(p[1] for poly in polys for p in poly)
        zmax=max(p[1] for poly in polys for p in poly)
        ax.add_patch(Rectangle((beam[0][1]*100,beam[0][2]*100),(beam[1][1]-beam[0][1])*100,(beam[1][2]-beam[0][2])*100,facecolor='#cbd7e4',edgecolor='#315474',label='V16 — 20 × 30 cm'))
        ax.add_patch(Rectangle((landing[0][1]*100,zmin*100),(0.4-landing[0][1])*100,(zmax-zmin)*100,facecolor='#d4eee3',edgecolor='#217654',alpha=.8,label='Patamar — 14 cm na ligação'))
        ax.plot([10,10],[zmin*100,zmax*100],color='#bf542e',lw=4,label='Seção verificada na face da viga')
        ax.axvline(0,color='gray',lw=.8,ls='--')
        ax.text(10.8,156,'Face da viga\nY = 10 cm',fontsize=9,color='#9c4027')
        ax.annotate('Sobreposição de 2,592 cm' if key=='Revit' else 'Contato face a face',
                    xy=(8.7 if key=='Revit' else 10,169),xytext=(-16,185),
                    arrowprops=dict(arrowstyle='->',color='#454545'),fontsize=10)
        ax.set(xlim=(-20,42),ylim=(142,192),xlabel='Y (cm)',ylabel='Z (cm)',title=title)
        ax.set_aspect('equal');ax.grid(alpha=.2)
    axs[0].legend(loc='upper left',bbox_to_anchor=(0,-.18),fontsize=9,frameon=False)
    axs[1].text(.5,-.22,'Seção comum: 1,95 × 0,14 = 0,273 m²\n4 nós por ID ligam a grelha do patamar à viga, em cada receptor.',
                transform=axs[1].transAxes,ha='center',fontsize=10)
    fig.suptitle('H03/R181 — diferença de contorno junto à V16 sem folga na face verificada',fontsize=14,fontweight='bold')
    fig.text(.5,.025,'ESTUDO PRELIMINAR — NÃO EXECUTAR | Contato geométrico e conectividade exportada não validam vínculo, armadura ou capacidade.',ha='center',fontsize=9,color='#8b3526')
    fig.subplots_adjust(left=.07,right=.97,bottom=.28,top=.86,wspace=.22)
    fig.savefig(OUT/'R181-ligacao-patamar.png',dpi=150)
    plt.close(fig)


if __name__=='__main__':
    main()

"""Figura da geometria IFC medida; nao e prancha de execucao."""
import sys
sys.path[:0]=['D:/TCC/work/ifc/deps','D:/TCC/work/plot-deps']
import ifcopenshell, ifcopenshell.geom
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from auditar_escada import OUT


def main():
    model=ifcopenshell.open(str(OUT/'CAD-IFC/R177-CAD-ESCADA-CONTROLE.IFC'))
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    meshes={}
    for e in model.by_type('IfcElement'):
        if e.Name not in {'LE1','LE2','LE3','AE1A','AE1B','V16','P4','P10'}: continue
        if e.Name in {'P4','P10'} and not e.is_a('IfcColumn'): continue
        shape=ifcopenshell.geom.create_shape(settings,e)
        v=np.asarray(shape.geometry.verts).reshape(-1,3)
        f=np.asarray(shape.geometry.faces).reshape(-1,3)
        if e.is_a('IfcColumn') and v.max(0)[2]>3.21: continue
        meshes[e.GlobalId]=(e,v,f)
    fig=plt.figure(figsize=(13,7.5),facecolor='#f7f8fa')
    ax=fig.add_subplot(121,projection='3d');ax.set_facecolor('#f7f8fa')
    for e,v,f in meshes.values():
        color=('#e5a742' if e.Name.startswith('AE') else '#437ca6' if e.Name.startswith('LE') else '#b3b8bf')
        ax.add_collection3d(Poly3DCollection(v[f],facecolor=color,edgecolor='#374151',linewidth=.25,alpha=.95))
    ax.set(xlim=(4.15,6.8),ylim=(-.3,3.5),zlim=(0,3.5),xlabel='X (m)',ylabel='Y (m)',zlabel='Cota (m)')
    ax.set_box_aspect((2.65,3.8,3.5));ax.view_init(24,-115)
    ax.set_title('Geometria exportada pelo Eberick / CAD',fontsize=12,pad=12)
    ap=fig.add_subplot(122);ap.set_facecolor('#f7f8fa')
    ap.add_patch(Rectangle((4.4,.1),2.15,.8757833333,fill=False,edgecolor='#d37825',linewidth=2,label='Patamar Eberick (contorno medido)'))
    ap.add_patch(Rectangle((4.5,.0740833333),1.95,.9017,fill=False,edgecolor='#437ca6',linestyle='--',linewidth=2,label='Referência Revit R160'))
    ap.add_patch(Rectangle((4.5,.9757833333),.9,2.24,facecolor='#b8d0e3',edgecolor='#437ca6',alpha=.6))
    ap.add_patch(Rectangle((5.55,.9757833333),.9,2.24,facecolor='#b8d0e3',edgecolor='#437ca6',alpha=.6))
    ap.add_patch(Rectangle((4.4,-.1),2.15,.2,facecolor='#b3b8bf',edgecolor='#374151'))
    ap.text(5.475,0,'V16',ha='center',va='center',fontsize=10)
    ap.text(4.95,2.08,'LE3\n9 espelhos',ha='center',va='center',fontsize=11)
    ap.text(6.,2.08,'LE2\n8 espelhos',ha='center',va='center',fontsize=11)
    for x in [4.5,5.4]: ap.plot(x,3.2157833333,'s',color='#d99a34',ms=8)
    ap.text(5.475,3.4,'Marcadores de apoio idealizado',ha='center',fontsize=9,color='#835408')
    ap.set(xlim=(4.1,6.85),ylim=(-.3,3.65),xlabel='X (m)',ylabel='Y (m)',title='Contornos em planta: pendência de compatibilização')
    ap.set_aspect('equal');ap.grid(alpha=.2);ap.legend(loc='upper center',bbox_to_anchor=(.5,-.13),fontsize=8,frameon=False)
    fig.suptitle('H03/R177 — escada integrada nos receptores CAD e BIM',fontsize=16,fontweight='bold',y=.97)
    fig.text(.5,.025,'ESTUDO PRELIMINAR — NÃO EXECUTAR | Apoio inferior idealizado; contorno do patamar e arredondamento dos espelhos pendentes.',ha='center',fontsize=10,color='#8f341b')
    fig.subplots_adjust(left=.02,right=.98,bottom=.22,top=.88,wspace=.15)
    fig.savefig(OUT/'R177-escada-integrada-e-pendencias.png',dpi=150)
    plt.close(fig)


if __name__=='__main__':main()

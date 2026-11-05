"""Esquema de ancoragem a revisar; nao e plano de corte, nem altera PRJ."""
import argparse
import math
from pathlib import Path


def generate(path):
    items=[]
    def pair(code,value): items.extend((str(code),str(value)))
    def entity(kind,color=7): pair(0,kind);pair(8,'R223_ESTUDO');pair(62,color)
    def line(a,b,c,d,color=7):
        entity('LINE',color)
        for code,v in ((10,a),(20,b),(30,0),(11,c),(21,d),(31,0)):pair(code,v)
    def rect(x,y,w,h,color=7):
        for a,b,c,d in ((x,y,x+w,y),(x+w,y,x+w,y+h),(x+w,y+h,x,y+h),(x,y+h,x,y)):line(a,b,c,d,color)
    def text(x,y,t,h=1.6,color=7):
        entity('TEXT',color)
        for code,v in ((10,x),(20,y),(30,0),(40,h),(1,t),(50,0)):pair(code,v)
    def circle(x,y,r=.4,color=7):
        entity('CIRCLE',color)
        for code,v in ((10,x),(20,y),(30,0),(40,r)):pair(code,v)
    def arc(x,y,r,start,end,color=7):
        entity('ARC',color)
        for code,v in ((10,x),(20,y),(30,0),(40,r),(50,start),(51,end)):pair(code,v)
    pair(0,'SECTION');pair(2,'HEADER');pair(9,'$ACADVER');pair(1,'AC1009');pair(0,'ENDSEC')
    pair(0,'SECTION');pair(2,'ENTITIES')
    rect(0,0,240,165)
    text(5,156,'R223 | V1 - N0 | REVISAO EXTERNA 30 x 30',3,3)
    text(5,149,'ESTUDO ACADEMICO - NAO EXECUTAR - INTERFACES PENDENTES',2.15,1)
    text(5,143,'Proposta de ancoragem para revisao; nao substitui automaticamente o detalhe nativo.',1.7)
    # Secao real da hipotese, centimetros. Barras adicionais desconsideradas na capacidade auxiliar.
    sx,sy=10,97
    rect(sx,sy,30,30)
    rect(sx+3.315,sy+3.315,23.37,23.37,3)
    for x in (4.03,15,25.97): circle(sx+x,sy+25.97)
    for i in range(4):circle(sx+4.03+21.94*i/3,sy+4.03)
    for x in (4.03,25.97):
        for y in (4.03+21.94/3,4.03+2*21.94/3):circle(sx+x,sy+y,color=4)
    text(7,132,'SECAO TRANSVERSAL (cm)',1.8)
    text(46,125,'C25 | CA-50 | cnom = 3 cm',1.7)
    text(46,120,'Superior: 3 fi 8; inferior: 4 fi 8',1.7)
    text(46,115,'Laterais: 2 fi 8 por face, alem dos cantos',1.6,4)
    text(46,110,'Estribo fi 6,3; passo maximo 15 cm',1.7,3)
    text(46,105,'Triagem nao exige os grampos da antiga R218.',1.55)
    text(46,100,'Posicionar barras e ganchos sem colisao no no.',1.6,1)
    # Barra superior em elevacao: raio de eixo 2,4 cm = pino 4 cm + phi 0,8 cm.
    bx,by=10,45
    rect(bx,by,120,30)
    line(bx+30,by,bx+30,by+30,8);line(bx+90,by,bx+90,by+30,8)
    c=4.03;r=2.4;yy=by+30-c
    line(bx+c+r,yy,bx+120-c-r,yy,2)
    arc(bx+c+r,yy-r,r,90,180,2)
    arc(bx+120-c-r,yy-r,r,0,90,2)
    line(bx+c,yy-r,bx+c,yy-9.5,2)
    line(bx+120-c,yy-r,bx+120-c,yy-9.5,2)
    # Referencia das inferiores com ganchos projetados de 10 cm; nao fornece comprimento de corte.
    yy2=by+c
    line(bx+c+r,yy2,bx+120-c-r,yy2,4)
    arc(bx+c+r,yy2+r,r,180,270,4)
    arc(bx+120-c-r,yy2+r,r,270,360,4)
    line(bx+c,yy2+r,bx+c,yy2+10,4)
    line(bx+120-c,yy2+r,bx+120-c,yy2+10,4)
    for i in range(9):
        x=bx+3.315+113.37*i/8
        line(x,by+3.315,x,by+26.685,3)
    text(10,82,'ELEVACAO ESQUEMATICA | total 120; apoios 30 + vao 60 + apoio 30 cm',1.8)
    text(10,39,'9 posicoes de estribo no esquema: passo 14,17 cm. Nativo: 8 c/15.',1.65,3)
    text(139,76,'GANCHO PROPOSTO fi 8',1.8,2)
    text(139,70,'Pino >= 4,0 cm; raio do eixo 2,4 cm.',1.55)
    text(139,65,'Superior: projecao 9,5; ponta 7,1 cm.',1.55)
    text(139,60,'Ponta minima 8 fi = 6,4 cm.',1.55)
    text(139,55,'Superior nativo de 27 cm: rever.',1.55,1)
    text(139,50,'Pontas opostas: folga vertical 2,44 cm.',1.55)
    text(139,45,'Sem comprimento de corte liberado.',1.55,1)
    notes=[
        '1. V1 alargada de 20 para 30 cm; altura 30 cm e topo +0,20 m preservados.',
        '2. Gancho superior de 9,5 cm: proposta externa, ainda nao aplicada ao dimensionamento nativo.',
        '3. Boa aderencia: concretagem convencional da secao de 30 cm; verificar juntas e contato com solo.',
        '4. Apoios idealizados AE1A/AE1B: 30x30x20 cm no cadastro NAO dimensiona fundacoes.',
        '5. Avisos 19/98 mantidos. Fechar nos, confinamento, interferencias e ELS antes de liberar.',
        '6. Este estudo supera a geometria R218 20x30; antigos desenhos permanecem so como historico.',
    ]
    for i,t in enumerate(notes):text(5,31-i*4.7,t,1.55,1 if i in (1,3,4) else 7)
    pair(0,'ENDSEC');pair(0,'EOF')
    path.write_text('\n'.join(items)+'\n',encoding='ascii')


def render(dxf,png):
    import numpy  # Carrega a extensao compilada do ambiente antes das dependencias DXF locais.
    import sys
    sys.path.append(r'D:\TCC\work\dxf-deps')
    import ezdxf
    from PIL import Image,ImageDraw,ImageFont
    doc=ezdxf.readfile(dxf)
    im=Image.new('RGB',(1800,1250),'#111820');d=ImageDraw.Draw(im)
    colors={7:'#eef2f7',1:'#ff8a86',2:'#f6d66d',3:'#68dbc8',4:'#7fb9ff',8:'#8f9ba8'}
    scale=7.2
    def xy(x,y):return (35+x*scale,1220-y*scale)
    for e in doc.modelspace():
        color=colors.get(e.dxf.color,'white')
        if e.dxftype()=='LINE': d.line([xy(e.dxf.start.x,e.dxf.start.y),xy(e.dxf.end.x,e.dxf.end.y)],fill=color,width=2)
        elif e.dxftype()=='CIRCLE':
            x,y=xy(e.dxf.center.x,e.dxf.center.y);r=e.dxf.radius*scale
            d.ellipse((x-r,y-r,x+r,y+r),outline=color,width=2)
        elif e.dxftype()=='ARC':
            a,b=e.dxf.start_angle,e.dxf.end_angle
            pts=[xy(e.dxf.center.x+e.dxf.radius*math.cos(math.radians(t)),e.dxf.center.y+e.dxf.radius*math.sin(math.radians(t))) for t in numpy.linspace(a,b,36)]
            d.line(pts,fill=color,width=2)
        elif e.dxftype()=='TEXT':
            x,y=xy(e.dxf.insert.x,e.dxf.insert.y)
            font=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',round(e.dxf.height*scale*1.15))
            d.text((x,y),e.dxf.text,font=font,fill=color,anchor='ls')
    im.save(png)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);args=ap.parse_args()
    dxf=args.root/'R223-V1-ANCORAGEM-ESTUDO-NAO-EXECUTAR.dxf'
    generate(dxf);render(dxf,dxf.with_suffix('.png'))

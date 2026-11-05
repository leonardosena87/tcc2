"""Desenho DXF R12 de revisão externa, sem editar resultados binários do Eberick."""
from pathlib import Path
import argparse


def generate(path):
    parts = []
    def pair(code, value):
        parts.extend((str(code), str(value)))
    def entity(kind, color=7):
        pair(0, kind); pair(8, 'R218_V1'); pair(62, color)
    def line(x1,y1,x2,y2,color=7):
        entity('LINE',color)
        for c,v in ((10,x1),(20,y1),(30,0),(11,x2),(21,y2),(31,0)): pair(c,v)
    def rect(x,y,w,h,color=7):
        for a,b,c,d in ((x,y,x+w,y),(x+w,y,x+w,y+h),(x+w,y+h,x,y+h),(x,y+h,x,y)): line(a,b,c,d,color)
    def text(x,y,value,h=1.6,color=7):
        entity('TEXT',color)
        for c,v in ((10,x),(20,y),(30,0),(40,h),(1,value),(50,0)): pair(c,v)
    def circle(x,y,r,color=7):
        entity('CIRCLE',color)
        for c,v in ((10,x),(20,y),(30,0),(40,r)): pair(c,v)
    pair(0,'SECTION');pair(2,'HEADER');pair(9,'$ACADVER');pair(1,'AC1009');pair(0,'ENDSEC')
    pair(0,'SECTION');pair(2,'ENTITIES')
    rect(0,0,220,140)
    text(5,132,'R218 | V1 - N0 | COMPLEMENTO EXTERNO',3,3)
    text(5,126,'ESTUDO ACADEMICO - NAO EXECUTAR - ANCORAGENS PENDENTES',2.1,1)
    text(5,120,'Aplicacao grafica local; nao altera a armadura calculada automaticamente.',1.7)
    text(5,113,'SECAO 20 x 30 cm',2)
    x,y=12,75
    rect(x,y,20,30)
    rect(x+3.315,y+3.315,13.37,23.37,3)
    for xx in (4.03,15.97):
        for yy in (4.03,25.97): circle(x+xx,y+yy,.4)
    # Duas barras por face: mesmo arranjo lateral selecionado no Eberick.
    side_levels=(4.03+(25.97-4.03)/3,4.03+2*(25.97-4.03)/3)
    for yy in side_levels:
        line(x+3.315,y+yy,x+16.685,y+yy,3)
        for xx in (4.03,15.97): circle(x+xx,y+yy,.4,4)
    text(39,103,'Estribo fechado fi 6,3 c/9 cm',1.7,3)
    text(39,98,'2 grampos fi 6,3 por posicao',1.7,3)
    text(39,93,'Amarrar as 2 barras de cada face',1.6)
    text(39,88,'4 barras laterais fi 8 (2 por face)',1.7,4)
    text(39,83,'Dobras/ancoragens: definir e verificar',1.6,1)
    text(113,113,'ELEVACAO ESQUEMATICA',2)
    # Vista em escala reduzida; nao constitui plano de corte ou dobra.
    ex,ey,scale=113,75,.85
    rect(ex,ey,110*scale,30*scale)
    rect(ex,ey-5,20*scale,5);rect(ex+90*scale,ey-5,20*scale,5)
    for i in range(13):
        xx=ex+(3+104*i/12)*scale
        line(xx,ey+3*scale,xx,ey+27*scale,3)
    text(ex,65,'L total 110 cm | vao livre 70 cm',1.7)
    text(ex,60,'13 posicoes no esquema: passo 8,67 cm',1.6,3)
    text(5,65,'C25 | CA-50 | cobrimento 3 cm',1.8)
    text(5,60,'Geometria em cm; esquema sem escala de impressao.',1.6)
    notes=[
      '1. Complemento somente da V1; configuracao global dos estribos preservada.',
      '2. Nativo: fi 6,3 c/15. Revisao externa: fi 6,3 com espacamento maximo de 9 cm.',
      '3. Grampos horizontais nos dois niveis das barras laterais; ganchos apenas esquematicos.',
      '4. Nao se emite comprimento de corte/dobra. Conferir ganchos, cobrimento, apoios e montagem.',
      '5. Aviso 19 e avisos de ancoragem da pele permanecem abertos. Nao e aprovacao estrutural.',
      '6. Manter armadura longitudinal nativa como referencia; fechar ancoragem antes da liberacao.',
      '7. Base: verificacao complementar R217. Revisao R218: 4 barras laterais e 2 grampos.',
      '8. Desenho associado ao N0. Nao substitui os calculos nem atualiza a relacao de aco nativa.',
    ]
    for i,n in enumerate(notes):text(5,49-i*5,n,1.55,1 if i in (3,4) else 7)
    pair(0,'ENDSEC');pair(0,'EOF')
    path.write_text('\n'.join(parts)+'\n',encoding='ascii')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('output',type=Path)
    args=parser.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
    generate(args.output)
    print(args.output)

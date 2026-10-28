"""Compara geometria e rótulos DXF antes/depois do SAVEAS e reabertura DWG nativos."""
from pathlib import Path
import json,hashlib,re,collections
root=Path(__file__).parent
root=Path('D:/TCC/outputs/Intercambio-H03-R45-CAD-NAO-EXECUTAR')
base=root.parent/'Alternativa-H03-R43-ESTUDO-NAO-EXECUTAR'
def entities(path):
    lines=path.read_text(encoding='utf-8-sig',errors='replace').splitlines()
    pairs=[(int(lines[i].strip()),lines[i+1].strip()) for i in range(0,len(lines)-1,2)]
    start=next(i for i,p in enumerate(pairs) if p==(2,'ENTITIES'))+1
    rows=[];row=None
    for code,value in pairs[start:]:
        if code==0:
            if row:rows.append(row)
            if value=='ENDSEC':break
            row={'type':value,'pairs':[]}
        elif row is not None:row['pairs'].append((code,value))
    return rows
def signature(row):
    pairs=row['pairs'];kind=row['type']
    def values(code):return [v for c,v in pairs if c==code]
    def first(code,default=None):return next(iter(values(code)),default)
    def number(code,default=0):return round(float(first(code,default)),8)
    layer=first(8,'0')
    if kind=='LWPOLYLINE':
        xs=values(10);ys=values(20)
        assert len(xs)==len(ys)==int(first(90))
        coords=tuple((round(float(x),8),round(float(y),8)) for x,y in zip(xs,ys))
        return (kind,layer,int(first(70,'0'))&1,number(38),coords)
    if kind=='TEXT':
        text=re.sub(r'\\U\+([0-9A-Fa-f]{4})',lambda m:chr(int(m[1],16)),first(1,''))
        hjust=int(first(72,'0'));vjust=int(first(73,'0'))
        # Para texto justificado o ponto de referência é 11/21/31; o AutoCAD
        # recalcula 10/20/30 ao regenerar conforme fonte e conteúdo.
        anchor=11 if hjust or vjust else 10
        return (kind,layer,text,number(anchor),number(anchor+10),number(anchor+20),
                number(40),number(50),number(41,1),hjust,vjust,first(7,'Standard'))
    raise ValueError('Tipo não coberto: '+kind)

def field(row,code,default=None):return next((v for c,v in row['pairs'] if c==code),default)
def poly(row,factor,rename=False):
    assert row['type']=='LWPOLYLINE'
    assert all(abs(float(v))<1e-12 for c,v in row['pairs'] if c in (40,41,42,43)), 'Curvatura/largura não coberta pelo leitor.'
    assert all(float(field(row,c,str(default)))==default for c,default in ((210,0.),(220,0.),(230,1.))), 'Plano OCS não implementado.'
    xs=[float(v)/factor for c,v in row['pairs'] if c==10]
    ys=[float(v)/factor for c,v in row['pairs'] if c==20]
    points=[(round(x,7),round(y,7)) for x,y in zip(xs,ys)]
    closed=int(field(row,70,'0'))&1
    if closed and points[0]==points[-1]:points.pop()
    # O ponto inicial e o sentido não modificam um contorno fechado.
    if closed:
        choices=[tuple(p[i:]+p[:i]) for p in (points,list(reversed(points))) for i in range(len(p))]
        points=min(choices)
    layer=field(row,8,'0')
    if rename:layer=layer.replace('_',' ')
    return (layer,closed,round(float(field(row,38,'0'))/factor,7),tuple(points))
def texts(rows):
    return collections.Counter(''.join(v for c,v in r['pairs'] if c in (1,3)) for r in rows if r['type'] in ('TEXT','MTEXT'))
reports=[]
for level in (1,2):
    src=entities(base/f'H03-R43-N{level}.dxf');dst=entities(root/f'R45-Eberick-N{level}.dxf')
    sourcePolys=[x for x in src if x['type']=='LWPOLYLINE'];targetPolys=[x for x in dst if x['type']=='LWPOLYLINE']
    a=collections.Counter(poly(x,1,True) for x in sourcePolys)
    # A exportação gráfica do croqui em 1:50 usa coordenadas de desenho:
    # 1 m da origem -> 100 cm / 50 = 2 unidades no DXF de controle.
    b=collections.Counter(poly(x,2) for x in targetPolys)
    sourceLayers=sorted({field(x,8,'0') for x in src});mapping={x:x.replace('_',' ') for x in sourceLayers}
    assert len(set(mapping.values()))==len(mapping),'Colisão de nomes de camadas.'
    layerCountsSource=collections.Counter(mapping[field(x,8,'0')] for x in src)
    layerCountsTarget=collections.Counter(field(x,8,'0') for x in dst)
    contentMatch=texts(src)==texts(dst)
    # Controles de sensibilidade em memória, sem modificar arquivos empíricos.
    corrupted=collections.Counter(b)
    first=next(iter(corrupted));corrupted[first]-=1
    missingPolyDetected=a!=+corrupted
    missingText=texts(dst);missingText[next(iter(missingText))]-=1
    missingTextDetected=texts(src)!=+missingText
    wrongScaleDetected=a!=collections.Counter(poly(x,1) for x in targetPolys)
    assert all((missingPolyDetected,missingTextDetected,wrongScaleDetected))
    reports.append({'floor':f'N{level}','source':str(base/f'H03-R43-N{level}.dxf'),'readback':str(root/f'R45-Eberick-N{level}.dxf'),'sourceCounts':dict(collections.Counter(x['type'] for x in src)),
      'receivedCounts':dict(collections.Counter(x['type'] for x in dst)),
      'polylineContoursMatch':a==b,'textContentsMatch':contentMatch,
      'missingContourSignatures':sum((a-b).values()),'extraContourSignatures':sum((b-a).values()),
      'layerRenaming':mapping,'layerEntityCountsMatchUnderExplicitMapping':layerCountsSource==layerCountsTarget,
      'paperExportScale':50,'sourceMetersToExportDrawingUnits':2,
      'drawingRepresentationChanges':['TEXT convertido em MTEXT','Sublinhado substituído por espaço nos nomes de camadas','Fonte, altura e posicionamento tipográfico não preservados de modo idêntico; conteúdo confrontado separadamente.'],
      'fullTypographyEquivalenceVerified':False,'nativeStructuralElementConversionVerified':False,
      'sensitivityControls':{'missingPolylineDetected':missingPolyDetected,'missingTextDetected':missingTextDetected,'incorrectScaleDetected':wrongScaleDetected}})
record={'scope':'Desenho CAD recebido e reexportado pelo Eberick, em escala 1:50. Não é auditoria estrutural.',
 'floors':reports,'allContoursAndTextContentsMatch':all(x['polylineContoursMatch'] and x['textContentsMatch'] for x in reports),
 'interpretation':'A ausência de divergência nos contornos não converte linhas em vigas, pilares ou lajes calculáveis. Alterações tipográficas e nomes de camadas são registradas sem classificá-las automaticamente como erro estrutural.'}
(root/'R45-auditoria-recebimento-Eberick.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,ensure_ascii=True,indent=2))
assert record['allContoursAndTextContentsMatch'],'Investigar diferenças do recebimento.'

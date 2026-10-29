"""Triagem R55: paredes sobre geometria IFC R53, sem editar PRJ/RVT/DWG."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,csv,sys,shutil,time
sys.path.insert(0,'D:/TCC/work/ifc/deps')
import ifcopenshell,ifcopenshell.geom as geom
import numpy as np
root=Path('D:/TCC');out=root/'outputs/Paredes-H03-R55-ESTUDO-NAO-EXECUTAR';out.mkdir(exist_ok=True)
start=time.perf_counter();utc=datetime.now(timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(name,data): (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sources=[root/'outputs/Compatibilizacao-H01-R06/paredes-superior-referencia.json',root/'outputs/Concepcao-H03-R34-ESTUDO-NAO-ADOTADO/R34-referencia-arquitetonica.json']
walls=read(sources[0])['walls'];reference=read(sources[1]);openings=next(f['openings'] for f in reference['floors'] if f['id']=='S')
for branch in ('CAD','BIM'):sources.append(root/f'outputs/Cargas-H03-R53-PARCIAL-NAO-EXECUTAR/IFC-{branch}/Modelo 3D.IFC')
protected=read(root/'outputs/Apoios-H03-R54-NAO-EXECUTAR/R54-manifesto.json')['files']
for item in protected:assert sha(Path(item['path']))==item['sha256'],item['path']
def extract(path):
 m=ifcopenshell.open(str(path));s=geom.settings();s.set(s.USE_WORLD_COORDS,True);rows=[]
 for cls in ('IfcBeam','IfcSlab','IfcColumn'):
  for o in m.by_type(cls):
   shape=geom.create_shape(s,o);v=np.array(shape.geometry.verts).reshape(-1,3)
   rows.append(dict(kind=cls,name=o.Name,guid=o.GlobalId,min=[round(float(t),6) for t in v.min(axis=0)],max=[round(float(t),6) for t in v.max(axis=0)]))
 return rows
branches={b:extract(p) for b,p in zip(('CAD','BIM'),sources[2:])}
def spatial(rows):return sorted((r['kind'],tuple(r['min']+r['max'])) for r in rows)
assert spatial(branches['CAD'])==spatial(branches['BIM'])
def bimnames(items):
 return [b['name'] for a in items for b in branches['BIM'] if a['kind']==b['kind'] and a['min']==b['min'] and a['max']==b['max']]
# Piso/forro arquitetonicos de referencia; nao altera nivel estrutural.
roof=6.39;floor=3.2;surface=1.565;eps=1e-6
matrix=[];wallrecords=[];clashes=[]
for wall in walls:
 axis=0 if abs(wall['y2']-wall['y'])<eps else 1;other=1-axis
 lo=min(wall['x' if axis==0 else 'y'],wall['x2' if axis==0 else 'y2']);hi=max(wall['x' if axis==0 else 'y'],wall['x2' if axis==0 else 'y2']);fixed=wall['y' if axis==0 else 'x']
 def interval(obj):
  if obj['min'][other]-eps<=fixed<=obj['max'][other]+eps:
   a=max(lo,obj['min'][axis]);b=min(hi,obj['max'][axis])
   if b-a>eps:return a,b
 def match(o):
  a=o['x' if axis==0 else 'y'];b=o['x2' if axis==0 else 'y2'];c=o['y' if axis==0 else 'x'];d=o['y2' if axis==0 else 'x2']
  return abs(c-fixed)<eps and abs(d-fixed)<eps and min(a,b)>=lo-eps and max(a,b)<=hi+eps
 matched=[o for o in openings if match(o)]
 assert len(matched)==len(wall['openings']),(wall['id'],matched)
 wallrecords.append({**wall,'openingReferencesR34':matched,'openingDeductionApplied':False,'openingPositionStatus':'Triagem manual R34; confirmar faces e alturas antes de descontar','complete':False})
 eligible=[]
 for r in branches['CAD']:
  z=r['max'][2]
  if (r['kind'] in ('IfcBeam','IfcSlab') and (abs(z-floor)<eps or abs(z-roof)<eps)) or (r['kind']=='IfcColumn' and abs(z-roof)<eps):
   ab=interval(r)
   if ab:eligible.append((r,*ab))
 cuts=sorted(set([lo,hi]+[n for r,a,b in eligible for n in (a,b)]))
 for a,b in zip(cuts,cuts[1:]):
  if b-a<eps:continue
  mid=(a+b)/2;hits=[r for r,x,y in eligible if x-eps<mid<y+eps]
  col=[r for r in hits if r['kind']=='IfcColumn'];lower=[r for r in hits if abs(r['max'][2]-floor)<eps and r['kind']!='IfcColumn'];upper=[r for r in hits if abs(r['max'][2]-roof)<eps and r['kind']!='IfcColumn']
  beams=[r for r in lower if r['kind']=='IfcBeam'];slabs=[r for r in lower if r['kind']=='IfcSlab']
  route='coluna-sem-alvenaria' if col else 'viga' if beams else 'laje' if slabs else 'sem-apoio-geometrico'
  bottom=min((r['min'][2] for r in upper),default=None);base=wall['baseFinishedElevationM'];height=round(bottom-base,6) if bottom is not None and base is not None else None
  if height is not None:assert height>0
  nominalceiling=round(base+2.8,6) if base is not None else None
  clash=not col and bottom is not None and nominalceiling is not None and bottom<nominalceiling-eps
  p1=[wall['x'],wall['y']];p2=p1.copy();p1[axis]=round(a,6);p2[axis]=round(b,6)
  row=dict(wallId=wall['id'],fromM=round(a,6),toM=round(b,6),lengthM=round(b-a,6),p1=p1,p2=p2,route=route,lowerNativeNames=[r['name'] for r in beams or slabs],lowerNativeNamesBIM=bimnames(beams or slabs),upperNativeNames=[r['name'] for r in upper],upperNativeNamesBIM=bimnames(upper),columnNativeNames=[r['name'] for r in col],baseFinishedM=base,upperSoffitM=bottom,grossHeightReferenceM=height,grossLinearKNm=round(surface*height,6) if height is not None and not col else None,ceilingReferenceM=nominalceiling,ceilingInterference=clash,referenceCeilingHeightHypothesisM=2.8,appliedToNative=False,readyForNativeApplication=False)
  matrix.append(row)
  if clash:clashes.append(row)
assert len(wallrecords)==20 and len({o['id'] for w in wallrecords for o in w['openingReferencesR34']})==11
for wall in walls:
 assert abs(sum(r['lengthM'] for r in matrix if r['wallId']==wall['id'])-wall['lengthBetweenAxesM'])<1e-5
slabwalls=sorted(set(r['wallId'] for r in matrix if r['route']=='laje'))
summary=dict(revision='H03/R55',atUtc=datetime.now(timezone.utc).isoformat(),sourceGeometryRevision='IFC R53; auditoria pos-conversao R54 pendente',sameReferenceForBothBranches=True,sourceSpatialBoundingBoxesEqual=True,protectedR54FilesChecked=len(protected),wallCount=20,segmentCount=len(matrix),slabSupportedWalls=slabwalls,ceilingInterferenceWallIds=sorted(set(r['wallId'] for r in clashes)),allLoadsApplied=False,nativeFilesModified=False,calculationPerformed=False,inputs=[dict(path=str(p),sha256=sha(p)) for p in sources],wallCompositionHypothesis=dict(finishedThicknessM=.15,ceramicBlockM=.115,finishEachFaceM=.0175,uncoatedWallKNm2=.9,finishDensityKNm3=19,areaWeightKNm2=surface,source='Exemplar local NBR 6120:2019, Tabela 2, PDF17/pagina impressa11; 1,565 calculado por composicao, nao valor diretamente tabelado',manufacturerConfirmed=False),limits=['Caixas envolventes trianguladas de elementos ortogonais; nao verifica contatos/ligacoes analiticas, excentricidades ou resistencia.','Trechos nos pilares excluidos da alvenaria; acabamento sobre concreto, encontros de paredes, vergas/contravergas e esquadrias pendentes.','Nenhum desconto de vao aplicado. Altura cheia ate intradorso e hipotese, ainda nao liberada para lancamento.','W08 permanece sem altura/carga definida: base junto a escada pendente, nunca tratada como zero.','Forro a 2,80m acima do piso local e referencia de triagem; confirmar extensao/espessura do sistema por ambiente.','Nao somar cargas brutas como quantitativo final. Faltam paredes terreas, muros, platibandas e abrigo do tanque.','Nomes nativos CAD/BIM no CSV correspondidos por classe e caixa espacial; nao implica igualdade de numeracao ou vinculos.','Conflitos de forro sao comuns da concepcao; nao atribuidos como defeitos de transferencia.'])
write('R55-resumo.json',summary);write('R55-paredes-referencia.json',dict(walls=wallrecords));write('R55-trechos.json',dict(segments=matrix));write('R55-geometria-fonte.json',branches)
with (out/'R55-trechos.csv').open('w',encoding='utf-8-sig',newline='') as f:
 keys=['wallId','fromM','toM','lengthM','route','lowerNativeNames','lowerNativeNamesBIM','baseFinishedM','upperSoffitM','grossHeightReferenceM','grossLinearKNm','ceilingReferenceM','ceilingInterference','appliedToNative'];w=csv.DictWriter(f,fieldnames=keys,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(matrix)
text=f"""# H03/R55 — paredes e compatibilizacao preliminar da cobertura

Estudo comum aos dois fluxos; NAO EXECUTAR. Nenhum PRJ/RVT/DWG foi alterado. A fonte geometrica e o IFC R53 de cada ramo; a auditoria de exportacao posterior a conversao de apoios R54 continua pendente. Conferiram-se os hashes dos {len(protected)} arquivos do manifesto R54, sem alteracao.

Mapearam-se 20 paredes superiores em {len(matrix)} trechos por intersecao de eixos com caixas envolventes reais. As caixas espaciais exportadas R53 coincidem entre CAD e BIM. O CSV inclui nomes nativos CAD e BIM correspondidos por classe e caixa espacial. Paredes com trechos sobre laje: {', '.join(slabwalls)}. Esse contato geometrico nao comprova o caminho analitico da carga.

As 11 aberturas receberam identificadores individuais da referencia R34. A porta S-P3-01 fica na W19 e S-P3-02 na W18; nao sao uma abertura duplicada. Manteve-se a area bruta sem desconto de portas/janelas. W08 permanece sem base/altura resolvida junto a escada, com carga desconhecida (campo vazio), nunca carga numerica zero.

A parede acabada de 15cm e premissa do usuario. A composicao de estudo e bloco ceramico vazado horizontal de 11,5cm mais 1,75cm de argamassa por face. Pelo exemplar local da NBR 6120:2019, Tabela2/PDF17, usou-se 0,90kN/m2 sem revestimento e 19kN/m3 para argamassa; calculou-se 1,565kN/m2 de parede. Essa composicao nao foi medida nem confirmada por fabricante. A carga linear bruta e 1,565 vezes a altura de referencia do piso acabado ao menor intradorso interceptado. Nao aplicar esses numeros automaticamente.

A triagem marcou interferencia com a referencia de forro a 2,80m nas paredes: {', '.join(summary['ceilingInterferenceWallIds'])}. Algumas vigas exportadas da cobertura ainda apresentam altura de 35, 40, 45 ou 55cm; apenas os trechos com intradorso acima do forro atendem geometricamente essa condicao preliminar. Preservar a arquitetura conforme decisao do usuario: revisar seções/concepcao, calcular e verificar ELU/ELS antes de aceitar qualquer reducao. Nao elevar a cobertura para ocultar interferencia. O conflito pertence a concepcao comum; nao conta como erro de IFC ou DWG.

Ainda faltam definicao de faces/comprimentos liquidos, acabamento sobre pilares, encontros, vergas/contravergas, tara de esquadrias e suporte analitico. Nao ha soma final de cargas. A etapa nao mede tempo comparativo de fluxo: o registro de execucao do script exclui preparacao, pesquisa e revisao; nao equivale a esforco total de IA/humano.

Proxima etapa: resolver seções da cobertura preservando forro/pisos; exportar e auditar os estados posteriores a R54; fechar cargas por trechos e so entao aplicar a mesma matriz, em copias independentes, com temporizadores separados. Permanecem pendentes telhado, tanque1000L/apoio, escada, bordas, vento, combinacoes e processamento.
"""
(out/'LEIA-ME-R55.md').write_text(text,encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
write('R55-execucao-script.json',dict(startUtc=utc,endUtc=datetime.now(timezone.utc).isoformat(),durationMs=(time.perf_counter()-start)*1000,scope='Somente execucao do script; nao mede preparacao/revisao/IA total ou fluxo CAD/BIM'))
write('R55-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file() and p.name!='R55-manifesto.json']))
print(json.dumps(summary,ensure_ascii=False))

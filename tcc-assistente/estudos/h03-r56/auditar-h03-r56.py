"""Auditoria geometrica IFC R56; nao certifica modelo analitico ou calculo."""
from pathlib import Path
import json,hashlib,sys,time
from datetime import datetime,timezone
sys.path.insert(0,'D:/TCC/work/ifc/deps')
import ifcopenshell,ifcopenshell.geom as geom,ifcopenshell.util.element
import numpy as np
root=Path('D:/TCC');out=root/'outputs/Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(name,value):(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=time.perf_counter();utc=datetime.now(timezone.utc).isoformat()
def extract(path):
 m=ifcopenshell.open(str(path));s=geom.settings();s.set(s.USE_WORLD_COORDS,True);rows=[]
 for cls in ('IfcColumn','IfcBeam','IfcSlab','IfcFooting'):
  for o in m.by_type(cls):
   sh=geom.create_shape(s,o);v=np.array(sh.geometry.verts).reshape(-1,3);f=np.array(sh.geometry.faces).reshape(-1,3)
   top=v[:,2].max();area=sum(float(np.linalg.norm(np.cross(v[t][1]-v[t][0],v[t][2]-v[t][0]))/2) for t in f if np.max(abs(v[t][:,2]-top))<1e-5)
   r=dict(type=cls,name=o.Name,guid=o.GlobalId,min=[round(float(a),6) for a in v.min(0)],max=[round(float(a),6) for a in v.max(0)],topAreaM2=round(area,6))
   if cls=='IfcSlab':r['rawLoads']={k:v for p in ifcopenshell.util.element.get_psets(o).values() for k,v in p.items() if k in ('Acidental (Q)','Revestimento (G2)')}
   rows.append(r)
 return rows
results={};allrows={}
for b in ('CAD','BIM'):
 before=root/f'outputs/Cargas-H03-R53-PARCIAL-NAO-EXECUTAR/IFC-{b}/Modelo 3D.IFC';after=out/f'IFC-{b}/Modelo 3D.IFC'
 old=extract(before);new=extract(after);allrows[b]=new
 oldsuper={r['guid']:r for r in old if r['type']!='IfcFooting'};newsuper={r['guid']:r for r in new if r['type']!='IfcFooting'}
 assert set(oldsuper)==set(newsuper)
 changes=[];roof=[];unchanged=[]
 for guid,r in newsuper.items():
  prev=oldsuper[guid];assert (r['type'],r['name'])==(prev['type'],prev['name'])
  isroof=r['type']=='IfcBeam' and abs(r['max'][2]-6.39)<1e-5
  if isroof:
   assert r['min'][:2]==prev['min'][:2] and r['max']==prev['max']
   assert abs(r['min'][2]-6.09)<1e-5
   assert abs(r['topAreaM2']-prev['topAreaM2'])<1e-5
   h0=round(prev['max'][2]-prev['min'][2],6)
   row=dict(name=r['name'],guid=guid,oldHeightM=h0,newHeightM=.3,min=r['min'],max=r['max'])
   roof.append(row)
   if abs(h0-.3)>1e-5:changes.append(row)
  else:
   assert r==prev,(b,r['type'],r['name'],prev,r)
   unchanged.append(guid)
 footings=[r for r in new if r['type']=='IfcFooting'];assert len(footings)==11
 assert len(roof)==15 and len(changes)==13
 result=dict(branch=b,before=str(before),beforeSha256=sha(before),source=str(after),sha256=sha(after),
   counts={c:sum(r['type']==c for r in new) for c in ('IfcColumn','IfcBeam','IfcSlab','IfcFooting')},
   roofBeams=roof,changedRoofBeamSolids=changes,unchangedSuperstructureSolidCount=len(unchanged),
   allRoofBeamHeights30cm=True,allSuperstructureGuidsNamesPreserved=True,slabsGeometryAndRawLoadsPreserved=True,
   columnsAndN1BeamsGeometryPreserved=True,auxiliaryFootingsExcludedFromSuperstructure=True,
   footingMeaning='Cadastros geometricos auxiliares herdados da R54, sem sondagem/dimensionamento. Nao sao fundacoes executivas.',
   supportReleasesVerifiedByIFC=False,analyticalBarHeightVerified=False,structuralCalculationPerformed=False)
 results[b]=result;write(f'R56-auditoria-{b}.json',result)
def spatial(rows):
 return sorted((r['type'],tuple(r['min']+r['max']),r['topAreaM2'],tuple(sorted(r.get('rawLoads',{}).items()))) for r in rows)
assert spatial(allrows['CAD'])==spatial(allrows['BIM'])
protected=read(out/'R56-protegidos-R54.json')
for r in protected:assert sha(Path(r['path']))==r['sha256']
write('R56-geometria-exportada.json',allrows)
write('R56-validacao.json',dict(atUtc=datetime.now(timezone.utc).isoformat(),sameSpatialBoxesTopAreasAndSlabRawLoadsBothBranches=True,
 protectedR54FilesChecked=len(protected),allRoofBeams30cmBoth=True,
 roofTopM=6.39,roofBeamSoffitM=6.09,mainFloorM=3.25,mainCeilingReferenceM=6.05,geometricGapToCeilingReferenceM=.04,
 ceilingAssemblyAndServicesClearanceVerified=False,ceilingAcrossEveryRoomVerified=False,
 superstructurePostSupportConversionGeometricallyAudited=True,foundationAnalyticalParametersAudited=False,
 nativeUIReopenSamples={'CAD':'V4_1/N2','BIM':'V4/N2'},all15RoofBeamSolidsReadThroughIFC=True,
 sourceMetadata='R56 e primeira exportacao apos R54; nao cria exportacao retroativa R54.',
 runtime=dict(startUtc=utc,endUtc=datetime.now(timezone.utc).isoformat(),durationMs=(time.perf_counter()-start)*1000,scope='Somente execucao auditor; exclui preparacao/revisao/interface')))
print(json.dumps({b:dict(counts=r['counts'],roofSolids=len(r['roofBeams']),changed=len(r['changedRoofBeamSolids'])) for b,r in results.items()}))

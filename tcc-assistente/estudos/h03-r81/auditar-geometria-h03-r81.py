from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,'D:/TCC/work/ifc/deps')
import ifcopenshell,ifcopenshell.geom as geom,ifcopenshell.util.element
import numpy as np
root=Path('D:/TCC');out=root/'outputs/Agrupamento-H03-R81-TESTE-NAO-EXECUTAR';new=out/'IFC-BIM/Modelo 3D.IFC';old=root/'outputs/Verificacao-H03-R57-NAO-EXECUTAR/IFC-BIM/Modelo 3D.IFC';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def clean(x):
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items() if k!='id'}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 return x
def extract(p):
 m=ifcopenshell.open(str(p));s=geom.settings();s.set(s.USE_WORLD_COORDS,True);rows=[]
 for cls in ('IfcColumn','IfcBeam','IfcSlab','IfcFooting'):
  for o in m.by_type(cls):
   sh=geom.create_shape(s,o);v=np.array(sh.geometry.verts).reshape(-1,3);f=np.array(sh.geometry.faces).reshape(-1,3);top=v[:,2].max();area=sum(float(np.linalg.norm(np.cross(v[t][1]-v[t][0],v[t][2]-v[t][0]))/2) for t in f if np.max(abs(v[t][:,2]-top))<1e-5)
   rows.append(dict(type=cls,name=o.Name,guid=o.GlobalId,min=[round(float(a),6) for a in v.min(0)],max=[round(float(a),6) for a in v.max(0)],topAreaM2=round(area,6),exportedProperties=clean(ifcopenshell.util.element.get_psets(o))))
 return rows
historical=extract(old);control=out/'IFC-BIM-CONTROLE/Modelo 3D.IFC';a=extract(control);b=extract(new);assert len(historical)==76 and len(a)==len(b)==89
def key(r):return(r['type'],tuple(r['min']+r['max']))
am={key(r):r for r in a};bm={key(r):r for r in b};assert len(am)==len(bm)==89 and am.keys()==bm.keys()
matches=[]
for k,x in am.items():
 y=bm[k];assert abs(x['topAreaM2']-y['topAreaM2'])<=1e-5
 pd={p:dict(old=x['exportedProperties'].get(p),new=y['exportedProperties'].get(p)) for p in set(x['exportedProperties'])|set(y['exportedProperties']) if x['exportedProperties'].get(p)!=y['exportedProperties'].get(p)}
 matches.append(dict(type=x['type'],beforeName=x['name'],afterName=y['name'],guidChanged=x['guid']!=y['guid'],min=x['min'],max=x['max'],topAreasMatch=True,propertiesDiffer=pd))
partitions=[]
for r in historical:
 if r['type']!='IfcBeam':continue
 axis=0 if r['max'][0]-r['min'][0]>r['max'][1]-r['min'][1] else 1;fixed=[j for j in range(3) if j!=axis];parts=[n for n in a if n['type']=='IfcBeam' and all(abs(n[z][j]-r[z][j])<1e-5 for z in ('min','max') for j in fixed) and n['min'][axis]>=r['min'][axis]-1e-5 and n['max'][axis]<=r['max'][axis]+1e-5];assert parts
 parts.sort(key=lambda n:n['min'][axis]);assert abs(parts[0]['min'][axis]-r['min'][axis])<1e-5 and abs(parts[-1]['max'][axis]-r['max'][axis])<1e-5
 for left,right in zip(parts,parts[1:]):assert abs(left['max'][axis]-right['min'][axis])<1e-5
 assert abs(sum(n['topAreaM2'] for n in parts)-r['topAreaM2'])<1e-5
 partitions.append(dict(historicalName=r['name'],historicalGuid=r['guid'],min=r['min'],max=r['max'],newParts=[dict(name=n['name'],guid=n['guid'],min=n['min'],max=n['max']) for n in parts],coverageContinuousWithoutOverlap=True,topAreaSumPreserved=True))
assert sum(len(p['newParts']) for p in partitions)==45
historicalNonBeam={key(r):r for r in historical if r['type']!='IfcBeam'};controlNonBeam={key(r):r for r in a if r['type']!='IfcBeam'};assert historicalNonBeam.keys()==controlNonBeam.keys()
nameChanges=[r for r in matches if r['beforeName']!=r['afterName']];assert len(nameChanges)==1 and nameChanges[0]['beforeName']=='V2' and nameChanges[0]['afterName']=='V13'
result=dict(beforeControl=str(control),beforeControlSha256=sha(control),afterTest=str(new),afterTestSha256=sha(new),historical=str(old),historicalSha256=sha(old),geometryMatchingUnique89=True,superstructureGeometricParts78Preserved=True,auxiliaryGeometry11Preserved=True,dimensionedBeamPartsPerBranch=45,historicalBeamParts=32,historicalBeam32ToControl45CoverageChecked=True,additionalPartitions13AreNot13NewBeamGroups=True,nameChanges=nameChanges,propertyChanges=[r for r in matches if r['propertiesDiffer']],analyticalConnectivityVerified=False)
for name,value in [('R81-geometria-exportada.json',b),('R81-geometria-controle-exportada.json',a),('R81-geometria-comparada.json',result),('R81-particao-historica-32-para-45.json',partitions)]:
 p=out/name;assert not p.exists();p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(geometryMatchingUnique89=True,nameChanges=len(nameChanges),propertyChanges=len(result['propertyChanges']),partitionCoverage32To45=True,changedProperties=[dict(type=r['type'],name=r['afterName'],fields=list(r['propertiesDiffer'])) for r in result['propertyChanges']]),ensure_ascii=False))

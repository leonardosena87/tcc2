"""Compara duas exportacoes IFC nativas da R49; preserva primeira auditoria."""
from pathlib import Path
import sys,json,hashlib,shutil
sys.path.insert(0,'D:/TCC/work/ifc/deps')
import ifcopenshell,ifcopenshell.geom as geom
import numpy as np
out=Path('D:/TCC/outputs/Complementacao-H03-R49-LAJES-CAD-NAO-EXECUTAR')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def extract(path):
    m=ifcopenshell.open(str(path));s=geom.settings();s.set(s.USE_WORLD_COORDS,True)
    rows=[]
    for cls in ('IfcColumn','IfcBeam','IfcSlab'):
        for o in m.by_type(cls):
            shape=geom.create_shape(s,o);v=np.array(shape.geometry.verts).reshape(-1,3);f=np.array(shape.geometry.faces).reshape(-1,3)
            area=sum(float(np.linalg.norm(np.cross(v[t][1]-v[t][0],v[t][2]-v[t][0]))/2) for t in f if np.max(abs(v[t][:,2]-v[:,2].max()))<1e-5)
            rows.append(dict(type=cls,name=o.Name,guid=o.GlobalId,min=v.min(axis=0).tolist(),max=v.max(axis=0).tolist(),topAreaM2=area))
    return rows
a=out/'R49-primeira-exportacao.ifc';b=out/'Modelo 3D.IFC'
before=extract(a);after=extract(b)
old={r['guid']:r for r in before};new={r['guid']:r for r in after}
changes=[]
for guid,r in new.items():
    p=old.get(guid)
    if not p or r['type']!=p['type'] or r['name']!=p['name'] or any(abs(x-y)>1e-5 for k in ('min','max') for x,y in zip(r[k],p[k])) or abs(r['topAreaM2']-p['topAreaM2'])>1e-5:changes.append(guid)
r=dict(firstSha256=sha(a),reopenedSha256=sha(b),counts={c:sum(x['type']==c for x in after) for c in ('IfcColumn','IfcBeam','IfcSlab')},
       changedGuids=changes,missingGuids=sorted(set(old)-set(new)),sameGeometryNamesGuidsAndTopAreas=not changes and set(old)==set(new),computationalToleranceM=1e-5,
       limits='Caixas envolventes, nomes, GUIDs e areas superiores; nao valida apoio do balanco, conectividade ou calculo.')
assert r['sameGeometryNamesGuidsAndTopAreas']
(out/'R49-reabertura.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(b,out/'R49-apos-reabrir.ifc')
print(json.dumps(r,indent=2))

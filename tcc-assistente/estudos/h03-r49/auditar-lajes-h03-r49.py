"""Auditoria inicial R49: contornos geometricos; nao aprova apoio ou calculo."""
from pathlib import Path
import sys,json,hashlib,copy
sys.path.insert(0,'D:/TCC/work/ifc/deps')
import ifcopenshell,ifcopenshell.geom as geom
import numpy as np
out=Path('D:/TCC/outputs/Complementacao-H03-R49-LAJES-CAD-NAO-EXECUTAR')
source=out/'Modelo 3D.IFC'
p=json.loads(Path('D:/TCC/outputs/Alternativa-H03-R43-ESTUDO-NAO-EXECUTAR/H03-R43-proposta.json').read_text(encoding='utf-8-sig'))
m=ifcopenshell.open(str(source));s=geom.settings();s.set(s.USE_WORLD_COORDS,True)
rows=[]
for o in m.by_type('IfcSlab'):
    shape=geom.create_shape(s,o);v=np.array(shape.geometry.verts).reshape(-1,3);f=np.array(shape.geometry.faces).reshape(-1,3)
    area=sum(float(np.linalg.norm(np.cross(v[t][1]-v[t][0],v[t][2]-v[t][0]))/2) for t in f if np.max(abs(v[t][:,2]-v[:,2].max()))<1e-5)
    rows.append(dict(name=o.Name,guid=o.GlobalId,min=v.min(axis=0).tolist(),max=v.max(axis=0).tolist(),topAreaM2=area))
expected=[]
for e in p['elements']:
    if e['kind']!='slab':continue
    # Lajes interiores sao limitadas pelas faces internas das vigas de 20 cm.
    # Varanda limitada pela face externa x=9.75 e tres bordos livres originais.
    balcony=e['id']=='L7-VARANDA-N1'
    lo=[e['x']+.1,e['y']+(0 if balcony else .1),e['z']-e['h']]
    hi=[e['x2']-(0 if balcony else .1),e['y2']-(0 if balcony else .1),e['z']]
    expected.append(dict(id=e['id'],min=lo,max=hi,area=(hi[0]-lo[0])*(hi[1]-lo[1])))
def audit(items):
    matches=[]
    for r in items:
        found=[e for e in expected if np.allclose(r['min'],e['min'],rtol=0,atol=1e-5) and np.allclose(r['max'],e['max'],rtol=0,atol=1e-5) and abs(r['topAreaM2']-e['area'])<1e-5]
        matches.append(dict(**r,sourceIds=[e['id'] for e in found]))
    ids=[r['sourceIds'][0] for r in matches if len(r['sourceIds'])==1]
    return dict(slabs=matches,missingIds=sorted({e['id'] for e in expected}-set(ids)),geometryPass=len(items)==11 and len(set(ids))==11,expected=expected)
r=audit(rows);changed=copy.deepcopy(rows);changed[0]['min'][2]-=.01
r.update(source=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),counts={c:len(m.by_type(c)) for c in ('IfcColumn','IfcBeam','IfcSlab')},computationalToleranceM=1e-5,
    syntheticControls=dict(missingDetected=not audit(rows[1:])['geometryPass'],duplicateDetected=not audit(rows+[rows[0]])['geometryPass'],heightChangeDetected=not audit(changed)['geometryPass']),
    limits=['Contornos nominais por caixas envolventes e area superior triangulada; nao comprova conectividade nem apoio do balanco.',
            'Lajes internas descontam faces de vigas; varanda desconta face externa x=9.75, area esperada 3.2175 m2.',
            'Reabertura, engastamento, cargas, ELU/ELS e estabilidade pendentes.'])
(out/'R49-auditoria-lajes-inicial.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(r,ensure_ascii=True,indent=2))
assert all(r['syntheticControls'].values())

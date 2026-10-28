"""Compara exportacoes nativas anteriores/posteriores a reabertura do PRJ."""
from pathlib import Path
import hashlib,json,sys,shutil
sys.path.insert(0,'D:/TCC/work/ifc/deps')
import ifcopenshell
import ifcopenshell.geom as geom
ROOT=Path('D:/TCC/outputs/Intercambio-H03-R46-BIM-NAO-EXECUTAR')
SOURCE=Path('D:/TCC/outputs/H03_BIM_R46_IFC_NAO_EXECUTAR/Arquivos do projeto/Modelo 3D.IFC')
before=json.loads((ROOT/'R46-geometria-inicial.json').read_text(encoding='utf-8'))
m=ifcopenshell.open(str(SOURCE));s=geom.settings();s.set(s.USE_WORLD_COORDS,True)
rows=[]
for cls in ('IfcColumn','IfcBeam','IfcSlab'):
    for obj in m.by_type(cls):
        shape=geom.create_shape(s,obj);v=shape.geometry.verts
        rows.append({'class':cls,'name':obj.Name,'guid':obj.GlobalId,
                     'min':[min(v[i::3]) for i in range(3)],
                     'max':[max(v[i::3]) for i in range(3)]})
previous={r['guid']:r for r in before['geometry']}
changes=[]
for r in rows:
    p=previous.get(r['guid'])
    if not p or r['class']!=p['class'] or r['name']!=p['name'] or any(abs(a-b)>1e-5 for key in ('min','max') for a,b in zip(r[key],p[key])):
        changes.append(r['guid'])
missing=sorted(set(previous)-{r['guid'] for r in rows})
result={'source':str(SOURCE),'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'previousSha256':before['sha256'],'counts':{c:len(m.by_type(c)) for c in ('IfcColumn','IfcBeam','IfcSlab')},
        'changedGeometryOrNameGuids':changes,'missingGuids':missing,
        'sameGeometryAndIdentity':not changes and not missing and len(rows)==len(previous),
        'toleranceM':1e-5,'reopenedInSameComputer':True,
        'externalModelAssociationWarningObserved':False,
        'limits':'Caixas envolventes, classes, nomes e GUIDs; nao valida conectividade analitica ou calculo.'}
(ROOT/'R46-reabertura.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(SOURCE,ROOT/'R46-estrutura-apos-reabrir.ifc')
print(json.dumps(result,indent=2))
assert result['sameGeometryAndIdentity']

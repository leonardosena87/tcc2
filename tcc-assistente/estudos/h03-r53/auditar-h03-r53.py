"""Audita cargas brutas e geometria IFC R53 sem editar modelos nativos."""
from pathlib import Path
import sys,json,hashlib,time
from datetime import datetime,timezone
sys.path.insert(0,'D:/TCC/work/ifc/deps')
import ifcopenshell,ifcopenshell.geom as geom,ifcopenshell.util.element
import numpy as np
root=Path('D:/TCC');out=root/'outputs/Cargas-H03-R53-PARCIAL-NAO-EXECUTAR'
branch=sys.argv[1];assert branch in ('CAD','BIM')
start=time.perf_counter();startutc=datetime.now(timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=out/f'IFC-{branch}/Modelo 3D.IFC'
baseline=root/f'outputs/Conferencia-H03-R52-VINCULOS-NAO-EXECUTAR/IFC-{branch}/Modelo 3D.IFC'
def extract(path):
    m=ifcopenshell.open(str(path));s=geom.settings();s.set(s.USE_WORLD_COORDS,True);rows=[]
    for cls in ('IfcColumn','IfcBeam','IfcSlab'):
        for obj in m.by_type(cls):
            shape=geom.create_shape(s,obj);v=np.array(shape.geometry.verts).reshape(-1,3);f=np.array(shape.geometry.faces).reshape(-1,3)
            area=sum(float(np.linalg.norm(np.cross(v[t][1]-v[t][0],v[t][2]-v[t][0]))/2) for t in f if np.max(abs(v[t][:,2]-v[:,2].max()))<1e-5)
            row=dict(type=cls,name=obj.Name,guid=obj.GlobalId,min=v.min(axis=0).tolist(),max=v.max(axis=0).tolist(),topAreaM2=area)
            if cls=='IfcSlab':
                props=ifcopenshell.util.element.get_psets(obj)
                row['rawLoads']={k:val for ps in props.values() for k,val in ps.items() if k in ('Acidental (Q)','Revestimento (G2)')}
            rows.append(row)
    return rows
before=extract(baseline);after=extract(source)
old={r['guid']:r for r in before};new={r['guid']:r for r in after};changed=[]
for guid,r in new.items():
    p=old.get(guid)
    if not p or r['type']!=p['type'] or r['name']!=p['name'] or any(abs(x-y)>1e-5 for k in ('min','max') for x,y in zip(r[k],p[k])) or abs(r['topAreaM2']-p['topAreaM2'])>1e-5:changed.append(guid)
planned=json.loads((out/'R53-matriz-planejada.json').read_text(encoding='utf-8'))['matrix'];slabs=[]
for r in after:
    if r['type']!='IfcSlab':continue
    level='N1' if abs(r['max'][2]-3.2)<1e-5 else 'N2' if abs(r['max'][2]-6.39)<1e-5 else 'DESCONHECIDO'
    plan=next(p for p in planned if p['level']==level and p['nativeName']==r['name'])
    expected={'Acidental (Q)':plan['Q_kNm2']*100,'Revestimento (G2)':plan['G2partial_kNm2']*100}
    assert r['rawLoads']==expected,(r,expected)
    slabs.append(dict(level=level,**r,expectedNativeUI=dict(Q_kNm2=plan['Q_kNm2'],G2partial_kNm2=plan['G2partial_kNm2']),nativeUIAllIndividuallyReadAfterReopen=False))
assert len(slabs)==11 and not changed and set(old)==set(new)
result=dict(branch=branch,source=str(source),sha256=sha(source),baseline=str(baseline),baselineSha256=sha(baseline),
    counts={c:sum(r['type']==c for r in after) for c in ('IfcColumn','IfcBeam','IfcSlab')},slabs=slabs,
    sameGeometryNamesGuidsAndTopAreas=True,changedGuids=changed,all11RawLoadFieldsMatchPlannedPattern=True,
    UIToIFCRatioObserved=100,IFCPropertyExplicitUnitsMissing=True,
    nativeUIReadAfterReopenSamples=['L4/N1','L6/N1','L4/N2'],
    limits=['Razao empirica entre campos desta exportacao e UI; nao certifica unidade padrao IFC nem conversao geral.',
    'Leitura nativa apos reabrir por amostragem em 3 paineis; os outros 8 foram conferidos pelos campos exportados.',
    'Geometria por caixas envolventes/areas superiores, nomes e GUIDs; nao comprova malha integral, vinculos ou calculo.',
    'Acoes parciais: paredes, telhado, tanque, bordas, escada, vento e combinacoes continuam pendentes.'],
    calculationPerformed=False,completeLoads=False,analyticalLinksVerified=False,
    auditRuntime=dict(startUtc=startutc,endUtc=datetime.now(timezone.utc).isoformat(),durationMs=(time.perf_counter()-start)*1000,scope='Somente execucao do auditor IFC; exclui preparacao do script, UI e revisao tecnica.'))
(out/f'R53-auditoria-{branch}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(branch=branch,counts=result['counts'],geometryPreserved=True,slabsLoadPatternMatched=len(slabs))))

"""Auditoria geométrica da recepção CAD; não aprova vínculos ou cálculo."""
import json
import importlib.util
from pathlib import Path
import sys

_spec = importlib.util.spec_from_file_location('audit_r234', Path(__file__).resolve().parent.parent/'h03-r234/auditar.py')
_r234 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r234)
snapshot, semantic, sha, coverage, ezdxf = (_r234.snapshot, _r234.semantic, _r234.sha, _r234.coverage, _r234.ezdxf)

OUT = Path('D:/TCC/outputs/H03-R235-CAD-VIGAS-ESCADA-NAO-EXECUTAR')
TOL = 1e-4


def audit():
    read = lambda name: json.loads((OUT/name).read_text(encoding='utf-8-sig'))
    plan = read('R235-preparacao.json')
    project, = (OUT/'CAD/Projeto Eberick').glob('*.prj')
    original = Path(plan['source'])/'Projeto Eberick'/project.name
    control = OUT/'CAD/Arquivos do projeto/Modelo 3D.IFC'
    first = OUT/'R235-controle-antes-reabertura.ifc'
    prior_file = Path(plan['source'])/'Arquivos do projeto/Modelo 3D.IFC'
    paths = [project, original, control, first, prior_file]
    paths += list(map(Path, plan['cadDxfHashes']))
    paths += list(OUT.glob('R235-*.json'))
    paths = [p for p in paths if p.name not in ('R235-auditoria.json','R235-backup.json')]
    hashes = {str(p):sha(p) for p in paths}
    if sha(original) != plan['sourcePrjSha256']:
        raise ValueError('Projeto de origem R234 alterado')
    if any(sha(Path(p)) != h for p,h in plan['cadDxfHashes'].items()):
        raise ValueError('Origem CAD alterada')
    current, prior = snapshot(control), snapshot(prior_file)
    if len(prior)!=68 or len(current)!=70:
        raise ValueError('Contagem inesperada')
    retained = {g:p for g,p in current.items() if g in prior}
    if semantic(retained) != semantic(prior):
        raise ValueError('Geometria, identidade ou propriedades anteriores alteradas')
    added = {g:p for g,p in current.items() if g not in prior}
    if (sum(p['cls']=='IfcColumn' for p in current.values())!=35
            or sum(p['cls']=='IfcBeam' for p in current.values())!=35
            or {p['level'] for p in added.values()}!={'N0','PATAMAR'}):
        raise ValueError('Distribuição de classes/níveis inesperada')
    origins = []
    for entry in plan['beams']:
        s = entry['record']; level = entry['levelName']
        drawing = ezdxf.readfile(entry['cadPath'])
        if drawing.units != 6:
            raise ValueError('Unidade CAD diferente de metros')
        entities = [e for e in drawing.modelspace() if e.dxf.layer==level+'_VIGAS'
                    and e.get_xdata('TCC_R225')[0].value==s['id']]
        entity, = entities
        data = json.loads(next(t.value for t in entity.get_xdata('TCC_R225')
                              if t.code==1000 and t.value.startswith('{')))
        if data!=s or entity.dxftype()!='LWPOLYLINE' or not entity.closed:
            raise ValueError('Metadados CAD inconsistentes')
        along = 0 if s['x']!=s['x2'] else 1; cross = 1-along
        a = (s['x'],s['y']); b = (s['x2'],s['y2'])
        start,end = sorted((a[along],b[along]))
        expected = {(round(p,8),round(q,8)) if along==0 else (round(q,8),round(p,8))
                    for p in (start,end) for q in (a[cross]-s['b']/2,a[cross]+s['b']/2)}
        if {(round(x,8),round(y,8)) for x,y in entity.get_points('xy')}!=expected:
            raise ValueError('Polilinha CAD difere do eixo nominal')
        label=f"{s['id']} {round(s['b']*100)}x{round(s['h']*100)}cm"
        if sum(e.dxf.text==label for e in drawing.modelspace().query('TEXT'))!=1:
            raise ValueError('Rótulo de seção ausente ou duplicado')
        guid,p = next(iter([(g,p) for g,p in added.items() if p['level']==level]))
        if sum(p['level']==level for p in added.values())!=1 or p['cls']!='IfcBeam':
            raise ValueError('Viga sem associação única')
        lo,hi=p['geometry']['minM'],p['geometry']['maxM']
        if not (abs((lo[cross]+hi[cross])/2-a[cross])<TOL
                and abs(hi[cross]-lo[cross]-s['b'])<TOL
                and abs(hi[2]-s['z'])<TOL and abs(hi[2]-lo[2]-s['h'])<TOL
                and start-TOL<=lo[along]<hi[along]<=end+TOL):
            raise ValueError('Geometria da viga diverge do CAD')
        concrete=p['psets']['Pset_ConcreteElementGeneral']
        if concrete['StrengthClass']!='C-25' or concrete['ConcreteCover']!=3:
            raise ValueError('Material/cobrimento divergente')
        intervals=[(lo[along],hi[along])]; intersections=[]
        for col in current.values():
            if col['cls']!='IfcColumn': continue
            cl,ch=col['geometry']['minM'],col['geometry']['maxM']
            if (cl[cross]-TOL<=a[cross]<=ch[cross]+TOL and cl[2]<=s['z']-s['h']+TOL
                    and ch[2]>=s['z']-TOL and min(ch[along],end)-max(cl[along],start)>TOL):
                intervals.append((cl[along],ch[along])); intersections.append(col['name'])
        cov=coverage(intervals,start,end)
        if not cov['noGapAboveTolerance']:
            raise ValueError('Lacuna geométrica não explicada por pilares')
        origins.append(dict(source=s['id'],guid=guid,level=level,name=p['name'],
                            geometry=p['geometry'],sectionCm=[s['b']*100,s['h']*100],
                            intersectingColumns=sorted(set(intersections)),coverage=cov))
    reopening=read('R235-reabertura.json')
    persisted=semantic(snapshot(first))==semantic(current) and reopening['openedExplicitR235Root']
    if not persisted: raise ValueError('Persistência após reabertura não demonstrada')
    if hashes!={str(p):sha(p) for p in paths}:
        raise ValueError('Arquivo alterado durante auditoria')
    result=dict(revision='R235',allNativeElements=70,columns=35,beamParts=35,
                sourceCadBeamIdentitiesAccumulated=32,addedBeamParts=2,retainedR234Elements=68,
                allR234IdentitiesGeometryAndPsetsRetained=True,allAddedSectionsMatchCad=True,
                geometryToleranceM=TOL,persistedAfterReopen=persisted,sourceR234ProjectUnchanged=True,
                timingBase=read('R235-tempo-base.json'),timingLanding=read('R235-tempo-patamar.json'),
                baseSupportPending=True,loadsApplied=False,analyticalConnectivityVerified=False,
                structuralApproval=False,origins=origins,hashes=hashes)
    (OUT/'R235-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8-sig')
    print(json.dumps({k:v for k,v in result.items() if k not in ('origins','hashes')},ensure_ascii=False))
    return result


if __name__=='__main__':
    audit()

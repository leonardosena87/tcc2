"""Audita vigas N1 contra o CAD e preservacao dos 50 elementos R233."""
from collections import Counter
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'h03-r232'))
from auditar_pilares import snapshot, sha, coverage, ezdxf
OUT = Path('D:/TCC/outputs/H03-R234-CAD-VIGAS-N1-NAO-EXECUTAR')

TOL = 1e-4
CONTROL = OUT/'CAD/Arquivos do projeto/Modelo 3D.IFC'


def semantic(parts):
    # O número STEP do conjunto muda ao inserir vigas; não é propriedade de engenharia.
    return {guid:dict(p,psets={name:{k:v for k,v in values.items() if k!='id'}
                              for name,values in p['psets'].items()})
            for guid,p in parts.items()}


def audit():
    plan = json.loads((OUT/'R234-preparacao.json').read_text(encoding='utf-8-sig'))
    source = Path(plan['cadDxf'])
    project, = (OUT/'CAD/Projeto Eberick').glob('*.prj')
    original = Path(plan['source'])/'Projeto Eberick'/project.name
    paths = [source,project,original,CONTROL,OUT/'R234-preparacao.json',OUT/'R234-tempo-observado.json',
             Path(plan['source'])/'Arquivos do projeto/Modelo 3D.IFC']
    hashes = {str(p):sha(p) for p in paths}
    if sha(source) != plan['cadDxfSha256'] or sha(original) != plan['sourcePrjSha256']:
        raise ValueError('Origem CAD/R233 alterada')
    drawing = ezdxf.readfile(source)
    sources = plan['beams']
    if drawing.units != 6 or len(sources) != 16 or len({s['id'] for s in sources}) != 16:
        raise ValueError('Esperadas 16 identidades CAD em metros')
    for s in sources:
        hit = [e for e in drawing.modelspace() if e.dxf.layer=='N1_VIGAS'
               and e.get_xdata('TCC_R225')[0].value == s['id']]
        e, = hit
        tags = e.get_xdata('TCC_R225')
        record = json.loads(next(t.value for t in tags if t.code==1000 and t.value.startswith('{')))
        if record != s:
            raise ValueError('Plano difere da origem CAD')
        along = 0 if s['x'] != s['x2'] else 1
        cross = 1-along
        a = (s['x'],s['y']); b = (s['x2'],s['y2'])
        lo, hi = sorted((a[along],b[along]))
        expected = {(round(p,8),round(q,8)) if along==0 else (round(q,8),round(p,8))
                    for p in (lo,hi) for q in (a[cross]-s['b']/2,a[cross]+s['b']/2)}
        if not e.closed or {(round(x,8),round(y,8)) for x,y in e.get_points('xy')} != expected:
            raise ValueError('Polilinha não corresponde ao eixo nominal')
        label = f"{s['id']} {round(s['b']*100)}x{round(s['h']*100)}cm"
        if sum(e.dxf.text==label for e in drawing.modelspace().query('TEXT')) != 1:
            raise ValueError('Rótulo CAD ausente ou duplicado')
    current = snapshot(CONTROL)
    prior = snapshot(Path(plan['source'])/'Arquivos do projeto/Modelo 3D.IFC')
    columns = {k:v for k,v in current.items() if v['cls']=='IfcColumn'}
    retained = {k:v for k,v in current.items() if v['cls']=='IfcColumn' or v['level']=='N2'}
    if semantic(prior) != semantic(retained) or len(columns) != 35 or len(retained) != 50:
        raise ValueError('Pilares/vigas N2 da R233 não preservados')
    beams = []
    for guid,p in current.items():
        if guid in retained:
            continue
        if p['cls']!='IfcBeam' or p['level']!='N1':
            raise ValueError('Elemento fora do escopo')
        box = p['geometry']; lo,hi = box['minM'],box['maxM']; found=[]
        for s in sources:
            along = 0 if s['x']!=s['x2'] else 1; cross=1-along
            axis = (s['x'],s['y']); end=(s['x2'],s['y2'])
            start,finish = sorted((axis[along],end[along]))
            if (abs((lo[cross]+hi[cross])/2-axis[cross])<TOL
                and abs(hi[cross]-lo[cross]-s['b'])<TOL
                and abs(hi[2]-s['z'])<TOL and abs(hi[2]-lo[2]-s['h'])<TOL
                and lo[along]>=start-TOL and hi[along]<=finish+TOL
                and min(hi[along],finish)-max(lo[along],start)>TOL):
                found.append(s['id'])
        if len(found)!=1:
            raise ValueError('Viga sem associação CAD única: '+guid)
        props = p['psets']['Pset_ConcreteElementGeneral']
        if props['StrengthClass']!='C-25' or props['ConcreteCover']!=3:
            raise ValueError('Material/cobrimento divergente')
        beams.append(dict(guid=guid,source=found[0],**p))
    origins=[]
    for s in sources:
        along=0 if s['x']!=s['x2'] else 1; cross=1-along
        a=(s['x'],s['y']); b=(s['x2'],s['y2']); start,end=sorted((a[along],b[along]))
        hits=[p for p in beams if p['source']==s['id']]
        intervals=[(p['geometry']['minM'][along],p['geometry']['maxM'][along]) for p in hits]
        supports=[]
        # Intersecoes volumetricas explicam apenas recortes geometricos, nao vinculos analiticos.
        for p in current.values():
            if p['cls']=='IfcBeam' and (p['level']!='N1' or any(p['name']==q['name'] for q in hits)):
                continue
            lo,hi=p['geometry']['minM'],p['geometry']['maxM']
            if lo[cross]-TOL<=a[cross]<=hi[cross]+TOL and lo[2]<=s['z']-s['h']+TOL and hi[2]>=s['z']-TOL:
                if min(hi[along],end)-max(lo[along],start)>TOL:
                    supports.append((lo[along],hi[along]))
        cov=coverage(intervals+supports,start,end)
        if not cov['noGapAboveTolerance'] or not hits:
            raise ValueError('Lacuna fora dos solidos interceptantes em '+s['id'])
        origins.append(dict(id=s['id'],receiverNames=sorted({p['name'] for p in hits}),parts=len(hits),coverage=cov))
    if len(beams)!=18 or len(origins)!=16:
        raise ValueError('Contagem inesperada de vigas')
    first=OUT/'R234-controle-antes-reabertura.ifc'
    persisted=(first.is_file() and (OUT/'R234-reabertura.json').is_file()
               and snapshot(first)==current)
    if hashes != {str(p):sha(p) for p in paths}:
        raise ValueError('Arquivos alterados durante auditoria')
    result=dict(revision='R234',sourceCadBeams=16,receiverBeamParts=18,retainedColumns=35,retainedN2BeamParts=15,
                allSectionsMatchCad=True,beamTopM=3.2,allBeamsUniquelyMatchedToCad=True,
                noProjectionGapOutsideIntersectingSolids=True,allR233IdentitiesGeometryAndPsetsRetained=True,
                concreteClass='C-25',coverCm=3,geometryToleranceM=TOL,
                persistedAfterReopen=persisted,sourceR233ProjectUnchanged=True,
                timing=json.loads((OUT/'R234-tempo-observado.json').read_text(encoding='utf-8-sig')),
                nativeVerificationAtOpening=json.loads((OUT/'R234-abertura.json').read_text(encoding='utf-8-sig')),
                hashes=hashes,origins=origins,parts=beams,loadsApplied=False,
                analyticalConnectivityVerified=False,structuralApproval=False)
    (OUT/'R234-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8-sig')
    print(json.dumps({k:v for k,v in result.items() if k not in ('parts','origins','hashes')},ensure_ascii=False))
    return result


if __name__=='__main__':
    audit()

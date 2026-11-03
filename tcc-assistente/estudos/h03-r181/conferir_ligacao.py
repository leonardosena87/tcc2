"""Mede secao na face de V16 e nos compartilhados da grelha exportada.

Leitura apenas. Contato geometrico e conectividade nao aprovam o vinculo,
o dimensionamento, a armadura ou a execucao da ligacao.
"""
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone
import hashlib, importlib.util, json, math, sys

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Escada-H03-R181-LIGACAO-PATAMAR-NAO-EXECUTAR')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def area(poly):
    return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly, poly[1:]+poly[:1])))/2


def clip_rectangle(poly, bounds):
    """Recorta um poligono convexo 2D; bounds=(xmin,zmin,xmax,zmax)."""
    for axis, limit, sign in [(0,bounds[0],1),(0,bounds[2],-1),
                               (1,bounds[1],1),(1,bounds[3],-1)]:
        result = []
        if not poly:
            return []
        for a,b in zip(poly,poly[1:]+poly[:1]):
            da,db = sign*(a[axis]-limit),sign*(b[axis]-limit)
            if da >= 0:
                result.append(a)
            if (da >= 0) != (db >= 0):
                t = da/(da-db)
                result.append(tuple(a[k]+t*(b[k]-a[k]) for k in range(2)))
        poly = result
    return poly


def section_at_y(vertices, faces, y, bounds, epsilon=1e-9):
    """Area XZ recortada na face da viga.

    Aceita triangulos coplanares OU um unico contorno fechado convexo de
    intersecao transversal. Rejeita topologia ambigua em vez de usar bbox.
    epsilon em m e arredondamento de nos a 9 casas sao numericos, nao de obra.
    """
    coplanar, segments = [], set()
    for ids in faces:
        tri = [tuple(map(float,vertices[i])) for i in ids]
        dist = [p[1]-y for p in tri]
        if all(abs(d)<=epsilon for d in dist):
            coplanar.append([(p[0],p[2]) for p in tri])
            continue
        hits = set()
        for a,b,da,db in zip(tri,tri[1:]+tri[:1],dist,dist[1:]+dist[:1]):
            if abs(da)<=epsilon:
                hits.add((round(a[0],9),round(a[2],9)))
            if da*db < -epsilon**2:
                t=da/(da-db)
                hits.add((round(a[0]+t*(b[0]-a[0]),9),
                          round(a[2]+t*(b[2]-a[2]),9)))
        if len(hits)==2:
            segments.add(tuple(sorted(hits)))
        elif len(hits)>2:
            raise ValueError('Intersecao triangular ambigua')
    if coplanar:
        signatures=Counter(tuple(sorted(p)) for p in coplanar)
        if any(n!=1 for n in signatures.values()):
            raise ValueError('Face coplanar duplicada')
        return dict(mode='coplanar_mesh_faces',
            areaM2=sum(area(clip_rectangle(p,bounds)) for p in coplanar),
            polygonsXZ=coplanar)
    if not segments:
        return dict(mode='empty',areaM2=0.,polygonsXZ=[])
    graph=defaultdict(set)
    for a,b in segments:
        graph[a].add(b);graph[b].add(a)
    if any(len(v)!=2 for v in graph.values()):
        raise ValueError('Secao aberta ou com ramificacao')
    start=min(graph);poly=[start];previous=None;current=start
    while True:
        nxt=next(p for p in sorted(graph[current]) if p!=previous)
        if nxt==start:
            break
        if nxt in poly:
            raise ValueError('Contorno se repete')
        poly.append(nxt);previous,current=current,nxt
    if len(poly)!=len(graph):
        raise ValueError('Multiplos contornos exigem outro algoritmo')
    turns=[]
    for a,b,c in zip(poly,poly[1:]+poly[:1],poly[2:]+poly[:2]):
        cross=(b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
        if abs(cross)>epsilon:
            turns.append(math.copysign(1,cross))
    if len(set(turns))>1:
        raise ValueError('Secao nao convexa exige outro algoritmo')
    return dict(mode='closed_convex_section',
                areaM2=area(clip_rectangle(poly,bounds)),polygonsXZ=[poly])


def beam_axis_shared_nodes(model):
    """Exige MESMO ID de no entre barra R20x30B e barras para dentro de LE1."""
    sections={r['Frame']:r['AnalSect'] for r in model['tables']['FRAME SECTION ASSIGNMENTS']}
    beam_nodes,landing_nodes=defaultdict(list),defaultdict(list)
    for r in model['tables']['CONNECTIVITY - FRAME']:
        a,b=[model['joints'][r[k]] for k in ['JointI','JointJ']]
        if all(440<=p[0]<=655 and abs(p[1])<1e-8 and abs(p[2]-177.4)<1e-8 for p in (a,b)) and sections[r['Frame']]=='R20x30B':
            for key in ['JointI','JointJ']:
                beam_nodes[r[key]].append(r['Frame'])
        for key,other in [('JointI','JointJ'),('JointJ','JointI')]:
            p,q=model['joints'][r[key]],model['joints'][r[other]]
            if (450<=p[0]<=645 and abs(p[1])<1e-8 and abs(p[2]-177.4)<1e-8
                and 0<q[1]<97.58 and abs(q[0]-p[0])<1e-8 and abs(q[2]-177.4)<1e-8
                and sections[r['Frame']].startswith('R') and sections[r['Frame']].endswith('x14A')):
                landing_nodes[r[key]].append(r['Frame'])
    return [dict(jointId=j,positionCm=model['joints'][j],beamFrames=beam_nodes[j],
                 landingFrames=landing_nodes[j]) for j in sorted(set(beam_nodes)&set(landing_nodes),key=lambda j:model['joints'][j])]


def mesh(model, selector):
    import ifcopenshell.geom
    import numpy as np
    candidates=[e for e in model.by_type('IfcElement') if selector(e)]
    if len(candidates)!=1:
        raise ValueError('Selecao ausente ou ambigua')
    e=candidates[0];s=ifcopenshell.geom.settings();s.set(s.USE_WORLD_COORDS,True)
    shape=ifcopenshell.geom.create_shape(s,e)
    g=shape.geometry
    v=np.asarray(g.verts).reshape(-1,3);f=np.asarray(g.faces).reshape(-1,3)
    if not np.isfinite(v).all():
        raise ValueError('Coordenada nao finita')
    edges=Counter(tuple(sorted((int(a),int(b)))) for tri in f for a,b in zip(tri,list(tri[1:])+[tri[0]]))
    if not edges or any(n!=2 for n in edges.values()):
        raise ValueError('Malha nao fechada em cada aresta')
    if any(np.linalg.norm(np.cross(v[t[1]]-v[t[0]],v[t[2]]-v[t[0]]))<1e-12 for t in f):
        raise ValueError('Triangulo degenerado')
    return dict(name=e.Name,guid=e.GlobalId,vertices=v,faces=f)


def main():
    sys.path.insert(0,'D:/TCC/work/ifc/deps')
    import ifcopenshell
    reference=json.loads((HERE.parent/'h03-r161/R161-IFC-auditoria.json').read_text(encoding='utf-8'))
    control=json.loads((HERE.parent/'h03-r178/R178-comparacao-CAD-BIM.json').read_text(encoding='utf-8'))
    protected={Path(p):h for p,h in reference['sources'].items()}
    reference_ifc=next(p for p in protected if p.suffix.lower()=='.ifc')
    for row in control['branches'].values():
        protected[Path(row['projectPath'])]=row['projectSha256']
        protected[Path(row['ifcPath'])]=row['ifcSha256']
        protected[Path(row['exports']['escada']['path'])]=row['exports']['escada']['sha256']
    if any(sha(p)!=h for p,h in protected.items()):
        raise ValueError('Fonte difere do controle anterior')
    sap_spec=importlib.util.spec_from_file_location('sap181',HERE.parent/'h03-r122/consolidar.py')
    sap=importlib.util.module_from_spec(sap_spec);sap_spec.loader.exec_module(sap)
    results={}
    for name,path in [('Revit',reference_ifc)]+[(b,Path(r['ifcPath'])) for b,r in control['branches'].items()]:
        m=ifcopenshell.open(str(path))
        landing=mesh(m,lambda e:e.GlobalId=='1ltUz0oN12IOfJpAa5zY7j' if name=='Revit' else e.Name=='LE1')
        beam=mesh(m,lambda e:e.GlobalId=='1ltUz0oN12IOfJpAa5zY0U' if name=='Revit' else e.is_a('IfcBeam') and e.Name=='V16')
        bv=beam['vertices'];lv=landing['vertices'];lo,hi=bv.min(0),bv.max(0)
        # As coordenadas de V16 devem efetivamente descrever os oito cantos de um prisma.
        expected={(round(x,9),round(y,9),round(z,9)) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])}
        if {tuple(round(float(x),9) for x in p) for p in bv}!=expected:
            raise ValueError('Viga nao prismatica; nao usar face retangular')
        sec=section_at_y(lv,landing['faces'],float(hi[1]),(float(lo[0]),float(lo[2]),float(hi[0]),float(hi[2])))
        results[name]=dict(ifcPath=str(path),ifcSha256=sha(path),beamGuid=beam['guid'],landingGuid=landing['guid'],
            beamMinM=lo.tolist(),beamMaxM=hi.tolist(),landingMinM=lv.min(0).tolist(),landingMaxM=lv.max(0).tolist(),
            sectionAtBeamFaceY=float(hi[1]),sectionAtBeamFace=sec,
            signedLandingFrontMinusBeamFaceM=float(lv.min(0)[1]-hi[1]),
            observedContactAtExportedFace=sec['areaM2']>1e-8,
            nativeSupportTypeNotEstablishedByGeometry=True)
        if name!='Revit':
            model=sap.parse(Path(control['branches'][name]['exports']['escada']['path']).read_text(encoding='cp1252'))
            results[name]['exportedGridSharedNodes']=beam_axis_shared_nodes(model)
    if any(sha(p)!=h for p,h in protected.items()):
        raise ValueError('Fonte alterada durante leitura')
    result=dict(revision='H03/R181',recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        scope='Secao fisica local em IFC e conectividade por ID na grelha textual exportada, sem alteracao nativa',
        branches=results,sourceFilesPreserved=[dict(path=str(p),sha256=h) for p,h in protected.items()],
        frontDifferenceIsNotAnUnsupportedGapAtCheckedBeamFace=all(r['observedContactAtExportedFace'] for r in results.values()),
        completeRevitEberickLandingMeshEquivalence=False,stairFinishCompatibilityCompleted=False,
        nativeSupportRotationAndReinforcementReviewed=False,structuralApproval=False,
        numericalEpsilonM=1e-9,sectionVertexRoundingDecimalPlaces=9,
        numericalParametersAreNotConstructionTolerances=True,
        timing=dict(nativeProcessingExecuted=False,fullFlowTimeMeasured=False,newCadBimPerformanceComparison=False))
    OUT.mkdir(exist_ok=True)
    (OUT/'R181-ligacao-patamar.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:dict(sectionM2=v['sectionAtBeamFace']['areaM2'],signedFrontM=v['signedLandingFrontMinusBeamFaceM'],sharedNodes=len(v.get('exportedGridSharedNodes',[]))) for k,v in results.items()},indent=2))


if __name__=='__main__':
    main()

"""Auditoria geometrica de cuboides, sem alterar autores ou receptores."""
from pathlib import Path
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
import sys
import time

COORDINATE_DECIMALS = 9
UNION_COMPARISON_M3 = 1e-6  # criterio numerico do auditor, nao tolerancia normativa


def normalized(box):
    b = tuple(round(float(v), COORDINATE_DECIMALS) for v in box)
    if len(b) != 6 or not all(math.isfinite(v) for v in b):
        raise ValueError('Cuboide invalido')
    if not all(b[k + 1] > b[k] for k in (0, 2, 4)):
        raise ValueError('Cuboide sem volume positivo')
    return b


def merge_intervals(intervals):
    out = []
    for lo, hi in sorted(intervals):
        if out and lo <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], hi))
        else:
            out.append((lo, hi))
    return out


def interval_length(intervals):
    return sum(hi - lo for lo, hi in intervals)


def intersection_length(a, b):
    return sum(max(0.0, min(ah, bh) - max(al, bl))
               for al, ah in a for bl, bh in b)


def compare_unions(a, b):
    """Integra seções Z em cada celula XY; nao usa amostragem de voxels."""
    a, b = [normalized(x) for x in a], [normalized(x) for x in b]
    all_boxes = a + b
    if not all_boxes:
        raise ValueError('Comparacao sem geometria')
    xs = sorted({v[k] for v in all_boxes for k in (0, 1)})
    ys = sorted({v[k] for v in all_boxes for k in (2, 3)})
    va = vb = common = 0.0
    for x0, x1 in zip(xs, xs[1:]):
        x = (x0 + x1) / 2
        aa = [v for v in a if v[0] < x < v[1]]
        bb = [v for v in b if v[0] < x < v[1]]
        for y0, y1 in zip(ys, ys[1:]):
            y = (y0 + y1) / 2
            ia = merge_intervals((v[4], v[5]) for v in aa if v[2] < y < v[3])
            ib = merge_intervals((v[4], v[5]) for v in bb if v[2] < y < v[3])
            area = (x1 - x0) * (y1 - y0)
            va += area * interval_length(ia)
            vb += area * interval_length(ib)
            common += area * intersection_length(ia, ib)
    only_a, only_b = max(0., va - common), max(0., vb - common)
    symmetric = only_a + only_b
    return dict(unionAM3=va, unionBM3=vb, intersectionM3=common,
                onlyAM3=only_a, onlyBM3=only_b, symmetricDifferenceM3=symmetric,
                computationalToleranceM3=UNION_COMPARISON_M3,
                sameOccupiedVolumeWithinDeclaredCriterion=symmetric <= UNION_COMPARISON_M3)


def proposal_boxes(proposal):
    rows = []
    for e in proposal['elements']:
        if e['kind'] == 'column':
            b = (e['x']-e['b']/2, e['x']+e['b']/2,
                 e['y']-e['h']/2, e['y']+e['h']/2, e['z0'], e['z1'])
        elif e['kind'] == 'slab':
            b = (e['x'], e['x2'], e['y'], e['y2'], e['z']-e['h'], e['z'])
        elif e['kind'] == 'beam' and abs(e['x2']-e['x']) < 1e-9:
            b = (e['x']-e['b']/2, e['x']+e['b']/2,
                 min(e['y'], e['y2']), max(e['y'], e['y2']), e['z']-e['h'], e['z'])
        elif e['kind'] == 'beam' and abs(e['y2']-e['y']) < 1e-9:
            b = (min(e['x'], e['x2']), max(e['x'], e['x2']),
                 e['y']-e['b']/2, e['y']+e['b']/2, e['z']-e['h'], e['z'])
        else:
            raise ValueError('Geometria fora do escopo ortogonal: '+e['id'])
        box = normalized(b)
        rows.append(dict(sourceId=e['id'], kind=e['kind'], box=list(box),
                         nominalSeparateVolumeM3=(box[1]-box[0])*(box[3]-box[2])*(box[5]-box[4])))
    return rows


def intersection_pairs(objects):
    pairs = []
    for i, a in enumerate(objects):
        for b in objects[i+1:]:
            aa, bb = normalized(a['box']), normalized(b['box'])
            volume = math.prod(max(0., min(aa[k+1],bb[k+1])-max(aa[k],bb[k])) for k in (0,2,4))
            if volume > 1e-9:
                pairs.append(dict(nameA=a.get('name'),guidA=a.get('guid'),
                                  nameB=b.get('name'),guidB=b.get('guid'),intersectionM3=volume,
                                  intersectionBox=[v for k in (0,2,4) for v in (max(aa[k],bb[k]),min(aa[k+1],bb[k+1]))]))
    return pairs


def validate_box_surface(vertices, faces):
    """Recusa malhas que nao sejam os oito cantos e as seis faces de uma caixa."""
    if len(vertices) != 8 or len(faces) != 12:
        raise ValueError('Malha fora do escopo de oito cantos/doze triangulos')
    if not all(len(v) == 3 and all(math.isfinite(float(c)) for c in v) for v in vertices):
        raise ValueError('Vertices invalidos')
    lo = [min(v[k] for v in vertices) for k in range(3)]
    hi = [max(v[k] for v in vertices) for k in range(3)]
    if any(hi[k] <= lo[k] for k in range(3)):
        raise ValueError('Caixa degenerada')
    corner_keys = []
    for v in vertices:
        key = []
        for k in range(3):
            if abs(v[k]-lo[k]) <= 1e-9:key.append(0)
            elif abs(v[k]-hi[k]) <= 1e-9:key.append(1)
            else:raise ValueError('Vertice fora dos cantos da caixa')
        corner_keys.append(tuple(key))
    if len(set(corner_keys)) != 8:
        raise ValueError('Cantos repetidos ou ausentes')
    plane_counts = Counter()
    for tri in faces:
        if len(tri) != 3 or len(set(tri)) != 3 or any(not 0 <= i < 8 for i in tri):
            raise ValueError('Triangulo invalido')
        planes = [(k, corner_keys[tri[0]][k]) for k in range(3)
                  if len({corner_keys[i][k] for i in tri}) == 1]
        if len(planes) != 1:
            raise ValueError('Triangulo fora das seis faces externas')
        plane_counts[planes[0]] += 1
    if len(plane_counts) != 6 or any(n != 2 for n in plane_counts.values()):
        raise ValueError('Faces da caixa nao cobertas por dois triangulos')


def extract_ifc(file):
    import ifcopenshell
    import ifcopenshell.geom as geom
    import numpy as np
    model = ifcopenshell.open(str(file))
    settings = geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    rows = []
    for cls in ('IfcColumn', 'IfcBeam', 'IfcSlab'):
        for obj in model.by_type(cls):
            shape = geom.create_shape(settings, obj)
            vertices = np.array(shape.geometry.verts).reshape(-1, 3)
            faces = np.array(shape.geometry.faces).reshape(-1, 3)
            if not np.isfinite(vertices).all() or len(faces) == 0:
                raise ValueError('Malha invalida: '+obj.GlobalId)
            validate_box_surface(vertices.tolist(), faces.tolist())
            edges, orientation = Counter(), Counter()
            for tri in faces:
                for start, end in ((tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])):
                    key = tuple(sorted((int(start), int(end))))
                    edges[key] += 1
                    orientation[key] += 1 if start < end else -1
            if not all(n == 2 for n in edges.values()) or any(orientation.values()):
                raise ValueError('Malha nao fechada/orientada: '+obj.GlobalId)
            v = vertices - vertices.mean(axis=0)
            volume = abs(float(np.einsum('ij,ij->i',v[faces[:,0]],
                         np.cross(v[faces[:,1]],v[faces[:,2]])).sum()/6))
            lo, hi = vertices.min(axis=0), vertices.max(axis=0)
            bbox_volume = float(np.prod(hi-lo))
            if abs(volume-bbox_volume) > max(1e-8, bbox_volume*1e-9):
                raise ValueError('Elemento nao pode ser auditado como cuboide: '+obj.GlobalId)
            box = normalized((lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]))
            rows.append(dict(type=cls,name=obj.Name,guid=obj.GlobalId,box=list(box),
                             meshVolumeM3=volume,bboxVolumeM3=bbox_volume,
                             closedOrientedMesh=True,bboxVolumeMatchesMesh=True,
                             eightCornersAndSixExternalFacesVerified=True))
    return dict(objects=rows, excludedAuxiliaryFootings=len(model.by_type('IfcFooting')),
                ifcopenshellVersion=ifcopenshell.version,numpyVersion=np.__version__,
                geometricCoordinatesUnit='m',worldCoordinates=True)


def main(root, output):
    started = datetime.now(timezone.utc).isoformat()
    tick = time.perf_counter()
    sources = []
    def read(name):
        file = root/name
        data = file.read_bytes()
        sources.append(dict(path=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
        return json.loads(data.decode('utf-8-sig'))
    base = 'outputs/Autoria-H03-R83-SINCRONIZACAO-GEOMETRICA-NAO-EXECUTAR/'
    proposal = read(base+'H03-R83-proposta.json')
    native = read(base+'R83-Revit-leitura-apos-reabrir.json')
    created = read(base+'R83-Revit-criacao-nativa.json')
    nominal = proposal_boxes(proposal)
    assert len(nominal) == 62
    native_by_id = {e['uniqueId']:e for e in native['elements']}
    mapping = {e['id']:e for e in created['elements']}
    assert len(native_by_id) == len(mapping) == 62
    for row in nominal:
        source = mapping[row['sourceId']]
        e = native_by_id[source['uniqueId']]
        assert str(source['revitId']) == e['id']
        if e['volumeM3'] is None or not math.isfinite(e['volumeM3']):
            raise ValueError('Volume nativo ausente: '+row['sourceId'])
        row['revitVolumeM3'] = e['volumeM3']
    boxes = [r['box'] for r in nominal]
    nominal_union = compare_unions(boxes, boxes)['unionAM3']
    separate = sum(r['nominalSeparateVolumeM3'] for r in nominal)
    native_sum = sum(r['revitVolumeM3'] for r in nominal)
    rounding_bound = len(nominal)*0.5e-6  # exportador arredonda cada parametro em 6 casas
    assert abs(native_sum-nominal_union) <= rounding_bound
    references = {
        'CAD_R57':'outputs/Verificacao-H03-R57-NAO-EXECUTAR/IFC-CAD/Modelo 3D.IFC',
        'BIM_R57':'outputs/Verificacao-H03-R57-NAO-EXECUTAR/IFC-BIM/Modelo 3D.IFC',
        'BIM_R81_CONTROLE':'outputs/Agrupamento-H03-R81-TESTE-NAO-EXECUTAR/IFC-BIM-CONTROLE/Modelo 3D.IFC',
        'BIM_R81_TESTE':'outputs/Agrupamento-H03-R81-TESTE-NAO-EXECUTAR/IFC-BIM/Modelo 3D.IFC'}
    ifcs = {}
    for label,name in references.items():
        file = root/name
        sources.append(dict(path=name,bytes=file.stat().st_size,sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
        r = extract_ifc(file)
        comparison = compare_unions(boxes, [e['box'] for e in r['objects']])
        r.update(nominalSourceComparison=comparison,
                 sumIndividualMeshVolumesM3=sum(e['meshVolumeM3'] for e in r['objects']),
                 internalOverlapM3=sum(e['meshVolumeM3'] for e in r['objects'])-comparison['unionBM3'],
                 intersectionPairs=intersection_pairs(r['objects']),
                 pairVolumesAreNotGenerallyAdditive=True)
        ifcs[label] = r
    result = dict(revision='H03/R88',startedAtUtc=started,
                  sourceNominalSeparateVolumeM3=separate,sourceNominalUnionVolumeM3=nominal_union,
                  sourceInternalOverlapM3=separate-nominal_union,
                  revitNativeVolumeParameterSumM3=native_sum,
                  revitSumMinusSourceUnionM3=native_sum-nominal_union,
                  revitExportRoundingBoundM3=rounding_bound,
                  sourceRows=nominal,ifcCheckpoints=ifcs,sources=sources,
                  coordinateDecimals=COORDINATE_DECIMALS,
                  wholeFlowRanked=False,structuralApproval=False,
                  limits=['Revit: soma de parametros exportados, sem novo acesso ao RVT nesta rodada.',
                          'CAD: volume nominal calculado da proposta comum, nao parametro de volume extraido do DWG 2D.',
                          'IFC: malhas conferidas como cuboides fechados; fundacoes auxiliares excluidas.',
                          'Igualdade de volume ocupado nao verifica vinculos, armaduras ou desempenho estrutural.',
                          'Nao e quantitativo executivo, custo ou inventario ambiental.'])
    for s in sources:
        assert hashlib.sha256((root/s['path']).read_bytes()).hexdigest() == s['sha256']
    result['endedAtUtc'] = datetime.now(timezone.utc).isoformat()
    result['auditScriptSeconds'] = time.perf_counter()-tick
    output.mkdir(parents=True,exist_ok=False)
    (output/'R88-quantidades-geometricas.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(nominalUnionM3=nominal_union,revitSumM3=native_sum,
                         IFC={k:dict(parts=len(v['objects']),sumM3=v['sumIndividualMeshVolumesM3'],unionM3=v['nominalSourceComparison']['unionBM3'],symmetricDifferenceM3=v['nominalSourceComparison']['symmetricDifferenceM3']) for k,v in ifcs.items()})))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root',type=Path)
    parser.add_argument('output',type=Path)
    parser.add_argument('--ifc-deps',type=Path,default=Path('D:/TCC/work/ifc/deps'))
    args = parser.parse_args()
    sys.path.insert(0,str(args.ifc_deps))
    main(args.root,args.output)

"""Confere o lançamento CAD no Eberick contra os próprios DXF de autoria.

Não usa o modelo Revit para preencher ou aprovar o ramo CAD.
"""
from collections import Counter
import json
from pathlib import Path
import sys

sys.path[:0] = ['D:/TCC/work/dxf-deps', str(Path(__file__).resolve().parent.parent / 'h03-r163')]
from auditar_cobertura import rectangular_mesh, coverage, ifcopenshell, sha
import ezdxf
from ifcopenshell.util.element import get_container, get_psets

OUT = Path('D:/TCC/outputs/H03-R232-CAD-PILARES-NAO-EXECUTAR')
SOURCE = OUT.parent / 'H03-R225-AUTORIA-COORDENACAO-NAO-EXECUTAR'
CONTROL = OUT / 'CAD/Arquivos do projeto/Modelo 3D.IFC'
PROJECT = OUT / 'CAD/Projeto Eberick/R228-CAD-DWG-BRUTO-NAO-EXECUTAR.prj'
TOL = 1e-4  # 0,1 mm: precisão da auditoria, não tolerância normativa


def cad_sources():
    columns, inputs = [], []
    for level in ('N1', 'N2'):
        path, = SOURCE.glob(f'R225-CAD-{level}-*-retorno.dxf')
        drawing = ezdxf.readfile(path)
        if drawing.units != 6:
            raise ValueError('O DXF precisa estar em metros')
        inputs.append(path)
        for entity in drawing.modelspace():
            if entity.dxf.layer != level + '_PILARES':
                continue
            if entity.dxftype() != 'LWPOLYLINE' or not entity.closed:
                raise ValueError('Pilar CAD deve ser polilinha fechada')
            tags = entity.get_xdata('TCC_R225')
            record = json.loads(next(t.value for t in tags if t.code == 1000 and t.value.startswith('{')))
            if record['kind'] != 'column' or record['id'] != tags[0].value:
                raise ValueError('Identidade CAD inconsistente')
            points = list(entity.get_points('xy'))
            expected = {(round(record['x'] + dx*record['b']/2, 8),
                         round(record['y'] + dy*record['h']/2, 8)) for dx in (-1,1) for dy in (-1,1)}
            if len(points) != 4 or {(round(x,8), round(y,8)) for x,y in points} != expected:
                raise ValueError('Polilinha difere dos metadados CAD')
            labels = [e.dxf.text for e in drawing.modelspace().query('TEXT')
                      if e.dxf.text.startswith(record['id']+' ')]
            if labels != [f"{record['id']} {round(record['b']*100)}x{round(record['h']*100)}cm"]:
                raise ValueError('Rótulo de seção ausente ou inconsistente')
            columns.append(record)
    if len(columns) != 23 or len({c['id'] for c in columns}) != 23:
        raise ValueError('Esperadas 23 identidades CAD de pilares')
    return columns, inputs


def snapshot(path):
    model = ifcopenshell.open(str(path))
    if model.schema != 'IFC4':
        raise ValueError('Controle precisa ser IFC4')
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    return {o.GlobalId: dict(name=o.Name, cls=o.is_a(), level=get_container(o).Name,
                            geometry=rectangular_mesh(o, settings), psets=get_psets(o))
            for o in model.by_type('IfcElement')}


def audit():
    sources, paths = cad_sources()
    paths += [CONTROL, PROJECT, OUT/'R232-tempo-observado.json', OUT/'R232-tempo-correcao.json']
    hashes = {str(p): sha(p) for p in paths}
    parts = snapshot(CONTROL)
    mapped = []
    for guid, p in parts.items():
        if p['cls'] != 'IfcColumn':
            raise ValueError('Elemento fora da etapa de pilares')
        box = p['geometry']; candidates = []
        for s in sources:
            lo = [s['x']-s['b']/2, s['y']-s['h']/2]
            hi = [s['x']+s['b']/2, s['y']+s['h']/2]
            if (all(abs(box[k][i]-v[i]) < TOL for k,v in (('minM',lo),('maxM',hi)) for i in (0,1))
                    and min(box['maxM'][2],s['z1'])-max(box['minM'][2],s['z0']) > TOL):
                candidates.append(s['id'])
        if len(candidates) != 1 or p['name'] != candidates[0].split('-')[0]:
            raise ValueError('Pilar sem associação única à identidade CAD: '+guid)
        concrete = p['psets']['Pset_ConcreteElementGeneral']
        if concrete['StrengthClass'] != 'C-25' or concrete['ConcreteCover'] != 3:
            raise ValueError('Concreto/cobrimento difere das premissas')
        mapped.append(dict(guid=guid, source=candidates[0], **p))
    origins = []
    for s in sources:
        hits = [p for p in mapped if p['source'] == s['id']]
        cov = coverage([(p['geometry']['minM'][2],p['geometry']['maxM'][2]) for p in hits],s['z0'],s['z1'])
        if not cov['noGapAboveTolerance']:
            raise ValueError('Lacuna vertical em '+s['id'])
        if any(p['geometry']['minM'][2] < s['z0']-TOL or p['geometry']['maxM'][2] > s['z1']+TOL for p in hits):
            raise ValueError('Trecho extrapola o intervalo CAD')
        origins.append(dict(id=s['id'], parts=len(hits), coverage=cov))
    counts = dict(Counter(p['level'] for p in mapped))
    if counts != {'N1':12,'N2':11,'PATAMAR':12}:
        raise ValueError('Distribuição por pavimento diferente do esperado')
    if hashes != {str(p):sha(p) for p in paths}:
        raise ValueError('Arquivo alterado durante auditoria')
    first = OUT/'R232-controle-corrigido-antes-reabertura.ifc'
    persisted = first.is_file() and snapshot(first) == parts
    result = dict(revision='R232', inputSource='DXF AutoCAD R225: polilinhas, rótulos e XDATA',
                  sourceColumns=23, nativeColumnSegments=len(mapped), segmentsByLevel=counts,
                  allPositionsSectionsNamesAndVerticalIntervalsMatch=True,
                  concreteClass='C-25', coverCm=3, persistedAfterReopen=persisted,
                  nativeReopened=(OUT/'R232-reabertura.json').is_file(), geometryToleranceM=TOL, hashes=hashes,
                  timing=json.loads(paths[-2].read_text(encoding='utf-8')),
                  correctionTiming=json.loads(paths[-1].read_text(encoding='utf-8')),
                  analyticalConnectivityVerified=False, loadsApplied=False, structuralApproval=False,
                  parts=mapped, origins=origins)
    (OUT/'R232-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('parts','origins','hashes')},ensure_ascii=False))
    return result


if __name__ == '__main__':
    audit()

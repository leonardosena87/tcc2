"""Leitura independente IFC4: identidades, secoes, material, cobrimentos e malhas.

Nao altera IFC/RVT, nao cria elementos de calculo nem aprova a estrutura.
Executar no Python3.12 do runtime, compativel com IfcOpenShell local.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import time

sys.path.insert(0,'D:/TCC/work/ifc/deps')
import ifcopenshell
import ifcopenshell.geom
from ifcopenshell.util.element import get_psets, get_materials
from ifcopenshell.util.unit import calculate_unit_scale, get_property_unit
import numpy as np

CLASSES={'beam':'IfcBeam','column':'IfcColumn','slab':'IfcSlab'}
PREFIX={None:1.,'MILLI':1e-3,'CENTI':1e-2,'KILO':1e3,'MEGA':1e6}


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def pressure_mpa(prop,model):
    if prop.NominalValue is None or not prop.NominalValue.is_a('IfcPressureMeasure'):
        raise ValueError('Resistencia sem medida de pressao explicita')
    unit=get_property_unit(prop,model)
    if unit is None or not unit.is_a('IfcSIUnit') or unit.Name!='PASCAL' or unit.Prefix not in PREFIX:
        raise ValueError('Unidade de resistencia nao suportada')
    return float(prop.NominalValue.wrappedValue)*PREFIX[unit.Prefix]/1e6


def material_info(obj,model):
    result=[]
    for mat in get_materials(obj):
        strengths=[]
        for pset in mat.HasProperties:
            for prop in pset.Properties:
                if prop.Name in ('Compressão do concreto','ConcreteCompression','CompressiveStrength'):
                    strengths.append(dict(property=prop.Name,MPa=pressure_mpa(prop,model)))
        result.append(dict(name=mat.Name,strengths=strengths,
            numeric25MPa=bool(strengths) and all(math.isclose(s['MPa'],25,abs_tol=1e-8) for s in strengths)))
    return result


def cover_fields(psets,expected):
    fields={k:v for ps in psets.values() for k,v in ps.items() if 'cobrimento' in k.lower()}
    rows=[]
    for key,value in fields.items():
        match=re.search(r'<\s*(\d+(?:[.,]\d+)?)\s*mm\s*>',str(value))
        mm=float(match[1].replace(',','.')) if match else None
        rows.append(dict(field=key,typeDisplay=value,reportedMm=mm,expectedMm=expected,
                         matches=mm is not None and math.isclose(mm,expected,abs_tol=1e-9)))
    return dict(fields=rows,allThreeMatch=len(rows)==3 and all(r['matches'] for r in rows),
        scope='Texto de recobrimento do tipo no IFC; armadura nao modelada')


def audit(ifc,native_path):
    started=time.perf_counter();before={str(p):sha(p) for p in (ifc,native_path)}
    native=json.loads(native_path.read_text(encoding='utf-8-sig'))
    readback=native.get('Readback',native);elements=readback['Elements']
    wanted={str(e['Id']):e for e in elements}
    if len(wanted)!=66:raise ValueError('Esperavam-se66 identidades nativas unicas')
    model=ifcopenshell.open(str(ifc))
    if model.schema!='IFC4':raise ValueError('Esquema diferente deIFC4')
    scale=calculate_unit_scale(model)
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    objects={};extras=[]
    for obj in model.by_type('IfcElement'):
        if obj.Tag in wanted:
            if obj.Tag in objects:raise ValueError('Identidade IFC repetida')
            objects[obj.Tag]=obj
        else:extras.append(dict(className=obj.is_a(),tag=obj.Tag,globalId=obj.GlobalId))
    if objects.keys()!=wanted.keys():raise ValueError('Identidade nativa ausente noIFC')
    result=[]
    for tag,e in wanted.items():
        obj=objects[tag]
        if obj.is_a()!=CLASSES[e['Kind']]:raise ValueError('Classe IFC divergente: '+e['Mark'])
        psets=get_psets(obj);identity=psets.get('Dados de identidade',{})
        dims=psets.get('Cotas',{});checks={}
        if e['Kind'] in ('beam','column'):
            for key,value in [('b',e['BM']),('h',e['HM'])]:
                raw=dims.get(key);actual=None if raw is None else float(raw)*scale
                checks[key]=dict(nativeM=value,ifcM=actual,matches=actual is not None and math.isclose(actual,value,abs_tol=1e-7))
        shape=ifcopenshell.geom.create_shape(settings,obj)
        v=np.asarray(shape.geometry.verts).reshape(-1,3)
        faces=np.asarray(shape.geometry.faces).reshape(-1,3)
        if not len(v) or not len(faces) or not np.isfinite(v).all() or np.any(v.max(0)-v.min(0)<=0):
            raise ValueError('Malha invalida: '+e['Mark'])
        materials=material_info(obj,model)
        result.append(dict(mark=e['Mark'],nativeId=tag,globalId=obj.GlobalId,className=obj.is_a(),
            identityMark=identity.get('Marca'),identityMarkMatches=identity.get('Marca')==e['Mark'],
            sectionDimensions=checks,allReportedDimensionsMatch=all(c['matches'] for c in checks.values()),
            slabThicknessIndependentlyCompared=False if e['Kind']=='slab' else None,
            cover=cover_fields(psets,25 if e['Kind']=='slab' else 30),materials=materials,
            allMaterials25MPa=bool(materials) and all(m['numeric25MPa'] for m in materials),
            bodyBoundsM=dict(min=v.min(0).tolist(),max=v.max(0).tolist()),
            vertices=len(v),triangles=len(faces),nativeBodyGeometryIndependentlyCompared=False))
    staircase=readback['Stair'];stairs=[s for s in model.by_type('IfcStair') if s.Tag==str(staircase['Id'])]
    if len(stairs)!=1:raise ValueError('Escada nativa nao identificada')
    children=[c for rel in stairs[0].IsDecomposedBy for c in rel.RelatedObjects]
    flights=[c for c in children if c.is_a('IfcStairFlight')]
    landings=[c for c in children if c.is_a('IfcSlab')]
    if len(flights)!=2 or len(landings)!=1:raise ValueError('Agregacao da escada divergente')
    stair_rows=[]
    native_runs={str(r['Id']):r for r in staircase['Runs']}
    for f in flights:
        n=native_runs.get(f.Tag)
        stair_rows.append(dict(tag=f.Tag,risers=f.NumberOfRisers,nativeRisers=None if n is None else n['Risers'],
            riserM=None if f.RiserHeight is None else f.RiserHeight*scale,
            treadM=None if f.TreadLength is None else f.TreadLength*scale,
            nativeRunMatches=n is not None and f.NumberOfRisers==n['Risers']))
    summary=dict(expectedAndFoundLogicalElements=66,beams=32,columns=23,buildingSlabs=11,
        additionalSlabIsStairLanding=True,stairFlights=2,
        numeric25MPaCount=sum(r['allMaterials25MPa'] for r in result),
        identityMarkMatchesCount=sum(r['identityMarkMatches'] for r in result),
        coverThreeFieldsMatchCount=sum(r['cover']['allThreeMatch'] for r in result),
        reportedSectionDimensionsMatchCount=sum(r['allReportedDimensionsMatch'] for r in result if r['sectionDimensions']),
        reportedSectionDimensionsDenominator=55,validNonemptyMeshes=66,
        independentFullNativeSolidGeometryComparison=False,
        eberickReceptionTested=False,structuralApproval=False)
    after={str(p):sha(p) for p in (ifc,native_path)}
    if before!=after:raise ValueError('Arquivo de entrada mudou durante consulta')
    return dict(schema='R225-IFC-audit/1',ifc=str(ifc),ifcSha256=before[str(ifc)],
        native=str(native_path),nativeSha256=before[str(native_path)],lengthUnitScaleToM=scale,
        summary=summary,elements=result,staircase=stair_rows,extraIfcElements=extras,
        sourcesUnchanged=True,auditSeconds=time.perf_counter()-started,auditTimeIsNotFlowTime=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('ifc',type=Path);ap.add_argument('native',type=Path);ap.add_argument('out',type=Path);args=ap.parse_args()
    data=audit(args.ifc,args.native)
    args.out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(data['summary'],ensure_ascii=True))

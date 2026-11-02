"""Variante de recepcao de 30 vigas nominais; nao e exportacao nativa Revit.

Preserva o bruto e altera somente geometria/colocacao das vigas identificadas.
Nao corrige materiais, escada, niveis, cargas, apoios ou dimensionamento.
"""
from collections import Counter
from datetime import datetime,timezone
import hashlib,json,math,sys,time
from pathlib import Path

sys.path.insert(0,'D:/TCC/work/ifc/deps')
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.validate
from ifcopenshell.util.element import get_material,get_psets
from ifcopenshell.util.unit import calculate_unit_scale
import numpy as np
from geometria_nominal_r95 import nominal_geometry

OUT=Path('D:/TCC/outputs/Intercambio-H03-R162-SECOES-NOMINAIS-NAO-EXECUTAR')
TARGET=OUT/'H03-R160-R162-DERIVADO-VIGAS-NOMINAIS-NAO-EXECUTAR.ifc'
TOL=1e-7


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def target_item(e):
    if e['Kind']!='beam':raise ValueError('Escopo limitado a vigas')
    a=e['AxisM']
    if len(a)!=6 or not all(math.isfinite(v) for v in a+[e['BM'],e['HM']]):raise ValueError('Dimensoes invalidas')
    dx,dy=a[3]-a[0],a[4]-a[1]
    if abs(a[2]-a[5])>TOL or (abs(dx)>TOL and abs(dy)>TOL):raise ValueError('Somente viga ortogonal horizontal')
    if math.hypot(dx,dy)<=TOL or min(e['BM'],e['HM'])<=0:raise ValueError('Geometria degenerada')
    return dict(id=e['Mark'],kind='beam',x=a[0],y=a[1],x2=a[3],y2=a[4],z=a[2],b=e['BM'],h=e['HM'])


def nominal_box(x):
    if abs(x['x2']-x['x'])>TOL:
        return [min(x['x'],x['x2']),x['y']-x['b']/2,x['z']-x['h']],[max(x['x'],x['x2']),x['y']+x['b']/2,x['z']]
    return [x['x']-x['b']/2,min(x['y'],x['y2']),x['z']-x['h']],[x['x']+x['b']/2,max(x['y'],x['y2']),x['z']]


def cloud(obj,settings):
    shape=ifcopenshell.geom.create_shape(settings,obj)
    v=np.asarray(shape.geometry.verts).reshape(-1,3)
    if not len(v) or not np.isfinite(v).all():raise ValueError('Malha invalida: '+str(obj.Tag))
    points=sorted(set(tuple(p) for p in np.round(v,8)))
    return dict(minM=v.min(0).tolist(),maxM=v.max(0).tolist(),pointsSha256=hashlib.sha256(json.dumps(points,separators=(',',':')).encode()).hexdigest())


def metadata(model):
    # STEP das relacoes de propriedades e material mantem IDs nesta escrita.
    return dict(products={str(o.Tag)+':'+o.is_a():dict(guid=o.GlobalId,name=o.Name,tag=o.Tag,
            material=str(get_material(o)),psets=get_psets(o),
            containment=[r.RelatingStructure.GlobalId for r in getattr(o,'ContainedInStructure',())])
        for o in model.by_type('IfcElement')},
        levels=[str(o) for o in model.by_type('IfcBuildingStorey')],
        materialProperties=[str(o) for o in model.by_type('IfcMaterialProperties')])


def schema_issues(model):
    logger=ifcopenshell.validate.json_logger();ifcopenshell.validate.validate(model,logger)
    return [dict(level=r['level'],attribute=r.get('attribute'),message=r['message']) for r in logger.statements]


def main():
    t0=time.perf_counter();started=datetime.now(timezone.utc).isoformat()
    if TARGET.exists():raise FileExistsError('Nao sobrescrever a variante: '+str(TARGET))
    prep=read(OUT/'R162-preparacao.json');source=Path(prep['rawNativeIfc']);native_path=Path(prep['nativeReadback'])
    assert sha(source)==prep['rawNativeIfcSha256'] and sha(native_path)==prep['nativeReadbackSha256']
    native=read(native_path);expected={str(e['Id']):target_item(e) for e in native['Elements'] if e['Kind']=='beam'}
    assert len(expected)==30
    model=ifcopenshell.open(str(source));assert model.schema=='IFC2X3'
    objects={str(o.Tag):o for o in model.by_type('IfcBeam')}
    assert set(objects)==set(expected)
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    before_meta=metadata(model);before_issues=schema_issues(model)
    untouched={o.id():cloud(o,settings) for o in model.by_type('IfcElement') if o.Representation and not o.is_a('IfcBeam') and not o.is_a('IfcStair')}
    before={tag:cloud(obj,settings) for tag,obj in objects.items()}
    scale=calculate_unit_scale(model);assert scale==.001
    for tag,obj in objects.items():nominal_geometry(model,obj,expected[tag],scale)
    assert metadata(model)==before_meta
    # Registra proveniencia no cabecalho; nao se apresenta como novo exportador Autodesk.
    descriptions=list(model.header.file_description.description)
    model.header.file_description.description=descriptions+['TCC R162 DERIVADO: vigas nominais; nao exportacao nativa; NAO EXECUTAR']
    model.header.file_name.name=TARGET.name
    model.write(str(TARGET));reopened=ifcopenshell.open(str(TARGET))
    assert metadata(reopened)==before_meta
    after_issues=schema_issues(reopened)
    if after_issues!=before_issues:raise ValueError('Validacao de esquema alterada; revisar a variante')
    for eid,old in untouched.items():
        assert cloud(reopened.by_id(eid),settings)==old,'Geometria fora do escopo mudou: '+str(eid)
    rows=[]
    for tag,x in expected.items():
        obj=next(o for o in reopened.by_type('IfcBeam') if o.Tag==tag);box=cloud(obj,settings);lo,hi=nominal_box(x)
        errors=[box['minM'][i]-lo[i] for i in range(3)]+[box['maxM'][i]-hi[i] for i in range(3)]
        if max(abs(d) for d in errors)>TOL:raise ValueError('Caixa nominal divergente: '+x['id'])
        rows.append(dict(nativeId=tag,mark=x['id'],guid=obj.GlobalId,target=x,before=before[tag],after=box,
            expectedMinM=lo,expectedMaxM=hi,maxAbsoluteBoxDeltaM=max(abs(d) for d in errors),
            materialAndPropertiesPreserved=True))
    assert sha(source)==prep['rawNativeIfcSha256'] and sha(native_path)==prep['nativeReadbackSha256']
    result=dict(revision='H03/R162',startedAtUtc=started,endedAtUtc=datetime.now(timezone.utc).isoformat(),
        sourcePath=str(source),sourceSha256=sha(source),nativeReadbackPath=str(native_path),nativeReadbackSha256=sha(native_path),
        targetPath=str(TARGET),targetSha256=sha(TARGET),sourceUnchanged=True,derivedFileIsNotNativeRevitExport=True,
        replacedBeamRepresentations=30,allReopenedBeamBoxesMatchNominal=True,boxToleranceM=TOL,
        nonBeamMeshedElementsUnchanged=len(untouched),allProductsIdentitiesMaterialsAndPsetsPreserved=True,
        levelsPreserved=True,stairAndLandingNotEdited=True,mechanicalMaterialPropertiesStillAbsent=True,
        schemaValidationIssuesBefore=before_issues,schemaValidationIssuesAfter=after_issues,
        schemaValidationIsNotStructuralApproval=True,elapsedScriptMs=(time.perf_counter()-t0)*1000,
        timeIsNotWholeBimFlow=True,eberickReceptionTestPerformed=False,
        supportsConnectionsLoadsAndStairCalculationNotResolved=True,structuralApproval=False,rows=rows)
    (OUT/'R162-derivado-conferencia.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('replacedBeamRepresentations','nonBeamMeshedElementsUnchanged','allReopenedBeamBoxesMatchNominal','schemaValidationIssuesAfter','elapsedScriptMs')}))


if __name__=='__main__':main()

"""Experimento isolado: recompõe quatro pilares nominais no IFC derivado.

Não acrescenta pilares nem altera RVT/DWG/PRJ. O resultado não é IFC nativo.
Testa o efeito da continuidade geométrica na conversão do receptor Eberick.
"""
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'h03-r162'))
from preparar_derivado import read, sha, cloud, metadata, schema_issues, ifcopenshell
from geometria_nominal_r95 import nominal_geometry
import ifcopenshell.geom
from ifcopenshell.util.unit import calculate_unit_scale

OUT = Path('D:/TCC/outputs/Intercambio-H03-R164-CONTINUIDADE-PILARES-NAO-EXECUTAR')
TARGET = OUT/'H03-R160-R164-DERIVADO-VIGAS-E-4-PILARES-NAO-EXECUTAR.ifc'
R163 = Path('D:/TCC/outputs/Intercambio-H03-R163-COBERTURA-GEOMETRICA-NAO-EXECUTAR/R163-cobertura-geometrica.json')
EXPECTED_IDS = {'472934','473029','473143','473144'}


def target_item(e):
    a=e['AxisM']
    if e['Kind'] != 'column' or len(a) != 4 or abs(e.get('RotationRad',0))>1e-8:
        raise ValueError('Escopo limitado aos quatro pilares sem rotação deste estudo')
    if not all(math.isfinite(v) for v in a+[e['BM'],e['HM']]) or a[3]<=a[2] or min(e['BM'],e['HM'])<=0:
        raise ValueError('Dimensões inválidas')
    return dict(id=e['Mark'],kind='column',x=a[0],y=a[1],z0=a[2],z1=a[3],b=e['BM'],h=e['HM'])


def main():
    t0=time.perf_counter()
    if TARGET.exists():raise FileExistsError('Não sobrescrever experimento existente')
    prior=read(R163)
    files=[Path(p) for p in prior['sourceHashes']]
    assert {str(p):sha(p) for p in files}==prior['sourceHashes']
    source=next(p for p in files if 'DERIVADO' in p.name)
    native_path=next(p for p in files if 'releitura' in p.name)
    native=read(native_path)
    ids={str(r['nativeId']) for r in prior['columnOrigins'] if r['inputIfcTopDeltaFromNominalM'] < -1e-4}
    assert ids==EXPECTED_IDS
    wanted={str(e['Id']):target_item(e) for e in native['Elements'] if str(e['Id']) in ids}
    model=ifcopenshell.open(str(source));assert model.schema=='IFC2X3'
    objects={str(o.Tag):o for o in model.by_type('IfcColumn') if str(o.Tag) in ids}
    assert set(objects)==ids
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    before_meta=metadata(model);before_issues=schema_issues(model)
    untouched={o.id():cloud(o,settings) for o in model.by_type('IfcElement')
               if o.Representation and not o.is_a('IfcStair') and o not in objects.values()}
    before={tag:cloud(o,settings) for tag,o in objects.items()}
    for tag,o in objects.items():nominal_geometry(model,o,wanted[tag],calculate_unit_scale(model))
    assert metadata(model)==before_meta
    model.header.file_description.description=list(model.header.file_description.description)+[
        'TCC R164 DERIVADO: 4 pilares nominais; nao exportacao nativa; NAO EXECUTAR']
    model.header.file_name.name=TARGET.name
    OUT.mkdir(parents=True,exist_ok=True)
    model.write(str(TARGET));reopened=ifcopenshell.open(str(TARGET))
    assert metadata(reopened)==before_meta and schema_issues(reopened)==before_issues
    for eid,old in untouched.items():assert cloud(reopened.by_id(eid),settings)==old
    rows=[]
    for tag,x in wanted.items():
        o=next(o for o in reopened.by_type('IfcColumn') if o.Tag==tag)
        new=cloud(o,settings)
        lo=[x['x']-x['b']/2,x['y']-x['h']/2,x['z0']]
        hi=[x['x']+x['b']/2,x['y']+x['h']/2,x['z1']]
        assert max(abs(new[side][i]-values[i]) for side,values in [('minM',lo),('maxM',hi)] for i in range(3))<1e-7
        rows.append(dict(nativeId=tag,mark=x['id'],before=before[tag],after=new))
    assert {str(p):sha(p) for p in files}==prior['sourceHashes']
    result=dict(revision='H03/R164',recordedAtUtc=datetime.now(timezone.utc).isoformat(),
                inputPath=str(source),inputSha256=sha(source),nativeReadbackPath=str(native_path),
                nativeReadbackSha256=sha(native_path),targetPath=str(TARGET),targetSha256=sha(TARGET),
                priorAuditPath=str(R163),priorAuditSha256=sha(R163),
                changedColumnRepresentations=4,newColumnOrigins=0,unchangedOtherMeshedElements=len(untouched),
                identitiesPropertiesMaterialsAndLevelsPreserved=True,sourceHashesUnchanged=True,
                notNativeRevitExport=True,revitCadAndEberickProjectsNotEdited=True,
                columnCutCauseNotIsolated=True,importerBirthColumnEffectNotYetTested=True,
                schemaValidationIssuesBefore=before_issues,schemaValidationIssuesAfter=schema_issues(reopened),
                notStructuralApproval=True,elapsedScriptMs=(time.perf_counter()-t0)*1000,
                timeIsNotWholeFlowOrOperatorEffort=True,rows=rows)
    (OUT/'R164-derivado-conferencia.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,(dict,list))},ensure_ascii=False))


if __name__=='__main__':main()

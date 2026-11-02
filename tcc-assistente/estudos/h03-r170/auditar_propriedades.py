"""Compara informação IFC explicitamente exportada, sem inferir cargas ausentes."""
from collections import Counter
from datetime import datetime,timezone
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'h03-r167'))
from auditar_lajes import read,sha,ifcopenshell,properties,mesh,points,compare_points
from auditar_receptor import association,NATIVE,endpoint_supports,column_box,XY_TOL,Z_TOL,rectangular_mesh
import ifcopenshell.geom

OUT=Path('D:/TCC/outputs/Intercambio-H03-R170-PROPRIEDADES-NAO-EXECUTAR')
PATHS={'CAD_R165':Path('D:/TCC/outputs/Intercambio-H03-R165-CAD-GEOMETRIA-NAO-EXECUTAR/IFC-CAD-Eberick/Modelo 3D.IFC'),
       'BIM_R169':Path('D:/TCC/outputs/R169-BIM-VINCULO-VARANDA-NAO-EXECUTAR/Arquivos do projeto/Modelo 3D.IFC')}
LOADSET='AltoQi_Eberick_Cargas'
MATERIALSETS=('Pset_ConcreteElementGeneral','AltoQi_Eberick_Padrão')

def canonical(value):return json.dumps(value,sort_keys=True,ensure_ascii=False)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    hashes={str(p):sha(p) for p in [*PATHS.values(),NATIVE]}
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    native=read(NATIVE)['Elements'];sources=[e for e in native if e['Kind']=='beam']
    branches={};models={};parts={}
    for branch,path in PATHS.items():
        model=ifcopenshell.open(str(path));models[branch]=model;parts[branch]=[]
        for obj in model.by_type('IfcBeam'):
            part=dict(name=obj.Name,guid=obj.GlobalId,geometry=rectangular_mesh(obj,settings),properties=properties(obj))
            found=[r for e in sources if (r:=association(part,e,endpoint_supports(e,native)))]
            if len(found)!=1:raise ValueError('Viga sem correspondencia unica: '+branch+':'+obj.Name)
            part['origin']=found[0];parts[branch].append(part)
        branches[branch]=dict(path=str(path),productClasses=dict(Counter(o.is_a() for o in model.by_type('IfcProduct'))),
            explicitIfcStructuralLoadOrActionEntities=dict(Counter(o.is_a() for o in model if 'Load' in o.is_a() or 'Action' in o.is_a())),
            beamParts=len(parts[branch]),beamOrigins=len({r['origin']['nativeId'] for r in parts[branch]}))
    beam_rows=[]
    for e in sources:
        grouped={b:[p for p in ps if p['origin']['nativeId']==e['Id']] for b,ps in parts.items()}
        load_values={b:sorted({canonical(p['properties'].get(LOADSET)) for p in ps}) for b,ps in grouped.items()}
        material_values={b:sorted({canonical({s:p['properties'].get(s) for s in MATERIALSETS}) for p in ps}) for b,ps in grouped.items()}
        # Somente conjunto uniforme ao longo de todas as partes é comparável por este atalho.
        uniform=all(len(v)==1 and v[0]!='null' for v in load_values.values())
        beam_rows.append(dict(nativeId=e['Id'],nativeMark=e['Mark'],receiverNamesByBranch={b:[p['name'] for p in ps] for b,ps in grouped.items()},
            exportedUniformLoadSetsEqual=uniform and len(set(canonical(v) for v in load_values.values()))==1,
            exportedLoadSetsByBranch={b:[json.loads(s) for s in v] for b,v in load_values.items()},
            exportedMaterialSetsEqual=len(set(canonical(v) for v in material_values.values()))==1))
    assert len(beam_rows)==30 and all(r['exportedUniformLoadSetsEqual'] and r['exportedMaterialSetsEqual'] for r in beam_rows)
    cad_slabs=list(models['CAD_R165'].by_type('IfcSlab'));slab_rows=[]
    for obj in models['BIM_R169'].by_type('IfcSlab'):
        matches=[o for o in cad_slabs if compare_points(points(obj,settings),points(o,settings))['matches']]
        assert len(matches)==1
        other=matches[0]
        slab_rows.append(dict(bimName=obj.Name,bimGuid=obj.GlobalId,cadName=other.Name,cadGuid=other.GlobalId,
            exportedPropertySetsEqual=properties(obj)==properties(other),rawLoadSet=properties(obj).get(LOADSET)))
    assert len(slab_rows)==11 and len({r['cadGuid'] for r in slab_rows})==11 and all(r['exportedPropertySetsEqual'] for r in slab_rows)
    column_rows=[]
    for e in native:
        if e['Kind']!='column':continue
        box=column_box(e);by_branch={}
        for branch,model in models.items():
            matches=[]
            for obj in model.by_type('IfcColumn'):
                g=mesh(obj,settings)
                if all(abs(g[side][i]-box[side][i])<=XY_TOL for side in ('minM','maxM') for i in (0,1)) and min(g['maxM'][2],box['maxM'][2])-max(g['minM'][2],box['minM'][2])>XY_TOL:matches.append(obj)
            assert len(matches)==1
            by_branch[branch]=properties(matches[0])
        column_rows.append(dict(nativeId=e['Id'],nativeMark=e['Mark'],exportedPropertySetsEqual=len(set(canonical(p) for p in by_branch.values()))==1))
    assert len(column_rows)==22 and all(r['exportedPropertySetsEqual'] for r in column_rows)
    all_zero=all(all(v==0 for v in values.values()) for r in beam_rows for sets in r['exportedLoadSetsByBranch'].values() for values in sets)
    result=dict(revision='H03/R170',recordedAtUtc=datetime.now(timezone.utc).isoformat(),sourceHashes=hashes,
        scope='Receptores ja corrigidos CAD R165 e BIM R169; comparacao restrita a informacao explicitamente exportada.',
        sourcesUnchanged=hashes=={str(p):sha(p) for p in [*PATHS.values(),NATIVE]},branches=branches,
        beamOriginsWithEqualExportedUniformLoadSets=sum(r['exportedUniformLoadSetsEqual'] for r in beam_rows),
        beamExportedLoadFieldsAllZero=all_zero,beamOriginsWithEqualExportedMaterialSets=30,
        slabsWithEqualExportedPropertySets=11,columnsWithEqualExportedPropertySets=22,
        sourceNamesAloneNotUsedForMatching=True,rawIfcValuesComparedWithoutUnitConversion=True,
        beamPsetZerosDoNotProveNoAuxiliaryOrPointLoads=True,fullLoadInventoryVerified=False,
        roofWallTankLoadsEquivalenceVerified=False,allNativeBoundaryConditionsCompared=False,
        footingCountExcludedFromSuperstructureMetric=True,foundationDesignInScope=False,
        newStructuralCalculationPerformed=False,structuralApproval=False,fullFlowTimeCompared=False,
        beamPairs=beam_rows,slabPairs=slab_rows,columnPairs=column_rows)
    assert result['sourcesUnchanged']
    (OUT/'R170-propriedades-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('sourceHashes','beamPairs','slabPairs','columnPairs')},ensure_ascii=False))

if __name__=='__main__':main()

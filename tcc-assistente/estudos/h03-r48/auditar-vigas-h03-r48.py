"""Auditoria geometrica H03/R48 CAD. Nao modifica IFC ou projeto nativo.

Uso: python auditar-vigas-h03-r48.py arquivo.ifc inicial|reaberto
Reutiliza as mesmas regras R17/R46 de conciliacao espacial de vigas.
"""
from pathlib import Path
from datetime import datetime, timezone
import copy, hashlib, json, shutil, sys

ROOT=Path('D:/TCC')
OUT=ROOT/'outputs/Complementacao-H03-R48-VIGAS-CAD-NAO-EXECUTAR'
PROPOSAL=ROOT/'outputs/Alternativa-H03-R43-ESTUDO-NAO-EXECUTAR/H03-R43-proposta.json'
RULES=ROOT/'outputs/Reauditoria-H02-R17-NAO-EXECUTAR/auditar-geometria-h02-r17.py'
source=Path(sys.argv[1]); suffix=sys.argv[2]
assert suffix in ('inicial','reaberto')
sys.path.insert(0,str(ROOT/'work/ifc/deps'))
import ifcopenshell
import ifcopenshell.geom as geom
import ifcopenshell.validate
import ifcopenshell.util.unit as iu
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,o:p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
model=ifcopenshell.open(str(source)); settings=geom.settings()
settings.set(settings.USE_WORLD_COORDS,True)
rows=[]
for cls in ('IfcColumn','IfcBeam','IfcSlab'):
    for obj in model.by_type(cls):
        v=geom.create_shape(settings,obj).geometry.verts
        rows.append(dict(**{'class':cls},name=obj.Name,guid=obj.GlobalId,
                         min=[min(v[i::3]) for i in range(3)],
                         max=[max(v[i::3]) for i in range(3)]))
logger=ifcopenshell.validate.json_logger()
ifcopenshell.validate.validate(model,logger)
native=dict(source=str(source),sha256=sha(source),geometry=rows,schema=model.schema,
            lengthUnitToMeters=iu.calculate_unit_scale(model),
            counts={c:len(model.by_type(c)) for c in ('IfcColumn','IfcBeam','IfcSlab')},
            schemaValidationMessages=[dict(level=r['level'],attribute=r.get('attribute'),
                    message=r['message'],instance=str(r.get('instance'))) for r in logger.statements])
code=RULES.read_text(encoding='utf-8').split('result=audit(native')[0]
code=code.replace("proposal_path=root.parent/'Alternativa-H02-R12-NAO-EXECUTAR/H02-R12-proposta.json'",'proposal_path=provided_proposal')
code=code.replace("native=load(root/'R17-geometria-nativa.json')",'native=provided_native')
code=code.replace('len(colrows)==20 and len(set(colIds))==20','len(colrows)==len(columns) and len(set(colIds))==len(columns)')
ns=dict(__file__=str(RULES),provided_proposal=PROPOSAL,provided_native=native)
exec(compile(code,str(RULES),'exec'),ns)
audit=ns['audit']; result=audit(rows)
beam=next(r for r in rows if r['class']=='IfcBeam')
changed=copy.deepcopy(rows)
next(r for r in changed if r['class']=='IfcBeam')['min'][2]-=.01
controls=dict(missingBeamPartDetected=not audit([r for r in rows if r is not beam])['geometryPass'],
              changedBeamHeightDetected=not audit(changed)['geometryPass'],
              duplicatedBeamPartDetected=not audit(rows+[beam])['geometryPass'])
assert all(controls.values())
proposal=json.loads(PROPOSAL.read_text(encoding='utf-8-sig'))
result.update(atUtc=datetime.now(timezone.utc).isoformat(),sourceIfc=str(source),sourceSha256=sha(source),
    proposalRunId=proposal['runId'],proposalSha256=sha(PROPOSAL),rulesSource=str(RULES),rulesSha256=sha(RULES),
    comparisonToleranceM=ns['TOL'],exportedCounts=native['counts'],sensitivityControls=controls,
    schemaValidationMessageCount=len(logger.statements),structuralCalculationPerformed=False,
    missingSlabIds=[e['id'] for e in proposal['elements'] if e['kind']=='slab'],
    limits=['Caixas envolventes e cobertura axial de vigas descontando pilares.',
            'Correspondencia espacial independente dos nomes nativos e da divisao em trechos.',
            'Tolerancia computacional 0,00001 m, nao normativa.',
            'Nao comprova conectividade analitica, cargas, materiais, apoios, ELU/ELS ou armaduras.',
            'Lajes ainda nao lancadas no receptor CAD.'])
if suffix=='reaberto':
    before=json.loads((OUT/'R48-geometria-inicial.json').read_text(encoding='utf-8'))
    canon=lambda rr:sorted((r['class'],r['name'],r['guid'],tuple(round(v,6) for v in r['min']+r['max'])) for r in rr)
    result['sameGeometryAndGuidsAfterReopen']=canon(rows)==canon(before['geometry'])
write(OUT/f'R48-geometria-{suffix}.json',native)
write(OUT/f'R48-auditoria-vigas-{suffix}.json',result)
shutil.copy2(source,OUT/f'R48-pilares-vigas-{suffix}.ifc')
print(json.dumps({k:result[k] for k in ('geometryPass','columnSegmentsMatching','missingColumnIds',
    'duplicateColumnIds','matchedLogicalBeams','logicalBeamsPassing','unmatchedBeamParts','exportedCounts',
    'schemaValidationMessageCount')},indent=2))
if not result['geometryPass']:
    print(json.dumps([b for b in result['beams'] if not all(b['checks'].values())],indent=2))
assert result['geometryPass'],'Divergencia geometrica: investigar antes de aceitar.'
if suffix=='reaberto':assert result['sameGeometryAndGuidsAfterReopen']

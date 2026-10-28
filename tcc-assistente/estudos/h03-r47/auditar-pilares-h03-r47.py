"""Audita exclusivamente a geometria dos pilares H03 no receptor CAD R47.

Entrada IFC nativa preservada, sem modificar o projeto. Nao calcula estrutura.
Uso: python auditar-pilares-h03-r47.py caminho.ifc inicial|reaberto
"""
from pathlib import Path
from datetime import datetime, timezone
import collections, copy, hashlib, json, shutil, sys

ROOT = Path('D:/TCC')
OUT = ROOT/'outputs/Complementacao-H03-R47-CAD-NAO-EXECUTAR'
PROPOSAL = ROOT/'outputs/Alternativa-H03-R43-ESTUDO-NAO-EXECUTAR/H03-R43-proposta.json'
source = Path(sys.argv[1])
suffix = sys.argv[2]
assert suffix in ('inicial', 'reaberto')
sys.path.insert(0, str(ROOT/'work/ifc/deps'))
import ifcopenshell
import ifcopenshell.geom as geom
import ifcopenshell.validate
import numpy as np

sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
proposal = json.loads(PROPOSAL.read_text(encoding='utf-8-sig'))
expected = [e for e in proposal['elements'] if e['kind']=='column']
assert len(expected)==22
model = ifcopenshell.open(str(source))
settings = geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)
rows = []
for obj in model.by_type('IfcColumn'):
    shape = geom.create_shape(settings, obj)
    vertices = np.array(shape.geometry.verts).reshape(-1,3)
    rows.append(dict(name=obj.Name, guid=obj.GlobalId,
                     min=vertices.min(axis=0).tolist(),
                     max=vertices.max(axis=0).tolist()))
TOL = 1e-5

def audit(items):
    matches = []
    for row in items:
        found = [e['id'] for e in expected if
                 np.allclose(row['min'], [e['x']-e['b']/2,e['y']-e['h']/2,e['z0']],atol=TOL,rtol=0) and
                 np.allclose(row['max'], [e['x']+e['b']/2,e['y']+e['h']/2,e['z1']],atol=TOL,rtol=0)]
        matches.append(dict(**row, sourceIds=found))
    ids = [r['sourceIds'][0] for r in matches if len(r['sourceIds'])==1]
    missing = sorted({e['id'] for e in expected}-set(ids))
    duplicates = sorted(i for i,n in collections.Counter(ids).items() if n>1)
    unmatched = [r['name'] for r in matches if len(r['sourceIds'])!=1]
    return dict(columns=matches, missingIds=missing, duplicateIds=duplicates,
                unmatchedNames=unmatched,
                geometryPass=len(items)==len(expected) and not missing and not duplicates and not unmatched)

result = audit(rows)
altered = copy.deepcopy(rows)
altered[0]['max'][2] -= .01
controls = dict(missingColumnDetected=not audit(rows[1:])['geometryPass'],
                changedHeightDetected=not audit(altered)['geometryPass'],
                duplicateColumnDetected=not audit(rows+[rows[0]])['geometryPass'])
assert all(controls.values()), controls
logger = ifcopenshell.validate.json_logger()
ifcopenshell.validate.validate(model, logger)
result.update(atUtc=datetime.now(timezone.utc).isoformat(), source=str(source), sha256=sha(source),
              proposal=str(PROPOSAL), proposalSha256=sha(PROPOSAL), proposalRunId=proposal['runId'],
              schema=model.schema, computationalToleranceM=TOL, sensitivityControls=controls,
              counts={c:len(model.by_type(c)) for c in ('IfcColumn','IfcBeam','IfcSlab')},
              schemaValidationMessages=[dict(level=s['level'],attribute=s.get('attribute'),message=s['message']) for s in logger.statements],
              structuralCalculationPerformed=False,
              limits=['Caixas envolventes de pilares; tolerancia computacional, nao normativa.',
                      'Nao verifica conectividade analitica, cargas, materiais, estabilidade, ELU/ELS ou armaduras.',
                      'Vigas e lajes graficas importadas nao sao elementos calculaveis.',
                      'P11 parametrizado em b=20,h=30 cm e rotacao=90 graus para representar 30 cm em X e 20 cm em Y.'])
if suffix=='reaberto':
    initial=json.loads((OUT/'R47-auditoria-pilares-inicial.json').read_text(encoding='utf-8'))
    canon=lambda rr: sorted((r['name'],r['guid'],tuple(round(v,6) for v in r['min']+r['max'])) for r in rr)
    result['sameGeometryAndGuidsAfterReopen']=canon(rows)==canon(initial['columns'])
    assert result['sameGeometryAndGuidsAfterReopen']
(OUT/f'R47-auditoria-pilares-{suffix}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(source, OUT/f'R47-pilares-{suffix}.ifc')
print(json.dumps({k:result[k] for k in ('counts','geometryPass','missingIds','duplicateIds','unmatchedNames','sensitivityControls')},indent=2))
if not result['geometryPass']:
    print(json.dumps(rows,indent=2))
assert result['geometryPass'], 'Divergencia geometrica, conferir o lancamento antes de avancar.'

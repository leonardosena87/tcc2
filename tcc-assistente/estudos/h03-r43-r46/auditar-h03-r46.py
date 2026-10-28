"""Auditoria prospectiva do estado recebido H03; nao modifica RVT/IFC/PRJ.

Reutiliza as regras geometricas R17, trocando explicitamente a proposta e o
numero esperado de pilares. Conserva regras e dados de origem em disco.
"""
from pathlib import Path
from datetime import datetime, timezone
import collections, hashlib, json, re, shutil, sys, zipfile
import xml.etree.ElementTree as ET

ROOT = Path('D:/TCC')
OUT = ROOT/'outputs/Intercambio-H03-R46-BIM-NAO-EXECUTAR'
SRC = ROOT/'outputs/H03_BIM_R46_IFC_NAO_EXECUTAR'
PROPOSAL = ROOT/'outputs/Alternativa-H03-R43-ESTUDO-NAO-EXECUTAR/H03-R43-proposta.json'
CREATION = PROPOSAL.parent/'R43-revit-criacao-salva.json'
RULES = ROOT/'outputs/Reauditoria-H02-R17-NAO-EXECUTAR/auditar-geometria-h02-r17.py'
IFC = SRC/'Arquivos do projeto/Modelo 3D.IFC'
REPORT = SRC/'Arquivos do projeto/Documentos/Eberick/Relatorio_de_importacao_de_elementos_IFC.docx'
load = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT/'work/ifc/deps'))
import ifcopenshell
import ifcopenshell.geom as geom
import ifcopenshell.util.element as ie
import ifcopenshell.util.unit as iu
import ifcopenshell.validate

model = ifcopenshell.open(str(IFC))
settings = geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)
rows = []
for cls in ('IfcColumn', 'IfcBeam', 'IfcSlab'):
    for obj in model.by_type(cls):
        shape = geom.create_shape(settings, obj)
        verts = shape.geometry.verts
        rows.append(dict(class_=cls, name=obj.Name, guid=obj.GlobalId,
                         min=[min(verts[i::3]) for i in range(3)],
                         max=[max(verts[i::3]) for i in range(3)],
                         psets=ie.get_psets(obj)))
for row in rows:
    row['class'] = row.pop('class_')
logger = ifcopenshell.validate.json_logger()
ifcopenshell.validate.validate(model, logger)
native = {'source':str(IFC), 'sha256':sha(IFC), 'geometry':rows,
          'schema':model.schema, 'lengthUnitToMeters':iu.calculate_unit_scale(model),
          'counts':{c:len(model.by_type(c)) for c in ('IfcColumn','IfcBeam','IfcSlab')},
          'schemaValidationMessages':[
              {'level':r['level'], 'attribute':r.get('attribute'),
               'instance':str(r.get('instance')), 'message':r['message']}
              for r in logger.statements]}

# Somente definicoes: nao executa a auditoria historica nem suas gravacoes.
code = RULES.read_text(encoding='utf-8').split('result=audit(native')[0]
code = code.replace("proposal_path=root.parent/'Alternativa-H02-R12-NAO-EXECUTAR/H02-R12-proposta.json'",
                    'proposal_path=provided_proposal')
code = code.replace("native=load(root/'R17-geometria-nativa.json')", 'native=provided_native')
code = code.replace('len(colrows)==20 and len(set(colIds))==20',
                    'len(colrows)==len(columns) and len(set(colIds))==len(columns)')
ns = {'__file__':str(RULES), 'provided_proposal':PROPOSAL, 'provided_native':native}
exec(compile(code, str(RULES), 'exec'), ns)
audit = ns['audit']
result = audit(rows)
removed = next(r for r in rows if r['class']=='IfcBeam')
changed = json.loads(json.dumps(rows))
next(r for r in changed if r['class']=='IfcBeam')['min'][2] -= .01
controls = {
    'missingBeamPartDetected':not audit([r for r in rows if r is not removed])['geometryPass'],
    'changedBeamHeightDetected':not audit(changed)['geometryPass'],
    'duplicatedBeamPartDetected':not audit(rows+[removed])['geometryPass']}
assert all(controls.values()), controls

with zipfile.ZipFile(REPORT) as z:
    xml = ET.fromstring(z.read('word/document.xml'))
wns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
paras = [''.join(t.text or '' for t in p.findall('.//w:t',wns))
         for p in xml.findall('.//w:p',wns)]
report_text = '\n'.join(paras)
reported_ids = [int(re.search(r':(\d+) - Pavimento IFC:',p).group(1))
                for p in paras if p.startswith('Nome IFC:')]
creation = load(CREATION)
mapping = {e['revitId']:e['id'] for e in creation['elements']}
proposal = load(PROPOSAL)
expected = {e['id'] for e in proposal['elements'] if e['kind'] in ('column','beam')}
matched = [mapping[i] for i in reported_ids if i in mapping]
report_audit = {
    'source':str(REPORT), 'sha256':sha(REPORT), 'reportedSourceRecords':len(reported_ids),
    'matchedSourceIds':matched,
    'unknownRevitIds':[i for i in reported_ids if i not in mapping],
    'missingColumnBeamSourceIds':sorted(expected-set(matched)),
    'duplicateSourceIds':sorted({i for i in matched if matched.count(i)>1}),
    'reportedKinds':dict(collections.Counter(i.split('-')[0][0] for i in matched)),
    'limits':'Lista de origens importadas; nao prova conectividade ou preservacao de parametros.'}
assert len(reported_ids)==51 and set(matched)==expected
assert not report_audit['duplicateSourceIds'] and not report_audit['unknownRevitIds']
result.update({
    'atUtc':datetime.now(timezone.utc).isoformat(), 'sourceIfc':str(IFC),
    'sourceSha256':sha(IFC), 'proposalRunId':proposal['runId'], 'proposalSha256':sha(PROPOSAL),
    'rulesSource':str(RULES), 'rulesSha256':sha(RULES),
    'comparisonToleranceM':ns['TOL'], 'exportedCounts':native['counts'],
    'missingSlabIds':[e['id'] for e in proposal['elements'] if e['kind']=='slab'],
    'slabsNativeReceived':native['counts']['IfcSlab'],
    'sensitivityControls':controls, 'schemaValidationMessageCount':len(logger.statements),
    'structuralCalculationPerformed':False,
    'limits':[
        'Equivalencia nominal de caixas envolventes e cobertura axial, descontando pilares.',
        'Correspondencia espacial independente da renumeracao nativa.',
        'Tolerancia computacional de 0,00001 m; nao normativa.',
        'Nao verifica conectividade analitica, cargas, materiais completos, apoios, estabilidade ou ELU/ELS.',
        '11 lajes ausentes desta exportacao; preservacao apenas de pilares/vigas avaliada.',
        'Geometria e aviso inicial preservados antes de correcoes ou complementacoes.']})
for name, value in [('R46-geometria-inicial.json',native),
                    ('R46-auditoria-pilares-vigas.json',result),
                    ('R46-auditoria-relatorio-importacao.json',report_audit)]:
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'R46-relatorio-importacao.txt').write_text(report_text,encoding='utf-8')
shutil.copy2(REPORT, OUT/'R46-relatorio-importacao.docx')
shutil.copy2(IFC, OUT/'R46-estrutura-recebida-Eberick.ifc')
print(json.dumps({k:result[k] for k in ('geometryPass','columnSegmentsMatching',
    'missingColumnIds','duplicateColumnIds','matchedLogicalBeams','logicalBeamsPassing',
    'unmatchedBeamParts','exportedCounts','schemaValidationMessageCount')},indent=2))

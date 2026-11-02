"""Audita a alteração analítica real exportada pelo Eberick, sem executar SAP."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import importlib.util
import json
import math
from pathlib import Path
import shutil
import zipfile

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R173-PATAMAR-ANALITICO-NAO-EXECUTAR')

def module(name,rel):
 spec=importlib.util.spec_from_file_location(name,HERE.parent/rel)
 result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result

sap=module('sap_r173','h03-r122/consolidar.py')
summary=module('summary_r173','h03-r172/consolidar.py')
sha=sap.sha

def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def edges(model):return Counter(tuple(sorted(v)) for v in model['frames'].values())
def section_map(model):return {r['Frame']:r['AnalSect'] for r in model['tables']['FRAME SECTION ASSIGNMENTS']}
def section_properties(model):return {r['SectionName']:tuple(sorted((k,v) for k,v in r.items() if k!='SectionName')) for r in model['tables']['FRAME SECTION PROPERTIES 01 - GENERAL']}
def joint_force_evidence(model):
 totals=defaultdict(lambda:[0.]*6);rows=[]
 for r in model['tables']['JOINT LOADS - FORCE']:
  values=[sap.number(r[k]) for k in ['F1','F2','F3','M1','M2','M3']]
  totals[r['LoadPat']]=[a+b for a,b in zip(totals[r['LoadPat']],values)]
  rows.append(dict(positionCm=model['joints'][r['Joint']],pattern=r['LoadPat'],vector=values))
 return dict(totalsOfNodalTableOnlyKgfCm=dict(totals),rows=rows,
  scope='Somente tabela JOINT LOADS - FORCE; nao soma cargas de barras e nao representa o total da estrutura.')

def vertical_coverage(model):
 positions=defaultdict(list)
 for key,(a,b) in model['frames'].items():
  if a[:2]==b[:2] and a[2]!=b[2]:positions[a[:2]].append((min(a[2],b[2]),max(a[2],b[2])))
 merged={}
 for xy,rows in positions.items():
  result=[]
  for lo,hi in sorted(rows):
   if result and lo<result[-1][1]-1e-8:raise ValueError('Barras verticais sobrepostas')
   if result and abs(lo-result[-1][1])<1e-8:result[-1]=(result[-1][0],hi)
   else:result.append((lo,hi))
  merged[xy]=result
 return merged

def target_beam(model,z):
 expected=((441.,0.,z),(654.,0.,z))
 matches=[k for k,v in model['frames'].items() if tuple(v)==expected]
 if len(matches)!=1:raise ValueError('Viga de patamar ausente ou ambigua na cota esperada')
 return matches[0]

def assert_landing_connectivity(model,beam,z):
 rows={r['Frame']:r for r in model['tables']['CONNECTIVITY - FRAME']}
 graph=defaultdict(set)
 for r in rows.values():graph[r['JointI']].add(r['JointJ']);graph[r['JointJ']].add(r['JointI'])
 row=rows[beam]
 for x,beam_joint in [(440.,row['JointI']),(655.,row['JointJ'])]:
  candidates=[k for k,p in model['joints'].items() if p==(x,0.,z)]
  if len(candidates)!=1 or candidates[0] not in graph[beam_joint]:raise ValueError('Ligacao rigida da viga ao pilar ausente')
  joint=candidates[0]
  vertical=[]
  for r in rows.values():
   if joint in (r['JointI'],r['JointJ']):
    a,b=model['frames'][r['Frame']]
    if a[:2]==b[:2] and a[2]!=b[2]:vertical.append((min(a[2],b[2]),max(a[2],b[2])))
  if sorted(vertical)!=[(20.,z),(z,320.)]:raise ValueError('Pilar nao continuo no no do patamar')

def compare(a,b):
 before=target_beam(a,320.);after=target_beam(b,177.4)
 try:target_beam(b,320.)
 except ValueError:pass
 else:raise ValueError('Viga antiga duplicada em N1')
 assert_landing_connectivity(b,after,177.4)
 ca,cb=vertical_coverage(a),vertical_coverage(b)
 if ca!=cb or len(cb)!=11:raise ValueError('Mudanca na cobertura vertical ou nas posicoes de pilares')
 ea,eb=edges(a),edges(b)
 removed=list((ea-eb).elements());added=list((eb-ea).elements())
 expected_removed=[];expected_added=[]
 for x,y in ca:
  expected_removed.append(((x,y,20.),(x,y,320.)))
  expected_added.extend([((x,y,20.),(x,y,177.4)),((x,y,177.4),(x,y,320.))])
 for x1,x2 in [(440.,441.),(441.,654.),(654.,655.)]:
  expected_removed.append(((x1,0.,320.),(x2,0.,320.)))
  expected_added.append(((x1,0.,177.4),(x2,0.,177.4)))
 if Counter(removed)!=Counter(expected_removed) or Counter(added)!=Counter(expected_added):raise ValueError('Alteracao geometrica fora do escopo')
 pa,pb=section_properties(a),section_properties(b)
 if Counter(pa.values())!=Counter(pb.values()):raise ValueError('Propriedades das secoes alteradas')
 sa,sb=section_map(a),section_map(b)
 # Há barras auxiliares coincidentes de propriedades diferentes: conservar o multiconjunto.
 expected_sections=Counter()
 relocation={tuple(sorted(e)) for e in expected_removed if e[0][2]==e[1][2]}
 for k,(p,q) in a['frames'].items():
  if p[:2]==q[:2] and sorted([p[2],q[2]])==[20.,320.]:
   r=(*p[:2],177.4);segments=[(p,r),(r,q)]
  elif tuple(sorted((p,q))) in relocation:segments=[((*p[:2],177.4),(*q[:2],177.4))]
  else:segments=[(p,q)]
  for ends in segments:expected_sections[(tuple(sorted(ends)),pa[sa[k]])]+=1
 actual_sections=Counter((tuple(sorted(ends)),pb[sb[k]]) for k,ends in b['frames'].items())
 if expected_sections!=actual_sections:raise ValueError('Atribuicoes de secoes fora das alteracoes previstas')
 if pa[sa[before]]!=pb[sb[after]]:raise ValueError('Secao da viga do patamar mudou')
 # Contagens de forças não demonstram igualdade de posições, sentidos ou valores.
 joint_loads=lambda m:Counter((m['joints'][r['Joint']],tuple(sorted((k,v) for k,v in r.items() if k!='Joint'))) for r in m['tables']['JOINT LOADS - FORCE'])
 patterns=a['tables']['LOAD PATTERN DEFINITIONS']==b['tables']['LOAD PATTERN DEFINITIONS']
 if not patterns:raise ValueError('Padroes de acoes alterados')
 return dict(beforeBeamFrameId=before,afterBeamFrameId=after,beforeElevationCm=320.,afterElevationCm=177.4,
  verticalColumnPositions=11,verticalCoverageEqual=True,noNewPhysicalColumnPositions=True,
  allGeometryChangesExplainedByBeamRelocationAndElevenColumnSubdivisions=True,
  frameCounts=dict(before=len(a['frames']),after=len(b['frames'])),
  jointCounts=dict(before=len(a['joints']),after=len(b['joints'])),
  sectionPropertiesEqual=True,sectionAssignmentsConserved=True,beamConnectedThroughRigidLinksToContinuousColumns=True,
  jointForcesAtGlobalPositionsEqual=joint_loads(a)==joint_loads(b),loadPatternDefinitionsEqual=patterns,
  removedEdgesCm=removed,addedEdgesCm=added,fullAnalyticalLoadEquivalenceClaimed=False)

def main():
 prep=read(OUT/'R173-preparacao-plano.json');source=Path(prep['sourceRoot']);target=Path(prep['targetRoot'])
 for e in prep['sourceFiles']:
  if sha(source/e['relativePath'])!=e['sha256']:raise ValueError('Fonte R172 alterada')
 models={};exports={}
 for kind in ['antes','depois']:
  p=OUT/f'analitico-{kind}/portico_SAP2000_elastico.$2k';models[kind]=sap.parse(p.read_text(encoding='cp1252'))
  exports[kind]=dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size,zLevelsCm=sorted({p[2] for p in models[kind]['joints'].values()}))
 comparison=compare(models['antes'],models['depois'])
 write(OUT/'R173-forcas-nodais-exportadas.json',{k:joint_force_evidence(v) for k,v in models.items()})
 raw=(OUT/'R173-resumo-resultados.txt').read_text(encoding='utf-8')
 if 'R173-BIM-PATAMAR-ANALITICO-NAO-EXECUTAR' not in raw:raise ValueError('Resumo de outro projeto')
 current=summary.extract(raw.replace('R173-BIM-PATAMAR-ANALITICO-NAO-EXECUTAR','R172-BIM-DIAGNOSTICO-PARCIAL-NAO-EXECUTAR'),'BIM')
 previous=read(OUT.parent/'Analise-H03-R172-DIAGNOSTICO-PARCIAL-NAO-EXECUTAR/R172-resultado.json')['branches']['BIM']['summary']
 if current['verticalLoadsDisplayedTf']!=previous['verticalLoadsDisplayedTf']:raise ValueError('Parcelas verticais exibidas diferem')
 t=read(OUT/'R173-correcao-fim-primeiro-save.json');elapsed=t['fim']['ms']-t['inicio']['ms'];assert elapsed>0
 prjs=list(target.rglob('*.prj'));assert len(prjs)==1
 with zipfile.ZipFile(prjs[0]) as z:assert z.testzip() is None
 frozen=OUT/'R173-receptor-congelado';frozen.mkdir(exist_ok=True);entries=[]
 for p in sorted(target.rglob('*')):
  if not p.is_file() or p.suffix.lower() in ('.log','.errlog'):continue
  rel=p.relative_to(target);dest=frozen/rel
  if dest.exists() and sha(dest)!=sha(p):raise ValueError('Nao substituir receptor congelado divergente')
  dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);assert sha(p)==sha(dest)
  entries.append(dict(relativePath=str(rel),sha256=sha(p),bytes=p.stat().st_size))
 result=dict(revision='H03/R173',recordedAtUtc=datetime.now(timezone.utc).isoformat(),analyticalComparison=comparison,
  exports=exports,sourceFilesPreserved=len(prep['sourceFiles']),sourceFilesUnchanged=True,
  firstSavedPrjSha256=sha(OUT/'R173-primeiro-save-antes-analise.prj'),finalProjectPath=str(prjs[0]),finalProjectSha256=sha(prjs[0]),
  frozenFiles=entries,summaryBefore=previous,summaryAfter=current,displayedVerticalLoadsUnchanged=True,
  correctionIntervalMs=elapsed,correctionIntervalIncludesToolLatencyAndVerification=True,
  processingObservation=read(OUT/'R173-analise-tempo.json'),fullFlowTime=False,
  sapSoftwareExecuted=False,staticAnalysisWithWarnings=True,dimensioningPerformed=False,
  allRoofLoadsTransferred=False,stairIntegratedInReceiver=False,finalStructuralApproval=False)
 write(OUT/'R173-resultado.json',result)
 print(json.dumps(dict(geometry=comparison,correctionMs=elapsed,projectSha256=result['finalProjectSha256']),ensure_ascii=False))

if __name__=='__main__':main()

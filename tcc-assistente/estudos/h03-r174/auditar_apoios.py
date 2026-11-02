"""Confere somente os cinco apoios de cobertura restaurados na R174."""
from pathlib import Path
import hashlib,json,math,re,shutil,zipfile
OUT=Path('D:/TCC/outputs/Cargas-H03-R174-RESTAURACAO-BIM-NAO-EXECUTAR')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def extract(text,action,expected):
 if 'R174-BIM-CARGAS-COBERTURA-NAO-EXECUTAR' not in text:raise ValueError('Projeto incorreto')
 actual=set(re.findall(r'caixa de combinação \(settable, string\) Ação Value: ([^\n]+?) ID: 115',text))
 if actual!={action}:raise ValueError('Acao divergente')
 values={}
 for k in ['Fx','Fy','Fz','Mx','My','Mz']:
  rows=set(re.findall(r'editar \(settable, string\) '+k+r' Value: (\S+) ID:',text))
  if len(rows)!=1:raise ValueError('Componente ausente ou contraditorio')
  value=float(rows.pop())
  if not math.isfinite(value) or abs(value-expected[k])>0.0000051:raise ValueError('Componente divergente: '+k)
  if expected[k] and value*expected[k]<=0:raise ValueError('Sinal divergente')
  values[k]=value
 return values
def main():
 prep=read(OUT/'R174-preparacao-plano.json');target=Path(prep['targetRoot']);source=Path(prep['sourceRoot'])
 for e in prep['sourceFiles']:assert sha(source/e['relativePath'])==e['sha256']
 for e in prep['sourceLoadPlans']:assert sha(Path(e['path']))==e['sha256']
 rows=[r for r in prep['rows'] if r.get('bimPillar')];assert len(rows)==5
 evidence=[];zero={k:0. for k in ['Fx','Fy','Fz','Mx','My','Mz']}
 for row in rows:
  id=row['id'];identity=OUT/f'R174-{id}-identidade-reaberta.txt'
  text=identity.read_text(encoding='utf-8')
  assert f"Nome Value: {row['bimPillar']} ID: 801" in text and 'Croqui-TCC-7a6267fd-N2' in text
  for action,label in [('G','Adicional'),('QT','Q_TELHADO_MANUTENCAO')]:
   before=OUT/f'R174-{id}-{action}-antes.txt'
   if id=='VP1-02' and action=='G':before=OUT/'R174-VP1-02-cargas-iniciais.txt'
   original=extract(before.read_text(encoding='utf-8'),label,zero)
   after=OUT/f'R174-{id}-{action}-reaberto.txt';actual=extract(after.read_text(encoding='utf-8'),label,row[action])
   evidence.append(dict(id=id,pillar=row['bimPillar'],positionCm=[row['xCm'],row['yCm'],row['zCm']],action=action,expected=row[action],displayed=actual,
    originalDisplayed=original,beforeEvidence=before.name,beforeSha256=sha(before),afterEvidence=after.name,afterSha256=sha(after),identitySha256=sha(identity)))
 prjs=list(target.rglob('*.prj'));assert len(prjs)==1
 assert sha(prjs[0])=='8276615ab7bcfb72b8ccd42de467c0f6087225b627bc2486c6578e823871858c'
 with zipfile.ZipFile(prjs[0]) as z:assert z.testzip() is None
 frozen=OUT/'R174-receptor-cinco-apoios-congelado';frozen.mkdir(exist_ok=True);entries=[]
 for p in sorted(target.rglob('*')):
  if not p.is_file() or p.suffix.lower() in ('.log','.errlog'):continue
  rel=p.relative_to(target);dest=frozen/rel
  if dest.exists():assert sha(dest)==sha(p)
  dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);assert sha(p)==sha(dest)
  entries.append(dict(relativePath=str(rel),sha256=sha(p),bytes=p.stat().st_size))
 session=read(OUT/'R174-cinco-apoios-sessao-com-releitura.json');edition=read(OUT/'R174-cinco-apoios-primeiro-save.json')
 for t in [session,edition]:assert t['durationMs']==t['fim']['ms']-t['inicio']['ms']>0
 assert session['inicio']==edition['inicio'] and session['fim']['ms']>edition['fim']['ms']
 result=dict(revision='H03/R174',scope='cinco apoios VP1/P2; RC01-RC13 ainda pendentes',nativeChangesPerformed=True,
  projectPath=str(prjs[0]),projectSha256=sha(prjs[0]),sourceFilesUnchanged=True,protectedSourceFiles=len(prep['sourceFiles']),
  readings=evidence,componentsChecked=60,initialZeroComponentsChecked=60,restoredSupports=5,remainingRoofBeamNodes=13,
  allRoofLoadsRestored=False,calculationPerformed=False,priorAnalysisInvalidatedByLoadEdits=True,
  sessionTime=session,containedEditionTime=edition,doNotAddContainedTimes=True,fullFlowTimeMeasured=False,finalRankingAllowed=False,
  inputPermanentFzKN=sum(r['G']['Fz'] for r in rows),inputMaintenanceFzKN=sum(r['QT']['Fz'] for r in rows),
  sharedSupportContainsVp1AndP2Once=True,forroAlreadyPresentAndNotAddedAgain=True,
  structuralApproval=False,frozenFiles=entries)
 write(OUT/'R174-cinco-apoios-resultado.json',result)
 print(json.dumps(dict(checked=60,restored=5,remaining=13,sessionMs=session['durationMs'],editionMs=edition['durationMs'])))
if __name__=='__main__':main()

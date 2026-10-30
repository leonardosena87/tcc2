"""Mapa de unidades logicas e grupos inferidos do IFC, sem alterar projeto nativo."""
from pathlib import Path
from collections import defaultdict,Counter
from datetime import datetime,timezone
import json,hashlib,shutil,ast
root=Path('D:/TCC');prior=root/'outputs/Vigas-H03-R79-EXPLORATORIO-NAO-EXECUTAR';out=root/'outputs/Agrupamentos-H03-R80-AUDITORIA';repo=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r80');assert not out.exists() and not repo.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(prior/'R79-manifesto.json')['files']
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
sourcePath=root/'outputs/Alternativa-H03-R43-ESTUDO-NAO-EXECUTAR/H03-R43-proposta.json';geoPath=root/'outputs/Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR/R56-geometria-exportada.json';crossPath=root/'outputs/Resultados-H03-R72-PARCIAIS-NAO-FINAIS/R72-mapa-CAD-BIM-65-solidos.json'
source=[r for r in read(sourcePath)['elements'] if r['kind']=='beam'];assert len(source)==29
geo=read(geoPath);cross=read(crossPath);rows=[];tol=1e-5;allowance=.2
for branch,arr in geo.items():
 for r in arr:
  if r['type']!='IfcBeam':continue
  dx=r['max'][0]-r['min'][0];dy=r['max'][1]-r['min'][1];axis=0 if dx>dy else 1;c=1-axis;lo=r['min'][axis];hi=r['max'][axis];center=(r['min'][c]+r['max'][c])/2;keys=('x','y')
  candidates=[e for e in source if abs(e['z']-r['max'][2])<=tol and abs(e[keys[c]]-e[keys[c]+'2'])<=tol and abs(e[keys[c]]-center)<=tol and lo>=min(e[keys[axis]],e[keys[axis]+'2'])-allowance-tol and hi<=max(e[keys[axis]],e[keys[axis]+'2'])+allowance+tol]
  assert len(candidates)==1,(branch,r,candidates)
  e=candidates[0];floor='N1' if abs(e['z']-3.2)<tol else 'N2';key=f'{floor}/{r["name"]}';originLo=min(e[keys[axis]],e[keys[axis]+'2']);originHi=max(e[keys[axis]],e[keys[axis]+'2'])
  row=dict(branch=branch,floor=floor,sourceId=e['id'],nativeName=r['name'],nativeGroupKey=key,guid=r['guid'],min=r['min'],max=r['max'],axis='XY'[axis],sourceEndpointsM=[[e['x'],e['y']],[e['x2'],e['y2']]],sourceHeightM=e['h'],checkpointHeightM=round(r['max'][2]-r['min'][2],6),sourceWidthM=e['b'],checkpointWidthM=round(r['max'][c]-r['min'][c],6),startInsetM=round(lo-originLo,6),endInsetM=round(originHi-hi,6),matchingCandidateCount=1,matchingBasis='eixo ortogonal+centro transversal+cota de topo+contencao longitudinal com margem explicita',analyticalConnectivityVerified=False)
  assert abs(row['checkpointWidthM']-e['b'])<=tol
  if floor=='N1':assert abs(row['checkpointHeightM']-e['h'])<=tol
  else:assert abs(row['checkpointHeightM']-.3)<=tol
  rows.append(row)
assert len(rows)==64
for b in ('CAD','BIM'):
 assert len([r for r in rows if r['branch']==b])==32
 assert {r['sourceId'] for r in rows if r['branch']==b}=={e['id'] for e in source}
for r in cross:
 if r['type']!='IfcBeam':continue
 a=next(x for x in rows if x['branch']=='CAD' and x['guid']==r['CAD_guid']);b=next(x for x in rows if x['branch']=='BIM' and x['guid']==r['BIM_guid']);assert a['sourceId']==b['sourceId']
byGroup=defaultdict(list);bySource=defaultdict(list)
for r in rows:byGroup[r['branch'],r['nativeGroupKey']].append(r);bySource[r['branch'],r['sourceId']].append(r)
groupRows=[]
for (b,key),arr in sorted(byGroup.items()):
 ids=sorted({r['sourceId'] for r in arr});groupRows.append(dict(branch=b,nativeGroupKey=key,sourceIds=ids,solidCount=len(arr),sourceUnitCount=len(ids),mergesDistinctSourceUnits=len(ids)>1,heightVariationM=sorted({r['checkpointHeightM'] for r in arr}),nativeMessageIdentityConfirmed=False))
sourceRows=[]
for e in source:
 refs={b:dict(nativeGroupKeys=sorted({r['nativeGroupKey'] for r in bySource[b,e['id']]}),solidCount=len(bySource[b,e['id']])) for b in ('CAD','BIM')}
 sourceRows.append(dict(sourceId=e['id'],floor='N1' if e['z']==3.2 else 'N2',branches=refs,CADSplitAcrossGroups=len(refs['CAD']['nativeGroupKeys'])>1,BIMSplitAcrossGroups=len(refs['BIM']['nativeGroupKeys'])>1))
summary={b:dict(sourceUnits=29,solids=32,nativeGroupsInferred=len([r for r in groupRows if r['branch']==b]),byFloor={f:dict(sourceUnits=sum(e['id'].endswith(f) for e in source),solids=sum(r['branch']==b and r['floor']==f for r in rows),nativeGroups=sum(r['branch']==b and r['nativeGroupKey'].startswith(f+'/') for r in groupRows)) for f in ('N1','N2')},groupsMergingSourceUnits=sum(r['branch']==b and r['mergesDistinctSourceUnits'] for r in groupRows),sourceUnitsSplitAcrossGroups=sum(r[b+'SplitAcrossGroups'] for r in sourceRows)) for b in ('CAD','BIM')}
assert summary['CAD']['nativeGroupsInferred']==30 and summary['BIM']['nativeGroupsInferred']==20
statuses={b:read(prior/f'{b}-status-estruturado.json') for b in ('CAD','BIM')}
for b in ('CAD','BIM'):
 actual={(r['floor'].split('-')[-1],r['nativeElement']) for r in statuses[b]['messages'] if r['elementType']=='viga'}
 expected={tuple(r['nativeGroupKey'].split('/',1)) for r in groupRows if r['branch']==b};assert actual==expected,(b,actual^expected)
 for r in groupRows:
  if r['branch']==b:r['nativeMessageIdentityConfirmed']=True
out.mkdir();write=lambda n,v:(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write('R80-protegidos-R79.json',protected);write('R80-64-solidos-mapeados.json',rows);write('R80-50-grupos-nativos.json',groupRows);write('R80-29-unidades-origem.json',sourceRows)
sources=[dict(path=str(p),sha256=sha(p)) for p in (sourcePath,geoPath,crossPath)]
write('R80-resultado.json',dict(revision='H03/R80',atUtc=datetime.now(timezone.utc).isoformat(),sources=sources,summary=summary,toleranceNumericM=tol,longitudinalMatchingAllowanceM=allowance,matchingAllowanceIsNotConstructionTolerance=True,allSourceUnitsRepresentedBothBranches=True,allBeamPhysicalCrosswalksMatchSourceId=True,nativeGroupNamesConfirmedByStatusR79=True,causalOriginOfGroupingProven=False,finalErrorRateComputable=False,structuralApproval=False,originalsModified=False))
lines=['| Origem | Grupos CAD | Grupos BIM |','|---|---|---|']
for r in sourceRows:lines.append(f'| {r["sourceId"]} | '+', '.join(r['branches']['CAD']['nativeGroupKeys'])+' | '+', '.join(r['branches']['BIM']['nativeGroupKeys'])+' |')
merges='\n'.join(f'- {r["branch"]} `{r["nativeGroupKey"]}`: '+', '.join(r['sourceIds'])+f'; alturas atuais {r["heightVariationM"]} m.' for r in groupRows if r['mergesDistinctSourceUnits'])
splits='\n'.join(f'- {r["sourceId"]}: CAD '+', '.join(r['branches']['CAD']['nativeGroupKeys'])+'; BIM '+', '.join(r['branches']['BIM']['nativeGroupKeys'])+'.' for r in sourceRows if r['CADSplitAcrossGroups'] or r['BIMSplitAcrossGroups'])
(out/'LEIA-ME-R80.md').write_text('''# H03/R80 — unidades da origem, sólidos e grupos de detalhamento

Auditoria de correspondência, sem alteração de qualquer projeto nativo ou monografia. Usa proposta R43, geometria IFC R56/preservação R57, mapa físico R72 e mensagens reais do processamento exploratório R79.

## Resultado

As **29 unidades lógicas de viga da proposta** (15 em N1 e14 em N2) estão representadas em ambos os receptores. Existem **32 sólidos** por ramo (17 em N1 e15 em N2). Os agrupamentos nativos para cálculo/detalhamento são diferentes: **CAD30** (15+15), **BIM20** (12+8). Confirmou-se cada par pavimento/nome desses grupos nas mensagens nativas R79. Assim,29,32,30 e20 medem objetos diferentes; não representam contagens intercambiáveis de erro, operação ou perda.

A igualdade geométrica dos sólidos não garante que o agrupamento por viga, orientação, seção de apoio, critérios de detalhamento ou vínculo analítico seja o mesmo. Os registros históricos que denominam29 vigas lógicas nos receptores devem ser lidos como29 unidades da proposta representadas, e não como confirmação de29 grupos nativos. Essa distinção complementa os resultados anteriores e não apaga a evidência de disponibilidade inicial nem as complementações realizadas.

## Critério de correspondência

Para cada sólido de viga ortogonal, comparou-se eixo maior XY, centro transversal e cota superior com os segmentos da proposta. Exigiu-se um único candidato por sólido. Na contenção longitudinal usou-se margem declarada de0,20m para extremidades geométricas/apoios; essa margem é um parâmetro de associação e **não tolerância construtiva ou autorização de desalinhamento**. Tolerância numérica10⁻⁵m. Registraram-se afastamentos brutos das extremidades. Largura coincidiu; alturas N1 coincidiram com a proposta e N2 com a alteração30cm de R56. A altura antiga de N2 não foi usada para rejeitar um sólido atualizado.

Todas as32 correspondências físicas CAD/BIM previamente estabelecidas em R72 apontaram para a mesma unidade da proposta. A classe+caixa manteve-se como controle independente de nomes. Não se deduziu conectividade analítica, rigidez ou continuidade de armadura da caixa geométrica.

## Grupos que reúnem unidades distintas da proposta

'''+merges+'''

## Unidades da proposta divididas entre grupos nativos

'''+(splits or 'Nenhuma.')+'''

## Correspondência completa

'''+'\n'.join(lines)+'''

## Ensaio necessário para o D16

Em N1, BIM `V2` reúne as unidades `V3-N1` e `V4A-N1`, enquanto CAD usa `V2` e `V14`. O primeiro trecho tem20×45cm e o segundo20×16cm. O D16/A07 foi observado no detalhamento agrupado BIM. Para testar a contribuição do agrupamento, criar cópia isolada e separar a V2 BIM no apoio comum, mantendo seções, coordenadas, cargas, vínculos e limites. Reprocessar com as mesmas opções e comparar nós/armadura/status com a base congelada. Separar nomes/grupos não autoriza rotular a ligação ou mudar rigidez. Se a ferramenta nativa também alterar conectividade, registrar o efeito e não tratar o teste como variável única.

O agrupamento inicial pode resultar de importação, reconstrução ou edição posterior; esta auditoria não identifica sozinha sua origem causal. O D16 continua registrado como ocorrência diferencial a investigar, sem ser convertido em defeito comprovado de transferência. Outros agrupamentos devem ser padronizados no ensaio final conforme uma regra comum previamente definida. Contagem de correções exige ocorrência física/campo/regra e estado de aceitação; não se utiliza30 versus20 como pontuação de qualidade.

Não ocorreu nova exportação ou cálculo nesta revisão. Não se mediu duração retrospectiva. O ensaio final continua dependente de cargas completas, critérios iguais e medição prospectiva pareada conformeR69.
''',encoding='utf-8')
ast.parse(Path(__file__).read_text(encoding='utf-8'));shutil.copy2(Path(__file__),out/Path(__file__).name)
write('R80-validacao.json',dict(passed=True,protectedFilesUnchanged=len(protected),sourceUnits29CoveredPerBranch=True,uniqueCandidates64=True,beamCrosswalk32Confirmed=True,nativeGroupIdentities50MatchedStatus=True,geometryConnectivityClaimed=False))
write('R80-manifesto.json',dict(revision='H03/R80',files=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(out.iterdir()) if p.is_file() and p.name!='R80-manifesto.json']))
repo.mkdir(parents=True)
for p in out.iterdir():shutil.copy2(p,repo/p.name)
print(json.dumps(dict(out=str(out),summary=summary,splitUnits=[r for r in sourceRows if r['CADSplitAcrossGroups'] or r['BIMSplitAcrossGroups']]),ensure_ascii=False))

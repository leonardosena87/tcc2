from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,hashlib,shutil,zipfile,re,ast
root=Path('D:/TCC');out=root/'outputs/Agrupamento-H03-R81-TESTE-NAO-EXECUTAR';prior=root/'outputs/Vigas-H03-R79-EXPLORATORIO-NAO-EXECUTAR';repo=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r81');assert not repo.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();write=lambda n,v:(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
protected=read(out/'R81-protegidos-R79.json')
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
statusPath=out/'BIM-status-arvore-completa-UI.txt';text=statusPath.read_text(encoding='utf-8');stack=[];records=[];groups=[];types={'Viga(s)':'viga','Laje(s)':'laje','Pilar(es)':'pilar','Sapata(s)':'apoio auxiliar/sapata'}
for line in text.splitlines():
 m=re.match(r'^(\t+)\d+ item da árvore \(selectable\) (.+)$',line)
 if not m:continue
 depth=len(m[1]);label=m[2]
 while stack and stack[-1][0]>=depth:stack.pop()
 parents=[s[1] for s in stack];floor=next((s for s in parents if re.fullmatch(r'(?:TCC-[\w]+-)?N[012]',s)),None);typ=next((types[s] for s in parents if s in types),None)
 group=re.match(r'^(\d+) (Viga\(s\)|Laje\(s\)|Pilar\(es\)|Sapata\(s\)) (.+)$',label)
 if group:groups.append(dict(floor=floor,elementType=typ,nativeGroupLabel=label,count=int(group[1])))
 message=re.match(r'^(Erro|Aviso) (\w+) - (.+)$',label)
 if message:
  assert floor and typ and parents;records.append(dict(branch='BIM',floor=floor,elementType=typ,nativeElement=parents[-1],kind=message[1],code=message[2],message=message[3]))
 stack.append((depth,label))
beam=[r for r in records if r['elementType']=='viga'];assert len(beam)==23 and not any(r['kind']=='Erro' for r in beam);assert Counter(r['code'] for r in beam)==Counter({'123':21,'98':1,'08':1})
assert len({(r['floor'],r['nativeElement']) for r in beam})==21;assert sum(r['code']=='D42' for r in records)==11
write('BIM-status-estruturado.json',dict(source=str(statusPath),sourceSha256=sha(statusPath),groups=groups,messages=records,queryTriggeredAdditionalCalculations=True,completeStructuralValidation=False))
def summary(p):return re.search(r'editar Value: (Cargas verticais:[^\n]+)',p.read_text(encoding='utf-8'))[1]
assert summary(out/'BIM-resumo-analise-UI.txt')==summary(prior/'BIM-resumo-analise-UI.txt')
geo=read(out/'R81-geometria-comparada.json');assert geo['geometryMatchingUnique89'] and len(geo['nameChanges'])==1 and len(geo['propertyChanges'])==2
for r in geo['propertyChanges']:
 for changes in r['propertiesDiffer'].values():
  assert {k for k in set(changes['old'])|set(changes['new']) if changes['old'].get(k)!=changes['new'].get(k)}=={'Taxa de armadura'}
states=[]
for b,prepName,frozenName,changed in [('BIM-TESTE','R81-preparacao.json','congelado-BIM-TESTE',True),('BIM-CONTROLE','R81-controle-preparacao.json','congelado-BIM-CONTROLE',False)]:
 prep=read(out/prepName);prj=Path(prep['nativeProject']);assert (sha(prj)!=prep['initialPrjSha256'])==changed
 with zipfile.ZipFile(prj) as z:assert z.testzip() is None
 files=[]
 for p in sorted(prj.parent.parent.rglob('*')):
  if not p.is_file():continue
  q=out/frozenName/p.relative_to(prj.parent.parent);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==sha(p);files.append(dict(path=str(p),frozen=str(q),sha256=sha(q)))
 state=dict(branch=b,nativeProject=str(prj),initialPrjSha256=prep['initialPrjSha256'],nativeSha256=sha(prj),frozenFiles=files,prjZipIntegrityPassed=True,prjChanged=changed,geometryExported=True,structuralApproval=False)
 if changed:state.update(onlyEngineeringEditRequested='Dividir V2/N1 no no P5; nenhuma secao/carga/vinculo/limite editado explicitamente',nativeSplitAndLocalResultsCheckedAfterReopen=True,fullInternalConnectivityVerified=False)
 else:state.update(reprocessed=False,splitBeams=False,exportSettingsDiscardedOnClose=True)
 write(f'R81-estado-{b}.json',state);states.append(state)
t=read(out/'R81-tempo.json');p=read(out/'R81-processamento.json');assert t['elapsedMs']>0 and p['commandToFirstObservedFinishMs']>0
result=dict(revision='H03/R81',atUtc=datetime.now(timezone.utc).isoformat(),trial='Dividir grupo BIM V2/N1 em P5, nova copia isolada',before=dict(nativeBeamGroups20=True,error='D16/no2; A07/taxa >2%',P5MdShownKNm=-38.17,sectionRowsCM=[[20,16],[20,45]]),after=dict(nativeBeamGroups=21,beamErrorMessages=0,beamWarningCodes=dict(Counter(r['code'] for r in beam)),V2=dict(sectionCM=[20,16],nodes=['P6','P5'],MdKNm=[-6.55,-8.49],negativeRebar=['4 phi8','4 phi8']),V13=dict(sectionCM=[20,45],nodes=['P5','P4'],MdKNm=[-38.17,-33.20],negativeRebar=['3 phi10','4 phi8'])),localCADValuesAndRebarMatch=True,globalSummaryDisplayedUnchanged=True,IFCGeometryMatchesControl89Parts=True,IFCChangedFieldsOnlyTwoTaxaArmaduraAndOneName=True,nativeDivisionCausallyRemovedD16InThisTrial=True,underlyingSolverAlgorithmProven=False,allInternalConnectivityUnchangedProven=False,originalImportCausedGroupingProven=False,adoptedAsFinalDesign=False,sectionsOrLoadsExplicitlyEdited=False,rebarLimitsRaised=False,ELUELSCompleted=False,productivityRankingAllowed=False,realFoundationDesign=False)
write('R81-resultado.json',result)
(out/'LEIA-ME-R81.md').write_text(f'''# H03/R81 — teste local da contribuição do agrupamento ao D16

EXPERIMENTO COM CARGAS PARCIAIS. NÃO EXECUTAR. A cópia de teste e a de controle foram obtidas do mesmo congelamento BIM/R79. Nenhum autor RVT/DWG, receptor CAD ou texto da monografia foi alterado. O teste não substitui revisão técnica da solução estrutural.

## Operação e observação

No croqui N1 acionou-se o comando nativo **Dividir**, selecionou-se V2 e o nó existenteP5. O programa manteve o trecho raso com nomeV2 e criouV13 para o trecho mais alto. Não se inseriu nó, não se rotulou ou engastou manualmente, nem se editou seção, carga, nível ou limite de armadura. Repetiu-se a seleção de vigas N1/N2, demais tipos e pré-moldados desmarcados, análise linear/P-Delta e ELS desativados, comoR79. Registraram-se opções e seleção em imagens. O processamento terminou com avisos.

A V2 de20×16cm passou a exibir momentos−6,55 e−8,49kN·m nos apoiosP6/P5, com4ϕ8 nos dois. A V13 de20×45cm exibiu−38,17 e−33,20kN·m emP5/P4, com3ϕ10 e4ϕ8. Esses valores e escolhas locais coincidiram com os trechos correspondentes CAD/R79, respeitando orientação e identificação física. Mantiveram-se extensão/comprimento livre199,60/190cm e440/420cm, elevação0 e nível320cm.

Na árvore expandida, D16 não apareceu nas vigas:13 grupos N1 e8 grupos N2 apresentaram aviso123; também permaneceram98 naV11/N1 e08 naV3/N2. O desaparecimento do D16 após o único comando de divisão sustenta a contribuição operacional desse agrupamento neste teste específico. Não demonstra a origem histórica do agrupamento na importação, nem permite concluir defeito geral de IFC ou superioridade de um fluxo. Tampouco autoriza dividir toda viga contínua apenas para obter mensagem favorável. A adequação do detalhamento, continuidade, ancoragens, faces de apoio e aplicação normativa ainda exige revisão técnica.

O resumo global permaneceu integralmente igual ao BIM/R79. Isso inclui cargas ainda parciais e os avisos de relação carga/área e deslocamentos não verificados. A consulta de Status novamente disparou cálculos de outros tipos; capturou-se **LajeL5 calculando**. Persistiram11D42 dos apoios auxiliares, sem uso como fundação real. O arquivo de teste foi salvo, fechado e reaberto; conferiram-se a divisão no croqui e os momentos/armaduras daV2 após reabertura.

## Exportação de controle e mudança de representação

Exportou-se IFC4 completo do teste, sem agrupamento de exportação e sem armaduras3D. Exportou-se também cópia idêntica ao PRJ/R79, sem dividir ou reprocessar, para pasta separada. Descartaram-se ao fechar apenas as alterações de configuração de exportação dessa cópia de controle; seu PRJ permaneceu exatamente com o SHA256 inicial.

O primeiro ensaio de auditoria esperava76 partes comoR57 e falhou porque ambos os estados pós-dimensionamento exportam89:22 pilares,45 partes de vigas,11 lajes e11 auxiliares de apoio. Essa falha de hipótese foi investigada e não tratada como falha do projeto. A comparação direta controle/teste confirmou89 correspondências únicas por classe+caixa, mesma área superior e apenas uma alteração de nome (V2→V13). Entre propriedades exportadas, apenas a taxa de armadura dos dois trechos mudou, de Não calculado para0,63% no raso e0,22% no alto. Taxa de armadura exportada não equivale à verificação completa dos limites e detalhamento.

Comparou-se ainda a geometria histórica das32 partes de vigas com as45 do controle. Para cada parte anterior exigiu-se cobertura longitudinal contínua, sem lacuna/sobreposição entre caixas, mesma seção transversal e soma da área superior. As45 partes cobrem exatamente as32 caixas históricas. As caixas dos demais tipos também se preservaram. As13 partes adicionais refletem subdivisão da representação exportada neste estado; **não são13 novas vigas físicas ou grupos de detalhamento**. As29 unidades lógicas de origem e os grupos nativos20→21 continuam sendo outras medidas. Não se afirma equivalência de todo o modelo analítico a partir dessa auditoria geométrica.

## Tempo, preservação e decisão

O intervalo prospectivo de investigação durou{t['elapsedMs']/60000:.3f}min, incluindo navegação, elaboração da auditoria, exportação de controle e conferência após reabertura. O subintervalo comando→primeira captura de conclusão foi{p['commandToFirstObservedFinishMs']/1000:.3f}s, com latência de automação/captura; não é tempo puro de solver e não deve ser somado ao intervalo maior. Não houve participação humana nesta etapa. Tempo ativo exclusivo é desconhecido; não se utiliza este intervalo para ranking de produtividade.

Preservaram-se{len(protected)} arquivos protegidos R79. Congelaram-se separadamente teste e controle, com integridadeZIP/SHA256. Não se promoveu o teste a projeto final nem se corrigiu o D16 nas evidências R79. O próximo passo é completar as cargas e verificar vínculos/combinações/ELU/ELS em bases explicitamente selecionadas, mantendo disponível o estado anterior e o efeito observado do agrupamento. A monografia permanece intocada.
''',encoding='utf-8')
for script in (Path(__file__),root/'work/auditar-geometria-h03-r81.py'):
 ast.parse(script.read_text(encoding='utf-8'));shutil.copy2(script,out/script.name)
write('R81-validacao.json',dict(passed=True,protectedR79Unchanged=len(protected),nativeControlPrjUnchanged=True,testPrjChangedAndReopened=True,prjIntegrityBothPassed=True,beamD16AbsentAfterTrial=True,beamMessages23Parsed=True,geometryUnique89Matched=True,historical32To45CoverageChecked=True,completeStructuralValidation=False))
write('R81-manifesto.json',dict(revision='H03/R81',files=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='R81-manifesto.json']))
repo.mkdir(parents=True)
for p in out.iterdir():
 if p.is_file():shutil.copy2(p,repo/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-30.md';previous=guide.read_text(encoding='utf-8');guide.write_text('''# Continuação H03 — R80/R81

R80:29 unidades de origem→32 sólidos históricos por ramo; grupos nativos CAD30/BIM20. Nomes de todos os50 grupos conferidos em statusR79. Não comparar contagens de erro com denominadores distintos.

R81: cópia BIM dividiuV2/N1 emP5; trecho rasoV2(20×16),altoV13(20×45). Reprocessado, D16 ausente; valores locais/armaduras coincidem com CAD/R79; resumo global igual. Salvo/reaberto. Teste isolado, não solução final aprovada. Geometria IFC controle/teste89 partes iguais;45 partes de vigas pós-dimensionamento recobrem32 históricas. Nenhuma perda/adição física inferida dessa subdivisão. ConsultaStatus calcula outros elementos; auxiliares D42 não são fundação real.

Relatórios: `outputs/Agrupamentos-H03-R80-AUDITORIA`, `outputs/Agrupamento-H03-R81-TESTE-NAO-EXECUTAR`. Base comparativa congelada continuaR79 CAD/BIM; testeR81 separado, controleR79 preservado. Próximo: cargasQ da cobertura ainda não aplicadas (planoR65), compatibilidade/combinações e ELU/ELS. Monografia intocada.

---

'''+previous,encoding='utf-8')
print(json.dumps(dict(out=str(out),protectedUnchanged=len(protected),beamD16Absent=True,geometry89Matched=True,controlPRJUnchanged=True),ensure_ascii=False))

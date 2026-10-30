"""Consolida experimento exploratorio nativo e seus limites de interpretacao."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,re,hashlib,shutil,zipfile,ast
root=Path('D:/TCC');out=root/'outputs/Vigas-H03-R79-EXPLORATORIO-NAO-EXECUTAR';repo=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r79');assert not repo.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda n,v:(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
protected=read(out/'R79-protegidos-R78.json')
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
statuses={b:read(out/f'{b}-status-estruturado.json') for b in ('CAD','BIM')}
config={};summaries={};native=[]
for b in ('CAD','BIM'):
 text=(out/f'{b}-config-vigas-confirmado-UI.txt').read_text(encoding='utf-8');mask=text.split('\n\t\t1 Barra de status')[0].split('\n\t\t3393 Barra de status')[0]
 config[b]={k:v for v,k in re.findall(r'(?:editar|caixa de combinação) [^\n]*?Value: (.*?) ID: (\d+)',mask)}
 assert config[b]['2006']=='2' and config[b]['2003']=='10'
 summary=re.search(r'editar Value: (Cargas verticais:[^\n]+)',(out/f'{b}-resumo-analise-UI.txt').read_text(encoding='utf-8'))[1];summaries[b]=summary
 assert 'Os deslocamentos horizontais não foram verificados' in summary
 prep=read(out/f'R79-preparacao-{b}.json');prj=Path(prep['nativeProject']);assert sha(prj)!=prep['initialPrjSha256']
 with zipfile.ZipFile(prj) as z:assert z.testzip() is None
 frozen=[]
 for p in sorted(prj.parent.parent.rglob('*')):
  if not p.is_file():continue
  q=out/f'congelado-{b}'/p.relative_to(prj.parent.parent);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==sha(p)
  frozen.append(dict(path=str(p),frozen=str(q),sha256=sha(q)))
 state=dict(branch=b,nativeProject=str(prj),nativeSha256=sha(prj),initialPrjSha256=prep['initialPrjSha256'],prjZipIntegrityPassed=True,frozenFiles=frozen,completeLoads=False,executiveProject=False,dimensioningSelection='Vigas N1/N2',statusQueryTriggeredAdditionalCalculations=True,realFoundationsDesignedAndValidated=False)
 write(f'R79-estado-{b}.json',state);native.append(state)
assert config['CAD']==config['BIM'];assert summaries['CAD']==summaries['BIM']
write('R79-config-vigas-campos-comparados.json',config)
write('R79-resumo-analise-comparado.json',dict(displayedCADBIMEqual=True,summary=summaries['CAD'],comparison='Igualdade apenas dos valores exibidos no resumo; não prova igualdade de toda combinação, vínculo ou armadura'))
beam={b:[r for r in s['messages'] if r['elementType']=='viga'] for b,s in statuses.items()}
assert len(beam['CAD'])==32 and len(beam['BIM'])==22
assert sum(r['kind']=='Erro' for r in beam['CAD'])==0 and sum(r['kind']=='Erro' for r in beam['BIM'])==1
assert next(r for r in beam['BIM'] if r['kind']=='Erro')['code']=='D16'
bitolas=(out/'BIM-V2-no2-bitolas-A07-UI.txt').read_text(encoding='utf-8');barFailures=re.findall(r'item da árvore \(selectable\) ø ([\d.]+) - Erro (\w+) - ([^\n]+)',bitolas)
assert len(barFailures)==5 and all(c=='A07' for _,c,_ in barFailures)
detail=dict(branch='BIM',beam='V2',floor='N1',nativeReportedNode=2,nativeSupport='P5',negativeMomentShownKNm=-38.17,sectionRowsCM=[[20,16],[20,45]],barRows=dict(extensionCM=[199.6,440.0],clearSpanCM=[190,420],levelCM=[320,320],elevationCM=[0,0]),negativeRebarFailure=[dict(diameterMM=float(d),code=c,message=m) for d,c,m in barFailures],maximumConfiguredRebarPercent=2,maximumConfiguredCGPercent=10,evidence='BIM-N1-V2-*.png e BIM-V2-no2-bitolas-A07-UI.*',conclusion='D16 explicado na interface por A07 para todas as cinco bitolas; nenhuma correção aplicada')
write('R79-D16-detalhe-BIM.json',detail)
comparison=dict(sourceCrosswalk=str(root/'outputs/Resultados-H03-R72-PARCIAIS-NAO-FINAIS/R72-mapa-CAD-BIM-65-solidos.json'),physicalLine='N1; y=3,90m; x=0..6,55m',BIM=dict(group='V2',components=['V3-N1 da proposta R43','V4A-N1 da proposta R43'],supportP5MdKNm=-38.17,negativeArmature='D16/A07 no nó2'),CAD=dict(groups=['V2','V14'],V2=dict(sectionCM=[20,45],supportP2MdKNm=-33.20,supportP5MdKNm=-38.17,negativeRebarAtP2='4 phi8',negativeRebarAtP5='3 phi10'),V14=dict(sectionCM=[20,16],supportP5MdKNm=-8.49,supportP11MdKNm=-6.55,negativeRebarAtBothSupports='4 phi8')),inference='O agrupamento diferente é hipótese explicativa para a seleção de momentos/seções no detalhamento; a causa causal exige teste controlado de agrupamento, faces de apoio e critérios.',equivalentSupportNamesNotAssumed=True,analyticalConnectivityProven=False,causeAttributedToIFCTransfer=False)
write('R79-V2-V14-comparacao-local.json',comparison)
ia=dict(observedBothBranches=dict(chooseDiametersUsingAI=True,collectAutomatically=True,trainWhenSaving=True,collectedRecordsShown=17,trainedRecordsShown=0,accuracyShown=None,lastTrainingDateShown=None),CADObservation='após salvar/reabrir',BIMObservation='antes do salvamento final',stateBeforeProcessKnown=False,modelInferenceActuallyUsedVerified=False,manualTrainingTriggered=False,externalGenerativeAssistantIsSeparate=True,finalPairedTrialMustFreezeAndStandardizeNativeAIState=True)
write('R79-IA-nativa-observada.json',ia)
times={b:read(out/f'R79-tempo-{b}.json') for b in ('CAD','BIM')};assert all(t['elapsedMs']>0 and not t['rankingAllowed'] for t in times.values())
result=dict(revision='H03/R79',atUtc=datetime.now(timezone.utc).isoformat(),scope='Análise estática linear/P-Delta e dimensionamento exploratório selecionando vigas N1/N2 com cargas parciais; posterior consulta de status',nativeProjects=[dict(branch=s['branch'],nativeProject=s['nativeProject'],nativeSha256=s['nativeSha256']) for s in native],displayedGlobalSummaryEqual=True,beamMessages={b:dict(totalMessages=len(rows),errorMessages=sum(r['kind']=='Erro' for r in rows),countsByCode=dict(Counter(r['code'] for r in rows))) for b,rows in beam.items()},initialSelectedTypesOnlyBeams=True,statusReadOperationNotReadOnly=True,statusQueryTriggeredAdditionalCalculations=True,auxiliaryFootingD42DisplayedPerBranch=11,additionalResultsOutsideScopeMustNotBeUsedAsFoundationDesign=True,D16RootUI='A07 / taxa maior que configurada',causalRootCauseVerified=False,geometryReexportedThisRevision=False,finalQualityRankingAllowed=False,finalProductivityRankingAllowed=False,previousR78ProtectedFilesUnchanged=True,completeELUAndELSValidation=False,realFoundationDesignWithinResearchScope=False)
write('R79-resultado.json',result)
(out/'LEIA-ME-R79.md').write_text(f'''# H03/R79 — dimensionamento exploratório e diferença de agrupamento

ESTUDO COM CARGAS PARCIAIS. NÃO EXECUTAR. O propósito desta revisão é localizar impedimentos de dimensionamento e conferir diferenças entre os receptores. Nenhuma seção, vinculação ou armadura foi corrigida. A monografia e os autores RVT/DWG não foram alterados.

## O que se executou no programa

Criaram-se cópias independentes de R78, preservando fatores Q=0,50/0,40/0,30. Na janela de análise marcou-se dimensionamento apenas de elementos selecionados e escolheram-se exclusivamente vigas moldadas no local de N1/N2. Desmarcaram-se os demais tipos em todos os pavimentos e todos os pré-moldados. Executou-se análise estática linear com P-Delta já configurado. Deixou-se ELS/redistribuição adicional/dinâmica desativados neste recorte exploratório. As imagens de seleção e opções documentam o comando efetivamente preparado nos dois ramos.

**Limitação operacional identificada:** a consulta posterior **Status dos elementos** não foi uma simples leitura passiva: no BIM observou-se o programa calculando pilares automaticamente durante a abertura. A árvore completa também mostrou mensagens de lajes, pilares e sapatas auxiliares. Assim, não se declara que nenhum elemento além das vigas sofreu cálculo interno nesta sessão. Os cadastros auxiliares de sapata exibiram 11 erros D42 por ramo; não se corrigiu nem utilizou esse cálculo como fundação real. O estudo permanece delimitado à superestrutura e sem validação geotécnica. Antes de automatizar novas consultas, separar o processamento solicitado dos cálculos disparados por janelas/relatórios.

## Resumo global e mensagens

O resumo visível coincidiu integralmente entre os dois receptores: peso próprio75,69tf, adicional10,05tf, acidental17,11tf, total102,86tf, área aproximada132,81m² e relação774,46kgf/m². Persistiram os avisos de relação carga/área não usual e deslocamentos horizontais não verificados. Os valores0,00 de deslocamentos dessa janela não significam deslocamento físico nulo. Essa coincidência não prova igualdade de todas as combinações, malhas ou armaduras.

Na árvore de status do CAD apareceram 15 vigas com aviso em N1 e15 em N2, sem grupo de erro de viga. No BIM apareceram1 viga com erro e11 com aviso em N1 e8 com aviso em N2. São **grupos nativos de detalhamento diferentes**, não os mesmos denominadores. Não se calcula taxa de erro nem ranking a partir dessas contagens. Os32 sólidos de vigas por ramo e as29 unidades lógicas da proposta R43 são recortes distintos: as contagens históricas29/62 descrevem a proposta/transferência, e não comprovam que cada receptor tenha29 grupos nativos. A auditoria de agrupamentos posterior deve atualizar essa distinção sem apagar os registros anteriores.

O CAD apresentou aviso98 em V9/N1 (ancoragem da armadura de pele no nó3) e aviso08 em V13_1/N2 (carga negativa). O BIM apresentou aviso98 em V11/N1 (nó1), aviso08 em V3/N2 e erroD16 em V2/N1 (nó2). O aviso123 de deslocamentos não verificados apareceu nas30 vigas CAD e nas19 vigas BIM do grupo de avisos; não se infere que a viga com D16 tenha deslocamentos verificados. Também se preservaram mensagens dos outros elementos para rastreabilidade, sem atribuí-las automaticamente a defeitos de intercâmbio.

## D16 na V2 BIM e correspondência física

Na planilha Nó da V2/N1 selecionou-se a linha2, apoioP5, momento exibido−38,17kN·m. A janela de resultados da armadura mostrou A07 — taxa de armadura maior que a configurada — para as cinco bitolas8/10/12,5/16/20mm. O limite configurado foi2% nos dois ramos; a relação máxima de CG foi10%, também igual. Os demais valores de campos editáveis/combinações da máscara principal de Vigas coincidiram no recorte comparado. Não se elevou um limite para eliminar o erro.

A V2 BIM reúne barras de extensão199,60 e440,00cm, seções20×16 e20×45cm, nível320cm e elevação0. Pelo mapa geométrico R72, correspondem aos trechos físicos de V14 eV2 do CAD. O CAD mostrou na V2 os momentos−33,20 e−38,17kN·m, com4ϕ8 e3ϕ10 nos apoios; na V14, de20×16cm, mostrou−8,49 e−6,55kN·m, com4ϕ8. A existência de um momento−38,17 na mesma linha física não demonstra que ele deva ser automaticamente aplicado ao trecho raso em ambos os detalhamentos. O agrupamento e as faces/seções utilizadas nos nós precisam de teste controlado. A diferença de agrupamento é hipótese explicativa concreta, **ainda sem prova causal de que originou o D16 ou de que representa falha do IFC**. Nenhuma dessas armaduras foi aprovada para execução.

O procedimento para abrir Nó e Resultados da armadura segue a [documentação operacional AltoQi sobre D16](https://suporte.altoqi.com.br/hc/pt-br/articles/360000680694). Essa fonte explica a investigação no software; não é comprovação normativa do projeto.

## IA do Eberick e medição

Nos dois receptores observou-se a opção **Escolher bitolas usando IA**, coleta automática e treinamento ao salvar marcados; a janela mostrou17 dados coletados e0 treinados, sem acurácia ou data de treinamento. No CAD a leitura ocorreu após salvar/reabrir, no BIM antes do salvamento final. Esse estado observado não comprova inferência por modelo treinado durante o processamento nem permite atribuir economia de tempo à IA nativa. Não se acionou treinamento manual ou limpeza. Essa ferramenta difere da assistência generativa usada para scripts, navegação e interpretação; ambas precisam de registro próprio na metodologia. Um ensaio final deve congelar e padronizar também esse estado.

Os intervalos exploratórios prospectivos foram CAD{times['CAD']['elapsedMs']/60000:.3f}min e BIM{times['BIM']['elapsedMs']/60000:.3f}min; incluem navegação, desenvolvimento da investigação e esperas. O CAD inclui reposicionamento humano e tentativas de controle; o BIM inclui interrupção e retomada da conversa. Não se conhece tempo ativo isolado. O intervalo CAD terminou antes da conferência adicional de parâmetros/V14, realizada posteriormente e sem novo cronômetro; não se soma ou reconstrói essa duração. Os subintervalos de processamento registram comando/captura/latência, não tempo puro de CPU; estão contidos nas etapas e não devem ser adicionados novamente. Não constituem duração final dos fluxos ou ranking. Ver protocoloR69.

## Preservação e próximos passos

PRJ/companheiros foram salvos e congelados separadamente, com integridadeZIP e SHA256. Todos os {len(protected)} arquivos protegidos de R78 permaneceram iguais. A última confirmação de fechamento CAD após conferência exigiu usar a captura específica do diálogo: a coordenada do recorte de diálogo é relativa a ele; entradas dirigidas ao quadro principal não estavam acionando o botão. Esse procedimento não elimina automaticamente o problema dos campos editáveis de outras janelas.

O próximo trabalho é mapear as29 vigas lógicas da origem aos32 sólidos e grupos nativos de cada receptor, preservando as diferenças encontradas; depois testar uma hipótese de agrupamento em novas cópias, sem mudar cargas/seções/limites simultaneamente. Completar cargas, vínculos, ELU/ELS e critérios2026 continua necessário. O IFC não foi reexportado nesta revisão; não se afirma nova auditoria geométrica pós-processamento.
''',encoding='utf-8')
ast.parse(Path(__file__).read_text(encoding='utf-8'));shutil.copy2(Path(__file__),out/Path(__file__).name)
write('R79-validacao.json',dict(passed=True,protectedR78FilesChecked=len(protected),nativePrjIntegrityBothPassed=True,displayedSummariesEqual=True,beamConfigurationValuesEqual=True,manualGeometryReinforcementChangesMade=False,UIMessageParsingBothComplete=True,completeStructuralValidation=False))
write('R79-manifesto.json',dict(revision='H03/R79',files=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='R79-manifesto.json']))
repo.mkdir(parents=True)
for p in out.iterdir():
 if p.is_file():shutil.copy2(p,repo/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-30.md';previous=guide.read_text(encoding='utf-8');guide.write_text('''# Continuação H03 — atualização R79

Processamento exploratório executado nos dois receptores R79. Fatores Q mantidos R78. Cargas ainda parciais. Vigas selecionadas N1/N2; a consulta de Status disparou cálculos adicionais do programa, incluindo pilares e mensagens de auxiliares de apoio. Não usar como projeto real de fundações.

BIM V2/N1 apresenta D16/nó2, explicado por A07 para todas as cinco bitolas; limite2% igual CAD. V2 BIM agrupa os trechos CAD V2(20×45) eV14(20×16). Momentos de detalhamento divergem por lado/grupo: conferir agrupamento/faces com teste controlado antes de atribuir defeito ao IFC. IA nativa habilitada,17 coletados/0treinados nas leituras, sem prova de uso efetivo de inferência.

Relatório e congelamento: `outputs/Vigas-H03-R79-EXPLORATORIO-NAO-EXECUTAR`. Próximo: mapa origem29/unidades físicas32/grupos nativos; ensaio de agrupamento em novas cópias. Não apagar o D16 registrado nem comparar contagens de erros sem denominadores equivalentes. Monografia intocada.

---

'''+previous,encoding='utf-8')
print(json.dumps(dict(out=str(out),protectedUnchanged=len(protected),summariesEqual=True,beamConfigEqual=True,D16ExplainedByUIA07=True),ensure_ascii=False))

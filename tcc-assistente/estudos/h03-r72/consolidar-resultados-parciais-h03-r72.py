"""Resultados empiricos ja documentados; nao mede novamente a transferencia."""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import json,csv,hashlib,shutil,ast
root=Path('D:/TCC');out=root/'outputs/Resultados-H03-R72-PARCIAIS-NAO-FINAIS'
dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r72')
assert not out.exists() and not dest.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
relative={
'receiptState':'Intercambio-H03-R46-BIM-NAO-EXECUTAR/R46-estado-atual.json',
'cadDrawing':'Intercambio-H03-R45-CAD-NAO-EXECUTAR/R45-auditoria-recebimento-Eberick.json',
'bimGeometry':'Intercambio-H03-R46-BIM-NAO-EXECUTAR/R46-auditoria-pilares-vigas.json',
'geometry':'Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR/R56-geometria-exportada.json',
'persistence':'Verificacao-H03-R57-NAO-EXECUTAR/R57-resultado.json',
'roofG':'Cargas-H03-R64-CONFERENCIA-INDIVIDUAL-NAO-EXECUTAR/R64-resultado.json',
'roofQ':'Cobertura-H03-R65-PLANO-Q-NAO-APLICADO/R65-resultado.json',
'timeInventory':'Resultados-H03-R69-TEMPOS-EXPLORATORIOS/R69-inventario-tempos.json'}
# Nome do plano Q e resolvido por nome existente, sem presumir que a aplicacao ocorreu.
qdir=root/'outputs/Cobertura-H03-R65-PLANO-Q-NAO-APLICADO'
if not (root/'outputs'/relative['roofQ']).exists():
    candidates=list(qdir.glob('*plano*.json'))
    assert len(candidates)==1,[p.name for p in qdir.glob('*.json')]
    relative['roofQ']=str(candidates[0].relative_to(root/'outputs'))
paths={k:root/'outputs'/v for k,v in relative.items()};data={k:read(p) for k,p in paths.items()}
protected=read(root/'outputs/Reservatorio-H03-R71-ALTERNATIVAS-NAO-APLICADO/R71-manifesto.json')['files']
for p in protected:assert sha(Path(p['path']))==p['sha256'],p['path']
state=data['receiptState'];cad=data['cadDrawing'];bim=data['bimGeometry'];geo=data['geometry'];persist=data['persistence'];roof=data['roofG']
assert not state['CAD']['nativeStructuralLaunchPerformed']
expected=state['CAD']['expectedNativeComplementation'];assert expected==dict(columnSegments=22,logicalBeams=29,slabs=11)
assert bim['geometryPass'] and bim['columnSegmentsMatching']==22 and bim['logicalBeamsPassing']==29 and bim['slabsNativeReceived']==0
assert all(f['polylineContoursMatch'] and f['textContentsMatch'] for f in cad['floors'])
assert sum(f['receivedCounts']['LWPOLYLINE'] for f in cad['floors'])==62
assert sum(f['receivedCounts']['MTEXT'] for f in cad['floors'])==66
assert all(a['superstructureNamesGuidsBoxesTopAreasAndExportedPropertiesPreserved'] for a in persist['audits'].values())
assert roof['readCount']==26 and len(roof['comparison'])==13 and roof['allExpectedReadingsPassed']
assert all(r['equalDisplayedComponentsAndCoordinates'] for r in roof['comparison'])
classes=('IfcColumn','IfcBeam','IfcSlab')
def key(r):return (r['type'],tuple(r['min']+r['max']))
maps={b:{key(r):r for r in rows if r['type'] in classes} for b,rows in geo.items()}
for b,rows in geo.items():assert len(maps[b])==len([r for r in rows if r['type'] in classes])==65
assert maps['CAD'].keys()==maps['BIM'].keys()
crosswalk=[]
for k,a in sorted(maps['CAD'].items()):
    b=maps['BIM'][k];assert abs(a['topAreaM2']-b['topAreaM2'])<=1e-5
    crosswalk.append(dict(type=a['type'],CAD_name=a['name'],BIM_name=b['name'],CAD_guid=a['guid'],BIM_guid=b['guid'],min=a['min'],max=a['max'],sameName=a['name']==b['name'],topAreasMatch=True,matchBasis='classe+caixa unica; area superior conferida; nao vinculo analitico'))
counts=Counter(r['type'] for r in crosswalk);assert counts==dict(IfcColumn=22,IfcBeam=32,IfcSlab=11)
availability=[dict(element='Trecho de pilar',denominator=22,CAD_initialNative=0,BIM_initialNative=22,CAD_complemented=22,BIM_complemented=0),dict(element='Viga logica',denominator=29,CAD_initialNative=0,BIM_initialNative=29,CAD_complemented=29,BIM_complemented=0),dict(element='Laje',denominator=11,CAD_initialNative=0,BIM_initialNative=0,CAD_complemented=11,BIM_complemented=11)]
denom=sum(r['denominator'] for r in availability);typed=sum(r['BIM_initialNative'] for r in availability)
assert denom==62 and typed==51
for r in availability:r.update(CAD_initialPercent=100*r['CAD_initialNative']/r['denominator'],BIM_initialPercent=100*r['BIM_initialNative']/r['denominator'])
issueRows=[
('P01','Acoes Q do telhado e combinacoes','R65/R66','Plano13pontos em A1/A2 nao aplicado; configuracao Q cancelada, fatores originais mantidos','Aplicar acao justificada, reler fatores/combinacoes e conferir13pontos por ramo','entrada comum pendente'),
('P02','Vento','R63/R66','Vento e combinacoes completos nao verificados','Definir parametros locais/envoltoria/pressao interna e conferir casos e combinacoes','entrada comum pendente'),
('P03','Reservatorio P2','R71','1000L mantidos; centro/base e modelo somente candidatos, tara/cota absoluta pendentes','Fechar altimetria, instalacao e peso completo; dimensionar apoio e verificar cheio/vazio','concepcao comum pendente'),
('P04','Telhado P1 e P2','R60/R65','A1/A2 parciais; varandaP1 e regiao elevadaP2 nao entram nas reacoes atuais','Fechar cobrimento, apoios, pesos e reacoes das regioes excluidas','concepcao comum pendente'),
('P05','Paredes, esquadrias e vergas','R55/R56/R67/R68/R70','Matriz bruta e areas condicionais; nenhuma carga de parede aplicada; W08 especial','Rever aberturas com referenciaP3R68, peitorisJ1, tara/vergas, apoioW08 e distribuicao local','entrada comum pendente'),
('P06','Escada e guarda-corpo','R48/R53/R70','Faixa de laje/circulacao nao substitui lance real de escada, patamar ou guarda-corpo','Definir modelo/reacoes/protecao e aplicar parcelas sem duplicar as ja adotadas','concepcao comum pendente'),
('P07','Vinculos, apoios e rigidez','R52/R54/R56/R63','Comandos de continuidade/apoios e processamento parcial existentes; nao validam grelha final','Conferir malha, liberacoes, rigidezes, apoios idealizados e balanco de varanda','verificacao comum pendente'),
('P08','Materiais completos e detalhamento','R51','C25/CAAII/cobrimentos lidos e quatro campos ajustados por ramo; cadastro mecanico completo do aco nao conferido','Conferir aco, granulometria/espacamento real e detalhamento, sem inferir por nome do IFC','verificacao comum pendente'),
('P09','ELU/ELS e estabilidade','R63/R64','Processamento exploratorio com acoes incompletas; sem dimensionamento/ELS aprovado','Apos entradas completas avaliar resistencia, fissuras, deformacoes, estabilidade e revisar concepcao','verificacao comum pendente'),
('P10','Fontes Revit/AutoCAD','R56','Revisao das alturasN2 existe no receptor; fontes e textos CAD ainda exigem sincronizacao','Atualizar ambos segundo a hipotese aceita e conferir nova transferencia com hashes','atualizacao comum pendente'),
('P11','Ensaio pareado e tempos finais','R69','112arquivos inventariados; sem tempos completos comparaveis','Congelar entradas e executar protocolo equivalente e prospectivo, sem somar registros sobrepostos','metodo de comparacao pendente'),
('P12','Pacote de entrega e resultados','R72','Resultados parciais documentados, sem ranking global','Salvar nativos finais, evidencias, tabelas/figuras e limites; fechar texto apenas com resultados obtidos','documentacao final pendente')]
out.mkdir()
def write(n,v):(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write('R72-protegidos-R71.json',protected)
write('R72-mapa-CAD-BIM-65-solidos.json',crosswalk)
with (out/'R72-mapa-CAD-BIM-65-solidos.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(crosswalk[0]));w.writeheader();w.writerows(crosswalk)
issues=[dict(id=i,subject=s,evidenceRevisions=e,state=st,completionCriterion=c,category=cat,branch='ambos',transferDefectProven=False,closed=False) for i,s,e,st,c,cat in issueRows]
write('R72-matriz-fechamento.json',issues)
with (out/'R72-matriz-fechamento.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(issues[0]));w.writeheader();w.writerows(issues)
result=dict(revision='H03/R72',atUtc=datetime.now(timezone.utc).isoformat(),scope='Consolidacao retrospectiva de evidencias, nao nova transferencia ou calculo',sources=[dict(id=k,path=str(p),sha256=sha(p)) for k,p in paths.items()],initialTypedAvailability=availability,initialTypedAggregate=dict(denominatorLogicalElements=denom,CAD_native=0,BIM_native=typed,CAD_percent=0.,BIM_percent=100*typed/denom,notErrorRate=True,notOverallQualityScore=True),complementedLogicalElements=dict(CAD=62,BIM=11,notCorrectionOperationsCount=True,notDefectCount=True),cadDrawingContent=dict(contoursReceived=62,contoursExpected=62,textContentsReceived=66,textContentsExpected=66,typographyIdenticalVerified=False),bimInputTreatment=state['bimTransferTreatment'],currentReceiverGeometryCheckpoint=dict(revision='R56, preservacaoR57',solidCounts=dict(counts),uniquePairs=65,sameNamePairs=sum(r['sameName'] for r in crosswalk),sameNameNotMatchingCriterion=True,logicalBeams=29,auxiliaryFootingsExcludedPerBranch=11,analyticalConnectivityProven=False),roofGCheckpoint=dict(revision='R64',individualReads=26,pointsPerBranch=13,displayPrecisionToleranceKN=roof['displayPrecisionToleranceKN'],allPointsMatchBetweenBranches=True,roofComplete=False),closedFinalFlow=False,fullFlowTimes=dict(CAD=None,BIM=None),isolatedAIEffort=dict(tokens=None,cost=None,inferenceSeconds=None),finalRankingAllowed=False,structuralApproval=False)
write('R72-resultados-parciais.json',result)
avtable='\n'.join(f'| {r["element"]} | {r["denominator"]} | {r["CAD_initialNative"]} | {r["BIM_initialNative"]} | {r["CAD_complemented"]} | {r["BIM_complemented"]} |' for r in availability)
it='\n'.join(f'| {r["id"]} | {r["subject"]} | {r["completionCriterion"]} |' for r in issues)
(out/'LEIA-ME-R72.md').write_text(f'''# H03/R72 — resultados parciais e matriz de fechamento

ESTUDO NÃO DIMENSIONADO. NÃO EXECUTAR. Consolidou-se evidência histórica já obtida; não se executou nova importação, novo cálculo ou atualização da monografia. A R72 não transforma pendências em resultados finais.

## O que a chegada ao Eberick demonstrou

R45/CAD conservou62/62 contornos e66/66 conteúdos de texto na auditoria do desenho recebido. TEXT/MTEXT, nomes de camadas e tipografia mudaram como documentado; conteúdo preservado não significa tipografia idêntica ou elementos estruturais nativos. A base CAD não recebeu lançamento estrutural automático nessa etapa.

R46/BIM recebeu22/22 trechos de pilares e29/29 vigas lógicas com os critérios geométricos auditados, após tratamento explícito do IFC. Os32 sólidos representam29 vigas lógicas. Não recebeu as11 lajes nativas. O tratamento registrado alterou17 registros de geometria nominal e retirou2 pavimentos vazios: esse trabalho integra o fluxo BIM estudado e não pode desaparecer do relato de esforço.

| Unidade da proposta | Previsto comum | CAD nativo inicial | BIM nativo inicial | CAD complementado depois | BIM complementado depois |
|---|---:|---:|---:|---:|---:|
{avtable}

O total inicial de unidades lógicas tipadas foi0/62 no CAD e51/62 no BIM ({100*typed/denom:.2f}%). O denominador reúne trechos de pilar, vigas lógicas e lajes; não mistura32 sólidos de viga com29 vigas lógicas. Trata-se somente da disponibilidade geométrica nativa inicial neste caso. Não é taxa de erro, índice geral de qualidade ou prova de segurança. O CAD2D fornece referência gráfica e exige reconstrução nativa; isso deve ser medido como trabalho do fluxo e não rotulado automaticamente como falha de transferência.

As complementações posteriores documentadas R47/R48/R49 no CAD e R50 no BIM atenderam respectivamente62 e11 unidades lógicas. Esses números NÃO são62 e11 operações de interface, nem62 e11 defeitos: houve cópias por pavimento, comandos agrupados, divisão de sólidos, seleção e revisão. A contagem final de correções necessita ocorrência, campo, motivo e evidência de antes/depois. As diferenças comuns de materiais R51 (quatro campos por ramo) e de concepção N2/R56 não foram atribuídas a um defeito de DWG ou IFC.

## Mesmo estado geométrico dos receptores, com limites

No checkpoint R56, com preservação conferida R57, há65 pares únicos por classe e caixa:22 pilares,32 sólidos de viga e11 lajes. As áreas superiores também conferiram. A R72 produziu mapa CSV/JSON entre nomes/GUIDs dos ramos; o nome não foi usado para decidir correspondência. Há{sum(r['sameName'] for r in crosswalk)}/65 nomes iguais, sem converter nomes diferentes em erro. Excluíram-se11 IfcFooting auxiliares por ramo, que não representam fundações dimensionadas.

O mapa não comprova malha completa, ligações, rigidez, armaduras ou identidade de propriedades não extraídas. Refere-se aos receptores já complementados, não demonstra que o CAD reteve automaticamente dados tipados da origem. A exportação R57 teve seis verificações de lançamento sem mensagens, três por ramo; isso também não equivale a validação analítica ou aprovação ELU/ELS. Os hashes das evidências foram relidos nesta consolidação.

R64 acrescentou26 leituras individuais reais na interface das cargas permanentes parciais de telhado:13 pontos por ramo, com coordenadas e componentes de força coincidentes no exibido. A tolerância{roof['displayPrecisionToleranceKN']:.8f}kN trata a apresentação de seis casas; não representa precisão interna ou tolerância normativa. A equivalência desses13pontos não cobre todo o carregamento, pois P1/P2, água, paredes, vento e outras entradas permanecem pendentes.

## Tempo e esforço da IA

Os registros R69 contêm inventário de112 arquivos de tempo no recorte definido, com intervalos, ausências e sobreposições explicitados. Não há um tempo final completo comparável CAD/BIM. Campos de duração final, tokens, custo e inferência isolada permanecem nulos/desconhecidos. Não se inferiu esforço da IA pela quantidade de mensagens, pelo número de arquivos ou pelo tempo do script desta consolidação.

A atuação observada da IA compreende programação, geração e auditoria dos artefatos, pesquisa normativa/documental, leitura/operação de interface e preparação de hipóteses para revisão. As decisões humanas já registradas incluem materiais, escopo, preservação das alturas, hipóteses de cobertura/reservatório e confiança do suplemento. Não se atribuiu duração humana retrospectiva inexistente. O protocolo pareado R69 separa preparação comum, transferência, complementação, correções, análise e documentação, com pausas/interrupções persistidas. O trabalho exploratório não será somado para criar um vencedor.

## Critérios para encerrar o estudo

| ID | Frente ainda aberta nos dois ramos | Critério de encerramento |
|---|---|---|
{it}

Essa matriz lista12 frentes de trabalho, NÃO12 erros por ramo nem12 falhas de intercâmbio. Nenhuma foi encerrada só pela existência de relatório. As alterações técnicas comuns precisam ser aplicadas aos dois ramos em cópias independentes e verificadas por critério igual. O arquivo JSON conserva estado, origem e critério de aceite; o CSV facilita registrar evolução. Não se adicionou SPT fictício nem se dimensionou fundação.

O índice de retomada em D:/TCC aponta R72 e os arquivos nativos R64/R66. As etapas que dependiam de intervenção humana foram puladas nesta sessão, conforme orientação do usuário. A modificação parcial de fatores Q foi cancelada e a releitura CAD confirmou os originais; não se afirmou aplicação de Q_TELHADO. A monografia permanece preservada.
''',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name);ast.parse(Path(__file__).read_text(encoding='utf-8'))
write('R72-validacao.json',dict(cadContours62AndTexts66=True,bimColumns22AndBeams29AndSlabs0=True,uniquePairedSuperstructureBoxes=65,allTopAreasMatch=True,denominatorUsesLogicalElements=True,protectedR71FilesChecked=len(protected),sourcesHashRecorded=True,newNativeOperation=False))
write('R72-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file()]))
dest.mkdir()
for p in out.iterdir():shutil.copy2(p,dest/p.name);assert sha(p)==sha(dest/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
guide.write_text('''# Atualizacao R72 — resultados parciais e matriz de fechamento

Ler outputs/Resultados-H03-R72-PARCIAIS-NAO-FINAIS/LEIA-ME-R72.md. Chegada CAD62/62contornos e66/66textos; BIM apos adaptador22pilares/29vigaslogicas/0lajes. Complementacao posterior CAD62/BIM11unidades logicas NAO e numero de erros/operacoes. Mapa65pares geometricos CAD/BIM em CSV/JSON, sem confundir32solidos com29vigas. Matriz de12frentes pendentes com criterios de aceite. Tempos finais/tokens/custo nulos, sem ranking. NativosR64/R66preservados, Q_R65nao aplicado, modificacaoQ_R66cancelada. P3usarR68, W08R70, reservatorioalternativasR71. Sem monografia/origens alteradas. NAO EXECUTAR.

---
Historico anterior:

'''+old,encoding='utf-8')
print(json.dumps(dict(initialTypedBIMPercent=result['initialTypedAggregate']['BIM_percent'],pairedSolids=len(crosswalk),sameNamePairs=result['currentReceiverGeometryCheckpoint']['sameNamePairs'],openWorkfronts=len(issues),flowRankingAllowed=False),ensure_ascii=False))

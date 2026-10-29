"""Triagem parcial NBR6118 no checkpoint geometrico, sem dimensionamento."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,csv,hashlib,shutil,ast
root=Path('D:/TCC');out=root/'outputs/Normativa-H03-R74-TRIAGEM-NAO-DIMENSIONADO'
dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r74')
assert not dest.exists() and {p.name for p in out.iterdir()}=={'R74-versao-Eberick-UI.txt','R74-versao-instalada.json'}
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(root/'outputs/Acoes-H03-R73-RETOMADA-NAO-EXECUTAR/R73-manifesto.json')['files']
for p in protected:assert sha(Path(p['path']))==p['sha256'],p['path']
norm=root/'materiais/normas/ABNT NBR 6118-2026.pdf';gp=root/'outputs/Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR/R56-geometria-exportada.json';geo=read(gp)
version=read(out/'R74-versao-instalada.json');assert version['update']=='2025-04' and version['version']=='18.306'
items=[]
for branch,rows in geo.items():
 for r in rows:
  if r['type'] not in ('IfcColumn','IfcBeam','IfcSlab'):continue
  dx,dy,dz=[r['max'][i]-r['min'][i] for i in range(3)];short=min(dx,dy)
  row=dict(branch=branch,type=r['type'],name=r['name'],guid=r['guid'],min=r['min'],max=r['max'],basis='IFC R56; preservacao R57; geometria nominal ortogonal previamente auditada',completeNormativeCompliance=False,nativeDesignVerificationPerformed=False)
  if r['type']=='IfcColumn':
   area=dx*dy*1e4;row.update(clause='13.2.3',smallerDimensionCM=round(short*100,6),areaCM2=round(area,6),generalDimensionMinimumCM=19,absoluteAreaMinimumCM2=360,generalMinimumDimensionPass=short>=.19-1e-6,minimumAreaPass=area>=360-1e-4,additionalGammaNFromDimension=1.0 if short>=.19-1e-6 else None)
  elif r['type']=='IfcBeam':
   row.update(clause='13.2.2',widthCM=round(short*100,6),heightCM=round(dz*100,6),ordinaryBeamWidthMinimumCM=12,ordinaryWidthMinimumPass=short>=.12-1e-6,wallBeamClassificationVerified=False,reinforcementFitVerified=False)
  else:
   balcony=r['min'][0]>9.7 and abs(r['max'][2]-3.2)<1e-6
   roof=abs(r['max'][2]-6.39)<1e-6;minimum=.10 if balcony else (.07 if roof else .08)
   hcm=round(dz*100,6);gamma=max(1.,1.95-.05*hcm) if balcony else None
   row.update(clause='13.2.4.1 e tabela13.2',thicknessCM=hcm,classification='balanco da varanda' if balcony else ('cobertura sem balanco' if roof else 'piso sem balanco'),minimumThicknessCM=minimum*100,minimumThicknessPass=dz>=minimum-1e-6,cantilever=balcony,additionalGammaNRequiredForFinalDesignForces=gamma,nativeGammaNApplicationVerified=False if balcony else None,serviceabilityVerified=False)
  items.append(row)
assert len(items)==130
assert sum(r.get('cantilever',False) for r in items)==2
assert all(r.get('generalMinimumDimensionPass',True) and r.get('minimumAreaPass',True) and r.get('ordinaryWidthMinimumPass',True) and r.get('minimumThicknessPass',True) for r in items)
assert all(abs(r['additionalGammaNRequiredForFinalDesignForces']-1.25)<1e-6 for r in items if r.get('cantilever'))
widthMM=200;coverMM=30;stirrupHypothesisMM=6.3;barHypothesisMM=16;aggregateMM=25
inside=widthMM-2*(coverMM+stirrupHypothesisMM);required=max(20,barHypothesisMM,1.2*aggregateMM)
barExamples=[]
for n in (2,3,4):
 spacing=(inside-n*barHypothesisMM)/(n-1);barExamples.append(dict(barCount=n,longitudinalDiameterMM=barHypothesisMM,nominalInsideWidthMM=inside,computedHorizontalClearSpacingMM=spacing,requiredHorizontalClearSpacingMM=required,nominalSpacingPass=spacing>=required,exampleOnlyNotSelectedReinforcement=True))
assert barExamples[1]['nominalSpacingPass'] and not barExamples[2]['nominalSpacingPass']
def write(n,v):(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write('R74-protegidos-R73.json',protected);write('R74-triagem-130-registros.json',items)
with (out/'R74-triagem-130-registros.csv').open('w',newline='',encoding='utf-8-sig') as f:
 fields=list(dict.fromkeys(k for r in items for k in r));w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(items)
sources=[dict(id='norma-exemplar-local',path=str(norm),sha256=sha(norm),clauses=['13.2.2','13.2.3','13.2.4.1/tabela13.2','14.6.4.3','18.3.2.2'],visualTableCheck='PDF94/pagina impressa76'),dict(id='geometria-R56',path=str(gp),sha256=sha(gp)),dict(id='release-AltoQi',url='https://suporte.altoqi.com.br/hc/pt-br/novo-conhe%C3%A7a-a-atualiza%C3%A7%C3%A3o-2026-08-do-altoqi-eberick',published='2026-09-17',consulted='2026-10-29',topic='Alteracao no criterio de redistribuicao, limite0,75 na atualizacao2026-08')]
result=dict(revision='H03/R74',atUtc=datetime.now(timezone.utc).isoformat(),scope='Triagem parcial de limites dimensionais e informacao normativa; nao calculo ELU/ELS',sources=sources,installedSoftware=version,full6118_2026ImplementationConfirmed=False,softwareUpdated=False,dimensionalRecords=len(items),perBranchCheckedCounts={b:dict(Counter(r['type'] for r in items if r['branch']==b)) for b in ('CAD','BIM')},minimumGeometryChecksImplementedPassed=True,geometryPassingIsDesignApproval=False,balconyGammaN=dict(required=1.25,actsOn='esforcos solicitantes finais de calculo no dimensionamento da laje em balanco',actsOnWholeBuildingMass=False,shouldBeMultipliedTwice=False,nativeApplicationVerified=False),reinforcementLayoutExample=dict(clause='18.3.2.2',widthMM=widthMM,nominalCoverMM=coverMM,stirrupDiameterHypothesisMM=stirrupHypothesisMM,aggregateMaxMM=aggregateMM,nominalInsideWidthMM=inside,minimumHorizontalClearSpacingMM=required,examples=barExamples,nativeReinforcementDefined=False,bendsTolerancesAndJointsVerified=False),redistributionCriterion=dict(clause='14.6.4.3',deltaMinimum=.75,C25NeutralAxisRatioGeneralMaximum=.45,actualDelta=None,actualNeutralAxisRatio=None,nativeCurrentCriterionVerified=False),structuralApproval=False,monographEdited=False,nativeEngineeringFilesEdited=False)
write('R74-resultado.json',result)
updates=[dict(parentId='P07',extraCriterion='Conferir aplicacao unica de gamma_n1,25 na varanda14cm e os vinculos/malha de dimensionamento',closed=False),dict(parentId='P08',extraCriterion='Registrar Eberick2025-04 v18.306 e separar o que foi verificado manualmente do atendimento automatico nao comprovado a6118:2026',closed=False),dict(parentId='P09',extraCriterion='Conferir delta e x/d quando houver redistribuicao, espacamentos/ancoragens e ELS sem concluir por minimos geometricos',closed=False)]
write('R74-complemento-matriz-fechamento.json',updates)
exampleTable='\n'.join(f'| {r["barCount"]} | {r["computedHorizontalClearSpacingMM"]:.3f} | '+('sim' if r['nominalSpacingPass'] else 'não')+' |' for r in barExamples)
(out/'LEIA-ME-R74.md').write_text(f'''# H03/R74 — triagem normativa parcial e versão do Eberick

NÃO DIMENSIONADO. NÃO EXECUTAR. A auditoria usa o exemplar local ABNT NBR6118:2026 e a geometria nominal ortogonal já conferida R56, com preservação R57. Não substitui cálculo, detalhamento ou comprovação de atendimento integral. Nenhum projeto de engenharia ou monografia foi alterado.

## Versão efetivamente instalada

Consultou-se Ajuda→Sobre no aplicativo real, sem projeto aberto: **Eberick2025-04 [v.18.306], Infinity**. A leitura e a identificação UTC estão nos arquivos R74-versao*. Não foi inferida a versão só pelo título2025. Os metadados FileVersion/ProductVersion do executável consultado vieram vazios; essa fonte não foi usada para inventar um número.

A AltoQi informa que a atualização2026-08 incorpora o limite único de redistribuição0,75 da Emenda1:2026, retirando a diferenciação por nós fixos/móveis nessa verificação. A publicação não comprova que a instalação2025-04 já implemente esse critério. [Comunicado oficial de17/09/2026](https://suporte.altoqi.com.br/hc/pt-br/novo-conhe%C3%A7a-a-atualiza%C3%A7%C3%A3o-2026-08-do-altoqi-eberick).

No exemplar local, item14.6.4.3, confirmou-se o limiteδ≥0,75. Para C25, o limite geral de posição relativa da linha neutra é x/d≤0,45; se houver redistribuição, existe condição adicional em função deδ. Não se obteveδ ou x/d dos elementos processados nesta sessão e não se concluiu aprovação de redistribuição. Também não se afirmou que toda a instalação antiga é incompatível: registrou-se precisamente o atendimento que permanece não comprovado.

Não se instalou atualização, entrou em conta/licença ou migrou arquivo automaticamente. Antes de usar resultados finais como atendimento à edição2026, conferir implementação dos critérios aplicáveis ou registrar verificações complementares documentadas. Manter a mesma versão e os mesmos critérios nos dois ramos durante o ensaio pareado; uma futura migração precisa de novo checkpoint.

## Limites geométricos conferidos

Por ramo, examinaram-se22 trechos de pilares,32 sólidos de vigas e11 lajes. Os32 sólidos continuam correspondendo a29 vigas lógicas.

| Verificação limitada | Geometria do checkpoint | Resultado desta triagem |
|---|---|---|
| Pilar: menor dimensão geral≥19cm e área≥360cm², item13.2.3 | Menor dimensão20cm, área600cm² |22/22 por ramo atendem esses dois limites |
| Viga ordinária: largura geral≥12cm, item13.2.2 | Largura20cm |32/32 sólidos por ramo atendem só a largura |
| Laje maciça: espessura mínima pela classificação, item13.2.4.1 |14cm; piso/cobertura/balanço distinguidos |11/11 por ramo atendem só a espessura mínima |

Inferiu-se a largura pela menor extensão XY das caixas dos elementos ortogonais previamente auditados; esse procedimento não vale automaticamente para vigas oblíquas, curvas ou seções variáveis. Área e largura mínimas de pilares não verificam esbeltez, armadura, flexocompressão ou instabilidade. Não existe um mínimo genérico de altura30cm de viga deduzido dessas regras; a altura adotada exige resistência e deformações. A largura20cm também continua maior que a parede acabada15cm, pendência de faces/arquitetura.

## Varanda14cm: coeficiente adicional1,25

A laje da varanda N1 foi identificada pela caixa em X9,75..10,725m e topo+3,20m, nos dois ramos. A tabela13.2, conferida visualmente na página76/PDF94 do exemplar, conduz aγn=1,95−0,05×14=**1,25**. O mínimo geométrico10cm para laje em balanço não elimina essa exigência adicional.

O coeficiente majora os esforços solicitantes finais de cálculo ao dimensionar a laje em balanço. Não se aumenta25% o peso de toda a edificação, nem se aplica novamente sobre resultado já majorado internamente. A continuidade atribuída R52 e a geometria IFC não demonstram que o dimensionamento nativo aplicouγn. Essa leitura deve ser feita nos resultados/configurações apropriados após completar ações e processar dimensionamento. O campo de verificação permanece falso/desconhecido, sem lançar carga artificial.

## Brita25mm e espaço de armadura: exemplo de sensibilidade

O item18.3.2.2 relaciona o espaçamento horizontal livre ao maior valor entre20mm, diâmetro da barra/feixe/luva e1,2vez o agregado máximo. Com agregado25mm e barra hipotética16mm, a triagem exige30mm. Para uma viga de200mm, cobrimento nominal30mm e estribo HIPOTÉTICO de6,3mm, a largura interior nominal disponível entre faces internas do estribo seria{inside:.1f}mm.

| Barras hipotéticas16mm numa camada | Espaçamento livre resultante (mm) | Atende somente este critério horizontal nominal? |
|---|---:|---|
{exampleTable}

O exemplo explica por que largura mínima aprovada não garante acomodação: quatro barras16mm nessa única camada não atendem essa triagem, enquanto três atendem apenas a condição nominal examinada. Não se selecionou armadura ou estribo por esse cálculo. Tolerâncias, curvaturas, emendas, cruzamentos, ancoragens, espaço vertical, execução, fissuração e resistência continuam fora da verificação. As bitolas são hipóteses do exemplo; não são barras observadas ou lançadas no nativo.

## Registro para os resultados

Mantiveram-se separados: critério normativo consultado; dado efetivamente presente no modelo; regra implementada pelo auditor; e resultado nativo não verificado. O JSON/CSV contém130 registros,65 por ramo, sem pontuação global de conformidade. O complemento da matrizR72 acrescenta aceite explícito paraγn, versão normativa e detalhamento, sem reescrever o checkpoint anterior. O PDF protegido e as imagens da norma ficaram fora do repositório público.
''',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name);ast.parse(Path(__file__).read_text(encoding='utf-8'))
write('R74-validacao.json',dict(geometryRecords=130,balconyRecords=2,allImplementedMinimumChecksPassed=True,balconyGammaNArithmeticPassed=True,barSpacingArithmeticPassed=True,normTableVisuallyRead=True,softwareVersionActuallyReadInUI=True,protectedR73FilesChecked=len(protected),nativeDesignOrUpdatePerformed=False))
write('R74-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file()]))
dest.mkdir()
for p in out.iterdir():shutil.copy2(p,dest/p.name);assert sha(p)==sha(dest/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
guide.write_text('''# Atualizacao R74 — versao Eberick e triagem normativa

Ajuda/Sobre real confirmou Eberick2025-04 v18.306 Infinity. Comunicado oficial2026-08trata novo limite delta0,75; implementacao2026na instalacao atual nao comprovada, sem instalar atualizacao. Triagem130registros:22pilares/32solidosviga/11lajes por ramo atendem somente minimos geometricos conferidos. Varanda14cm requer gamma_n1,25 nos esforcos finais, conferir aplicacao UNICA no dimensionamento; nao aplicar25%a massa global. Exemplo brita25/cover30/st6,3/bar16 numa viga20cm mostra4barras numa camada sem espacamento suficiente; NAO e detalhamento. Ler outputs/Normativa-H03-R74-TRIAGEM-NAO-DIMENSIONADO/LEIA-ME-R74.md e complemento matrizR72. R73abertura cancelada sem projeto carregado/alterado; ambosPRJidenticosR64. Q_R65nao aplicado. Ultimo nativoengenhariaR64; R66/R73copiasinalteradas. Sem monografia alterada. NAO EXECUTAR.

---
Historico anterior:

'''+old,encoding='utf-8')
print(json.dumps(dict(checkedRecords=len(items),minimumOnly=True,balconyGammaN=1.25,installedUpdate=version['update'],installedVersion=version['version'],four16mmBarsFit=False,structuralApproval=False)))

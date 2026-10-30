"""Consolida leituras reais UI, sem aplicar Q ou recalcular projeto."""
from pathlib import Path
from datetime import datetime,timezone
from zipfile import ZipFile
import json,csv,hashlib,shutil,ast,re
root=Path('D:/TCC');out=root/'outputs/Cargas-H03-R77-Q-TELHADO-NAO-EXECUTAR';dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r77');assert not dest.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(out/'R77-protegidos-R64-R76.json')
for p in protected:assert sha(Path(p['path']))==p['sha256'],p['path']
prior=root/'outputs/Cargas-H03-R64-CONFERENCIA-INDIVIDUAL-NAO-EXECUTAR';nativeStates={}
for branch in ('CAD','BIM'):
 old=read(prior/f'R64-estado-{branch}.json');prep=read(out/f'R77-preparacao-{branch}.json');project=Path(prep['nativeProject']);folder=project.parent.parent;frozen=out/f'congelado-{branch}';assert not frozen.exists();frozen.mkdir();changed=[];missing=[];records=[]
 assert sha(project)==old['nativeSha256']
 with ZipFile(project) as z:assert z.testzip() is None
 for r in old['frozenFiles']:
  rel=Path(r['frozen']).relative_to(prior/f'congelado-{branch}');p=folder/rel
  if not p.exists():assert p.suffix.lower()=='.log',p;missing.append(dict(path=str(p),originalFrozenPreserved=sha(Path(r['frozen']))==r['sha256']));continue
  changedFromR64=sha(p)!=r['sha256']
  if changedFromR64:changed.append(str(rel));assert p.suffix.lower() in ('.ini','.qib'),p
  q=frozen/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==sha(p)
  records.append(dict(path=str(p),frozen=str(q),sha256=sha(p),byteIdenticalR64=not changedFromR64))
 nativeStates[branch]=dict(nativeProject=str(project),nativeSha256=sha(project),prjEngineeringByteIdenticalR64=True,prjZipIntegrityPassed=True,metadataChangedFromR64=changed,missingOldProcessLogs=missing,frozenFiles=records)
 (out/f'R77-estado-{branch}.json').write_text(json.dumps(nativeStates[branch],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Transcricoes independentes das oito tabelas observadas. Valores exibidos, nao dados internos.
# nivel, fachada, fachada transversal, cota, S2, arrasto, forca, transversal, torcao
raw={
 'CAD':{
 'X+':[['N2',705,965,639,.95,1.,11.17,0.,0.],['N1',710,1072.5,320,.90,.96,18.70,0.,0.],['N0',705,965,20,.43,1.,2.45,0.,0.]],
 'X-':[['N2',705,965,639,.95,1.,11.17,0.,0.],['N1',710,1072.5,320,.90,.96,18.70,0.,0.],['N0',705,965,20,.43,1.,2.45,0.,0.]],
 'Y+':[['N2',965,705,639,.95,1.14,17.57,0.,0.],['N1',1072.5,710,320,.90,1.14,32.16,0.,0.],['N0',965,705,20,.43,1.14,4.21,0.,0.]],
 'Y-':[['N2',965,705,639,.95,1.14,17.57,0.,0.],['N1',1072.5,710,320,.90,1.14,32.16,0.,0.],['N0',965,705,20,.43,1.14,4.21,0.,0.]]},
 'BIM':{
 'X+':[['N2',705,965,639,.95,1.,11.17,0.,0.],['N1',710,1072.5,320,.90,.96,18.70,0.,0.],['N0',705,965,20,.43,1.,2.45,0.,0.]],
 'X-':[['N2',705,965,639,.95,1.,11.17,0.,0.],['N1',710,1072.5,320,.90,.96,18.70,0.,0.],['N0',705,965,20,.43,1.,2.45,0.,0.]],
 'Y+':[['N2',965,705,639,.95,1.14,17.57,0.,0.],['N1',1072.5,710,320,.90,1.14,32.16,0.,0.],['N0',965,705,20,.43,1.14,4.21,0.,0.]],
 'Y-':[['N2',965,705,639,.95,1.14,17.57,0.,0.],['N1',1072.5,710,320,.90,1.14,32.16,0.,0.],['N0',965,705,20,.43,1.14,4.21,0.,0.]]}}
rows=[];caseNames={'X+':'Xmais','X-':'Xmenos','Y+':'Ymais','Y-':'Ymenos'}
fields=['level','facadeCM','transverseFacadeCM','levelCM','S2Displayed','dragCoefficientDisplayed','forceMagnitudeDisplayedKN','transverseForceDisplayedKN','torsionDisplayedKNm']
for branch,cases in raw.items():
 for case,values in cases.items():
  evidence=out/f'{branch}-vento-{caseNames[case]}-tabela-UI.png';assert evidence.is_file()
  for v in values:rows.append(dict(branch=branch,case=case,**dict(zip(fields,v)),nativeLevelName=v[0] if branch=='CAD' else 'TCC-cdd31967-'+v[0],evidence=str(evidence),evidenceSha256=sha(evidence),source='transcricao visual da tabela real; valores arredondados exibidos'))
assert len(rows)==24 and raw['CAD']==raw['BIM']
q={};wind={}
for branch in ('CAD','BIM'):
 txt=(out/f'{branch}-Q-antes-UI.txt').read_text(encoding='utf-8')
 q[branch]=dict(psi0=float(re.search(r'= Value: ([\d.]+) ID: 152',txt)[1]),psi1=float(re.search(r'= Value: ([\d.]+) ID: 153',txt)[1]),psi2=float(re.search(r'= Value: ([\d.]+) ID: 154',txt)[1]),gammaConcreteNormalUnfavorable=float(re.search(r'Normais \(desfavorável\) Value: ([\d.]+) ID: 131',txt)[1]),changed=False)
 txt=(out/f'{branch}-vento-atual-UI.txt').read_text(encoding='utf-8')
 assert 'Velocidade Value: 42 ID: 103' in txt and 'Ângulo Value: 0 ID: 127' in txt and 'Categoria II ID: 121' in txt
 wind[branch]=dict(basicSpeedDisplayedMS=42,angleDeg=0,cases=4,analysis='estatico; leitura visual',S1=1.,S3=1.,terrainRoughnessCategory='II',dimensionClass='Menor que20m',criticalDampingRatioDisplayed=.02,neighborhoodFactorDisplayed=1.,comfortFields=dict(probability=.63,recurrenceYears=1,notULSReturnPeriod=True),calculateAutomatically=True,useSketchFacades=True,obtainDragFromStructure=True,turbulence='Baixa',singleDragValueAllLevels=False,arbitraryHeightCheckbox=False,inactiveArbitraryHeightFieldCM=639,siteJustificationVerified=False,edited=False)
assert q['CAD']==q['BIM'] and wind['CAD']==wind['BIM']
def write(n,v):(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write('R77-24-leituras-vento.json',rows)
with (out/'R77-24-leituras-vento.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
times={b:read(out/f'R77-tempo-{b}.json') for b in ('CAD','BIM')}
totals={b:{c:round(sum(v[6] for v in rs),2) for c,rs in cases.items()} for b,cases in raw.items()}
assert totals['CAD']==dict(zip(('X+','X-','Y+','Y-'),(32.32,32.32,53.94,53.94)))
result=dict(revision='H03/R77',atUtc=datetime.now(timezone.utc).isoformat(),status='Ambos ramos abertos visualmente; Q/vento auditados, sem alteracao de engenharia',Q=q,wind=wind,forceTableRows=24,tableValuesMatchBetweenBranches=True,perCaseDisplayedMagnitudeSumsKN=totals,theseSumsAreNotSupportReactionsOrNetWind=True,fullGeneratedCombinationsAudited=False,BIMCombinationOptionsVisuallyRead=True,CADCombinationOptionsSource='R66, geometria/PRJ de base preservados',QAttempt=dict(branch='CAD',setValueError='element 20166 is not available in cached app state for Eberick.exe',raiseError='element 20089 has no cached secondary actions for Eberick.exe',typeTextDidNotChangeDisplayedPsi=True,configurationCanceled=True,BIMEditingNotRetried=True),QRoofActionCreated=False,QRoofLoadsApplied=False,nativeWindEdited=False,processingPerformed=False,nativeStates=nativeStates,assistedTimes=times,rankingAllowed=False,structuralApproval=False,fullFlowTimes=None,isolatedAIEffort=None,monographEdited=False)
write('R77-resultado.json',result)
summary='\n'.join(f'| {case} | {raw["CAD"][case][0][6]:.2f} | {raw["CAD"][case][1][6]:.2f} | {raw["CAD"][case][2][6]:.2f} | {totals["CAD"][case]:.2f} |' for case in ('X+','X-','Y+','Y-'))
(out/'LEIA-ME-R77.md').write_text(f'''# H03/R77 — auditoria real de Q e vento nos dois receptores

ESTUDO PARCIAL. NÃO EXECUTAR. As duas cópias independentes R77 foram abertas no Eberick2025-04 v.18.306 e fechadas sem salvar alteração de engenharia. A monografia permaneceu intacta. A ação Q_TELHADO e as cargas planejadas R65 continuam NÃO aplicadas.

## Abertura recuperada e edição pulada

Para contornar o seletor textual indisponível, prepararam-se pastas de cópia com prefixos00/01, selecionáveis visualmente no início da lista de edificações. Antes da abertura, alterou-se somente o campo textual ProjetoRecente/Arquivo no EdificacaoEberick.ini da nova cópia, apontando para seu próprio PRJ. Isso evita selecionar a cópia e abrir inadvertidamente o original por um caminho absoluto antigo. Nenhum binário de engenharia foi editado por script. O título da janela confirmou a pasta correta de cada ramo.

No CAD, a tentativa de alterarψ0 por set_value retornou erro de cache; uma tentativa de digitação não alterou o valor exibido. A opção Raise trouxe o diálogo à frente uma vez, mas também falhou posteriormente. Cancelou-se integralmente Ações; não se confirmou ou salvou o ajuste. No BIM a edição não foi repetida. A dificuldade é operacional do controle nesta sessão, não defeito demonstrado de DWG/IFC.

Os dois PRJ permaneceram byte a byte iguais aos respectivos R64 e passaram na integridade ZIP. As diferenças de metadados e a eventual ausência do log do processo anterior na pasta de trabalho estão discriminadas nos estados JSON; os logs originais R64 congelados foram conferidos e preservados. Os arquivos de engenharia associados também foram comparados, sem alteração aceita fora deINI/QIB. Os estados R77 foram congelados depois do fechamento.

## Q e opções de combinações

Nos dois ramos, a ação Acidental/Q mostrouψ0=0,70;ψ1=0,60;ψ2=0,40 eγq normal desfavorável do concreto1,40. Esses dados são leituras reais, sem inferir o BIM a partir do CAD. A referência residencial R66, extraída do exemplar6118:2026, continua a exigir harmonização justificada dos fatores adotados. Não se adotou conservadorismo geral só porque um número é maior.

No BIM, a aba Combinações apresentou geração automática e uso de todas as permanentes habilitados, Combinar entre acidentais desabilitado e Acidental isolada habilitada paraQ,Água eSubpressão. Esses pontos coincidem com a leitura CAD histórica R66. A árvore acessível não fornece todos os estados de seleção; por isso a leitura visual foi preservada em imagem. Isso não é auditoria da lista completa de combinações geradas.

A documentação operacional do fornecedor esclarece que deixar Combinar entre acidentais desmarcado NÃO significa excluir toda simultaneidade: são geradas combinações com as acidentais em conjunto e as isoladas selecionadas. Marcá-lo amplia as possibilidades intermediárias e isoladas. A opção precisa representar as ações do estudo; não se muda só para acelerar ou reduzir mensagens. A explicação operacional não substitui a norma vigente ou a verificação caso a caso. [AltoQi, combinações e dimensionamento](https://suporte.altoqi.com.br/hc/pt-br/articles/15675742914967).

## Hipóteses de vento efetivamente cadastradas

Ambos mostraramV0=42m/s,ângulo0°,quatro casos,vento estático,S1=1,00,S3=1,00,rugosidadeCategoriaII,maior dimensão menor que20m,fator de vizinhança1,00 e amortecimento0,02. Os campos de conforto exibem probabilidade0,63 e período1ano: não se confundem com o período de recorrência que define a velocidade básica para projeto.

Em Forças médias, observaram-se cálculo automático, fachadas do croqui e obtenção de arrasto a partir da estrutura habilitados; turbulênciaBaixa. Adotar valor único para toda a estrutura e Arbitrar altura total acima do solo estavam desabilitados. O campo não adotado de altura exibia639cm; não se afirmou que uma altura arbitrada de639cm estava ativa.

42m/s é o valor CADASTRADO, não uma escolha agora justificada para Vitória da Conquista. Não se demonstrou sua origem nem se declarou o valor local correto. O mapa gráfico fornecido pelo programa foi consultado, sem georreferenciamento/interpolação documentada do ponto. A CAAII de durabilidade não determina a CategoriaII de rugosidade: são classificações diferentes. Permanecem pendentes topografia, entorno, parâmetros da velocidade e exposição da cobertura elevadaP2. O exemplar6123/8681 não foi encontrado na busca nominal da pastaFTC desta sessão; não se simulou consulta ao texto integral dessas normas.

## Oito tabelas,24linhas comparadas

Transcreveram-se visualmente três pavimentos em cada um dos quatro casos, nos dois ramos, com imagens das tabelas preservadas para auditoria. O BIM denomina os níveis TCC-cdd31967-N2/N1/N0; a conciliação utilizou a correspondência comN2/N1/N0 e as cotas639/320/20cm. Conferiram-se fachada, fachada transversal, cota,S2,arrasto,força,força transversal e torção mostradas.

| Caso, independente dos demais | N2(kN) | N1(kN) | N0(kN) | Soma das magnitudes exibidas(kN) |
|---|---:|---:|---:|---:|
{summary}

Cada linha vale para ambos os ramos no estado lido. Não se somamX+eX−ouY+eY−como ações simultâneas. As magnitudes positivas da tabela não foram convertidas em sinais globais sem consultar o vetor do caso. As somas32,32/53,94kN não são reações de apoio ou comprovação de equilíbrio do pórtico. S2e arrasto são valores arredondados exibidos; não foram usados para reconstruir a pressão interna exata.

EmX, a fachada é705/710/705cm e a transversal965/1072,5/965cm; emY ocorre a troca correspondente. S2mostrou0,95/0,90/0,43 emN2/N1/N0. O arrasto emXfoi1,00/0,96/1,00 e emY1,14nos três níveis. Força transversal e torção da tabela exibiram0,00; isso não prova ausência de torção interna ou excentricidade no modelo. A identidade dessas tabelas é resultado parcial, não validação da ação do vento para o local ou da estrutura.

## Tempo, preservação e continuidade

CAD:{times['CAD']['durationMs']/1000:.3f}s assistidos, incluindo abertura, tentativa de editarQ, recuperações, consulta ao mapa e às tabelas, e fechamento. BIM:{times['BIM']['durationMs']/1000:.3f}s, incluindo abertura, leituraQ/opções de combinações, tabelas e confirmação de fechamento, sem repetir a edição ou o mapa. Os escopos diferem. Não calcular vantagem percentual ou duração total de fluxo. A primeira captura posterior ao comando de fecharBIM tem intervalo parcial arquivado e já contido no encerramento final; não somar os dois.

As imagens foram mantidas como evidência dos valores que a árvore acessível não expõe, sem recorte ou alteração do conteúdo. Não representam inspeção em outro computador. O protocolo de medições finais permanece R69, e a entrega parcial R76 continua disponível sem envio. As leituras R77 complementam essa entrega; nenhum nativo R76 foi modificado.

Próximo: concluir entradas/combinações e verificar os critérios normativos aplicáveis; uma análise exploratória com cargas incompletas, se realizada em outra cópia, deve ser identificada separadamente. Não transformar este resultado de igualdade dos cadastros em aprovação deELU/ELS, fundações ou projeto executivo.
''',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name);ast.parse(Path(__file__).read_text(encoding='utf-8'))
write('R77-validacao.json',dict(actualBothBranchesOpened=True,independentNativeProjects=True,forceTableRowsCompared=24,allDisplayedTableValuesEqual=True,QFactorReadbackBothBranches=True,prjUnchangedBothBranches=True,protectedPreviousFilesChecked=len(protected),engineeringEditsSaved=False,QRoofApplied=False,rankingAllowed=False))
manifestFiles=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()]
write('R77-manifesto.json',dict(files=manifestFiles))
dest.mkdir()
for p in out.iterdir():
 if p.is_file():shutil.copy2(p,dest/p.name);assert sha(p)==sha(dest/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig');guide.write_text('''# Atualização R77 — ambos os receptores abertos e Q/vento auditados

Abertura visual funcionou em00-H03-R77-CAD e01-H03-R77-BIM após rebind apenas doProjetoRecente/Arquivo noINI de cada nova cópia. PRJ e arquivos de engenharia mantêm bytesR64; configurações canceladas, semQ_TELHADOcriada/aplicada ou novo processamento. Q=.70/.60/.40eγq1.40nos dois. Vento42m/s,S1/S3=1,rugosidadeII,estático,4casos: valores cadastrados NÃOjustificados para o local.24linhas das4tabelas de vento coincidem, com imagens/CSV/JSON.32,32kN porX e53,94porY são somas de magnitudes exibidas, não reações. Tempos assistidos de escopos diferentes, semranking. Leroutputs/Cargas-H03-R77-Q-TELHADO-NAO-EXECUTAR/LEIA-ME-R77.md. NativosR77congelados, mas último estado efetivo de engenharia continuaR64. EntregaR76ZIP12,4MBpreservada; nãoenviada. Sem monografia alterada. NÃOEXECUTAR.

---
Histórico anterior:

'''+old,encoding='utf-8')
print(json.dumps(dict(forceRows=24,displayValuesEqual=True,prjEngineeringUnchanged=True,QApplied=False,metadataChanges={b:s['metadataChangedFromR64'] for b,s in nativeStates.items()},missingLogs={b:len(s['missingOldProcessLogs']) for b,s in nativeStates.items()}),ensure_ascii=False))

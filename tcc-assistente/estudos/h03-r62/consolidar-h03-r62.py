"""Registra tentativa CAD divergente; nao promove um lancamento incompleto a validado."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,re,shutil,zipfile
root=Path('D:/TCC')
out=root/'outputs/Cargas-H03-R62-TELHADO-G-PARCIAL-NAO-EXECUTAR'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,v):
    (out/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
protected=read(out/'R62-protegidos-R61.json')
for row in protected:assert sha(Path(row['path']))==row['sha256'],row['path']
plan=read(out/'R62-preparacao-CAD.json')
expected_new=plan['plannedNewGDownKN']
summary=(out/'CAD-resultados-texto.txt').read_text(encoding='utf-8')
assert summary in (out/'CAD-resultados-UI.txt').read_text(encoding='utf-8')
assert 'Adicional = 9.73 tf' in summary and 'Total = 102.53 tf' in summary
assert 'Estrutura processada com avisos' in (out/'CAD-conclusao-UI.txt').read_text(encoding='utf-8')
before=(out/'CAD-RC12-forca-lida-UI.txt').read_text(encoding='utf-8')
after=(out/'CAD-RC12-carga-confirmada-UI.txt').read_text(encoding='utf-8')
assert 'X Value: 732.5' in before and 'Y Value: 705' in before and 'Fz Value: 0 ID: 108' in before
assert 'Fz Value: -0.807804' in after
states={}
for b in ('CAD','BIM'):
    pre=read(out/f'R62-preparacao-{b}.json')
    native=Path(pre['nativeProject']);base=native.parent.parent;frozen=out/f'congelado-{b}'
    assert not frozen.exists(), 'Preservar congelamento anterior'
    with zipfile.ZipFile(native) as z:assert z.testzip() is None
    files=[]
    for p in sorted(base.rglob('*')):
        if not p.is_file() or p.suffix.lower() in ('.bak','.bak-g2','.bak-g3','.tmp'):continue
        q=frozen/p.relative_to(base);q.parent.mkdir(exist_ok=True,parents=True)
        shutil.copy2(p,q);assert sha(p)==sha(q)
        files.append(dict(path=str(p),frozen=str(q),sha256=sha(q)))
    unchanged=None
    if b=='BIM':
        source=read(Path(pre['sourceState']))
        unchanged=all(sha(base/Path(r['frozen']).relative_to(Path(pre['sourceState']).parent/'congelado-BIM'))==r['sha256'] for r in source['frozenFiles'])
        assert unchanged
    states[b]=dict(nativeProject=str(native),nativeSha256=sha(native),frozenFiles=files,closedBeforeFreeze=True,zipIntegrityPassed=True,engineeringEdited=b=='CAD',openedInThisRevision=b=='CAD',bimCopyUnchangedFromR61=unchanged,nativeLoadSetValidated=False,summaryCurrentForSavedModel=False if b=='CAD' else True,postCorrectionReprocessingPerformed=False,postCorrectionReopenPerformed=False,newIFCExportPerformed=False)
    write(f'R62-estado-{b}.json',states[b])
timer=read(out/'R62-tempo-CAD.json');solve=read(out/'R62-tempo-processamento-CAD.json')
result=dict(revision='H03/R62',atUtc=datetime.now(timezone.utc).isoformat(),status='Diagnostico CAD incompleto, nao usar como par comparativo',protectedR61FilesChecked=len(protected),plannedNewGDownKN=expected_new,expectedDeltaTfUsingStandardGravity=expected_new/9.80665,displayedAdditionalBeforeTf=8.49,displayedAdditionalAttemptTf=9.73,displayedTotalAttemptTf=102.53,loadIncreaseAccepted=False,observedMissingLoad=dict(node='RC12',xCm=732.5,yCm=705,action='Adicional',readFzKN=0,typedCorrectionFzKN=-.807804,correctionConfirmedInNodeDialog=True,projectSavedAfterCorrection=True,persistenceAfterReopenVerified=False),allOtherNodesReadIndividually=False,otherMissingLoadsProven=False,conversionFactorNativeConfirmed=False,technicalRootCauseProven=False,cadDwgTransferDefectProven=False,bimExpanded=False,bimCopyUnchangedFromR61=True,summaryPredatesRC12Correction=True,postCorrectionReprocessingPerformed=False,prospectiveAssistedTimeCAD=timer,observedProcessingTimeCAD=solve,fullFlowRankingAllowed=False,eluElsApproved=False,sourceRvtDwgEdited=False,monographEdited=False)
write('R62-resultado.json',result)
fmt=lambda ms:f'{int(ms//60000)} min {(ms%60000)/1000:.3f} s'
report=f'''# H03/R62 — ampliação CAD em diagnóstico

ESTUDO PARCIAL, NÃO EXECUTAR. Esta revisão NÃO constitui par CAD/BIM validado. A referência pareada anterior permanece a R61, com apenas RC01 e RC02 conferidos nos dois ramos. Criou-se a cópia BIM R62, mas ela não foi aberta ou ampliada: os arquivos copiados foram conferidos por hash e permanecem iguais aos congelados R61.

## Operação realizada no CAD

Inseriram-se os onze nós previstos RC03..RC13 em N2, por coordenadas em centímetros. Configuraram-se seis grupos de Fz permanente, ação Adicional, conforme o mapa R60: RC03; RC04/RC05; RC06; RC07/RC08/RC12/RC13; RC09/RC10; RC11. Os registros preservam valores digitados e contagens de seleção 1/2/1/4/2/1. Contagem de seleção não prova que cada força ficou armazenada; a leitura posterior demonstrou essa limitação.

Antes da aplicação de RC09/RC10, detectou-se entrada com sinal duplicado (--1.146561). O Eberick apresentou aviso de número real inválido. Corrigiu-se o campo e conferiu-se -1.146561 antes de prosseguir. A tentativa de definir o campo por UIA set_value falhou com 0x80040200; o valor foi corrigido por teclado após limpar o campo. Registrar como ocorrência operacional de automação, sem atribuir à transferência DWG.

## Divergência detectada

Processou-se apenas Análise estática linear, com P-Delta indicado, sem dimensionamento ou deslocamentos ELS. O programa retornou Estrutura processada com avisos. O resumo dessa PRIMEIRA TENTATIVA mostrou peso próprio75,69tf, adicional9,73tf, acidental17,11tf, total102,53tf, área aproximada132,81m2 e relação772,02kgf/m2. Esse resumo foi gerado ANTES da correção individual de RC12 descrita abaixo. Não utilizar esses valores como resultado do arquivo corrigido salvo.

O acréscimo exibido em relação à R61 foi1,24tf. O plano previa {expected_new:.6f}kN novos, equivalentes a {expected_new/9.80665:.9f}tf usando explicitamente9,80665kN/tf. A diferença excede o arredondamento dos resumos. Não se confirmou o fator de conversão interno do programa, nem se demonstrou a causa integral dessa diferença; não se ajustaram valores para forçar igualdade.

Consultou-se RC12 individualmente: X732,5cm/Y705cm e Fz0kN na ação Adicional. Portanto, ao menos esse ponto não continha a força prevista, apesar da seleção anterior do grupo. Digitou-se Fz=-0,807804kN, confirmou-se o diálogo Carga concentrada e depois o diálogo Nó, salvou-se o projeto e fechou-se normalmente. Ainda não se reabriu ou reprocessou após essa correção. Não se afirmou que os outros três pontos do grupo estavam zerados; não foram relidos individualmente nesta etapa. Não se demonstrou causa por foco, concorrência de comandos, conectividade ou intercâmbio.

## Tempo e preservação

Tempo CAD prospectivo assistido: {fmt(timer['durationMs'])}, incluindo abertura, onze nós, tentativa de cargas, processamento, investigação e correção parcial/salvamento. Intervalo observado de processamento: {fmt(solve['durationMs'])}, incluindo latência até leitura da conclusão. Não há tempo BIM de execução R62, pois o ramo não foi iniciado. Não preencher com zero. Nenhum desses valores autoriza ranking ou economia percentual.

Conferiram-se {len(protected)} arquivos protegidos R61. Congelaram-se os conjuntos nativos R62 após o fechamento; PRJ com integridade ZIP verificada. O CAD é diagnóstico com cargas não validadas; BIM é apenas cópia da R61. A monografia e as origens RVT/DWG não foram editadas.

## Próxima ação concreta

Retomar em nova cópia do CAD R62 congelado, sem modificar esta evidência: reler RC07/RC08/RC13 e demais nós/cargas, além de confirmar RC12 após reabrir; corrigir somente o que a consulta demonstrar; reprocessar e reconciliar a soma com unidades/fatores documentados. Só depois ampliar o BIM usando operações confirmadas e comparar o mesmo estado. Preservar os resumos anteriores, identificar sempre qual estado foi processado e separar tempo de tentativa/correção de tempo de transferência.

O escopo permanece parcial: falta Q do telhado, P1/varanda, P2/abrigo, perfis/apoios/ancoragens, paredes, reservatório1000L/tara/base, escada, bordas, vento/com­binações e ELU/ELS. Não há fundação real dimensionada ou aprovação das vigas20x30cm. A igualdade R61 limita-se aos resumos exibidos, não à equivalência integral.
'''
(out/'LEIA-ME-R62.md').write_text(report,encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
for p in out.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'))
write('R62-validacao.json',dict(evidenceSyntaxAndHashesPassed=True,nativeLoadIncreaseValidated=False,bothBranchesCompleted=False,postCorrectionResultsValid=False,syntheticAssistantTestsThisTurn=dict(passed=9,failed=0,nativeStructuralValidation=False),liveOpenAIApiCalls=False))
write('R62-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='R62-manifesto.json']))
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
assert not old.startswith('# Atualizacao R62')
guide.write_text(f'''# Atualizacao R62 — 29/10/2026

ATENCAO: R62 CAD e tentativa divergente, nao par validado. Referencia pareada anterior: R61, apenas RC01/RC02 nos dois ramos. R62 BIM somente copiado de R61, nunca aberto/ampliado. Nativos R62 em outputs/H03_CAD_R62_TELHADO_G_PARCIAL_NAO_EXECUTAR e H03_BIM_R62_TELHADO_G_PARCIAL_NAO_EXECUTAR; congelados em outputs/Cargas-H03-R62-TELHADO-G-PARCIAL-NAO-EXECUTAR. Ver LEIA-ME-R62.md e R62-resultado.json.

CAD: inseridos11nos, tentativa de6grupos G e processamento com avisos. Resumo9,73tf adicional/102,53tf total divergente da soma esperada. Consulta RC12(732,5;705)cm mostrou Fz0; corrigido individualmente para-0,807804kN, confirmado nos dois dialogos, salvo/fechado. NAO reaberto/reprocessado apos correcao. Resumo preservado ANTERIOR a correcao, nao atual para o arquivo salvo. Outros pontos nao relidos; nao presumir todos aplicados ou todos zerados. Sinal duplicado em RC09/RC10 corrigido antes de aplicar, registrado como ocorrencia de interface; causa integral da divergencia e conversao nativa ainda pendentes. Nao atribuir a defeito DWG.

TempoCAD {fmt(timer['durationMs'])}, inclui tentativa/investigacao/correcao parcial/latencia. BIM sem tempo de execucao R62, nao zero. Ambos projetos fechados, Eberick sem dialogo. R61 protegida por hashes. Monografia e RVT/DWG intactos.

PROXIMO: criar nova copia do CADR62 congelado; ler RC07/RC08/RC13 e demais nos/cargas, confirmar RC12 apos reabrir; corrigir com leitura individual, recalcular e reconciliar unidades/soma. Depois ampliar BIM e comparar o mesmo estado. Nao usar R62 como projeto concluido. Demais cargas/concepcao e ELU/ELS pendentes, superestrutura com apoios idealizados, NAO EXECUTAR.

---
Historico anterior:

'''+old,encoding='utf-8')
dst=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r62');dst.mkdir(exist_ok=False)
for p in out.iterdir():
    if p.is_file() and p.suffix.lower() in ('.json','.md','.txt','.py'):
        shutil.copy2(p,dst/p.name);assert sha(p)==sha(dst/p.name)
print(json.dumps(dict(status=result['status'],protectedR61=len(protected),frozen={b:len(s['frozenFiles']) for b,s in states.items()},cadTime=fmt(timer['durationMs'])),ensure_ascii=False))

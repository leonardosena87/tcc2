"""Consolida leituras reais apos reabertura; nao interpreta o binario de calculo."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,shutil,zipfile,ast
root=Path('D:/TCC');out=root/'outputs/Acoes-H03-R78-CONFIGURACAO-NAO-EXECUTAR'
repo=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r78');assert not repo.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda name,value:(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
protected=read(out/'R78-protegidos-R77.json')
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
allfields={};branches=[]
for branch in ('CAD','BIM'):
 prep=read(out/f'R78-preparacao-{branch}.json');native=Path(prep['nativeProject']);folder=native.parent.parent
 observations={}
 for moment,name in [('before',f'{branch}-Q-antes-UI.txt'),('afterReopen',f'{branch}-Q-persistido-apos-reabrir-UI.txt')]:
  text=(out/name).read_text(encoding='utf-8');assert f'R78-{branch}-NAO-EXECUTAR' in text
  pairs=re.findall(r'editar [^\n]*?Value: (.*?) ID: (\d+)',text);fields={key:value for value,key in pairs};assert len(fields)==len(pairs)
  assert fields['121']=='Acidental' and fields['122']=='Q';observations[moment]=fields
 assert set(observations['before'])==set(observations['afterReopen'])
 changed=[k for k in observations['before'] if observations['before'][k]!=observations['afterReopen'][k]];assert set(changed)=={'152','153','154'}
 assert [observations['before'][k] for k in ('152','153','154')]==['0.70','0.60','0.40']
 assert [observations['afterReopen'][k] for k in ('152','153','154')]==['0.50','0.40','0.30'];allfields[branch]=observations
 assert sha(native)!=prep['initialPrjSha256']
 with zipfile.ZipFile(native) as z:assert z.testzip() is None
 frozen=[]
 for p in sorted(folder.rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(folder);q=out/f'congelado-{branch}'/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==sha(p)
  frozen.append(dict(path=str(p),frozen=str(q),sha256=sha(q)))
 state=dict(branch=branch,nativeProject=str(native),nativeSha256=sha(native),initialPrjSha256=prep['initialPrjSha256'],prjChangedFromR77=True,prjZipIntegrityPassed=True,readAfterCloseAndReopen=True,requestedAndObservedFactors=[.5,.4,.3],frozenFiles=frozen,binaryEngineeringSemanticsDecoded=False)
 write(f'R78-estado-{branch}.json',state)
 t=read(out/f'R78-tempo-{branch}.json');assert t['elapsedMs']>0 and not t['rankingAllowed'] and t['includesHumanEntryAndWait']
 branches.append(dict(branch=branch,editableFieldsCompared=len(changed)+len(observations['before'])-len(changed),displayedFieldsChanged=changed,persistedFactors=[.5,.4,.3],intervalMs=t['elapsedMs'],manualEntryReportedByUser=True,nativeProject=str(native)))
assert allfields['CAD']['afterReopen']==allfields['BIM']['afterReopen']
write('R78-comparacao-campos-UI.json',allfields)
norm=root/'materiais/normas/ABNT NBR 6118-2026.pdf'
result=dict(revision='H03/R78',atUtc=datetime.now(timezone.utc).isoformat(),scope='Harmonização assistida dos fatores da ação Acidental/Q nos receptores nativos; conferência após fechar e reabrir',branches=branches,classification='Ajuste metodológico comum; não atribuído à transferência DWG ou IFC',normativeReference=dict(path=str(norm),sha256=sha(norm),clause='Tabela 11.2, página impressa 67/PDF85; ocupação residencial/acesso restrito'),roofMaintenanceQApplied=False,customRoofActionCreated=False,structuralReprocessingPerformed=False,completeLoadCases=False,fullNormativeComplianceEstablished=False,comparisonRankingAllowed=False,aiEffort=dict(nativeAutomaticFieldEditFailed=True,humanEntryRequestsCompleted=2,changedConfigurationValuesObserved=6,manualTypingDurationMs=None,tokenUsage=None,apiCost=None),sourceR77AllFilesUnchanged=True)
write('R78-resultado.json',result)
cad,bim=branches
(out/'LEIA-ME-R78.md').write_text(f'''# H03/R78 — fatores Q harmonizados e persistência conferida

ESTUDO PARCIAL. NÃO EXECUTAR. Esta etapa trata do cadastro de ações dos receptores Eberick; não atualiza a monografia nem os autores RVT/DWG.

Nas cópias independentes `02-H03-R78-CAD-NAO-EXECUTAR` e `03-H03-R78-BIM-NAO-EXECUTAR`, a ação existente **Acidental**, indicação **Q**, passou de ψ0/ψ1/ψ2 = 0,70/0,60/0,40 para **0,50/0,40/0,30**. A referência é a tabela 11.2 do exemplar local ABNT NBR 6118:2026, página 67/PDF85, para ocupação residencial e acesso restrito. Essa classificação não define a intensidade de cada carga nem comprova todas as combinações.

O controle automático voltou a retornar campo indisponível na tentativa de editar ψ0 do CAD. O usuário informou a conclusão da entrada manual e do salvamento de cada cópia. Em seguida, cada projeto foi fechado e reaberto no aplicativo real: leu-se novamente a mesma ação e confirmaram-se os três valores. Compararam-se {cad['editableFieldsCompared']} valores de campos da máscara por ramo; apenas os controles 152/153/154 diferiram nas leituras antes/depois. Os demais valores dessa máscara coincidiram entre os ramos. Esse recorte de interface não equivale a uma auditoria semântica de todo o binário ou de todas as configurações.

Os PRJ mudaram em relação ao estado inicial R77 e passaram na verificação de integridade ZIP. As pastas de trabalho fechadas foram congeladas com SHA256. Todos os {len(protected)} arquivos protegidos de R77 permaneceram iguais. A intervenção constitui ajuste comum de premissas, sem atribuição de erro de transferência ao CAD ou ao BIM.

## Registro de tempo e participação

Os intervalos prospectivos foram **CAD {cad['intervalMs']/60000:.3f} min** e **BIM {bim['intervalMs']/60000:.3f} min**, desde a abertura operacional até a confirmação final de fechamento após a conferência. Incluem espera pela entrada humana, navegação, consulta, raciocínio e latência. O CAD inclui a tentativa automática frustrada; o BIM não a repete. São intervalos assistidos exploratórios, de escopos diferentes; não são duração total de cada fluxo, não demonstram produtividade relativa e não entram em ranking. Não se reconstruiu uma duração exclusiva da digitação humana. Dois pedidos de intervenção foram atendidos; observaram-se seis valores de configuração alterados. Quantidade real de teclas, tokens de IA e custos não foi inferida.

## Próxima verificação

As cargas permanecem parciais: a ação específica Q_TELHADO e as 13 reações variáveis planejadas em R65 ainda não foram cadastradas/aplicadas. Não ocorreu reprocessamento nesta revisão. Qualquer resultado anteriormente processado pertence ao estado anterior, não constitui resultado recalculado de R78. A harmonização dos fatores não fecha vento, paredes, varanda coberta, reservatório, escada, apoios e demais verificações de ELU/ELS.

O próximo processamento deve usar novas cópias a partir deste congelamento. A exploração de vigas, com cargas atuais, serve para localizar impedimentos de concepção; não aprova seções nem dispensa o carregamento completo. O estudo continua delimitado à superestrutura com apoios idealizados, sem dimensionamento de fundações reais.
''',encoding='utf-8')
ast.parse(Path(__file__).read_text(encoding='utf-8'));shutil.copy2(Path(__file__),out/Path(__file__).name)
write('R78-validacao.json',dict(passed=True,originalR77FilesPreserved=len(protected),independentlyReopenedBranches=2,persistedFactorsMatched=True,displayedBeforeAfterDifferencesPerBranch=3,prjZipIntegrityBothPassed=True,monographModified=False,nativeReprocessingPerformed=False))
write('R78-manifesto.json',dict(revision='H03/R78',files=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='R78-manifesto.json']))
repo.mkdir(parents=True)
for p in out.iterdir():
 if p.is_file():shutil.copy2(p,repo/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-30.md';assert not guide.exists()
guide.write_text('''# Continuação H03 — 30/10/2026

## Estado atual R78

Os dois receptores Eberick R78 têm ψ0/ψ1/ψ2 da ação Acidental/Q = 0,50/0,40/0,30, digitados pelo usuário e confirmados no aplicativo real após fechamento/reabertura. Estado congelado e relatório em `outputs/Acoes-H03-R78-CONFIGURACAO-NAO-EXECUTAR`. PRJ alterado, integridade verificada; R77 preservado.

Ainda não se reprocessou R78. O último processamento continua R63/R64, com cargas parciais e sem dimensionamento/ELS. Não confundir cadastro de fatores com aplicação das reações Q_TELHADO de R65, que continua pendente.

Próxima ação: explorar exclusivamente o dimensionamento de vigas, em novas cópias, com análise atualizada e cargas atuais explicitamente parciais. Não dimensionar fundações reais nem atribuir validade final a esse processamento. Registrar causas e elementos; manter equivalência e posterior ensaio de tempo pareado conforme R69.

O guia histórico `CONTINUAR-AQUI-H03-2026-10-29.md` contém R77 e etapas anteriores. A entrega parcial R76 continua preservada; não inclui R78. A monografia permanece sem alteração nesta retomada. Nenhum arquivo foi enviado ao orientador ou ao GitHub nesta etapa.
''',encoding='utf-8')
print(json.dumps(dict(out=str(out),repo=str(repo),branches=branches,protectedUnchanged=len(protected)),ensure_ascii=False))

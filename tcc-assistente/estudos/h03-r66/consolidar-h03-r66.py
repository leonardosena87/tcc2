"""Registra consulta CAD e cancelamento do ajuste incompleto; Q nao aplicada."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,ast,zipfile,re
root=Path('D:/TCC');out=root/'outputs/Acoes-H03-R66-Q-TELHADO-NAO-EXECUTAR'
dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r66')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not dest.exists() and not (out/'R66-manifesto.json').exists()
protected=read(out/'R66-protegidos-R64-R65.json')
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
after=(out/'CAD-Q-cancelamento-confirmado-UI.txt').read_text(encoding='utf-8')
for value,id_ in [('0.70',152),('0.60',153),('0.40',154)]:assert f'Value: {value} ID: {id_}' in after
states={}
for b in ('CAD','BIM'):
 p=read(out/f'R66-preparacao-{b}.json');n=Path(p['nativeProject']);s=read(Path(p['sourceState']))
 assert sha(n)==s['nativeSha256'],n
 with zipfile.ZipFile(n) as z:assert z.testzip() is None
 states[b]=dict(nativeProject=str(n),nativeSha256=sha(n),byteIdenticalToR64=True,zipIntegrityPassed=True,engineeringChangesSaved=False,roofQApplied=False,actionsInspectedThisRevision=b=='CAD')
result=dict(revision='H03/R66',atUtc=datetime.now(timezone.utc).isoformat(),status='Consulta CAD concluida; ajuste incompleto cancelado; BIM nao inspecionado nesta revisao',protectedFilesChecked=len(protected),states=states,observedCADQFactors=[.7,.6,.4],intendedResidentialFactors=[.5,.4,.3],normativeBasis='Exemplar local NBR6118:2026, tabela11.2, PDF85/pagina67, acesso restrito/residencial',factorChangeSaved=False,partialPsi0EntryCanceledAndReadBack=True,newActionCreated=False,roofQApplied=False,newProcessingPerformed=False,uiBlock='Ativacao da janela principal perde foco de dialogo; indices de campos frequentemente retornam not available in cached app state',technicalTransferDefectProven=False,prospectiveComparableDurationAvailable=False,timingLimit='Inicio de cronometro anterior permaneceu apenas em runtime reiniciado; nao reconstruir duracao por timestamps de arquivos',sourceRvtDwgEdited=False,monographEdited=False,eluElsApproved=False)
(out/'R66-resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'LEIA-ME-R66.md').write_text('''# H03/R66 — inspeção de ações e pendência de edição nativa

NÃO EXECUTAR. O estado de engenharia permanece R64. Prepararam-se cópias independentes CAD/BIM e verificaram-se 80 arquivos protegidos R64/R65 por hash. Somente a configuração CAD foi inspecionada nesta revisão. O BIM não chegou a ser aberto: não se infere a leitura atual de seus fatores a partir do CAD.

Na ação Acidental/Q do CAD observaram-se ψ0/ψ1/ψ2=0,70/0,60/0,40. O exemplar local NBR6118:2026, tabela11.2/PDF85/página67, consultado visualmente, apresenta0,50/0,40/0,30 para ocupação residencial e acesso restrito. Registrou-se a necessidade de enquadrar as ações conforme o uso do estudo. Esse confronto é uma pendência de configuração comum, não defeito demonstrado de DWG ou IFC. A conformidade global e a compatibilidade com NBR8681 vigente não foram encerradas.

A consulta da aba Combinações mostrou geração automática habilitada, consideração de todas as permanentes habilitada, combinar entre acidentais desabilitado, Q/Água/Subpressão com Acidental isolada marcado, e opções de ELS/desaprumo conforme o TXT. Esses registros parciais não são exportação nem auditoria de todas as combinações geradas. Nenhuma opção foi confirmada ou alterada.

A digitação pela automação perdeu foco; ocorreram erros de índice de acessibilidade indisponível. Uma entrada ψ0=0,50 foi aceita provisoriamente pelo formulário. Cancelou-se o diálogo inteiro, reabriu-se a ação e confirmou-se novamente0,70/0,60/0,40. Nenhum ajuste parcial foi salvo. O projeto CAD foi fechado. O seletor BIM foi cancelado. Os hashes dos dois PRJ R66 permaneceram idênticos aos correspondentes R64 e a integridade ZIP passou.

Não se criou Q_TELHADO_MANUTENCAO, não se aplicou Q do telhado, não se alteraram cargas G ou arquivos RVT/DWG e não houve processamento ou edição da monografia. A R65 continua sendo plano calculado, não aplicado. Para retomar, conferir os fatores dos dois ramos, a classificação e as combinações da ação de manutenção antes de lançar a matriz. Não somar ou excluir cargas por conveniência.

O início do cronômetro anterior permaneceu em runtime que foi reiniciado; não existe intervalo completo recuperável desta tentativa. Não se estimou duração usando datas de arquivos nem se registrou zero. A falha de instrumentação fica como pendência de qualidade; o ensaio final terá cronometragem persistida antes das operações. Não se incluiu esta tentativa em ranking ou tempo puro de cálculo.

Como autorizado pelo usuário ausente, a etapa dependente da interface foi pulada e o trabalho seguiu para tarefas independentes. Nenhuma aprovação estrutural foi emitida.
''',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
for p in out.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'))
(out/'R66-manifesto.json').write_text(json.dumps(dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file()]),ensure_ascii=False,indent=2),encoding='utf-8')
dest.mkdir()
for p in out.iterdir():
 if p.is_file():shutil.copy2(p,dest/p.name);assert sha(p)==sha(dest/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
guide.write_text('''# Atualizacao R66 — consulta CAD; ajuste nao salvo

Ultimo estado de engenharia R64. R66 inspecionou Q CAD psi0/1/2=0,70/0,60/0,40; proposta de enquadramento residencial0,50/0,40/0,30 pela tabela11.2 do exemplar6118:2026. Entrada parcial cancelada e fatores anteriores relidos. PRJs CAD/BIM identicos R64. BIM nao aberto nesta revisao. Q telhado ainda NAO aplicada. Falha foco/indices de UI registrada; etapa pulada conforme pedido do usuario ausente. Cronometro anterior perdido no reinicio de runtime, sem duracao reconstruida. Ler outputs/Acoes-H03-R66-Q-TELHADO-NAO-EXECUTAR/LEIA-ME-R66.md. Sem novo processamento, monografia ou origens alteradas. NAO EXECUTAR.

---
Historico anterior:

'''+old,encoding='utf-8')
print(json.dumps(dict(status=result['status'],protected=len(protected),nativeHashesPassed=True),ensure_ascii=False))

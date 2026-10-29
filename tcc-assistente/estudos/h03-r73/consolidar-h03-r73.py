"""Encerra tentativa de abertura cancelada; preserva ambos os projetos."""
from pathlib import Path
from datetime import datetime,timezone
from zipfile import ZipFile
import json,hashlib,shutil,ast
root=Path('D:/TCC');out=root/'outputs/Acoes-H03-R73-RETOMADA-NAO-EXECUTAR'
dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r73');assert not dest.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(out/'R73-protegidos-R64-R72.json')
for p in protected:assert sha(Path(p['path']))==p['sha256'],p['path']
checks={};prior=root/'outputs/Cargas-H03-R64-CONFERENCIA-INDIVIDUAL-NAO-EXECUTAR'
for b in ('CAD','BIM'):
 state=read(prior/f'R64-estado-{b}.json');folder=root/f'outputs/H03_{b}_R73_ACOES_NAO_EXECUTAR';rows=[]
 for r in state['frozenFiles']:
  p=folder/Path(r['frozen']).relative_to(prior/f'congelado-{b}');assert sha(p)==r['sha256'];rows.append(dict(path=str(p),sha256=sha(p)))
 project=Path(read(out/f'R73-preparacao-{b}.json')['nativeProject'])
 with ZipFile(project) as z:assert z.testzip() is None
 checks[b]=dict(files=rows,allFilesByteIdenticalR64=True,prjZipIntegrityPassed=True,projectOpened=False,nativeEdited=False)
t=read(out/'R73-tempo-CAD.json');assert not t['projectOpened'] and not t['engineeringEdits']
assert 'janela Abrir edificação' not in (out/'R73-apos-cancelar-UI.txt').read_text(encoding='utf-8')
result=dict(revision='H03/R73',atUtc=datetime.now(timezone.utc).isoformat(),status='Abertura cancelada por falha de controle; nenhum projeto carregado ou alterado',branches=checks,CADAttemptTime=t,BIMAttemptTime=None,BIMAttemptPerformed=False,error='element 16300 is not available in cached app state for Eberick.exe',modalSeparatelyTargetable=False,folderDialogCanceled=True,buildingDialogCanceled=True,actionQCreated=False,loadsApplied=False,partialConfigurationSaved=False,fullFlowRankingAllowed=False)
(out/'R73-resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'LEIA-ME-R73.md').write_text(f'''# H03/R73 — retomada de abertura cancelada

Não se abriu nem se alterou projeto. Criaram-se novas cópias independentes do estado R64 para tentar retomar a configuração de ações. A abertura pelo botão da barra mostrou Abrir edificação; o botão de pasta abriu o seletor. O controle não aceitou o campo de pasta: `element 16300 is not available in cached app state for Eberick.exe`. A janela modal não apareceu como alvo separado em list_windows. Não se contornou o controle por comandos internos ou mudança de segurança.

Cancelaram-se o seletor e Abrir edificação, com releitura do estado sem projeto aberto. Conforme orientação do usuário ausente, a etapa foi pulada sem solicitar intervenção. Não se tentou repetir o mesmo procedimento no BIM. Tempo de tentativa CAD: {t['durationMs']/1000:.3f}s, medido prospectivamente em relógio monotônico, com UTC persistido. Inclui navegação/raciocínio/latência. O BIM não possui intervalo nesta etapa; nulo não é zero. O intervalo não integra comparação de produtividade nem tempo total de fluxo.

Conferiram-se{len(protected)} arquivos protegidos R64/R72 e todos os arquivos das cópias R73 contra os congelados R64. As duas PRJ passaram na integridade ZIP e mantiveram bytes idênticos. Não se criou Q_TELHADO, não se aplicaram cargas ou fatores e não se processou cálculo. As cópias R73 não substituem R64 como último estado efetivo de engenharia. A configuração parcialmente digitada na R66 já havia sido cancelada naquela revisão.

O trabalho independente prosseguiu com auditoria normativa e leitura real de Ajuda/Sobre, registrada em R74. Não houve atualização/instalação de software, alteração da monografia ou envio externo. NÃO EXECUTAR.
''',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name);ast.parse(Path(__file__).read_text(encoding='utf-8'))
(out/'R73-manifesto.json').write_text(json.dumps(dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file()]),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dest.mkdir()
for p in out.iterdir():shutil.copy2(p,dest/p.name)
print(json.dumps(dict(nativeUnchanged=True,protected=len(protected),CADAttemptSeconds=t['durationMs']/1000,BIMAttemptPerformed=False)))

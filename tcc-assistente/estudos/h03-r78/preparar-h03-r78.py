"""Copias independentes para harmonizar acoes; dados de engenharia preservados."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
root=Path('D:/TCC');prior=root/'outputs/Cargas-H03-R77-Q-TELHADO-NAO-EXECUTAR';out=root/'outputs/Acoes-H03-R78-CONFIGURACAO-NAO-EXECUTAR';assert not out.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(prior/'R77-manifesto.json')['files']
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
out.mkdir()
(out/'R78-protegidos-R77.json').write_text(json.dumps(protected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for index,branch in enumerate(('CAD','BIM'),2):
 state=read(prior/f'R77-estado-{branch}.json');folder=root/f'outputs/{index:02d}-H03-R78-{branch}-NAO-EXECUTAR';folder.mkdir(exist_ok=False)
 for r in state['frozenFiles']:
  p=Path(r['frozen']);assert sha(p)==r['sha256'];q=folder/p.relative_to(prior/f'congelado-{branch}');q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==r['sha256']
 project=folder/'Projeto Eberick'/Path(state['nativeProject']).name;ini=folder/'_DADOS_/EdificacaoEberick.ini';before=ini.read_bytes();old=before.splitlines(keepends=True);new=[b'Arquivo='+str(project).encode('ascii')+b'\r\n' if line.startswith(b'Arquivo=') else line for line in old];assert sum(a!=b for a,b in zip(old,new))==1;ini.write_bytes(b''.join(new));assert sha(project)==state['nativeSha256']
 (out/f'R78-preparacao-{branch}.json').write_text(json.dumps(dict(branch=branch,preparedUtc=datetime.now(timezone.utc).isoformat(),nativeProject=str(project),initialPrjSha256=sha(project),sourceState=str(prior/f'R77-estado-{branch}.json'),onlyPreparationFieldChanged='EdificacaoEberick.ini/ProjetoRecente/Arquivo',engineeringBinaryModified=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
print(json.dumps(dict(out=str(out),protectedFiles=len(protected),preparedBothBranches=True,engineeringUnchanged=True)))

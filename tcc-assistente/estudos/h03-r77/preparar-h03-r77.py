"""Copias R64 com vinculo textual local de edificação, para abertura visual."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
root=Path('D:/TCC');prior=root/'outputs/Cargas-H03-R64-CONFERENCIA-INDIVIDUAL-NAO-EXECUTAR'
out=root/'outputs/Cargas-H03-R77-Q-TELHADO-NAO-EXECUTAR';assert not out.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=[]
for manifest in (prior/'R64-manifesto.json',root/'outputs/Entrega-H03-R76-PARCIAL/R76-manifesto.json'):
 for r in read(manifest)['files']:assert sha(Path(r['path']))==r['sha256'];protected.append(r)
out.mkdir()
(out/'R77-protegidos-R64-R76.json').write_text(json.dumps(protected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for index,branch in enumerate(('CAD','BIM')):
 state=read(prior/f'R64-estado-{branch}.json');dest=root/f'outputs/{index:02d}-H03-R77-{branch}-NAO-EXECUTAR';dest.mkdir(exist_ok=False)
 for r in state['frozenFiles']:
  p=Path(r['frozen']);assert sha(p)==r['sha256'];q=dest/p.relative_to(prior/f'congelado-{branch}');q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==r['sha256']
 project=dest/'Projeto Eberick'/Path(state['nativeProject']).name
 ini=dest/'_DADOS_/EdificacaoEberick.ini';before=ini.read_bytes();oldLines=before.splitlines(keepends=True);newLines=[b'Arquivo='+str(project).encode('ascii')+b'\r\n' if x.startswith(b'Arquivo=') else x for x in oldLines];assert sum(a!=b for a,b in zip(oldLines,newLines))==1;ini.write_bytes(b''.join(newLines));assert sha(project)==state['nativeSha256']
 (out/f'R77-preparacao-{branch}.json').write_text(json.dumps(dict(branch=branch,atUtc=datetime.now(timezone.utc).isoformat(),nativeProject=str(project),sourceState=str(prior/f'R64-estado-{branch}.json'),initialPrjSha256=sha(project),edificationMetadata=dict(path=str(ini),beforeSha256=hashlib.sha256(before).hexdigest(),afterSha256=sha(ini),onlyFieldChanged='ProjetoRecente/Arquivo',engineeringBinaryModified=False),reasonFolderPrefix='Facilitar selecao visual no inicio da lista; sem automacao de campo textual indisponivel'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
print(json.dumps(dict(out=str(out),copiedBranches=2,prjEngineeringBytesUnchanged=True,projectRecentPathsReboundOnlyInNewCopies=True),ensure_ascii=False))

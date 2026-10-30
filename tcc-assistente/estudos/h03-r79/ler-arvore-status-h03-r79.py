"""Estrutura dados de status capturados pela UI real; nao acessa memoria do Eberick."""
from pathlib import Path
from collections import Counter
import re,json,sys,hashlib,shutil
out=Path('D:/TCC/outputs/Vigas-H03-R79-EXPLORATORIO-NAO-EXECUTAR');branch=sys.argv[1];assert branch in ('CAD','BIM')
p=out/f'{branch}-status-arvore-completa-UI.txt';text=p.read_text(encoding='utf-8');stack=[];records=[];groups=[]
types={'Viga(s)':'viga','Laje(s)':'laje','Pilar(es)':'pilar','Sapata(s)':'apoio auxiliar/sapata'}
for line in text.splitlines():
 m=re.match(r'^(\t+)\d+ item da árvore \(selectable\) (.+)$',line)
 if not m:continue
 depth=len(m[1]);label=m[2]
 while stack and stack[-1][0]>=depth:stack.pop()
 parents=[s[1] for s in stack];floor=next((s for s in parents if re.fullmatch(r'(?:TCC-[\w]+-)?N[012]',s)),None);typ=next((types[s] for s in parents if s in types),None)
 group=re.match(r'^(\d+) (Viga\(s\)|Laje\(s\)|Pilar\(es\)|Sapata\(s\)) com (.+)$',label)
 if group:groups.append(dict(branch=branch,floor=floor,elementType=typ,nativeGroupLabel=label,count=int(group[1])))
 message=re.match(r'^(Erro|Aviso) (\w+) - (.+)$',label)
 if message:
  assert floor is not None and typ is not None and parents
  records.append(dict(branch=branch,floor=floor,elementType=typ,nativeElement=parents[-1],kind=message[1],code=message[2],message=message[3],source='árvore de status expandida pelo comando nativo'))
 stack.append((depth,label))
assert groups and records
dest=out/f'{branch}-status-estruturado.json';assert not dest.exists()
dest.write_text(json.dumps(dict(branch=branch,source=str(p),sourceSha256=hashlib.sha256(p.read_bytes()).hexdigest(),groups=groups,messages=records,interpretation='Mensagens do programa; nao comprovam dimensionamento completo nem atendimento normativo',foundationsExcludedFromResearch=True),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
copy=out/Path(__file__).name
if not copy.exists():shutil.copy2(Path(__file__),copy)
else:assert copy.read_bytes()==Path(__file__).read_bytes()
print(json.dumps(dict(branch=branch,groups=groups,messageCounts=[dict(elementType=k[0],kind=k[1],code=k[2],count=v) for k,v in Counter((r['elementType'],r['kind'],r['code']) for r in records).items()],beamMessageCount=sum(r['elementType']=='viga' for r in records),beamErrorMessageCount=sum(r['elementType']=='viga' and r['kind']=='Erro' for r in records)),ensure_ascii=False))

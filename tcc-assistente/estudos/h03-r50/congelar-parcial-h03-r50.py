from pathlib import Path
import json,hashlib,shutil
from datetime import datetime,timezone
root=Path('D:/TCC');out=root/'outputs/Complementacao-H03-R50-LAJES-BIM-NAO-EXECUTAR'
native=root/'outputs/H03_BIM_R50_LAJES_NAO_EXECUTAR'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for folder in ('Projeto Eberick','_DADOS_'):
    for p in (native/folder).rglob('*'):
        if not p.is_file() or p.suffix.lower() in ('.bak','.lck','.tmp'):continue
        target=out/'congelado-dez-lajes'/p.relative_to(native)
        target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():assert sha(target)==sha(p),str(target)
        else:shutil.copy2(p,target)
        records.append(dict(path=str(p),frozen=str(target),sha256=sha(p)))
(out/'R50-congelamento-dez-lajes.json').write_text(json.dumps(dict(atUtc=datetime.now(timezone.utc).isoformat(),files=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(frozenFiles=len(records))))

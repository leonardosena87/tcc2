"""Prepara copia do receptor BIM R46; nao importa geometria CAD."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,time
start=time.perf_counter();at=datetime.now(timezone.utc).isoformat()
root=Path('D:/TCC');src=root/'outputs/Intercambio-H03-R46-BIM-NAO-EXECUTAR'
dst=root/'outputs/H03_BIM_R50_LAJES_NAO_EXECUTAR/Projeto Eberick'
out=root/'outputs/Complementacao-H03-R50-LAJES-BIM-NAO-EXECUTAR'
dst.mkdir(parents=True,exist_ok=False);out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((src/'R46-estados-congelados.json').read_text(encoding='utf-8'))
files=[]
for row in manifest['files']:
    if row['branch']!='BIM':continue
    a=Path(row['frozen']);assert sha(a)==row['sha256']
    rel=a.relative_to(src/'congelado');b=dst/rel
    b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b);assert sha(a)==sha(b)
    files.append(dict(source=str(a),copy=str(b),sha256=sha(b)))
r=dict(atUtc=at,files=files,nativeProject=str(dst/'H03_BIM_R46_IFC_NAO_EXECUTAR.prj'),
       status='COPIA PREPARADA; LAJES AINDA NAO LANCADAS',
       preparationScriptElapsedMs=(time.perf_counter()-start)*1000,
       limits=['Tempo apenas do script, nao inclui operacao no Eberick.',
               'Nome-base R46 mantido para conservar caminhos relativos do modelo externo; pasta identifica R50.',
               'Conferir associacao externa ao abrir; nao substituir modelo recebido por copia CAD.'])
(out/'R50-preparacao.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
print(json.dumps(dict(files=len(files),nativeProject=r['nativeProject'],preparationScriptElapsedMs=r['preparationScriptElapsedMs'])))

from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
root=Path('D:/TCC');out=root/'outputs/Resultados-H03-R75-FIGURA-PARCIAL';dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r75');assert not dest.exists()
p=out/'R75-origem-dados.json';data=json.loads(p.read_text(encoding='utf-8'));data.update(visualQAStatus='aprovada: PNG integral inspecionado, texto legivel, sem sobreposicao/corte, setas e limites claros',visualQAUtc=datetime.now(timezone.utc).isoformat());p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(out/'R75-manifesto.json').write_text(json.dumps(dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file()]),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dest.mkdir()
for p in out.iterdir():shutil.copy2(p,dest/p.name);assert sha(p)==sha(dest/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig');guide.write_text('# Atualizacao R75 — figura de resultados parciais\n\nPNG180dpi e SVG revisados visualmente em outputs/Resultados-H03-R75-FIGURA-PARCIAL. Mostram conteudo CAD, chegada BIM apos adaptador, complementacoes62/11unidades e checkpoint65pares. Nao sao contagem de erros/operacoes nem tempos finais. Nenhuma insercao na monografia. Estado nativo continuaR64; prioridadesR72/R74, Qnaoaplicado.\n\n---\nHistorico anterior:\n\n'+old,encoding='utf-8')
print('R75 figura verificada e arquivada')

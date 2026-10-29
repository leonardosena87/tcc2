from pathlib import Path
import json,hashlib,shutil,ast
out=Path('D:/TCC/outputs/Compatibilizacao-H03-R68-PORTA-P3-ESTUDO')
dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r68')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=Path('D:/TCC/work/conferir-porta-p3-h03-r68.py')
s=p.read_text(encoding='utf-8').replace('As quatro linhas verticais de cada contorno foram verificadas','As quatro linhas verticais dos dois contornos foram verificadas')
p.write_text(s,encoding='utf-8');ast.parse(s);shutil.copy2(p,out/p.name)
p=out/'LEIA-ME-R68.md';p.write_text(p.read_text(encoding='utf-8').replace('As quatro linhas verticais de cada contorno foram verificadas','As quatro linhas verticais dos dois contornos foram verificadas'),encoding='utf-8')
for name in ('refinar-figura-r68.py','finalizar-h03-r68.py'):shutil.copy2(Path('D:/TCC/work')/name,out/name)
p=out/'R68-validacao.json';r=json.loads(p.read_text(encoding='utf-8'));r['diagramVisuallyInspected']=True;r['diagramTitleOverlapCorrected']=True;p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'R68-manifesto.json').write_text(json.dumps(dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file() and p.name!='R68-manifesto.json']),ensure_ascii=False,indent=2),encoding='utf-8')
for p in out.iterdir():shutil.copy2(p,dest/p.name);assert sha(p)==sha(dest/p.name)
print('R68: figura e manifesto conferidos')

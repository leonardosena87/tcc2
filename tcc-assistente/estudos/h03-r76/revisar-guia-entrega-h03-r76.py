"""Revisa apenas guia deste pacote e recalcula sua integridade; origens intactas."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,shutil,ast
root=Path('D:/TCC');package=root/'entrega-orientador/TCC-Projetos-parciais-2026-10-29-H03-R76';archive=package.with_suffix('.zip');out=root/'outputs/Entrega-H03-R76-PARCIAL';repo=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r76')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
v=read(out/'R76-verificacao.json');assert sha(archive)==v['archiveSha256']
template=Path(__file__).with_name('R76-LEIA-ME-PARCIAL.md');script=Path(__file__).with_name('empacotar-parcial-h03-r76.py');ast.parse(script.read_text(encoding='utf-8'))
shutil.copy2(template,package/'LEIA-ME-PARCIAL.md')
files=[dict(relative=str(p.relative_to(package)).replace('\\','/'),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(package.rglob('*')) if p.is_file() and p.name!='R76-manifesto-sha256.json']
(package/'R76-manifesto-sha256.json').write_text(json.dumps(dict(files=files,manifestItselfExcluded=True),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(package.rglob('*')):
  if p.is_file():z.write(p,str(p.relative_to(package)).replace('\\','/'))
with ZipFile(archive) as z:
 assert z.testzip() is None and len(z.namelist())==66
 for f in files:assert hashlib.sha256(z.read(f['relative'])).hexdigest()==f['sha256']
for s in read(out/'R76-mapeamento-fontes.json')['sources']:assert sha(Path(s['source']))==s['sha256']
v.update(archiveSha256=sha(archive),archiveBytes=archive.stat().st_size,readmeLanguageAndScopeReviewed=True)
(out/'R76-verificacao.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p in (template,script,Path(__file__)):shutil.copy2(p,out/p.name)
shutil.copy2(template,out/'LEIA-ME-R76.md')
(out/'R76-manifesto.json').write_text(json.dumps(dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file() and p.name!='R76-manifesto.json']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p in out.iterdir():shutil.copy2(p,repo/p.name);assert sha(p)==sha(repo/p.name)
print(json.dumps(dict(archive=str(archive),bytes=v['archiveBytes'],sha256=v['archiveSha256'],files=66,sourceFilesUnchanged=True),ensure_ascii=False))

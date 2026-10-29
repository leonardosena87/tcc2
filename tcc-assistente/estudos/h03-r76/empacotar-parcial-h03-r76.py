"""Entrega parcial local para revisao; nao transmite arquivos e nao muda nativos."""
from pathlib import Path
from datetime import datetime,timezone
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,shutil,ast
root=Path('D:/TCC');name='TCC-Projetos-parciais-2026-10-29-H03-R76'
package=root/'entrega-orientador'/name;archive=package.with_suffix('.zip')
out=root/'outputs/Entrega-H03-R76-PARCIAL';repo=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r76')
assert not package.exists() and not archive.exists() and not out.exists() and not repo.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(root/'outputs/Resultados-H03-R75-FIGURA-PARCIAL/R75-manifesto.json')['files']
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
manifest46=read(root/'outputs/Intercambio-H03-R46-BIM-NAO-EXECUTAR/R46-manifesto.json')['files'];expected46={Path(r['path']):r['sha256'] for r in manifest46}
sources=[]
def add(src,relative,expected=None,role='evidencia',revision=None):
 assert src.is_file(),src
 if expected:assert sha(src)==expected,src
 assert not any(s['relative']==str(relative).replace('\\','/') for s in sources),relative
 sources.append(dict(source=str(src),relative=str(relative).replace('\\','/'),sha256=sha(src),bytes=src.stat().st_size,role=role,revision=revision))
r43=root/'outputs/Alternativa-H03-R43-ESTUDO-NAO-EXECUTAR'
for n in ('H03-R43-Revit.rvt','H03-R43-AutoCAD.dwg','H03-R43-proposta.json','H03-R43-N1.dxf','H03-R43-N2.dxf','H03-R43-Revit.ifc','LEIA-ME-R43.md'):
 p=r43/n;assert p in expected46,n;add(p,p.relative_to(root),expected46[p],'autoria anterior as revisoes no receptor','R43')
arch=root/'PROJETO ARQUITETONICO-A0.pdf';add(arch,'arquitetura/'+arch.name,'3a57561f03e2c0e92964b19e577a02939b04fc93cdf1ef27cad6f79ad2deb12d','arquitetura de referencia','origem')
r44=root/'outputs/Intercambio-H03-R44-ESTUDO-NAO-EXECUTAR'
for n in ('H03-R44-geometria-nominal.ifc','H03-R44-geometria-nominal.adaptacao.json','LEIA-ME-R44.md'):
 p=r44/n;add(p,p.relative_to(root),expected46.get(p),'IFC adaptado de entrada; dependencia relativa BIM','R44')
prior=root/'outputs/Cargas-H03-R64-CONFERENCIA-INDIVIDUAL-NAO-EXECUTAR';nativeMeta={};excludedLogs=[]
for branch in ('CAD','BIM'):
 state=read(prior/f'R64-estado-{branch}.json');destFolder=Path(state['nativeProject']).parent.parent.relative_to(root)
 for r in state['frozenFiles']:
  p=Path(r['frozen']);assert sha(p)==r['sha256'],p
  relative=p.relative_to(prior/f'congelado-{branch}')
  if p.suffix.lower()=='.log':excludedLogs.append(str(p));continue
  add(p,destFolder/relative,r['sha256'],'nativo '+branch+' com dependencias congeladas','R64')
 nativeMeta[branch]=dict(projectRelative=str(destFolder/'Projeto Eberick'/Path(state['nativeProject']).name).replace('\\','/'),prjSha256=state['nativeSha256'],originalState=str(prior/f'R64-estado-{branch}.json'))
 with ZipFile(state['nativeProject']) as z:assert z.testzip() is None
r57=root/'outputs/Verificacao-H03-R57-NAO-EXECUTAR'
for b in ('CAD','BIM'):
 p=r57/f'IFC-{b}/Modelo 3D.IFC';add(p,p.relative_to(root),read(r57/'R57-resultado.json')['audits'][b]['sha256'],'IFC de controle do receptor, geometria R57','R57')
selected={
'Cargas-H03-R63-AUDITORIA-AMPLIACAO-NAO-EXECUTAR':['LEIA-ME-R63.md'],
'Cargas-H03-R64-CONFERENCIA-INDIVIDUAL-NAO-EXECUTAR':['LEIA-ME-R64.md','R64-resultado.json'],
'Cobertura-H03-R65-PLANO-Q-NAO-APLICADO':['LEIA-ME-R65.md'],
'Compatibilizacao-H03-R68-PORTA-P3-ESTUDO':['LEIA-ME-R68.md','R68-referencia-arquitetonica-estudo.json'],
'Resultados-H03-R69-TEMPOS-EXPLORATORIOS':['LEIA-ME-R69.md','PROTOCOLO-ENSAIO-PAREADO.md','R69-inventario-tempos.json'],
'Compatibilizacao-H03-R70-W08-J4-ESTUDO':['LEIA-ME-R70.md'],
'Reservatorio-H03-R71-ALTERNATIVAS-NAO-APLICADO':['LEIA-ME-R71.md','R71-reservatorio-alternativas.json'],
'Resultados-H03-R72-PARCIAIS-NAO-FINAIS':['LEIA-ME-R72.md','R72-resultados-parciais.json','R72-matriz-fechamento.csv','R72-mapa-CAD-BIM-65-solidos.csv'],
'Normativa-H03-R74-TRIAGEM-NAO-DIMENSIONADO':['LEIA-ME-R74.md','R74-resultado.json','R74-complemento-matriz-fechamento.json','R74-versao-instalada.json'],
'Resultados-H03-R75-FIGURA-PARCIAL':['LEIA-ME-R75.md','R75-fluxos-resultados-parciais.png','R75-fluxos-resultados-parciais.svg']}
# A pasta R63 e localizada por nome de relatorio unico, sem escolher estado por data.
for directory,names in selected.items():
 folder=root/'outputs'/directory
 if not folder.exists() and directory.startswith('Cargas-H03-R63-'):
  matches=[p for p in (root/'outputs').glob('*R63*') if (p/'LEIA-ME-R63.md').is_file()];assert len(matches)==1;folder=matches[0]
 for n in names:
  p=folder/n;add(p,p.relative_to(root),role='resultado parcial ou protocolo',revision=directory.split('-R')[-1].split('-')[0])
out.mkdir();package.mkdir()
for r in sources:
 p=Path(r['source']);q=package/r['relative'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==r['sha256']
# O vinculo externo relativo deve resolver dentro da entrega, nao depender do D: original.
bimPrj=package/nativeMeta['BIM']['projectRelative'];link=next((bimPrj.parent/(bimPrj.stem+'_Modelos 3D')).glob('Vinculo*.ini'));lines=link.read_text(encoding='cp1252').splitlines();value=next(x.split('=',1)[1] for x in lines if x.lower().startswith('caminho='));target=(link.parent/Path(value)).resolve();assert target.is_relative_to(package.resolve()) and target.is_file();assert sha(target)==sha(r44/'H03-R44-geometria-nominal.ifc')
readme=Path(__file__).with_name('R76-LEIA-ME-PARCIAL.md').read_text(encoding='utf-8')
(package/'LEIA-ME-PARCIAL.md').write_text(readme,encoding='utf-8')
mapping=dict(revision='H03/R76',createdUtc=datetime.now(timezone.utc).isoformat(),sources=sources,nativeProjects=nativeMeta,relativeBIMExternalTarget=str(target.relative_to(package)).replace('\\','/'),excludedNativeLogs=excludedLogs,sourceAuthoringRevision='R43',receiverEngineeringRevision='R64',sourceNativeRevisionsSynchronized=False,localCopyOnly=True,externallySent=False,appOpeningRepeated=False,crossMachinePortabilityVerified=False,structuralApproval=False)
(package/'R76-mapeamento-fontes.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[dict(relative=str(p.relative_to(package)).replace('\\','/'),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(package.rglob('*')) if p.is_file()]
(package/'R76-manifesto-sha256.json').write_text(json.dumps(dict(files=files,manifestItselfExcluded=True),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with ZipFile(archive,'x',compression=ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(package.rglob('*')):
  if p.is_file():z.write(p,str(p.relative_to(package)).replace('\\','/'))
with ZipFile(archive) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(files)+1
 for f in files:assert hashlib.sha256(z.read(f['relative'])).hexdigest()==f['sha256']
 for n in z.namelist():assert not (n.startswith('/') or '..' in Path(n).parts or Path(n).suffix.lower() in ('.env','.pem','.pfx','.p12','.log'))
for r in sources:assert sha(Path(r['source']))==r['sha256']
verification=dict(revision='H03/R76',package=str(package),archive=str(archive),archiveSha256=sha(archive),archiveBytes=archive.stat().st_size,fileCountIncludingManifest=len(files)+1,copiedSourceFiles=len(sources),allCopiedHashesPassed=True,archiveCRCAndAllEntryHashesPassed=True,bothNativePrjZipIntegrityPassed=True,relativeIFCLinkResolvesInsidePackage=True,originalSourcesUnchanged=True,sourceNativeRevisionsSynchronized=False,appOpeningRepeated=False,crossMachinePortabilityVerified=False,externallySent=False,structuralApproval=False)
for n,value in [('R76-verificacao.json',verification),('R76-mapeamento-fontes.json',mapping),('R76-protegidos-R75.json',protected)]:
 (out/n).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(Path(__file__).with_name('R76-LEIA-ME-PARCIAL.md'),out/'R76-LEIA-ME-PARCIAL.md');shutil.copy2(package/'LEIA-ME-PARCIAL.md',out/'LEIA-ME-R76.md');shutil.copy2(Path(__file__),out/Path(__file__).name);ast.parse(Path(__file__).read_text(encoding='utf-8'))
(out/'R76-manifesto.json').write_text(json.dumps(dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file()]),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
repo.mkdir()
for p in out.iterdir():shutil.copy2(p,repo/p.name);assert sha(p)==sha(repo/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig');guide.write_text(f'# Atualizacao R76 — entrega parcial local atualizada\n\nZIP:{archive}\nOrigemRevit/AutoCADR43, receptoresEberickR64comcompanheiros eIFCexternoR44relativoincluido. ResultadosR72, figuraR75, normasR74, temposR69 ependenciasincluidos. Revisoesdeautoria/receptoraindaNAOsincronizadas, explicitadoREADME. CRC/SHAverificados; NAOaberturanativarepetidaouportabilidadeouenvio. Naoalteroumonografiaouorigens. LerLEIA-ME-PARCIAL.md. UltimoestadorealengenhariaR64; Q_R65naoaplicado; R73cancelada.\n\n---\nHistorico anterior:\n\n'+old,encoding='utf-8')
print(json.dumps(verification,ensure_ascii=False))

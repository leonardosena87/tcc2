"""Confere seis consultas nativas e audita IFC pos-verificacao sem certificar calculo."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,shutil,zipfile,time
sys.path.insert(0,'D:/TCC/work/ifc/deps')
import ifcopenshell,ifcopenshell.geom as geom,ifcopenshell.util.element
import numpy as np
root=Path('D:/TCC');out=root/'outputs/Verificacao-H03-R57-NAO-EXECUTAR'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(name,value):(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=time.perf_counter();utc=datetime.now(timezone.utc).isoformat()
def clean(x):
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items() if k!='id'}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 return x
def extract(p):
 m=ifcopenshell.open(str(p));s=geom.settings();s.set(s.USE_WORLD_COORDS,True);rows=[]
 for cls in ('IfcColumn','IfcBeam','IfcSlab','IfcFooting'):
  for o in m.by_type(cls):
   sh=geom.create_shape(s,o);v=np.array(sh.geometry.verts).reshape(-1,3);f=np.array(sh.geometry.faces).reshape(-1,3);top=v[:,2].max()
   area=sum(float(np.linalg.norm(np.cross(v[t][1]-v[t][0],v[t][2]-v[t][0]))/2) for t in f if np.max(abs(v[t][:,2]-top))<1e-5)
   rows.append(dict(type=cls,name=o.Name,guid=o.GlobalId,min=[round(float(a),6) for a in v.min(0)],max=[round(float(a),6) for a in v.max(0)],topAreaM2=round(area,6),exportedProperties=clean(ifcopenshell.util.element.get_psets(o))))
 return sorted(rows,key=lambda r:r['guid'])
audits={};states={};times={};checks=[]
protected=read(out/'R57-protegidos-R56.json')
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
for b in ('CAD','BIM'):
 for level in ('N2','N1','N0'):
  p=out/f'{b}-{level}-lancamento-UI.txt';text=p.read_text(encoding='utf-8')
  assert 'Não foram detectados problemas no lançamento deste pavimento.' in text
  assert f'Croqui-{level}' in text or f'Croqui-TCC-cdd31967-{level}' in text
  checks.append(dict(branch=b,level=level,result='Nao foram detectados problemas no lancamento deste pavimento.',detectedMessages=0,evidence=str(p),sha256=sha(p)))
 old=root/f'outputs/Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR/IFC-{b}/Modelo 3D.IFC';new=out/f'IFC-{b}/Modelo 3D.IFC'
 before=extract(old);after=extract(new)
 superBefore=[r for r in before if r['type']!='IfcFooting'];superAfter=[r for r in after if r['type']!='IfcFooting']
 assert len(superBefore)==65 and superBefore==superAfter,(b,'Alteracao na superestrutura; investigar antes de consolidar')
 auxBefore=[r for r in before if r['type']=='IfcFooting'];auxAfter=[r for r in after if r['type']=='IfcFooting'];auxPairs=[];matched=set()
 assert len(auxBefore)==len(auxAfter)==11
 for r in auxBefore:
  candidates=[n for n in auxAfter if n['name']==r['name'] and n['min']==r['min'] and n['max']==r['max']]
  assert len(candidates)==1,(b,'Correspondencia auxiliar ambigua',r['name'])
  n=candidates[0]
  assert n['guid'] not in matched,(b,'Auxiliar duplicado',n['guid'])
  matched.add(n['guid'])
  assert {k:v for k,v in r.items() if k!='guid'}=={k:v for k,v in n.items() if k!='guid'},(b,'Alteracao em auxiliar alem do GUID',r['name'])
  auxPairs.append(dict(name=r['name'],oldGuid=r['guid'],newGuid=n['guid'],guidChanged=r['guid']!=n['guid'],min=r['min'],max=r['max'],allOtherExtractedFieldsPreserved=True))
 write(f'R57-identidade-auxiliares-{b}.json',auxPairs)
 audits[b]=dict(source=str(new),sha256=sha(new),baseline=str(old),baselineSha256=sha(old),objectsChecked=len(after),counts={c:sum(r['type']==c for r in after) for c in ('IfcColumn','IfcBeam','IfcSlab','IfcFooting')},superstructureObjectsChecked=len(superAfter),superstructureNamesGuidsBoxesTopAreasAndExportedPropertiesPreserved=True,auxiliaryGuidChanges=sum(r['guidChanged'] for r in auxPairs),auxiliaryNamesBoxesTopAreasAndExportedPropertiesPreserved=True,matchingAuxiliaries='Correspondencia unica por nome e caixa; comparacao de todos os demais campos extraidos, exceto GUID',analyticalModelVerified=False)
 write(f'R57-auditoria-{b}.json',audits[b])
 prep=read(out/f'R57-preparacao-{b}.json');native=Path(prep['nativeProject']);basedir=native.parent.parent;frozen=out/f'congelado-{b}';files=[]
 with zipfile.ZipFile(native) as z:assert z.testzip() is None
 for p in sorted(basedir.rglob('*')):
  if not p.is_file() or p.suffix.lower() in ('.bak','.tmp'):continue
  q=frozen/p.relative_to(basedir);q.parent.mkdir(exist_ok=True,parents=True)
  if q.exists():assert sha(q)==sha(p),q
  else:shutil.copy2(p,q)
  files.append(dict(path=str(p),frozen=str(q),sha256=sha(q)))
 states[b]=dict(nativeProject=str(native),nativeSha256=sha(native),frozenFiles=files,launchCheckedFloors=['N2','N1','N0'],engineeringLoadsModified=False,integrityVerificationOnOpeningPerformed=b=='CAD',structuralCalculationPerformed=False)
 write(f'R57-estado-{b}.json',states[b]);times[b]=read(out/f'R57-tempo-{b}.json')
assert 'Detectou-se que ocorreu um erro' in (out/'CAD-aviso-abertura-UI.txt').read_text(encoding='utf-8')
assert 'Detectou-se que ocorreu um erro' not in (out/'CAD-reabertura-apos-verificacao-UI.txt').read_text(encoding='utf-8')
fmt=lambda ms:f'{int(ms//60000)} min {(ms%60000)/1000:.3f} s'
result=dict(revision='H03/R57',atUtc=datetime.now(timezone.utc).isoformat(),checks=checks,audits=audits,
 zeroMessagesInAllSixLaunchChecks=True,protectedR56FilesChecked=len(protected),
 CADOpeningIntegrityWarning=True,CADIntegrityVerificationExecuted=True,CADReopenedWithoutRepeatingWarning=True,
 warningRootCauseProven=False,warningClassification='Ocorrencia operacional local sem causa comprovada; nao atribuida a erro de transferencia CAD/DWG.',
 supportsIdealizedOnly=True,realFoundationsDesigned=False,completeLoads=False,structuralCalculationPerformed=False,
 CADBIMWholeFlowRankingAllowed=False,times={b:dict(**t,formatted=fmt(t['durationMs'])) for b,t in times.items()})
write('R57-resultado.json',result)
write('R57-execucao-auditor.json',dict(startUtc=utc,endUtc=datetime.now(timezone.utc).isoformat(),durationMs=(time.perf_counter()-start)*1000,scope='Somente auditor/consolidacao; exclui preparacao, operacao nativa e revisao'))
report=f'''# H03/R57 — verificacao nativa do lancamento

Revisao de 29/10/2026 em copias independentes dos estados R56 congelados. Nao executar: modelo academico com cargas parciais, sem dimensionamento. A monografia, RVT e DWG de origem nao foram alterados.

Executou-se Lancamento > Outros > Verificar lancamento no N2, N1 e N0 de cada ramo. As seis consultas retornaram "Nao foram detectados problemas no lancamento deste pavimento". Cada consulta possui TXT de acessibilidade com identificacao do croqui e mensagem do programa. O retorno se limita ao conjunto de verificacoes desse comando; nao constitui comprovacao de ligacoes analiticas, resistencia, estabilidade, deformacoes, cargas completas ou atendimento integral a normas.

Na abertura CAD R57 apareceu aviso de possivel inconsistencia na ultima edicao. Executou-se Verificar projeto danificado na copia de estudo, cujo calculo ainda nao havia sido processado nesta H03. Depois verificaram-se os tres croquis e salvou-se. Na reabertura do CAD, o aviso nao voltou a aparecer. O BIM abriu sem esse aviso. Nao foi determinada a causa; nao contar como defeito comprovado de transferencia DWG/IFC. O intervalo CAD inclui essa ocorrencia e a localizacao do comando (a primeira selecao de barras foi cancelada sem executar, ampliou-se a janela para acessar o comando correto). A verificacao de integridade e uma operacao nativa de consistencia, nao um processamento estrutural bem-sucedido.

Exportou-se IFC4 de ambos apos as consultas; o CAD foi reaberto antes da exportacao. A comparacao com a propria R56 manteve 76 objetos por ramo: 22 IfcColumn, 32 IfcBeam, 11 IfcSlab e 11 IfcFooting. Nos 65 objetos da superestrutura preservaram-se nomes, GUIDs, caixas envolventes arredondadas a seis casas decimais em metros, areas superiores arredondadas a seis casas e todas as propriedades exportadas retornadas por get_psets, excluindo apenas o identificador interno numerico "id". Os 11 IfcFooting de cada ramo receberam novos GUIDs. Cada auxiliar foi associado de forma unica por nome e caixa; todos os demais campos extraidos permaneceram iguais. As correspondencias e os GUIDs antigos/novos estao nos JSONs R57-identidade-auxiliares. Trata-se de variacao de identidade observada entre exportacoes; a causa nao foi determinada e nao se comprovou perda geometrica ou erro de transferencia. As cargas Q/G2 parciais das lajes permanecem identicas. Nao se comparou malha integral, nem se certificou que todo parametro nativo e exportado. Os auxiliares continuam excluidos dos quantitativos da superestrutura e nao representam fundacoes executivas. Integridade ZIP dos dois PRJs aprovada; preservados os {len(protected)} hashes R56. Estados nativos R57 congelados em separado.

## Tempos prospectivos da consulta assistida

| Ramo | Abrir, consultar N2/N1/N0 e salvar |
|---|---:|
| CAD | {fmt(times['CAD']['durationMs'])} |
| BIM | {fmt(times['BIM']['durationMs'])} |

Incluem raciocinio/latencia; CAD inclui verificacao de integridade, consulta de suporte e descoberta do comando; BIM usa procedimento conhecido e janela ja ampliada. Nao e repeticao controlada e nao mede tempo humano ativo ou inferencia de IA isolada. Nao gerar ranking dos fluxos completos. A reabertura adicional CAD e as exportacoes posteriores nao pertencem a esses intervalos; nao foram cronometradas como etapas completas. O auditor tem duracao propria de execucao, sem preparacao/revisao.

## Pendencias

Nenhuma carga nova foi aplicada. Permanecem a matriz bruta de paredesR56 (W08/base da escada desconhecida), as acoes do telhado/camadas, reservatorio1000L/apoio, escada, bordas/guarda-corpo, vento/combinacoes, confirmacao de apoios/ligacoes analiticas e sensibilidade da barra auxiliar. As vigas de cobertura20x30 sao apenas alternativa geometrica sem ELU/ELS. Faltam processamento, estabilidade e deformacoes; depois selecionar concepcao e atualizar arquivos de origem e textos manuais CAD. Usar novas copias a partir da R57 para completar acoes e diagnosticar.

Referencias operacionais oficiais: [verificacao por pavimento](https://suporte.altoqi.com.br/hc/pt-br/articles/115004249733) e [verificacao/recuperacao de arquivo](https://suporte.altoqi.com.br/hc/pt-br/articles/115002084993). Nenhum envio de relatorio para terceiros foi realizado.
'''
(out/'LEIA-ME-R57.md').write_text(report,encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
write('R57-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='R57-manifesto.json']))
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
intro=f'''# Atualizacao R57 — 29/10/2026

Estados atuais: outputs/H03_CAD_R57_VERIFICACAO_NAO_EXECUTAR e H03_BIM_R57_VERIFICACAO_NAO_EXECUTAR. Cada um deriva da propria R56. Ver outputs/Verificacao-H03-R57-NAO-EXECUTAR/LEIA-ME-R57.md. Verificar lancamento executado em N2/N1/N0 de cada ramo: seis retornos sem problemas. CAD exibiu aviso de possivel inconsistencia ao abrir; executou-se verificacao nativa de integridade, salvou-se/reabriu-se sem repetir aviso; causa nao comprovada. IFCs mantiveram 76 objetos por ramo: 65 da superestrutura com nomes/GUIDs/caixas/areas/propriedades exportadas preservados; 11 auxiliares com GUIDs alterados, associados unicamente por nome/caixa e demais campos preservados em relacao a propria R56. Nao houve processamento estrutural nem novas cargas. Apoios idealizados, sem fundacoes reais.

Tempos assistidos CAD {fmt(times['CAD']['durationMs'])}; BIM {fmt(times['BIM']['durationMs'])}; CAD inclui ocorrencia operacional e descoberta do comando, sem ranking. Cargas parciais. Vigas20x30 de cobertura ainda nao dimensionadas; origemRVT/DWG e textos CAD manuais aguardam escolha tecnica. Proximo: completar acoes, confirmar apoios/ligacoes e processar diagnostico; verificar ELU/ELS. Nao alterar monografia. Eberick no CADR57 salvo apos exportacao, janela ampliada1920x1040, sem dialogos.

---
Historico anterior:

'''
if not old.startswith('# Atualizacao R57'):guide.write_text(intro+old,encoding='utf-8')
print(json.dumps(dict(checks=len(checks),messages=0,audits=audits,times={b:fmt(t['durationMs']) for b,t in times.items()})))

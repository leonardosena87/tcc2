"""Congela estados independentes R56 e atualiza matriz de paredes; sem editar modelos."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,zipfile,csv
root=Path('D:/TCC');out=root/'outputs/Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(name,value):(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
v=read(out/'R56-validacao.json');assert v['allRoofBeams30cmBoth']
for r in read(out/'R56-protegidos-R54.json'):assert sha(Path(r['path']))==r['sha256']
states={};times={}
for b in ('CAD','BIM'):
 prep=read(out/f'R56-preparacao-{b}.json');native=Path(prep['nativeProject']);assert native.is_file()
 with zipfile.ZipFile(native) as z:assert z.testzip() is None
 basedir=native.parent.parent;frozen=out/f'congelado-{b}';files=[]
 for p in sorted(basedir.rglob('*')):
  if not p.is_file() or p.suffix.lower() in ('.bak','.tmp'):continue
  dest=frozen/p.relative_to(basedir);dest.parent.mkdir(exist_ok=True,parents=True)
  if dest.exists():assert sha(dest)==sha(p),dest
  else:shutil.copy2(p,dest)
  files.append(dict(path=str(p),frozen=str(dest),sha256=sha(dest)))
 sample=(out/f'{b}-V4-N2-reaberto-UI.txt').read_text(encoding='utf-8')
 assert 'h Value: 30' in sample and 'bw Value: 20' in sample and '/ Value: 0' in sample
 states[b]=dict(nativeProject=str(native),nativeSha256=sha(native),frozenFiles=files,
  sourceNativeState='R54 congelado proprio',saveCloseReopenPerformed=True,
  nativeUIReopenedSample=v['nativeUIReopenSamples'][b],allRoofBeamHeightsAuditedByIFC=True,
  structurallyAccepted=False,calculationPerformed=False,originRVTorDWGUpdated=False,
  timesExportMetadataSaved=True)
 write(f'R56-estado-{b}.json',states[b]);times[b]=read(out/f'R56-tempo-{b}.json')
# Os cortes XY R55 continuam validos: auditor comprovou mesmas projecoes XY.
old=read(root/'outputs/Paredes-H03-R55-ESTUDO-NAO-EXECUTAR/R55-trechos.json')['segments']
geometry=read(out/'R56-geometria-exportada.json');segments=[]
for source in old:
 r=dict(source);mid=[(r['p1'][i]+r['p2'][i])/2 for i in (0,1)]
 hit=lambda o:all(o['min'][i]-1e-6<=mid[i]<=o['max'][i]+1e-6 for i in (0,1))
 upper=[o for o in geometry['CAD'] if o['type'] in ('IfcBeam','IfcSlab') and abs(o['max'][2]-6.39)<1e-6 and hit(o)]
 upperb=[o for o in geometry['BIM'] if o['type'] in ('IfcBeam','IfcSlab') and abs(o['max'][2]-6.39)<1e-6 and hit(o)]
 r['upperNativeNames']=[o['name'] for o in upper];r['upperNativeNamesBIM']=[o['name'] for o in upperb]
 r['upperSoffitM']=min((o['min'][2] for o in upper),default=None)
 r['grossHeightReferenceM']=round(r['upperSoffitM']-r['baseFinishedM'],6) if r['upperSoffitM'] is not None and r['baseFinishedM'] is not None else None
 r['grossLinearKNm']=round(1.565*r['grossHeightReferenceM'],6) if r['grossHeightReferenceM'] is not None and r['route']!='coluna-sem-alvenaria' else None
 r['ceilingInterference']=r['route']!='coluna-sem-alvenaria' and r['ceilingReferenceM'] is not None and r['upperSoffitM'] is not None and r['upperSoffitM']<r['ceilingReferenceM']-1e-6
 r['sourceGeometryRevision']='IFC R56';r['readyForNativeApplication']=False;segments.append(r)
assert len(segments)==59 and not any(r['ceilingInterference'] for r in segments)
assert all(r['grossLinearKNm'] is None for r in segments if r['wallId']=='W08')
write('R56-paredes-trechos.json',dict(segments=segments,source='R55 eixos/aberturas e IFC R56; carga bruta preliminar sem descontos',allLoadsApplied=False))
with (out/'R56-paredes-trechos.csv').open('w',encoding='utf-8-sig',newline='') as f:
 keys=['wallId','fromM','toM','lengthM','route','lowerNativeNames','lowerNativeNamesBIM','baseFinishedM','upperSoffitM','grossHeightReferenceM','grossLinearKNm','ceilingReferenceM','ceilingInterference','appliedToNative']
 w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore',delimiter=';');w.writeheader();w.writerows(segments)
fmt=lambda ms:f'{int(ms//60000)} min {(ms%60000)/1000:.3f} s'
summary=dict(revision='H03/R56',atUtc=datetime.now(timezone.utc).isoformat(),branches=states,
 allRoofBeams30cmBoth=True,changedRoofBeamSolidsPerBranch=13,totalRoofBeamSolidsPerBranch=15,
 preservedRelativeToOwnR53=['22 pilares: caixas/nomes/GUIDs/areas superiores','11 lajes: caixas/nomes/GUIDs/areas superiores/campos brutos Q/G2','17 solidos de vigas N1: caixas/nomes/GUIDs/areas superiores'],
 auxiliaryFootingsPerBranch=11,auxiliaryFootingsExcluded=True,
 commonConceptionRevisionNotTransferDefect=True,wallSegments=59,wallSegmentsIntersectingCeilingReferenceAfter=0,
 clearanceVerifiedForInstalledCeilingSystem=False,
 sourceRVTandDWGStillPreviousGeometry=True,manualCADAnnotationsStale=True,
 times={b:dict(**t,formatted=fmt(t['durationMs'])) for b,t in times.items()},wholeFlowRankingAllowed=False,
 structuralAcceptance=False,completeLoads=False,structuralCalculationPerformed=False,
 pending=['Cargas de paredes ainda brutas e nao aplicadas; W08/base da escada pendente','Telhado/camadas finais, tanque1000L e apoio, escada, bordas/guarda-corpo','Vento e combinacoes','Verificacao nativa de lancamento, ligacoes analiticas e apoios; sensibilidade da barra auxiliar','Processamento e verificacoes ELU/ELS, estabilidade e deformacoes','Compatibilizar instalacoes e sistema de forro no espaco geometrico residual','Atualizar origem Revit/AutoCAD e anotacoes CAD apos selecionar alternativa aceita'])
write('R56-comparacao.json',summary)
report=f'''# H03/R56 — alternativa de cobertura com vigas de 30 cm

Revisao academica de 29/10/2026, NAO EXECUTAR. Alteracao real em copias nativas independentes do Eberick 2025 Infinity, cada uma derivada de seu proprio ramo R54 congelado. A monografia, RVT e DWG de origem nao foram alterados. O estado da R54 permanece preservado.

## Alteracao e verificacao

Adotou-se como alternativa geometrica a altura de 30 cm em todas as vigas da cobertura N2, mantendo largura de 20 cm, projecoes XY e elevacao zero. No CAD alterou-se o trecho V3_1 e copiou-se apenas h para N2; no BIM alterou-se o trecho V1 e repetiu-se a copia de h apenas no N2. As opcoes carga de parede, carga extra, travamento, ambiente, elevacao, largura e demais propriedades permaneceram desmarcadas. A largura de 20cm ainda sobrepassa a parede acabada de 15cm e precisa de compatibilizacao de faces.

Salvaram-se, fecharam-se e reabriram-se ambos os PRJs. Leu-se individualmente uma amostra por ramo: CAD V4_1/N2 e BIM V4/N2, no trecho correspondente x=6,55..9,65, y=0. Ambas mostraram bw20, h30 e elevacao0. Nao se afirma leitura UI individual das 15 vigas exportadas. A auditoria IFC4 posterior a reabertura confirmou as 15 com altura30; 13 solidos tiveram altura reduzida, dois ja tinham30. O numero de solidos nao e o numero de vigas logicas. A selecao via lista incluiu somente N2. A integridade ZIP dos dois PRJs passou; arquivos nativos congelados em separado.

Em relacao ao proprio IFC R53, preservaram-se nomes/GUIDs/caixas envolventes/areas superiores dos 22 pilares, das 11 lajes e dos 17 solidos de vigas N1. Os campos brutos Q/G2 das lajes tambem permaneceram identicos; a carga continua parcial. Nas 15 vigas N2, preservaram-se nomes/GUIDs/projecoes XY/topo/areas superiores e verificou-se apenas a mudanca prevista de intradorso. O confronto CAD/BIM coincide por classe, caixas, areas superiores e campos brutos das lajes. Esse controle nao comprova identidade de toda malha nem vinculos analiticos.

Foram exportados tambem 11 IfcFooting por ramo, oriundos dos cadastros auxiliares de apoio da R54. Esses solidos padrao nao representam fundacoes dimensionadas e ficam excluidos dos quantitativos da superestrutura. O IFC manteve as bases geometricas dos pilares em +0,20m. Isso NAO valida a cota analitica da barra auxiliar de10cm nem seu comprimento efetivo ou liberacoes. Nao se infere apoio analitico por aparencia do solido. A primeira auditoria geometrica posterior a R54 foi realizada no estado R56; nao existe uma exportacao R54 retroativa.

## Compatibilizacao e cargas de paredes

Topo6,39 menos altura0,30 resulta em intradorso6,09m. Para piso3,25 e forro de referencia2,80, o plano do forro fica em6,05m: diferenca geometrica4cm. Nao se alterou a altura arquitetonica. Atualizaram-se os 59 trechos das 20 paredes R55; nenhum dos trechos com referencia de forro definida intercepta esse plano na triagem R56. Nao se verificou todo ambiente, espessura do forro, suspensao, instalacoes, tolerancias ou deformacoes futuras; portanto, nao se declara compatibilizacao executiva concluida.

A matriz R56 de paredes continua bruta, sem desconto de portas/janelas, acabamento sobre concreto, encontros, vergas/contravergas ou tara de esquadrias. A composicao hipotetica de1,565kN/m2 foi herdada da R55 e nao confirmada por fabricante. W08 continua com carga desconhecida, campo vazio. Nenhuma carga de parede foi aplicada. Nao somar essa matriz como quantitativo final. As alteracoes de intradorso mudam a altura da alvenaria, portanto reutilizar diretamente as alturas R55 seria incorreto.

As anotacoes CAD amarelas do esboco original ainda mostram secoes antigas em alguns trechos: sao textos de referencia desatualizados, nao dados estruturais correntes. O croqui BIM nao tem esses mesmos textos manuais. Registrar essa diferenca de documentacao sem transforma-la em defeito comprovado do IFC/DWG; atualizar ambos os arquivos de origem e a documentacao apos selecionar uma alternativa aceita por calculo.

## Tempos da etapa assistida

| Ramo | Abrir copia, alterar/copiar altura, salvar/reabrir e ler 1 amostra |
|---|---:|
| CAD | {fmt(times['CAD']['durationMs'])} |
| BIM | {fmt(times['BIM']['durationMs'])} |

Registros prospectivos UTC e relogio monotonico. Incluem raciocinio/latencia; CAD inclui descoberta de coordenadas de paineis flutuantes, ambiguidades de selecao e recuperacao de foco; BIM aproveita procedimento e opcoes ja conhecidos. Nao medem esforco humano ativo ou inferencia isolada de IA e nao permitem ranking dos fluxos completos. Exportacoes e execucao do auditor possuem registros separados; nao somar indiscriminadamente. A revisao e comum da concepcao no receptor, sem contagem de erro de transferencia.

## Limite estrutural e proximo passo

Nao se processou calculo nesta revisao. Reduzir h de55 para30cm reduz a inercia bruta retangular, a largura constante, para aproximadamente16,2% do valor anterior: satisfazer um plano de forro nao demonstra rigidez ou resistencia suficiente. Vao, cargas, armadura, fissuracao, fluencia e deformacoes precisam de avaliacao. A alternativa nao esta dimensionada nem aceita para execucao. Nao dispensar a possibilidade de novos apoios alinhados as paredes, conforme autorizacao do usuario, quando necessarios e compativeis com portas/janelas/circulacao.

Proximo: completar acoes, verificar lancamento/ligacoes/apoios e processar diagnostico no Eberick; avaliar ELU/ELS e deformacoes, revisando concepcao se necessario. Atualizar Revit/AutoCAD depois da escolha tecnica, com mesma referencia para ambos. Fontes operacionais oficiais: https://suporte.altoqi.com.br/hc/pt-br/articles/115002183633 e https://suporte.altoqi.com.br/hc/pt-br/articles/360014260893 .
'''
(out/'LEIA-ME-R56.md').write_text(report,encoding='utf-8')
for name in ('auditar-h03-r56.py','consolidar-h03-r56.py'):shutil.copy2(root/'work'/name,out/name)
write('R56-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='R56-manifesto.json']))
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
intro=f'''# Atualizacao R56 — 29/10/2026

Estados nativos atuais de ESTUDO: outputs/H03_CAD_R56_COBERTURA_ESTUDO_NAO_EXECUTAR e H03_BIM_R56_COBERTURA_ESTUDO_NAO_EXECUTAR. Cada ramo deriva de seu proprio R54 congelado. Vigas de N2 com h30/bw20, topo6,39, elevacao0; 1 amostra UI apos salvar/reabrir em cada ramo e todas as15 vigas exportadas auditadas. Preservados pilares/vigasN1/lajes/cargasQG2 em relacao a propria R53; 11 cadastros auxiliares IfcFooting excluidos por ramo. Conferiram-se os 36 arquivos protegidos R54. Ver LEIA-ME-R56.md em outputs/Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR.

Intradorso6,09 acima do plano de forro6,05; folga geometrica4cm sem validar sistema/instalacoes/deformacoes. A alternativa de30cm NAO foi calculada ou aceita estruturalmente. Matriz preliminar atualizada de20paredes/59trechos, nao aplicada; W08 continua pendente. Textos CAD manuais e RVT/DWG de origem ainda possuem secoes anteriores. Nao apresentar como modelos finais sincronizados. Nao alterar monografia.

Tempo assistido CAD {fmt(times['CAD']['durationMs'])}; BIM {fmt(times['BIM']['durationMs'])}, sem ranking. Proximo: completar acoes e verificar lancamento/ligacoes/apoios; processar diagnostico e ELU/ELS; revisar concepcao se necessario; sincronizar origens/documentacao apos escolha tecnica. Eberick no CAD R56, salvo apos metadados de exportacao, sem dialogos abertos.

---
Historico anterior:

'''
if not old.startswith('# Atualizacao R56'):guide.write_text(intro+old,encoding='utf-8')
print(json.dumps(dict(times={b:fmt(t['durationMs']) for b,t in times.items()},nativeFrozen={b:len(d['frozenFiles']) for b,d in states.items()},wallSegments=len(segments))))

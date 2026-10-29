"""Consolida diagnostico nativo parcial, tempos e persistencia sem aprovar ELU/ELS."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,zipfile,re,time
start=time.perf_counter()
root=Path('D:/TCC');out=root/'outputs/Processamento-H03-R58-DIAGNOSTICO-PARCIAL-NAO-EXECUTAR'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(n,v):(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
protected=read(out/'R58-protegidos-R57.json')
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
summaries={};states={};times={};solveTimes={}
for b in ('CAD','BIM'):
 text=(out/f'{b}-resultados-texto.txt').read_text(encoding='utf-8')
 full=(out/f'{b}-resultados-UI.txt').read_text(encoding='utf-8')
 reopened=(out/f'{b}-resultados-reaberto-UI.txt').read_text(encoding='utf-8')
 assert f'H03_{b}_R58_DIAGNOSTICO_PARCIAL_NAO_EXECUTAR' in full
 assert text in reopened and text in full
 assert 'Estrutura processada com avisos' in (out/f'{b}-processamento-concluido-UI.txt').read_text(encoding='utf-8')
 assert 'Detectou-se que ocorreu um erro' not in (out/f'{b}-reabertura-UI.txt').read_text(encoding='utf-8')
 def number(pattern):
  match=re.search(pattern,text);assert match,pattern
  return float(match.group(1))
 loads=dict(selfWeightTf=number(r'Peso próprio = ([\d.]+) tf'),additionalTf=number(r'Adicional = ([\d.]+) tf'),liveTf=number(r'Acidental = ([\d.]+) tf'),totalTf=number(r'Total = ([\d.]+) tf'),approxAreaM2=number(r'Área aproximada = ([\d.]+) m²'),ratioKgfM2=number(r'Relação = ([\d.]+) kgf/m²'))
 assert abs(loads['selfWeightTf']+loads['additionalTf']+loads['liveTf']-loads['totalTf'])<.021
 gammaPart=text.split('Verificação de estabilidade (Gama-Z): ')[1].split('Análise de 2ª ordem:')[0]
 gamma={d:float(v) for d,v in re.findall(r'([XY][+-]) = ([\d.]+)',gammaPart)}
 pd=text.split('Deslocamentos no topo da edificação: ')[1]
 pdelta=[dict(case=n.strip(),beforeCm=float(a),afterCm=float(z),variationPercent=float(p)) for n,a,z,p in re.findall(r'([^:]+): ([\d.]+) »» ([\d.]+) \(\+([\d.]+)%\)',pd)]
 assert len(gamma)==4 and len(pdelta)==9
 warnings=['Relação de carga por área não usual para edifícios','Os deslocamentos horizontais não foram verificados']
 assert all(w in text for w in warnings)
 options=read(out/f'{b}-opcoes-observadas.json')
 assert options['analysisStaticLinear'] and all(options[k] is False for k in ('elementDesign','redistributionLimits','frameDisplacements','slabDisplacements','dynamicFrame','dynamicSlabs'))
 summaries[b]=dict(loads=loads,gammaZ=gamma,pDelta=pdelta,warningsVisibleInSummary=warnings,summaryPreservedAfterNativeReopen=True,structuralAdequacyApproved=False)
 write(f'R58-resumo-{b}.json',summaries[b])
 native=Path(read(out/f'R58-preparacao-{b}.json')['nativeProject']);base=native.parent.parent;frozen=out/f'congelado-{b}';files=[]
 with zipfile.ZipFile(native) as z:assert z.testzip() is None
 for p in sorted(base.rglob('*')):
  if not p.is_file() or p.suffix.lower() in ('.bak','.tmp'):continue
  q=frozen/p.relative_to(base);q.parent.mkdir(exist_ok=True,parents=True)
  assert not q.exists(),q
  shutil.copy2(p,q);assert sha(q)==sha(p)
  files.append(dict(path=str(p),frozen=str(q),sha256=sha(q)))
 states[b]=dict(nativeProject=str(native),nativeSha256=sha(native),frozenFiles=files,nativeProjectClosedBeforeFreeze=True,zipIntegrityPassed=True,summaryReopenedWithoutReprocessing=True,engineeringLoadsEdited=False,sectionsEdited=False,newIFCExportPerformed=False)
 write(f'R58-estado-{b}.json',states[b]);times[b]=read(out/f'R58-tempo-{b}.json');solveTimes[b]=read(out/f'R58-tempo-processamento-{b}.json')
assert summaries['CAD']==summaries['BIM']
assert (out/'CAD-resultados-texto.txt').read_bytes()==(out/'BIM-resultados-texto.txt').read_bytes()
fmt=lambda ms:f'{int(ms//60000)} min {(ms%60000)/1000:.3f} s'
op=read(out/'R58-observacoes-operacao.json')
assert op['bothClosedNormallyBeforeFreeze'] and op['bothNativeProjectsSaved']
result=dict(revision='H03/R58',atUtc=datetime.now(timezone.utc).isoformat(),operation=op,summaries=summaries,summaryTextsEqualAtDisplayedPrecision=True,protectedR57FilesChecked=len(protected),times=times,observedProcessingTimes=solveTimes,partialLoadsOnly=True,structuralProcessingPerformed=True,elementDesignPerformed=False,elsDisplacementsVerified=False,realFoundationsDesigned=False,fullFlowRankingAllowed=False,perElementForcesCompared=False,postProcessingIFCGeometryAudited=False)
write('R58-resultado.json',result)
report=f'''# H03/R58 - processamento diagnostico parcial, NAO EXECUTAR

Em 29/10/2026, processaram-se copias independentes dos estados CAD e BIM R57 congelados no Eberick 2025 Infinity. Nenhuma carga nova ou secao foi editada. A monografia e os arquivos de origem RVT/DWG nao foram alterados. Os dois ramos conservam as cargas parciais e as pendencias de concepcao anteriores.

Selecionou-se apenas Analise estatica linear no dialogo: dimensionamento, limites de redistribuicao, deslocamentos ELS e dinamica desmarcados. O programa montou o modelo, calculou paineis de lajes e processou o portico; retornou Estrutura processada com avisos nos dois ramos. O resumo indica Processo P-Delta; portanto o nome do botao nao significa calculo exclusivamente de primeira ordem.

## Resumos observados na interface

| Grandeza nativa | CAD | BIM |
|---|---:|---:|
| Peso proprio (tf) | 75,69 | 75,69 |
| Adicional (tf) | 8,20 | 8,20 |
| Acidental (tf) | 17,11 | 17,11 |
| Total (tf) | 101,00 | 101,00 |
| Area aproximada (m2) | 132,81 | 132,81 |
| Relacao (kgf/m2) | 760,52 | 760,52 |
| Gama-Z X+ / X- | 1,09 / 1,08 | 1,09 / 1,08 |
| Gama-Z Y+ / Y- | 1,06 / 1,05 | 1,06 / 1,05 |

O texto completo dos resumos e identico na precisao exibida; as unidades foram transcritas sem presumir conversao fisica. A area aproximada do Eberick nao e automaticamente a area arquitetonica ou de faces IFC. Nao se compararam esforcos por elemento, reacoes por apoio, conectividade analitica integral ou resultados sem arredondamento. A igualdade dos resumos nao certifica equivalencia integral dos modelos ou atendimento normativo.

Constam os avisos Relacao de carga por area nao usual para edificios e Os deslocamentos horizontais nao foram verificados. Os valores 0,00 cm desse bloco nao sao flechas ELS verificadas. No P-Delta, vento X passou de 0,96 para 1,10 cm (+13,92%) e vento Y de 1,06 para 1,15 cm (+7,92%), nos dois sentidos e ramos. Sao valores do modelo parcial. Embora os Gama-Z mostrados sejam inferiores ao limite 1,10 exibido, nao se declarou estabilidade aprovada: cargas, vento, combinacoes, apoios e demais verificacoes continuam pendentes.

## Persistencia e ocorrencia operacional

Ambos foram salvos, fechados normalmente, reabertos e consultados pelo comando de resultados da analise (icone Estrutura > Analise). Nao se reprocessou para essa consulta: os resumos armazenados permaneceram identicos aos iniciais. Os projetos foram fechados normalmente antes de congelar o conjunto nativo, incluindo resultados e auxiliares. Os ZIPs PRJ passaram na verificacao de integridade; preservados os {len(protected)} arquivos protegidos R57. Nao houve nova exportacao IFC nesta R58; a auditoria geometrica IFC anterior e a R57, nao uma auditoria posterior ao processamento.

Na primeira abertura da copia CAD apareceu novamente o aviso de possivel inconsistencia da ultima edicao. Executou-se a verificacao nativa de integridade nessa copia antes do processamento. A reabertura apos salvar/fechar nao repetiu o aviso. O BIM abriu/reabriu sem esse aviso. A causa nao foi demonstrada; registrar como ocorrencia operacional, sem atribuir a perda de transferencia DWG. A confirmacao de fechamento antes do congelamento nao prova a causa dos avisos anteriores.

## Tempos prospectivos assistidos

| Ramo | Abrir, processar, ler resumo e salvar | Intervalo observado de processamento |
|---|---:|---:|
| CAD | {fmt(times['CAD']['durationMs'])} | {fmt(solveTimes['CAD']['durationMs'])} |
| BIM | {fmt(times['BIM']['durationMs'])} | {fmt(solveTimes['BIM']['durationMs'])} |

Incluem raciocinio, interacao da IA, latencia e leitura. CAD inclui verificacao de integridade; BIM veio em seguida, com procedimento conhecido. O intervalo do processamento termina na leitura da conclusao e inclui o tempo entre capturas; nao mede exclusivamente o solver. A conferencia posterior de fechamento/reabertura tem registro separado em R58-tempo-reabertura-QA.json. Nao se mediu tempo humano ativo ou inferencia isolada da IA; nao houve chamada direta a API OpenAI nesta rodada. Nao e ensaio controlado, nem ranking/economia percentual/tempo total dos fluxos.

## Continuidade

Permanecem paredes (incluindo W08/base da escada), telhado, reservatorio de 1.000 L e apoio/tara/base, escada, bordas/guarda-corpo, vento/combinacoes, sensibilidade dos apoios idealizados e verificacao completa de ligacoes. Vigas de cobertura 20x30 cm ainda sao alternativa sem dimensionamento/ELS. O usuario aceitou nesta sessao a hipotese de telha ondulada de fibrocimento 6 mm a 10% sobre estrutura metalica leve; o peso e as reacoes ainda precisam de memoria e aplicacao comum. Essa carga nao integra os resultados R58. A superestrutura permanece como escopo; nao se dimensionaram fundacoes reais. Completar acoes e verificar ELU/ELS antes de selecionar a concepcao, sincronizar origens e elaborar resultados finais.

Referencia operacional: [opcoes de analise AltoQi](https://suporte.altoqi.com.br/hc/pt-br/articles/360008798134) e [etapas/inconsistencias](https://suporte.altoqi.com.br/hc/pt-br/articles/115004281814). Os resultados desta rodada provem da interface nativa preservada, nao dessas paginas.
'''
(out/'LEIA-ME-R58.md').write_text(report,encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
write('R58-execucao-consolidador.json',dict(durationMs=(time.perf_counter()-start)*1000,scope='Somente execucao de consolidacao; exclui preparacao, operacao nativa e revisao'))
write('R58-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='R58-manifesto.json']))
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
intro=f'''# Atualizacao R58 - 29/10/2026

Bases limpas anteriores: R57 congelados. Copias processadas de DIAGNOSTICO PARCIAL em outputs/H03_CAD_R58_DIAGNOSTICO_PARCIAL_NAO_EXECUTAR e H03_BIM_R58_DIAGNOSTICO_PARCIAL_NAO_EXECUTAR. Ver outputs/Processamento-H03-R58-DIAGNOSTICO-PARCIAL-NAO-EXECUTAR/LEIA-ME-R58.md. Ambos: Estrutura processada com avisos, somente opcao Analise estatica linear com P-Delta configurado; sem dimensionamento, ELS ou dinamica. Resumos identicos na precisao exibida, inclusive apos salvar/fechar/reabrir sem reprocessar: 75,69 tf proprio, 8,20 tf adicional, 17,11 tf acidental, total 101,00 tf; area aproximada132,81m2; Gama-Z X+1,09/X-1,08/Y+1,06/Y-1,05. Nao constituem aprovacao estrutural ou equivalencia integral.

Tempos assistidos CAD {fmt(times['CAD']['durationMs'])}; BIM {fmt(times['BIM']['durationMs'])}; QA de persistencia separado, sem ranking. CAD repetiu aviso de integridade ao abrir copia: verificacao executada e reabertura sem aviso; causa nao comprovada. Todos os arquivos R57 protegidos. Ambos R58 fechados normalmente antes do congelamento. Eberick aberto sem projeto/dialogo, janela1416x766. Sem exportacao IFC pos-R58.

Proximo: memoria de cargas da cobertura: usuario aceitou fibrocimento ondulado6mm, inclinacao10%, estrutura metalica leve, pesos/reacoes como hipoteses documentadas. Nao aplicado na R58. Completar paredes/tanque/escada/bordas/vento e combinacoes, confirmar ligacoes/apoios, calcular ELU/ELS e depois sincronizar RVT/DWG. Apoios idealizados, sem fundacoes reais. Nao alterar monografia.

---
Historico anterior:

'''
assert not old.startswith('# Atualizacao R58')
guide.write_text(intro+old,encoding='utf-8')
print(json.dumps(dict(summaryEqual=True,protected=len(protected),frozenFiles={b:len(s['frozenFiles']) for b,s in states.items()},times={b:fmt(t['durationMs']) for b,t in times.items()})))

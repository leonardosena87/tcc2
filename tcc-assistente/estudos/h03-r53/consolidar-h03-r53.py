"""Congela R53, confronta dados, registra limites e preservacao dos antecedentes."""
from pathlib import Path
import json,hashlib,shutil,csv,zipfile
from datetime import datetime,timezone
root=Path('D:/TCC');out=root/'outputs/Cargas-H03-R53-PARCIAL-NAO-EXECUTAR'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
protected=read(out/'R53-protegidos-R52.json')
for row in protected:assert sha(Path(row['path']))==row['sha256'],row['path']
branches={}
for branch in ('CAD','BIM'):
    prep=read(out/f'R53-preparacao-{branch}.json');audit=read(out/f'R53-auditoria-{branch}.json')
    assert audit['all11RawLoadFieldsMatchPlannedPattern'] and audit['sameGeometryNamesGuidsAndTopAreas']
    native=Path(prep['nativeProject']);assert zipfile.ZipFile(native).testzip() is None
    nativeRoot=native.parent.parent;frozen=[]
    for row in prep['files']:
        a=Path(row['copy']);b=out/f'congelado-{branch}'/a.relative_to(nativeRoot)
        b.parent.mkdir(parents=True,exist_ok=True)
        if b.exists():assert sha(a)==sha(b),'Congelamento existente diverge; nao sobrescrever.'
        else:shutil.copy2(a,b)
        frozen.append(dict(path=str(a),frozen=str(b),sha256=sha(b)))
    assert sha(native)!=next(r['sha256'] for r in prep['files'] if r['copy']==str(native))
    branches[branch]=dict(nativeProject=str(native),nativeSha256=sha(native),frozenFiles=frozen,
        uniformLoadsAssignedSlabs=11,saveCloseReopenPerformed=True,nativeUISamplesAfterReopen=['L4/N1','L6/N1','L4/N2'],
        all11ExportedRawLoadsChecked=True,individualNativeUIAll11ReadAfterReopen=False,
        materialSettingsInheritedR51=True,balconyLinkHypothesisInheritedR52=True,
        fullLoadsComplete=False,analyticalLinksVerified=False,calculationPerformed=False)
    write(out/f'R53-estado-{branch}.json',branches[branch])
audits={b:read(out/f'R53-auditoria-{b}.json') for b in branches}
def spatial(a):return sorted((r['level'],r['name'],tuple(round(v,5) for v in r['min']+r['max']),round(r['topAreaM2'],5),tuple(sorted(r['rawLoads'].items()))) for r in a['slabs'])
assert spatial(audits['CAD'])==spatial(audits['BIM'])
matrix=read(out/'R53-matriz-planejada.json');pending=matrix['pending']
times={b:read(out/f'R53-tempo-{b}.json') for b in branches}
fmt=lambda ms:f'{int(ms//60000)} min {(ms%60000)/1000:.3f} s'
summary=dict(revision='H03/R53',atUtc=datetime.now(timezone.utc).isoformat(),branches=branches,
    sameSlabGeometryAndExportedLoadsAcrossBranches=True,geometryPreservedRelativeToOwnR52Both=True,
    protectedR52FilesChecked=len(protected),pending=pending,completeLoads=False,calculationPerformed=False,
    correctionClassification='Complementacao comum de acoes no Eberick receptor; nao erro comprovado de transferencia CAD/BIM.',
    times={b:dict(**times[b],formatted=fmt(times[b]['durationMs'])) for b in times},wholeFlowRankingAllowed=False)
write(out/'R53-comparacao.json',summary)
with (out/'R53-cargas-lajes.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f,delimiter=';');w.writerow(['fluxo','nivel','laje','Q_UI_planejado_kNm2','G2_UI_parcial_planejado_kNm2','Q_IFC_bruto_sem_unidade_explicita','G2_IFC_bruto_sem_unidade_explicita','area_superior_IFC_m2','leitura_UI_apos_reabrir'])
    for branch,audit in audits.items():
        for r in sorted(audit['slabs'],key=lambda r:(r['level'],r['name'])):
            w.writerow([branch,r['level'],r['name'],r['expectedNativeUI']['Q_kNm2'],r['expectedNativeUI']['G2partial_kNm2'],r['rawLoads']['Acidental (Q)'],r['rawLoads']['Revestimento (G2)'],r['topAreaM2'],'Sim, amostra' if f"{r['name']}/{r['level']}" in audit['nativeUIReadAfterReopenSamples'] else 'Nao; conferido pelo campo exportado'])
report=f'''# H03/R53 — cargas uniformes parciais nos dois fluxos

Revisao de 29/10/2026. Arquivos em D:\\TCC. Modelo academico preliminar, nao dimensionado, nao executar.

Aplicaram-se separadamente, no Eberick 2025 Infinity, as mesmas parcelas uniformes nas 11 lajes de cada ramo. Cada copia deriva do seu proprio estado R52 congelado, sem transplantar o PRJ de um fluxo ao outro. A monografia, RVT e DWG de origem nao foram alterados nesta etapa.

| Nivel e lajes nativas | Uso/hipotese | Q (kN/m2) | G2 parcial (kN/m2) |
|---|---|---:|---:|
| N1 L1 a L4 | Residencial | 1,5 | 1,00 |
| N1 L5 | Faixa junto a escada, hipotese provisoria de uso restrito | 2,5 | 1,00 |
| N1 L6 | Varanda residencial | 2,5 | 1,00 |
| N2 L1 a L5 | Cobertura de concreto, acesso apenas para manutencao | 1,0 | 0,25 |

Q fundamenta-se na Tabela 10 da ABNT NBR 6120:2019, exemplar local: PDF 24 (varanda), 25 (cobertura), 26 (residencial), 27 (escada). G2 do N1 e hipotese de pacote de piso de 5 cm a 20 kN/m3, parcial e revisavel; nao inclui automaticamente forro de pavimentos inferiores, paredes ou impermeabilizacao. G2 do N2 inclui somente a parcela de forro acartonado, cuja hipotese de sistema foi autorizada pelo usuario; o telhado e demais camadas nao estao incluidos. L5 nao substitui a modelagem da escada e suas reacoes. A varanda ainda exige guarda-corpo, carga de borda e camadas finais. O peso proprio de referencia da laje de 14 cm e 3,50 kN/m2; nao foi duplicado no campo de revestimento. A geracao do peso proprio e seus resultados ainda devem ser verificados no processamento.

Usou-se Lancamento > Outros > Copiar dados, marcando apenas Grupo de Carga (Nenhum), que leva as parcelas Q e G2. Geometria, elevacao, grelha, cargas extras e efeitos termicos permaneceram desmarcados. Aplicou-se a cada pavimento isolado; depois ajustaram-se L5 e L6 de N1 para 2,5. No CAD, a escolha da entidade em algumas anotacoes exigiu selecionar Laje em vez de Texto. Trata-se de esforco de interface observado, sem atribui-lo como defeito de intercambio.

## Verificacao real realizada

Ambos os PRJs foram salvos, fechados e reabertos. Leram-se apos reabrir as amostras L4/N1, L6/N1 e L4/N2 em cada ramo, com registros de acessibilidade TXT e observacao dos dialogos. Nao se afirma leitura nativa individual de todas as 11 apos reabrir. Exportou-se IFC4 de cada projeto reaberto para pastas exclusivas desta revisao. Os campos brutos Q e G2 das 11 lajes coincidiram com o padrao planejado nos dois arquivos. A razao empirica entre UI e esses campos e 100; o Pset nao informa unidade explicita. Isso nao autoriza conversao geral de outros campos IFC.

Cada exportacao contem 22 IfcColumn, 32 IfcBeam (29 vigas logicas) e 11 IfcSlab. Em relacao a propria R52, preservaram-se classes, nomes, GUIDs, caixas envolventes e areas superiores, com tolerancia computacional de 0,00001 m nos comprimentos. O confronto entre ramos tambem coincide para geometria das lajes e campos de carga. Nao se verificou identidade de malha completa nem ligacao analitica por esse controle. A integridade ZIP dos PRJs passou. Conferiram-se os hashes de {len(protected)} arquivos protegidos do manifesto R52; os estados nativos R53 foram congelados em separado.

## Tempos prospectivos desta etapa

| Ramo | Intervalo assistido de aplicacao, salvar/reabrir e amostragem |
|---|---:|
| CAD | {fmt(times['CAD']['durationMs'])} |
| BIM | {fmt(times['BIM']['durationMs'])} |

Os arquivos R53-tempo-CAD/BIM.json guardam inicio/fim UTC e duracao por relogio monotonico. Incluem raciocinio, latencia e operacao de interface. CAD incluiu descoberta e exploracao da copia de dados e ambiguidades Texto/Laje; BIM utilizou procedimento ja conhecido. Portanto, ha efeito de aprendizagem e nao houve repeticao controlada, mensuracao de tempo humano ativo ou isolamento de inferencia da IA. Nao calcular superioridade percentual nem ranking de fluxos completos a partir desses intervalos. Exportacao e execucao do auditor possuem registros adicionais, com escopos distintos explicitados e sem soma indiscriminada.

## Pendencias para calculo

'''+ '\n'.join(f'- {p}.' for p in pending)+'''

Mantem-se o recorte da superestrutura sem sondagem, com apoios idealizados ainda a conferir. Nao houve processamento estrutural, dimensionamento, comprovacao de estabilidade, ELU/ELS ou liberacao de execucao. Esta revisao e complementacao comum de acoes no receptor, nao contagem de falhas comprovadas da transferencia. Os proximos ajustes devem partir de novas copias, preservando R53.

Referencia operacional consultada: https://suporte.altoqi.com.br/hc/pt-br/articles/115003144013 (cargas tipicas e copia de dados). Nao se adotou um grupo padrao de uso sem verificar os valores.
'''
(out/'LEIA-ME-R53.md').write_text(report,encoding='utf-8')
for name in ('preparar-h03-r53.py','auditar-h03-r53.py','consolidar-h03-r53.py'):
    shutil.copy2(root/'work'/name,out/name)
write(out/'R53-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='R53-manifesto.json']))
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md'
old=guide.read_text(encoding='utf-8-sig')
intro=f'''# Atualizacao R53 — 29/10/2026

Os estados atuais sao H03_CAD_R53_CARGAS_PARCIAIS_NAO_EXECUTAR e H03_BIM_R53_CARGAS_PARCIAIS_NAO_EXECUTAR em D:/TCC/outputs. Consultar outputs/Cargas-H03-R53-PARCIAL-NAO-EXECUTAR/LEIA-ME-R53.md e R53-comparacao.json. Aplicaram-se parcelas Q/G2 nas 11 lajes de cada ramo, salvaram-se/reabriram-se ambos, leram-se 3 amostras nativas em cada ramo e auditaram-se as 11 lajes exportadas em IFC4. Geometria/nomes/GUIDs/areas superiores preservados em relacao a propria R52. Cargas permanecem parciais. Sem calculo ou verificacao analitica dos vinculos. Tempo assistido CAD {fmt(times['CAD']['durationMs'])}; BIM {fmt(times['BIM']['durationMs'])}, sem ranking por efeito de aprendizagem/latencia. Proximo passo: cargas de paredes/telhado/tanque/escada, bordas, vento/combinacoes e apoios idealizados N0. Nao tratar pendencias como zero. Nao alterar monografia.

O Eberick foi deixado no CAD R53 apos exportacao; a unica alteracao nao salva e metadado de destino da exportacao. O PRJ de engenharia foi salvo/reaberto antes dela e congelado. Ao trocar de arquivo, descartar apenas esse metadado se continuar sem outras edicoes.

---
Historico anterior:

'''
if not old.startswith('# Atualizacao R53'):guide.write_text(intro+old,encoding='utf-8')
print(json.dumps(dict(protectedFiles=len(protected),times={b:fmt(times[b]['durationMs']) for b in times},comparison=True)))

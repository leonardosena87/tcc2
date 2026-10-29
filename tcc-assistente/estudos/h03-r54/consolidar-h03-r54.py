"""Consolida atribuicao de apoios por lote e releitura amostral, sem atestar calculo."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,zipfile
root=Path('D:/TCC');out=root/'outputs/Apoios-H03-R54-NAO-EXECUTAR'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
protected=read(out/'R54-protegidos-R53.json')
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
mapping=[dict(x=0,y=0,CAD='P1',BIM='P8'),dict(x=9.65,y=7.05,CAD='P9',BIM='P3'),dict(x=6.55,y=3.9,CAD='P11',BIM='P6')]
branches={}
for branch in ('CAD','BIM'):
    prep=read(out/f'R54-preparacao-{branch}.json');native=Path(prep['nativeProject']);nr=native.parent.parent
    assert '(11 sel.)' in (out/f'{branch}-selecao-UI.txt').read_text(encoding='utf-8')
    text=(out/f'{branch}-parametros-conversao-UI.txt').read_text(encoding='utf-8')
    for token in ('Apoio Value: Rotulado','Altura barra Value: Fixo','Value: 10 ID: 803','Profundidade (df) Value: 0'):assert token in text,(branch,token)
    samples=[]
    for row in mapping:
        name=row[branch];p=out/f'{branch}-{name}-N0-reaberto-UI.txt';text=p.read_text(encoding='utf-8')
        for token in (f'Nome Value: {name} ID: 801','Altura barra Value: Fixo','Value: 10 ID: 803','Vínculo pilar Value: Engastado','Vínculo apoio Value: Rotulado','b Value: 20 ID: 810','h Value: 30 ID: 811','Elevação Value: 0','Profundidade (df) Value: 0'):assert token in text,(p,token)
        samples.append(dict(nativeName=name,referencePositionM=[row['x'],row['y']],barHeightCm=10,barHeightMode='Fixo',support='Rotulado',pillarLink='Engastado',bCm=20,hCm=30,rotationDeg=90 if row['x']==6.55 else 0,depthDfCm=0,elevationCm=0,readAfterReopen=True,evidence=str(p),evidenceSha256=sha(p)))
    assert zipfile.ZipFile(native).testzip() is None
    frozen=[]
    for row in prep['files']:
        a=Path(row['copy']);b=out/f'congelado-{branch}'/a.relative_to(nr);b.parent.mkdir(parents=True,exist_ok=True)
        if b.exists():assert sha(a)==sha(b),'Nao sobrescrever congelamento divergente'
        else:shutil.copy2(a,b)
        frozen.append(dict(path=str(a),frozen=str(b),sha256=sha(b)))
    branches[branch]=dict(nativeProject=str(native),nativeSha256=sha(native),frozenFiles=frozen,assignedInOneBatch=11,readAfterReopenSamples=samples,all11IndividuallyReadAfterReopen=False,saveCloseReopenPerformed=True,studyHypothesis=prep['studyHypothesis'],structuralAnalysisPerformed=False,fullLoadSetComplete=False,newIFCExportPerformed=False,postRevisionSuperstructureGeometryAuditPending=True)
    write(out/f'R54-estado-{branch}.json',branches[branch])
times={b:read(out/f'R54-tempo-{b}.json') for b in branches}
fmt=lambda ms:f'{int(ms//60000)} min {(ms%60000)/1000:.3f} s'
result=dict(revision='H03/R54',atUtc=datetime.now(timezone.utc).isoformat(),branches=branches,sampleCoordinateMapping=mapping,protectedR53FilesChecked=len(protected),timeByBranch={b:dict(**v,formatted=fmt(v['durationMs'])) for b,v in times.items()},wholeFlowRankingAllowed=False,realFoundationsDesigned=False,analyticalBaseCoordinatesVerified=False,auxiliaryBarSensitivityVerified=False,materialOrLoadsIntentionallyChanged=False,postRevisionIFCGeometryAuditPending=True)
write(out/'R54-comparacao.json',result)
report=f'''# H03/R54 — apoios idealizados da superestrutura

Revisao academica de 29/10/2026, nao dimensionada, nao executar. Partiu-se de copias independentes dos estados congelados R53 em D:\\TCC, preservando os dois fluxos e os {len(protected)} hashes protegidos do manifesto anterior.

No Eberick 2025 Infinity, selecionaram-se os 11 pilares nascendo em N0 de cada ramo. Aplicou-se Lancamento > Pilares > Converter em pilares de fundacao, com cadastro auxiliar Sapata, apoio Rotulado, altura da barra Fixo 10 cm e profundidade df=0. Esse cadastro permite representar o apoio; nao define nem dimensiona uma sapata real. Nao se adotaram capacidade de suporte, sondagem, recalques ou interacao solo-estrutura.

Ambos os arquivos foram salvos, fechados e reabertos. Foram lidos individualmente tres apoios geometricamente equivalentes em cada ramo:

| Coordenadas de referencia X,Y (m) | CAD | BIM |
|---|---|---|
| 0; 0 | P1 | P8 |
| 9,65; 7,05 | P9 | P3 |
| 6,55; 3,90 | P11 | P6 |

As seis amostras mostraram barra fixa 10 cm, apoio Rotulado, vinculo do pilar Engastado, secao nativa 20 x 30 cm, elevacao zero e df zero. No novo pilar, a rotacao de 90 graus preserva a orientacao 30 cm em X e 20 cm em Y da proposta. Ha um TXT de acessibilidade por leitura e por selecao/parametrizacao. A atribuicao de 11 por ramo foi confirmada pela selecao do lote e pela sequencia da interface; nao se afirma releitura individual dos outros oito de cada ramo. A integridade ZIP dos dois PRJs passou e seus arquivos foram congelados.

O apoio rotulado libera rotacoes e restringe translacoes segundo a definicao do programa. A barra auxiliar de 10 cm faz parte da representacao numerica, portanto nao equivale exatamente a um apoio nodal em N0. Para N0=+0,20 m, a base em +0,10 m e uma inferencia ainda nao conferida no modelo analitico. A sensibilidade ao comprimento da barra e ao vinculo segue pendente, sem garantia de conservadorismo. Excluir cadastros auxiliares e barras abaixo de N0 dos quantitativos comparados da superestrutura.

## Tempos da etapa assistida

| Ramo | Abrir, parametrizar lote, salvar/reabrir e ler 3 amostras |
|---|---:|
| CAD | {fmt(times['CAD']['durationMs'])} |
| BIM | {fmt(times['BIM']['durationMs'])} |

Registro prospectivo UTC e relogio monotonico em JSON. Inclui raciocinio e latencia da interface. CAD inclui localizacao/exploracao de comandos; BIM aproveita procedimento conhecido. Nao mede tempo humano ativo nem inferencia isolada de IA, nao e repeticao controlada e nao permite ranking dos fluxos completos. Complementacao comum de parametrizacao no receptor, nao falha comprovada de transferencia.

Nao se processou calculo, estabilidade ou ELU/ELS. Nao se executou verificacao automatica de lancamento nem nova exportacao IFC nesta revisao; a auditoria pos-conversao da geometria/cargas da superestrutura continua pendente. Nao atribuir a R54 a auditoria IFC realizada na R53. A monografia, RVT e DWG de origem permaneceram inalterados.

Proximo passo: auditoria pos-conversao, releitura complementar dos apoios quando necessaria e cargas de paredes/telhado/tanque/escada/bordas, vento e combinacoes. Manter entradas incompletas como pendencias.

Fontes oficiais consultadas: [vinculo de apoio](https://suporte.altoqi.com.br/hc/pt-br/articles/360012152833), [barra da fundacao](https://suporte.altoqi.com.br/hc/pt-br/articles/115002375753) e [conversao no programa](https://suporte.altoqi.com.br/hc/pt-br/articles/360022925613).
'''
(out/'LEIA-ME-R54.md').write_text(report,encoding='utf-8')
for name in ('preparar-h03-r54.py','consolidar-h03-r54.py'):shutil.copy2(root/'work'/name,out/name)
write(out/'R54-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='R54-manifesto.json']))
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
if not old.startswith('# Atualizacao R54'):
    guide.write_text('''# Atualizacao R54 — 29/10/2026

Estados atuais: outputs/H03_CAD_R54_APOIOS_NAO_EXECUTAR e H03_BIM_R54_APOIOS_NAO_EXECUTAR. Consultar outputs/Apoios-H03-R54-NAO-EXECUTAR/LEIA-ME-R54.md e R54-comparacao.json. Atribuiram-se 11 apoios auxiliares por ramo: Rotulado, barra fixa 10 cm, df=0, cadastro Sapata auxiliar, sem dimensionar fundacao real. Salvar/fechar/reabrir e 3 amostras por ramo confirmadas (CAD P1/P9/P11; BIM P8/P3/P6). Outros oito nao relidos individualmente. Nao houve nova exportacao IFC, verificacao automatica de lancamento ou calculo; auditoria pos-conversao da superestrutura pendente. Cargas R53 herdadas, ainda incompletas. Proximos passos: auditoria da superestrutura e cargas de paredes, telhado, tanque, escada, bordas, vento/combinacoes. Eberick no BIM R54 reaberto, sem edicoes de engenharia posteriores. Nao alterar monografia.

---
Historico anterior:

'''+old,encoding='utf-8')
print(json.dumps(dict(times={b:fmt(v['durationMs']) for b,v in times.items()},samples=6,protected=len(protected))))

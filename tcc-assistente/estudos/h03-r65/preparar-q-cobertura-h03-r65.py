"""Mapa calculado de Q do telhado; nao altera nem processa arquivos nativos."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from time import perf_counter
import hashlib,json,shutil,ast
started=datetime.now(timezone.utc).isoformat();tick=perf_counter()
root=Path('D:/TCC')
out=root/'outputs/Cobertura-H03-R65-PLANO-Q-NAO-APLICADO'
repo=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r65')
assert not out.exists() and not repo.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
src=root/'outputs/Cobertura-H03-R60-REACOES-PARCIAIS-NAO-EXECUTAR/R60-arranjo-reacoes.json'
r=read(src)
prior=root/'outputs/Cargas-H03-R64-CONFERENCIA-INDIVIDUAL-NAO-EXECUTAR'
protected=read(prior/'R64-manifesto.json')['files']
for f in protected: assert sha(Path(f['path']))==f['sha256'],f['path']
norm=root/'materiais/normas/ABNT NBR 6120-2019.pdf'
q=Decimal('0.25');rows=[]
for n in r['reactionNodes']:
    d=Decimal(str(round(n['qRoofDownKN'],9)))
    rows.append(dict(id=n['id'],xCm=round(n['xM']*100,5),yCm=round(n['yM']*100,5),proposedFzKN=-float(d),proposedInputFzKN=-float(d.quantize(Decimal('.000001'),rounding=ROUND_HALF_UP)),sources=n['sourceRafters'],nativeTargets=n['nativeTargets'],nativeApplied=False))
total=sum(-v['proposedFzKN'] for v in rows)
mx=sum(-v['proposedFzKN']*v['xCm']/100 for v in rows)
my=sum(-v['proposedFzKN']*v['yCm']/100 for v in rows)
integral=[0.,0.,0.]
for p in r['planes'][:2]:
    x0,y0,x1,y1=p['box'];force=float(q)*(x1-x0)*(y1-y0)
    integral[0]+=force;integral[1]+=force*(x0+x1)/2;integral[2]+=force*(y0+y1)/2
assert len(rows)==13
assert all(abs(a-b)<1e-9 for a,b in zip((total,mx,my),integral))
rounded=sum(-v['proposedInputFzKN'] for v in rows)
assert abs(rounded-total)<.00001
out.mkdir()
def write(n,v):(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write('R65-protegidos-R64.json',protected)
result=dict(revision='H03/R65',status='Plano Q calculado; NAO aplicado no Eberick',sourceMap=dict(path=str(src),sha256=sha(src)),normativeExemplar=dict(path=str(norm),sha256=sha(norm),edition='NBR 6120:2019 versao corrigida do exemplar local',consultedPdfPages=[25,35,36],consultedPrintedPages=[19,29,30],currentCatalogStatusVerified=False),roofSlopeHypothesisPercent=10,qHorizontalKNm2=float(q),areaNominalAxesM2=r['partialProjectedAreaM2'],nodes=rows,equilibrium=dict(downKN=total,firstMomentXKNm=mx,firstMomentYKNm=my,distributedIntegral=integral,passed=True),inputRounding=dict(method='6 decimais ROUND_HALF_UP',sumDownKN=rounded,deltaKN=rounded-total,notInternalNativePrecisionClaim=True),existingN2SlabQKNm2=1.0,existingN2SlabG2ForroKNm2=.25,existingSlabLoadsChanged=False,roofQEqualsSlabQ=False,automaticSimultaneityAssumed=False,proposedDedicatedActionName='Q_TELHADO_MANUTENCAO',nativeActionCreated=False,loadCombinationFactorsChosen=False,nativeModelsEdited=False,structuralDesignApproved=False,isolatedMemberCheck1KNRequiredNotPerformed=True,excludedRoofPlanes=['P1','P2'],operationalSources=[dict(url='https://suporte.altoqi.com.br/hc/pt-br/articles/115001646393',scope='Criacao de acoes personalizadas e fatores; nao evidencia de norma vigente'),dict(url='https://suporte.altoqi.com.br/hc/pt-br/articles/360000624993',scope='Ativacao, combinacoes e acidental isolada; nao configuracao efetivamente verificada neste plano')])
write('R65-plano-Q.json',result)
table='\n'.join(f'| {n["id"]} | {n["xCm"]:g} | {n["yCm"]:g} | {n["proposedFzKN"]:.7f} | {n["proposedInputFzKN"]:.6f} |' for n in rows)
(out/'LEIA-ME-R65.md').write_text(f'''# H03/R65 — plano da carga variável do telhado

PLANO CALCULADO, NÃO APLICADO NO EBERICK. NÃO EXECUTAR. O último estado nativo conferido permanece R64. Nenhuma ação ou combinação foi criada, nenhuma carga nativa foi modificada e nenhum novo processamento foi realizado nesta etapa.

## Parcela calculada

Retomou-se o arranjo hipotético R60 de oito barras metálicas biapoiadas, com reações verticais de extremidade e ausência idealizada de empuxo horizontal. Mantiveram-se os trechos nominais A1/A2, 55,9425 m² em projeção horizontal, e a hipótese de inclinação de 10%. O exemplar local NBR 6120:2019, subseção6.4/páginas impressas29–30, fundamenta a parcela distribuída de manutenção de 0,25 kN/m² para esse recorte. A consulta não confirma por si só a vigência de catálogo nem aprova o arranjo metálico. A tabela10/página19 trata separadamente a laje de cobertura de concreto, para a qual a R53 já lançou Q=1,0 kN/m². Não se substituiu esse Q por 0,25 nem se declarou que ambos representam a mesma carga.

| Ponto | X (cm) | Y (cm) | Fz calculado (kN) | Entrada proposta (kN) |
|---|---:|---:|---:|---:|
{table}

A soma calculada é {total:.6f} kN descendente, igual a 0,25 vezes55,9425 m². Verificaram-se também os primeiros momentos, confrontando as reações com as integrais dos dois retângulos: soma(Fx_coordenada)={mx:.9f} kN.m e soma(Fy_coordenada)={my:.9f} kN.m, em que Fx/Fy_coordenada significam força vertical multiplicada pela coordenada, não componentes horizontais de força. No JSON usam-se nomes firstMomentX/firstMomentY para identificar essas somas. O equilíbrio dos três escalares passou com tolerância1e-9. O arredondamento proposto a seis decimais, HALF_UP, soma {rounded:.6f} kN e produz diferença de {rounded-total:.9f} kN; não é medição da precisão interna do Eberick.

## Ações e prevenção de duplicação

Propõe-se ação identificável Q_TELHADO_MANUTENCAO para manter rastreabilidade da manutenção do telhado, distinta da Q da laje. Não se escolheu fator de ponderação/combinação nem simultaneidade neste plano. A ausência de uma decisão justificada sobre correlação entre as manutenções não autoriza marcar ações como mutuamente excludentes ou somá-las integralmente por conveniência. Antes de aplicar, deve-se conferir no Eberick a classificação, os grupos, fatores e combinações efetivas dos dois ramos e documentar a decisão com a base normativa adotada. O forro acartonado G2=0,25 kN/m² da R53 é carga permanente: igualdade numérica com Q do telhado não torna as parcelas intercambiáveis.

O item6.4 também exige verificação específica de elemento isolado com força concentrada de1kN na posição desfavorável, além das permanentes e isolada das demais variáveis. Essa verificação local NÃO foi substituída pelas 13 reações distribuídas, NÃO foi aplicada como1kN em todos os nós e permanece pendente com o dimensionamento metálico. A inclinação nominal não substitui projeto de drenagem, rigidez, sucção e ancoragens.

## Procedimento seguinte no receptor

Criar cópias independentes dos congelados R64, verificar as ações e combinações atuais, estabelecer a classificação de Q do telhado e aplicar apenas a parcela aprovada em cada nó existente, preservando G. Conferir coordenadas e ação antes da digitação; salvar/fechar/reabrir e reler cada ponto. Reprocessar e confrontar resumos somente após fechar o escopo de cargas. Registrar os mesmos limites de etapa nos dois ramos e separar esforço de instrumentação, transferência, correção e conferência. A preparação deste mapa não conta como transferência ou resultado de aplicação nativa.

P1/varanda, P2/abrigo e sua altimetria, tanque1000L/tara/base, paredes/aberturas, escada, vento/combinações e ELU/ELS continuam pendentes. Este plano não acrescenta carga de P1/P2 à área A1/A2 nem aprova fundações ou segurança estrutural.

## Fontes e preservação

Exemplar normativo local identificado por hash no JSON; páginas PDF25/35/36 visualmente consultadas. A busca aberta não recuperou confirmação direta do estado atual no catálogo ABNT, portanto não se afirmou vigência confirmada. Documentação operacional oficial consultada: [criar ações](https://suporte.altoqi.com.br/hc/pt-br/articles/115001646393) e [configurações de ações](https://suporte.altoqi.com.br/hc/pt-br/articles/360000624993); seus exemplos normativos não substituem a edição adotada no TCC. Verificaram-se {len(protected)} arquivos do manifesto R64 por hash. PDF normativo e imagens de suas páginas permanecem locais e não são copiados para o repositório público. Nenhuma monografia ou origem RVT/DWG foi editada.
''',encoding='utf-8')
ast.parse(Path(__file__).read_text(encoding='utf-8'))
shutil.copy2(Path(__file__),out/Path(__file__).name)
write('R65-validacao.json',dict(equilibriumPassed=True,nodeCount=13,protectedR64Files=len(protected),scriptSyntaxPassed=True,nativeApplicationPerformed=False,atStartUtc=started,atEndUtc=datetime.now(timezone.utc).isoformat(),scriptElapsedSeconds=perf_counter()-tick,scriptTimingIsAIEffortOrFlowTime=False))
write('R65-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file()]))
repo.mkdir()
for p in out.iterdir():
    shutil.copy2(p,repo/p.name);assert sha(p)==sha(repo/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md'
old=guide.read_text(encoding='utf-8-sig')
guide.write_text('''# Atualizacao R65 — plano Q, ainda NAO aplicado

Ultimo nativo: R64, 13 cargas G conferidas em cada ramo. R65 apenas calcula mapa Q telhado A1/A2=13,985625kN em 13 pontos, verifica equilibrio vertical/primeiros momentos e documenta a necessidade de acao identificavel e combinacoes justificadas em relacao a Q=1kN/m2 da laje. Nao alterou cargas, acoes ou combinacoes no Eberick. Nao substitui verificacao local1kN de elemento isolado. Ler outputs/Cobertura-H03-R65-PLANO-Q-NAO-APLICADO/LEIA-ME-R65.md e R65-plano-Q.json antes de aplicar. NAO EXECUTAR.

PROXIMO: novas copias R64; inspecionar acoes/grupos/fatores/combinacoes nativos, justificar simultaneidade e so entao aplicar Q dedicada, salvar/reabrir/ler. Nenhuma monografia editada.

---
Historico anterior:

'''+old,encoding='utf-8')
print(json.dumps(dict(status=result['status'],nodes=len(rows),totalKN=total,firstMoments=[mx,my],roundedSumKN=rounded,protected=len(protected)),ensure_ascii=False))

"""Memoria unitaria da cobertura: dados normativos separados de hipoteses e reacoes."""
from pathlib import Path
from datetime import datetime,timezone
import math,json,hashlib,shutil,time
start=time.perf_counter();root=Path('D:/TCC');out=root/'outputs/Cobertura-H03-R59-MEMORIA-ESTUDO-NAO-EXECUTAR';out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(n,v):(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
src=root/'outputs/Processamento-H03-R58-DIAGNOSTICO-PARCIAL-NAO-EXECUTAR'
protected=read(src/'R58-manifesto.json')['files']
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
write('R59-protegidos-R58.json',protected)
inclination=.10;factor=math.sqrt(1+inclination**2);sheet=.18;steel=.15;maintenance=.25
g=sheet*factor+steel
assert abs(factor-1.004987562112089)<1e-12
sourceNorm=root/'materiais/normas/ABNT NBR 6120-2019.pdf';architecture=root/'PROJETO ARQUITETONICO-A0.pdf'
cases=[dict(steelAllowanceKNm2=s,sheetHorizontalKNm2=sheet*factor,totalRoofPermanentKNm2=sheet*factor+s) for s in (.10,.15,.20)]
# Exemplo aritmetico parametrico: nao e levantamento de uma terca/tesoura da edificação.
b=1.5;span=3.9;lineG=g*b;lineQ=maintenance*b
reaction=dict(meaning='Exemplo de barra simplesmente apoiada, sob carregamento uniforme; nao reacao extraida da arquitetura ou Eberick',tributaryWidthM=b,spanM=span,linePermanentKNm=lineG,lineVariableKNm=lineQ,leftPermanentKN=lineG*span/2,rightPermanentKN=lineG*span/2,leftVariableKN=lineQ*span/2,rightVariableKN=lineQ*span/2,windIncluded=False,stiffnessRedistributionIncluded=False,actualNativeElement=None)
assert abs(reaction['leftPermanentKN']+reaction['rightPermanentKN']-lineG*span)<1e-12
assert abs(reaction['leftVariableKN']+reaction['rightVariableKN']-lineQ*span)<1e-12
data=dict(revision='H03/R59',atUtc=datetime.now(timezone.utc).isoformat(),scope='Memoria unitaria de cargas, sem edicao de modelos',userAccepted=dict(sheet='Fibrocimento ondulado 6 mm',roofSlopePercent=10,supportSystem='Estrutura metalica leve',weightsAndReactionsMayBeStudyHypotheses=True),
 sources=dict(architecture=dict(path=str(architecture),sha256=sha(architecture),observed='Planta com tres anotacoes fibrocimento a 10%; cobertura de policarbonato a 5% separada; corte BB com reservatorio 1000 L e ressalto local de 0,60 m'),norm=dict(path=str(sourceNorm),sha256=sha(sourceNorm),editionRead='ABNT NBR 6120:2019, exemplar local',catalogCurrentEditionIndependentlyConfirmed=False,table5=dict(pdfPage=19,printedPage=13,sheetPermanentInclinedKNm2=sheet,inclusions=['sobreposicao','fixacao','absorcao de agua']),section64=dict(pdfPage=35,printedPage=29,roofMaintenanceHorizontalKNm2=maintenance,meaning='Cobertura acessivel apenas para manutencao, i=10%; nao substituir automaticamente a sobrecarga da laje')),manufacturer=dict(url='https://www.brasilit.com.br/sites/brasilit.com.br/files/produto/arquivos/Guia%20T%C3%A9cnico%20Brasilit%202026.pdf',pdfPage=37,printedPage=37,referenceMassPerAreaKgM2=18,meaning='Referencia comercial corroborativa; nao somada a carga normativa nem especificacao obrigatoria de compra')),
 loads=dict(slopeRadians=math.atan(inclination),slopeDegrees=math.degrees(math.atan(inclination)),inclinedAreaPerHorizontalArea=factor,sheetInclinedKNm2=sheet,sheetHorizontalKNm2=sheet*factor,steelHorizontalAllowanceKNm2=steel,steelAllowanceIsHypothesis=True,steelMembersQuantified=False,roofPermanentHorizontalKNm2=g,roofMaintenanceHorizontalKNm2=maintenance,existingSlabForroG2KNm2=.25,existingSlabLiveQKNm2=1.0,roofPermanentAppliedToSlabG2=False,roofMaintenanceAddedToSlabQ=False),
 sensitivity=cases,parametricReactionExample=reaction,actualRoofAreaM2=None,actualRoofTotalPermanentKN=None,actualRoofSupportReactions=None,loadPathDefined=False,nativeModelsEdited=False,monographEdited=False,
 pending=['Mapear as tres aguas, recortes, bordas, calhas e eventual area do abrigo do reservatorio em coordenadas H03.','Definir terças/tesouras, comprimentos tributarios e pontos/linhas reais de apoio na estrutura de concreto.','Quantificar os perfis, ligacoes e contraventamentos para substituir a reserva de peso.','Avaliar apoios locais, vento/succao e combinacoes; nao distribuir pontualmente ou sobre lajes por conveniencia.','Manter sobrecarga da laje distinta da cobertura e decidir simultaneidade; nao somar nem substituir automaticamente.','Detalhar reservatorio, base, tara, cota e paredes do abrigo; nao incluir no peso unitario das telhas.','Consultar catalogo ABNT antes de fechar a versao normativa do trabalho e a verificacao final.'])
write('R59-memoria-cobertura.json',data)
report=f'''# H03/R59 - memoria unitaria de cargas da cobertura - ESTUDO, NAO EXECUTAR

O usuario aceitou telha ondulada de fibrocimento de 6 mm a 10% sobre estrutura metalica leve, com pesos e reacoes documentados como hipoteses. A arquitetura registra fibrocimento a 10% e uma cobertura de policarbonato a 5% separada; o corte BB representa o reservatorio de 1.000 L e ressalto local de 0,60 m. Nao se estendeu a hipotese de fibrocimento ao policarbonato e nao se considerou o abrigo/apoio do tanque resolvido pelo modelo plano de lajes.

## Entradas e qualidade da informacao

| Entrada | Valor | Origem / situacao |
|---|---:|---|
| Espessura da telha | 6 mm | Hipotese aceita pelo usuario |
| Inclinacao | 10% = {math.degrees(math.atan(inclination)):.5f} graus | Arquitetura e decisao do usuario |
| Peso da telha na superficie inclinada | 0,18 kN/m2 | Exemplar local NBR 6120:2019, Tabela 5, PDF19/p.13 |
| Fator superficie inclinada / horizontal | {factor:.8f} | sqrt(1 + 0,10^2) |
| Peso da telha em projecao horizontal | {sheet*factor:.6f} kN/m2 | Conversao geometrica da entrada normativa |
| Reserva da estrutura metalica | 0,15 kN/m2 horizontal | Hipotese numerica proposta nesta memoria, sem levantamento de perfis |
| Permanentes telha + reserva metalica | {g:.6f} kN/m2 horizontal | Soma preliminar, sem forro/tanque/abrigo/paredes |
| Variavel de manutencao do telhado | 0,25 kN/m2 horizontal | Exemplar local, secao 6.4, PDF35/p.29, i=10% |

A Tabela 5 inclui sobreposicao, fixacao e absorcao de agua; nao adicionar esses itens novamente. A Tabela 6 nao apresenta diretamente a composicao fibrocimento 6 mm + estrutura metalica adotada: por isso o valor da estrutura metalica nao foi apresentado como valor dessa tabela. O [Guia Tecnico Brasilit 2026](https://www.brasilit.com.br/sites/brasilit.com.br/files/produto/arquivos/Guia%20T%C3%A9cnico%20Brasilit%202026.pdf), p.37, informa 18 kg/m2 para telha de 6 mm incluindo agua/recobrimento/fixacao. E referencia comercial de ordem de grandeza; nao foi somada aos 0,18 kN/m2 e nao representa conversao exata entre kg e kN. O nome de fabricante nao constitui especificacao de compra.

A edicao normativa efetivamente lida e a do exemplar local identificado por hash; nao se confirmou nesta memoria a vigencia diretamente no catalogo ABNT. Nao se declarou atendimento integral a normas. Nao houve dimensionamento de telhas/perfis/fixacoes nem verificacao de vento, estanqueidade ou drenagem. Os recobrimentos e apoios dependem do produto e da inclinacao.

## Sensibilidade do peso ainda estimado

| Reserva metalica (kN/m2 horizontal) | Telha + metal (kN/m2 horizontal) |
|---:|---:|
| 0,10 | {cases[0]['totalRoofPermanentKNm2']:.6f} |
| 0,15 | {cases[1]['totalRoofPermanentKNm2']:.6f} |
| 0,20 | {cases[2]['totalRoofPermanentKNm2']:.6f} |

A faixa evidencia a parcela desconhecida, sem provar que os perfis reais estao dentro dela. Substituir por soma dos pesos efetivos dos perfis, ligacoes e contraventamentos quando houver arranjo e dimensionamento. Nao usar a area liquida das lajes IFC como area real do telhado: bordas, recortes, planos elevados e apoios diferem. A area e as reacoes totais permanecem nulas no sentido de desconhecidas (null), nunca zero numerico.

## Da carga por area as reacoes

Para uma barra simplesmente apoiada de vao L e faixa tributaria b, sob carga uniforme: wG = g_horizontal*b, wQ = q_horizontal*b; RG_esquerda = RG_direita = wG*L/2; RQ_esquerda = RQ_direita = wQ*L/2. O equilibrio pode ser conferido por soma(R)=w*L.

Exemplo unicamente aritmetico, b=1,50 m e L=3,90 m: wG={lineG:.6f} kN/m e wQ={lineQ:.6f} kN/m; cada extremidade recebe RG={reaction['leftPermanentKN']:.6f} kN e RQ={reaction['leftVariableKN']:.6f} kN. Esses numeros NAO sao reacoes reais do telhado do TCC, nao foram associados a vigas do Eberick e nao abrangem continuidade, excentricidade, vento/succao ou concentracao local. O vao do exemplo nao e vao aprovado de telha ou perfil. O mapa real de terças/tesouras e seus apoios precisa anteceder o lancamento.

## Compatibilidade com as cargas ja existentes

As lajes N2 mantem G2=0,25 kN/m2 (forro) e Q=1,00 kN/m2 no estado R58. O novo g do telhado e parcela separada, cuja transmissao por apoios reais ainda nao foi definida. Nao substituir G2 por 0,330898 e apagar o forro; tambem nao somar uniformemente a laje se o telhado descarrega em vigas/pontos distintos. A variavel do telhado de 0,25 e a da laje de 1,00 pertencem a superficies/funcoes distintas; nao se reduziu Q da laje nem se adicionou 0,25 automaticamente sem avaliar simultaneidade/casos.

O reservatorio de 1.000 L, sua tara, base e abrigo nao integram essa parcela. Permanecem tambem as paredes, escada, bordas, vento, combinacoes e verificacoes ELU/ELS. Aplicar a mesma memoria e o mesmo mapa de reacoes aos dois ramos quando estiverem fechados, cronometrando cada operacao e auditando o estado salvo.

Nao houve edicao de PRJ, RVT, DWG ou monografia nesta R59. Preservados {len(protected)} arquivos do manifesto R58. O tempo do script e somente sua execucao; exclui pesquisa, leitura, elaboracao e revisao. Nao produz medicao comparativa dos fluxos.
'''
(out/'LEIA-ME-R59.md').write_text(report,encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
write('R59-execucao-script.json',dict(durationMs=(time.perf_counter()-start)*1000,scope='Somente execucao do script; nao esforco total de IA/humano nem tempo de fluxo'))
write('R59-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='R59-manifesto.json']))
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
intro=f'''# Atualizacao R59 - 29/10/2026

Memoria unitaria da cobertura em outputs/Cobertura-H03-R59-MEMORIA-ESTUDO-NAO-EXECUTAR/LEIA-ME-R59.md. Usuario aceitou fibrocimento6mm/inclinacao10%/estrutura metalica leve. Do exemplar NBR6120:2019 Tabela5: telha0,18kN/m2 inclinado -> {sheet*factor:.6f} horizontal; reserva metalica0,15 proposta e nao quantificada -> g={g:.6f} horizontal; q_manutencao_telhado0,25. Nao aplicado. Area real/mapa de reacoes/metal/apoios ainda pendentes; exemplo de reacoes e apenas aritmetico, nao cargas do modelo. Nao substituir/somar automaticamente G2forro0,25 e Q_laje1,00. Policarbonato e abrigo elevado do tanque separados. Vigencia da NBR6120 nao conferida diretamente em catalogo nesta memoria.

Projetos nativos atuais: R58 diagnostico parcial (ambos salvos/reabertos e fechados, congelados com resultados); R57 e base limpa anterior. Nenhuma edicao nativa ou na monografia na R59. Proximo: definir arranjo/apoios do telhado, completar acoes e ELU/ELS. Ver pendencias no JSON da memoria. Nao executar.

---
Historico anterior:

'''
assert not old.startswith('# Atualizacao R59')
guide.write_text(intro+old,encoding='utf-8')
print(json.dumps(dict(output=str(out),sheetHorizontalKNm2=sheet*factor,roofGWithHypothesisKNm2=g,nativeModelsEdited=False)))

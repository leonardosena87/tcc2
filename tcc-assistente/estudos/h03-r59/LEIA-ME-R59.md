# H03/R59 - memoria unitaria de cargas da cobertura - ESTUDO, NAO EXECUTAR

O usuario aceitou telha ondulada de fibrocimento de 6 mm a 10% sobre estrutura metalica leve, com pesos e reacoes documentados como hipoteses. A arquitetura registra fibrocimento a 10% e uma cobertura de policarbonato a 5% separada; o corte BB representa o reservatorio de 1.000 L e ressalto local de 0,60 m. Nao se estendeu a hipotese de fibrocimento ao policarbonato e nao se considerou o abrigo/apoio do tanque resolvido pelo modelo plano de lajes.

## Entradas e qualidade da informacao

| Entrada | Valor | Origem / situacao |
|---|---:|---|
| Espessura da telha | 6 mm | Hipotese aceita pelo usuario |
| Inclinacao | 10% = 5.71059 graus | Arquitetura e decisao do usuario |
| Peso da telha na superficie inclinada | 0,18 kN/m2 | Exemplar local NBR 6120:2019, Tabela 5, PDF19/p.13 |
| Fator superficie inclinada / horizontal | 1.00498756 | sqrt(1 + 0,10^2) |
| Peso da telha em projecao horizontal | 0.180898 kN/m2 | Conversao geometrica da entrada normativa |
| Reserva da estrutura metalica | 0,15 kN/m2 horizontal | Hipotese numerica proposta nesta memoria, sem levantamento de perfis |
| Permanentes telha + reserva metalica | 0.330898 kN/m2 horizontal | Soma preliminar, sem forro/tanque/abrigo/paredes |
| Variavel de manutencao do telhado | 0,25 kN/m2 horizontal | Exemplar local, secao 6.4, PDF35/p.29, i=10% |

A Tabela 5 inclui sobreposicao, fixacao e absorcao de agua; nao adicionar esses itens novamente. A Tabela 6 nao apresenta diretamente a composicao fibrocimento 6 mm + estrutura metalica adotada: por isso o valor da estrutura metalica nao foi apresentado como valor dessa tabela. O [Guia Tecnico Brasilit 2026](https://www.brasilit.com.br/sites/brasilit.com.br/files/produto/arquivos/Guia%20T%C3%A9cnico%20Brasilit%202026.pdf), p.37, informa 18 kg/m2 para telha de 6 mm incluindo agua/recobrimento/fixacao. E referencia comercial de ordem de grandeza; nao foi somada aos 0,18 kN/m2 e nao representa conversao exata entre kg e kN. O nome de fabricante nao constitui especificacao de compra.

A edicao normativa efetivamente lida e a do exemplar local identificado por hash; nao se confirmou nesta memoria a vigencia diretamente no catalogo ABNT. Nao se declarou atendimento integral a normas. Nao houve dimensionamento de telhas/perfis/fixacoes nem verificacao de vento, estanqueidade ou drenagem. Os recobrimentos e apoios dependem do produto e da inclinacao.

## Sensibilidade do peso ainda estimado

| Reserva metalica (kN/m2 horizontal) | Telha + metal (kN/m2 horizontal) |
|---:|---:|
| 0,10 | 0.280898 |
| 0,15 | 0.330898 |
| 0,20 | 0.380898 |

A faixa evidencia a parcela desconhecida, sem provar que os perfis reais estao dentro dela. Substituir por soma dos pesos efetivos dos perfis, ligacoes e contraventamentos quando houver arranjo e dimensionamento. Nao usar a area liquida das lajes IFC como area real do telhado: bordas, recortes, planos elevados e apoios diferem. A area e as reacoes totais permanecem nulas no sentido de desconhecidas (null), nunca zero numerico.

## Da carga por area as reacoes

Para uma barra simplesmente apoiada de vao L e faixa tributaria b, sob carga uniforme: wG = g_horizontal*b, wQ = q_horizontal*b; RG_esquerda = RG_direita = wG*L/2; RQ_esquerda = RQ_direita = wQ*L/2. O equilibrio pode ser conferido por soma(R)=w*L.

Exemplo unicamente aritmetico, b=1,50 m e L=3,90 m: wG=0.496347 kN/m e wQ=0.375000 kN/m; cada extremidade recebe RG=0.967876 kN e RQ=0.731250 kN. Esses numeros NAO sao reacoes reais do telhado do TCC, nao foram associados a vigas do Eberick e nao abrangem continuidade, excentricidade, vento/succao ou concentracao local. O vao do exemplo nao e vao aprovado de telha ou perfil. O mapa real de terças/tesouras e seus apoios precisa anteceder o lancamento.

## Compatibilidade com as cargas ja existentes

As lajes N2 mantem G2=0,25 kN/m2 (forro) e Q=1,00 kN/m2 no estado R58. O novo g do telhado e parcela separada, cuja transmissao por apoios reais ainda nao foi definida. Nao substituir G2 por 0,330898 e apagar o forro; tambem nao somar uniformemente a laje se o telhado descarrega em vigas/pontos distintos. A variavel do telhado de 0,25 e a da laje de 1,00 pertencem a superficies/funcoes distintas; nao se reduziu Q da laje nem se adicionou 0,25 automaticamente sem avaliar simultaneidade/casos.

O reservatorio de 1.000 L, sua tara, base e abrigo nao integram essa parcela. Permanecem tambem as paredes, escada, bordas, vento, combinacoes e verificacoes ELU/ELS. Aplicar a mesma memoria e o mesmo mapa de reacoes aos dois ramos quando estiverem fechados, cronometrando cada operacao e auditando o estado salvo.

Nao houve edicao de PRJ, RVT, DWG ou monografia nesta R59. Preservados 65 arquivos do manifesto R58. O tempo do script e somente sua execucao; exclui pesquisa, leitura, elaboracao e revisao. Nao produz medicao comparativa dos fluxos.

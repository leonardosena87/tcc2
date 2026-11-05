# R223 — Ensaio nativo da V1 de 30 × 30 cm nos dois fluxos

Pasta local: `D:/TCC/outputs/H03-R223-V1-30X30-ENSAIO-NAO-EXECUTAR`. Preservou-se integralmente a R222. A alteração foi aplicada pela interface do Eberick 2025 Infinity, em cópias independentes CAD e BIM. Não se alterou o trabalho escrito, o Revit nem o AutoCAD nesta revisão.

## Alteração aplicada e processamento

A largura da V1 do N0 passou de 20 para 30 cm, mantendo altura de 30 cm e topo em +0,20 m. Os apoios AE1A/AE1B foram representados com B=H=30 cm, altura de 20 cm, elevação zero e vínculo engastado. Esses cadastros nativos do tipo Sapata continuam sendo **apoios idealizados, não fundações dimensionadas**. A ampliação da representação não valida transmissão ao solo, capacidade geotécnica ou corpo de apoio.

Processou-se cada cópia com análise estática ELU, dimensionamento geral e cálculo de deslocamentos do pórtico e das lajes com rigidez fissurada. Não se marcou dimensionamento somente dos elementos selecionados nem análise dinâmica. As mensagens nativas registraram sucesso de dimensionamento para os elementos da superestrutura e 14 sapatas com erro por fluxo, fora do dimensionamento do estudo. Sucesso automático não encerra os avisos e verificações externas.

| Registro da R223 | CAD | BIM |
|---|---:|---:|
| Tempo total de processamento informado pelo Eberick | 10 s | 11 s |
| Dimensionamento dos elementos, já incluído no total | 3 s | 3 s |
| Carga vertical total exibida | 114,47 tf | 114,47 tf |
| Gama-Z máximo exibido | 1,06 | 1,06 |
| Deslocamento horizontal máximo exibido | 0,15 cm | 0,16 cm |
| Limite de deslocamento exibido | 0,42 cm | 0,42 cm |
| Casos e combinações da V1 no relatório | 19 + 68 | 19 + 68 |

Trata-se de uma observação por fluxo, com as mesmas opções de cálculo. Não é duração total do desenvolvimento, média experimental ou prova de ganho de produtividade. Não se soma novamente o dimensionamento ao total. O intervalo entre clique e observação do término inclui espera e controle da interface e não substitui a duração do relatório. Tokens, custo e tempo de inferência de IA não foram medidos nesta revisão. As pequenas diferenças de rigidez anteriormente registradas no N1 e de agrupamento nominal das vigas não foram eliminadas pelo ensaio.

O detalhe nativo da V1 gerou 3Ø8 superiores contínuos com ganchos projetados de 27 cm, preservou 4Ø8 inferiores com ganchos de 10 cm e 2×2Ø8 laterais, e apresentou 8 estribos Ø6,3 c/15. Permaneceram o Aviso19 e dois Avisos98. Conferiu-se, após reabertura dos projetos, a continuidade de 6Ø10 nos três lances de P2/P9 no CAD e P3/P4 no BIM; não foi necessário reaplicar a uniformização nesta revisão.

## Conferência complementar reproduzível

Exportaram-se novamente pórtico, grelhas das lajes N1/N2 e grelha da escada, com **Exportar seções desmarcado** e **Exportar coeficientes redutores marcado**. Emitiram-se novos relatórios de combinações da V1. As 87 tabelas de cada relatório coincidem nos 14 campos numéricos, na precisão impressa. Não se executou SAP2000. O arquivo genérico foi lido pelo código auxiliar de reconstrução linear.

A nova grelha contém cinco trechos deformáveis da V1, entre X=456 e534 cm, Y=321,58 cm e Z=20 cm, área900 cm², I22=I33=67500 cm⁴. Os trechos externos de rigidez muito elevada não foram tratados como viga deformável. A área, as extremidades e o comprimento de78 cm foram verificados explicitamente, mantendo controles distintos dos88 cm da R217. O vão livre exibido pelo detalhe é60 cm; não se confundem vão livre e extensão das barras do modelo analítico.

O erro máximo de reprodução dos momentos verticais G1/G2/Q é inferior a0,005 kN·m nos dois fluxos. O resíduo relativo do sistema é inferior a3,4×10⁻⁶. A verificação de sensibilidade com deformação de cisalhamento foi repetida. Isso controla a implementação auxiliar, mas não valida independentemente todos os esforços horizontais ou a análise integral do Eberick.

A resistência auxiliar conserva somente dois Ø8 de canto por face, desprezando a armadura adicional nativa. Para cada combinação, somaram-se índices de flexão nos dois planos com resistência mínima nos extremos do intervalo axial. É um critério adicional conservador adotado no estudo, sem atribuir à norma uma expressão biaxial que não tenha sido demonstrada. O índice máximo foi0,3036. A sensibilidade com piso vertical de8 kN·m, conservada do histórico de dimensionamento, resultou0,8388; não corresponde a um novo momento simultâneo observado. Os limites por combinação podem ocorrer em posições diferentes.

Na triagem transversal, d=259,7 mm nos dois planos; o limite de espaçamento longitudinal é155,82 mm, superior aos150 mm nativos, e a distância entre ramos233,7 mm é inferior a259,7 mm. O maior cortante vertical foi18,965 kN e o horizontal15,830 kN. O índice linear adicional, desprezando a contribuição do concreto e somando as demandas das duas direções nos estribos, foi0,8238. A triagem da biela forneceu0,1030. Os dois cortantes são inferiores a20% de VRd2 no regime usado para limitar a distância entre ramos. Assim, o ensaio30×30 elimina as duas incompatibilidades geométricas de espaçamento que motivaram o complemento externo R218 c/9 e seus grampos. Isso não encerra todas as verificações da viga.

## Ancoragem e desenho proposto

Incluiu-se M/z nos dois planos, V nos dois planos e tração axial, por combinação, como limite conservador da força para estudar ancoragem. O maior limite foi49,676 kN. A triagem com três barras superiores e quatro inferiores forneceu, respectivamente, comprimentos necessários com gancho de159,83 e119,87 mm, com boa aderência. A disponibilidade geométrica antes do início da dobra foi estimada em235,7 mm, já descontando cobrimento, estribo, raio da barra e raio de eixo da curva. Para a face lateral, duas barras sem contar os cantos forneceram154,07 mm de ancoragem reta na triagem horizontal. Não se assume que cada barra tenha força idêntica ou que a soma de limites substitua a verificação do nó.

O gancho superior automático de27 cm **não foi aceito como geometria final**. Preparou-se DXF/PNG complementar com proposta de projeção superior de9,5 cm e pino mínimo de40 mm para Ø8 CA-50, raio de eixo24 mm e ponta reta71 mm, superior aos64 mm requeridos para o gancho de90°. Com o gancho inferior de10 cm, a folga vertical nominal entre pontas opostas fica24,4 mm. A projeção de9,5 cm evita a folga de apenas19,4 mm que resultaria de dois ganchos opostos de10 cm na mesma linha. O estudo indica nove posições de estribo em113,37 cm, passo14,17 cm, distinguindo essa distribuição proposta das oito posições nativas. Não se libera comprimento de corte.

A força de25% de uma barra Ø8 totalmente solicitada é5,464 kN; um ramo Ø6,3 tem resistência de escoamento13,553 kN. Esse confronto de área não comprova a localização efetiva de confinamento no nó. É necessário fechar a disposição e os ganchos de todos os estribos, a ancoragem das barras laterais, o cruzamento de barras e a ligação ao apoio. Boa aderência pressupõe concretagem convencional da seção de30 cm e verificação das juntas; a sensibilidade de má aderência foi mantida no JSON. Alternância entre tração e compressão e ancoragem das barras comprimidas também precisam ser tratadas conforme9.4.2.1.

O DXF é **externo e não foi importado no Eberick**: o gerenciador voltou a retornar indisponibilidade do AltoQi Builder. A armadura nativa, os ganchos e a relação de aço não foram substituídos pelo desenho. O arquivo PNG foi inspecionado visualmente. Os desenhos20×30 da R218 e o diagnóstico herdado da R222 permanecem somente históricos dentro das cópias e não devem ser apresentados como saídas atualizadas da R223.

## Reprodução e limites

`verificar.py` gera `R223-resultados.json`; `desenhar.py` gera o DXF e sua prévia PNG; `preservar.py` verifica os originais R222, os CRC dos PRJ e os hashes dos arquivos incluídos no ZIP local. Os parâmetros adicionados ao solver R217 conservam seus valores padrão para reproduzir a revisão antiga. Não se editam binários de engenharia por script.

Passaram sete testes da R223, dez regressões da R217, sete regressões de ancoragem da R221 e82 testes JavaScript de `tcc-assistente`. São controles de software; não são aprovação estrutural, chamadas reais à IA ou ensaios físicos. A aplicação e o processamento descritos acima ocorreram efetivamente no Eberick.

Persistem: fechar a ligação/ancoragens e ELS local da V1, conferir o Aviso08 da cobertura, demais apoios/interferências essenciais, sincronizar a geometria nos arquivos de autoria Revit/AutoCAD e consolidar os resultados e tempos totais válidos. O estudo está limitado à superestrutura com apoios idealizados. **A R223 é uma hipótese favorável à triagem, ainda não liberada como projeto executivo.**

Norma consultada: exemplar local ABNT NBR6118:2026, itens9.3,9.4.2,17.3.5,17.4 e18.3. As verificações normativas finais e a responsabilidade técnica não são substituídas pelos testes auxiliares. Fontes do fabricante: [Aviso19](https://suporte.altoqi.com.br/hc/pt-br/articles/360009988354), [exportação genérica](https://suporte.altoqi.com.br/hc/pt-br/articles/360016037073) e ajuda instalada `detalhamento_vigas_ancoragem.htm`.

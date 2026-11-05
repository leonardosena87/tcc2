# R222 — Continuidade de armadura dos pilares e diagnóstico atual

Pasta local: `D:/TCC/outputs/H03-R222-CONTINUIDADE-PILARES-NAO-EXECUTAR`. Cópias completas CAD e BIM da R221, preservada. Não se alterou o trabalho escrito.

Na releitura do CAD, identificou-se que P2 e P9 tinham 6Ø10 no lance L3 e 4Ø10 nos lances L2/L1. Aplicou-se **Uniformizar abaixo** (Alt+U), a partir de L3, individualmente nos dois pilares. O Eberick passou a indicar 6Ø10 e As efetivo de 4,71 cm² nos três lances. Nos dois inferiores, registrou As anterior de 3,14 cm² e acréscimo de 1,57 cm². Salvou-se com Ctrl+B, fechou-se e reabriu-se o CAD; confirmou-se a retenção nas duas prumadas. Esta correção recupera a uniformização perdida após o processamento CAD anterior; não é uma falha nova de importação CAD.

No BIM, os correspondentes P4 e P3 já apresentavam 6Ø10 e 4,71 cm² nos três lances. Não se reaplicou uma alteração desnecessária. As capturas registram os dois pilares. Conferiu-se também a V1 do N0: os dois fluxos mantiveram quatro barras inferiores Ø8 e 2×2 Ø8 de pele após a emissão dos diagnósticos. A armadura superior adicional rejeitada na R221 continua desligada.

Emitiram-se relatórios nativos **Diagnóstico da estrutura** dos dois projetos. Preservaram-se separadamente os relatórios herdados da R221 antes de substituí-los nas cópias de trabalho. A emissão pode recalcular dimensionamentos pendentes; no BIM observou-se a janela de cálculo de vigas. Não se acionou um novo processamento global de pórtico/grelhas e não se registrou uma duração pareada. O BIM mostrou falha de acesso ao Builder depois da emissão, mas o DOCX foi gravado e seu conteúdo foi extraído e conferido. A mensagem foi fechada; não se tratou a falha de visualização como ausência de relatório.

| Leitura nativa atual | CAD | BIM |
|---|---:|---:|
| Cargas verticais totais | 1.144,28 kN | 1.144,28 kN |
| Gama-Z exibido | 1,06 | 1,06 |
| Deslocamento horizontal exibido | 0,15 cm | 0,16 cm |
| Limite exibido para esse deslocamento | 0,42 cm | 0,42 cm |
| Erros automáticos na superestrutura | 0 | 0 |
| Vigas com avisos no N2 | 1 | 1 |
| Vigas com avisos no N0 | 1 | 1 |
| Pilares idealizados com avisos no N0 | 11 | 11 |
| Sapatas com erros, fora do dimensionamento do estudo | 14 | 14 |

Os relatórios afirmam não haver elemento com deslocamento excessivo. Esses indicadores e a ausência de erros automáticos **não aprovam os avisos de detalhamento, os apoios nem a estrutura**. A V1 continua com verificação externa incompleta; a cobertura mantém Aviso 08. A revisão de estribos R218 continua externa, com limite máximo de 9 cm, enquanto o detalhe automático e sua relação de aço mostram c/15. Por isso, os quantitativos automáticos de aço e os custos padrão do diagnóstico não são apresentados como quantitativos ou orçamento finais.

O CAD agrupa mais vigas nomeadas que o BIM. Os totais de itens dos relatórios não são contagens equivalentes de elementos físicos nem medidas de retrabalho; a comparação exige os eixos/trechos já auditados. Não se interpretam diferenças pequenas de deslocamento ou de aço automático como superioridade de um fluxo.

As prioridades restantes são o fechamento do detalhe e da ligação da V1, a conferência do Aviso 08 e dos apoios/interferências essenciais, a atualização comum de Revit/AutoCAD e a consolidação dos resultados e tempos comparáveis. Esta revisão conclui a correção de uniformização de P2/P9 no CAD, não o projeto executivo. As conferências foram feitas dentro do Eberick e nos relatórios gerados; não houve teste simulado da interface.

# H03/R145 — complemento de forro sob N1

Estudo parcial, NÃO EXECUTAR. Criaram-se duas cópias independentes das bases R116: 70/CAD e 71/BIM. Os 35 arquivos-fonte permaneceram íntegros por SHA-256. As cópias fechadas após o cadastro foram congeladas em `congelados-apos-cadastro`, na pasta local desta revisão.

A leitura dos cortes AA e BB da arquitetura mostra indicação de forro de gesso nos ambientes abaixo dos dois pavimentos elevados. O cadastro anterior de N1 contemplava apenas a hipótese de piso de 5 cm × 20 kN/m³ = 1,00 kN/m². Acrescentou-se 0,25 kN/m² para o forro sob as quatro lajes internas N1/L1–L4, reutilizando a hipótese de peso adotada para N2 na R53. Não se trata de especificação de fabricante ou levantamento completo dos componentes de uma instalação real. O resultado nesses quatro campos Revestimento passou a 1,25 kN/m². Não se somou novamente o peso próprio da laje.

Em cada ramo, alteraram-se quatro campos pela interface nativa. A carga variável permaneceu 1,50 kN/m², a espessura 14 cm, a elevação zero e o campo Extra zero. Salvaram-se os desenhos e o projeto; fechou-se, reabriu-se e releu-se cada laje. Como controles, N1/L5 e L6 mantiveram Revestimento 1,00 kN/m² e Acidental 2,50 kN/m². N2 não foi aberto nem relido nesta sessão. Não se estendeu automaticamente a hipótese de forro ao hall, varanda, lances ou patamar da escada.

Obtiveram-se oito alterações de cadastro, doze leituras individuais após reabertura e trinta pares de campos iguais nas seis lajes N1. Essa contagem não representa correções provocadas pelo formato DWG ou IFC: o complemento decorreu da evolução comum das hipóteses do estudo. O hash do PRJ salvo permaneceu igual durante a consulta posterior nos dois ramos. O teste de integridade ZIP confirmou apenas a legibilidade do contêiner.

Os textos AX intermediários `BIM-N1-L3-editada-UI.txt` e `BIM-N1-L4-editada-UI.txt` contêm valores transitórios duplicados. Não foram usados para confirmar a gravação. Preservaram-se os arquivos originais; as imagens e a leitura limpa após reabrir documentam o valor efetivamente observado. Na seleção CAD/L5 foi necessário escolher Laje em vez de Texto na lista de objetos sobrepostos; isso é operação de interface, não defeito comprovado do DWG.

| Intervalo observado | Duração |
|---|---:|
| CAD, abrir → editar → salvar → reabrir → consultar → fechar | 481,466 s (8 min 1,466 s) |
| BIM, mesmo conjunto de cadastro e consulta | 479,637 s (7 min 59,637 s) |

Os intervalos incluem observações, latência, raciocínio e registros; o BIM também inclui a compactação do contexto após o fechamento da janela. Executou-se o BIM depois do CAD, com aprendizagem e agrupamento de ações. Não se calcula vantagem percentual, ranking ou tempo total dos fluxos a partir dessa dupla. Não houve intervenção humana durante a operação. Tempo ativo humano, inferência isolada, tokens e custo da IA não foram medidos.

Não houve processamento estrutural ou nova exportação nesta revisão. Os resultados antigos eventualmente presentes nas cópias pertencem à R116 e não são resultados recalculados para as cargas R145. O cadastro corrigido pode servir de entrada parcial para o próximo processamento, mantendo em aberto paredes, escada, reservatório, vento, compatibilização e verificações completas de ELU/ELS. Os ensaios de paredes não aceitos não foram incorporados. Não se alterou a monografia, o RVT ou o DWG de autoria.

Os testes automatizados verificam a extração das leituras reais e a rejeição de projeto/laje ou valores contraditórios; não constituem ensaio físico, dimensionamento ou validação normativa. PRJ e demais binários nativos permanecem somente em D:/TCC.

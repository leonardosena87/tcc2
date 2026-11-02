# H03/R148 — triagem de dimensionamento com cargas parciais

Em cópias independentes 74/CAD e 75/BIM da R146, habilitou-se dimensionamento apenas de vigas, pilares e lajes de N1/N2, pela lista de elementos selecionados. N0 e fundações permaneceram desmarcados. A análise manteve deslocamentos do pórtico com rigidez configurada; não se calcularam flechas das lajes, rigidez fissurada ou dinâmica. O término foi “Estrutura processada com avisos”. As cargas continuam incompletas; a execução do comando não significa aprovação do projeto ou das armaduras.

| Pavimento / categoria nativa | CAD: dimensionada / aviso / erro | BIM: dimensionada / aviso / erro |
|---|---:|---:|
| N1 — vigas | 14 / 1 / nenhuma categoria de erro exibida | 10 / 1 / 1 |
| N1 — lajes | nenhuma categoria sem aviso / 6 / nenhuma categoria de erro exibida | nenhuma categoria sem aviso / 6 / nenhuma categoria de erro exibida |
| N1 — pilares | 10 / 1 / nenhuma categoria de erro exibida | 10 / 1 / nenhuma categoria de erro exibida |
| N2 — vigas | 14 / 1 / nenhuma categoria de erro exibida | 7 / 1 / nenhuma categoria de erro exibida |
| N2 — lajes | nenhuma categoria sem aviso / 5 / nenhuma categoria de erro exibida | nenhuma categoria sem aviso / 5 / nenhuma categoria de erro exibida |
| N2 — pilares | 11 / nenhuma categoria de aviso ou erro exibida | 11 / nenhuma categoria de aviso ou erro exibida |

São contagens de peças na janela nativa, não contagens dos 29 elementos lógicos de viga da proposta nem um índice direto de defeitos. A diferença de agrupamento e continuidade das vigas precisa ser reconciliada antes de comparar detalhamento ou taxas de correção. Não se igualaram resultados apagando mensagens ou alterando seções.

O BIM/N1 apresentou **V2 — Erro D16: armadura negativa, nó 2**. Não apareceu categoria de erro na leitura CAD correspondente de N1. A documentação oficial orienta examinar os resultados da armadura por bitola no nó indicado para identificar a restrição específica: https://suporte.altoqi.com.br/hc/pt-br/articles/360000680694 . Essa consulta detalhada ainda não ocorreu; não se atribui o erro automaticamente ao IFC, a insuficiência de resistência ou a uma causa de ancoragem.

Nas mensagens expandidas, CAD/N1 V9 exibiu Aviso 98 de ancoragem da armadura de pele, nó 3; BIM/N1 V11 exibiu o mesmo código, nó 1. CAD/N1 P2 e BIM/N1 P4 exibiram Aviso 10, armadura inferior ao lance acima. CAD/N2 V13_1 e BIM/N2 V3 exibiram Aviso 08, carga negativa. A identidade geométrica desses pares ainda exige conferência; os nomes diferentes não são prova de peças diferentes ou iguais. A amostra CAD/N2 L1 mostrou Aviso 123, deslocamentos não verificados, coerente com flechas de lajes desmarcadas. Não se expandiram todos os onze avisos das lajes nem se inferiu que todos tenham o mesmo código. Nenhum desses avisos foi resolvido nesta revisão.

Os resumos verticais mantiveram PP 75,69 tf, adicional 12,04 tf, acidental 17,11 tf, QT 1,78 tf e total 106,62 tf. Isso não elimina as diferenças de direção e percentuais já registradas na R146.

Salvaram-se e fecharam-se as cópias. A integridade ZIP dos PRJs e os hashes do congelamento foram verificados; os 35 arquivos-fonte R146 permaneceram íntegros. Não se releram todas as armaduras após reabertura. Houve falhas de seleção indexada e de referência de imagem; coordenadas de capturas atualizadas permitiram continuar. O diálogo de status CAD foi trazido à área visível por dois deslocamentos na própria interface. A tentativa Alt+Espaço abriu uma janela auxiliar do ChatGPT, sem alterar dados do modelo. Não houve intervenção humana na operação do Eberick; a resposta do usuário sobre a escada é decisão de projeto, registrada separadamente.

Sessão CAD: 647,233 s (10 min 47,233 s). Sessão BIM: 15.662,690 s (4 h 21 min 2,690 s), **incluindo longa interrupção entre turnos**, retomada e resposta sobre a escada. Não representam trabalho contínuo ou tempo ativo comparável. Os intervalos comando → observação de término foram 16,323 s CAD e 18,542 s BIM, com captura intermediária a 78%/87% e latência do assistente. Estão contidos nas sessões e não devem ser somados. Não se calcula vantagem, ranking, inferência isolada, tokens ou custo da IA.

Os testes extraem evidências reais, preservam a existência do erro BIM e rejeitam consulta ao projeto errado. A primeira captura `BIM-status-N1-vigas` teve árvore AX anterior à expansão, embora a imagem já mostrasse os grupos; utilizou-se a captura posterior `BIM-erros-N1-V2` para a extração validada. Preservaram-se ambas sem reconstruir o histórico. Não se alteraram RVT, DWG ou monografia. Os binários nativos permanecem em D:/TCC.

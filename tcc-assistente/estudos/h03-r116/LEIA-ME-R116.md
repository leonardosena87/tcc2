# H03/R116 — sensibilidade calculada com P2

Processaram-se cópias independentes da R115 no Eberick 2025 Infinity, após acrescentar a hipótese gravitacional P2-GRAV-A à varanda VP1-A. Selecionaram-se análise estática e determinação dos deslocamentos do pórtico com **rigidez configurada**, mantendo desativados dimensionamento, flechas das lajes, rigidez fissurada e análises dinâmicas. As capturas finais de configuração documentam esse escopo nos dois ramos. Ambos concluíram com avisos, foram salvos, fechados e congelados.

| Parcela vertical exibida | CAD (tf) | BIM (tf) | Variação exibida em relação à própria R111 (tf) |
| --- | ---: | ---: | ---: |
| Peso próprio | 75,69 | 75,69 | 0,00 |
| Adicional | 10,56 | 10,56 | +0,40 |
| Acidental | 17,11 | 17,11 | 0,00 |
| Q_TELHADO_MANUTENCAO | 1,78 | 1,78 | +0,30 |
| Total | 105,14 | 105,14 | +0,70 |

O resumo mantém o aviso de relação carga/área não usual, com área aproximada de 132,81 m² e relação de 791,65 kgf/m². O acréscimo exibido não substitui balanço integral de reações e cargas, nem calibração da conversão de unidades do programa. Os totais possuem arredondamento e ainda representam um modelo de cargas parcial.

O deslocamento horizontal máximo apresentado foi 0,20 cm em X+, X−, Y+ e Y−, com limite exibido de 0,42 cm. O máximo relativo apresentado foi 0,17 cm, com limite exibido de 0,35 cm. Gama-Z apresentou 1,09, 1,08, 1,06 e 1,05 respectivamente em X+, X−, Y+ e Y−, com limite exibido de 1,10. Esses valores e limites coincidiram entre os ramos. Não se validou nesta etapa a adequação final dos parâmetros e limites normativos, do vento, das combinações ou da rigidez.

Persistiu a diferença de direção associada ao máximo relativo: CAD **N1/Y−**, BIM **TCC-cdd31967-N1/Y+**. A correspondência de pavimentos foi explicitada nas etapas anteriores; a diferença de direção não foi apagada ao comparar o valor de 0,17 cm. Sua causa continua desconhecida e não se demonstrou defeito de transferência.

No trecho de deslocamentos do topo, os pares numéricos arredondados coincidiram, mas os aumentos percentuais apresentaram duas diferenças: Vento X+ = 14,61% no CAD e 14,60% no BIM; Vento Y+ = 8,29% no CAD e 8,30% no BIM. Cada diferença é de 0,01 ponto percentual. A unidade não aparece explicitamente nesse trecho do resumo; o JSON preserva os números como exibidos sem lhes atribuir unidade não confirmada. Não se inferiu erro, equivalência interna exata ou ausência de mudança de esforços a partir desses arredondamentos.

O tempo observado entre acionar OK e capturar a primeira tela de término foi **21,528879 s no CAD** e **22,313809 s no BIM**. Inclui latência da interface e da captura, sem instrumentação interna do solver. Está contido no tempo de sessão e não deve ser somado a ele. A sessão CAD durou 6.142,434294 s (cerca de 1h42min22s), incluindo intervalo de retomada; a BIM durou 264,005402 s (4min24s). Essas sessões não permitem comparação de produtividade ou classificação final dos fluxos. O tempo ativo e o esforço isolado de inferência da IA não foram medidos separadamente.

Os 33 arquivos fonte R115 conservaram seus hashes. Congelaram-se e conferiram-se 16 arquivos CAD e 19 BIM após fechamento. Os binários ficam em D:/TCC; somente código, evidências e registros pertinentes foram preparados para o repositório. Dois controles verificam a leitura das evidências reais, a preservação das divergências e a rejeição de resumo incompleto ou intervalo fora da sessão.

Não houve dimensionamento de concreto, armaduras, cobertura metálica ou ancoragens. Reservatório, demais cargas, vento/sucção, caso localizado de manutenção e combinações continuam pendentes. O resultado comprova a conclusão do ensaio parcial com essas parcelas, sem aprovar a estrutura ou encerrar a comparação CAD/BIM.

Arquivos:

- CAD: `D:/TCC/outputs/30-H03-R116-CAD-P2-NAO-EXECUTAR/`
- BIM: `D:/TCC/outputs/31-H03-R116-BIM-P2-NAO-EXECUTAR/`
- Evidências e congelados: `D:/TCC/outputs/Analise-H03-R116-P2-NAO-EXECUTAR/`

Próximas frentes: atualizar o inventário temporal sem dupla contagem e completar as pendências de cargas/compatibilização, preservando os resultados R116 para comparação posterior.

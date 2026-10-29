# H03/R69 — inventário dos tempos e preparação dos resultados

Inventariaram-se 112 arquivos de tempos nas pastas de primeiro nível de outputs. Foram classificados 87 arquivos com duração principal explícita, 10 contêineres/consolidados e 15 registros sem duração principal. A cobertura da busca é explícita: não inclui tempos em work, pacote de entrega, congelados, banco do painel ou logs de API não chamados *tempo*.json. Não se criou uma contagem de todo o esforço do TCC.

Preservaram-se caminho, hash, campo original da duração, limites UTC quando disponíveis, escopo e declarações de comparabilidade. Os campos ausentes são nulos, nunca zero. Datas sem fuso não foram adivinhadas. Não se expandiram contêineres históricos para evitar recontar registros que também existem em arquivos separados. Não se somaram duração geral, exportação e processamento, pois podem representar intervalos sobrepostos. O JSON aponta10 pares com sobreposição temporal dos limites declarados, que são candidatos a revisão, não erros comprovados.

## Intervalos exploratórios recentes H03

| Revisão | CAD, duração assistida declarada | BIM, duração assistida declarada | Uso nos resultados |
|---|---:|---:|---|
| R53 | 9 min 8.857 s | 10 min 50.100 s | Exploratória; consultar escopos individuais |
| R54 | 12 min 37.827 s | 11 min 8.593 s | Exploratória; consultar escopos individuais |
| R56 | 3 min 52.908 s | 2 min 10.735 s | Exploratória; consultar escopos individuais |
| R57 | 5 min 22.321 s | 3 min 43.229 s | Exploratória; consultar escopos individuais |
| R58 | 1 min 43.431 s | 1 min 19.665 s | Exploratória; consultar escopos individuais |
| R61 | 9 min 50.106 s | 11 min 36.352 s | Exploratória; consultar escopos individuais |
| R63 | 25 min 40.686 s | 23 min 50.756 s | Exploratória; consultar escopos individuais |
| R64 | 33 min 39.634 s | 52 min 36.698 s | Exploratória; consultar escopos individuais |

Os números acima permanecem resultados operacionais parciais. Os escopos não são necessariamente iguais: por exemplo, na R63 o CAD corrigiu pontos anteriores e o BIM inseriu onze nós; na R64 ambos leram13 pontos, mas o BIM incluiu recuperação da captura e os intervalos incorporaram latência/continuidade. O inventário não transforma uma sequência exploratória em ensaio controlado. Não se calculou percentual de economia, tempo total por fluxo ou vencedor. R66 sem intervalo completo recuperável foi mantida como ausência de dado, não como0s; ela é documentada no relatório próprio e não apareceu artificialmente nesta tabela.

## Como esses dados entram no TCC

Apresentar o histórico como desenvolvimento e aperfeiçoamento do protótipo: duração, escopo, produto entregue, ocorrência e evidência. Distinguir três origens de correção: interpretação da arquitetura/concepção comum; representação ou transferência demonstrada; operação/instrumentação. Uma falta de carga após aplicação nativa ou perda de foco não é automaticamente erro DWG/IFC. A correção de referência da porta na R68 é interpretação geométrica comum; não é vantagem comprovada de um programa.

O comparativo principal deve ser o ensaio pareado definido no protocolo separado. Informar explicitamente que o teste de uma edificação e de versões/configurações determinadas não permite generalização estatística para todos os projetos. Não reconstruir tempo ativo humano por tempo de conversa nem inferência da IA por duração de script. Quando houver log real de chamada IA, tempo, tokens e custo devem ter fonte/ID e ser apresentados em campos próprios, sem duplicar um subintervalo já incluído no tempo total.

## Preservação

Conferiram-se os hashes de11 arquivos R68. Nenhum registro histórico, nativo, monografia ou arquivo de origem foi alterado. Os testes do instrumento de tempos, quando executados, são simulados e não produzem medições empíricas dos programas. A última configuração de engenharia conferida permanece R64; R65Q e R66ações continuam pendentes.

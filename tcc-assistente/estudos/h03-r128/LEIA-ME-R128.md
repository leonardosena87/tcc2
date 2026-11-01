# H03/R128 — resultados parciais e roteiro de fechamento

Esta síntese reúne evidências verificadas, sem alterar a monografia ou os modelos. O estudo permanece parcial e sem dimensionamento final aprovado. As diferenças de unidades lógicas, sólidos e barras analíticas são mantidas; nenhuma contagem vira automaticamente número de erros ou ações de interface.

## Chegada inicial ao Eberick — evidência histórica R45/R46, consolidada na R72

| Unidade lógica | Proposta comum | CAD nativo inicial | BIM nativo inicial |
|---|---:|---:|---:|
| Trecho de pilar | 22 | 0 | 22 |
| Viga lógica | 29 | 0 | 29 |
| Laje | 11 | 0 | 0 |

Havia 0/62 unidades tipadas no CAD e 51/62 no BIM (82,26%). O CAD preservou 62/62 contornos e 66/66 conteúdos textuais, como referência gráfica. A reconstrução posterior abrangeu 62 unidades no CAD e 11 no BIM. Esses números são unidades lógicas complementadas, não operações de interface, correções ou defeitos. O fluxo BIM incluiu tratamento explícito de 17 registros de geometria nominal e retirada de 2 pavimentos vazios; esse esforço permanece parte do fluxo.

## Conferências posteriores

R119: 11 lajes por ramo, 44 campos pareados iguais (cargas Q/G2, espessura e elevação). R122: coordenadas e conexões geométricas coincidem no pórtico e nas grelhas exportadas. R123: há inversão da ordem I/J em 68 pares únicos do pórtico, 76 da grelha N1 e 159 da N2; isso não é contagem de erros nem prova da causa da direção relativa Y−/Y+. Propriedades/cargas locais não foram transformadas para declarar equivalência mecânica completa.

R127: apoio W17, CAD V14/BIM V2, com seção de 20 × 16 cm, elevação 0 e carga de parede/soma extra exibidas 0. A seção coincide, mas sua capacidade sob o conjunto completo de ações não foi aprovada. A opção de edição “Manter seção constante” difere visualmente e foi preservada.

## Análise parcial e ensaio de parede

| Revisão | Adicional exibido, ambos ramos (tf) | Total vertical exibido, ambos ramos (tf) |
|---|---:|---:|
| 116 | 10,56 | 105,14 |
| 121 | 12,51 | 107,09 |

A R116 é a referência parcial anterior. A R121 é um ensaio da W03 não aceito como lançamento definitivo. O aumento exibido de 1,95 tf é coerente com 1,9536 tf na exportação R122, que aplica a carga em 4,40 m entre eixos; a faixa livre tem 4,20 m. A consulta R125 confirmou 444 kgf/m ↔ 4,44 kN/m na exibição nativa, sem editar a carga, e restaurou a unidade original. Isso identifica a convenção observada, sem afirmar conversão SI exata ou calibração universal.

Na R126, tentativas de nós junto à face do pilar foram recusadas; um controle no meio do vão foi descartado ao fechar sem salvar. Não houve aplicação de carga ou tentativa BIM equivalente. A delimitação continua pendente. Não se adotou a intensidade reduzida ou a viga inteira para forçar igualdade do resumo.

O Gama-Z X+ exibido na R121 chegou a 1,10, igual ao limite mostrado. Valor arredondado no limite não é aprovação. Permanecem a indicação relativa CAD Y−/BIM Y+ e a necessidade de esclarecer sua causa. As análises parciais não abrangem resistência completa, flechas de lajes, fissuração e todos os carregamentos.

## Tempos e esforço

O inventário R124 reúne 203 candidatos: 162 com duração, 26 sem duração principal e 15 contêineres, com 23 pares sobrepostos. É a fotografia até aquela revisão. A tabela abaixo acrescenta quatro intervalos observados posteriormente, sem refazer a contagem de candidatos ou somar o histórico:

| Revisão | Ramo | Escopo | Intervalo observado |
|---|---|---|---:|
| R125 | BIM | Consulta de unidades: segmento retomado | 2 min 31,343 s |
| R126 | CAD | Tentativa de delimitação não aceita | 12 min 27,789 s |
| R127 | CAD | Consulta da seção do apoio W17 | 2 min 27,423 s |
| R127 | BIM | Consulta da seção do apoio W17 | 2 min 13,586 s |

Os intervalos incluem navegação, leitura, pesquisa, erro de interface ou evidências, conforme cada JSON. A retomada R125 exclui a consulta preliminar e espera da ajuda. A tentativa R126 não foi concluída como lançamento e não possui medição BIM correspondente. As consultas R127 tiveram caminhos de seleção distintos. Não sustentam ranking, tempo final de fluxo ou economia percentual. Intervalos de processamento contidos nas sessões não são somados novamente.

A atuação da IA compreende código, artefatos, pesquisa, operação e auditoria. A intervenção humana compreende premissas, decisões e ações registradas nos aplicativos. Tempo ativo humano, inferência isolada, tokens e custo não foram reconstruídos por quantidade de mensagens ou arquivos. **Tempo final CAD/BIM, esforço isolado da IA e ranking continuam desconhecidos.**

## Frentes para fechar o estudo

| ID | Frente | Estado | Critério para encerrar |
|---|---|---|---|
| F01 | Delimitar ações nas faixas reais de paredes | pendente | Extremos e intensidade preservados após salvar/reabrir e conferidos na representação analítica dos dois ramos. |
| F02 | Completar paredes, aberturas, vergas e caminho de carga W08 | parcial | Todas as parcelas e apoios definidos, lançados e relidos sem duplicar concreto ou cargas existentes. |
| F03 | Resolver reservatório de 1.000 L, posição/base/acesso e cargas cheio/vazio | pendente | Compatibilização física e apoio definidos com pesos documentados e casos nativos verificados. |
| F04 | Completar escada, guarda-corpo e cargas remanescentes | pendente | Modelo/reação documentados e parcelas aplicadas sem duplicar ações de lajes. |
| F05 | Validar vento local, manutenção localizada e conjunto completo de combinações | parcial | Parâmetros e todos os casos/combinações justificados e conferidos nos dois receptores. |
| F06 | Concluir ELU/ELS e revisar seções preservando alturas arquitetônicas | pendente | Entradas completas, esforços/resistência/flechas/fissuração/estabilidade verificados e revisões relidas. |
| F07 | Sincronizar Revit/AutoCAD com a hipótese técnica aceita | pendente | Nova transferência de fontes congeladas, com geometria/propriedades e ocorrências auditadas. |
| F08 | Executar comparação prospectiva de tempos e fechar pacote de resultados | pendente | Mesmo escopo inicial/final, pausas e esforço humano/IA/interface registrados; tabelas finais vinculadas às evidências. |

As oito frentes são agrupamentos de trabalho, não erros por ramo. Uma conferência parcial concluída não encerra toda a frente. Fundações permanecem fora do escopo pela ausência de sondagem; apoios idealizados devem continuar explicitados.

O JSON conserva os hashes das fontes e os limites. Não se executou nova importação, cálculo, alteração de arquivos nativos ou edição acadêmica nesta consolidação. Saída local: `D:\TCC\outputs\Resultados-H03-R128-PARCIAIS-NAO-EXECUTAR`.

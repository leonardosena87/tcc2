# H03/R206 — Ensaio de delimitação e registro dos tempos recentes

Esta etapa abriu a cópia CAD derivada da R204 e ampliou o croqui do patamar. A inserção de nó em (450, 0) cm voltou a informar que existe um nó na posição, mesmo após alternar a captura personalizada. Uma tentativa posterior de entrada numérica não ficou confirmada na tela. A edição por acessibilidade retornou elemento indisponível. O comando foi cancelado. A causa da recusa da carga parcial ainda precisa ser estabelecida no croqui. A comparação dos hashes dos dois arquivos PRJ com suas bases R204 confirmou igualdade ao final da consulta.

## Tempos registrados nos cenários recentes

| Revisão | Escopo da execução | CAD | BIM | Dimensionamento incluído CAD/BIM |
|---|---|---:|---:|---:|
| R196 | Parede W08 integral | 7 s | 7 s | 2 / 2 s |
| R201 | Verificação de deslocamentos com rigidez fissurada e dimensionamento selecionado herdado | 9 s | 9 s | 2 / 2 s |
| R205 | Verificação de deslocamentos com rigidez fissurada e dimensionamento integral | 10 s | 10 s | 3 / 3 s |

Cada linha representa uma execução por fluxo, em um cenário diferente. O dimensionamento está incluído no tempo total. Cada cenário apresenta igualdade dos tempos nativos registrados entre CAD e BIM. A resolução nativa é de um segundo. A preparação, a modelagem, a exportação/importação, o diagnóstico, a edição, as intervenções humanas e as falhas de automação requerem seus próprios registros.

A soma das linhas mistura diferentes hipóteses e opções de análise. Ela não representa o tempo completo de nenhum dos dois fluxos. Tampouco se utiliza a média destas revisões como estimativa de uma execução padronizada. O JSON anexo mantém os cenários e suas fontes separados.

## Registro para a discussão

A W08 foi cadastrada no Eberick nos dois fluxos com a mesma intensidade e a mesma extensão analítica excedente. Trata-se de uma ocorrência comum de lançamento. Essa ocorrência deve ser identificada por parede, revisão de origem, sintoma e correção realizada, evitando contá-la novamente a cada reprocessamento. O erro D16 da V2 no BIM depende da continuidade e da segmentação das vigas na comparação com o CAD. A comparação final de retrabalho depende de aplicar uma regra de equivalência geométrica e de registrar o tempo de cada correção aceita.

## Trabalho aberto

A carga parcial da W08 ainda exige edição aceita e confirmação por nova exportação analítica. A V1 exige verificação dos esforços simultâneos nos dois eixos. A solução da V2 precisa respeitar as alturas arquitetônicas e a transmissão aos pilares. O apoio do pano inferior da W08 continua pendente. O reprocessamento final e a consolidação dos tempos completos dependem dessas etapas.

[Procedimento AltoQi para delimitar carga por nós na viga](https://suporte.altoqi.com.br/hc/pt-br/articles/360046158854)

# H03/R80 — unidades da origem, sólidos e grupos de detalhamento

Auditoria de correspondência, sem alteração de qualquer projeto nativo ou monografia. Usa proposta R43, geometria IFC R56/preservação R57, mapa físico R72 e mensagens reais do processamento exploratório R79.

## Resultado

As **29 unidades lógicas de viga da proposta** (15 em N1 e14 em N2) estão representadas em ambos os receptores. Existem **32 sólidos** por ramo (17 em N1 e15 em N2). Os agrupamentos nativos para cálculo/detalhamento são diferentes: **CAD30** (15+15), **BIM20** (12+8). Confirmou-se cada par pavimento/nome desses grupos nas mensagens nativas R79. Assim,29,32,30 e20 medem objetos diferentes; não representam contagens intercambiáveis de erro, operação ou perda.

A igualdade geométrica dos sólidos não garante que o agrupamento por viga, orientação, seção de apoio, critérios de detalhamento ou vínculo analítico seja o mesmo. Os registros históricos que denominam29 vigas lógicas nos receptores devem ser lidos como29 unidades da proposta representadas, e não como confirmação de29 grupos nativos. Essa distinção complementa os resultados anteriores e não apaga a evidência de disponibilidade inicial nem as complementações realizadas.

## Critério de correspondência

Para cada sólido de viga ortogonal, comparou-se eixo maior XY, centro transversal e cota superior com os segmentos da proposta. Exigiu-se um único candidato por sólido. Na contenção longitudinal usou-se margem declarada de0,20m para extremidades geométricas/apoios; essa margem é um parâmetro de associação e **não tolerância construtiva ou autorização de desalinhamento**. Tolerância numérica10⁻⁵m. Registraram-se afastamentos brutos das extremidades. Largura coincidiu; alturas N1 coincidiram com a proposta e N2 com a alteração30cm de R56. A altura antiga de N2 não foi usada para rejeitar um sólido atualizado.

Todas as32 correspondências físicas CAD/BIM previamente estabelecidas em R72 apontaram para a mesma unidade da proposta. A classe+caixa manteve-se como controle independente de nomes. Não se deduziu conectividade analítica, rigidez ou continuidade de armadura da caixa geométrica.

## Grupos que reúnem unidades distintas da proposta

- BIM `N1/V1`: V5-N1, V6-N1; alturas atuais [0.45, 0.55] m.
- BIM `N1/V12`: V11-N1, V12-N1; alturas atuais [0.35, 0.4] m.
- BIM `N1/V2`: V3-N1, V4A-N1; alturas atuais [0.16, 0.45] m.
- BIM `N2/V1`: V5-N2, V6-N2; alturas atuais [0.3] m.
- BIM `N2/V2`: V3-N2, V4A-N2; alturas atuais [0.3] m.
- BIM `N2/V4`: V1-N2, V2-N2; alturas atuais [0.3] m.
- BIM `N2/V5`: V7-N2, V8-N2; alturas atuais [0.3] m.
- BIM `N2/V6`: V10-N2, V9-N2; alturas atuais [0.3] m.
- BIM `N2/V8`: V11-N2, V12-N2; alturas atuais [0.3] m.

## Unidades da proposta divididas entre grupos nativos

- V2-N2: CAD N2/V3, N2/V4_1; BIM N2/V4.

## Correspondência completa

| Origem | Grupos CAD | Grupos BIM |
|---|---|---|
| V1-N1 | N1/V1 | N1/V5 |
| V2-N1 | N1/V4 | N1/V6 |
| V3-N1 | N1/V2 | N1/V2 |
| V4A-N1 | N1/V14 | N1/V2 |
| V4B-N1 | N1/V13 | N1/V3 |
| V5-N1 | N1/V3 | N1/V1 |
| V6-N1 | N1/V5 | N1/V1 |
| V7-N1 | N1/V6 | N1/V7 |
| V8-N1 | N1/V10 | N1/V8 |
| V9-N1 | N1/V7 | N1/V9 |
| V10-N1 | N1/V11 | N1/V10 |
| V11-N1 | N1/V8 | N1/V12 |
| V12-N1 | N1/V12 | N1/V12 |
| V13-N1 | N1/V9 | N1/V11 |
| V15-N1 | N1/V15 | N1/V4 |
| V1-N2 | N2/V1_1 | N2/V4 |
| V2-N2 | N2/V3, N2/V4_1 | N2/V4 |
| V3-N2 | N2/V2_1 | N2/V2 |
| V4A-N2 | N2/V2 | N2/V2 |
| V4B-N2 | N2/V13_1 | N2/V3 |
| V5-N2 | N2/V3_1 | N2/V1 |
| V6-N2 | N2/V5_1 | N2/V1 |
| V7-N2 | N2/V6_1 | N2/V5 |
| V8-N2 | N2/V10_1 | N2/V5 |
| V9-N2 | N2/V7_1 | N2/V6 |
| V10-N2 | N2/V11_1 | N2/V6 |
| V11-N2 | N2/V8_1 | N2/V8 |
| V12-N2 | N2/V12_1 | N2/V8 |
| V13-N2 | N2/V9_1 | N2/V7 |

## Ensaio necessário para o D16

Em N1, BIM `V2` reúne as unidades `V3-N1` e `V4A-N1`, enquanto CAD usa `V2` e `V14`. O primeiro trecho tem20×45cm e o segundo20×16cm. O D16/A07 foi observado no detalhamento agrupado BIM. Para testar a contribuição do agrupamento, criar cópia isolada e separar a V2 BIM no apoio comum, mantendo seções, coordenadas, cargas, vínculos e limites. Reprocessar com as mesmas opções e comparar nós/armadura/status com a base congelada. Separar nomes/grupos não autoriza rotular a ligação ou mudar rigidez. Se a ferramenta nativa também alterar conectividade, registrar o efeito e não tratar o teste como variável única.

O agrupamento inicial pode resultar de importação, reconstrução ou edição posterior; esta auditoria não identifica sozinha sua origem causal. O D16 continua registrado como ocorrência diferencial a investigar, sem ser convertido em defeito comprovado de transferência. Outros agrupamentos devem ser padronizados no ensaio final conforme uma regra comum previamente definida. Contagem de correções exige ocorrência física/campo/regra e estado de aceitação; não se utiliza30 versus20 como pontuação de qualidade.

Não ocorreu nova exportação ou cálculo nesta revisão. Não se mediu duração retrospectiva. O ensaio final continua dependente de cargas completas, critérios iguais e medição prospectiva pareada conformeR69.

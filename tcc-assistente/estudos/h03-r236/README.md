# H03/R236 — marco comum de vigas e pilares no Eberick

Conferência realizada em 6 de novembro de 2026, somente leitura, sobre os controles IFC4 dos projetos salvos: CAD R235 e BIM R231. Os modelos e seus arquivos nativos não foram alterados; registraram-se hashes antes e depois da análise. Os resultados completos, incluindo a correspondência de cada elemento, estão em `D:/TCC/outputs/H03-R236-COMPARACAO-GEOMETRICA-CAD-BIM-NAO-EXECUTAR/R236-comparacao.json`.

## Resultado da comparação

| Indicador | CAD R235 | BIM R231 |
|---|---:|---:|
| Identidades de pilar da autoria, conforme auditorias de origem | 23 | 23 |
| Identidades de viga da autoria, conforme auditorias de origem | 32 | 32 |
| Trechos nativos de pilar no controle IFC4 | 35 | 35 |
| Trechos nativos de viga no controle IFC4 | 35 | 35 |
| Trechos com correspondência geométrica única no outro fluxo | 70/70 | 70/70 |
| Pavimentos com correspondência única | 4 | 4 |

Verificou-se que cada geometria é uma malha retangular fechada. A associação exige a mesma classe IFC e a coincidência dos seis limites da caixa tridimensional, com tolerância computacional de 0,2 mm. Conferiu-se a associação nos dois sentidos, sem reutilizar um elemento. A maior diferença foi **0,01765 mm**, no arredondamento de cota do patamar. Essa tolerância não constitui limite normativo de execução.

Nenhum par apresentou diferença nos conjuntos de propriedades exportados, após excluir apenas o identificador STEP auxiliar `id`. Coincidiram, entre outros campos presentes, a classe C-25 e o cobrimento de 3 cm. Isso demonstra igualdade dos dados disponíveis nesses controles, não a transmissão integral de todos os parâmetros da autoria: parte das configurações foi aplicada no receptor e nem toda informação interna aparece no IFC.

Os nomes nativos diferem em **64 dos 70 pares**. A comparação geométrica permitiu manter a rastreabilidade por GUID e nome de cada fluxo sem renumerar os modelos. Essa diferença de identificação não foi contada como erro estrutural. Os quatro níveis também conservam nomenclaturas diferentes, com associação biunívoca por posição dos elementos.

## O que esse resultado permite concluir

A reconstrução CAD R232–R235 e a recepção BIM corrigida R231 atingiram o mesmo marco geométrico de vigas e pilares. O ramo CAD foi preenchido a partir dos DXF de autoria. O ramo BIM exigiu tratamento adicional dos corpos IFC: 13 vigas e 5 trechos de pilar recompostos ao longo das etapas R230–R231. A comparação final foi feita depois desses tratamentos; portanto, não representa recepção automática sem correções.

O método evita concluir equivalência apenas pela contagem: conferiu-se cada sólido, seção, posição e conjunto de propriedades. Por outro lado, a igualdade de sólidos/propriedades exportadas não demonstra igualdade da conectividade analítica, das combinações ou das armaduras. Nenhum desses dois receptores foi aprovado estruturalmente nesta conferência.

## Tempos observados e limites de comparação

| Registro | Duração bruta | Limite principal |
|---|---:|---|
| CAD R232 — lançamento de pilares | 15 min 43,3 s | Exclui preparação, exportação e auditoria posteriores |
| CAD R232 — correção de continuidade | 50,8 s | Intervenção complementar, não repetição do fluxo |
| CAD R233 — vigas N2 | 32 min 25,1 s | Inclui interrupção e retomada |
| CAD R234 — vigas N1 | 39 min 17,9 s | Inclui interrupções; duração obtida dos horários ISO |
| CAD R235 — viga do patamar | 79 min 49,8 s | Inclui interrupção; inadequado para ranking |
| CAD R235 — viga da base | 5 min 41,4 s | Inclui recuperação de entrada e consultas da interface |
| BIM R231 — confirmação do IFC até salvar | 2 min 33,1 s | Exclui diagnóstico, preparação, programação e auditoria |

Os registros originais permanecem nas respectivas pastas de revisão. Não se calculou ganho percentual nem se apresentou a soma desses intervalos como tempo total de produção. O escopo e a continuidade de observação são diferentes. A etapa R230 do BIM foi um ensaio anterior, com entrada diferente; a R231 não é uma repetição independente. O tempo de preparação automática da R231, de 2,36 s, também não representa o esforço total de desenvolver o tratamento do IFC.

## Próximo marco necessário

Para comparar o receptor completo, faltam nesta rodada lajes, escada, definição dos apoios/vínculos e aplicação das cargas. A base da escada no CAD ainda apresenta a pendência de apoio idealizado. As revisões calculadas R227 são anteriores e permanecem separadas, com seus avisos e verificações complementares. Este marco não substitui esses modelos e não autoriza execução da estrutura.

O programa `comparar.py` usa os arquivos efetivos e produz os resultados públicos resumidos e a matriz local completa. A auditoria não utiliza nomes iguais como requisito de associação, nem promove campos de carga zero a comprovação de levantamento de cargas concluído.

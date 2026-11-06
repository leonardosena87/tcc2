# R227 — Ensaio de continuidade das barras superiores da cobertura

Em 6 de novembro de 2026, salvaram-se duas cópias independentes da R224 no Eberick 2025 Infinity. Na guia Nó da viga de cobertura V13_1 no CAD e V3 no BIM, selecionaram-se duas barras superiores Ø10 mm nos dois apoios. A escolha experimental manteve a geometria de concreto de 20 × 30 cm, o vão livre de 2,85 m e o topo em +6,39 m. Os valores exibidos nos apoios permaneceram em −13,16 e −8,01 kN·m. Reabriu-se cada cópia, recalculou-se e gerou-se novamente o detalhamento. Os relatórios anteriores mantiveram seus arquivos originais.

O detalhe nativo passou a apresentar duas barras superiores Ø10 contínuas, comprimento indicado de 375 cm, projeção longitudinal de 329 cm e ganchos indicados de 29 e 22 cm. A barra superior curta do arranjo anterior deixou de aparecer. Mantiveram-se duas barras inferiores Ø8 e 19 estribos Ø6,3 c/15. O Eberick continuou exibindo o Aviso 08 em ambas as cópias, que exige avaliação da ancoragem e da distribuição da armadura devido à carga negativa. [Orientação do fabricante](https://suporte.altoqi.com.br/hc/pt-br/articles/360003993253).

| Resultado do processamento | CAD | BIM |
|---|---:|---:|
| Duração nativa, com resolução de 1 s | 10 s | 10 s |
| Total vertical exibido | 114,47 tf | 114,47 tf |
| Gama-Z máximo exibido | 1,06 | 1,06 |
| Deslocamento horizontal máximo por vento exibido | 0,15 cm | 0,16 cm |
| Cortante de cálculo da viga de cobertura | 27,10 kN | 27,11 kN |
| Aberturas de fissuras impressas, no vão e nos dois apoios | 0,05 / 0,08 / 0,03 mm | 0,05 / 0,08 / 0,03 mm |

O processamento executou análise estática, dimensionamento geral e determinação dos deslocamentos do pórtico e das lajes com rigidez fissurada. As mensagens nativas registraram sucesso automático para os elementos de superestrutura e 14 sapatas com erro em cada cópia. O escopo acadêmico adota apoios idealizados. A relação entre carga total e área aproximada continuou sinalizada pelo Eberick nos dois modelos. O tempo inclui a rodada de cálculo e dimensionamento no receptor. O cronômetro de ponta a ponta, o tempo ativo exclusivo e a contagem de correções atribuíveis à transferência permanecem fora desta rodada. A edição da armadura constitui a mesma revisão de dimensionamento em ambos os fluxos.

## Ancoragem superior

A triagem adotou a face do apoio como origem, centro da barra a 41,3 mm da face exterior e raio de eixo de 30 mm. Supôs boa aderência e cobrimento normal ao gancho de pelo menos três diâmetros. A projeção horizontal estimada até o início da curva é de 228,7 mm no apoio esquerdo de 30 cm e 128,7 mm no direito de 20 cm. Para as áreas de flexão indicadas nos relatórios (1,20 e 0,72 cm²), a triagem resulta em 201,4 e 120,9 mm, respectivamente. No lado direito, usar a área final impressa de 0,90 cm² como sensibilidade eleva o comprimento a 151,1 mm. Em má aderência, a triagem falha em ambos os lados já para as áreas de flexão. Referência consultada no exemplar local: ABNT NBR 6118:2026, 9.3, 9.4.2 e 18.3.2.4.1. [Catálogo ABNT](https://www.abntcatalogo.com.br/default.aspx?P=C0W59PS6VY3A).

O apoio direito tem margem pequena e sensível à posição real da gaiola e à hipótese de aderência. A sobreposição espacial dos ganchos superiores e inferiores, o confinamento no pilar, a transferência de esforços no nó e a verificação da envoltória negativa no vão seguem em aberto. A continuidade foi confirmada no detalhamento nativo. A R227 permanece como ensaio acadêmico, sem liberação executiva.

Pasta local `D:/TCC/outputs/H03-R227-COBERTURA-CONTINUIDADE-NAO-EXECUTAR`. O script `consolidar.py` lê os relatórios recém-emitidos, identifica as hipóteses da triagem, valida os CRCs dos PRJ e compara os hashes com as referências R224. A opção `--backup` preserva os dois projetos fechados, relatórios e capturas em um ZIP verificado por hash. Os arquivos nativos e as capturas permanecem no armazenamento local.

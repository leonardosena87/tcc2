# H03/R182 — diagnóstico nativo de dimensionamento

Estudo preliminar, não executar. Processou-se o dimensionamento em duas cópias independentes dos receptores R178. Preservaram-se 24 arquivos da fonte CAD e 31 da fonte BIM, conferidos por SHA-256. Não se alteraram nesta etapa as seções, os apoios, as bitolas disponíveis ou os limites de dimensionamento para eliminar mensagens de erro.

## Escopo do ensaio

Selecionaram-se vigas, pilares e lajes de N1 e N2, além de escadas de N1. Não se selecionou N0 nem fundações, reservatórios, muros ou alvenaria. Ativou-se o dimensionamento ELU dos elementos selecionados e manteve-se o cálculo de deslocamentos do pórtico com rigidez configurada. Permaneceram desativados o cálculo de flechas das lajes, a análise dinâmica, as etapas construtivas e a verificação de limites de redistribuição em nós semirrígidos. Portanto, o ensaio não encerra a verificação dos estados-limite.

Na abertura da cópia CAD apareceu um aviso do Eberick sobre possível inconsistência na última edição. Executou-se a verificação nativa apenas nessa cópia e depois o processamento. O aviso não apareceu na abertura da cópia BIM. A preparação e a verificação de integridade não integram os tempos nativos abaixo. A cópia CAD foi salva, fechada e reaberta, com resultados de escada ainda presentes. As fontes R178 não foram substituídas por essas cópias. Ainda é necessário conferir a retenção de geometria e cargas mediante novas exportações das cópias R182; os IFCs/SAP herdados dentro delas continuam sendo arquivos anteriores, não exportações deste ensaio.

## Resultados efetivamente observados

O relatório Mensagens da análise apresentou as seguintes contagens. A expressão “com sucesso” é a classificação do relatório e pode incluir avisos; não significa revisão de armaduras ou aprovação estrutural.

| Pavimento/categoria | CAD — com sucesso / com erro | BIM — com sucesso / com erro |
|---|---:|---:|
| N2 — pilares | 11 / 0 | 11 / 0 |
| N2 — vigas | 15 / 0 | 9 / 0 |
| N2 — lajes | 5 / 0 | 5 / 0 |
| N1 — pilares | 11 / 0 | 11 / 0 |
| N1 — vigas | 16 / 0 | 11 / 1 |
| N1 — lajes | 9 / 0 | 9 / 0 |

A leitura específica da planilha **Escadas → Positivo** identificou **LE1 calculado, LE2 calculado e LE3 com Erro D31 em ambos os receptores**. No resultado da armadura de LE3, todas as bitolas exibidas — 6,3; 8; 10; 12,5 e 16 mm — indicaram **A11: largura do apoio insuficiente**. Assim, o resumo de lajes do relatório não pode ser usado para concluir que toda a escada foi dimensionada com sucesso. Ainda se deve identificar o bordo/apoio e conferir o comprimento disponível e a condição de ancoragem. Não se atribuiu o erro automaticamente a um determinado apoio sem essa leitura.

No BIM, o Status dos elementos identificou **V2 de N1, D16, nó 2**. A planilha Nó mostrou P5, Md = −36,90 kN·m; a planilha Seção mostrou trechos de 20 × 16 e 20 × 45 cm. O resultado da armadura negativa indicou **A07: taxa de armadura maior que a configurada** para 8; 10; 12,5; 16 e 20 mm. O valor do limite configurado ainda não foi relido. Não se elevou esse limite nem se aumentou a seção nesta revisão.

O patamar e o lance superior receberam resultados experimentais de armadura, que permanecem sem revisão. O lance inferior segue sem solução de armadura na condição ensaiada. As capturas mostram resultados de diagnóstico, não detalhamento liberado para execução.

## Agrupamento das vigas e limite da comparação

Os relatórios contêm 31 vigas no CAD e 21 no BIM. Essa diferença não demonstra falta de dez vigas físicas: os agrupamentos e nomes diferem. Para localizar a V2 problemática, conferiu-se o IFC **de referência R178**, anterior ao diagnóstico, e não uma nova exportação R182. Os dois prismas de V2 no N1 do BIM correspondem aos sólidos CAD V2 e V14: Y entre 3,80 e 4,00 m; primeiro trecho X entre 0,10 e 4,30 m, seção 20 × 45 cm; segundo X entre 4,50 e 6,40 m, seção 20 × 16 cm; topo em +3,20 m.

A equivalência desses prismas foi verificada pelos oito vértices, fechamento das arestas, localização dos triângulos nas seis faces e área de cada face, permitindo diagonais de triangulação diferentes. A precisão de comparação de 10⁻⁷ m é computacional e não tolerância de obra. Não se afirmou igualdade integral dos modelos nativos. A relação causal entre agrupamento e erro de armadura ainda precisa ser verificada, incluindo continuidade, seções, materiais, vínculos e critérios de dimensionamento. Não se pode apresentar o único erro de viga do BIM como superioridade do CAD antes dessa reconciliação.

## Tempos medidos

| Medição do relatório nativo | CAD | BIM |
|---|---:|---:|
| Total do processamento deste ensaio | 7 s | 7 s |
| Dimensionamento, já incluído no total | 2 s | 2 s |

Há uma observação por receptor, executada sequencialmente no mesmo computador, CAD antes de BIM. Não se calculou média, significância ou vantagem de produtividade. Os 2 s não devem ser somados novamente aos 7 s. O escopo difere da análise parcial R178, de 5 s/6 s, portanto não se substituíram essas medições históricas.

Também se registrou UTC imediatamente antes do OK e na primeira confirmação de término: 21,613 s no CAD e 19,525 s no BIM. Esses intervalos incluem latência de ferramentas e a retomada da observação; não representam tempo ativo de trabalho, duração interna do cálculo ou tempo completo dos fluxos. Não foram usados para classificar desempenho. O inventário histórico R180 permanece separado e não foi somado a estes registros.

## Validação, referências e continuidade

O consolidado preserva os DOCX nativos, o texto extraído, a seleção de classes, as opções, as capturas dos erros e os hashes dos projetos salvos. Nove testes verificam interpretação de nomes e contagens, omissões, rejeição de estados desconhecidos, tempos contidos no total, impossibilidade de aprovar a escada pelo resumo e identificação de prismas com triangulação diferente. Esses testes são de leitura de evidências; não são ensaios estruturais.

A consulta oficial do AltoQi orienta examinar os resultados por bitola para discriminar a causa de [D16](https://suporte.altoqi.com.br/hc/pt-br/articles/360000680694) e [D31](https://suporte.altoqi.com.br/hc/pt-br/articles/360000681913). Aplicou-se essa consulta às planilhas efetivamente abertas, sem adotar automaticamente soluções ilustradas para outros projetos.

O próximo trabalho é conferir o apoio/ancoragem de LE3 nos dois receptores e reconciliar a V2 BIM com V2/V14 CAD e seus critérios. Permanecem a compatibilização de acabamentos e cota inferior, o conflito V16/J4, a justificativa dos apoios idealizados, as cargas provisórias, o ELS e o detalhamento, além da consolidação final de tempos e retrabalho com fronteiras equivalentes. O projeto escrito não foi alterado.

# H03/R64 — conferência individual das cargas permanentes da cobertura

ESTUDO PARCIAL — NÃO EXECUTAR. Conferiram-se 13 pontos em cada ramo no Eberick 2025 Infinity, em cópias independentes dos congelados R63. As 26 leituras confirmaram coordenadas X/Y, ação Adicional, Fz negativo e Fx/Fy/Mx/My/Mz nulos. Todas corresponderam ao plano e as leituras CAD/BIM coincidiram entre si.

## Resultado verificável

| Ponto | X (cm) | Y (cm) | Fz pretendido (kN) | CAD exibido (kN) | BIM exibido (kN) |
|---|---:|---:|---:|---:|---:|
| RC01 | 110 | 0 | -1.419551 | -1.41955 | -1.41955 |
| RC02 | 330 | 0 | -1.419551 | -1.41955 | -1.41955 |
| RC03 | 547.5 | 0 | -1.387289 | -1.38729 | -1.38729 |
| RC04 | 110 | 390 | -2.566112 | -2.56611 | -2.56611 |
| RC05 | 330 | 390 | -2.566112 | -2.56611 | -2.56611 |
| RC06 | 547.5 | 390 | -2.507791 | -2.50779 | -2.50779 |
| RC07 | 732.5 | 390 | -0.807804 | -0.807804 | -0.807804 |
| RC08 | 887.5 | 390 | -0.807804 | -0.807804 | -0.807804 |
| RC09 | 110 | 705 | -1.146561 | -1.14656 | -1.14656 |
| RC10 | 330 | 705 | -1.146561 | -1.14656 | -1.14656 |
| RC11 | 547.5 | 705 | -1.120503 | -1.1205 | -1.1205 |
| RC12 | 732.5 | 705 | -0.807804 | -0.807804 | -0.807804 |
| RC13 | 887.5 | 705 | -0.807804 | -0.807804 | -0.807804 |

A soma das forças pretendidas arredondadas é 18,511247 kN, descendente, somente nos trechos A1/A2 da R60. A tolerância de 0,0000051 kN atende à precisão da janela observada; por exemplo, -1,120503 aparece como -1,1205. Não se concluiu que o valor interno foi truncado nem se alteraram forças para reproduzir a janela. Não houve edição de engenharia, novo processamento, mudança de unidade ou correção nesta revisão. As consultas foram encerradas por Escape, inclusive o diálogo do nó.

Os pontos CAD RC07/RC08/RC13 corrigidos na R63 e RC12 corrigido na R62 persistiram. A conclusão se limita ao lançamento G consultado; não comprova equivalência integral da transferência DWG/IFC ou de esforços, armaduras, combinações e demais cargas. Não se atribuem correções anteriores a defeito DWG. A genealogia é AutoCAD 2027/DWG2D e Revit 2027.2/IFC adaptado; não se operaram esses dois programas nesta auditoria.

## Qualidade dos registros

Cada leitura válida possui arquivo próprio *-leitura-UI.txt e linha estruturada em R64-leituras-CAD/BIM.json. Comparou-se por coordenadas, sem depender apenas da posição visual ou do nome de uma viga. Preservaram-se três capturas iniciais BIM com sufixo INVALIDA: um vínculo de estado do runtime apontava a observação anterior e registrou a árvore incorreta. Foram excluídas da análise e substituídas por consultas reais posteriores com estado global explícito; não se contaram como divergências estruturais ou defeitos IFC. Essa recuperação é esforço de instrumentação da IA/interface.

Verificaram-se por SHA-256 84 arquivos R63 protegidos. Após fechar cada projeto, verificou-se a integridade ZIP dos PRJ e congelou-se o conjunto com seus arquivos associados. Igualdade binária do PRJ em relação à R63: CAD=True, BIM=True; igualdade dos conteúdos descompactados: CAD=True, BIM=True. Arquivos auxiliares de interface podem ser gravados pelo Eberick; não se afirmou que todo arquivo nativo permaneceu idêntico. Nenhuma monografia, RVT ou DWG foi editada.

## Tempos prospectivos e esforço assistido

CAD: 33 min 39.634 s, de 2026-10-29T21:27:05.417Z a 2026-10-29T22:00:45.051Z. BIM: 52 min 36.698 s, de 2026-10-29T20:34:08.619Z a 2026-10-29T21:26:45.317Z. Os JSON preservam início/fim UTC e duração bruta. São intervalos de auditoria assistida, incluindo navegação, raciocínio, latência, recuperação de captura e continuidade entre mensagens; não medem tempo de transferência ou solver. O BIM incluiu a recuperação das capturas iniciais inválidas. Não se isolou tempo humano ativo, esforço cognitivo da IA, tokens ou custo. Não se calcula vantagem percentual nem vencedor dos fluxos com esses intervalos. O ensaio final exige tarefas pareadas, entradas congeladas, mesmos critérios de início/fim e separação entre transferência, reconstrução, correções, verificação, espera e intervenção humana.

## Continuidade e limites

A pendência de leitura individual dos 13 pontos G dos dois ramos foi encerrada. Segue pendente a ação variável do telhado, sem duplicar a sobrecarga das lajes, além de P1/varanda, P2/abrigo e sua altimetria, perfis/apoios/ancoragens metálicas, paredes/aberturas, reservatório de 1.000 L/tara/base, escada/bordas, vento/combinações, ELU/ELS e sincronização das origens RVT/DWG. Os avisos e resumos de processamento R63 permanecem históricos; não foram reprocessados nesta revisão. Mantém-se o recorte da superestrutura com apoios idealizados e sem fundações reais dimensionadas. A auditoria de dados não equivale à aprovação da segurança estrutural.

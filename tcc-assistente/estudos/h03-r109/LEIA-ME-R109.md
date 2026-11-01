# H03/R109 — lançamento experimental da varanda nos dois receptores

Aplicou-se a hipótese VP1-A da R108 em duas cópias independentes da R102, pelo próprio Eberick 2025 Infinity. A etapa compreendeu lançamento das cargas, salvamento, fechamento, reabertura e consulta aos seis componentes de cada ação em cada apoio. A hipótese permanece um estudo de sensibilidade, sem dimensionamento dos perfis e das ligações metálicas.

| Posição nominal no N2 (m) | Identificador | Pilar no CAD | Pilar no BIM |
| --- | --- | --- | --- |
| X = 9,65; Y = 3,90 | VP1-01 | P8 | P7 |
| X = 9,65; Y = 7,05 | VP1-02 | P9 | P3 |

A correspondência utiliza posição e identificação nativa, pois a numeração dos pilares difere entre os fluxos. A geometria histórica R56/R60 fundamenta o plano da R108; o diálogo de cada pilar no receptor R109 confirma sua identificação na consulta. A referência de topo de concreto de 6,39 m não define uma nova cota absoluta de telhamento.

| Ação nativa | Fz em cada apoio (kN) | My em cada apoio (kN.m) | Outros quatro componentes |
| --- | ---: | ---: | --- |
| Adicional — parcela G | −0,521164 | +0,260582 | zero |
| Q_TELHADO_MANUTENCAO — parcela QT | −0,393750 | +0,196875 | zero |

O momento acompanha o transporte da força vertical por uma excentricidade de 0,50 m. Os valores de G foram arredondados para seis casas decimais no lançamento. Não se interpretou a força de apoio sobre a estrutura metálica como carga aplicada ao concreto: o plano R108 define os sinais das ações sobre o concreto.

## Resultado da conferência

Confirmou-se igualdade em **24 de 24 componentes pareados**: dois apoios × duas ações × seis componentes. A conferência corresponde a 48 leituras escalares, 24 em cada fluxo. O extrator rejeita ação errada, componente ausente e duplicação contraditória na árvore de acessibilidade; a repetição idêntica do mesmo diálogo é aceita. Dois controles sintéticos verificam essas falhas e a perda do momento ou do sinal vertical. Os testes não constituem verificação de resistência.

Os 33 arquivos fontes da R102 permaneceram com os mesmos hashes. Preservaram-se cópias da primeira gravação e cópias após a consulta final, com verificação de 15 arquivos do CAD e 18 do BIM. O PRJ de cada ramo permaneceu inalterado durante a consulta posterior à gravação. Alterações auxiliares decorrentes da abertura/fechamento constam no resultado JSON. Não se reprocessou a estrutura nesta etapa; resultados anteriores não representam o acréscimo R109.

As outras 13 posições da cobertura A1/A2 não foram selecionadas para o novo lançamento. Não se repetiu a leitura de todas essas posições na R109, portanto não se declara uma auditoria integral das demais cargas nesta revisão.

## Esforço e tempos observados

| Sessão exploratória | Início UTC | Fim UTC | Duração aproximada |
| --- | --- | --- | ---: |
| CAD | 2026-11-01 11:13:42,329 | 2026-11-01 11:35:31,600 | 21 min 49,271 s |
| BIM | 2026-11-01 11:35:56,815 | 2026-11-01 11:48:10,094 | 12 min 13,279 s |

São intervalos de sessão medidos por relógio monotônico e acompanhados por UTC. Incluem observação, interface, captura de evidências e aprendizagem; a sessão BIM inclui consolidação de contexto e retomada. Não medem execução pura, tempo de inferência, tempo ativo humano ou duração total dos fluxos. Não se calcula vantagem percentual nem se classifica o desempenho a partir desses intervalos.

No CAD, a sobreposição do desenho de referência dificultou a seleção do pilar nativo: o duplo clique apresentava uma escolha de poligonais. Ajustou-se a seleção das camadas na própria cópia: CR-Pilares visível e ativo; TCC PILARES visível e inativo. Uma ocultação temporária de CR-Pilares foi revertida antes de salvar. A reabertura permitiu selecionar diretamente P8/P9. Registrou-se esse trabalho como esforço de interface nesta sessão exploratória, sem atribuí-lo automaticamente a defeito de transferência do DWG. No BIM, o duplo clique abriu diretamente P7/P3 nas posições consultadas. A diferença observada não basta para generalizar a produtividade dos fluxos.

## Arquivos e limites

Os projetos permanecem em `D:/TCC/outputs/22-H03-R109-CAD-VARANDA-NAO-EXECUTAR/` e `D:/TCC/outputs/23-H03-R109-BIM-VARANDA-NAO-EXECUTAR/`. Evidências, hashes, resultado e cópias preservadas encontram-se em `D:/TCC/outputs/Varanda-H03-R109-SENSIBILIDADE-NAO-EXECUTAR/`. PRJs e seus auxiliares não integram o repositório público.

P2, reservatório, paredes, escada, vento, combinações e verificações finais continuam pendentes. A R109 não aprova a capacidade do concreto, dos perfis, das ligações ou das ancoragens. Não houve modificação no Revit, AutoCAD ou texto da monografia nesta etapa.

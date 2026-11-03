# H03/R202 — Estudo da V2 preservando alturas

A R202 foi criada como cópia experimental BIM da R201. A V2 reúne um trecho de 20x16 cm e outro de 20x45 cm. A R201 apresenta D16 no apoio intermediário P5, com momento negativo de -36,97 kN.m. A altura reduzida exige rever a concepção e o dimensionamento da ligação.

## Ensaios nativos

| Ensaio | Seções em cm | Resultado após reprocessamento |
|---|---|---|
| 1 | 60x16 e 20x45 | D16 mantido no nó 2, A07 nas bitolas de 8 a 20 mm |
| 2 | 60x16 e 60x45 | D16 eliminado, armaduras calculadas, Aviso 38 nos três apoios |

O segundo ensaio exibe momentos negativos de -9,22, -37,74 e -30,26 kN.m e armaduras superiores de 6 phi 8, 11 phi 10 e 5 phi 10 nos apoios P6, P5 e P4. Os momentos positivos lidos são 3,51 e 55,94 kN.m, com armaduras de 6 phi 8 e 5 phi 10. As alturas e elevações da seção foram preservadas. A largura de 60 cm exige verificar a transferência aos pilares e a compatibilidade com lajes, arquitetura, aberturas e detalhamento das barras.

A árvore completa de status confirma que o segundo ensaio substituiu o erro D16 por três Avisos 38 de condição de apoio da V2. O diagnóstico registra dez vigas N1 com sucesso, duas com avisos e nenhuma com erro. As três peças da escada e as 11 lajes continuam com sucesso. O diagnóstico informa ausência de deslocamentos excessivos. A carga vertical total passou de 1133,09 kN na R201 para 1156,08 kN no segundo ensaio R202, pelo acréscimo de seção. A alteração afeta a distribuição de esforços e as reações.

A largura foi uma hipótese de estudo escolhida pela IA. A seção final exige verificar os apoios e compatibilizar a geometria. A cópia CAD e os arquivos de autoria Revit/AutoCAD ainda correspondem a outras revisões. Portanto, o ensaio R202 ainda exige repetição equivalente no CAD antes da comparação final. A R201 pareada continua como referência controlada da comparação.

## Apoio inferior da escada

O Aviso 19 da V1 no N0 continua pendente nas cópias atuais. A documentação oficial do Eberick informa que a solicitação horizontal introduzida por um elemento inclinado pode gerar flexão oblíqua e que essa componente não integra o dimensionamento usual de vigas. A verificação complementar ou a revisão do caminho da força horizontal precisa integrar o estudo do apoio idealizado. A conclusão do cálculo da escada exige resolver essa frente.

## Evidências

D:/TCC/outputs/Vigas-H03-R202-ESTUDO contém capturas, diagnóstico e mensagens DOCX, suas extrações e a árvore final de status. O JSON identifica o PRJ experimental e seu hash. O tempo nativo da última execução consta do relatório de mensagens. Apenas a segunda execução tem relatório de tempos preservado separadamente. Não se deve atribuir esse tempo ao desenvolvimento completo dos dois ensaios.

Fontes operacionais
- https://suporte.altoqi.com.br/hc/pt-br/articles/360009988354
- https://suporte.altoqi.com.br/hc/pt-br/articles/115004457454

O artigo A07 consultado descreve a taxa de armadura em pilares. Os códigos aplicáveis à V2 foram lidos diretamente no painel nativo. Os limites de pilares citados nesse artigo não foram transferidos ao dimensionamento da viga.

Próxima etapa necessária. Conferir os três apoios da viga larga, escolher e compatibilizar a solução, reproduzi-la no ramo CAD equivalente e verificar a V1 para flexão oblíqua. O estudo continua com as demais pendências R201.

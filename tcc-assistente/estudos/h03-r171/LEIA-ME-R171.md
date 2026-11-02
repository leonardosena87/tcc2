# R171 — apoios idealizados da superestrutura no receptor BIM

Em cópia independente da R169, converteram-se os onze pilares existentes de N0 em pilares de fundação do Eberick. O uso dessa categoria representa os **apoios idealizados do modelo**; não constitui projeto, dimensionamento ou recomendação de fundação. Não há sondagem e não se avaliou a capacidade do solo. Não se criaram novas posições de pilares na edificação.

Adotaram-se os campos conferidos nos onze apoios CAD R165: apoio Rotulado, vínculo do pilar Engastado, altura de barra Fixo 10 cm e df=0. A categoria Sapata é apenas o tipo nativo exigido para representar o apoio. O df=0 e a barra de 10 cm são hipóteses de idealização herdadas, não profundidade executiva ou detalhamento construtivo. Não se dimensionaram esses elementos.

O comando de conversão selecionou onze pilares. A primeira seleção de ícone acionou “Girar pilar”, cancelado antes de selecionar qualquer pilar; em seguida acionou-se a conversão correta. A gravação foi fechada/reaberta e consultaram-se novamente os onze apoios. A verificação nativa de lançamento apresentou “Não foram detectados problemas no lançamento deste pavimento” em **N0, N1 e N2**. Isso resolve os avisos L04/L07 de N0 observados na R170, sem aprovar a análise estrutural.

No IFC de controle, as 33 partes de vigas, os 22 segmentos de pilares e as 11 lajes mantiveram geometria e propriedades exportadas; acrescentaram-se onze IfcFooting de representação de apoio. A aparência desses objetos não é evidência de dimensionamento. O PRJ conserva o nome interno R166; a pasta externa R171 identifica a revisão. Os arquivos-fonte R169 e CAD R165 mantiveram os hashes de controle.

O intervalo **213.651 ms (3 min 33,651 s)** cobre a abertura do croqui N0, navegação, tentativa de comando cancelada, seleção/conversão, edição, primeira verificação e salvar. Exclui preparação da cópia, pesquisa/consultas CAD anteriores, exportação, releitura e auditoria posteriores. Não representa tempo completo do BIM, tempo puro do programa ou inferência isolada da IA.

Não houve processamento ou dimensionamento nesta etapa. A escada ainda falta no modelo de cálculo; permanecem cargas de paredes/cobertura/reservatório, vínculos internos, conflito V16/J4, verificações completas de ELU/ELS e cronômetros pareados finais. A próxima análise, se realizada, deve usar novas cópias e identificar explicitamente as cargas parciais. Não se alterou a monografia ou os arquivos de autoria RVT/DWG. NÃO EXECUTAR.

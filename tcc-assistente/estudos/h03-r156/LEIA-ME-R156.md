# H03/R156 — triagem da chegada e do apoio da escada

A escada de 17 espelhos criada no Revit foi confrontada, por sua definição de superfícies acabadas R153, com a proposta nominal de autoria R83. Esta é uma análise de coordenadas de arquivos, **não uma inspeção dos sólidos nativos ou uma conferência visual completa da R155**. A criação nativa confirmou contagens e cotas, mas não exportou todos os vértices dos sólidos.

## Chegada superior

A chegada acabada está em Y = 2,935783 m. A borda nominal da laje L6 e o eixo da viga V15 da proposta estão em Y = 2,85 m. A diferença é **85,783 mm**. O piso da última pisada, associado ao espelho 16, está em +3,071765 m e entra nas caixas nominais de L6 (cotas +3,06 a +3,20) e V15 (+2,90 a +3,20).

Também se encontrou uma faixa lateral de 24,883 mm dentro da caixa nominal de V13 nas pisadas associadas aos espelhos 15 e 16. A viga tem eixo X = 6,55 m e largura nominal de 20 cm; a borda acabada direita da escada está em X = 6,474883 m. Ao todo, a triagem identificou quatro pares face/elemento em três elementos nominais. O primeiro processamento foi interrompido porque o controle esperava apenas os dois pares da chegada; a leitura completa revelou os dois pares laterais adicionais, que foram incorporados ao relatório, sem exclusão silenciosa.

O script conserva as áreas e intervalos dessas sobreposições. Não se considera automaticamente cada sobreposição um erro: uma ligação de apoio pode exigir contato entre elementos. Também não se considera a interferência resolvida pela simples existência desse contato. É necessário definir a geometria resistente da chegada e a ligação, com o acabamento separado. Há diferença de 5 cm entre o piso acabado superior +3,25 e o topo nominal de concreto +3,20; essa diferença ainda não foi transformada em camada de acabamento ou desconto da escada monolítica.

Essa questão pertence à compatibilização da concepção comum. Não constitui, por si só, perda no IFC, defeito do DWG ou superioridade de um fluxo. Os valores nominais devem ser conferidos nas autorias e nos receptores antes de alterar suas geometrias.

## Patamar e apoios

O patamar acabado está em +1,824118 m; o fundo hipotético seria +1,684118 m com 14 cm e sem desconto de acabamento. Não há viga da proposta R83 na faixa vertical desse patamar. P4 e P10 são colunas existentes próximas à fachada, mas sua presença não demonstra ligação, transmissão de reações ou capacidade para receber a escada. Não foi escolhida silenciosamente uma escada autoportante, nem uma parede de vedação foi promovida a apoio.

A [orientação oficial AltoQi](https://suporte.altoqi.com.br/hc/pt-br/articles/115001700534), consultada nesta revisão, apresenta a sequência de níveis intermediários, estrutura auxiliar, patamares, lances e ajustes geométricos, com exceções conforme o sistema da escada. Portanto, o próximo lançamento precisa explicitar o sistema resistente e seus apoios antes de tratar o modelo como calculável.

Nenhuma dimensão de viga, coluna, laje ou escada foi alterada nesta triagem. Nenhum peso foi aplicado e não houve processamento no Eberick. As três fontes foram verificadas por SHA-256 antes e depois; o tempo do script permanece separado dos tempos CAD/BIM. A figura é própria, gerada dos dados nominais. A monografia não foi editada.

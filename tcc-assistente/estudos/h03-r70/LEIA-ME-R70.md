# H03/R70 — fachada W08 e janela J4 da escada

ESTUDO, NÃO EXECUTAR. A leitura visual da tabela de esquadrias da prancha confirma J4 fixa em alumínio,1,60×3,20m, peitoril0,20m. O corte AA indica piso da escada no térreo em+0,22m, patamar em+1,70m e piso superior em+3,25m. A referência T-J4-01 está na fachada Y0, X4,70..6,30m, dentro da faixa W08. A posição em planta continua aproximada; não foi feita medição executiva.

## Por que W08 não recebe automaticamente a altura das demais paredes superiores

Se o peitoril0,20m for referido ao piso interno+0,22m do corte, o vão ocupa Z0.42..3.62m e atravessa o plano estrutural N1+3,20m. Portanto, a janela não se limita a uma parede iniciada no piso superior. Adotar diretamente a base+3,25m e descontar uma janela de3,20m nessa faixa seria geometricamente incoerente. A base efetiva e o apoio de W08 continuam não resolvidos no modelo; a altura não foi preenchida artificialmente.

Na geometria exportada R56, preservada R57, não há viga N1 cruzando o trecho livre W08 X4,50..6,45/Y0. O teste de caixas também não encontrou viga, pilar ou laje interceptando a caixa condicional do vão J4 em nenhum dos dois ramos. Isso esclarece que o modelo não deve receber uma viga nesse trecho apenas para transformar a parede em um lançamento padrão: uma solução assim precisa preservar J4. Ausência de interseção de caixas não comprova caminho de carga, ligações ou compatibilidade executiva completa.

## Quantificação condicional, sem lançamento

Para compreender a ordem geométrica da fachada, considerou-se somente a faixa livre de pilares1,95m, entre X4,50 e6,45m, da base hipotética+0,22m ao intradorso N2+6,09m. A área bruta seria11.4465m²; o vão J4 representa5.1200m²; a área líquida de alvenaria seria6.3265m². Na composição hipotética1,565kN/m², o peso dessa parcela seria9.900973kN. O número NÃO foi aplicado ao Eberick e não inclui esquadria, verga/contraverga, encontros ou acabamento sobre concreto.

Essa quantificação não define onde o peso entra na estrutura de concreto. Uma fachada contínua com apoio inferior e uma fachada apoiada em verga/viga intermediária produzem caminhos de carga distintos. Nenhuma dessas soluções foi adotada ou dimensionada. O recorte sem sondagem permanece na superestrutura; não se criou fundação real para resolver a parede. No JSON, nativeLoadValue é nulo, nunca zero.

## Continuidade

Definir o suporte e o detalhamento da fachada preservando J4, patamar e passagem da escada; conferir a referência vertical do peitoril e as faces. Quantificar esquadria/vergas e só então decidir as ações sobre o pórtico e o que permanece fora do recorte. Não transformar o peso condicional acima em carga linear uniforme no N1, onde não existe apoio geométrico neste trecho. Não apagar a parede da lista de pendências por ter calculado uma área.

Os recortes originais de leitura ficaram em work, sem copiar a prancha ao repositório público. Os registros R55/R56/R67 continuam históricos. Nenhum PRJ/RVT/DWG, arquitetura original ou monografia foi editado, e não houve processamento ou aprovação ELU/ELS.

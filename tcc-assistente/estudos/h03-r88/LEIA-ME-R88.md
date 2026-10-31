# H03/R88 — volumes, interseções e domínio geométrico ocupado

Esta auditoria de dados compara a proposta nominal R83, os parâmetros de volume da leitura Revit R83 depois de reabrir o arquivo e quatro IFCs já exportados pelo Eberick. Não se abriu nem alterou qualquer projeto nativo. Não se executou análise estrutural ou dimensionamento. Os onze objetos auxiliares IfcFooting de cada IFC foram excluídos do recorte de superestrutura.

## Resultado

| Fonte e critério | Quantidade de unidades/partes | Volume (m³) |
|---|---:|---:|
| Proposta R83, soma das peças nominais isoladas | 62 | 30,4131 |
| Proposta R83, união geométrica sem duplicar encontros | 62 | 27,9009 |
| Revit R83, soma dos parâmetros de volume exportados | 62 | 27,9009 |
| Eberick CAD/R57, soma dos volumes das malhas IFC | 65 | 27,9129 |
| Eberick BIM/R57, soma dos volumes das malhas IFC | 65 | 27,9129 |
| Eberick BIM/R81 controle, soma das malhas IFC | 78 | 27,9129 |
| Eberick BIM/R81 teste, soma das malhas IFC | 78 | 27,9129 |
| União geométrica de cada um dos quatro IFCs | 65 ou 78 | 27,9009 |

Nos quatro IFCs, a diferença simétrica espacial em relação à união dos cuboides nominais da proposta foi **0 m³** no cálculo efetuado. Não se comparou apenas o total: um sólido deslocado pode ter o mesmo volume, mas produzir diferença simétrica diferente de zero. O critério computacional foi fixado em 10⁻⁶ m³, com coordenadas normalizadas a nove casas decimais; ele não é tolerância construtiva ou normativa.

A soma nominal de 30,4131 m³ contém 2,5122 m³ contados repetidamente nos encontros entre peças. Esse número não representa concreto adicional a executar. A soma IFC de 27,9129 m³ supera a união em 0,0120 m³. Localizaram-se quatro interseções entre partes de vigas, de 0,0030 m³ cada, nos quatro checkpoints. Os GUIDs e caixas das interseções ficam no JSON. Elas ocorrem tanto no ramo CAD como no BIM; não são evidência de defeito exclusivo de um intercâmbio. Não se apagaram nem cortaram peças para alterar o resultado.

A soma de interseções par a par não é, em geral, o volume duplicado: encontros triplos podem contá-lo novamente. O volume ocupado foi calculado por união de intervalos; a soma das quatro interseções coincide com a diferença apenas neste conjunto. Há teste específico com três cuboides coincidentes para impedir essa confusão.

## Distribuição por classe

| Classe | Parâmetros Revit R83 (m³) | Malhas Eberick IFC, cada checkpoint (m³) |
|---|---:|---:|
| Pilares | 3,9909 | 4,0854 |
| Vigas | 5,2221 | 7,1388 |
| Lajes | 18,6879 | 16,6887 |

A distribuição do volume entre classes/elementos e as deduções de encontros não são iguais nessas representações. Não se conclui perda de material comparando uma linha dessa tabela sem analisar como os encontros são atribuídos. Para o critério geométrico global de volume ocupado, os quatro IFCs e a proposta nominal conferiram. As 65 e 78 partes são decomposições de exportação distintas; não são 13 novas vigas físicas.

## Método

1. Reconstituíram-se os prismas ortogonais da proposta a partir das coordenadas, largura, altura, espessura e cotas de cada elemento. Vigas inclinadas em planta e geometria não suportada são recusadas.
2. Associaram-se os 62 parâmetros Revit aos elementos da proposta por ID e UniqueId, sem aceitar volume ausente como zero. O exportador arredonda cada parâmetro a seis casas; o limite de arredondamento acumulado considerado foi 62 × 0,5 × 10⁻⁶ m³.
3. Leram-se as malhas IFC em coordenadas globais com IfcOpenShell 0.9.0.post1 e NumPy 2.5.4, usando o runtime Python 3.12.14. Conferiram-se oito cantos únicos, doze triângulos distribuídos nas seis faces externas, arestas fechadas em pares, orientação consistente e igualdade entre volume da malha e volume do cuboide envolvente. A coincidência de volumes sozinha não é o teste de forma. Uma malha não compatível é recusada, sem substituição por uma caixa aproximada.
4. Integraram-se intervalos em Z sobre todas as células definidas pelas coordenadas XY das faces. Não se usa grade de voxels ou resolução de imagem. Calcularam-se união, interseção e diferença simétrica dos domínios.
5. Preservaram-se hashes dos sete arquivos de origem e conferiu-se novamente sua integridade ao terminar. O tempo do script é somente instrumentação desta auditoria, não tempo de produtividade de CAD/BIM.

## Limites de interpretação

A soma dos parâmetros Revit igual à união nominal é um controle de quantidade; sozinha não verifica coordenadas independentes do RVT. Esta rodada usa a leitura histórica R83 e não extrai novas malhas do Revit. O volume da proposta usado como referência CAD é calculado dos dados comuns, não um parâmetro de volume nativo do DWG 2D. Os checkpoints IFC são R57 e R81, não uma nova transferência da autoria R83 ao Eberick.

Igualdade do domínio geométrico ocupado não comprova classificação, vínculos, continuidade analítica, materiais, armaduras, condições de apoio, cargas ou segurança. Não constitui quantitativo executivo, orçamento ou inventário ambiental. As pendências de cálculo e o teste de agrupamento R81 continuam com seus próprios critérios.

## Reprodução

Executar `python -m unittest discover -s <esta-pasta> -p test_volumes.py` para os sete testes do algoritmo. Eles são separados da auditoria dos arquivos reais.

Executar `python auditar_volumes.py D:/TCC <nova-pasta> --ifc-deps D:/TCC/work/ifc/deps` usando Python 3.12 compatível com os binários locais. Não se distribuem bibliotecas instaladas ou arquivos nativos neste diretório público.

O resultado completo entregue localmente está em `D:/TCC/outputs/Quantidades-H03-R88-UNIAO-GEOMETRICA-NAO-EXECUTAR/verificacao-rigorosa/R88-quantidades-geometricas.json`. As pastas preliminares foram preservadas; a versão rigorosa inclui a localização das interseções e a conferência das faces externas.

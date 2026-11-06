# H03/R229 — efeito da normalização dos níveis IFC

O ensaio reaproveitou o IFC4 bruto da R225. A variante derivada manteve N0, patamar, N1 e N2, nas cotas +0,20 m, +1,77411765 m, +3,20 m e +6,39 m. Cinco níveis auxiliares foram retirados. O contêiner da escada mudou do nível virtual de +0,17 m para N0. A posição mundial dos corpos da escada ficou preservada. A releitura conferiu os metadados de 72 elementos, as nuvens de pontos de 71 corpos e 22 conjuntos de propriedades de materiais.

O Eberick recebeu a variante em projeto separado, com a mesma opção de converter vigas e pilares. O projeto foi salvo e reaberto. O relatório nativo manteve os 55 identificadores da R228, com as mesmas classes e os mesmos níveis de origem para vigas e pilares. A comparação geométrica usou as exportações nativas de controle e o IFC R225 congelado.

| Resultado | IFC bruto R228 | IFC com quatro níveis R229 |
|---|---:|---:|
| Origens de viga identificadas no relatório | 32 | 32 |
| Origens de pilar identificadas no relatório | 23 | 23 |
| Trechos de viga no IFC de controle | 33 | 35 |
| Segmentos de pilar no IFC de controle | 67 | 33 |
| Segmentos de pilar de até 5 cm | 23 | 0 |
| Vigas de origem com seção receptora divergente da nominal | 13 | 13 |
| Origens de pilar sem trecho correspondente no IFC de controle | 0 | 2 |
| Tempo corrido assistido da confirmação do IFC ao salvamento | 3 min 53,5 s | 1 min 58,3 s |

Os dois trechos superiores sem corpo correspondente são **P5-N2** (ID 473029, eixo X = 4,40 m) e **P11-N2** (ID 473144, eixo X = 6,55 m), ambos no eixo Y = 3,90 m. No Revit, os eixos nominais vão de +3,20 m a +6,39 m. No IFC de origem, os corpos vão de +3,20 m a +6,25 m. No controle R228, havia corpos nesses eixos entre +3,20 m e +6,25 m. No controle R229, os mesmos eixos apresentam corpos somente até +3,06 m. A identificação textual no relatório permaneceu, apesar da ausência geométrica no IFC de controle. A conectividade analítica ainda requer conferência.

A variante R229 serve como evidência da influência da organização dos níveis. Para a próxima recepção BIM, a prioridade é recuperar a continuidade dos dois pilares superiores e as 13 seções nominais, mantendo separada a verificação dos apoios da escada. O lançamento e a conferência CAD continuam na sua própria cópia de trabalho. Os modelos calculados da R227 permanecem como referência de análise.

A preparação automática levou 2,39 s em uma execução registrada. Esse intervalo ficou fora dos 1 min 58,3 s da recepção. Os tempos incluem interação assistida e latência, com uma execução por variante. A diferença observada ainda não isola a influência da normalização no tempo e não representa duração integral do fluxo.

`preparar_niveis.py` gera o IFC em pasta separada e recusa sobrescrever uma variante. `conferir_receptor.py` audita a recepção e os hashes dos arquivos preservados. Ensaio de interoperabilidade, limitado à superestrutura e sem recálculo desta variante.

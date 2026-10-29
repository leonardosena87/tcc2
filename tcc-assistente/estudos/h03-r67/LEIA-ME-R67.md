# H03/R67 — aberturas e massa condicional das paredes superiores

ESTUDO NÃO APLICADO. NÃO EXECUTAR. Analisaram-se as 11 aberturas R34/R55 sobre os59 trechos R56 das20 paredes superiores. A geometria R56 teve preservação da superestrutura verificada em R57. Não se efetuou nova exportação ou edição de PRJ/RVT/DWG. A fonte não representa uma vistoria arquitetônica nova.

## Confronto com os pilares

| Abertura | Parede | Área nominal do vão (m²) | Sobreposição nominal com pilar em planta (m) | Faixa com translação de ±0,05m (m) |
|---|---|---:|---:|---:|
| S-J1-01 | W01 | 1.600 | 0.000 | 0.000 a 0.000 |
| S-J1-02 | W02 | 1.600 | 0.000 | 0.000 a 0.000 |
| S-J1-03 | W04 | 1.600 | 0.000 | 0.000 a 0.000 |
| S-P4-01 | W06 | 4.200 | 0.000 | 0.000 a 0.000 |
| S-J2-01 | W09 | 0.480 | 0.000 | 0.000 a 0.000 |
| S-J2-02 | W10 | 0.480 | 0.000 | 0.000 a 0.000 |
| S-P2-01 | W12 | 1.470 | 0.000 | 0.000 a 0.050 |
| S-P2-02 | W13 | 1.470 | 0.000 | 0.000 a 0.050 |
| S-P2-03 | W16 | 1.470 | 0.000 | 0.000 a 0.000 |
| S-P3-02 | W18 | 1.260 | 0.100 | 0.050 a 0.100 |
| S-P3-01 | W19 | 1.260 | 0.000 | 0.000 a 0.000 |

A sobreposição é uma interseção do intervalo horizontal de um vão aproximado com a caixa de um pilar que atravessa o pavimento. Trata-se de triagem geométrica, não prova de interferência executiva. A margem±0,05m foi herdada do estudo R34 e não é precisão de levantamento nem tolerância normativa. Os extremos da faixa incluem os pontos de quebra geométrica das interseções, não apenas duas amostras extremas. Confirmar faces e posição da abertura antes de alterar pilar ou vão. Não se deslocou nenhum apoio por esse diagnóstico.

Na porta S-P3-01, a leitura vetorial bruta tem largura aproximadamente0,60113m, enquanto a tabela especifica0,60m. Usou-se a largura nominal centralizada no intervalo lido para a análise condicional, preservando ambos os valores no JSON. Não se ocultou a discrepância nem se modificou a arquitetura. S-P3-01/W19 e S-P3-02/W18 continuam identificadores distintos.

## Área de alvenaria, ainda condicional

| Parede | Área bruta conhecida, sem trechos de pilares (m²) | Área líquida condicional de alvenaria (m²) |
|---|---:|---:|
| W01 | 10.2240 | 8.6240 |
| W02 | 8.0940 | 6.4940 |
| W03 | 11.9280 | 11.9280 |
| W04 | 14.3420 | 12.7420 |
| W05 | 10.2600 | 10.2600 |
| W06 | 8.0940 | 3.8940 |
| W07 | 11.9280 | 11.9280 |
| W08 | pendente | pendente |
| W09 | 4.1325 | 3.6525 |
| W10 | 4.1325 | 3.6525 |
| W11 | 11.9280 | 11.9280 |
| W12 | 10.2240 | 8.7540 |
| W13 | 2.5560 | 1.0860 |
| W14 | 5.5380 | 5.5380 |
| W15 | 3.1340 | 3.1340 |
| W16 | 3.1340 | 1.6640 |
| W17 | 2.6980 | 2.6980 |
| W18 | 8.1225 | 7.0725 |
| W19 | 10.4025 | 9.1425 |
| W20 | 11.7070 | 11.7070 |

A diferença retira apenas a parcela geométrica do vão sobre o intervalo de alvenaria com altura conhecida. Não se desconta novamente uma abertura na parcela de pilar já excluída. A massa condicional multiplica a área por1,565kN/m², composição hipotética herdada da R55 para parede acabada de15cm. Esse coeficiente não foi confirmado por fabricante. Não se apresenta soma final da edificação: falta W08, paredes térreas, encontros, acabamentos sobre concreto e outras parcelas.

O cálculo de área de janela independe da altura do peitoril apenas se o vão couber integralmente na faixa de alvenaria. Os peitoris J1 permanecem desconhecidos e a verificação vertical correspondente é nula/desconhecida no JSON; não foram inventados. J2 tem peitoril de referência1,50m. As portas usam a hipótese de partir do piso, registrada pela checagem de altura. Tara de esquadrias, vergas/contravergas, arremates e transferência das cargas em torno das aberturas não estão incluídos. Por isso a diferença de massa não é redução liberada de carga estrutural, nem uma distribuição linear pronta para aplicar em cada viga.

Paredes apoiadas sobre laje e caminhos analíticos continuam exigindo análise própria. A massa global não permite substituir cargas locais junto aos vãos por uma carga uniforme sem justificar a distribuição. W08 permanece desconhecida, sem valor zero. A folga geométrica ao forro da R56 não foi convertida em aprovação de flecha ou compatibilização completa.

## Continuidade

Usar o diagnóstico para priorizar a confirmação de faces e das aberturas com sobreposição possível. Completar altura/base de W08, dados verticais J1, pesos de esquadrias e vergas; então preparar matriz local de cargas e aplicar a mesma hipótese aos dois ramos em novas cópias. Nenhuma ocorrência foi atribuída a defeito de transferência DWG/IFC. Não houve edição da monografia ou validação ELU/ELS. O tempo do script registrado mede somente execução computacional, não esforço total da IA, trabalho humano ou duração dos fluxos.

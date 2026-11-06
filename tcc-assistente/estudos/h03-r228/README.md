# H03/R228 — recepção dos arquivos R225 no Eberick

Ensaio exploratório de 6 de novembro de 2026, em duas edificações novas do AltoQi Eberick 2025 Infinity. Os insumos de autoria são o IFC4 do Revit 2027 e quatro DWGs do AutoCAD 2027. O RVT, o IFC e os quatro DWGs conferem com o manifesto congelado da R225. A R228 preserva o primeiro estado recebido. Os modelos calculados estão na R227.

| Indicador | AutoCAD 2D → Eberick | Revit/IFC4 → Eberick |
|---|---|---|
| Entrada | Quatro DWGs, um para N0, patamar, N1 e N2 | Um IFC4 sem transformação prévia |
| Configuração | Quatro cotas cadastradas e unidade de origem em metros, escala 1:1 e camadas de origem mantidas | Nove níveis reconhecidos pelo assistente, com conversão de vigas e pilares habilitada |
| Recepção verificada | Quatro referências visíveis após reabertura. O IFC de controle contém zero elementos estruturais | Relatório com 32/32 vigas e 23/23 segmentos de pilar identificados. Controle com 33 trechos de viga e 67 de pilar |
| Complementação | Lançamento dos elementos a partir das referências. Legendas e metadados não conferidos individualmente no receptor | Lajes e escada a lançar. O controle contém zero lajes e zero lances nativos, embora a entrada IFC contenha essas classes |
| Correção identificada | Conversão estrutural ainda não executada nesta cópia. Correções de geometria após lançamento ainda não medidas | 13 de 32 vigas com seção divergente da nominal. Segmentação dos pilares em níveis auxiliares a revisar |

A distinção entre desenho de referência e conversão automática de vigas e pilares acompanha a operação documentada pelo fornecedor. [Importação DWG/DXF](https://suporte.altoqi.com.br/hc/pt-br/articles/115001514973) · [Nova edificação com modelo externo IFC](https://suporte.altoqi.com.br/hc/pt-br/articles/360021136733)

## Geometria e informações recebidas

- O relatório nativo manteve os 55 identificadores de origem, sem omissão nem duplicidade e com as classes e os níveis de origem esperados. O IFC de controle separa os sólidos produzidos pelo Eberick do modelo de referência vinculado.
- O cruzamento espacial associou os 100 sólidos do controle a uma origem única por eixo, cota e sobreposição em relação ao corpo do IFC bruto, com tolerância computacional de 0,2 mm. A seção do receptor foi comparada separadamente com o tipo nominal do Revit. A V3B-N1, por exemplo, passou de 30 × 20 cm nominais para 30 × 6 cm, com topo 14 cm abaixo do nominal e coincidente com o topo do corpo exportado na origem. A viga do patamar V16 e a viga de base V17 mantiveram as seções nominais de 20 × 30 cm e 30 × 30 cm.
- Dos 67 segmentos de pilar, 23 têm até 5 cm e coincidem com os intervalos introduzidos pelos níveis de piso acabado. O controle contém sete níveis com elementos exportados. A V2-N2 aparece em dois trechos separados por 20 cm na projeção da caixa do IFC bruto. Esse intervalo coincide com a projeção do pilar P10-N2 da autoria, P11 no receptor, e exige leitura do vínculo analítico antes de ser classificado como falha.
- O IFC de controle atribui C-25, cobrimento de 3 cm e classe de exposição 2 aos 100 trechos. Os materiais associados não trazem conjuntos de propriedades mecânicas no arquivo de controle. O BIM herdou critérios do CAD R227 e o CAD desta rodada herdou a configuração do BIM R228. A procedência de C-25 e do cobrimento por transferência IFC não foi isolada.

## Tempos observados

| Etapa | CAD | BIM |
|---|---:|---:|
| Da confirmação da primeira entrada ao salvamento observado na R228 | 3 min 16,8 s | 3 min 53,5 s |
| Da abertura da edição de níveis CAD até o mesmo salvamento na R228 | 7 min 14,4 s | — |
| Processamento interno dos modelos calculados na R227 | 10 s | 10 s |

Os dois primeiros intervalos incluem navegação assistida e latência. Os 7 min 14,4 s do CAD contêm os 3 min 16,8 s da importação. A contagem do IFC começa na confirmação do seletor e inclui a configuração do assistente. A contagem dos DWGs na primeira linha começa com os pavimentos já criados e termina com os desenhos recebidos. Esses marcos têm escopos distintos. A duração do processamento interno pertence a outra revisão. Os valores não sustentam total ou percentual de ganho dos fluxos.

## Próxima medição

Congelar as duas recepções e trabalhar em cópias. No BIM, corrigir as 13 seções pelo tipo nominal, tratar a segmentação decorrente dos níveis auxiliares e verificar a ligação no eixo da V2-N2. No CAD, medir o lançamento inicial a partir das quatro referências. Nos dois ramos, registrar separadamente o tempo de complementação, as operações de correção e a verificação final. O marco comum inclui geometria, lajes e escada, apoios, ações e vínculos conferidos. A análise do estudo permanece limitada à superestrutura.

O script `auditar_par.py` executa a conferência somente leitura dos arquivos nativos e IFCs, grava o registro detalhado no diretório local da R228 e verifica hashes antes e depois. A exportação de controle não estabelece conectividade, transferência de propriedades internas ou aprovação estrutural. Nenhuma das duas cópias brutas foi recalculada.

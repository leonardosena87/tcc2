# H03/R205 — Reprocessamento integral de controle e ensaio da W08

Em 03/11/2026 foram abertas cópias independentes derivadas da R204 CAD e BIM. Na abertura da cópia BIM, executou-se a verificação de projeto danificado oferecida pelo Eberick, como já ocorrera na R201. Para as duas rodadas de controle, desmarcou-se Dimensionar apenas elementos selecionados. Mantiveram-se habilitadas as verificações de deslocamento do pórtico e das lajes com rigidez fissurada. O carregamento de parede da V16 permaneceu o da base.

| Tempo nativo do Eberick, uma execução por fluxo | CAD | BIM |
|---|---:|---:|
| Processamento total | 10 s | 10 s |
| Dimensionamento, incluído no total | 3 s | 3 s |

Os relatórios DOCX foram gerados de forma independente após cada rodada e tiveram seu texto extraído para arquivos TXT. A medição nativa representa o processamento selecionado, incluindo categorias de elementos mantidas no arquivo. O tempo de diagnóstico, abertura e reparo de cópia, tentativa de edição, uso de ferramentas e inspeção não foi medido integralmente. A rodada de 10 s difere da R201 por habilitar o dimensionamento de todos os elementos. As medições pertencem a revisões distintas e não são repetições de um mesmo ensaio.

No CAD, o relatório apresenta 15, 16 e 1 vigas com sucesso nos três níveis. No BIM, apresenta 9 vigas com sucesso em um nível, 11 com sucesso e 1 com erro em outro e 1 com sucesso no nível inferior. A nomenclatura dos níveis foi preservada nos relatórios originais. A quantidade de vigas depende da segmentação dos modelos. Não se utiliza a diferença de contagens como indicador direto de melhor desempenho estrutural.

As duas rodadas apresentam 13 sapatas com erro. A fundação permanece fora do escopo adotado do TCC. Esse registro precisa acompanhar a descrição das opções de cálculo, pois o comando de dimensionamento integral ainda inclui as categorias presentes no arquivo. Os apoios idealizados e os avisos da superestrutura exigem suas verificações próprias.

O resumo de cada rodada exibe peso próprio 79,06 tf, adicional 14,02 tf, acidental 18,45 tf, Q_TELHADO_MANUTENCAO 1,78 tf e total 113,31 tf. O processamento encerrou com avisos.

## Tentativa de delimitação da W08

No BIM da R204 testou-se o comando Modelo > Cargas > Linear com os pontos (450, 0) e (645, 0) cm no croqui do patamar. O Eberick recusou a operação por posicionar carga de parede parcialmente sobre trechos ou barras. Na R205 CAD, a alternativa pelo campo Adicional da mesma ferramenta produziu a mesma recusa. A captura CAD-carga-parcial-recusada.png registra a mensagem. A operação não foi aceita, portanto a carga parcial continua pendente.

A W08 nominal tem 6,75454 kN/m em 1,95 m. A distribuição integral observada em 2,13 m produz 1,2158 kN adicionais por modelo. Reduzir a intensidade integral para 6,1837338 kN/m preservaria o peso total, mas alteraria a distribuição. Essa aproximação não foi aplicada. Para ilustrar a diferença, uma viga ideal simplesmente apoiada de 2,13 m teria momento central de 3,8032 kN.m com o trecho central carregado e 3,5069 kN.m com a carga integral de mesmo peso. Esse exemplo analítico não corresponde ao sistema contínuo da V16 e não verifica a sua seção.

## Referências de entrada SAP

Prepararam-se dois arquivos identificados V16-referencia-parcial-NAO-CALCULADA.$2k a partir das exportações CAD e BIM da R204. Em cada arquivo alterou-se apenas o intervalo relativo da carga distribuída G2 da barra 42 para 0,0422535211 a 0,9577464789. Verificou-se por reversão textual que o restante do conteúdo permaneceu idêntico. Esses arquivos são entradas modificadas externamente, sem importação ou cálculo posterior, e servem como referência para conferir uma futura correção no Eberick.

Para encerrar a W08, delimitar o trecho da própria V16 no croqui, confirmar a retenção dos vínculos da escada, substituir a carga integral, exportar novamente o pórtico e conferir comprimento, resultante e ausência de duplicidade. Os dois fluxos devem receber o mesmo tratamento.

As evidências estão em D:/TCC/outputs/W08-H03-R205-ENSAIO-NAO-EXECUTAR.

[Procedimento de carga em trecho da viga, AltoQi](https://suporte.altoqi.com.br/hc/pt-br/articles/360046158854)

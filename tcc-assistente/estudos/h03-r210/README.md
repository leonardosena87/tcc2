# H03/R210 — V2 e apoio P6, ensaio BIM

## Alterações e resultado

Partiu-se da cópia BIM30-P12-preservado da R209, mantendo o novo apoio P12. Na cópia independente R210, ampliou-se o P6 para 30 x 30 cm, com manutenção da seção na prumada. A planilha de pilares em prumada confirmou b/h de 30/30 cm nos três lances, com níveis 20, 320 e 639 cm. Não se ampliou o P5, próximo de duas portas na arquitetura.

O primeiro recálculo, com V2 de largura 30 cm e alturas 16/45/45 cm, eliminou o Aviso 38, mas manteve o Aviso 02 de viga-parede no trecho curto. Reduziu-se apenas esse trecho, entre P5 e P12, para 30 x 20 cm e executou-se novo dimensionamento integral com deslocamentos por rigidez fissurada. A planilha final confirmou três trechos de 30 x 16, 30 x 20 e 30 x 45 cm, todos com elevação zero. Os comprimentos livres apresentados foram 190, 65 e 335 cm.

No status final do N1, constam 12 vigas dimensionadas, sem vigas nos grupos de erro ou aviso. A V2 apresentou armaduras nos quatro apoios e nos três vãos, sem D16. Isso representa a saída do programa para esta hipótese, sujeita à revisão de detalhamento e compatibilização.

| Apoio da V2 | Md negativo (kN.m) | Armadura superior exibida |
|---|---:|---|
| P6 | -8,40 | 4 phi 8 |
| P5 | -5,69 | 4 phi 8 |
| P12 | -26,65 | 4 phi 12,5 |
| P4 | -22,28 | 4 phi 8 |

P5 e P12 apresentaram também 4 phi 8 inferiores. Nos três vãos, o Md positivo foi 2,42 / 6,35 / 27,21 kN.m, com 4 phi 8 inferiores. No trecho raso, a planilha de cisalhamento exibiu estribos mínimos phi 6,3 a cada 6 cm, com quatro ramos; no curto, phi 6,3 a cada 8 cm, quatro ramos, além do reforço à esquerda a cada 6 cm em 100 cm; no longo, phi 6,3 a cada 21 cm, dois ramos. A descrição transcreve a planilha, sem aprovar viabilidade de montagem, ancoragem ou sobreposição nas mudanças de seção.

No N1, o P6 apresentou Fd 211,95 kN, 4 phi 12,5 e relação Mrd/Msd 1,43; o P12 apresentou Fd 95,75 kN, 8 phi 10 e relação 1,11. Esses valores são resultados locais da hipótese, não reações de base nem aprovação global.

## Diagnóstico completo

Emitiram-se novamente Mensagens da análise e Diagnóstico da estrutura após a última alteração. O relatório de mensagens agrupa avisos como elementos calculados com sucesso; o diagnóstico separa sucesso, aviso e erro. O diagnóstico final registra:

| Pavimento | Elemento | Sucesso | Aviso | Erro |
|---|---|---:|---:|---:|
| N2 | Vigas | 8 | 1 | 0 |
| N2 | Lajes | 5 | 0 | 0 |
| N2 | Pilares | 11 | 0 | 0 |
| N1 | Vigas | 12 | 0 | 0 |
| N1 | Lajes | 6 | 0 | 0 |
| N1 | Pilares | 10 | 2 | 0 |
| N1 | Escadas | 3 | 0 | 0 |
| N0 | Vigas | 0 | 1 | 0 |
| N0 | Pilares | 0 | 11 | 0 |
| N0 | Sapatas | 0 | 0 | 14 |

Na árvore de status, P3 e P4 do N1 exibem Aviso 10: bitola ou número de barras menor que no lance acima. V3 do N2 exibe Aviso 08: carga negativa. Em P1 do N0 conferiu-se Aviso 07: pilar não travado no pavimento; não se extrapola a leitura individual para todos os demais pilares. A viga do N0 permanece pendente de conferência específica nesta revisão. Nenhum deslocamento excessivo foi listado pelo diagnóstico.

O diagnóstico apresenta 1144,28 kN de cargas verticais (803,27 próprias; 138,86 adicionais; 184,35 acidentais; 17,80 manutenção), área aproximada 138,06 m², gama-Z máximo 1,06 e deslocamento horizontal 0,16 cm para vento Y+, contra limite cadastrado 0,42 cm. Esses dados correspondem aos critérios e vínculos cadastrados, sem validação normativa independente. Valores de custo automáticos do relatório não foram validados para orçamento e não são resultados econômicos do TCC.

As 14 sapatas com erro permanecem fora do escopo de dimensionamento. O estudo limita-se à superestrutura e utiliza apoios idealizados, sem sondagem. O cadastro geométrico provisório da R209 não constitui solução de fundação. A continuidade, os vínculos e as reações desses apoios precisam ser auditados.

## Arquitetura e comparação

Na referência R195, P6 está em x6,55/y3,90 m. Com seção quadrada de 30 cm, sua face inferior nominal fica em y3,75 m; o limite superior interpretado da porta P3 próxima está em y3,72745 m. A folga nominal de aproximadamente 2,3 cm é menor que a incerteza de 5 cm da referência. Portanto, a ausência de interferência com marco/acabamento/folha não está demonstrada. P12 exige igualmente compatibilização, inclusive a saliência em relação à parede acabada de 15 cm.

As alterações desta revisão estão apenas na cópia analítica BIM do Eberick. Não foram incorporadas ao Revit, DWG ou fluxo CAD nesta etapa. Não se considera a comparação pareada fechada nem se atribui ao CAD o resultado BIM.

## Tempo e arquivos

O relatório nativo final registra 9 segundos de processamento integral. Inclui cálculo e dimensionamento de elementos de fundação fora do escopo e não representa duração do fluxo, tempo de IA, trabalho humano ou retrabalho. Uma execução isolada e sem CAD equivalente não sustenta vantagem de produtividade.

Pasta local: D:/TCC/outputs/V2-H03-R210-CORRECAO-P6-NAO-EXECUTAR. O PRJ está em BIM/Projeto Eberick/R166-R160-3NIVEIS-CONFIG-CAD-NAO-EXECUTAR.prj. As capturas distinguem a primeira variante da final. R210-final-mensagens.txt e R210-final-diagnostico.txt são extrações dos relatórios nativos reemitidos; o relatório herdado de diagnóstico e a primeira variante de mensagens foram preservados separadamente.

As capturas e os documentos nativos ficam no salvamento local. Este registro não é liberação para execução.

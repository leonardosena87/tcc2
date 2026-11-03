# H03/R207 — Ensaio da carga equivalente da W08 superior

Foi efetivada a edição da V16 nos dois modelos Eberick derivados da R204, nas cópias de trabalho R206. Adicionaram-se nós em (452, 0) e (643, 0) cm, na cota analítica 177,4 cm. A entrada por teclas individuais foi aceita onde a entrada de texto havia falhado. A exportação nativa posterior confirmou três barras, de 11, 191 e 11 cm. Foram preservadas as bases R201 e R204.

## Carregamento conferido

| Trecho em X (cm) | Comprimento | Carga adicional nominal |
|---|---:|---:|
| 441–452 | 0,11 m | 1,23 kN/m |
| 452–643 | 1,91 m | 6,75454 kN/m |
| 643–654 | 0,11 m | 1,23 kN/m |

A carga de parede original foi retirada somente dos dois trechos externos e substituída por carga extra da ação Adicional. O trecho central manteve a parede original. O resultado exportado apresenta G2 de 1,2300 / 6,7545 / 1,2300 nos dois modelos. Os arquivos SAP declaram kgf/cm e usam conversão nominal própria: a soma SI abaixo é reconstruída a partir das entradas de projeto, sem tratar os números brutos como uma medição SI.

O alvo nominal é 6,75454 × 1,95 = 13,171353 kN. Com o arredondamento exportado, a soma é 13,171695 kN, diferença de +0,000342 kN (+0,00260%). A hipótese anterior, uniforme em 2,13 m, correspondia a 14,387170 kN.

Esta é uma aproximação de distribuição. Cada faixa real de parede de 2 cm na extremidade foi distribuída sobre um segmento de 11 cm, com intensidade equivalente teórica de 1,228098 kN/m, arredondada pelo programa para 1,23. O centroide de cada faixa desloca-se 4,5 cm para fora. A simetria conserva o centroide global e a resultante praticamente coincide com o alvo, mas não comprova equivalência dos momentos locais. A distribuição exata nas faces 450/645 cm e a sensibilidade dos esforços continuam como verificações de modelagem. O ensaio não constitui aprovação estrutural.

## Recálculo e tempos

Executou-se dimensionamento integral, com determinação dos deslocamentos do pórtico e das lajes por rigidez fissurada. Ambos terminaram com avisos e carga vertical total exibida de 113,19 tf (79,06 própria, 13,90 adicional, 18,45 acidental e 1,78 de manutenção). No N1, a árvore CAD exibiu 15 vigas dimensionadas e uma com aviso (V9). A árvore BIM exibiu dez dimensionadas, uma com aviso e uma com erro (V2/D16). A V16 não apareceu nos grupos com erro ou aviso consultados.

Os relatórios de mensagens foram emitidos novamente na sessão após os recálculos: CAD 10 s e BIM 11 s de processamento nativo. O relatório CAD inicialmente copiado era herdado da base e foi substituído pela emissão atual. Incluiu-se dimensionamento integral, inclusive fundações que permanecem fora do escopo do TCC; portanto esses tempos não são exclusivos da superestrutura. Um segundo de diferença, com uma execução registrada por fluxo e resolução de um segundo, não estabelece vantagem de produtividade. Os 10/11 s não representam o tempo completo dos fluxos.

O intervalo observado de correção BIM foi de 22:47:49.312Z a 22:52:00.212Z em 03/11/2026 (250,900 s). Inclui navegação, capturas, raciocínio e edição automatizada; não representa tempo exclusivo de cálculo ou intervenção humana. O CAD envolveu descoberta do procedimento e não possui início comparável registrado. A comparação pareada do retrabalho não está fechada.

## Salvamento e evidências

Pasta: D:/TCC/outputs/W08-H03-R207-ENSAIO. Contém exportações separadas CAD/BIM, mensagens DOCX/TXT emitidas na sessão, capturas de resultados/status, R207-conferencia.json e manifesto-salvamento.json com hashes. Projetos-salvos contém as cópias Eberick completas. Autoria-salva preserva o Revit H03-R195-SEM-J4 e o DWG R160 do patamar, em revisões diferentes do ensaio analítico; não se presume sincronização final. O Revit foi salvo pela interface. O AutoCAD estava aberto em somente leitura.

Continuam pendentes a decisão final da distribuição W08 superior, o apoio do pano inferior, a V2 no BIM e sua equivalência geométrica com o CAD, a verificação simultânea da V1 e os avisos remanescentes. O desligamento às 22h foi informado pelo usuário; esta etapa não alterou seu agendamento.

Procedimento operacional consultado: [AltoQi — cargas em um trecho de viga](https://suporte.altoqi.com.br/hc/pt-br/articles/360046158854), [AltoQi — carga linear](https://suporte.altoqi.com.br/hc/pt-br/articles/360058309854). Para a próxima análise da V2: [AltoQi — D16](https://suporte.altoqi.com.br/hc/pt-br/articles/360000680694).

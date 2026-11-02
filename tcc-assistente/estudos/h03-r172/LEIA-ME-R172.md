# R172 — análise de diagnóstico com geometrias corrigidas e cargas parciais

Executaram-se análises no Eberick em cópias independentes CAD R165 e BIM R171. Em ambas, mantiveram-se análise estática e deslocamentos do pórtico com **rigidez configurada**; desmarcaram-se dimensionamento, flechas das lajes, cálculo de rigidez fissurada e dinâmica. A opção de verificar redistribuição semirrígida foi deixada desmarcada em ambas. O BIM inicialmente abriu com redistribuição marcada e deslocamentos do pórtico desmarcados; guardou-se esse estado antes do alinhamento. Isso confirma que copiar a configuração de um projeto não dispensa reler as opções efetivas de processamento.

Ambos terminaram com avisos. A captura documenta o aviso de relação carga/área não usual, sem aprovação dos limites normativos exibidos.

| Parcela vertical exibida (tf) | CAD | BIM |
|---|---:|---:|
| Peso próprio | 75,72 | 75,72 |
| Adicional | 12,00 | 9,65 |
| Acidental | 17,01 | 17,01 |
| Q_TELHADO_MANUTENCAO | 1,78 | Não consta do resumo |
| Total | 106,51 | 102,38 |

A área aproximada exibida é 132,41 m² em ambos. A diferença entre totais exibidos é **4,13 tf** e entre adicionais **2,35 tf**, com arredondamento. A parcela QT ausente permanece `null` no consolidado e não foi imputada como zero. Não se comprovou a origem de toda a diferença por inspeção desses totais; o relançamento das lajes no receptor novo não transferiu automaticamente o conjunto de cargas concentradas cadastradas anteriormente no Eberick. Para atribuir diferenças a parcelas específicas, deve-se reler as cargas nativas e o modelo analítico.

O deslocamento horizontal máximo exibido em X+/X− é 0,15 cm no CAD e 0,20 cm no BIM. Em Y+/Y− aparece 0,20 cm nos dois. O máximo relativo é CAD N1/Y−=0,16 cm e BIM N1/Y+=0,17 cm. Gama-Z X+/X− é 1,07/1,06 CAD e 1,09/1,08 BIM; Y+/Y− é 1,06/1,05 nos dois. Os limites exibidos não foram validados nesta etapa. A diferença de direção crítica permanece explícita.

Há uma pendência analítica importante da viga do patamar: no BIM ela está contida em N1 com Elevação=-142,6 cm, embora a geometria IFC mostre a cota correta. O manual instalado `dialogo_edicao_elemento_viga_adicionar_editar.htm` e a [documentação oficial](https://suporte.altoqi.com.br/hc/pt-br/articles/360038789694) esclarecem que esse campo se destina ao detalhamento e não altera a montagem do pórtico. A [orientação para nível intermediário](https://suporte.altoqi.com.br/hc/pt-br/articles/115002186654) é aplicável ao patamar. A equivalência geométrica não demonstra equivalência analítica. Deve-se corrigir em cópia e conferir o pórtico; não se atribui toda a diferença de deslocamentos a essa única causa sem ensaio controlado.

| Recorte observado | CAD | BIM |
|---|---:|---:|
| Selecionar cópia → configurar/analisar/capturar/salvar/fechar | 398,281 s | 136,967 s |

O CAD inclui aviso de diretório de relatório inexistente, Salvar como no próprio arquivo da cópia e uma segunda análise. O primeiro relatório foi solicitado por menu após fechar a primeira tela; o resumo usado veio da segunda análise, pelo botão Resultados. Há dois intervalos comando/captura CAD, contidos na sessão; o BIM tem um. Não se somam às sessões nem se extraem ranking, economia percentual, tempo puro do solver, tempo total de desenvolvimento, tokens ou custo da IA. As formas de observação dos intervalos foram preservadas nos JSON. Não houve intervenção humana.

Os 28 arquivos-fonte permaneceram íntegros por hash. Os PRJs foram salvos e fechados, tiveram a integridade ZIP conferida e foram congelados com auxiliares. Não se releram todos os resultados após nova abertura. Os três testes verificam extração de evidências reais e rejeição de projeto errado/contradição, preservando QT ausente e direção crítica. Não são aprovação de engenharia. Não se alterou o trabalho escrito, o RVT ou DWG.

Próximo: corrigir a representação analítica da viga de patamar em nível intermediário na cópia BIM, preservando as cargas para isolar a alteração. Depois, recuperar/conferir as ações de cobertura nas posições corretas, integrar escada/apoios e completar paredes, reservatório, vento, combinações e ELU/ELS. NÃO EXECUTAR.

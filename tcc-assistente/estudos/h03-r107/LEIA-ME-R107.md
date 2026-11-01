# H03/R107 - relatorios detalhados recuperados e comparados

As quatro tabelas de deslocamentos geradas nativamente pelo Eberick coincidem entre CAD e BIM na precisao exibida, apos pareamento explicito dos tres nomes de pavimento. Conferiram-se56 celulas numericas correspondentes, todas iguais; isso nao representa56 ensaios independentes. Nao se comprovou equivalencia global ou aprovacao da estrutura.

## O que foi observado

| Tabela relativa, ambos os ramos | X+ (cm) | X- (cm) | Y+ (cm) | Y- (cm) | Limite exibido (cm) |
| --- | ---: | ---: | ---: | ---: | ---: |
| N2 | 0,03 | 0,03 | 0,04 | 0,04 | 0,38 |
| N1 | 0,17 | 0,17 | 0,16 | 0,16 | 0,35 |
| N0 | 0,01 | 0,01 | 0,01 | 0,01 | 0,12 |

O resumo regenerado em cada ramo coincide com seu proprio resumo R106: CAD indica N1/Y- com0,17cm e BIM indica TCC-cdd31967-N1/Y+ com0,17cm. A celula da tabela com o mesmo rotulo de direcao apresenta0,16cm em ambos. A identificacao nao foi reconciliada. A comparacao literal nao determina a causa ou eventual diferenca de semantica das saidas; nao demonstra defeito do software, empate ou erro de transferencia. Nao se alteram os rotulos para produzir uma concordancia artificial.

A tabela geral registra altura total719cm, deslocamento caracteristico0,67cm em X e0,68cm em Y, fator denominado gf2=0,30 e deslocamento de combinacoes frequentes0,20cm nos quatro sentidos. As demais tabelas registram alturas de pavimento, deslocamentos absolutos, massas, centros de massa e raios de giro. As celulas de centro de rigidez estao vazias; nao equivalem a zero. O proprio relatorio condiciona os centros ao efeito de diafragma rigido, cuja adequacao final nao foi concluida.

Mantem-se o escopo parcial R106: rigidez configurada, sem dimensionamento final, flechas de lajes, vibracoes ou rigidez fissurada calculada. Carregamento e vento local continuam incompletos. Os limites exibidos nao constituem conferencia normativa concluida.

## Recuperacao da emissao

Ao solicitar o relatorio em cada copia R106, o programa informou "A pasta para criacao da edificacao nao foi encontrada" e exigiu salvar em outro local. Preservou-se a mensagem. A ajuda instalada a_pasta_da_edificacao_nao_foi_encontrada.htm descreve a ocorrencia em caminhos alterados e orienta salvar em novo local. Essa explicacao e compatibilidade de sintomas; nao prova a causa exata desta ocorrencia.

O comando nativo Salvar como gerou copias laterais independentes:

- D:/TCC/outputs/R107-CAD/H03-CAD-NAO-EXECUTAR.prj
- D:/TCC/outputs/R107-BIM/H03-BIM-NAO-EXECUTAR.prj

Apos Salvar como, os resultados do CAD ficaram inativos no menu observado. Regenerou-se a analise parcial nas duas copias para recuperar a emissao, mantendo as opcoes visuais da R106. A repeticao tem essa justificativa operacional e nao conta como novo ensaio final de produtividade. Ambos os resumos regenerados foram relidos e coincidem com seus respectivos antecessores. Os relatorios DOCX foram emitidos pelo proprio Eberick e suas tabelas foram conferidas no Word. Nao se editou a monografia.

Os dois PRJs de origem R106 permaneceram inalterados. A reabertura atualizou oito arquivos auxiliares SAV/SAV-G2/SAV-G3/log, quatro por ramo; as diferencas estao discriminadas no resultado. Os congelados R106 anteriores continuam preservados. As novas copias R107 foram salvas, fechadas e congeladas com hashes conferidos.

## Tempos e limites metodologicos

O tempo CAD inclui uma lacuna de conversa de varias horas entre a tentativa inicial e a retomada. O tempo BIM corresponde a outra janela de recuperacao. Nenhum dos dois mede trabalho ativo, solver isolado ou produtividade comparavel. Os intervalos comando-registro estao contidos nas sessoes; nao se somam. As marcas monotonicamente medidas e UTC foram preservadas, sem descontar pausas retrospectivamente. O cabecalho de data/hora gerado no DOCX identifica a emissao, sem ser usado para calcular duracao.

O consolidado preserva as quatro tabelas sem alterar valores, os nomes originais e o mapa de nomes explicito. A tabela vazia que contem somente o grafico foi excluida da comparacao textual, sem eliminar seu desenho do DOCX. Dois controles de extracao rejeitam pavimento desconhecido, direcao reordenada e tabela ausente, e verificam que a igualdade das tabelas nao apaga a divergencia do resumo. Sao controles de dados, sem validacao estrutural.

Os projetos nativos e DOCX ficam apenas em D:/TCC. O repositorio recebe codigo, instrucoes, tabelas JSON e capturas pertinentes. Proxima tarefa: fechamento das cargas e vento, com a pendencia de identificacao critica preservada. Nao repetir calculo identico para tentar eliminar a divergencia.

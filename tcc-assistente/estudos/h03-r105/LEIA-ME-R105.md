# H03/R105 - inventario de tempos apos diagnostico R104

O recorte atualizado encontrou164 arquivos candidatos:126 intervalos com duracao principal explicita,26 registros sem essa duracao e12 conteineres nao expandidos. Foram identificados13 pares de intervalos com sobreposicao. Nao se somou o conjunto e nao se calculou vantagem CAD/BIM.

A busca abrange arquivos com tempo no nome diretamente nas pastas filhas de D:/TCC/outputs, quatro processos tecnicos CAD da R84, resumo separado do banco central e demonstracoes da palestra separadas. O arquivo criado por esta execucao nao existia no momento da busca. Nao e inventario de todo o esforco da pesquisa nem contagem de164 ensaios independentes.

O instrumento passou a reconhecer commandToRecordedFinishMs e commandToFirstObservedFinishMs, alem do limite UTC endFirstFinishRecorded. Esses campos medem janela de observacao, nao solver isolado. Os campos originais e os limites UTC continuam preservados separadamente. Os13 pares sobrepostos incluem intervalos de processamento contidos nas respectivas sessoes; nao devem ser somados novamente a elas.

A atualizacao passou em sete testes Node, incluindo rejeicao de duracao negativa, preservacao do intervalo monotônico e da diferenca UTC, deteccao de sobreposicao e impedimento de ranking final. Sao testes do instrumento, distintos das duas execucoes nativas R104. O arquivo R86-inventario-tempos.json conserva o nome e a revisao do formato do inventariador reutilizado; R105-resumo.json identifica este marco de coleta.

Os tempos totais finais CAD/BIM permanecem nulos. Inferencia isolada, tokens e custo da IA na edificacao principal continuam desconhecidos. Os quatro registros da demonstracao e as tres sessoes do banco central nao se tornam ensaios finais da H03. Nao se estimou consumo de creditos a partir destes arquivos.

As medicoes R104 de abertura ate fechamento foram134,9102873sCAD e134,5801248sBIM; incluem navegacao e registros. As janelas comando-registro foram33,6689288s e19,1562105s, com limites de observacao distintos, documentados na R104. Nao se calculou percentual de rapidez. A igual precisao exibida do resumo estrutural e uma observacao de resultado, nao um criterio suficiente de qualidade integral ou equivalencia dos fluxos.

Reproducao: node inventariar.mjs D:/TCC <pasta nova>. Os originais do inventario anterior e o banco central foram somente lidos. O trabalho escrito e os arquivos nativos nao foram alterados nesta consolidacao.

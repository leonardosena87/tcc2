# H03/R104 - diagnostico estatico pareado, parcial

Executou-se analise estatica em duas copias independentes da R102. Desmarcou-se Dimensionamento dos elementos em ambas; ELS-DEF e ELS-VE permaneceram desmarcados. A construcao do modelo, os paineis de lajes e o portico espacial foram processados. Ambas concluiram com avisos. Nao se realizou dimensionamento final nem verificacao de deslocamentos de servico.

## Hipotese comum da base

Mantem-se, para este diagnostico, o vinculo rotulado dos onze apoios N0 ja consultados na R103: translações X/Y/Z restringidas e rotacoes livres. O vinculo do pilar segue Engastado, com barra fixa de10cm. Essa e uma idealizacao analitica para o estudo da superestrutura, nao uma caracterizacao medida do solo. O tipo Sapata do cadastro nao constitui solucao geotecnica ou fundacao dimensionada. Nao se atribuiu automaticamente o apoio elastico padrao da R101.

A documentacao oficial esclarece a diferenca entre os vinculos: [AltoQi - vinculo de apoio das fundacoes](https://suporte.altoqi.com.br/hc/pt-br/articles/360012152833). A ajuda instalada controle_de_vinculacoes_de_fundacoes.htm confirma os graus de liberdade. A manutencao do vinculo atual permite testar os dois receptores sob a mesma hipotese; sua sensibilidade e adequacao final continuam sujeitas a verificacao com o carregamento completo.

## Resultado observado

Os dois resumos nativos coincidiram integralmente na precisao exibida:

| Grandeza exibida | CAD | BIM |
| --- | ---: | ---: |
| Peso proprio (tf) | 75,69 | 75,69 |
| Adicional (tf) | 10,05 | 10,05 |
| Acidental (tf) | 17,11 | 17,11 |
| QT (tf) | 1,40 | 1,40 |
| Total (tf) | 104,25 | 104,25 |
| Area aproximada (m2) | 132,81 | 132,81 |
| Relacao (kgf/m2) | 784,99 | 784,99 |
| Gama-Z X+ / X- | 1,09 / 1,08 | 1,09 / 1,08 |
| Gama-Z Y+ / Y- | 1,06 / 1,05 | 1,06 / 1,05 |

Os avisos exibidos incluem relacao de carga por area nao usual e deslocamentos horizontais nao verificados. O bloco que mostra0,00cm para esses deslocamentos nao representa verificacao aprovada nem deslocamento fisico nulo. No bloco separado de P-Delta, o resumo informa Vento X:0,96 para1,10 e Vento Y:1,06 para1,15, conforme transcricao integral preservada. Nao se deduz aprovacao ELS desses numeros. A terminologia e o limite1,10 exibidos pelo programa nao substituem conferencia normativa final.

Esta coincidencia parcial nao prova que todo esforco, vinculacao, malha ou detalhamento seja identico. Cargas de P1/P2, reservatorio, paredes/aberturas, escada, parametros locais de vento e combinacoes efetivas continuam pendentes. Nao se usa este processamento como resultado estrutural final ou como autorizacao para executar obra.

## Tempos e preservacao

| Recorte exploratorio | CAD (s) | BIM (s) |
| --- | ---: | ---: |
| Abertura ate fechamento, incluindo navegacao e registros | 134,9102873 | 134,5801248 |
| Comando ate registro do termino observado | 33,6689288 | 19,1562105 |

O segundo recorte inclui latencia e intervalo entre observacoes. No CAD, a marca de fim foi registrada na chamada posterior a captura de conclusao; no BIM, junto a captura de conclusao. Por isso, nao se classifica velocidade do solver nem desempenho dos fluxos por esses valores. O recorte menor esta contido na sessao e nao deve ser somado a ela. O tempo puro do solver permanece nulo. Preparo das copias, abertura do aplicativo e consolidacao posterior nao integram as sessoes.

O programa nao estava aberto na retomada. O primeiro retorno da abertura nao encontrou janela; a consulta seguinte encontrou o Eberick. Houve atualizacao da captura apos notificacao de entrada do usuario. Nao se atribui esse esforco de interface a defeito DWG/IFC.

As copias processadas foram salvas e fechadas. Permanecem laterais ao conjunto principal R102:

- D:/TCC/outputs/18-H03-R104-CAD-DIAGNOSTICO-NAO-EXECUTAR
- D:/TCC/outputs/19-H03-R104-BIM-DIAGNOSTICO-NAO-EXECUTAR

Os33 arquivos de origem R102 mantiveram os hashes. Congelaram-se16 arquivos CAD e19 BIM apos o processamento, conferidos contra as copias fechadas. O arquivo R102-preparacao.json nesta pasta e o manifesto gerado pelo preparador reutilizado, com caminhos R104; o nome foi preservado para rastreabilidade. Nao se sobrescreveram resultados anteriores, autoria RVT/DWG ou monografia.

Um controle sintetico rejeita resumo ausente, incompleto ou contraditorio. A evidencia real e a captura de conclusao e do resumo em cada receptor. O script nao interpreta automaticamente as selecoes das imagens nem valida dimensionamento. Continuar pelo fechamento das cargas e pela auditoria das ligacoes/relatorios efetivos, aproveitando os resultados parciais sem confundi-los com o ensaio final pareado.

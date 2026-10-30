# H03/R79 — dimensionamento exploratório e diferença de agrupamento

ESTUDO COM CARGAS PARCIAIS. NÃO EXECUTAR. O propósito desta revisão é localizar impedimentos de dimensionamento e conferir diferenças entre os receptores. Nenhuma seção, vinculação ou armadura foi corrigida. A monografia e os autores RVT/DWG não foram alterados.

## O que se executou no programa

Criaram-se cópias independentes de R78, preservando fatores Q=0,50/0,40/0,30. Na janela de análise marcou-se dimensionamento apenas de elementos selecionados e escolheram-se exclusivamente vigas moldadas no local de N1/N2. Desmarcaram-se os demais tipos em todos os pavimentos e todos os pré-moldados. Executou-se análise estática linear com P-Delta já configurado. Deixou-se ELS/redistribuição adicional/dinâmica desativados neste recorte exploratório. As imagens de seleção e opções documentam o comando efetivamente preparado nos dois ramos.

**Limitação operacional identificada:** a consulta posterior **Status dos elementos** não foi uma simples leitura passiva: no BIM observou-se o programa calculando pilares automaticamente durante a abertura. A árvore completa também mostrou mensagens de lajes, pilares e sapatas auxiliares. Assim, não se declara que nenhum elemento além das vigas sofreu cálculo interno nesta sessão. Os cadastros auxiliares de sapata exibiram 11 erros D42 por ramo; não se corrigiu nem utilizou esse cálculo como fundação real. O estudo permanece delimitado à superestrutura e sem validação geotécnica. Antes de automatizar novas consultas, separar o processamento solicitado dos cálculos disparados por janelas/relatórios.

## Resumo global e mensagens

O resumo visível coincidiu integralmente entre os dois receptores: peso próprio75,69tf, adicional10,05tf, acidental17,11tf, total102,86tf, área aproximada132,81m² e relação774,46kgf/m². Persistiram os avisos de relação carga/área não usual e deslocamentos horizontais não verificados. Os valores0,00 de deslocamentos dessa janela não significam deslocamento físico nulo. Essa coincidência não prova igualdade de todas as combinações, malhas ou armaduras.

Na árvore de status do CAD apareceram 15 vigas com aviso em N1 e15 em N2, sem grupo de erro de viga. No BIM apareceram1 viga com erro e11 com aviso em N1 e8 com aviso em N2. São **grupos nativos de detalhamento diferentes**, não os mesmos denominadores. Não se calcula taxa de erro nem ranking a partir dessas contagens. Os32 sólidos de vigas por ramo e as29 unidades lógicas da proposta R43 são recortes distintos: as contagens históricas29/62 descrevem a proposta/transferência, e não comprovam que cada receptor tenha29 grupos nativos. A auditoria de agrupamentos posterior deve atualizar essa distinção sem apagar os registros anteriores.

O CAD apresentou aviso98 em V9/N1 (ancoragem da armadura de pele no nó3) e aviso08 em V13_1/N2 (carga negativa). O BIM apresentou aviso98 em V11/N1 (nó1), aviso08 em V3/N2 e erroD16 em V2/N1 (nó2). O aviso123 de deslocamentos não verificados apareceu nas30 vigas CAD e nas19 vigas BIM do grupo de avisos; não se infere que a viga com D16 tenha deslocamentos verificados. Também se preservaram mensagens dos outros elementos para rastreabilidade, sem atribuí-las automaticamente a defeitos de intercâmbio.

## D16 na V2 BIM e correspondência física

Na planilha Nó da V2/N1 selecionou-se a linha2, apoioP5, momento exibido−38,17kN·m. A janela de resultados da armadura mostrou A07 — taxa de armadura maior que a configurada — para as cinco bitolas8/10/12,5/16/20mm. O limite configurado foi2% nos dois ramos; a relação máxima de CG foi10%, também igual. Os demais valores de campos editáveis/combinações da máscara principal de Vigas coincidiram no recorte comparado. Não se elevou um limite para eliminar o erro.

A V2 BIM reúne barras de extensão199,60 e440,00cm, seções20×16 e20×45cm, nível320cm e elevação0. Pelo mapa geométrico R72, correspondem aos trechos físicos de V14 eV2 do CAD. O CAD mostrou na V2 os momentos−33,20 e−38,17kN·m, com4ϕ8 e3ϕ10 nos apoios; na V14, de20×16cm, mostrou−8,49 e−6,55kN·m, com4ϕ8. A existência de um momento−38,17 na mesma linha física não demonstra que ele deva ser automaticamente aplicado ao trecho raso em ambos os detalhamentos. O agrupamento e as faces/seções utilizadas nos nós precisam de teste controlado. A diferença de agrupamento é hipótese explicativa concreta, **ainda sem prova causal de que originou o D16 ou de que representa falha do IFC**. Nenhuma dessas armaduras foi aprovada para execução.

O procedimento para abrir Nó e Resultados da armadura segue a [documentação operacional AltoQi sobre D16](https://suporte.altoqi.com.br/hc/pt-br/articles/360000680694). Essa fonte explica a investigação no software; não é comprovação normativa do projeto.

## IA do Eberick e medição

Nos dois receptores observou-se a opção **Escolher bitolas usando IA**, coleta automática e treinamento ao salvar marcados; a janela mostrou17 dados coletados e0 treinados, sem acurácia ou data de treinamento. No CAD a leitura ocorreu após salvar/reabrir, no BIM antes do salvamento final. Esse estado observado não comprova inferência por modelo treinado durante o processamento nem permite atribuir economia de tempo à IA nativa. Não se acionou treinamento manual ou limpeza. Essa ferramenta difere da assistência generativa usada para scripts, navegação e interpretação; ambas precisam de registro próprio na metodologia. Um ensaio final deve congelar e padronizar também esse estado.

Os intervalos exploratórios prospectivos foram CAD17.848min e BIM129.332min; incluem navegação, desenvolvimento da investigação e esperas. O CAD inclui reposicionamento humano e tentativas de controle; o BIM inclui interrupção e retomada da conversa. Não se conhece tempo ativo isolado. O intervalo CAD terminou antes da conferência adicional de parâmetros/V14, realizada posteriormente e sem novo cronômetro; não se soma ou reconstrói essa duração. Os subintervalos de processamento registram comando/captura/latência, não tempo puro de CPU; estão contidos nas etapas e não devem ser adicionados novamente. Não constituem duração final dos fluxos ou ranking. Ver protocoloR69.

## Preservação e próximos passos

PRJ/companheiros foram salvos e congelados separadamente, com integridadeZIP e SHA256. Todos os 54 arquivos protegidos de R78 permaneceram iguais. A última confirmação de fechamento CAD após conferência exigiu usar a captura específica do diálogo: a coordenada do recorte de diálogo é relativa a ele; entradas dirigidas ao quadro principal não estavam acionando o botão. Esse procedimento não elimina automaticamente o problema dos campos editáveis de outras janelas.

O próximo trabalho é mapear as29 vigas lógicas da origem aos32 sólidos e grupos nativos de cada receptor, preservando as diferenças encontradas; depois testar uma hipótese de agrupamento em novas cópias, sem mudar cargas/seções/limites simultaneamente. Completar cargas, vínculos, ELU/ELS e critérios2026 continua necessário. O IFC não foi reexportado nesta revisão; não se afirma nova auditoria geométrica pós-processamento.

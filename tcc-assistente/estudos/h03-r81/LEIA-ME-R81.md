# H03/R81 — teste local da contribuição do agrupamento ao D16

EXPERIMENTO COM CARGAS PARCIAIS. NÃO EXECUTAR. A cópia de teste e a de controle foram obtidas do mesmo congelamento BIM/R79. Nenhum autor RVT/DWG, receptor CAD ou texto da monografia foi alterado. O teste não substitui revisão técnica da solução estrutural.

## Operação e observação

No croqui N1 acionou-se o comando nativo **Dividir**, selecionou-se V2 e o nó existenteP5. O programa manteve o trecho raso com nomeV2 e criouV13 para o trecho mais alto. Não se inseriu nó, não se rotulou ou engastou manualmente, nem se editou seção, carga, nível ou limite de armadura. Repetiu-se a seleção de vigas N1/N2, demais tipos e pré-moldados desmarcados, análise linear/P-Delta e ELS desativados, comoR79. Registraram-se opções e seleção em imagens. O processamento terminou com avisos.

A V2 de20×16cm passou a exibir momentos−6,55 e−8,49kN·m nos apoiosP6/P5, com4ϕ8 nos dois. A V13 de20×45cm exibiu−38,17 e−33,20kN·m emP5/P4, com3ϕ10 e4ϕ8. Esses valores e escolhas locais coincidiram com os trechos correspondentes CAD/R79, respeitando orientação e identificação física. Mantiveram-se extensão/comprimento livre199,60/190cm e440/420cm, elevação0 e nível320cm.

Na árvore expandida, D16 não apareceu nas vigas:13 grupos N1 e8 grupos N2 apresentaram aviso123; também permaneceram98 naV11/N1 e08 naV3/N2. O desaparecimento do D16 após o único comando de divisão sustenta a contribuição operacional desse agrupamento neste teste específico. Não demonstra a origem histórica do agrupamento na importação, nem permite concluir defeito geral de IFC ou superioridade de um fluxo. Tampouco autoriza dividir toda viga contínua apenas para obter mensagem favorável. A adequação do detalhamento, continuidade, ancoragens, faces de apoio e aplicação normativa ainda exige revisão técnica.

O resumo global permaneceu integralmente igual ao BIM/R79. Isso inclui cargas ainda parciais e os avisos de relação carga/área e deslocamentos não verificados. A consulta de Status novamente disparou cálculos de outros tipos; capturou-se **LajeL5 calculando**. Persistiram11D42 dos apoios auxiliares, sem uso como fundação real. O arquivo de teste foi salvo, fechado e reaberto; conferiram-se a divisão no croqui e os momentos/armaduras daV2 após reabertura.

## Exportação de controle e mudança de representação

Exportou-se IFC4 completo do teste, sem agrupamento de exportação e sem armaduras3D. Exportou-se também cópia idêntica ao PRJ/R79, sem dividir ou reprocessar, para pasta separada. Descartaram-se ao fechar apenas as alterações de configuração de exportação dessa cópia de controle; seu PRJ permaneceu exatamente com o SHA256 inicial.

O primeiro ensaio de auditoria esperava76 partes comoR57 e falhou porque ambos os estados pós-dimensionamento exportam89:22 pilares,45 partes de vigas,11 lajes e11 auxiliares de apoio. Essa falha de hipótese foi investigada e não tratada como falha do projeto. A comparação direta controle/teste confirmou89 correspondências únicas por classe+caixa, mesma área superior e apenas uma alteração de nome (V2→V13). Entre propriedades exportadas, apenas a taxa de armadura dos dois trechos mudou, de Não calculado para0,63% no raso e0,22% no alto. Taxa de armadura exportada não equivale à verificação completa dos limites e detalhamento.

Comparou-se ainda a geometria histórica das32 partes de vigas com as45 do controle. Para cada parte anterior exigiu-se cobertura longitudinal contínua, sem lacuna/sobreposição entre caixas, mesma seção transversal e soma da área superior. As45 partes cobrem exatamente as32 caixas históricas. As caixas dos demais tipos também se preservaram. As13 partes adicionais refletem subdivisão da representação exportada neste estado; **não são13 novas vigas físicas ou grupos de detalhamento**. As29 unidades lógicas de origem e os grupos nativos20→21 continuam sendo outras medidas. Não se afirma equivalência de todo o modelo analítico a partir dessa auditoria geométrica.

## Tempo, preservação e decisão

O intervalo prospectivo de investigação durou14.652min, incluindo navegação, elaboração da auditoria, exportação de controle e conferência após reabertura. O subintervalo comando→primeira captura de conclusão foi8.261s, com latência de automação/captura; não é tempo puro de solver e não deve ser somado ao intervalo maior. Não houve participação humana nesta etapa. Tempo ativo exclusivo é desconhecido; não se utiliza este intervalo para ranking de produtividade.

Preservaram-se100 arquivos protegidos R79. Congelaram-se separadamente teste e controle, com integridadeZIP/SHA256. Não se promoveu o teste a projeto final nem se corrigiu o D16 nas evidências R79. O próximo passo é completar as cargas e verificar vínculos/combinações/ELU/ELS em bases explicitamente selecionadas, mantendo disponível o estado anterior e o efeito observado do agrupamento. A monografia permanece intocada.

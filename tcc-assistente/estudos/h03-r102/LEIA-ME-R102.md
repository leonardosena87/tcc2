# H03/R102 - inclusao da QT nas combinacoes verticais

Criaram-se duas copias independentes dos receptores fechados R98. Os 33 arquivos de origem foram conferidos por hash na copia e apos o trabalho. Apenas o apontamento ProjetoRecente/Arquivo do INI foi ajustado na preparacao para cada PRJ proprio.

No Eberick, alterou-se somente o coeficiente da acao Q_TELHADO_MANUTENCAO nas duas combinacoes auxiliares:

| Combinacao | Antes QT | Depois QT | Expressao nativa apos reabrir |
| --- | --- | --- | --- |
| Vertical de calculo P-Delta | 0,00 | 1,40 | 1.4G1+1.4G2+1.4Q+1.1A+1.4QT |
| Vertical caracteristica do desaprumo | 0,00 | 1,00 | G1+G2+Q+A+QT |

O fator 1,40 acompanha o fator normal desfavoravel do concreto ja cadastrado para QT, mantendo o criterio majorado comum existente para Q; 1,00 inclui o valor caracteristico integral. E uma decisao documentada de configuracao do estudo, sujeita a revisao juntamente com a simultaneidade e as demais acoes. Nao define todas as combinacoes ELU/ELS, nem dispensa a verificacao normativa final. Nenhum outro coeficiente foi intencionalmente alterado.

A ajuda instalada oficial configuracoes_analise.htm esclarece que a combinacao de calculo define a carga axial empregada no P-Delta e que a caracteristica determina a carga vertical para o desaprumo. Referencia complementar: [AltoQi - processo P-Delta](https://suporte.altoqi.com.br/hc/pt-br/articles/115001189434). Nao se confunde essas combinacoes com a geracao automatica das envoltorias de dimensionamento.

Ambas as copias foram salvas, fechadas e reabertas. As quatro expressoes nativas regeneradas foram relidas e conferidas. A grade foi observada visualmente durante a edicao; nao e interpretada pelo script. No BIM, Ctrl+S nao concluiu a gravacao: o fechamento solicitou salvar e a opcao Sim foi acionada, antes da reabertura de conferencia. Uma primeira digitacao na celula concatenou texto; corrigiu-se integralmente com selecao Home/Shift+End antes de aceitar. Isso e esforco de interface, nao perda de intercambio.

Arquivos atuais fechados:

- CAD: D:/TCC/outputs/16-H03-R102-CAD-QT-VERTICAL-NAO-EXECUTAR/Projeto Eberick/H03_CAD_R49_LAJES_NAO_EXECUTAR.prj
- BIM: D:/TCC/outputs/17-H03-R102-BIM-QT-VERTICAL-NAO-EXECUTAR/Projeto Eberick/H03_BIM_R46_IFC_NAO_EXECUTAR.prj

R102-resultado.json contem hashes, releituras e tempos. CAD: 298,7709324 s; BIM: 1154,2696177 s. Sao recortes exploratorios com registro e interrupcao de conversa no BIM; nao classificam produtividade, nao sao tempo ativo e nao devem ser somados como total final de cada fluxo. O preparo das copias e a consolidacao posterior ficam fora desses recortes.

Dois testes sinteticos verificam rejeicao de evidencia ausente/contraditoria/sem QT e aceitacao de duplicatas identicas. A conferencia nativa real corresponde a quatro expressoes apos reabrir. Nao houve novo processamento estrutural. As leituras nodais G/QT da R99 continuam historicas; nao foram repetidas nesta revisao.

Continuam pendentes apoios efetivos e ligacoes, materiais locais, P1/P2, reservatorio, paredes/aberturas/escada, vento, combinacoes efetivas, ELU/ELS e ensaio final pareado. A monografia e os modelos de autoria foram preservados. Resultados anteriores nao representam esta nova entrada.

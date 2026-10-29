# H03/R55 — paredes e compatibilizacao preliminar da cobertura

Estudo comum aos dois fluxos; NAO EXECUTAR. Nenhum PRJ/RVT/DWG foi alterado. A fonte geometrica e o IFC R53 de cada ramo; a auditoria de exportacao posterior a conversao de apoios R54 continua pendente. Conferiram-se os hashes dos 36 arquivos do manifesto R54, sem alteracao.

Mapearam-se 20 paredes superiores em 59 trechos por intersecao de eixos com caixas envolventes reais. As caixas espaciais exportadas R53 coincidem entre CAD e BIM. O CSV inclui nomes nativos CAD e BIM correspondidos por classe e caixa espacial. Paredes com trechos sobre laje: W15, W16, W20. Esse contato geometrico nao comprova o caminho analitico da carga.

As 11 aberturas receberam identificadores individuais da referencia R34. A porta S-P3-01 fica na W19 e S-P3-02 na W18; nao sao uma abertura duplicada. Manteve-se a area bruta sem desconto de portas/janelas. W08 permanece sem base/altura resolvida junto a escada, com carga desconhecida (campo vazio), nunca carga numerica zero.

A parede acabada de 15cm e premissa do usuario. A composicao de estudo e bloco ceramico vazado horizontal de 11,5cm mais 1,75cm de argamassa por face. Pelo exemplar local da NBR 6120:2019, Tabela2/PDF17, usou-se 0,90kN/m2 sem revestimento e 19kN/m3 para argamassa; calculou-se 1,565kN/m2 de parede. Essa composicao nao foi medida nem confirmada por fabricante. A carga linear bruta e 1,565 vezes a altura de referencia do piso acabado ao menor intradorso interceptado. Nao aplicar esses numeros automaticamente.

A triagem marcou interferencia com a referencia de forro a 2,80m nas paredes: W01, W02, W03, W04, W05, W06, W07, W09, W10, W11, W12, W13, W14, W15, W19, W20. Algumas vigas exportadas da cobertura ainda apresentam altura de 35, 40, 45 ou 55cm; apenas os trechos com intradorso acima do forro atendem geometricamente essa condicao preliminar. Preservar a arquitetura conforme decisao do usuario: revisar seções/concepcao, calcular e verificar ELU/ELS antes de aceitar qualquer reducao. Nao elevar a cobertura para ocultar interferencia. O conflito pertence a concepcao comum; nao conta como erro de IFC ou DWG.

Ainda faltam definicao de faces/comprimentos liquidos, acabamento sobre pilares, encontros, vergas/contravergas, tara de esquadrias e suporte analitico. Nao ha soma final de cargas. A etapa nao mede tempo comparativo de fluxo: o registro de execucao do script exclui preparacao, pesquisa e revisao; nao equivale a esforco total de IA/humano.

Proxima etapa: resolver seções da cobertura preservando forro/pisos; exportar e auditar os estados posteriores a R54; fechar cargas por trechos e so entao aplicar a mesma matriz, em copias independentes, com temporizadores separados. Permanecem pendentes telhado, tanque1000L/apoio, escada, bordas, vento, combinacoes e processamento.

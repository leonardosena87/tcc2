# R224 — Complemento da V1 incorporado e comparação da cobertura

Pasta local: `D:/TCC/outputs/H03-R224-FECHAMENTO-DETALHES-NAO-EXECUTAR`. Cópias independentes dos dois projetos R223. Esta revisão não altera a monografia nem sincroniza os arquivos de autoria Revit/AutoCAD.

## Trabalho executado no programa

Incorporou-se o DXF complementar R223 da V1 ao gerenciador de desenhos nativo dos dois projetos, pelo AltoQi Builder. Conferiu-se visualmente o conteúdo e salvou-se em formato CAD nativo, associado ao N0:

- CAD: `CAD/Desenhos/Estrutural/N0/R224-V1-ANCORAGEM-COMPLEMENTAR-NAO-EXECUTAR.cad`.
- BIM: `BIM/Desenhos/Estrutural/TCC-7a6267fd-N0/R224-V1-ANCORAGEM-COMPLEMENTAR-NAO-EXECUTAR.cad`.

O complemento continua sendo **estudo externo**, com a hipótese de gancho superior de 9,5 cm. Importar o desenho não modifica a armadura dimensionada pelo Eberick, não substitui a armadura automática e não aprova ancoragens, nós ou execução. A indicação R223 dentro da prancha identifica a origem do estudo; R224 identifica sua incorporação ao projeto. O detalhe nativo da V1 conserva o gancho superior de 27 cm. O estudo de 30×30 cm e suas limitações permanecem descritos na R223.

Preservou-se também um desenho de sessão R218 recuperado, identificado como histórico. O arquivo `R224-V1-REVISAO-EXTERNA-30X30-NAO-EXECUTAR.CAD`, criado vazio durante a navegação no CAD, é um registro de interface e **não é o complemento**. O arquivo correto contém `ANCORAGEM-COMPLEMENTAR` no nome. Desenhos antigos R218 não representam a seção e o detalhamento atuais.

## Cobertura: CAD V13_1 e BIM V3

Emitiram-se relatórios novos de combinações, com seleção exclusiva da viga correspondente em cada projeto. Os documentos estão em `CAD` e `BIM`, na subpasta `Arquivos do projeto/Documentos/Eberick/Pav3_Vigas_Combinacoes.docx`. Preservaram-se capturas dos dois detalhamentos, incluindo o Aviso 08.

Cada relatório contém 19 casos simples e 68 combinações, com três subdivisões de carregamento da mesma viga, não três vãos independentes. A comparação considera 14 campos numéricos por subdivisão, totalizando **3.654 pares de valores**. Encontraram-se **37 diferenças**, todas com magnitude de uma unidade na última casa decimal impressa: 0,01 kN/m, kN ou kN·m, conforme o campo. Os campos efetivamente divergentes constam do JSON; não se arredonda a diferença para declarar igualdade. A origem dessas diferenças não foi isolada nesta revisão. A pequena magnitude isolada não comprova irrelevância em toda verificação estrutural.

O detalhamento visual coincide nos dois fluxos: seção20×30 cm, topo+6,39 m, vão livre285 cm, apoios30/20 cm, duas barras superiores contínuas Ø8 C376 com trecho329 cm e ganchos24/27 cm; uma barra superior adicional à esquerda Ø8 C109, trecho87 cm e gancho24 cm; duas inferiores Ø8 C345, trecho329 cm e ganchos10/10 cm; 19 estribos Ø6,3 C88 c/15. As posições nativas dos apoios são P11/P8 no CAD e P6/P7 no BIM. Essa correspondência não é equivalência por numeração.

**O Aviso 08 não foi encerrado.** A ajuda local oficial `aviso_08.htm` alerta para verificar a armadura superior, o escalonamento e a ancoragem no caso de inversão. A presença de barras contínuas não comprova, por si só, atendimento da ligação. Não se alterou o momento de cálculo para forçar uma armadura, não se retirou carga negativa apenas para eliminar o aviso e não se substituiu o cálculo por uma alteração gráfica.

## Medições e reprodutibilidade

Não se executou novo processamento integral nesta revisão. Os10 s CAD e11 s BIM pertencem à R223 e continuam sendo uma observação nativa por fluxo, sem duração total comparável. A emissão dos relatórios e a incorporação do complemento não receberam um cronômetro pareado; horários dos arquivos não foram usados para inventar duração. Tokens, custo e tempo exclusivo de inferência permanecem indisponíveis.

Reprodução: `python tcc-assistente/estudos/h03-r224/conferir.py <pasta-R224>`. O programa lê DOCX emitidos pelo Eberick; não edita o PRJ e não dimensiona barras. Cinco testes verificam leitura de valores em parágrafos separados, identificação e ordem de elementos, casos repetidos, casos diferentes e diferenças pequenas que não podem ser descartadas. Casos simples de vento contêm o sinal `+`; a classificação considera também o código entre parênteses, para não contá-los como combinações. Testes sintéticos do leitor são distintos da execução nativa efetivamente observada no Eberick/Builder. Não houve chamada real a IA pela automação testada.

## Pendências essenciais

Permanecem a verificação final das ligações e ELS local da V1, o Aviso08 da cobertura, o apoio inferior da W08 e as interfaces arquitetônicas ainda não demonstradas. A autoria Revit/AutoCAD permanece em revisão anterior ao cálculo. É necessário consolidar as correções comuns e as perdas de informação por fluxo, sem misturá-las, e concluir uma medição prospectiva de mesmo escopo para comparar produtividade total. As 14 sapatas com erro por fluxo continuam fora do dimensionamento autorizado; os cadastros da base representam apoios idealizados. **O conjunto ainda não está liberado como projeto executivo.**

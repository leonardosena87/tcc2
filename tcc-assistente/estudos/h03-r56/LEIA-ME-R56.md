# H03/R56 — alternativa de cobertura com vigas de 30 cm

Revisao academica de 29/10/2026, NAO EXECUTAR. Alteracao real em copias nativas independentes do Eberick 2025 Infinity, cada uma derivada de seu proprio ramo R54 congelado. A monografia, RVT e DWG de origem nao foram alterados. O estado da R54 permanece preservado.

## Alteracao e verificacao

Adotou-se como alternativa geometrica a altura de 30 cm em todas as vigas da cobertura N2, mantendo largura de 20 cm, projecoes XY e elevacao zero. No CAD alterou-se o trecho V3_1 e copiou-se apenas h para N2; no BIM alterou-se o trecho V1 e repetiu-se a copia de h apenas no N2. As opcoes carga de parede, carga extra, travamento, ambiente, elevacao, largura e demais propriedades permaneceram desmarcadas. A largura de 20cm ainda sobrepassa a parede acabada de 15cm e precisa de compatibilizacao de faces.

Salvaram-se, fecharam-se e reabriram-se ambos os PRJs. Leu-se individualmente uma amostra por ramo: CAD V4_1/N2 e BIM V4/N2, no trecho correspondente x=6,55..9,65, y=0. Ambas mostraram bw20, h30 e elevacao0. Nao se afirma leitura UI individual das 15 vigas exportadas. A auditoria IFC4 posterior a reabertura confirmou as 15 com altura30; 13 solidos tiveram altura reduzida, dois ja tinham30. O numero de solidos nao e o numero de vigas logicas. A selecao via lista incluiu somente N2. A integridade ZIP dos dois PRJs passou; arquivos nativos congelados em separado.

Em relacao ao proprio IFC R53, preservaram-se nomes/GUIDs/caixas envolventes/areas superiores dos 22 pilares, das 11 lajes e dos 17 solidos de vigas N1. Os campos brutos Q/G2 das lajes tambem permaneceram identicos; a carga continua parcial. Nas 15 vigas N2, preservaram-se nomes/GUIDs/projecoes XY/topo/areas superiores e verificou-se apenas a mudanca prevista de intradorso. O confronto CAD/BIM coincide por classe, caixas, areas superiores e campos brutos das lajes. Esse controle nao comprova identidade de toda malha nem vinculos analiticos.

Foram exportados tambem 11 IfcFooting por ramo, oriundos dos cadastros auxiliares de apoio da R54. Esses solidos padrao nao representam fundacoes dimensionadas e ficam excluidos dos quantitativos da superestrutura. O IFC manteve as bases geometricas dos pilares em +0,20m. Isso NAO valida a cota analitica da barra auxiliar de10cm nem seu comprimento efetivo ou liberacoes. Nao se infere apoio analitico por aparencia do solido. A primeira auditoria geometrica posterior a R54 foi realizada no estado R56; nao existe uma exportacao R54 retroativa.

## Compatibilizacao e cargas de paredes

Topo6,39 menos altura0,30 resulta em intradorso6,09m. Para piso3,25 e forro de referencia2,80, o plano do forro fica em6,05m: diferenca geometrica4cm. Nao se alterou a altura arquitetonica. Atualizaram-se os 59 trechos das 20 paredes R55; nenhum dos trechos com referencia de forro definida intercepta esse plano na triagem R56. Nao se verificou todo ambiente, espessura do forro, suspensao, instalacoes, tolerancias ou deformacoes futuras; portanto, nao se declara compatibilizacao executiva concluida.

A matriz R56 de paredes continua bruta, sem desconto de portas/janelas, acabamento sobre concreto, encontros, vergas/contravergas ou tara de esquadrias. A composicao hipotetica de1,565kN/m2 foi herdada da R55 e nao confirmada por fabricante. W08 continua com carga desconhecida, campo vazio. Nenhuma carga de parede foi aplicada. Nao somar essa matriz como quantitativo final. As alteracoes de intradorso mudam a altura da alvenaria, portanto reutilizar diretamente as alturas R55 seria incorreto.

As anotacoes CAD amarelas do esboco original ainda mostram secoes antigas em alguns trechos: sao textos de referencia desatualizados, nao dados estruturais correntes. O croqui BIM nao tem esses mesmos textos manuais. Registrar essa diferenca de documentacao sem transforma-la em defeito comprovado do IFC/DWG; atualizar ambos os arquivos de origem e a documentacao apos selecionar uma alternativa aceita por calculo.

## Tempos da etapa assistida

| Ramo | Abrir copia, alterar/copiar altura, salvar/reabrir e ler 1 amostra |
|---|---:|
| CAD | 3 min 52.908 s |
| BIM | 2 min 10.735 s |

Registros prospectivos UTC e relogio monotonico. Incluem raciocinio/latencia; CAD inclui descoberta de coordenadas de paineis flutuantes, ambiguidades de selecao e recuperacao de foco; BIM aproveita procedimento e opcoes ja conhecidos. Nao medem esforco humano ativo ou inferencia isolada de IA e nao permitem ranking dos fluxos completos. Exportacoes e execucao do auditor possuem registros separados; nao somar indiscriminadamente. A revisao e comum da concepcao no receptor, sem contagem de erro de transferencia.

## Limite estrutural e proximo passo

Nao se processou calculo nesta revisao. Reduzir h de55 para30cm reduz a inercia bruta retangular, a largura constante, para aproximadamente16,2% do valor anterior: satisfazer um plano de forro nao demonstra rigidez ou resistencia suficiente. Vao, cargas, armadura, fissuracao, fluencia e deformacoes precisam de avaliacao. A alternativa nao esta dimensionada nem aceita para execucao. Nao dispensar a possibilidade de novos apoios alinhados as paredes, conforme autorizacao do usuario, quando necessarios e compativeis com portas/janelas/circulacao.

Proximo: completar acoes, verificar lancamento/ligacoes/apoios e processar diagnostico no Eberick; avaliar ELU/ELS e deformacoes, revisando concepcao se necessario. Atualizar Revit/AutoCAD depois da escolha tecnica, com mesma referencia para ambos. Fontes operacionais oficiais: https://suporte.altoqi.com.br/hc/pt-br/articles/115002183633 e https://suporte.altoqi.com.br/hc/pt-br/articles/360014260893 .

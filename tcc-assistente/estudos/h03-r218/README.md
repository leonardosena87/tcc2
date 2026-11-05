# H03/R218 — Complemento local da V1 no Eberick

Por escolha do autor, incorporou-se a revisão transversal como desenho complementar externo somente da V1 do N0. O limite global dos estribos foi preservado. As cópias CAD e BIM ficam em `D:/TCC/outputs/H03-R218-APLICACAO-V1-NAO-EXECUTAR`.

## Alterações e conferência nativa

Na configuração individual da V1, marcou-se “Sempre adotar armadura de pele”. Após o cálculo individual, selecionou-se `2×2 Ø8`, isto é, quatro barras laterais, duas em cada face. A seleção foi gravada nos dois PRJ, que foram fechados e reabertos; a tabela Vão confirmou a retenção da opção Ø8. As capturas de releitura estão na pasta local. Permanecem o Aviso 19 e dois Avisos 98 relativos às ancoragens da pele.

O CAD exigiu recuperação de edição inconsistente e processamento global antes dessa alteração. Esse processamento teve avisos; não equivale a aprovação da estrutura. No BIM recalculou-se individualmente a V1 após alterar sua configuração. Não se alteraram os PRJ R217 de referência.

## Desenho complementar

Gerou-se DXF R12 e importou-se pela interface Arquivo → Importar → DWG/DXF, com unidade centímetros. Salvou-se o desenho em formato nativo `.cad` pelo gerenciador AltoQi Builder, associado ao pavimento N0 de cada fluxo. O BIM mantém o nome de nível `TCC-7a6267fd-N0`.

O desenho `R218-V1-COMPLEMENTO-EXTERNO` apresenta estribo Ø6,3 com espaçamento máximo de 9 cm, quatro barras laterais Ø8 e dois grampos horizontais Ø6,3 por posição. O esquema mostra 13 posições em 104 cm, com passo de aproximadamente 8,67 cm. A distribuição junto aos apoios, os ganchos e os comprimentos de corte dependem da verificação e do detalhamento final. A seção esquemática usa dois níveis de grampos para amarrar as duas barras de cada face; isso adapta a hipótese R217, que representava apenas duas barras laterais no total.

**O desenho complementar não muda os estribos do dimensionamento automático, que continuam Ø6,3 c/15, nem sua relação nativa de aço.** Essa diferença está escrita no próprio desenho. O detalhe automático foi salvo separadamente como `R218-V1-NATIVO-C15-REFERENCIA`. Não se declara o complemento como detalhamento executivo ou a V1 como plenamente verificada.

## Pendências

Concluir a verificação de ancoragem das barras longitudinais e laterais, definir dobras/ganchos e montagem dos grampos e conferir a transferência aos apoios idealizados. A documentação de base e suas hipóteses estão na R217. A R218 registra a aplicação documental e a alteração nativa da pele; não reproduz toda a análise estrutural. A correção é comum aos dois fluxos e não representa perda exclusiva de interoperabilidade CAD ou BIM.

## Reprodução e validação

`gerar_complemento.py` gera o desenho externo sem editar binários do programa. O DXF foi lido pelo Eberick e o desenho salvo foi inspecionado visualmente no Builder dos dois fluxos. `preservar.py` verifica os PRJ R217, o CRC dos PRJ R218, a existência dos desenhos e os hashes dos projetos dentro do backup ZIP. O código e o registro de auditoria ficam neste diretório; os arquivos nativos permanecem locais.

O intervalo total R218 atravessou uma interrupção entre sessões, sem cronômetro contínuo confiável. Portanto não se preenche uma duração de fluxo nem consumo de tokens. A recuperação global CAD e o recálculo individual BIM também impedem tratar esta revisão como ensaio de tempo pareado.

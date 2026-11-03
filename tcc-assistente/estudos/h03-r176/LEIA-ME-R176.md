# H03/R176 — comparação espacial dos receptores corrigidos

Comparação acadêmica somente leitura, sem dimensionamento ou aprovação estrutural. Os modelos de referência são o receptor CAD R172 e o BIM R175. Ambos foram copiados para consulta; seus PRJ e todas as fontes mantiveram os hashes de preparação.

## Procedimento e evidência

Exportou-se pela interface do Eberick o pórtico e as grelhas N1/N2 da cópia CAD R176. Para o BIM, reutilizou-se a exportação final R175, produzida após reprocessar e salvar o modelo; a proveniência e os hashes dos três arquivos estão registrados. Não se repetiu uma exportação BIM apenas para criar um segundo tempo. Não houve execução do SAP2000 nem nova análise estrutural nesta etapa.

As tabelas foram comparadas por coordenadas e extremidades de barras, retirando somente a dependência dos identificadores numéricos. A atribuição de seção foi comparada pelas propriedades completas da seção correspondente. Conservaram-se a orientação I-J, eixos locais, posições relativas e valores das cargas. Não se somou nem descartou carga duplicada, não se preencheu tabela ausente e não se ocultou diferença por arredondamento.

## Achados confirmados nos arquivos exportados

| Modelo | CAD: nós / barras | BIM: nós / barras | Coordenadas e segmentos sem direção | Seções por segmento |
|---|---:|---:|---|---|
| Pórtico | 123 / 147 | 123 / 147 | Iguais | Iguais |
| Grelha N1 | 467 / 838 | 467 / 838 | Iguais | Iguais |
| Grelha N2 | 443 / 794 | 443 / 794 | Iguais | Iguais |

Também coincidiram, após mapeamento espacial e na precisão exportada: os apoios do pórtico; os apoios e molas das grelhas; as tabelas de materiais, propriedades de seção, combinações, padrões e casos de carga. A igualdade é restrita ao conteúdo efetivamente exportado.

No pórtico e na grelha N2, as chaves posição/ação dos carregamentos nodais coincidiram. Nove vetores G2 diferiram apenas em F3, em nove pontos RC: RC01, RC02, RC03, RC04, RC05, RC06, RC09, RC10 e RC11. A maior diferença absoluta observada foi 0,0003 no campo F3 exportado em kgf. A entrada histórica CAD tinha menos casas decimais em alguns desses pontos. Os demais componentes desses vetores e os registros QT coincidiram. Não se adotou uma tolerância estrutural para apagar essas diferenças; elas permanecem listadas.

Há 56 trechos do pórtico, 72 da grelha N1 e 117 da grelha N2 com orientação I-J invertida entre as representações. Isso não significa novas barras nem alteração das seções. As tabelas de cargas locais distribuídas e pontuais continuam diferentes na comparação que conserva a orientação. Não foi efetuada transformação física completa dos vetores locais nem confronto independente dos esforços. Portanto, não se declara equivalência analítica integral.

## Tempo e integridade

A consulta/exportação CAD, desde abrir o menu até fechar a cópia, teve intervalo observado de **51,803 s**, incluindo ferramenta e orquestração. Esse intervalo não mede criação/importação/correção do fluxo CAD e não é pareado com uma nova exportação BIM. Não se usa esse número para estabelecer classificação de produtividade.

Os PRJ das cópias R176 permaneceram iguais aos controles de origem. Os arquivos de consulta ficam em `D:/TCC/outputs/R176-CAD-COMPARACAO-ANALITICA-NAO-EXECUTAR` e `D:/TCC/outputs/R176-BIM-COMPARACAO-ANALITICA-NAO-EXECUTAR`. As versões de trabalho continuam CAD R172 e BIM R175.

## Continuação necessária

Concluir o exame das cargas em coordenadas locais e dos esforços; integrar e conferir a escada nos dois receptores; resolver V16/janela J4 e apoio do reservatório; fechar as ações restantes, inclusive a vedação; dimensionar e tratar os avisos; então consolidar os resultados de retenção, correções e tempos por etapa. A comparação desta revisão é posterior às correções e não mede diretamente a retenção inicial do DWG/IFC. Não editar o trabalho escrito com conclusões de superioridade a partir deste controle.

Auditoria e diferenças completas: `R176-resultado.json`. Código: `comparar_receptores.py`. Quatro testes cobrem arquivos reais, troca de identificadores, carga deslocada com total constante, duplicação e tabela ausente.

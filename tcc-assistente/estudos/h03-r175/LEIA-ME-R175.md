# H03/R175 — reposição de cargas da cobertura no receptor BIM

Estudo acadêmico parcial, não executar. Não há dimensionamento nem aprovação estrutural nesta etapa.

## Alteração efetiva

A cópia R175 deriva da R174, preservada por SHA-256. Foram criados 13 nós nos eixos das vigas da cobertura N2 e lançadas as ações Adicional (G) e Q_TELHADO_MANUTENCAO (QT), conforme o plano histórico comum aos fluxos. Os cinco apoios de cobertura corrigidos na R174 foram herdados. Não se acrescentou novamente o forro às lajes.

O lançamento foi feito na interface do Eberick 2025 Infinity, com observações nativas e registro das seleções. A geometria analítica passou de 110 nós/134 barras para 123 nós/147 barras, pela subdivisão de trechos existentes; não foram criadas novas posições de pilares.

## Conferência executada

Após regenerar o modelo por análise estática e cálculo de deslocamentos do pórtico com rigidez configurada, exportou-se o pórtico em texto para auditoria. Não se executou SAP2000. Nos 13 nós, verificaram-se 26 vetores e 156 componentes, ações, coordenadas e conexão a dois trechos por nó. As tabelas de geometria, seções, materiais, vínculos, eixos, combinações e cargas distribuídas permaneceram iguais entre as duas análises R175.

O arquivo foi salvo, fechado e reaberto. Consultou-se uma amostra explícita de RC03 e RC11, nas duas ações: 24 componentes nativos. Isso é releitura amostral, não censo nativo dos 13 nós. O PRJ manteve o SHA-256 durante a releitura: `735ea69b5cbd0c95b92e88f6d25268452e5baf97a0c03ded19b4471a2974f849`. Preservou-se uma cópia congelada local.

## Resultados parciais e limites

O resumo passou a indicar peso próprio 75,72 tf; adicional 12,00 tf; acidental 17,01 tf; QT 1,78 tf; total 106,51 tf. Esses totais apresentados coincidem com o CAD na R172, mas não comprovam equivalência completa das cargas e condições dos modelos. O Eberick manteve aviso de relação de carga por área não usual. Não se realizou dimensionamento, flechas de lajes, rigidez fissurada ou análise dinâmica.

Também se conservaram as diferenças das reações transferidas da grelha: duas linhas nodais G2/QT fora dos 13 nós e diversas cargas pontuais nas barras mudaram no reprocessamento. Elas estão integralmente listadas no JSON; não se declarou que apenas 26 linhas do arquivo mudaram. A relação numérica observada entre os vetores nativos e os exportados foi 100, nas unidades declaradas por cada interface. Isso não calibra conversão física SI entre kN e kgf.

A primeira exportação realizada depois de criar os nós, antes de reprocessar, ainda continha 110 nós/134 barras e nenhum dos 13 pontos novos. Foi rejeitada e preservada em `analitico-nos-sem-cargas`. A exportação regenerada sem as novas cargas está em `analitico-apos-regenerar`; a final está em `analitico-cargas-final`. Esse achado exige controlar atualização do modelo ao analisar retenção de informações.

## Tempo observado

Do início do lançamento dos nós até o primeiro salvamento com G/QT: **25 min 36,001 s**. Sessão completa, incluindo criação, duas análises, exportações, correções de interface, fechamento, reabertura e releitura amostral: **33 min 46,554 s**. O primeiro intervalo está contido no segundo e não deve ser somado a ele. Ambos incluem orquestração e latência; não representam tempo puro de processamento nem um ensaio completo e pareado CAD versus BIM.

## Arquivos e continuação

- Projeto: `D:/TCC/outputs/R175-BIM-CARGAS-A1-A2-NAO-EXECUTAR/Projeto Eberick/R166-R160-3NIVEIS-CONFIG-CAD-NAO-EXECUTAR.prj`.
- Evidências: `D:/TCC/outputs/Cargas-H03-R175-A1-A2-BIM-NAO-EXECUTAR/`.
- Auditoria: `R175-resultado.json`; plano: `R175-preparacao-plano.json`.
- Código de auditoria somente leitura: `auditar_cobertura.py`; quatro testes de evidência real e rejeição de adulterações: `test_auditar_cobertura.py`.

Prosseguir com exportação atual do receptor CAD e comparação espacial das cargas e condições. A escada ainda não está integrada aos receptores; permanecem pendentes o conflito V16/janela J4, o reservatório, o fechamento das demais ações e a verificação/dimensionamento estrutural. Não há classificação final do melhor fluxo.

# H03/R84 — conferência da autoria R83 e DWGs por pavimento

Concluiu-se a conferência disponível da revisão de autoria R83, que harmoniza as alturas das vigas N2 com o estudo geométrico R56. O recorte não atualiza cargas ou materiais no Eberick nem aprova as seções. Os modelos e o trabalho escrito de origem foram preservados.

## Revit: leitura nativa após reabertura

Associaram-se as 62 unidades da proposta aos 62 elementos da exportação nativa por ID da criação, ID do Revit e UniqueId: 22 trechos de pilares, 29 vigas lógicas e 11 lajes. As categorias conferiram. Os 29 comprimentos de curva de viga e as 11 áreas de laje conferiram com a geometria nominal da proposta, na resolução de apresentação de seis casas decimais do exportador.

Essa exportação não contém coordenadas dos eixos, b/h, vínculos, cargas, armaduras ou modelo analítico. Portanto, a associação de 62 elementos e a igualdade dessas 40 medidas não constituem uma conferência completa das seções e das ligações. A criação R83 já contém sua própria verificação de parâmetros; não se amplia retrospectivamente o escopo da releitura. A amostra de seção N2 preservada em imagem continua sendo uma amostra.

## AutoCAD: desenho geral e desenhos por pavimento

A releitura DXF existente do DWG geral R83 preservou os 62 contornos e os textos da fonte. Compararam-se camada, fechamento, coordenadas dos vértices, conteúdo, posição de alinhamento, altura, justificação e rotação dos textos; handles não são critério de igualdade. Valores são normalizados para seis casas decimais. A comparação rejeita arcos, larguras especiais e geometria não planar, em vez de ignorá-los.

Gravaram-se e reabriram-se adicionalmente os DWGs N1 e N2 no AutoCAD Core Console 2027, com saída de processo 0 e sem limite de tempo atingido. O comando AUDIT retornou zero erros encontrados e zero corrigidos nos registros. A releitura confirmou:

| Arquivo | Contornos | Textos | Origem da referência | Resultado |
|---|---:|---:|---|---|
| N1 | 32 | 34 | 0,0 m | Preservado |
| N2 | 30 | 32 | 0,0 m | Preservado |

Cada fonte de pavimento também coincidiu com a geração independente a partir da proposta comum. As referências mantêm a origem do modelo; não se usa o deslocamento lateral da prancha geral ao importar um pavimento no Eberick. Linhas e textos no DWG continuam sendo representação CAD 2D, sem virar elementos estruturais calculáveis por esta conversão.

Tempos prospectivos do processo técnico: conversão N1 3,367 s, reabertura/extração N1 3,142 s, conversão N2 3,388 s e reabertura/extração N2 3,104 s. São tempos de processos do AutoCAD Core com seus comandos, não CPU puro, tempo total do fluxo ou comparação com o Revit. Não incluem desenvolvimento ou preparação. O JSON guarda os valores originais.

Não se abriu o AutoCAD gráfico para uma revisão visual da disposição nesta etapa. A conferência algébrica de textos não demonstra ausência de sobreposição gráfica. Os arquivos nativos permanecem locais em `D:/TCC/outputs/Autoria-H03-R84-AUDITORIA-NAO-EXECUTAR` e os autores gerais R83 permanecem na pasta R83.

## Evidências e limites

`R84-auditoria-autoria.json` registra os arquivos-fonte e hashes, as associações do Revit e a comparação do CAD geral. `R84-CAD-pavimentos-conferidos.json` registra origem, contagens, hashes dos DWG e tempos dos processos. Os registros completos e os nativos ficam locais; o código e os resultados selecionados ficam neste repositório.

Os seis testes novos exercitam mudanças de texto, vértices, multiplicidade, alinhamento e entradas não suportadas. São testes do instrumento, separados das execuções reais de AutoCAD e da leitura histórica do Revit. A suíte Node completa passou com 69 testes.

O teste de agrupamento BIM R81 não foi promovido automaticamente a solução técnica. A tentativa R85 de retomar o cadastro de Q no Eberick foi interrompida por falha de foco/captura de janela; os dois PRJ permaneceram byte a byte iguais às fontes R79. As cargas de telhado, reservatório, paredes, escada e demais verificações permanecem com os estados documentados, sem atualização fictícia.

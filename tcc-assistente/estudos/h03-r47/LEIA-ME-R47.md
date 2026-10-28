# H03/R47 — pilares nativos no receptor CAD

28/10/2026. **ESTUDO PRELIMINAR NÃO DIMENSIONADO — NÃO EXECUTAR.** A monografia não foi alterada.

## Resultado efetivamente obtido

O receptor CAD recebeu 11 posições de pilares por coordenadas digitadas em centímetros no croqui N1. Aplicou-se a cópia nativa dos pilares para N0 e N2, formando 22 trechos da superestrutura, entre +0,20/+3,20 m e +3,20/+6,39 m. A presença de 11 posições nos três croquis não corresponde a 33 trechos.

Trabalhou-se em cópia da base CAD R45 congelada, sem copiar o receptor BIM. O Eberick criou a associação da edificação durante o salvamento. O projeto foi salvo, fechado e reaberto pelo histórico do aplicativo, e exportou-se um segundo IFC4 com outro nome, preservando a primeira exportação.

Projeto nativo: `D:/TCC/outputs/H03_CAD_R47_PILARES_NAO_EXECUTAR/Projeto Eberick/H03_CAD_R47_PILARES_NAO_EXECUTAR.prj`.

## Lançamento e recuperação operacional

P1 a P10: seção 20 × 30 cm, rotação zero, centros conforme a proposta H03/R43. P11: centro (655; 390) cm e seção nominal de 30 cm em X por 20 cm em Y. O Eberick recusou a entrada b=30 e h=20, por exigir b≤h. Por isso, parametrizou-se b=20 e h=30 com rotação de 90°. A geometria física resultante corresponde à proposta comum.

Mantiveram-se os parâmetros iniciais visíveis de elevação zero, ambiente externo, vínculo engastado e verticalidade automática. Esses campos não foram aprovados como modelo analítico definitivo. Ainda não se harmonizaram materiais, cobrimentos e ações entre os receptores nesta revisão.

Registraram-se recuperação de foco e comandos sem alteração útil: abertura e cancelamento da conversão em fundações, tentativa de Ctrl+A que acionou a abertura de projeto, cancelada sem descartar o trabalho, e tentativa de seleção por arraste sem resultado útil. Selecionaram-se posteriormente os onze pilares pelos rótulos; o programa exibiu 11 selecionados antes da cópia para os dois níveis. A sobrescrita do primeiro IFC foi recusada e o segundo foi salvo como `R47-pos-reabertura.IFC`.

As recuperações pertencem ao esforço operacional assistido observado. Não foram contadas como falhas geométricas do DWG nem como correções de engenharia da concepção.

## Auditoria geométrica e qualidade das evidências

Os dois IFCs nativos contêm 22 IfcColumn, 0 IfcBeam e 0 IfcSlab. Conferiram-se as caixas envolventes em coordenadas globais, incluindo posição horizontal, duas dimensões da seção e cotas inferior e superior. Houve correspondência espacial única com os 22 identificadores da proposta, sem ausências, duplicações ou pilares adicionais. A tolerância de 0,00001 m é computacional e não representa tolerância de execução ou critério normativo.

Após a reabertura, os nomes, GUIDs e caixas envolventes dos 22 trechos coincidiram com a primeira exportação. O auditor também detectou três alterações sintéticas: remoção de um pilar, redução de 1 cm na altura e duplicação de um pilar. Esses controles exercitam a sensibilidade do instrumento e não são defeitos observados no arquivo real.

A validação de esquema IFC registrou oito erros em listas opcionais vazias de identificação, preservados no JSON e nos IFCs originais. A aprovação geométrica não equivale à aprovação do esquema nem à conformidade estrutural. Não se verificaram conectividade analítica, rigidez, armaduras, ELU/ELS ou estabilidade. As vigas e lajes desenhadas no fundo do croqui continuam referências gráficas.

Os nove testes pertinentes de `exchange.test.mjs` e `structural.test.mjs` passaram no Node. São testes locais/sintéticos do protótipo, distintos da operação real no Eberick e da auditoria dos IFCs exportados; não houve chamada real à IA nesses testes.

## Tempo e esforço da IA

Intervalo prospectivo: 21:38:49,963 a 22:08:28,647 UTC de 28/10/2026. Duração monotônica registrada: **1.778.682,9168 ms — 29 min 38,683 s**.

O intervalo abrange preparação da cópia, inicialização/abertura do Eberick, lançamento, cópia vertical, recuperação de comandos, consulta à documentação, desenvolvimento e execução do auditor, exportações, reabertura, latência de IA/ferramentas e retomada de contexto. A primeira tentativa de gravar o cronômetro falhou por variável não declarada; o registro corrigido inclui essa recuperação. A consolidação documental posterior ficou fora do intervalo.

Não se mediram isoladamente tempo ativo humano, duração interna de inferência, tokens ou custo da IA; esses valores permanecem indisponíveis, e não zero. A atuação da IA nesta etapa compreendeu preparação de arquivos, leitura e decisão sobre estados de tela, operação do programa e programação/conferência do auditor. Não houve chamada de teste à API de IA nos testes do auditor.

Trata-se de ensaio exploratório assistido. Não se deve comparar esse valor isolado com a importação BIM, somar subintervalos sobrepostos ou atribuir a diferença à produtividade intrínseca dos programas. Os dois ramos ainda não atingiram o mesmo estado de aceitação.

## Estado dos dois ramos ao concluir R47

| Conteúdo calculável | CAD R47 | BIM R46 preservado |
|---|---:|---:|
| Trechos de pilares | 22 | 22 |
| Vigas lógicas | 0 | 29 |
| Sólidos de viga exportados | 0 | 32 |
| Lajes | 0 | 0 |
| Cálculo estrutural desta H03 realizado | Não | Não |

O recebimento das 29 vigas BIM foi conferido na R46; a R47 verificou por hashes que esse estado anterior permaneceu preservado. A diferença entre 29 vigas lógicas e 32 sólidos não foi classificada automaticamente como erro: decorre dos recortes geométricos identificados na auditoria anterior.

## Preservação e sequência

Confirmaram-se 36 arquivos de origem protegidos e os 81 arquivos do manifesto da etapa anterior, todos sem alteração. Preservaram-se sete arquivos nativos de R47, incluindo PRJ, PRJ-CAD, INI e associação da edificação, na pasta `congelado`. Isso não constitui teste de portabilidade em outro computador.

O roteiro `R48-vigas-a-lancar-proposta.json` conserva as 29 vigas da proposta comum como dados para o próximo lançamento; não prova que elas já existam no receptor CAD. A próxima revisão deve partir da cópia R47 e medir o lançamento/conferência das vigas. Depois permanecem as 11 lajes em cada ramo, cargas completas, apoio do reservatório, compatibilização, parâmetros de análise, apoios idealizados da superestrutura e verificações estruturais. Fundos de croqui não substituem esses elementos ou entradas.

Documentação operacional consultada: [lançamento de pilares](https://suporte.altoqi.com.br/hc/pt-br/articles/360001109753) e [cópia entre pavimentos](https://suporte.altoqi.com.br/hc/pt-br/articles/360012136193), AltoQi. A evidência do resultado reside nos arquivos IFC/JSON desta revisão.

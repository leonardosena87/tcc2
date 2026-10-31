# H03/R95 — recepção experimental do IFC com propriedades de materiais

Criou-se um receptor independente no Eberick 2025 Infinity para o derivado da R94 que contém as propriedades dos materiais. A autoria Revit R93, os três IFCs brutos R94 e os receptores principais CAD/BIM foram preservados. Esta revisão é ensaio de intercâmbio com configuração inicial do programa, sem carregamentos completos, processamento estrutural ou uso para execução. Não substitui o ramo BIM principal R79/R85.

Projeto experimental: `D:/TCC/outputs/H03_R95_MATERIAIS_IFC_NAO_EXECUTAR/Projeto Eberick/H03_R95_MATERIAIS_IFC_NAO_EXECUTAR.prj`.

## Preparação explícita

A entrada provém do IFC2X3 Coordination View da R94, com propriedades de materiais habilitadas; não é a variante CV2.0. Retiraram-se somente os níveis +0,00 e +3,00 m, comprovadamente vazios, preservando +0,20 / +3,20 / +6,39 m. Reaplicou-se a regra histórica de adaptação nominal, que reconstruiu 17 geometrias de pilares/vigas e preservou os outros 45 registros de produtos. O arquivo derivado foi relido: 62 identidades conferidas, geometria nominal aprovada pelo critério do adaptador, sem mensagens de esquema após a limpeza prevista.

Após o tratamento, compressão, Young, densidade e Poisson continuaram iguais à leitura nativa R93 nos 62 elementos. A preparação técnica do primeiro script durou 2,1299358 s, excluindo interface, decisões e auditorias anteriores/posteriores. Uma segunda execução, com o script de reprodução mantido nesta pasta, gerou IFC nominal com o mesmo SHA256. Esse subintervalo não é esforço completo de preparação nem duração do fluxo BIM.

`adaptador_base_historico.py` é cópia preservada do adaptador existente em `D:/TCC/tcc-assistente/estrutural/ifc_intercambio.py`. Não se editou o original. Sua advertência textual antiga sobre C25 deve ser lida junto da evidência nova: a R93/R94 confirma compressão cadastrada de 25 MPa, mas não valida integralmente o material. A adaptação é documentada como transformação intermediária; não se apresenta o derivado como exportação bruta do Revit.

## Recepção e geometria

O assistente recebeu os três níveis e a opção **Importar pilares e vigas**. Manteve-se a altura inicial de 100 cm e o nível de solo 0,00 cm como estado do assistente, sem interpretar isso como fundação real. Utilizou-se **Configuração inicial do programa**, explicitamente diferente da cópia principal já configurada para o estudo.

O programa exibiu o aviso de elementos importados com seção retangular e necessidade de conferência. O relatório nativo DOCX listou 51 origens, conciliadas pelos IDs da leitura Revit: **22 trechos de pilares e 29 vigas**, sem falta, repetição ou origem desconhecida nesse conjunto. O relatório não demonstra preservação de conectividade ou propriedades de cálculo.

Antes de editar qualquer entrada estrutural, salvou-se o receptor e congelaram-se seus 12 arquivos, com hashes conferidos. A consulta de materiais foi cancelada sem aplicar alterações; o PRJ permaneceu com o mesmo hash recebido. Exportou-se IFC4 completo, com PropertySets, sem quantitativos, sem agrupamento de trechos e sem armaduras 3D. A saída contém **22 IfcColumn, 32 IfcBeam e zero IfcSlab**. Os 32 sólidos correspondem a 29 vigas lógicas pelo critério de cobertura axial nominal.

A conferência espacial associou os 22 pilares e as 29 vigas, sem partes de vigas sem correspondência ou duplicadas. O critério é de caixas envolventes e cobertura axial, descontando faces dos pilares, com tolerância computacional de 0,00001 m. Não comprova vínculos, continuidade analítica, armaduras ou segurança. Os três controles em memória detectaram remoção de parte de viga, alteração de 1 cm na altura e duplicação de parte.

O IFC4 do receptor apresentou oito mensagens de validação de esquema, mantidas nos dados da auditoria. Não se modificou o arquivo para ocultá-las. As onze lajes presentes na entrada não apareceram como lajes estruturais nessa saída completa; a existência delas no modelo externo vinculado não equivale à conversão em elementos calculáveis.

Ao fechar, salvou-se a configuração do destino de exportação na cópia de trabalho. O hash desse PRJ mudou; o estado recebido anterior continua congelado separadamente. A cópia de trabalho foi reaberta no mesmo computador, sem aviso de associação observado, e o pórtico foi exibido em 3D. Não se realizou uma segunda exportação geométrica após reabrir nem teste em outro computador; não se declara releitura integral dos parâmetros ou das 54 partes após a reabertura.

## Materiais no receptor: observação e limite causal

O diálogo de materiais mostrou C25 para vigas, pilares e lajes, CAA II, agregado de 19 mm e cobrimentos externos/internos de 3 cm para vigas/pilares e 2,5 cm para lajes. A presença de uma linha de configuração para lajes não prova que existam lajes nativas no receptor.

Na classe C25, observou-se fck 25 MPa, γc 1,4, peso específico de 25 kN/m³, abatimento de 5 cm, agregado granito e cimento CP-IV. O módulo estava marcado para obtenção a partir do fck: **Eci 28.000 MPa e Ecs 24.150 MPa**. A origem possui Young de 20.500 MPa nas lajes e 23.250 MPa nas vigas/pilares, com a ressalva de que esse campo não é automaticamente Eci/Ecs. Portanto, não se afirma que o módulo tenha sido transferido diretamente para o parâmetro de cálculo. Há também diferenças entre configurações iniciais e as hipóteses adotadas para agregado/abatimento/cimento, ainda sem correção nesta cópia.

O IFC4 exportado apresentou classe C25 em todos os 54 sólidos de pilares/vigas. Isso confirma a identificação exibida/exportada pelo receptor, **sem provar que a classe veio do IFC de entrada**, pois coincide com uma possível configuração inicial do programa. Um controle adicional com entrada de propriedade distinta e inicialização idêntica é necessário para atribuição causal. Não se rotula essa coincidência como transferência confirmada, nem como perda demonstrada.

## Tempo e retomada

O recorte prospectivo de recepção foi **206,3124431 s (3 min 26,312 s)**, da tentativa de preencher o caminho do IFC ao retorno após Ctrl+S do receptor criado. Inclui falha de acessibilidade, recuperação, assistente, planificação, aviso, relatório, leitura e deliberação intercaladas. Exclui abertura do aplicativo, preparação do IFC, auditoria completa posterior e reabertura. Não é duração total BIM e não é diretamente comparável à preparação CAD. Não foi somado aos intervalos internos como se fossem independentes.

`R95-preparacao.json` é o marco anterior à importação; seu campo `receiverImported=false` é histórico. O estado posterior está em `R95-recepcao-e-parametros.json`, `R95-auditoria-receptor-FINAL.json` e `R95-estado-final.json`. Os arquivos nativos, IFCs, DOCX e congelamento permanecem em `D:/TCC`; não entram no repositório público.

Para reproduzir a preparação, executar `preparar_recepcao.py` com Python 3.12 e argumentos `--deps`, `--source`, `--proposal`, `--registry`, `--native`, `--out`; a pasta de saída deve ser nova. Para a auditoria do receptor, executar `auditar_receptor.py` com `--deps`, `--ifc`, `--proposal`, `--out`; o relatório deve ser novo. O auditor utiliza apenas as definições geométricas derivadas da R17, generalizando a contagem de pilares para a proposta fornecida, sem executar o código histórico de entrada/saída. Os scripts foram executados nos arquivos reais desta revisão e os controles de sensibilidade passaram. Não houve nova chamada real à API de IA por esses scripts.

Continuam abertos o alinhamento integral dos materiais e cobrimentos, a determinação da origem efetiva dos parâmetros no receptor, as cargas e apoios idealizados, as verificações ELU/ELS e o ensaio comparativo final sob o mesmo critério de aceitação. O tempo total e a classificação dos dois fluxos permanecem indisponíveis. Não se alterou a monografia.

# H03/R234 — vigas de N1 no fluxo CAD

Etapa executada em 6 de novembro de 2026, em cópia independente da R233, salva em `D:/TCC/outputs/H03-R234-CAD-VIGAS-N1-NAO-EXECUTAR/CAD`. O arquivo nativo conserva o nome interno `R228-CAD-DWG-BRUTO-NAO-EXECUTAR.prj`. Não houve alteração no PRJ R233 nem na origem CAD, conforme hashes registrados.

## Desenvolvimento e conferência

O plano de lançamento contém as 16 vigas de N1 extraídas do DXF de retorno do AutoCAD R225. Conferiram-se polilinhas fechadas, rótulos de seção e metadados XDATA. O modelo Revit não foi usado para preencher o ramo CAD.

No Eberick 2025 Infinity, lançou-se cada viga retangular com a seção do CAD, elevação zero e topo no pavimento +3,20 m. Utilizaram-se os pilares existentes como pontos de captura. Para a travessa CAD V15-N1, utilizou-se entrada absoluta em centímetros: (440; 303,57833333) até (655; 303,57833333). Conservou-se a numeração automática do receptor, com correspondência por geometria no relatório de auditoria.

As 16 identidades CAD correspondem a 18 trechos de viga no controle IFC. A interseção da travessa V15-N1, denominada V16 no receptor, subdivide as vigas longitudinais CAD V9-N1 e V13-N1. A auditoria verifica eixo, seção, cota e cobertura da projeção; nas interseções, considera os intervalos ocupados pelos sólidos interceptantes. Essa operação geométrica não comprova os vínculos analíticos.

Confirmou-se associação única de cada trecho à origem CAD, C-25, cobrimento de 3 cm e correspondência das seções, com tolerância computacional de 0,1 mm, sem caráter normativo. Os 35 trechos de pilar e 15 trechos de viga N2 da R233 conservaram GUIDs, nomes, geometria, níveis e propriedades. Na comparação entre revisões, excluiu-se somente o número STEP `id` acrescentado pelo IfcOpenShell às propriedades.

Ao abrir a cópia para edição, aceitou-se a rotina nativa “Verificar projeto danificado”; não se atribuiu causa ao aviso. Depois do lançamento, salvou-se, fechou-se e reabriu-se a R234 sem novo aviso. A nova exportação confirmou os mesmos 68 sólidos e as mesmas identidades, geometrias e propriedades do controle anterior à reabertura.

## Tempo observado

Registrou-se o início no primeiro diálogo de lançamento em 06/11/2026 às 18:05:26,975 UTC e o término após salvar às 18:44:44,903756 UTC: **39 min 17,9 s brutos**. O intervalo inclui interrupções e reinicialização da sessão de controle. Não há cronômetro monotônico preservado nem medição líquida de trabalho ativo. Mantêm-se `interrupted=true`, `monotonicSeconds=null` e `netActiveSeconds=null`; não se usa esse intervalo para calcular ganho percentual CAD/BIM. A diferença foi calculada interpretando ambos os registros como datas ISO 8601, sem conversão regional ambígua.

O intervalo exclui a preparação da cópia, a verificação inicial, a auditoria posterior e o backup. Não representa cálculo estrutural nem tempo total do fluxo.

## Continuidade

Nesta cópia faltam as duas vigas da escada em N0/PATAMAR, lajes, escada, cargas e conferência dos vínculos. O lançamento e a persistência geométrica não equivalem à aprovação estrutural. Os modelos já calculados R227 e suas pendências permanecem separados desta rodada de recepção dos arquivos R225.

`auditar.py` confere o DXF e os IFC efetivos; `consolidar.py` produz o resultado público e verifica todos os hashes e o CRC do backup. Os testes do suplemento são distintos dessas verificações no Eberick e não comprovam dimensionamento.

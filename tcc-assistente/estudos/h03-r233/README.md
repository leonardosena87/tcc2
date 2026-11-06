# H03/R233 — vigas da cobertura no fluxo CAD

Etapa executada em 6 de novembro de 2026, em cópia independente do CAD R232. A edificação está em `D:/TCC/outputs/H03-R233-CAD-VIGAS-N2-NAO-EXECUTAR/CAD`. O nome interno do arquivo nativo permanece `R228-CAD-DWG-BRUTO-NAO-EXECUTAR.prj`. O PRJ R232 foi preservado e seu hash conferido.

## Desenvolvimento e qualidade da informação

Extraíram-se do DXF de retorno do AutoCAD R225 as 14 vigas de N2, com eixo, largura, altura, cota e identificador. A preparação gravou o plano de lançamento e copiou o projeto antes da edição. Não se utilizou o Revit como fonte para preencher este ramo.

No Eberick 2025 Infinity, usou-se o comando nativo de viga retangular, seção 20 × 30 cm, elevação zero, cota de pavimento +6,39 m e fixação pelo eixo. A primeira viga foi lançada com coordenadas absolutas; as demais, por captura dos nomes dos pilares existentes, seguida de confirmação pelo eixo. Mantiveram-se as numerações automáticas do receptor. A auditoria associa pela geometria, registrando a correspondência entre as identidades CAD e os nomes nativos.

Ao abrir a cópia R233, o Eberick recomendou executar “Verificar projeto danificado”. Executou-se a rotina antes do lançamento. Não se atribuiu uma causa ao aviso. A exportação posterior confirmou a retenção dos identificadores IFC, nomes, posições, seções, intervalos verticais e valores das propriedades dos 35 trechos de pilar da R232. Na comparação das propriedades entre revisões, ignorou-se somente o campo `id` acrescentado pelo IfcOpenShell, que corresponde ao número STEP do conjunto e muda ao inserir entidades; nenhum valor de engenharia foi excluído.

O controle contém 15 sólidos de viga, associados de forma única às 14 origens CAD. A viga CAD V2-N2 corresponde a dois trechos de V2 no receptor, separados pelo apoio intermediário P10. A projeção completa foi conferida pela união dos trechos de viga com os intervalos ocupados pelos pilares; não se somaram trechos sobrepostos nem se confundiu o espaço do pilar com uma lacuna de viga.

Todas as seções e topos correspondem ao DXF, com tolerância computacional de 0,1 mm, sem caráter normativo. O controle atribui C-25 e cobrimento de 3 cm às vigas. Fechou-se e reabriu-se a edificação; a nova exportação conservou os 50 sólidos, seus GUIDs, nomes, níveis, geometria e propriedades. Não houve novo aviso na reabertura observada.

## Tempo e limitações da medição

O intervalo prospectivo começou em 06/11/2026 às 17:09:15,167 UTC e terminou no salvamento observado às 17:41:40,298 UTC: **32 min 25,1 s brutos**. Esse intervalo contém a interrupção do turno e a retomada. Não há medição válida do tempo ativo nem marcação suficiente para descontar a pausa com precisão. Conserva-se o registro bruto e marca-se `interrupted=true`, `netActiveSeconds=null`. Não se usa esse valor para ranquear produtividade ou calcular ganho percentual entre os fluxos.

O intervalo exclui cópia, abertura/verificação nativa anterior, exportação e auditoria posteriores. Não é tempo de processamento do cálculo nem tempo total CAD. Os intervalos de pilares R232 continuam separados: 15 min 43,3 s de lançamento inicial e 50,8 s de correção de continuidade.

## Pendências

Nesta cópia ainda faltam 16 vigas de N1 e as duas vigas da escada nos outros níveis, além de lajes, escada, cargas e verificação dos vínculos. A auditoria de projeção não comprova conectividade analítica, dimensionamento, ancoragem ou aprovação para execução. Os modelos calculados R227 e as verificações estruturais locais pendentes permanecem separados desta rodada de recepção e lançamento.

Os scripts `preparar.py` e `auditar.py` executam a preparação da cópia/plano e a conferência dos arquivos efetivos. Os 82 testes automatizados do `tcc-assistente` foram aprovados nesta rodada; não representam teste dentro do Eberick. Nenhuma chamada à IA de serviço externo foi necessária para esses scripts.

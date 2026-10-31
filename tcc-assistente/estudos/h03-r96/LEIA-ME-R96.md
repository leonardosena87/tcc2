# H03/R96 — controle da recepção da compressão do concreto

O ensaio alterou exclusivamente a propriedade numérica de compressão do IFC derivado, de 25 para 30 MPa, e repetiu a recepção em uma edificação independente com **Configuração inicial do programa**. A especificação do estudo continua C25. A entrada de 30 MPa é uma perturbação experimental identificada como **NÃO EXECUTAR**, sem adoção no projeto principal.

## Preparação e isolamento

A origem foi `H03-R95-geometria-nominal.ifc`, SHA256 `5a47ec8e9a1602374f947778a22630dd746aefe71a891c2cd46b6e2ed94518d5`. O controle tem SHA256 `a161b1164c9bf5c36fef9564673b982974977e83b3fb33c00f6bcc765b1cc2ac`. A entidade STEP 2451, compartilhada pelos materiais, foi a única alterada: `IfcPressureMeasure` de 25.000.000 para 30.000.000 Pa. Mantiveram-se os demais registros STEP, as 62 identidades, as malhas e as outras três propriedades numéricas da leitura R93. Não se tratou a modificação de uma propriedade compartilhada como 62 edições independentes.

O script `preparar_controle.py` exige entrada esperada, pressão em Pascal sem prefixo e saída nova. Verifica a alteração única, o esquema IFC, a releitura e a preservação da origem. Uma reprodução em pasta separada gerou o mesmo hash do controle.

## Recepção real no Eberick

Criou-se e salvou-se `D:/TCC/outputs/H03_R96_CONTROLE_30MPa_NAO_EXECUTAR/Projeto Eberick/H03_R96_CONTROLE_30MPa_NAO_EXECUTAR.prj`. Mantiveram-se os três níveis, o solo 0 cm, a altura inicial de 100 cm e a opção de importar pilares/vigas, conforme o assistente da R95. Esse estado inicial não define fundações reais. O aviso de seções retangulares foi reconhecido e o relatório nativo foi preservado. Nenhuma carga ou análise estrutural foi aplicada.

O relatório conciliou 51 origens pelos IDs: 22 trechos de pilares e 29 vigas, sem repetição, falta ou ID desconhecido nesse conjunto. Antes da consulta, congelaram-se os 12 arquivos presentes. O congelamento inclui um arquivo temporário de bloqueio do Word, apenas como registro local; esse arquivo e os demais binários não entram no Git público.

A leitura visual de **Materiais e durabilidade**, com aplicação ao projeto inteiro, mostrou C25 para vigas, pilares e a linha de configuração de lajes. Ao selecionar C25 em **Classes de concreto**, observou-se fck de 25 MPa, γc 1,4, fcd 17,86 MPa, Eci 28.000 MPa e Ecs 24.150 MPa, com módulo derivado do fck. O peso específico mostrou 25 kN/m³, o abatimento 5 cm, agregado granito, dimensão 19 mm e cimento CP-IV. São valores iniciais desta cópia, sem alinhamento final às hipóteses do estudo. Cancelaram-se os dois diálogos sem aplicar mudanças.

Exportou-se a edificação completa em IFC4 pelo intercâmbio BIM. A saída contém 22 `IfcColumn`, 32 partes `IfcBeam` e zero `IfcSlab`. As partes correspondem a 22 pilares e 29 vigas lógicas no critério geométrico. **Todos os 54 sólidos exportados indicam C25**, apesar da propriedade de 30 MPa presente nos 62 elementos da entrada.

A conferência por caixas envolventes e cobertura axial passou, com tolerância computacional de 0,00001 m. Os controles em memória detectaram remoção de parte de viga, alteração de 1 cm na altura e duplicação. Não se verificou conectividade analítica, armadura ou capacidade resistente. A saída do receptor apresentou oito mensagens de esquema, preservadas integralmente. A ausência de lajes na saída estrutural completa não implica ausência no modelo externo vinculado.

## Interpretação para a comparação

Na R95, a entrada de 25 MPa coincidiu com C25 na saída. Na R96, a alteração isolada da propriedade para 30 MPa **não atualizou a classe nativa exportada**, sob essa configuração e esse caminho de importação. A coincidência anterior não constitui evidência de transferência causal da compressão para a classe de cálculo.

O resultado delimita uma propriedade, um importador, uma inicialização e esta edificação. Não se conclui que todo IFC perde materiais, que o Eberick ignora todas as propriedades ou que os demais formatos apresentam o mesmo comportamento. A perturbação tampouco investiga se outro nome de campo ou mapeamento seria reconhecido. O achado fundamenta a necessidade de conferir/configurar o receptor; não mede ainda o número ou o tempo das correções do ramo BIM principal.

As 54 partes exportadas, as 51 origens importadas e os 62 elementos da entrada representam unidades diferentes. Não se apresentam como 54 erros ou 54 intervenções. Não se atribui vantagem global ao CAD ou ao BIM a partir desse controle.

## Tempo, preservação e reprodução

O recorte prospectivo durou **218,3104342 s (3 min 38,310 s)**, da digitação do caminho IFC ao retorno após Ctrl+S. Inclui assistente, espera, relatório e trabalho intercalado. Exclui preparação, auditoria posterior e duração total do fluxo. Não se compara diretamente com o recorte R95 de 206,3124431 s, pois inclui navegação e esperas variáveis. Os totais CAD/BIM e o ranking permanecem indisponíveis.

O PRJ manteve o hash recebido `0f71edecb345d51793a02870d603cddaafe9d61e8c72319fc2734c58f40d1033` após as consultas canceladas e a exportação. Os 12 arquivos congelados foram conferidos. Não se fechou/reabriu a R96 nem se realizou novo teste em outro computador. A monografia e os receptores principais não foram editados.

Os arquivos nativos e IFCs estão em `D:/TCC/outputs/Controle-H03-R96-MATERIAL-30MPa-NAO-EXECUTAR` e na pasta de projeto nativo indicada acima. `R96-preparacao.json` é anterior à importação; seu campo `receiverCreated=false` é histórico. O estado posterior está em `R96-estado-final.json`.

Para reproduzir a preparação, usar Python 3.12: `preparar_controle.py --deps D:/TCC/work/ifc/deps --source <IFC R95> --out <novo IFC>`. A auditoria geométrica usa `../h03-r95/auditar_receptor.py --deps <deps> --ifc <IFC4 receptor> --proposal <proposta R83> --out <novo JSON> --revision H03/R96`. Acrescentou-se apenas o argumento opcional de revisão; a execução sem esse argumento reproduziu integralmente o relatório R95 anterior. `consolidar_controle.py --root <pasta R96> --native <leitura nativa R93> --previous <auditoria R95>` concilia os arquivos reais e recusa saída existente. Ele não automatiza a leitura da interface; o registro `R96-leitura-UI.json` identifica essa procedência.

Executou-se a preparação/reprodução nos arquivos reais, a auditoria do IFC4 com três controles de sensibilidade, a regressão integral R95 e nove testes Node de procedência/tempos. Esses testes não são chamadas reais de IA nem verificações estruturais. A recepção e a consulta de parâmetros foram realizadas dentro do Eberick.

Continuam pendentes o alinhamento integral de materiais, cargas e apoios dos ramos principais, as verificações ELU/ELS e o ensaio final com critérios e cronometragem equivalentes.

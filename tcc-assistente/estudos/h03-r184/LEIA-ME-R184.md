# H03/R184 — controle de ancoragem; alternativa de gancho pendente

Estudo preliminar, não executar. A pasta nativa contém `ENSAIO-GANCHO` por ter sido preparada para esse objetivo; **o nome não comprova que o gancho foi selecionado ou ensaiado**. A revisão terminou com ancoragem reta e sem recalculação com gancho. Não se concluiu comparação pareada nesta etapa.

## O que foi executado

Criaram-se duas cópias independentes dos receptores R182, conferindo a igualdade inicial dos PRJ. Os PRJ de referência R182 permaneceram iguais aos hashes de início da R183. A cópia BIM R184 não foi aberta para ensaio e permaneceu igual à inicial. As exportações IFC/SAP existentes nas pastas copiadas são herdadas, sem representar nova exportação R184.

Na abertura da cópia CAD ocorreu aviso de erro na última edição, semelhante ao aviso registrado na preparação R182. Executou-se a verificação nativa somente na cópia experimental. Como essa verificação limpa os resultados, repetiu-se o controle com ancoragem reta antes da alternativa. A seleção incluiu vigas, pilares e lajes de N1/N2 e escadas de N1; excluiu N0 e fundações. Manteve-se o cálculo de deslocamentos do pórtico com rigidez configurada, sem flechas de lajes ou análise dinâmica.

O controle terminou como “Estrutura processada com avisos”. O relatório nativo registrou **7 s de processamento total, com 2 s de dimensionamento já contidos nesse total**. A planilha Escadas → Positivo mostrou LE1/LE2 calculados e LE3 com D31; o resultado por bitola mostrou A11 para 6,3; 8; 10; 12,5 e 16 mm. Portanto, o controle reproduziu a falha do lance inferior antes de qualquer seleção confirmada de gancho.

Preservou-se uma cópia do PRJ imediatamente após o controle em `D:/TCC/outputs/Escada-H03-R184-ENSAIO-GANCHO-NAO-EXECUTAR/CAD-controle-reta.prj`. Essa cópia representa o controle com erro e não um projeto corrigido. O arquivo de trabalho experimental foi salvo novamente após a restauração das opções de tela; não se afirmou igualdade binária entre essas duas gravações nem retenção de geometria por nova exportação.

## O que não foi executado

A lista de tipo de ancoragem perdeu foco repetidamente durante o controle automático. Nas tentativas de selecionar “gancho”, a opção vizinha de evitar transpasse chegou a ser acionada. A conferência visual detectou a alteração e restaurou essa opção para desmarcada; não houve processamento enquanto a opção estava alterada. A última captura confirmou **reta**, com a opção de evitar transpasse desmarcada. Não se contou a tentativa como correção ou como teste de gancho bem-sucedido. As capturas intermediárias das tentativas não são evidência de gancho aplicado.

O teste de gancho fica pendente. A próxima intervenção deve confirmar visualmente a seleção antes de qualquer recalculação, preservar as outras configurações e registrar quais elementos foram recalculados. Não se alteraram deliberadamente os limites de esforços, a largura da barra inferior, as seções ou os vínculos para eliminar A11.

## Limites dos tempos

Os 7 s pertencem somente ao processamento nativo do controle CAD desta revisão. O BIM não possui nova medição R184; o teste de gancho tampouco possui tempo medido. Esses campos permanecem ausentes, sem substituir por zero. O intervalo entre clique e primeira confirmação inclui latência das ferramentas e observação, e não equivale ao tempo ativo de edição. Nenhum desses registros permite ordenar a produtividade integral de CAD e BIM.

Permanecem as pendências da R183: apoio físico e ancoragem da base, cisalhamento, ELS, reconciliação das vigas, conflito V16/J4 e comparação completa dos fluxos. Não se alteraram Revit, AutoCAD ou monografia nesta revisão.

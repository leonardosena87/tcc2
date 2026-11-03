# H03/R191 — ensaio de ancoragem na laje adjacente

Estudo preliminar, não executar. Na cópia CAD derivada de R189, habilitou-se “Permitir ancoragem na laje adjacente”. Manteve-se o gancho da R188 e a largura hipotética de 20 cm na barra ordinária inferior de LE3. Não se criou pilar nem se modificou geometria física. Essa largura de ensaio não representa fundação ou apoio dimensionado.

O controle anterior à intervenção e o novo processamento apresentaram **LE1 e LE2 calculados, LE3 com D31 e A11 nas cinco bitolas: 6,3; 8; 10; 12,5 e 16 mm**. O erro e a opção habilitada foram conferidos novamente após salvar, fechar e reabrir o PRJ. A hipótese testada não resolveu o problema de ancoragem.

Cada relatório nativo registrou **7 segundos de processamento total, incluindo 2 segundos de dimensionamento**. Os intervalos externos entre comando e confirmação foram 18,590 s no controle e 17,417 s no ensaio, incluindo a latência de observação. Não se trata de tempo ativo, de duração completa do fluxo ou de comparação CAD/BIM. Não houve réplica BIM desta intervenção.

Ao abrir a cópia, o Eberick apresentou aviso de integridade. Executou-se a verificação nativa e recalculou-se o controle antes da mudança. A tentativa de salvar esse controle com Ctrl+S não persistiu: `CAD-controle-apos-integridade.prj` conserva exatamente os bytes da fonte R189 e **não comprova gravação do controle recalculado**. Esse artefato e o registro de gravação ambíguo permanecem locais e foram excluídos do pacote versionado. O controle efetivamente calculado é comprovado pelo relatório DOCX e pela leitura nativa. A gravação final do ensaio ocorreu pelo botão de disco, com novo hash e reabertura verificada.

Os resumos de pilares, vigas e lajes coincidiram; eles não incluem uma aprovação de LE3. Não se exportou novo IFC/SAP nem se comprovou equivalência analítica completa. Os controles R182 e a fonte R189 permaneceram com os hashes anteriores.

A opção adjacente pressupõe concreto disponível e geometria compatível de ligação; habilitá-la não comprova que a armadura esteja ancorada. A falha persistente exige identificar o bordo governante e conferir o encontro entre lance e patamar. A dispensa de verificação ao cisalhamento, herdada das configurações, continua pendente de revisão. Não se elevaram limites de momento ou tração para suprimir o erro. [Documentação AltoQi sobre largura do apoio](https://suporte.altoqi.com.br/hc/pt-br/articles/115003201013).

Mantiveram-se os arquivos principais de comparação anteriores. A monografia não foi alterada. O arquivo experimental está em `D:/TCC/outputs/R191-CAD-ENSAIO-ANCORAGEM-ADJACENTE-NAO-EXECUTAR/Projeto Eberick/H03_CAD_R49_LAJES_NAO_EXECUTAR.prj`; seu hash e as limitações constam em `R191-resultado.json`.

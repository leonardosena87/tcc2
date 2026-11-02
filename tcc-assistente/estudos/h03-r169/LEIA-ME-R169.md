# R169 — continuidade localizada da laje da varanda

Em cópia independente do BIM R167, aplicou-se **Modelo → Lajes → Engastar** à borda comum V12 entre L4 e L6 no N1. Trata-se do vínculo entre lajes adjacentes; não se utilizou o comando diferente “Engastar em viga”. O aviso L10 “Laje em balanço não engastada” deixou de aparecer na verificação nativa do lançamento. Após salvar, fechar e reabrir o PRJ, repetiu-se a verificação: o pavimento N1 não apresentou problemas detectados por esse comando. A definição é de estudo, sujeita à conferência da continuidade, rigidez, armadura e cálculo.

O intervalo observado do acionamento da correção até salvar, incluindo a primeira conferência nativa, foi **76.077 ms (1 min 16,077 s)**. Não inclui preparação da cópia, pesquisa anterior, exportação ou releitura posterior e não constitui tempo completo do fluxo BIM. A exportação posterior disparou um pedido adicional de gravação ao fechar; escolheu-se não regravar para preservar o primeiro PRJ salvo, posteriormente reaberto e conferido.

A releitura comparou 33 partes de vigas, 22 segmentos de pilares e 11 lajes antes/depois: geometria e conjuntos de propriedades exportados permaneceram iguais. Portanto, neste par de arquivos e configuração de exportação, o IFC de geometria/propriedades **não evidencia a alteração nativa de vínculo** que modificou o diagnóstico. Não se infere que toda informação de vínculos seja impossível de exportar em qualquer software ou configuração.

Os 13 arquivos do controle R167 foram preservados por hash. A cópia R169 foi congelada localmente e possui manifesto. O arquivo PRJ conserva o nome interno herdado R166; o diretório externo R169 identifica a revisão correta.

Não se processou ou dimensionou a estrutura. Não foi demonstrada igualdade integral dos vínculos/cargas entre CAD e BIM. Permanecem escada no modelo de cálculo, apoio inferior, conflito V16/J4, cargas de paredes/cobertura/reservatório e verificações ELU/ELS. O trabalho escrito não foi alterado. Os arquivos são de estudo e não são liberados para execução.

`auditar_vinculo.py` é uma auditoria somente leitura dos arquivos nativos/IFC, com evidência textual da releitura da interface; não constitui chamada à IA, teste simulado de Eberick ou aprovação de engenharia.

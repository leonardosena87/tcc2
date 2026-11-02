# R165 — revisão geométrica da escada no receptor CAD

Revisão real no Eberick 2025 Infinity, em cópia independente da R161, em 02/11/2026. O PRJ foi salvo, fechado e reaberto. Não houve processamento estrutural novo, alteração do trabalho escrito ou aprovação de seções.

## Alterações e releitura

- V15 no N1: altura de 30 para 16 cm; largura 20 cm e elevação zero mantidas. Seção preliminar, ainda sem comprovação ELU/ELS.
- Dois nós extremos: Y de 285 para 303,5783333333 cm. O IFC apresenta eixo em 3,0358 m, diferença de +0,016667 mm em relação ao eixo nominal do Revit R160.
- O contorno da L5 não acompanhou a edição numérica dos nós no primeiro IFC. Removeu-se somente essa laje e relançou-se no contorno atualizado. Reaplicaram-se os valores registrados: maciça, 14 cm, ambiente Externo, elevação zero, acidental 2,5 kN/m², revestimento 1 kN/m², extra zero, grupo Nenhum, grelha a 90° adotando o espaçamento configurado. Esses valores foram preservados para isolar a revisão geométrica; não representam nova aprovação das cargas.
- Os campos de V15 e L5 foram lidos novamente depois da reabertura. Hash do PRJ: `6eaf1a915410830e83613a0e1e0c60c23f961818881396b7991183532a8decdf`.

O IFC4 de controle contém 46 peças de vigas, 22 de pilares e 11 de lajes. Permanecem 11 nomes/posições de pilares, P1–P11, e as mesmas caixas geométricas desses 22 segmentos. Não se acrescentou P12/P13. A V16 continua entre os pilares existentes P4/P10, seção preliminar 20 × 30 cm, com arredondamento de nível já registrado na R161.

No controle, a V15 ocupa X=4,4–6,55 m; Y=2,9358–3,1358 m; Z=3,04–3,20 m. A face livre inferior em planta da L5 passou de Y=2,95 para 3,13581 m. A diferença de 0,01 mm em relação à face da viga foi registrada dentro da tolerância computacional de 0,1 mm, sem qualificá-la como tolerância normativa. As quatro peças laterais V7/V9 tiveram seus pontos de segmentação deslocados com os nós, mantendo os extremos globais; isso não representa quatro novas vigas.

A L5 do Eberick corresponde espacialmente à L6-N1 do Revit. O nome sozinho não prova identidade. O perfil nominal completo da laje no Revit e a caixa do sólido livre entre vigas do Eberick são representações diferentes; não se declarou igualdade de áreas ou equivalência integral das condições de apoio. Vínculos de bordo e continuidade analítica ainda exigem auditoria específica.

## Tempo observado e tentativas

Da seleção inicial da V15 até a observação após salvar a revisão de seção, nós e laje: **2.369.140 ms = 39 min 29,140 s**. Inclui tentativas, pesquisa do comando, auditorias intermediárias, retomada de foco e interação da sessão. Uma tentativa moveu somente a identificação da V15; essa tentativa está incluída, sem ser contada como reposicionamento estrutural. O nível gráfico TCCVIGAS foi ocultado/inativado apenas nesta cópia durante a seleção; a referência gráfica antiga ainda aparece ao fundo.

Esse intervalo sobrepõe as duas medições intermediárias; **não somá-las**. Não representa tempo total do fluxo CAD, tempo de cálculo, esforço computacional puro da IA, tokens, custo ou comparação conclusiva CAD/BIM. A geração/auditoria de variantes IFC R162/R164 constitui outra etapa, explicitamente derivada.

## Arquivos e próximos passos

- PRJ: `D:\TCC\outputs\R165-CAD-REVISAO-ESCADA-R160-NAO-EXECUTAR\Projeto Eberick\H03_CAD_R49_LAJES_NAO_EXECUTAR.prj`.
- IFC de conferência: `IFC-CAD-Eberick\Modelo 3D.IFC` nesta pasta de resultados.
- `R165-CAD-auditoria.json`: comparação independente, hashes, caixas antes/depois, preservação dos controles e limites.
- `R165-reabertura-*`: releituras e capturas nativas; `R165-L5-*-antes/depois.txt`: parâmetros/grelha.
- `controle-apos-nos-antes-contorno`: PRJ/IFC intermediários preservados localmente, não publicados no Git.

O PRJ R161 original e todos os arquivos registrados na preparação da cópia foram conferidos por hash e permanecem iguais. Resultados de cálculo herdados não são resultados atuais da R165. Escada nativa, apoio inferior, cargas finais e interferência V16/J4 continuam pendentes. Esta revisão não encerra a comparação pareada nem o dimensionamento estrutural.

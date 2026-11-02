# H03/R159 — implantação do candidato com viga no patamar

## Estado desta rodada

A revisão dá continuidade à orientação do usuário de incluir a viga exigida pelo orientador nos dois fluxos. A posição e as seções do candidato R158 continuam hipóteses. Não se modificou a monografia, nem se promoveu a revisão à condição de projeto calculado.

O desenho parcial CAD R158 foi salvo nativamente em DWG, fechado, reaberto e exportado novamente para DXF no AutoCAD 2027. A conferência identificou as mesmas 96 faces, identificadores XDATA e camadas; diferença máxima de coordenadas de 1,333 x 10^-15 m. Esse desenho contém as superfícies acabadas e superiores do concreto da escada, além das caixas dos cinco elementos novos/revisados. Não contém volume resistente fechado da escada ou o edifício completo.

Adicionalmente, geraram-se três plantas 2D a partir do JSON comum R158: N1, N2 e patamar. O conjunto representa os 65 elementos candidatos da edificação (24 segmentos de pilares, 30 vigas e 11 lajes), com a mesma origem XY. Os contornos são polilinhas em Z=0; o nível real está identificado nos avisos e nos dados XDATA. Não se deve interpretar a coordenada gráfica Z=0 como mudança das cotas estruturais. Na planta intermediária, os pilares passantes aparecem como contexto e não representam novos segmentos acrescentados à contagem de 65.

As três plantas foram abertas no AutoCAD, salvas como DWG 2018, fechadas, reabertas e exportadas para arquivos DXF de retorno por uma sequência nativa de comandos. A conferência externa confirmou polilinhas fechadas, camadas, identificadores, conteúdo JSON XDATA, textos e eixos. A diferença máxima dos contornos foi de 8,882 x 10^-16 m. A conferência do arquivo não equivale à revisão completa de legibilidade ou compatibilização arquitetônica. Houve cancelamento de uma abertura duplicada durante a navegação; essa ocorrência está incluída na duração da sessão.

## Situação do Revit

Preparou-se uma cópia isolada da R157, com hash inicial idêntico à referência congelada. A primeira tentativa do comando R159 falhou antes de iniciar transações, ao tentar ler o SHA-256 do RVT aberto com compartilhamento incompatível com o bloqueio do Revit. O relatório nativo registrou `Saved=false`, nenhum aviso e 17,2766 ms de execução do comando. Corrigiu-se a leitura para um fluxo somente leitura com compartilhamento de leitura/escrita/exclusão, mantendo a conferência do hash e da ausência de alterações pendentes.

A DLL corrigida compilou com zero avisos e zero erros. Após reiniciar, o Revit permaneceu sem janela principal capturável. Os journals locais indicaram um diálogo de confiança de complemento. Solicitou-se ao usuário que trouxesse a janela para a tela; não se alterou a política de segurança nem se escolheu confiança por automação. Uma tentativa condicionada de recuperação por encerramento foi abortada pela proteção que detectou journals já iniciados; nenhum processo foi encerrado por essa tentativa.

Portanto, **a viga ainda não tem implantação nativa R159 confirmada no Revit**. A cópia R159 continua byte a byte igual à R157 congelada enquanto não houver criação, salvamento e releitura nativos confirmados. Não se deve utilizar sua existência como prova de aplicação da viga.

Ao fechar a sessão anterior da R157, preservou-se primeiro a referência congelada. Salvou-se a sessão aberta em arquivo de preservação separado e restaurou-se a referência congelada com verificação do hash. Não se adotaram automaticamente eventuais alterações daquela sessão. Os caminhos e hashes estão em `R159-preservacao-R157.json`.

## Limites do comando preparado

O comando só aceita o caminho exato da cópia R159, ainda sem alterações pendentes, com hash inicial conferido e 62 elementos estruturais. Também confere o hash do candidato comum, 60 elementos retidos, duas alterações previstas e três novos elementos. A rotina utiliza transações agrupadas e registra falhas.

A intenção é preservar identidades, tipos, eixos/perfis, seções e materiais dos 60 elementos retidos; revisar V15 e L6; acrescentar P12/P13 e V16-ESC-PAT; e recriar a escada nativa com 17 espelhos (9+8). A preservação é uma comparação lógica desses dados, não uma afirmação de igualdade dos volumes recortados pelas uniões automáticas. A rotina também verifica o cadastro de fck=25 MPa nos 65 elementos estruturais; isso não verifica módulo, densidade, cargas ou capacidade.

A escada usa acabamento hipotético constante de 5 cm, referência virtual inferior de concreto +0,17 m, topo +3,20 m e patamar de concreto +1,774118 m. A espessura resistente inicial de 14 cm permanece sem dimensionamento. A diferença de 3 cm entre a referência virtual inferior e N0 +0,20 m continua pendente; não se criou fundação real. Largura útil, altura livre, balanço do patamar, continuidade, torção, armadura e ancoragem exigem análise. O corrimão automático não constitui detalhamento aprovado.

## Recepção no Eberick e igualdade dos fluxos

As novas plantas ainda não foram incorporadas aos receptores CAD/BIM do Eberick. Um DWG/DXF fornece referência gráfica; não se afirmou que seus XDATA sejam convertidos automaticamente em material ou objetos de cálculo. A aplicação IFC também permanece pendente do Revit. O estudo deve registrar em cada receptor o que efetivamente chegou, o que exigiu relançamento e o tempo correspondente.

No [procedimento oficial de nível intermediário da AltoQi](https://suporte.altoqi.com.br/hc/pt-br/articles/115002186654), a inserção ocorre a partir do pavimento superior e a altura é medida desde o pavimento inferior. Com N0=+0,20 m e patamar de concreto=+1,774118 m, a diferença geométrica candidata é de 1,574118 m. Esse valor não autoriza modificar níveis sem conferir a convenção e os vínculos das duas cópias. A própria documentação distingue os pilares passantes e sua continuidade; não se deve duplicá-los como novos pilares independentes por constarem no desenho de contexto.

O [procedimento oficial sobre apoios inadequados de escadas](https://suporte.altoqi.com.br/hc/pt-br/articles/115004562614) orienta conferir a seleção dos eixos, os contornos de apoio e a grelha. Por isso, contato entre a superfície da escada e a caixa de uma viga não foi aceito como comprovação de vínculo resistente. A verificação no Eberick deve tratar os dois fluxos com as mesmas hipóteses, sem eliminar contatos apenas para reduzir a contagem de interferências.

## Tempos e esforço da automação

A retomada da conferência do desenho CAD parcial durou 133.299,75 ms (2 min 13,30 s), incluindo navegação, capturas e raciocínio. A sessão das plantas 2D durou 213.654,36 ms (3 min 33,65 s), incluindo a recuperação de foco. O intervalo entre iniciar a sequência nativa e observar seu término foi 23.287,84 ms; está contido naquela sessão e **não deve ser somado novamente**. Não se trata de tempo de CPU do AutoCAD. A geração dos três DXF pelo script levou 808,17 ms, medidos separadamente.

Esses valores são medições de desenvolvimento e conferência parcial. Não estabelecem vantagem de CAD ou BIM, pois não constituem ensaio pareado completo. O registro distingue a falha do suplemento, a correção do código, a intervenção humana de confiança, as esperas e a navegação. Não há telemetria de tempo de inferência, tokens ou custo de IA para atribuir valores a essas categorias.

Executou-se a suíte existente de `tcc-assistente`: 81 testes aprovados, nenhum reprovado ou ignorado. Executaram-se também cinco testes do comparador de retorno CAD, incluindo rejeição de face ausente, vértice deslocado, contorno cruzado e camada alterada. Os testes automatizados não acionaram cálculo estrutural, inferência paga ou uma sessão real do Word. A gravação/reabertura no AutoCAD foi uma verificação nativa separada; o comando Revit corrigido ainda aguarda verificação nativa.

## Retomada

Após a janela do Revit ficar acessível, conferir o aviso e a DLL local corrigida com o usuário, abrir a cópia R159 e executar o comando novo de aplicação. Inspecionar o resultado e os avisos, salvar, fechar, reabrir e executar a conferência R159. Exigir os relatórios de criação e releitura e conferir os 65 elementos antes de atualizar o apontador de estado. Repetir a verificação nativa de interferências, classificar os contatos e completar a análise dos apoios. Somente então preparar a exportação IFC e o ensaio de recepção correspondente ao DWG.

`preparar.py` e `preparar_formas_cad.py` recusam sobrescrever a preparação. O arquivo SCR preservado documenta a execução nativa desta rodada; não deve ser reaplicado sobre arquivos existentes. Os binários RVT/DWG/DLL permanecem em D:\TCC e não são versionados. **NÃO EXECUTAR EM OBRA.**

# R225 — Retorno das correções comuns aos arquivos de autoria

Pasta local: `D:/TCC/outputs/H03-R225-AUTORIA-COORDENACAO-NAO-EXECUTAR`.

## Estado desta etapa

**CAD concluído e conferido; atualização geométrica aplicada, salva e reaberta no Revit em06/11/2026.** O arquivo `R225-aplicacao-nativa.json` confirma66 elementos e escada preservada, com zero avisos na transação. Uma releitura após fechamento e reabertura confirmou o cadastro. A primeira exportação IFC4 revelou cobrimentos de tipo diferentes das premissas. O usuário corrigiu o cadastro pela interface e salvou; a segunda exportação confirmou30 mm nos55 pilares/vigas e25 mm nas11 lajes, nos três campos de cada peça. O original R195 manteve seu hash. Nenhuma barreira de segurança foi contornada; a escolha de confiança foi feita pelo usuário.

Preparou-se um candidato de66 elementos:23 trechos de pilares,32 vigas e11 lajes. Esta é uma atualização da geometria de estudo a partir das correções analíticas comuns R210/R211/R223. Não representa um novo ensaio de importação, nem transforma o modelo final do Eberick em uma entrada original independente.

As alterações previstas são: seção30×30 cm na prumada de autoria P11-N1/P11-N2, correspondente ao P6 BIM/P11 CAD do receptor; inclusão do P12 de20×30 cm em X3,55/Y3,90 m somente atéN1; subdivisão da viga deY3,90 m em trechos30×45 e30×20 cm, com apoio no P12; largura30 cm no trecho raso de16 cm atéX6,55 m; inclusão da viga inferior da escada30×30 cm, eixoX4,50–5,40 m/Y3,2158 m, topo+0,20 m. Não se recriam os dois pilares da escada retirados na R160.

Preserva-se a escada nativa R160 de17 espelhos, distribuição9+8, patamar de concreto+1,774117647 m e piso acabado hipotético+1,824117647 m. Essa é a geometria efetivamente salva e integrada no receptor, distinta de alternativas antigas discutidas no chat. Não se move a escada nem se declara resolvida a interface de3 cm na base. J4 continua suprimida na referência herdada; o PDF arquitetônico original permanece intacto.

O controle parcial contra os dois pórticos genéricos R223 encontrou segmentos de eixo e I33 compatíveis para as32 vigas previstas. O controle não comprova, separadamente, todas as larguras, alturas, volumes, recortes, lajes, orientações ou ligações. Não se modifica a exportação analítica para impor igualdade.

## AutoCAD: trabalho efetivamente executado

Geraram-se quatro referências2D em metros, com a origemXY preservada e coordenada geométricaZ=0: N0, patamar, N1 e N2. A cota do concreto, as seções e a identidade dos elementos ficam nas legendas e no XDATA. Os pilares passantes e a projeção dos degraus aparecem como contexto; não se contam novamente como novos elementos. A representação dos degraus é referência geométrica e não modelo resistente ou levantamento de peso próprio.

Executou-se o **AutoCAD2027 CoreConsole nativo** instalado no computador. Para cada planta, importou-se o DXF, salvou-se DWG2018, encerrou-se o processo, reabriu-se o DWG em outro processo e exportou-se DXF de retorno. São8 execuções nativas, com logs preservados. Não se confunde essa verificação com uma inspeção visual da interface gráfica.

A conferência do retorno preservou os66 elementos únicos, metadados XDATA, textos, linhas de eixo, camadas e polígonos, dentro da tolerância computacional de10⁻⁹ m. A maior diferença numérica foi1,34×10⁻¹⁵ m. A tolerância é de leitura/comparação, não tolerância construtiva ou de interpretação da arquitetura. Os novos DWGs não foram importados no Eberick nesta etapa.

## Tempos e falhas preservadas

O lote nativo bem-sucedido, sequencial, levou **22,882736 s**, incluindo inicialização dos8 processos, salvamentos e exportações de retorno. A geração dos quatro DXFs levou166,5184 ms. São métricas de operações diferentes; não representam o tempo total CAD ou o esforço da IA. A auditoria externa e a preparação/correção da automação ficam fora desses intervalos. Não há medição Revit pareada concluída nesta revisão; não se calcula economia percentual.

Preservou-se uma primeira tentativa que importou o N0, mas não salvou DWG porque o comando `-SAVEAS` não foi reconhecido. O processo retornou código0; o controle detectou ausência do arquivo e recusou sucesso. Corrigiu-se para `SAVEAS` e executou-se o lote completo. Essa tentativa não se apaga do histórico e não integra o intervalo bem-sucedido de22,88 s. Também se preservam a distinção entre igualdade de metadados e comparação numérica de coordenadas, e o fato de que pequenas diferenças binárias de ponto flutuante não representam deslocamento geométrico nessa precisão.

## Revit: aplicação nativa e primeira exportação

Compilou-se `RevitCoordinationR225` paraRevit2027, sem erros ou avisos de compilação, e executou-se a rotina noRevit2027.2, arquivo executável27.2.0.39. O suplemento está limitado ao caminho da cópia R225 e ao hash do candidato. Verificou as63 geometrias e materiais C25 da referência; preservou59 elementos, modificou4 e criou3; conferiu as66 geometrias resultantes e a escada. A operação nativa, incluindo conferência e salvamento, registrou **2.836,1638 ms**. Não é tempo de autoria completa, tempo de IA ou intervalo pareado com o lote CAD, que tem outra condição inicial e executa quatro arquivos em oito processos.

Após fechar e reabrir o RVT, executou-se a releitura das66 peças e da escada. O RVT fechado apresentou hash30412f9bafa6ececccc34452872ba0c05f5a449063341443fef4eb542ffacf6c, antes da correção posterior de cobrimentos. O original R195 permaneceu em b8d0499545252227e7e2048d645c2c3ded37c4317185f5feffcb1bd93b76f483. A primeira exportaçãoIFC4 registrou4.439,7059 ms de comando; o arquivo531.859 bytes teve hash52d0a9b8affa13beb47ac84e8c7430158c8c149eed6879a3f696309702f0c50f. A transação transitória da exportação foi revertida para preservar o RVT salvo, que continuou sem edição pendente.

A auditoria independente IfcOpenShell encontrou32IfcBeam,23IfcColumn e11 lajes da edificação com os66IDs e marcas esperados; confirmou b/h nos55 pilares/vigas e resistência numérica25 MPa, por propriedade de pressão e unidade explícita, nos materiais de todas as66 peças. As66 malhas são finitas e não vazias. O12ºIfcSlab é o patamar agregado à escada, junto aos dois lances; não é uma laje excedente da edificação. A auditoria registra as caixas dos sólidos, mas não compara independentemente todo o sólido nativo, cortes de união ou a espessura de cada laje.

Na primeira exportação, os55 pilares/vigas apresentam os três campos de recobrimento como25 mm e as11 lajes como20 mm, divergindo das premissas30/25 mm. São66 elementos e198 campos de cadastro; não equivalem a198 operações humanas ou198 defeitos de transferência. A divergência provém do cadastro padrão da autoria e não foi demonstrada como alteração causada pelo IFC. A cópia RVT e o IFC anteriores à correção ficam em `Antes-correcao-cobrimentos`. Essa diferença não altera as dimensões externas do concreto, mas precisa ser corrigida e auditada como qualidade da informação. Os cobrimentos do Eberick não foram substituídos pelos padrões Revit nessa etapa.

O IFC posterior à correção preservou os66IDs globais e as caixas geométricas dos66 sólidos, com diferença máxima zero nessas caixas; o cadastro geométrico nativo e a leitura da escada permaneceram idênticos. Essa conferência não compara toda a topologia de cada sólido nem constitui modelo de armadura. A segunda exportação registrou1.612,2187 ms,531.910 bytes e hashd67649691c7d352499b5a6343059808f796d19ecfad8b7c74c1cd41048ed9964. As duas durações de exportação não constituem repetições controladas, pois houve edição intermediária, cache e outra condição de execução. O RVT salvo após a correção e fechado para backup tem hash673b9be8ff16a239d9add12e6353248bc12283fb3274c1fa361c603904243d88.

Doze testes locais passaram: sete de coordenação/eixos e cinco de unidades/campos IFC, incluindo conversão Pa/MPa, unidade explícita, medida inadequada e campos ausentes. Os scripts e testes não chamaram uma API de IA. O uso de tokens e o custo da conversa do assistente não foram disponibilizados para medição. As dependências instaladas, DLLs, arquivos temporários e material nativo de projeto ficam fora do repositório público.

A participação da IA nesta revisão incluiu preparação do candidato comum, programação dos controles, geração2D, operação da interface, conferência e documentação. A participação humana incluiu a escolha de confiança do suplemento e a edição de cobrimentos solicitada diante da falha de seleção automática da lista. Não se converte o intervalo de espera pela resposta em tempo ativo humano ou inferência exclusiva. Os dados das demonstrações da palestra permanecem separados do estudo principal.

## Limites da entrega

As referências de autoria continuam identificadas como estudo não executivo. Permanecem ligações/ancoragens e ELS local daV1, Aviso08 da cobertura, apoio daW08 inferior e interfaces arquitetônicas P11/P6/P12, além da nova transferência auditada e das medições completas de mesmo escopo. Apoios idealizados não constituem fundações dimensionadas. Esta revisão não altera o dimensionamento no Eberick nem a monografia.

Reprodução: `python preparar.py` uma única vez na pasta nova; `python formas_cad.py gerar`, `nativo` e `conferir`, nessa ordem. Não sobrescrever saídas nativas existentes. A referência original permanece em `W08-H03-R207-ENSAIO/Autoria-salva`; sua integridade é registrada no arquivo de configuração.

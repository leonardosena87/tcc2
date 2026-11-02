# H03/R160 — somente a viga no local marcado pelo usuário

Aplicou-se a orientação expressa do usuário, acompanhada de imagem: retirar os dois pilares adicionais da R159 e manter somente uma viga no trecho vermelho entre os pilares existentes. A posição interpretada corresponde a P4/P10, eixo Y=0, do X=4,40 ao X=6,55 m. A imagem fornecida foi preservada, com hash, em `R160-marcacao-usuario.png`.

## Resultado nativo

O Revit retirou somente P12-ESC-N1/473797 e P13-ESC-N1/473798. Reposicionou-se V16-ESC-PAT/473802 do Y=0,875783 m para Y=0, preservando identidade, tipo, material e seção candidata de 20x30 cm, com topo +1,774118 m. Não se acrescentou outra viga além dessa única viga em relação à base de 62 elementos. O conjunto contém 22 trechos de pilares, 30 vigas e 11 lajes: 63 elementos nessas categorias, além da escada.

A escada permaneceu com 17 espelhos, 9+8, e seu relatório de parâmetros, contornos, tipos e materiais coincidiu exatamente com a R159. Os cadastros lógicos dos outros 62 elementos também coincidiram: identidades, tipos, eixos/perfis, seções e materiais. Não se afirma igualdade de todas as malhas ou volumes afetados por uniões automáticas. O material nativo dos 63 elementos manteve compressão cadastrada de 25 MPa; módulo, densidade, cargas e dimensionamento não foram validados por essa conferência.

O arquivo foi salvo, fechado, reaberto e auditado pelo comando somente leitura. O objeto Readback coincidiu com o registrado na aplicação. A categoria Escadas estava desmarcada na vista nova e foi habilitada no diálogo nativo de visibilidade, sem mudar a geometria. Essa alteração da vista foi salva e permaneceu visível após reabrir. A aplicação registrou zero avisos de falha; a ausência de avisos não comprova compatibilidade completa. A fonte R159 permaneceu byte a byte preservada.

Arquivo Revit: `D:/TCC/outputs/Escada-H03-R160-SOMENTE-VIGA-NAO-EXECUTAR/H03-R160-Revit-SOMENTE-VIGA-PATAMAR-NAO-EXECUTAR.rvt`.

## CAD

As três plantas N1, N2 e patamar foram geradas a partir do mesmo candidato comum R160, abertas no AutoCAD, salvas em DWG 2018, fechadas, reabertas e exportadas para DXF de retorno. Conferiram-se 63 identidades distribuídas nas plantas, contornos, eixos, camadas, textos e JSON XDATA. A diferença máxima de coordenadas foi 8,882x10^-16 m. Os pilares passantes no desenho do patamar são contexto, sem novos segmentos acrescentados ao conjunto. O CAD fornece referência gráfica 2D; não se declarou conversão automática de lajes, materiais ou elementos analíticos no Eberick.

Arquivos na mesma pasta:

- `R160-CAD-N1-FORMA-CANDIDATA.dwg`;
- `R160-CAD-N2-FORMA-CANDIDATA.dwg`;
- `R160-CAD-PATAMAR-FORMA-CANDIDATA.dwg`.

## Compatibilização pendente

A faixa frontal da viga cruza a caixa da janela J4 sob a interpretação arquitetônica já registrada na R158. O usuário determinou a posição da viga, mas não se interpretou isso como aprovação de uma alteração da janela. Não se moveu J4, parede, porta, fachada, piso ou lance da escada. A interferência permanece explicitada para revisão arquitetônica/orientador. A seção 20x30 cm foi herdada como hipótese, sem dimensionamento; apoio inferior, contato resistente do patamar, continuidade, torção, armadura e ancoragem não foram aprovados.

O IFC e os receptores Eberick da R159 continuam históricos, com a geometria anterior e os dois pilares adicionais. A R160 ainda precisa de nova exportação e incorporação pelos dois caminhos de intercâmbio. O ensaio de recepção R159 não foi apresentado como atualizado por esta revisão. A monografia não foi alterada. **NÃO EXECUTAR EM OBRA.**

## Tempo e validação

O comando Revit mediu **1.244,8423 ms**, excluindo preparação, compilação, confiança do suplemento, navegação, ajuste de visibilidade e reabertura. A sessão CAD mediu **144.887,64 ms (2 min 24,89 s)**, incluindo recuperação de foco e duas tentativas de acionar o script antes da execução completa. A geração dos DXF mediu 1.683,46 ms, separadamente. Esses recortes têm escopos distintos e não são ensaio pareado nem tempo total de fluxo. O registro de clique/observação no Revit também fica separado do tempo do comando. Não há telemetria de tokens/custo/inferência para atribuir valores ao esforço de IA.

A compilação final teve zero erros e zero avisos, após incluir a referência WindowsDesktop que faltava na primeira compilação. Cinco testes sintéticos do comparador CAD passaram. Os testes do suplemento são registrados separadamente em `R160-validacao.json`; não acionam cálculo estrutural ou inferência paga. A releitura nativa e a comparação dos DXF reais são evidências adicionais aos testes.

O conector R160 reutiliza os leitores públicos da DLL R159, cuja dependência e hash foram registrados na preparação. A leitura da escada usa o candidato R158 preservado porque seus contornos não mudaram nesta revisão. A rotina recusa outro caminho de documento, cópia alterada, contagem inicial diferente de 65 ou identidades imprevistas. A operação usa transações agrupadas e verifica a preservação antes de salvar. Não se deve reaplicar o comando na R160 já alterada; o bloqueio inicial deve recusá-lo.

`R160-resultado.json` contém o estado consolidado, fontes e hashes. A imagem `R160-Revit-reaberto.png` mostra a revisão realmente reaberta. Os binários RVT/DWG/DLL permanecem em D:/TCC; código, contratos e evidências pertinentes foram registrados no Git local, sem envio a terceiros nesta etapa.

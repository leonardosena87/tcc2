# H03/R146 — análise parcial após complemento de forro N1

Processaram-se cópias independentes 72/CAD e 73/BIM do cadastro R145, preservando os 35 arquivos-fonte. Em ambas, selecionaram-se análise estática linear e deslocamentos do pórtico com rigidez configurada. Permaneceram desmarcados dimensionamento dos elementos, flechas das lajes, cálculo de rigidez fissurada e dinâmica. As capturas documentam as opções efetivas. O término foi “Estrutura processada com avisos”; não corresponde a aprovação ou projeto executivo.

| Parcela exibida | CAD (tf) | BIM (tf) | Variação em cada ramo desde R116 (tf) |
|---|---:|---:|---:|
| Peso próprio | 75,69 | 75,69 | 0,00 |
| Adicional | 12,04 | 12,04 | +1,48 |
| Acidental | 17,11 | 17,11 | 0,00 |
| Q_TELHADO_MANUTENCAO | 1,78 | 1,78 | 0,00 |
| Total | 106,62 | 106,62 | +1,48 |

O resumo exibiu área aproximada 132,81 m² e relação 802,83 kgf/m², mantendo o aviso de relação não usual. A diferença entre totais arredondados confirma sensibilidade à nova entrada, mas não substitui integral de cargas e reações. O peso do forro permanece hipótese de estudo.

Os valores exibidos de deslocamento horizontal máximo coincidiram em 0,20 cm nas quatro direções, com limite apresentado 0,42 cm. O máximo relativo foi 0,17 cm, limite apresentado 0,35 cm. A direção crítica continuou CAD N1/Y− e BIM TCC-cdd31967-N1/Y+. Não se determinou a causa dessa divergência nem se demonstrou defeito de transferência. Gama-Z exibiu 1,09/1,08/1,06/1,05 em X+/X−/Y+/Y−, com limite apresentado 1,10. A adequação normativa final dos parâmetros, ações e limites não foi encerrada.

No trecho de deslocamentos no topo, preservado sem unidade inferida onde ela não aparece no texto, os aumentos percentuais de Vento X+ foram CAD 14,83% e BIM 14,84%; em X−, CAD 14,84% e BIM 14,83%. Os demais pares desse trecho coincidiram. São diferenças de 0,01 ponto percentual; não se convertem automaticamente em erro, correção ou inequivalência estrutural completa.

As sessões abrir → processar → capturar → salvar → fechar duraram 73,291 s CAD e 60,669 s BIM. O intervalo comando → registro de término foi 10,995 s CAD e 4,812 s BIM. No CAD, o registro temporal ocorreu na chamada seguinte à primeira imagem de término, incluindo uma rodada do assistente; no BIM, ocorreu na própria chamada de captura. Os intervalos de comando estão contidos nas sessões e não devem ser somados. Não se calcula ranking de solver, produtividade integral ou economia percentual. Não houve intervenção humana. Tempo ativo, inferência isolada, tokens e custo da IA não foram medidos.

Salvaram-se e fecharam-se as cópias; o congelamento verificou os hashes de cada arquivo e a integridade ZIP dos PRJs. Não houve exportação SAP, processamento em outro solver, dimensionamento de concreto/armaduras, metal ou ancoragens. Permanecem pendentes cargas e apoios da escada, paredes não aceitas, reservatório, vento/composições e verificações completas de ELU/ELS. Não se alteraram o RVT, DWG ou monografia. Os binários nativos ficam somente em D:/TCC; as evidências e os scripts pertinentes ficam no repositório.

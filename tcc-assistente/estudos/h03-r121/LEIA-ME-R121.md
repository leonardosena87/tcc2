# H03/R121 — ensaio pareado de carga extra na faixa W03

Criaram-se cópias independentes dos dois receptores R116. Conferiu-se o trecho sob W03: CAD V3/N1 e primeiro trecho BIM V1/TCC-cdd31967-N1. A escolha se baseou no mapa geométrico R120 e na localização nativa, preservando os nomes distintos. A V1 BIM também possui outro trecho com o mesmo nome; não se aplicou carga nele deliberadamente, mas a ausência de alteração nesse trecho vizinho ainda exige releitura específica.

Antes do ensaio, o campo Carga de parede apresentava 0,00 kN/m e as seis linhas da grade Carga extra apresentavam zero nos dois trechos consultados. A grade foi transcrita visualmente a partir das imagens, pois seus valores não são extraídos pela árvore UIA. Não se afirma que todas as cargas do edifício tenham sido inspecionadas por essa consulta.

Digitou-se **+4,4446 kN/m** exclusivamente na linha Adicional da carga extra do trecho. O valor representa a magnitude por metro da hipótese R120 para parede sem abertura, com altura de referência 2,84 m e peso superficial hipotético de 1,565 kN/m². Não se cadastrou a parede na biblioteca global, nem se somou novamente a carga ao campo de parede. Os valores padrão do diálogo Parede (altura 280 cm, espessura 15 cm e peso 13 kN/m³) foram apenas observados e cancelados no CAD, sem serem adotados.

No CAD, houve tentativa de criar nó na coordenada digitada `10,705` cm. O programa respondeu “Já existe um nó nesta posição no pavimento”. Não foi criado nó duplicado. Esse aviso não comprova que a face livre de alvenaria tenha se tornado um limite analítico exato, nem informa a tolerância de associação usada pelo programa. Por isso a carga aplicada pelo diálogo de viga permaneceu como **ensaio experimental de extensão**, sem aceitação como lançamento final de W03.

Após salvar, fechar e reabrir, os dois trechos apresentaram **4,44 kN/m** no resumo e na linha Adicional da grade; Solo, Acidental, Água, Subpressão e QT permaneceram em zero na leitura visual. Ao entrar em edição da célula reaberta, ela continuou mostrando 4,44, sem recuperar visualmente as quatro casas digitadas. O valor interno armazenado permanece desconhecido. As seções consultadas mantiveram 20 × 45 cm e elevação zero. Não se alteraram vínculos, rigidez ou nomes. A opção Manter seção constante na viga já diferia entre CAD e BIM, conforme as imagens; não se alterou essa opção, que se refere à seção, nem se inferiu dela o escopo da carga.

Processaram-se as cópias com análise estática e ELS-DEF do pórtico usando rigidez configurada. As imagens documentam dimensionamento desativado, sem cálculo de rigidez fissurada, flechas das lajes ou dinâmica. Ambos concluíram com avisos.

| Parcela vertical exibida | CAD (tf) | BIM (tf) | Variação em relação à própria R116 (tf) |
| --- | ---: | ---: | ---: |
| Peso próprio | 75,69 | 75,69 | 0,00 |
| Adicional | 12,51 | 12,51 | +1,95 |
| Acidental | 17,11 | 17,11 | 0,00 |
| Q_TELHADO_MANUTENCAO | 1,78 | 1,78 | 0,00 |
| Total | 107,09 | 107,09 | +1,95 |

O resumo mantém o aviso de relação carga/área não usual: 132,81 m² e 806,36 kgf/m². O deslocamento horizontal exibido continua 0,20 cm nos quatro sentidos, com limite 0,42 cm. O relativo continua 0,17 cm, com limite 0,35 cm; a identificação permanece CAD N1/Y− e BIM TCC-cdd31967-N1/Y+. A causa dessa diferença não foi estabelecida, e não se demonstrou defeito de transferência.

Gama-Z passou a exibir **1,10 em X+**, mantendo 1,08 em X−, 1,06 em Y+ e 1,05 em Y−. O limite mostrado é 1,10. Igualdade com o limite arredondado não constitui aprovação de estabilidade, rigidez ou parâmetros normativos. O vento, as combinações e o conjunto de cargas permanecem incompletos. Os valores e percentuais de deslocamentos do topo coincidiram nesta revisão; a unidade não aparece explicitamente nesse trecho e foi mantida desconhecida no JSON.

A faixa livre W03 tem 4,20 m e peso hipotético de 18,66732 kN, enquanto a distância entre eixos de pilares é 4,40 m. A diferença de resumos arredondados, 1,95 tf, admite aproximadamente 1,94–1,96 tf se cada parcela foi arredondada ao centésimo mais próximo. Como diagnóstico aritmético, 4,4446 × 4,40 / 10 = 1,955624 tf cai nessa faixa; 4,4446 × 4,20 / 10 = 1,866732 tf não cai. Usar 9,80665 kN/tf produz outras previsões, também conservadas no JSON. **Isso sugere investigar a extensão entre eixos e a conversão usada, mas não calibra a unidade nem prova o comprimento interno carregado.** Não se ajustou a carga apenas para forçar coincidência do resumo.

O [suporte oficial de cargas lineares](https://suporte.altoqi.com.br/hc/pt-br/articles/360058309854) descreve a atribuição pelo diálogo do elemento e diferencia a linha definida sobre laje. A [orientação para carga em parte da viga](https://suporte.altoqi.com.br/hc/pt-br/articles/360046158854) exige definir nós delimitadores quando o trecho não está representado. O [aviso de carga negativa em viga](https://suporte.altoqi.com.br/hc/pt-br/articles/360003993253) relaciona o sinal negativo distribuído à ação para cima, o que é compatível com o acréscimo positivo observado neste ensaio; isso não substitui a reconciliação integral de unidades e extensão.

As sessões duraram **1.198,181313 s no CAD (19min58s)** e **1.074,334925 s no BIM (17min54s)**. O CAD inclui exploração de menus, pesquisa, consulta de vínculos e tentativa de nó; o BIM inclui retomada entre mensagens e usa o procedimento aprendido. Os intervalos comando–registro de término foram 54,861498 s no CAD e 27,378296 s no BIM. No CAD, o marco foi gravado após a inspeção da captura de término, acrescentando tempo de inspeção ao intervalo. Portanto, esses intervalos não medem o solver e não sustentam ranking; estão contidos nas sessões e não devem ser somados a elas. Não se mediram isoladamente inferência da IA ou trabalho humano ativo.

Os 35 arquivos fonte R116 conservaram seus hashes. Após a consulta de retenção, os PRJs R121 conservaram os hashes registrados antes dela; no CAD o hash foi tomado após reabrir e antes de consultar, no BIM antes da reabertura. As cópias fechadas foram congeladas e conferidas: 16 arquivos CAD e 19 BIM, com integridade ZIP dos PRJs aprovada. Esses binários permanecem locais em D:/TCC. Dois testes verificam os resultados reais, a divergência de direção, a retenção exibida e a distinção entre hipóteses de extensão e calibração.

Evidências em `D:/TCC/outputs/Parede-W03-H03-R121-ESTUDO-NAO-EXECUTAR/`. As cópias nativas são `36-H03-R121-CAD-W03-NAO-EXECUTAR` e `37-H03-R121-BIM-W03-NAO-EXECUTAR`. **A referência anterior R116 foi preservada; a R121 não é promovida a lançamento definitivo de paredes.** Não houve modificação de RVT/DWG, arquitetura ou monografia. Permanecem pendentes extensão efetiva da carga, trecho vizinho BIM, demais paredes, tanque, escada, vento e verificações completas. A próxima operação deve esclarecer a geometria analítica carregada antes de ampliar o lançamento.

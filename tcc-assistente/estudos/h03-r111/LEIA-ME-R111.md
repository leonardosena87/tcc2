# H03/R111 — processamento exploratório com a varanda VP1-A

Processaram-se duas cópias independentes da R109, com as cargas excêntricas da varanda já conferidas na interface nativa. O acréscimo de cargas justifica o novo ensaio. Aplicou-se o mesmo recorte da R106: análise estática e deslocamentos do pórtico ELS-DEF com rigidez configurada. Desmarcou-se o dimensionamento; o cálculo dos deslocamentos das lajes, a rigidez fissurada e as vibrações permaneceram desmarcados. Não houve dimensionamento dos perfis ou das ligações metálicas.

## Resultado exibido e comparação com a referência anterior

| Grandeza | R106 CAD/BIM, sem VP1-A | R111 CAD/BIM, com VP1-A |
| --- | ---: | ---: |
| Peso próprio (tf) | 75,69 | 75,69 |
| Adicional (tf) | 10,05 | 10,16 |
| Acidental (tf) | 17,11 | 17,11 |
| Q_TELHADO_MANUTENCAO (tf) | 1,40 | 1,48 |
| Total vertical (tf) | 104,25 | 104,44 |
| Deslocamento horizontal X+/X−/Y+/Y− (cm) | 0,20 | 0,20 |
| Máximo relativo (cm) | 0,17 | 0,17 |
| Gama-Z X+/X−/Y+/Y− | 1,09 / 1,08 / 1,06 / 1,05 | 1,09 / 1,08 / 1,06 / 1,05 |

O acréscimo no total exibido corresponde a 0,19 tf. A diferença é entre números arredondados, sem verificação de equilíbrio global por reações. Não se deduz a conversão interna de unidades do programa a partir dessa diferença. Tampouco se deduz que os esforços ou deslocamentos completos permaneceram inalterados porque o resumo conservou duas casas decimais.

Nos dois ramos, o limite horizontal exibido foi 0,42 cm, o relativo 0,35 cm e o de Gama-Z 1,10. São limites apresentados pelo receptor, sem aprovação de sua adequação normativa final. A análise terminou com avisos, incluindo relação de carga por área não usual, agora de 786,37 kgf/m² para área aproximada de 132,81 m².

A direção do máximo relativo permanece **Y− em N1 no CAD** e **Y+ em TCC-cdd31967-N1 no BIM**. O valor de 0,17 cm é igual; o caso crítico identificado no resumo difere. A causa segue desconhecida. A igualdade dos relatórios detalhados anteriores da R107 não autoriza corrigir os rótulos deste resumo ou declarar um defeito de transferência.

## Tempos e preservação

| Recorte | CAD (s) | BIM (s) |
| --- | ---: | ---: |
| Sessão de navegação, configuração, processamento e evidência | 122,389065 | 124,041714 |
| Comando até registro do término observado, contido na sessão | 25,567843 | 26,933859 |

Esses tempos incluem interface, observação e registro; não são tempos isolados do solver nem totais completos de desenvolvimento. Não se somam os intervalos contidos às sessões, não se inferem tempo ativo humano ou esforço de inferência e não se classifica a produtividade dos fluxos a partir deste ensaio.

Os 33 arquivos fontes da R109 permaneceram inalterados. Salvaram-se e fecharam-se as duas cópias antes de congelar os arquivos finais e conferir seus hashes. Os projetos estão em `D:/TCC/outputs/24-H03-R111-CAD-VARANDA-NAO-EXECUTAR/` e `D:/TCC/outputs/25-H03-R111-BIM-VARANDA-NAO-EXECUTAR/`. Evidências e cópias preservadas: `D:/TCC/outputs/Analise-H03-R111-VARANDA-NAO-EXECUTAR/`.

O parser preserva a direção e extrai as parcelas verticais e as quatro direções de Gama-Z. Dois controles pertinentes verificam as leituras reais e rejeitam parcela ausente ou direção duplicada. São testes do tratamento das evidências, sem aprovação de engenharia.

Continuam pendentes P2, reservatório, paredes, escada, vento local, combinações efetivas, rigidez fissurada, dimensionamento e verificações ELU/ELS finais. Os apoios são idealizações da superestrutura, sem projeto geotécnico. A hipótese da varanda continua condicionada à verificação do metal, das ancoragens, dos nós de concreto e da compatibilidade espacial. Esta revisão preserva os arquivos de autoria e a monografia.

# H03/R58 - processamento diagnostico parcial, NAO EXECUTAR

Em 29/10/2026, processaram-se copias independentes dos estados CAD e BIM R57 congelados no Eberick 2025 Infinity. Nenhuma carga nova ou secao foi editada. A monografia e os arquivos de origem RVT/DWG nao foram alterados. Os dois ramos conservam as cargas parciais e as pendencias de concepcao anteriores.

Selecionou-se apenas Analise estatica linear no dialogo: dimensionamento, limites de redistribuicao, deslocamentos ELS e dinamica desmarcados. O programa montou o modelo, calculou paineis de lajes e processou o portico; retornou Estrutura processada com avisos nos dois ramos. O resumo indica Processo P-Delta; portanto o nome do botao nao significa calculo exclusivamente de primeira ordem.

## Resumos observados na interface

| Grandeza nativa | CAD | BIM |
|---|---:|---:|
| Peso proprio (tf) | 75,69 | 75,69 |
| Adicional (tf) | 8,20 | 8,20 |
| Acidental (tf) | 17,11 | 17,11 |
| Total (tf) | 101,00 | 101,00 |
| Area aproximada (m2) | 132,81 | 132,81 |
| Relacao (kgf/m2) | 760,52 | 760,52 |
| Gama-Z X+ / X- | 1,09 / 1,08 | 1,09 / 1,08 |
| Gama-Z Y+ / Y- | 1,06 / 1,05 | 1,06 / 1,05 |

O texto completo dos resumos e identico na precisao exibida; as unidades foram transcritas sem presumir conversao fisica. A area aproximada do Eberick nao e automaticamente a area arquitetonica ou de faces IFC. Nao se compararam esforcos por elemento, reacoes por apoio, conectividade analitica integral ou resultados sem arredondamento. A igualdade dos resumos nao certifica equivalencia integral dos modelos ou atendimento normativo.

Constam os avisos Relacao de carga por area nao usual para edificios e Os deslocamentos horizontais nao foram verificados. Os valores 0,00 cm desse bloco nao sao flechas ELS verificadas. No P-Delta, vento X passou de 0,96 para 1,10 cm (+13,92%) e vento Y de 1,06 para 1,15 cm (+7,92%), nos dois sentidos e ramos. Sao valores do modelo parcial. Embora os Gama-Z mostrados sejam inferiores ao limite 1,10 exibido, nao se declarou estabilidade aprovada: cargas, vento, combinacoes, apoios e demais verificacoes continuam pendentes.

## Persistencia e ocorrencia operacional

Ambos foram salvos, fechados normalmente, reabertos e consultados pelo comando de resultados da analise (icone Estrutura > Analise). Nao se reprocessou para essa consulta: os resumos armazenados permaneceram identicos aos iniciais. Os projetos foram fechados normalmente antes de congelar o conjunto nativo, incluindo resultados e auxiliares. Os ZIPs PRJ passaram na verificacao de integridade; preservados os 46 arquivos protegidos R57. Nao houve nova exportacao IFC nesta R58; a auditoria geometrica IFC anterior e a R57, nao uma auditoria posterior ao processamento.

Na primeira abertura da copia CAD apareceu novamente o aviso de possivel inconsistencia da ultima edicao. Executou-se a verificacao nativa de integridade nessa copia antes do processamento. A reabertura apos salvar/fechar nao repetiu o aviso. O BIM abriu/reabriu sem esse aviso. A causa nao foi demonstrada; registrar como ocorrencia operacional, sem atribuir a perda de transferencia DWG. A confirmacao de fechamento antes do congelamento nao prova a causa dos avisos anteriores.

## Tempos prospectivos assistidos

| Ramo | Abrir, processar, ler resumo e salvar | Intervalo observado de processamento |
|---|---:|---:|
| CAD | 1 min 43.431 s | 0 min 16.547 s |
| BIM | 1 min 19.665 s | 0 min 12.798 s |

Incluem raciocinio, interacao da IA, latencia e leitura. CAD inclui verificacao de integridade; BIM veio em seguida, com procedimento conhecido. O intervalo do processamento termina na leitura da conclusao e inclui o tempo entre capturas; nao mede exclusivamente o solver. A conferencia posterior de fechamento/reabertura tem registro separado em R58-tempo-reabertura-QA.json. Nao se mediu tempo humano ativo ou inferencia isolada da IA; nao houve chamada direta a API OpenAI nesta rodada. Nao e ensaio controlado, nem ranking/economia percentual/tempo total dos fluxos.

## Continuidade

Permanecem paredes (incluindo W08/base da escada), telhado, reservatorio de 1.000 L e apoio/tara/base, escada, bordas/guarda-corpo, vento/combinacoes, sensibilidade dos apoios idealizados e verificacao completa de ligacoes. Vigas de cobertura 20x30 cm ainda sao alternativa sem dimensionamento/ELS. O usuario aceitou nesta sessao a hipotese de telha ondulada de fibrocimento 6 mm a 10% sobre estrutura metalica leve; o peso e as reacoes ainda precisam de memoria e aplicacao comum. Essa carga nao integra os resultados R58. A superestrutura permanece como escopo; nao se dimensionaram fundacoes reais. Completar acoes e verificar ELU/ELS antes de selecionar a concepcao, sincronizar origens e elaborar resultados finais.

Referencia operacional: [opcoes de analise AltoQi](https://suporte.altoqi.com.br/hc/pt-br/articles/360008798134) e [etapas/inconsistencias](https://suporte.altoqi.com.br/hc/pt-br/articles/115004281814). Os resultados desta rodada provem da interface nativa preservada, nao dessas paginas.

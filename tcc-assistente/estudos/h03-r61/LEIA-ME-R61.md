# H03/R61 — piloto de duas cargas da cobertura

ESTUDO PARCIAL, SEM DIMENSIONAMENTO — NAO EXECUTAR. Criaram-se copias independentes dos conjuntos CAD e BIM R58 no Eberick 2025 Infinity. Inseriram-se apenas RC01 e RC02 do arranjo proposto R60, no pavimento N2, em (110;0) e (330;0) cm. Aplicou-se em ambos Fz=-1,419551 kN por no, acao Adicional, demais componentes nulas. A unidade kN foi conferida no dialogo instalado. O comando mostrou selecao de dois nos em cada ramo. Consultou-se individualmente RC01 no CAD e RC02 no BIM: coordenadas e Fz=-1,41955 kN na precisao exibida. Nao se releram todos os nos individualmente.

O plano inicial previa 13 pontos; limitou-se o ensaio a dois para conferir unidade, sinal, posicao e acrescimo global antes de ampliar. Restam RC03 a RC13. A soma digitada foi 2.839102 kN descendentes, enquanto a soma dos 13 pontos propostos R60 e 18,511248 kN. Nenhuma reacao variavel Q_telhado foi aplicada. Preservaram-se G2 do forro e Q das lajes. A discretizacao por nos pertence a concepcao comum, sem classificar essa operacao como defeito de transferencia.

## Resultado observado e persistencia

Processou-se apenas a opcao Analise estatica linear, com Processo P-Delta indicado no resumo; dimensionamento, ELS e dinamica desmarcados. Ambos retornaram Estrutura processada com avisos. O texto completo do resumo e igual na precisao exibida, inclusive apos salvar, fechar, reabrir e consultar resultados armazenados sem reprocessar.

| Grandeza | R58 em ambos | R61 em ambos |
|---|---:|---:|
| Peso proprio (tf) | 75,69 | 75,69 |
| Adicional (tf) | 8,20 | 8,49 |
| Acidental (tf) | 17,11 | 17,11 |
| Total (tf) | 101,00 | 101,29 |
| Area aproximada (m2) | 132,81 | 132,81 |
| Relacao (kgf/m2) | 760,52 | 762,66 |

Usando explicitamente 9,80665 kN/tf, o acrescimo esperado das duas forcas e 0.289507834 tf. O incremento exibido de 0,29 tf e compativel com a diferenca de dois valores arredondados a 0,01 tf (tolerancia combinada 0,01 tf). Isso nao demonstra precisao interna do programa nem verifica distribuicao local dos esforcos. Gama-Z permaneceu X+1,09/X-1,08/Y+1,06/Y-1,05. A variacao P-Delta passou a 8,85% no caso acidental, 13,97% em vento X, 7,94% em vento Y, 13,76% em desaprumo X e 7,78% em desaprumo Y. Os textos integrais preservam os valores.

Persistem os avisos Relacao de carga por area nao usual para edificios e Os deslocamentos horizontais nao foram verificados. Igualdade de resumos nao certifica equivalencia integral ou atendimento normativo. Nao se compararam esforcos por elemento, nem se verificaram ELU, flechas ELS, vento completo ou fundacoes reais. Nao houve exportacao IFC posterior ao piloto; a geometria atual apos os nos adicionais nao foi auditada por IFC. Os arquivos de origem RVT/DWG e a monografia ficaram intactos.

## Tempos prospectivos assistidos

| Ramo | Piloto ate salvamento | Intervalo observado de processamento |
|---|---:|---:|
| CAD | 9 min 50.106 s | 0 min 16.663 s |
| BIM | 11 min 36.352 s | 0 min 19.753 s |

O escopo inclui abertura, dois nos, cargas, consulta amostral, processamento, leitura e salvamento; inclui raciocinio, latencia e aprendizado da interface. O BIM inclui interrupcao de contexto antes do salvamento final. A ordem foi CAD primeiro, BIM depois. O intervalo de processamento termina na leitura da conclusao, nao isola o solver. A verificacao de persistencia ocorreu depois desses cronometros. Nao se mediram tempo humano ativo, tokens ou inferencia isolada da IA. Nao houve chamada direta a API OpenAI nesta rodada. Estes intervalos exploratorios nao autorizam ranking, economia percentual ou tempo total dos fluxos.

## Preservacao e continuidade

Os dois projetos foram salvos, reabertos sem aviso de integridade e fechados normalmente antes do congelamento. Preservaram-se 67 arquivos protegidos R58 e 7 arquivos R59; conferiram-se 8 entradas do manifesto R60. Os PRJ passaram na integridade ZIP. O conjunto nativo congelado inclui auxiliares/resultados e permanece em D:/TCC; o repositorio recebe apenas memoria, scripts e evidencias textuais pertinentes.

Proximo: ampliar em copias novas para RC03..RC13, com mesmos pontos e acoes nos dois ramos, conferir soma e posicoes; resolver P1/varanda e P2/abrigo elevado, perfis/altimetria/apoios/ancoragens, paredes, tanque1000L/tara/base, escada, bordas, vento/combinacoes e ELU/ELS. A hipotese metalica sem empuxo horizontal exige apoios e contraventamento ainda nao dimensionados. A reserva metalica0,15kN/m2 segue como hipotese. Nao extrapolar os 55,9425m2 nominais parciais para toda a cobertura.

Referencia operacional para sinal e insercao de nos: [AltoQi — cargas concentradas](https://suporte.altoqi.com.br/hc/pt-br/articles/115003467013). A evidencia do piloto provem da interface nativa preservada.

# H03/R106 - deslocamentos de servico, ensaio parcial

Processou-se o portico ELS-DEF com a opcao "Adotar rigidez configurada" em duas copias independentes da R104. Dimensionamento dos elementos, flechas de lajes, vibracoes e calculo de rigidez fissurada permaneceram desmarcados nas imagens observadas. As duas analises concluiram com avisos e foram salvas e fechadas. O recorte usa cargas ainda incompletas; nao constitui verificacao final da estrutura.

## Resultado nativo e divergencia preservada

| Grandeza exibida | CAD | BIM |
| --- | --- | --- |
| Maximo horizontal do centro de massa, X+/X-/Y+/Y- (cm) | 0,20 em cada direcao | 0,20 em cada direcao |
| Limite horizontal exibido (cm) | 0,42 | 0,42 |
| Maximo relativo do centro de massa (cm) | 0,17 | 0,17 |
| Limite relativo exibido (cm) | 0,35 | 0,35 |
| Pavimento nativo do maximo relativo | N1 | TCC-cdd31967-N1 |
| Direcao do maximo relativo | **Y-** | **Y+** |

O resumo deixou de exibir o aviso de deslocamentos horizontais nao verificados observado na R104. Permanece o aviso de relacao de carga por area nao usual. Os totais verticais continuam 104,25tf, dos quais QT corresponde a1,40tf; Gama-Z continua X+=1,09, X-=1,08, Y+=1,06, Y-=1,05 na precisao exibida.

O valor arredondado igual nao demonstra igualdade dos casos criticos. A direcao relativa difere e sua causa permanece desconhecida. Nao se atribui a diferenca a arredondamento, empate, orientacao de eixos ou defeito de transferencia sem evidencia adicional. O parser conserva o nome do pavimento e o sinal da direcao; a comparacao de resumos integrais e falsa. Os limites apresentados sao os cadastrados/exibidos, sem concluir sua adequacao normativa final. Rigidez configurada nao equivale a rigidez fissurada calculada.

Mantem-se a idealizacao comum de apoios rotulados documentada na R103/R104, para o recorte da superestrutura. Nao se dimensionou fundacao. Permanecem pendentes o fechamento de cargas, vento local, ligacoes, combinacoes efetivas, dimensionamento e verificacoes ELU/ELS finais.

## Tempos registrados

| Recorte exploratorio | CAD (s) | BIM (s) |
| --- | ---: | ---: |
| Sessao de navegacao, processamento e registros | 165,8286214 | 244,0697792 |
| Comando ate registro do termino observado | 24,7418747 | 20,7399035 |

Os valores menores estao contidos nas sessoes. Nao se somam os dois recortes. Observacao, interface, registro e lacunas integram o tempo decorrido; nao se mediu o solver isoladamente. A sessao BIM inclui o intervalo de consolidacao de contexto antes de salvar e fechar. Nao se desconta retroativamente esse intervalo nem se infere produtividade relativa. O preparo das copias e a consolidacao posterior ficam fora das sessoes. Nao houve nova intervencao humana solicitada nesta etapa.

## Preservacao e reprodutibilidade

Os35 arquivos de origem R104 permaneceram inalterados. Congelaram-se16 arquivos CAD e19 BIM apos salvar e fechar, com hashes conferidos. As copias laterais sao:

- D:/TCC/outputs/20-H03-R106-CAD-DESLOCAMENTOS-NAO-EXECUTAR
- D:/TCC/outputs/21-H03-R106-BIM-DESLOCAMENTOS-NAO-EXECUTAR

R102 continua conjunto principal de entrada; R104 e R106 sao ensaios exploratorios derivados. A monografia e os arquivos de autoria RVT/DWG foram preservados. O nome R102-preparacao.json decorre do preparador reutilizado; os caminhos internos identificam as origens R104 e destinos R106.

Dois controles sinteticos verificam a conservacao da divergencia de direcao e a rejeicao de evidencia ausente, conflitante ou nao verificada. Nao representam validacao de engenharia. A evidencia nativa consiste nas seis capturas e respectivas arvores de acessibilidade. O consolidado R106-resultado.json inclui hashes, tempos e limites. Proximo passo: consultar os relatorios detalhados por direcao sem alterar os dados ou repetir o processamento sem motivo.

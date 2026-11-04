# H03/R211 — Reprodução no CAD da hipótese local R210

## Base preservada e correspondência

Criou-se uma cópia independente do CAD salvo na R207. Não se substituiu esse modelo pelo BIM. Os nomes originais diferem: na linha horizontal de y390 cm, o CAD P2 corresponde ao BIM P4 em x0; P5 corresponde a P5 em x440; CAD P11 corresponde ao BIM P6 em x655. O novo P12 foi inserido em x355/y390 cm, seção20x30 cm, rotação zero, vértice central e deslocamento zero. Copiou-se somente esse pilar para N0 e N1 intermediário (altura157,4 cm), sem selecionar N2. No N0, converteu-se em fundação geométrica provisória engastada, tipo sapata60x60 cm, H1=20/H0=15 cm e colarinho20x30 cm, como no BIM. Não se dimensiona ou propõe essa fundação; trata-se do cadastro do apoio idealizado do estudo sem sondagem.

Alterou-se a prumada P11 para30x30 cm; a planilha final confirmou os três lances com níveis20/320/639 cm. O P12 apresentou apenas o lance L2 principal, de altura300 cm e nível320 cm; a base é cadastro de fundação, e o intermediário foi copiado separadamente. A continuidade analítica ainda requer auditoria por exportação.

## Edição e recálculo

A V2 do CAD percorre P2–P12–P5; a V14 percorre P5–P11. No BIM essa linha aparece em uma única V2, em sentido inverso. A primeira tentativa de editar a largura da V2 na planilha ainda baseada na topologia anterior não foi retida após a subdivisão pelo novo apoio: o primeiro recálculo mostrou dois trechos20x45 cm. Identificou-se o problema por releitura, sem considerar essa tentativa como alteração efetiva. A V14 reteve30x16 cm.

Corrigiu-se diretamente o croqui: selecionou-se o trecho estrutural após os dois elementos gráficos poligonais sobrepostos; fixou-se30x45 cm no trecho longo P2–P12 e30x20 cm no curto P12–P5, desmarcando a manutenção de seção constante. A janela da V14 confirmou30x16 cm. Reprocessou-se integralmente, com cálculo de deslocamentos do pórtico e lajes por rigidez fissurada. A planilha posterior confirmou as duas seções da V2 e os comprimentos livres335/65 cm; o vão livre da V14 foi190 cm.

O primeiro cálculo não representa a hipótese final. Os relatórios Mensagens da análise e Diagnóstico da estrutura foram emitidos novamente após o segundo cálculo, preservando os herdados separadamente. O diagnóstico final lista:

| Pavimento | Elemento | Sucesso | Aviso | Erro |
|---|---|---:|---:|---:|
| N2 | Vigas | 14 | 1 | 0 |
| N2 | Lajes | 5 | 0 | 0 |
| N2 | Pilares | 11 | 0 | 0 |
| N1 | Vigas | 16 | 0 | 0 |
| N1 | Lajes | 6 | 0 | 0 |
| N1 | Pilares | 10 | 2 | 0 |
| N1 | Escadas | 3 | 0 | 0 |
| N0 | Vigas | 0 | 1 | 0 |
| N0 | Pilares | 0 | 11 | 0 |
| N0 | Sapatas | 0 | 0 | 14 |

Não há deslocamento excessivo listado. O diagnóstico apresenta cargas verticais803,27/138,86/184,35/17,80 kN (própria/adicional/acidental/manutenção), total1144,28 kN, área138,06m², gama-Z máximo1,06 e deslocamento horizontal0,15 cm para vento Y-, ante limite cadastrado0,42 cm. O cálculo permanece com avisos e com14 erros de sapatas fora do escopo. Não se atribui automaticamente aos avisos CAD os identificadores BIM; a árvore CAD precisa ser consultada individualmente.

## Comparação local de resultados

| Ponto/trecho | CAD R211 (kN.m) | BIM R210 (kN.m) |
|---|---:|---:|
| Apoio externo esquerdo (CAD P2/BIM P4), negativo | -22,29 | -22,28 |
| P12, negativo | -26,67 | -26,65 |
| P5, lado V2 do CAD, negativo | -5,69 | -5,69 |
| P5, lado V14 do CAD, negativo | -2,11 | sem célula independente na V2 unificada |
| Apoio externo direito (CAD P11/BIM P6), negativo | -8,40 | -8,40 |
| Vão longo, positivo | 27,25 | 27,21 |
| Vão curto, positivo | 6,36 | 6,35 |
| Vão raso, positivo | 2,42 | 2,42 |

O CAD apresentou4phi8 superiores no apoio esquerdo,4phi12,5 no P12 e4phi8 em P5 e P11. P12 e P5 da V2 também apresentaram4phi8 inferiores. Os três vãos apresentaram4phi8 inferiores, e o curto também4phi8 superiores. No cisalhamento do CAD, o trecho longo exibiu phi6,3 c/21 cm, dois ramos; o curto phi6,3 c/8 cm, quatro ramos; a V14 phi6,3 c/6 cm, quatro ramos. Não apareceu na planilha CAD o reforço adicional à esquerda de100 cm que o BIM mostrou no trecho curto. A diferença requer revisão do detalhamento e do agrupamento dos trechos; não se classifica como vantagem ou falha de intercâmbio sem essa análise.

Outra diferença de cadastro: a tabela Nó mostrou largura superior do apoio P12 igual a0 no CAD e20 cm no BIM, embora não se tenha pretendido continuar o P12 até N2. Reabriu-se o BIM salvo e sua planilha de prumada também apresentou somente L2 para P12 (altura300 cm, nível320 cm), sem L3. Portanto não se interpreta a célula isolada como prova de um pilar no N2. O significado e a origem dessa diferença de propriedade permanecem pendentes de conferência. O Fd do P12 no N1 foi95,73 kN (BIM95,75), com8phi10 e Mrd/Msd1,11. Essas informações são saídas locais, sem aprovação estrutural ou verificação independente de armaduras.

A carga total é igual à do BIM na precisão dos relatórios. Isso não estabelece equivalência completa: a divisão em vigas é diferente (N1 CAD16/BIM12; N2 CAD15/BIM9), há diferenças de deslocamentos e armaduras, e os avisos e apoios precisam de conferência. Também permanece a compatibilidade com a porta junto ao CAD P11/BIM P6, cuja folga nominal na referência é inferior à incerteza de5 cm; não se validou a ampliação em toda a altura perante a arquitetura. Revit e DWG de autoria ainda não incorporam esta hipótese.

## Tempos, salvamento e limites

O processamento nativo final do CAD foi9 s, igual ao registrado no BIM R210. São execuções únicas de cálculo integral, incluindo fundações fora do escopo, com resolução de um segundo. Não medem o fluxo completo nem esforço exclusivo da IA ou do usuário. Não permitem afirmar ganho de produtividade. O arquivo R211-tempos-observados.json registra o intervalo da etapa CAD e as partidas dos dois cálculos, incluindo navegação, capturas, raciocínio e correções; não há intervalo BIM pareado equivalente.

Pasta local: D:/TCC/outputs/V2-H03-R211-CAD-EQUIVALENTE-NAO-EXECUTAR. Projeto: CAD/Projeto Eberick/H03_CAD_R49_LAJES_NAO_EXECUTAR.prj. A base R207 permanece preservada. Relatórios automáticos de custos não foram validados como orçamento. Não se alterou o texto acadêmico nesta etapa.

Procedimentos operacionais consultados: [AltoQi — copiar pilares entre pavimentos](https://suporte.altoqi.com.br/hc/pt-br/articles/360012136193), [lançar pilares](https://suporte.altoqi.com.br/hc/pt-br/articles/360001109753) e [cadastro de sapatas geométricas](https://suporte.altoqi.com.br/hc/pt-br/articles/360007654334). A consulta orienta a operação do software e não constitui validação normativa do projeto.

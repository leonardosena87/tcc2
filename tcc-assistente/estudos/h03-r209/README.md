# H03/R209 — Apoio adicional e conferência das seções

## Correção da interpretação R208

Conferiram-se as janelas dos pilares no croqui N1: P4 e P5 têm b20/h30 cm, rotação zero; P6 tem b20/h30 cm, rotação 90 graus. Portanto, para a viga horizontal em X, a dimensão transversal Y é 30 cm em P4/P5 e 20 cm em P6. A largura apresentada na guia Nó não havia sido interpretada corretamente na R208. Foram corrigidos o README e o JSON da R208 no repositório, preservando o relato dos ensaios e a rastreabilidade desta correção. A nova leitura baseia-se em seção, rotação e croqui, não apenas na tabela de apoios.

## Triagem arquitetônica

Renderizou-se a prancha arquitetônica A0 com Poppler e consultou-se a referência R195. O recorte superior mostra duas portas P2 adjacentes ao P5. Nas linhas vetoriais próximas a x793,44–801,84 pt, identificaram-se limites de parede em top1270,16/1285,52 pt e linhas de marcos em top1268,00/1287,68 pt. Com escala56,6929 pt/m, esses intervalos correspondem a27,09 e34,71 cm, respectivamente. Não são cotas executivas de pilar ou vão livre: a simbologia dos marcos e as aproximações da referência exigem conferência de compatibilidade. Alargar o P5 para40 cm em toda a altura não foi adotado como correção automática.

Estudou-se um novo apoio P12 em x3,55/y3,90 m, seção20x30 cm, rotação zero. A caixa nominal em planta é x3,45–3,65/y3,75–4,05 m. O vão horizontal T-P4-02 da cozinha, na referência interpretada, termina em x3,25 m; a face do novo pilar fica20 cm depois desse limite, antes de considerar a incerteza de5 cm da referência. No piso superior, a posição coincide nominalmente com a parede horizontal, fora das portas junto ao P5. A triagem não verifica folhas em movimento, acabamentos, vinculações, altura livre ou todos os equipamentos.

## Lançamento e processamento

Criou-se uma cópia independente do ensaio BIM30 da R208, em D:/TCC/outputs/V2-H03-R209-APOIOS-NAO-EXECUTAR/BIM-NOVO-APOIO. Inseriu-se o P12 no N1, copiou-se para N0 e para o nível intermediário de altura157,4 cm. A primeira tentativa, sem o nível intermediário, produziu L02/L11 e modelo inválido. Após incluir esse nível, o programa construiu o modelo e processou com avisos.

A base N0 foi representada por vínculo engastado, cadastrado no programa em um elemento do tipo sapata com geometria provisória60x60 cm, H1=20/H0=15 cm e colarinho20x30 cm. Esses números foram usados apenas para viabilizar o cadastro do apoio idealizado. Não há sondagem, verificação geotécnica ou dimensionamento de fundação; essa geometria não é uma solução de fundação e não integra a entrega executiva. O novo apoio precisa ter reações, vinculação e continuidade auditadas no modelo analítico.

Com a V2 de30 cm de largura e alturas16/45 cm, o painel Nó apresentou armaduras calculadas nos quatro apoios. Os momentos negativos P6/P5/P12/P4 foram−7,45/−14,40/−39,23/−20,18 kN.m. As armaduras superiores exibidas foram4phi8/5phi10/6phi8/4phi8; P5 eP12 exibiram armaduras inferiores de4phi8 e2phi8. O momento no P5 reduziu em módulo de37,73 kN.m na R208 para14,40 kN.m neste ensaio, com redistribuição para o novo apoio. A estrutura exibiu carga vertical total114,17 tf, área aproximada138,12m² e processamento nativo9 s. O tempo é do cálculo integral, não do desenvolvimento ou da comparação CAD/BIM.

Em seguida, reduziu-se a largura dos três trechos da V2 para20 cm e reprocessou-se. O D16 reapareceu nas quatro células de armadura superior, com momentos−6,12/−13,61/−35,56/−20,10 kN.m. Essa redução não foi adotada. Não foi emitido relatório separado de tempos para esse segundo ensaio; não se atribui a ele o tempo do primeiro.

BIM30-P12-preservado contém a cópia salva do primeiro ensaio. BIM-NOVO-APOIO encerra o segundo ensaio de20 cm, com erro de armadura, para diagnóstico. As capturas distinguem as duas hipóteses. Nenhuma delas foi incorporada ao Revit ou ao CAD como solução final.

## Continuidade necessária

A hipótese P12 com V2 de30 cm deve ter seu status completo, reações e detalhamento conferidos. A ligação ao P6, cuja largura transversal é20 cm, continua exigindo estudo, inclusive a porta P3 próxima na arquitetura. A armadura calculada no painel Nó não comprova resolução dos avisos, da ancoragem, da fissuração, dos pilares ou do apoio idealizado. Depois de fechar a concepção, deve-se reproduzir a mesma geometria no CAD, conferir o intercâmbio e comparar os tempos e correções com escopos equivalentes.

Fontes operacionais: [AltoQi — Aviso38](https://suporte.altoqi.com.br/hc/pt-br/articles/360007183014) e [AltoQi — aplicação de capitéis](https://suporte.altoqi.com.br/hc/pt-br/articles/360016103453). Consultou-se a aplicação de capitéis, mas não se adotou capitel como solução para a ligação de viga neste ensaio.

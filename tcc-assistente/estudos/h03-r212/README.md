# H03/R212 — Uniformização dos pilares e auditoria espacial CAD/BIM

## Cópias e correção efetiva

Criaram-se cópias independentes do BIM R210 e CAD R211 em D:/TCC/outputs/H03-R212-AVISOS-NAO-EXECUTAR. Na abertura BIM executou-se a verificação de projeto danificado oferecida pelo programa, seguida de novo cálculo integral com rigidez fissurada para deslocamentos. Esse cálculo é de controle após a verificação da cópia; seu tempo nativo não foi reemitido e não recebe o tempo herdado R210.

No BIM P3/P4 e CAD P9/P2, respectivamente, a planilha de prumada mostrou seis barras de10 mm no lance L3 e quatro barras de10 mm em L2 e L1. Aplicou-se Uniformizar abaixo apenas nessas prumadas. L2 e L1 passaram de3,14 para4,71 cm², mantendo a bitola10 mm e seis barras; a diferença exibida foi1,57 cm² por lance. Não se alteraram seções, cargas, critérios de resistência ou limites de armadura para eliminar a mensagem. O trecho L1 de altura zero no cadastro de base não é uma peça dimensionada de fundação.

A árvore de status e os diagnósticos reemitidos confirmaram12 pilares do N1 dimensionados, sem avisos ou erros nos dois fluxos. As capturas preservam o antes e o depois. Não houve novo cálculo integral após uniformizar as armaduras; trata-se de ajuste de detalhamento a partir do cálculo existente. Os projetos foram salvos após a alteração.

## Diagnóstico posterior

| Pavimento/elemento | CAD: sucesso/aviso/erro | BIM: sucesso/aviso/erro |
|---|---|---|
| N2 vigas | 14/1/0 | 8/1/0 |
| N2 lajes | 5/0/0 | 5/0/0 |
| N2 pilares | 11/0/0 | 11/0/0 |
| N1 vigas | 16/0/0 | 12/0/0 |
| N1 lajes | 6/0/0 | 6/0/0 |
| N1 pilares | 12/0/0 | 12/0/0 |
| N1 escadas | 3/0/0 | 3/0/0 |
| N0 vigas | 0/1/0 | 0/1/0 |
| N0 pilares | 0/11/0 | 0/11/0 |
| N0 sapatas | 0/0/14 | 0/0/14 |

O diagnóstico não lista deslocamento excessivo. Os erros das14 sapatas e os avisos da base não foram removidos ou tratados como dimensionamento aprovado. A fundação está fora do escopo, sem sondagem; os vínculos de base são idealizações a auditar, e a superestrutura exige verificar as solicitações transmitidas.

## Avisos das vigas

Conferiu-se Aviso08 no CAD V13_1 e BIM V3, no N2. As planilhas de cargas exibem os mesmos valores arredondados: no terceiro trecho, reação permanente−2,78 e acidental−0,41 kN/m; carga mínima−1,67 e máxima−1,27 kN/m. Emitiram-se os detalhamentos e exportaram-se DWGs separados, identificados como não executivos. Os dois desenhos exibem seção20x30 cm, vão livre285 cm, duas barras superiores N4 phi8, C376 cm, segmento principal329 cm, extremidades indicadas24/27 cm; uma barra adicional N3 phi8 C109 cm à esquerda e duas barras inferiores N2 phi8 C329 cm;19 estribos N1 phi6,3 c/15 cm. A igualdade visual desses elementos não verifica comprimentos de ancoragem ou a transferência de esforços no apoio. O aviso permanece e exige revisão específica do detalhamento.

No BIM V1 do N0 confirmou-se Aviso19, flexão oblíqua não considerada pelo dimensionamento automático. Emitiram-se relatórios de esforços e cálculo e captura do detalhe. O relatório de esforços apresenta Nd17,51 kN, Vd18,47 kN, Md positivo0,90 kN.m e negativos−2,04/−2,38 kN.m. O relatório de cálculo adota Md mínimo8,00 kN.m e mostra2phi8 superiores e inferiores, mas isso não verifica a componente horizontal de flexão omitida pelo programa. Não se suprimiu o aviso nem se declarou a escada completamente validada.

## Auditoria dos modelos exportados

Exportaram-se novamente pórtico unifilar, grelhas N1/N2 e grelha da escada em cada fluxo, com seções e coeficientes redutores. SAP2000 não foi executado. O script auditar.py reutiliza o leitor R122 e a comparação espacial R176, preservando as diferenças de sentido I–J. A comparação usa coordenadas, multiconjuntos de segmentos e propriedades, não os identificadores numéricos do arquivo. As unidades declaradas são kgf, cm e graus Celsius; não se equiparam números brutos a kN.

| Modelo | Nós por fluxo | Barras por fluxo | Coordenadas e segmentos sem sentido | Propriedades por segmento sem sentido |
|---|---:|---:|---|---|
| Pórtico | 148 | 183 | Iguais | Iguais |
| Escada | 298 | 389 | Iguais | Iguais |
| Grelha N1 | 473 | 844 | Iguais | Diferentes |
| Grelha N2 | 443 | 794 | Iguais | Iguais |

No pórtico coincidem as14 condições de apoio, as324 linhas de combinações exportadas, os12 padrões de ações, as13 definições de casos, as propriedades de materiais e de seções. As tabelas orientadas de barras e cargas não são idênticas. Há20 linhas de forças nodais globais diferentes, com diferença máxima0,0421 kgf em força e0,0097 kgf.cm em momento, sem chave posição/ação ausente. Na grelha N2 há nove linhas nodais diferentes, com máximo0,0003 kgf. As tabelas de forças nodais da escada e da grelha N1 coincidem. Isso não demonstra equivalência de todas as cargas de barras, pois a inversão dos eixos locais não foi transformada nesta comparação.

Na grelha N1, a seção R30x20 do trecho P12–P5 tem I33=20000 cm⁴ no CAD e18540 cm⁴ no BIM, diferença−1460 cm⁴ (−7,3% em relação ao CAD). A seção aparece em três barras entre x359 e436 cm, y390/z320 cm. As dimensões30x20 e os modificadores explícitos de flexão são os mesmos. A janela Modelo do BIM mostrou modificadores de flexão iguais a1. A origem da inércia diferente permanece em investigação; não se alterou manualmente o valor exportado para forçar igualdade. A V2 unificada no BIM e as V2/V14 separadas no CAD são uma hipótese de causa a testar, não uma conclusão demonstrada.

## Continuidade e reações do P12

A exportação dos dois pórticos mostra o P12 em x355/y390 cm nos níveis0,20,177,4 e320 cm. As três barras verticais cobrem0–20,20–177,4 e177,4–320 cm; o nó de cota0 está restringido nos seis graus de liberdade. Não há prolongamento do P12 acima do N1. Essas condições foram conferidas por asserções no script e confirmam o cadastro analítico, sem validar o engaste fisicamente ou uma fundação.

Emitiu-se Relatório de Cargas nas Fundações no BIM. O P12 apresenta parcelas42,43 kN próprias,10,17 adicionais,12,02 acidentais e−0,06 de manutenção; a coluna Carga máxima positiva mostra68,39 kN e negativa0. O relatório soma803,27/138,86/184,35/17,80 kN nas quatro ações verticais, total1144,28 kN, coerente com o diagnóstico na precisão apresentada. Não se soma a coluna de máximos individuais como combinação simultânea. O sinal negativo isolado da parcela de manutenção não significa, por si só, levantamento da base.

## Tempo, validação e continuidade

Os9 s CAD/BIM das revisões R210/R211 continuam válidos apenas para aquelas execuções. Não se transfere esse valor ao cálculo de controle BIM R212, e não se mediu uma etapa de correção pareada com condições iguais nesta revisão. O tempo exclusivo de inferência da IA e o tempo humano não são inferidos a partir da duração de arquivos ou das capturas.

Executaram-se a auditoria nos oito arquivos reais exportados e quatro testes unitários da comparação R176 (renomeação de identificadores, carga movida com mesma resultante, diferenças reais e rejeição de dados incompletos/duplicados). São verificações de extração e comparação, não testes normativos de dimensionamento. Revit e DWG de autoria ainda precisam receber a geometria final compatibilizada. Os DWGs de detalhes aqui são exportações de diagnóstico, sem liberação para execução.

Fontes operacionais: [AltoQi — Aviso10](https://suporte.altoqi.com.br/hc/pt-br/articles/115002412574), [uniformização de barras](https://suporte.altoqi.com.br/hc/pt-br/articles/115003099673), [Aviso08](https://suporte.altoqi.com.br/hc/pt-br/articles/360003993253) e [Aviso19](https://suporte.altoqi.com.br/hc/pt-br/articles/360009988354). A aplicação dessas rotinas não substitui a verificação do projeto e de seus detalhes.

# R221 — Reforço inferior da V1 e revisão da triagem de ancoragem

Arquivos locais: `D:/TCC/outputs/H03-R221-VERIFICACAO-ANCORAGEM-NAO-EXECUTAR`. Criaram-se cópias completas dos dois projetos R220 fechados. O estudo continua limitado à superestrutura, com apoios idealizados e sem dimensionamento de fundações.

## Alteração mantida no Eberick

Na V1 do N0 dos fluxos CAD e BIM, selecionou-se a armadura inferior na tabela Vão e utilizou-se o comando nativo **Acrescentar barra** (Alt+M). A seleção passou de 2Ø8 para **4Ø8 inferiores**. O detalhamento confirmou quatro barras C120, com segmento cotado de 104 cm e ganchos de 10 cm nas duas extremidades. Mantiveram-se duas barras superiores C154 com ganchos de 27 cm e quatro barras laterais Ø8 (duas por face). Não se alteraram cargas, seções, resistência ou limite global dos estribos. Salvou-se pelo comando Ctrl+B. Os dois projetos foram fechados e reabertos sem solicitar recuperação; confirmou-se a retenção das quatro barras inferiores. A opção superior adicional foi desmarcada no CAD após sua primeira releitura, e no BIM antes da releitura final.

Exportou-se pela interface o detalhe BIM como `BIM-V1-nativo.dxf`. A extração dos textos desse arquivo confirmou a indicação da pele **2×2 Ø8 C117**, com segmento de 104 cm e cotas de gancho de 9 cm. O texto sobreposto na captura não deve ser interpretado como C917. O desenho exportado é uma representação esquemática; seus arcos não comprovam o diâmetro físico de dobra.

O complemento transversal R218 continua externo: estribos Ø6,3 com espaçamento máximo de 9 cm e dois grampos por posição. O detalhe automático ainda mostra Ø6,3 c/15. A relação de aço nativa não inclui essa revisão externa. Os desenhos R218 não devem ser usados como representação atual da quantidade de barras inferiores: esta revisão substitui essa informação por quatro barras.

## Ensaio superior retirado

Testou-se a opção As pos sup adicional com quatro barras Ø8. O detalhamento resultou em duas barras superiores C154 com ganchos e duas barras adicionais retas C90, interrompidas antes dos apoios. Essa disposição não comprova a continuidade necessária. Desmarcou-se a opção nos dois projetos; o ensaio não integra a solução mantida. As capturas que contêm `ensaio` documentam a alternativa rejeitada, não o estado final.

## Refinamento do cálculo auxiliar

A triagem R217 concentrava V vertical + V horizontal + tração axial no par de barras. Esse limite não inclui o termo M/z relevante para a armadura de apoio. A R221 acrescenta os limites Mv/(0,9dv) e Mh/(0,9dh), preservando as combinações. Adota-se al/d=1 como hipótese de triagem do Modelo I a 45°. A soma dos planos e de posições diferentes é um critério conservador auxiliar, e não uma fórmula normativa exata de ancoragem biaxial ou uma força simultânea medida em uma barra.

Usam-se os esforços históricos R217 e a grelha R214; não houve nova emissão global de esforços R221. O programa auxiliar não altera PRJ ou binários. A combinação governante CAD é `1.4G1+1.4G2+1.4Q+0.84V1+0.84D1+0.7QT`, com limite de força de aproximadamente 56,974 kN. A análise BIM fornece 56,971 kN; a pequena diferença decorre da reconstrução auxiliar, apesar da igualdade dos valores nativos impressos da R217.

| Grupo hipotético Ø8 | F/(As fyd), CAD | lb,nec com gancho condicionado | Resultado da triagem geométrica |
|---|---:|---:|---|
| 2 barras | 1,3035 | 275,0 mm | Não passa |
| 3 barras | 0,8690 | 183,3 mm | Não passa |
| 4 barras | 0,6517 | 137,5 mm | Passa somente a comparação preliminar de comprimentos |

A projeção até o eixo nominal da dobra é 159,7 mm, descontando cobrimento, estribo e meio diâmetro, em vez dos 170 mm nominais da triagem inicial. Não se confunde essa projeção com comprimento reto até o início da curva. O espaço livre nominal entre quatro barras em uma camada é 31,8 mm, frente a 30 mm pelo agregado adotado. Para Ø8 CA-50, considerou-se pino de dobramento mínimo de 40 mm e ponta reta de gancho a 90° mínima de 64 mm, conforme itens 9.4.2.3 e 9.4.2.5 da NBR 6118:2026 disponível localmente. O fator 0,7 só é usado na hipótese de cobrimento normal ao gancho ≥3Ø. A hipótese de boa aderência também precisa ser confirmada por barra.

**A V1 permanece sem verificação integral concluída.** A triagem do grupo de quatro barras não comprova a distribuição entre barras inferiores, superiores e laterais, o confinamento, a geometria das dobras e a transferência aos apoios. Permanecem Aviso 19 e dois Avisos 98. A ligação aos apoios idealizados e a armadura superior continuam pendências essenciais; não são classificados como ajustes cosméticos.

## Cobertura

Na viga BIM V3 do N2, confirmou-se o detalhe com duas barras superiores contínuas C376 (segmento de 329 cm e ganchos de 24/27 cm), uma adicional Ø8 C109 à esquerda, e duas inferiores C345 com ganchos de 10 cm. A tabela Nó indicou Md −13,16 kN.m e 3Ø8 à esquerda, e −8,01 kN.m e 2Ø8 à direita. O vão livre permaneceu 285 cm e a seção 20×30 cm.

Testou-se individualmente a distância máxima para unir negativos de 200 para 300 cm. O detalhe principal permaneceu igual; restabeleceu-se 200 cm. Não se manteve uma alteração sem efeito demonstrado. O Aviso 08 continua registrado e exige a conferência do escalonamento e da ancoragem, conforme a [orientação oficial da AltoQi](https://suporte.altoqi.com.br/hc/pt-br/articles/360003993253). A observação de barras contínuas não é aprovação completa desse aviso.

## Validação e sequência

Sete testes do cálculo auxiliar passaram, cobrindo a inclusão dos momentos, a distinção de compressão e tração, o cobrimento para gancho, as dimensões mínimas de dobra e os limites de acomodação. Eles verificam o código auxiliar e não aprovam o edifício. Não se apresenta esta revisão como ensaio pareado de produtividade e não se atribuem tempos antigos ou tokens a ela.

Prosseguir pelo detalhe completo de ancoragem da V1, conferência do Aviso 08 e dos apoios/compatibilização; depois sincronizar a geometria Revit/CAD e emitir resultados finais pareados. Os originais escritos e as revisões R218/R220 foram preservados.

```text
python -m unittest discover -s tcc-assistente/estudos/h03-r221 -p test_ancoragem.py -v
python tcc-assistente/estudos/h03-r221/ancoragem.py D:/TCC/outputs/H03-R217-V1-VERIFICACAO-NAO-EXECUTAR/R217-resultados.json D:/TCC/outputs/H03-R221-VERIFICACAO-ANCORAGEM-NAO-EXECUTAR/R221-ancoragem.json
```

# H03/R185 — reconciliação geométrica e agrupamento das vigas

Estudo preliminar, não executar. A auditoria cobre os **IFCs de referência R178**, anteriores aos ensaios nativos R182/R184. Não se trata de nova exportação dessas revisões nem de aprovação de dimensionamento. O procedimento apenas lê os arquivos; seus hashes permaneceram iguais ao registro R178.

## Resultado da correspondência

| Unidade de contagem | CAD | BIM |
|---|---:|---:|
| Peças exportadas como IfcBeam | 48 | 48 |
| Peças em N1 | 20 | 20 |
| Peças em N2 | 28 | 28 |
| Grupos por nome e pavimento | 31 | 21 |
| Grupos em N1 | 16 | 12 |
| Grupos em N2 | 15 | 9 |
| Peças sem correspondente geométrico | 0 | 0 |

As 48 peças receberam correspondência única pelos prismas fechados, e os pavimentos normalizados dos pares concordaram. A soma dos volumes prismáticos é 7,1956 m³ em cada exportação. Essa soma não desconta eventuais interseções entre peças, não representa volume líquido de compra e não foi utilizada para comparar consumo de concreto dimensionado.

Identificaram-se **21 componentes de correspondência entre os agrupamentos**: doze relacionam um grupo CAD a um grupo BIM; nove relacionam múltiplos grupos CAD a um único grupo BIM. Os nove componentes explicam a redução de 31 para 21 grupos sem desaparecimento das peças exportadas. Não se encontrou agrupamento de um CAD para vários BIM ou muitos para muitos nesses arquivos; o algoritmo também contempla essas situações.

O arquivo `R185-correspondencia-vigas.md` apresenta os 48 pares, suas coordenadas e os 21 componentes. O JSON contém GUIDs de ambos os fluxos para rastreabilidade. Identifica-se o grupo pela combinação de pavimento e nome, evitando fundir vigas homônimas de pavimentos diferentes.

## Relação com o dimensionamento

O grupo BIM **N1/V2** corresponde aos grupos CAD **N1/V2 e N1/V14**, confirmando e ampliando o mapeamento pontual da R182. A V16 do patamar corresponde a um grupo de mesmo nome em cada fluxo. A existência de dois trechos físicos geometricamente iguais não comprova igualdade de continuidade de armadura, vinculação, rigidez ou tratamento de mudanças de seção.

A contagem de grupos coincide com as contagens de vigas dos relatórios nativos R182: 31 no CAD e 21 no BIM. Essa coincidência entre registros de revisões diferentes não substitui uma exportação atualizada R182. O diagnóstico nativo permanece um grupo BIM com D16/A07 e LE3 com D31/A11 nos dois receptores.

Consequentemente, **não se deve apresentar a divisão 0/31 versus 1/21 como taxa comparável de erros físicos**. Antes de ranquear os fluxos, deve-se registrar a correspondência e verificar se o grupo contínuo foi concebido e detalhado de modo equivalente. A diferença pode contribuir para a investigação da V2, mas a R185 não demonstra relação causal entre agrupamento e A07. Tampouco elimina diferenças de cargas nodais e de modelo analítico já documentadas na R179.

## Método e validação

Para cada IfcBeam, obtém-se a malha em coordenadas globais e metros pelo IfcOpenShell. A função de validação R182 exige oito cantos de um prisma retangular, doze triângulos não degenerados, fechamento das arestas e área completa nas seis faces. Permite-se mudar a diagonal de triangulação de uma face sem caracterizar mudança no sólido. Não basta igualdade de bounding boxes.

Compara-se a assinatura das coordenadas mínimas e máximas somente após validar o prisma, com arredondamento computacional de 10⁻⁷ m. Essa precisão não constitui tolerância de execução. O procedimento rejeita prismas duplicados, GUIDs repetidos e associações ambíguas, em vez de escolher um par arbitrário. Não utiliza apenas nomes para provar correspondência geométrica.

Os nove testes R185 verificam agrupamento distinto sem perda de peças, duplicidade geométrica/GUID, rejeição de bounding box sem prova do prisma, peça sem par, divergência de pavimento, nomes repetidos entre níveis, componente muitos para muitos e nível não identificado. Os testes R182 cobrem a validação geométrica do prisma, incluindo triangulações diferentes e faces inválidas. São testes de código e dados IFC, sem equivaler a teste de armaduras no Eberick.

## Escopo remanescente

Não houve processamento nativo nesta auditoria; não existe nova duração de CAD/BIM a somar aos tempos anteriores. O tempo de leitura computacional não foi contabilizado como tempo de produção em nenhum fluxo. Permanecem pendentes a solução física/ancoragem da base da escada, o ensaio de gancho, cisalhamento/ELS, a continuidade da V2, o conflito V16/J4 e a comparação integral com tempos de escopo equivalente. Não se alteraram os arquivos nativos ou a monografia.

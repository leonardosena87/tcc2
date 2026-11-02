# H03/R152 — opção atual: 17 espelhos, dois lances retos e patamar

Por determinação do usuário — **“coloque com 17 espelhos”** — a alternativa atual do estudo passa a 17 espelhos iguais, distribuídos em 8 no primeiro lance e 9 no segundo, mantendo o formato em U com patamar. As alternativas R149/R151 de 18 espelhos permanecem no histórico e deixam de ser a escolha atual. A restrição anterior de preservar paredes, portas, fachada e pisos não foi revogada.

O desnível acabado é 3,03 m: cada espelho mede exatamente 3,03/17 m (17,823529… cm). O patamar acabado passa a +1,645882… m, aproximadamente 5,4 cm abaixo de +1,70 m. Mantêm-se pisos +0,22/+3,25 m. Com a hipótese de pisada de 28 cm, o primeiro lance tem sete intervalos e projeção 1,96 m; o segundo tem oito e projeção 2,24 m. A relação geométrica 2e+p resulta em 63,647 cm, sem declaração de atendimento normativo global. Conservar a precisão interna do quociente; o valor arredondado de exibição não substitui a amarração às cotas dos pisos.

Foram gerados definição JSON, imagem/SVG e perfil DXF independente, em metros. O perfil está desdobrado para apresentar os 17 espelhos; não é corte espacial da escada em U, não contém espessura resistente nem representa apoios calculados. O DXF não substitui o DWG do projeto e não foi aberto/validado dentro do AutoCAD nesta revisão.

## Encaixe ainda não resolvido

A projeção do lance superior excede a referência gráfica em cerca de 28 cm. Preservar o patamar e a face sul faria o hall gráfico remanescente cair de aproximadamente 0,889 para 0,609 m. Preservar o hall deslocando o início do patamar reduziria sua profundidade gráfica de aproximadamente 0,902 para 0,622 m. **Nenhuma dessas reduções foi adotada ou autorizada automaticamente.**

A linha de chegada calculada mantendo o patamar fica em Y local aproximadamente 3,216 m. Ela entra na faixa longitudinal da porta S-P3-01, conforme a referência R68. Trata-se de uma interferência de triagem com medidas gráficas aproximadas; faces, folhas, níveis e corte precisam ser conferidos. Não se deslocou nem removeu a porta. Não se considerou que a escolha de 17 autoriza alterar paredes ou reduzir circulação.

## Estado da aplicação

A escolha está registrada como definição atual em D:/TCC/dados-pesquisa/escada-h03-atual.json, apontando para o JSON desta revisão com seu hash. **Os modelos nativos Revit, AutoCAD e Eberick ainda não receberam a escada**, pois o encaixe, altura livre, largura útil, estrutura de apoio e espessuras continuam pendentes. Não foram aplicadas novas cargas ou modificada a monografia.

Ao resolver a posição, ambos os fluxos deverão receber a mesma geometria, níveis, apoios e cargas antes da nova comparação no Eberick. O relógio desta revisão mede apenas a execução do script de geração, não tempo total da IA ou tempo final dos fluxos. As fontes geométricas R147/R68 são preservadas por SHA-256. A numeração de 17 espelhos e a conta de 15 pisadas mais patamar são verificadas por testes; isso não constitui dimensionamento ou aprovação estrutural.

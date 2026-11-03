# Escada LE3 · localização dos esforços na grelha

A consulta no Eberick localizou o máximo positivo exibido para a combinação 1,4G1 + 1,4G2 + 1,4Q + 0,7QT na barra 309, próxima à base do lance inferior. A captura registra o modo **Elástico · Axiais** e a unidade **kN/m**. Os dois valores seguem a ordem do painel, que não nomeia os extremos. As coordenadas abaixo vêm dos arquivos analíticos de referência R178. A leitura dos esforços foi feita no CAD R192.

| Posição na grelha | Barra | X de referência (cm) | Leituras na tela (kN/m) |
| --- | ---: | ---: | ---: |
| Base, lado próximo ao vão entre lances | 309 | 528,75 | 86,52 e 87,97 |
| Base, faixa interna | 315 | 506,25 | −1,44 e 0,00 |
| Base, faixa interna | 321 | 483,75 | −1,44 e 0,00 |
| Base, lateral oposta | 327 | 461,25 | 60,50 e 61,94 |
| Encontro com o patamar, na mesma linha da barra 309 | 304 | 528,75 | 38,65 e 40,09 |

Nos dois arquivos R178, a barra 309 chega a Y = 321,58 cm e Z = 20 cm. A barra 304 chega ao patamar em Y = 97,58 cm e Z = 177,4 cm. As cinco barras têm as mesmas coordenadas nos modelos CAD e BIM de referência. A correspondência com a R192 se baseia na posição em planta e na identificação exibida. A confirmação de todas as coordenadas da R192 depende de exportação própria.

Na referência, o nó inferior da barra 309 se liga a duas barras transversais do bordo. Nas extremidades externas desse bordo, os elementos analíticos 163 e 164 descem 20 cm até dois nós com as seis restrições ativas. A ancoragem física do aço nesse apoio idealizado permanece por definir. Na barra 309, a tela da R192 mostra os multiplicadores locais de rigidez em 1 e o vínculo de extremidade como engastado.

Há concentração lateral do esforço axial na combinação consultada. Para atribuir o A11 a um bordo específico, falta confrontar os momentos positivos nas extremidades, a combinação determinante e o comprimento disponível para a armadura. A [descrição da AltoQi sobre a ancoragem](https://suporte.altoqi.com.br/hc/pt-br/articles/115003202014) fundamenta essa distinção. A localização do pico orienta a análise do apoio inferior antes de qualquer alteração física.

A R193 é uma leitura do PRJ CAD R192. A conferência preservou o arquivo por SHA-256. O esforço do BIM, a equivalência de dimensionamento e os tempos totais dos dois fluxos continuam em aberto.

# H03/R108 - varanda P1, alternativa para ensaio de sensibilidade

Definiu-se a alternativa VP1-A para estudar a parcela nominal de3,15m2 da cobertura P1, antes excluida das13 cargas A1/A2. A alternativa e uma concepcao analitica preliminar: dois bracos metalicos em balanco na direcao X, em Y3,90 e7,05m, recebem uma barra longitudinal no centro da faixa, X10,15m. O transporte das resultantes aos nos existentes em X9,65m inclui o momento da excentricidade de0,50m. Nao se declarou a viabilidade dos perfis, ancoragens ou nos de concreto e nao se elevou a arquitetura.

Mantiveram-se as hipoteses unitarias R59: G=0,330897761180176kN/m2 horizontal e QT=0,25kN/m2 horizontal. G inclui telha e reserva metalica0,15kN/m2; essa reserva ainda nao resulta de levantamento de perfis. A area por eixos nominais nao e quantidade liquida de telha. O forro e a sobrecarga da laje permanecem separados.

| Acao | Cada Fz (kN) | Cada My (kN.m) | Soma de forcas descendentes (kN) |
| --- | ---: | ---: | ---: |
| G adicional | -0,521163974 | +0,260581987 | 1,042327948 |
| Q_TELHADO_MANUTENCAO | -0,393750000 | +0,196875000 | 0,787500000 |

As cargas sao as acoes transmitidas ao concreto, em eixos globais. Fz negativo aponta para baixo. Para braco r=(+0,50;0;0) e forca vertical negativa, o produto vetorial r x F fornece My positivo. A reacao do concreto sobre o metal possui sentido oposto; nao deve ser digitada no lugar da carga sobre o concreto. A documentacao oficial descreve as seis componentes nodais e a convencao pela mao direita: [AltoQi - cargas concentradas](https://suporte.altoqi.com.br/hc/pt-br/articles/115003467013).

Conferiu-se o equilibrio da forca e dos dois momentos globais da carga distribuida no retangulo X9,65..10,65/Y3,90..7,05. A exclusao de My preservaria o peso, mas perderia o efeito excentrico. Dois controles sinteticos verificam o transporte completo e rejeitam geometria/carga invalida; nao verificam resistencia ou deformacao.

A geometria historica R56, vinculada por hash a R60, identifica os seguintes candidatos de topo N2: CAD P8/BIM P7 em9,65;3,90m e CAD P9/BIM P3 em9,65;7,05m. A cota6,39m e a referencia do topo de concreto existente, sem atribui-la ao plano inclinado de telhas. Nome/GUID historico nao dispensa reler o alvo no receptor atual antes de qualquer lancamento. O plano JSON registra aplicacao nativa falsa; eventual ensaio posterior exige evidencia separada e releitura apos salvar/fechar/reabrir.

Esta alternativa nao encerra P2, reservatorio, paredes, escada, vento/succao, ligacoes ou verificacoes locais. A estrutura metalica precisa de verificacao de capacidade, estabilidade, flecha, ancoragens e compatibilidade espacial. Nao se atribui viabilidade construtiva ao simples equilibrio das resultantes. Os13 pontos A1/A2 nao sao alterados nem acrescidos outra vez. Nao se editou RVT, DWG, PRJ ou monografia nesta R108.

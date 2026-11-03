# H03/R204 — Comparação do lançamento da parede W08 no patamar

Foram exportados separadamente no Eberick 2025 Infinity o pórtico, a grelha da escada e as grelhas dos dois pisos de cada cópia derivada da R201. A verificação considera a ação distribuída G2 da parede superior. A ação G1 e as cargas pontuais provenientes da grelha pertencem a outros lançamentos.

| Observação no pórtico | CAD | BIM |
|---|---:|---:|
| Barra da V16 e nós inicial e final | 42, 89–90 | 42, 89–90 |
| X inicial e final na cota Z = 177,4 cm e Y = 0 | 441 a 654 cm | 441 a 654 cm |
| Intervalo relativo de G2 exportado | 0 a 1 | 0 a 1 |
| Nós nas faces da parede, de X = 450 a 645 cm | 87 e 88 | 87 e 88 |
| Barras incidentes no nó 87 | 35 e 122 | 35 e 122 |
| Barras incidentes no nó 88 | 36 e 123 | 36 e 123 |

O excesso geométrico é de 9 cm em cada extremidade nos dois modelos. Com o carregamento nominal de projeto de 6,75454 kN/m, o produto pelo comprimento atual é 14,3872 kN. O pano livre de 1,95 m corresponde a 13,1714 kN. A diferença nominal é 1,2158 kN por modelo. O arquivo SAP declara kgf e cm. Esses produtos utilizam o valor SI de projeto, sem interpretar os números brutos exportados como medições no SI.

No croqui CAD, a V16 apresentou seção 20 × 30 cm e carga de parede exibida de 6,75 kN/m. O comando de adição de nó em (450, 0) informou que já existe um nó nessa posição no pavimento. Ao encerrar a consulta, a edição experimental foi descartada. O SHA-256 de cada PRJ da R204 coincidiu com o da respectiva R201 após as exportações.

Para conferir uma correção mantendo o eixo analítico observado, o intervalo relativo esperado da carga distribuída é de 9/213 a 204/213 (aproximadamente 0,042254 a 0,957746). Se o programa subdividir a barra, deve-se conferir a soma das extensões físicas carregadas e a resultante nas novas barras. A comparação deve isolar a carga distribuída da parede, preservar a transferência das cargas pontuais da escada e verificar ausência de duplicidade. A parte inferior da W08 requer identificação independente do seu apoio.

No levantamento de retrabalho, registrar a W08 superior como uma ocorrência comum a cada fluxo, de mesma origem no lançamento realizado no Eberick. R204 documenta o diagnóstico. Não houve correção persistida, novo processamento ou medição completa de duração de retrabalho nesta etapa.

As exportações originais estão nas subpastas SAP-CAD-antes e SAP-BIM-antes de D:/TCC/outputs/W08-H03-R204-COMPARACAO-NAO-EXECUTAR.

SHA-256 do pórtico CAD: 59390625831F6F80DD76156D81AF3071D263DCC1A1B1C803DEC65EEA953123C1

SHA-256 do pórtico BIM: 88F9F0EF9BEAE24F4D9C1BE956917DB79833FDB79ABE0F3B0974E3BB994173E4

[Procedimento da AltoQi para cargas em um trecho de viga](https://suporte.altoqi.com.br/hc/pt-br/articles/360046158854)

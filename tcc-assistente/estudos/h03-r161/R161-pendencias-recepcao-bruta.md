# R161 — pendencias observadas na recepcao bruta

O conjunto abaixo e parcial: 12 origens associadas com diferencas em relacao aos parametros nominais do Revit. Os 12 desvios de topo ja existem na malha IFC bruta; nao representam 12 novos erros introduzidos pelo Eberick. Duas origens apresentam diferenca adicional de altura no receptor: V4A-N1 e V15-N1, de 0,02 m na caixa da malha bruta para 0,05 m na caixa receptora. Nao e o total final de correcoes. A associacao espacial nao prova conectividade analitica.

| Origem Revit | Parte Eberick | Topo fonte (m) | Topo receptor (m) | Altura fonte (m) | Altura receptor (m) |
|---|---|---:|---:|---:|---:|
| V10-N1 | V4 | 3.200000 | 3.060000 | 0.350000 | 0.210000 |
| V10-N2 | V6 | 6.390000 | 6.250000 | 0.300000 | 0.160000 |
| V12-N1 | V5 | 3.200000 | 3.060000 | 0.350000 | 0.210000 |
| V13-N2 | V7 | 6.390000 | 6.250000 | 0.300000 | 0.160000 |
| V15-N1 | V3 | 3.200000 | 3.060000 | 0.160000 | 0.050000 |
| V3-N1 | V1 | 3.200000 | 3.060000 | 0.450000 | 0.310000 |
| V3-N2 | V2 | 6.390000 | 6.250000 | 0.300000 | 0.160000 |
| V4A-N1 | V1 | 3.200000 | 3.060000 | 0.160000 | 0.050000 |
| V4A-N2 | V2 | 6.390000 | 6.250000 | 0.300000 | 0.160000 |
| V4B-N1 | V2 | 3.200000 | 3.060000 | 0.300000 | 0.160000 |
| V4B-N2 | V3 | 6.390000 | 6.250000 | 0.300000 | 0.160000 |
| V9-N2 | V6 | 6.390000 | 6.250000 | 0.300000 | 0.160000 |

## Investigacoes adicionais

- V9-N1 e V13-N1 nao foram associadas pelo criterio nominal: duas partes permanecem sem associacao devido aos limites longitudinais. Nao foram forcadas nem contadas como correcoes confirmadas.
- 64 solidos de pilares correspondem a segmentacao do receptor; nao equivalem automaticamente a 64 pilares fisicos nem a duplicidades.
- Nenhuma laje ou escada nativa aparece no IFC de controle; conferir lancamento e cargas na etapa de correcao.
- Nove niveis recebidos pelo assistente, com seis IfcBuildingStorey na saida de controle; conferir funcao dos niveis auxiliares antes de simplificar.
- Nome C25 no receptor nao comprova transferencia causal da resistencia: o IFC de entrada nao contem propriedades mecanicas de material.
- Viga do patamar renomeada V1 no receptor. Seus 20 x 30 cm e elevacao zero foram relidos sem editar; a associacao por ID do relatorio e geometria evita comparar apenas os nomes.
- Preservar bruto; executar correcoes em outra copia, medir intervalos e reexportar para conferir os efeitos.

Nenhum calculo estrutural foi executado neste receptor. Apoios, ancoragem, J4, cargas e ELU/ELS permanecem pendentes.

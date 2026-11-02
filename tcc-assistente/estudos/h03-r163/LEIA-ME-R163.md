# R163 — cobertura geométrica do receptor derivado R162

Ensaio de leitura em 02/11/2026. Não altera o trabalho escrito nem RVT, DWG, PRJ e IFC de controle. Não constitui cálculo ou aprovação estrutural.

## Resultado e critério

As cinco peças anteriormente sem associação pelo critério longitudinal estrito foram associadas por eixo, topo, largura, altura e extensão limitada ao volume dos apoios de extremidade da autoria. Foram associadas 33 peças às 30 origens de vigas. As cinco extensões além dos eixos ficam dentro das projeções dos pilares; não foram admitidos avanços arbitrários. A associação usa geometria, não o nome renumerado no Eberick.

Nos trechos entre faces dos apoios, retiradas também as projeções dos pilares intermediários, as 30 origens apresentam cobertura axial observada. A viga V2-N2 é segmentada no pilar intermediário em X=6,55 m; o intervalo de 20 cm ocupado por esse pilar não foi classificado como lacuna de viga. Tolerância computacional de 0,1 mm, explicitamente sem caráter normativo. A malha das peças de vigas foi verificada como caixa ortogonal fechada antes do uso de suas projeções.

Os 64 sólidos de pilares cobrem os intervalos verticais dos 22 sólidos de origem presentes no IFC de entrada. Entretanto, quatro segmentos — P5-N1/P5-N2 e P11-N1/P11-N2, IDs 472934/473029/473143/473144 — terminam 14 cm abaixo do topo nominal lido no Revit. Essa diferença já consta no IFC de entrada: +3,06 em vez de +3,20 m e +6,25 em vez de +6,39 m. Portanto, não é uma nova perda atribuída ao receptor. A causa do corte na exportação/autoria não foi isolada.

No croqui N1 do Eberick R162 observaram-se os rótulos P12(NASCE) e P13(NASCE) nessas duas posições existentes. O diálogo do primeiro foi relido, sem edição: P12, seção 20 × 30 cm, elevação zero. Esses nomes foram atribuídos pelo receptor e não representam os IDs dos dois pilares rejeitados pelo usuário na R159. A observação motivou o experimento R164 de continuidade geométrica.

## Evidência e limites

- `R163-cobertura-geometrica.json`: associações, intervalos, apoios candidatos, lacunas nominais e hashes de entrada/saída inalterados.
- `R163-croqui-N1.png`: duas indicações NASCE; `R163-P12-nativo.txt` e PNGs: leitura do diálogo.
- `auditar_cobertura.py`: auditoria de arquivos com IfcOpenShell, sem edição dos controles.
- `test_cobertura.py`: sete testes de regressão com dados sintéticos, separados da leitura de arquivos reais e da inspeção nativa.

O IFC receptor não contém IfcRelConnectsElements. Projeções, contato geométrico e rótulos do croqui não demonstram toda a conectividade analítica, engastamento, ancoragem, dimensionamento ou segurança. Não houve lançamento de cargas, escada, lajes ou processamento estrutural. Os tempos de execução do script são computacionais e não medem esforço integral da IA, do operador ou do fluxo BIM.

Os arquivos reais permanecem em `D:\TCC\outputs\Intercambio-H03-R163-COBERTURA-GEOMETRICA-NAO-EXECUTAR`. Não reescrever o resultado histórico ao repetir o estudo; criar nova pasta/revisão.

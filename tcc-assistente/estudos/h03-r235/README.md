# H03/R235 — vigas da escada na recepção CAD

Em 6 de novembro de 2026, concluiu-se o lançamento geométrico das duas vigas restantes em cópia independente da R234, no Eberick 2025 Infinity. Diretório: `D:/TCC/outputs/H03-R235-CAD-VIGAS-ESCADA-NAO-EXECUTAR/CAD`. O arquivo nativo conserva o nome interno `R228-CAD-DWG-BRUTO-NAO-EXECUTAR.prj`.

## Resultado observado

A viga CAD V17-BASE-ESC corresponde à V1 do N0, seção 30 × 30 cm, topo +0,20 m, eixo de (4,50; 3,2158) até (5,40; 3,2158) m. A viga CAD V16-ESC-PAT corresponde à V1 do PATAMAR, seção 20 × 30 cm, topo +1,7741 m, entre os pilares existentes P4/P10. Os recortes de extremidade no sólido do patamar correspondem aos volumes dos pilares; não se inseriu outro pilar nesta revisão.

Os 68 elementos anteriores conservaram GUIDs, nomes, níveis, geometria e propriedades. A R235 contém 70 sólidos: 35 trechos de pilar e 35 trechos de viga. No conjunto das etapas CAD R232–R235, representam-se 23 identidades de pilar e 32 identidades de viga da autoria R225. A contagem de trechos do receptor difere da contagem de identidades da autoria.

A auditoria compara as polilinhas, rótulos e metadados do CAD com os sólidos IFC4 exportados do Eberick. Conferiram-se as duas seções, os eixos, as cotas, o C-25 e o cobrimento de 3 cm. A tolerância computacional de 0,1 mm serve à comparação geométrica, sem caráter normativo. Uma reabertura explícita da pasta R235 e nova exportação confirmaram a persistência de todos os 70 elementos e propriedades. O número STEP auxiliar de cada conjunto de propriedades é excluído da comparação semântica.

## Tempos e intervenções

O lançamento do patamar registrou **79 min 49,8 s brutos**, com interrupção e retomada. Esse intervalo não é tempo ativo e não permite ranking. O lançamento da base registrou **5 min 41,4 s brutos**, sem interrupção registrada, incluindo recuperação da entrada de texto e consultas da interface. Também não representa tempo líquido, cálculo estrutural ou fluxo completo. Ambos preservam `netActiveSeconds=null` e seus limites originais de medição.

Houve uma gravação/exportação intermediária fora da observação contínua. Não se atribuiu autoria ou duração a essa ação; conferiu-se o arquivo efetivamente salvo por reabertura e reexportação observadas. Os intervalos não incluem a auditoria posterior nem o backup.

## Pendências que afetam o cálculo

Ao lançar a viga da base, o Eberick indicou ausência de apoio nas duas extremidades. O lançamento foi mantido para conferir a geometria; o apoio idealizado autorizado para o estudo ainda precisa ser definido nesta cópia. Interseção de sólidos não prova vinculação analítica. Não há aprovação estrutural, aplicação de cargas ou dimensionamento nesta etapa.

Faltam nesta rodada de recepção as lajes, a escada, os vínculos/apoios e as cargas. Os projetos já calculados R227 e suas pendências permanecem separados. Não se deve substituir esses projetos por esta cópia ainda não calculada.

`auditar.py` é uma conferência de arquivos reais, somente leitura dos modelos. `consolidar.py` registra o resultado e verifica CRC e hashes de todos os arquivos do backup. Os testes do suplemento não equivalem a cálculo ou validação normativa.

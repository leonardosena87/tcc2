# H03/R133 — sensibilidade da grelha na carga W15

Em cópias dos dois ramos, alterou-se somente a configuração individual da laje L4/N1 de 50 × 50 cm (espaçamento configurado) para 10 × 10 cm (individual), mantendo ângulo 90°. Não se modificaram deliberadamente a arquitetura, a linha da W15, sua intensidade, seções, demais lajes ou ações. A geometria analítica da N1 muda por discretização; isso é documentado nas exportações e não deve ser descrito como geometria analítica inalterada.

As cópias são **52-H03-R133-CAD-W15-GRELHA-NAO-EXECUTAR** e **53-H03-R133-BIM-W15-GRELHA-NAO-EXECUTAR**, em D:/TCC/outputs, derivadas respectivamente das cópias 46/47 da R131. Fechou-se e reabriu-se cada projeto: L4 permaneceu com X=10 cm, Y=10 cm, espessura 14 cm, elevação 0, Q=1,5 kN/m² e revestimento 1 kN/m². A evidência dessa conferência é visual.

## Distribuição da carga exportada

| Medida na grelha N1, igual nos dois ramos | R132 / 50 cm | R133 / 10 cm |
|---|---:|---:|
| Nós totais da N1 exportada | 467 | 2.236 |
| Nós com força G2 da W15 identificada | 2 | 10 |
| Soma Fz | −446,0250 kgf | −446,0250 kgf |
| Centro das forças X | 487,725 cm | 499,434 cm |
| Centro das forças Y | 468,750 cm | 493,360 cm |
| Distância ao centro ideal (497,5;495) cm | 28,01095 cm | 2,53574 cm |
| Diferença de Mx em torno da origem | +11.708,15625 kgf·cm | +731,48100 kgf·cm |
| Diferença de My em torno da origem | −4.359,894375 kgf·cm | +862,61235 kgf·cm |

O afastamento do centro reduziu **90,9473% neste ensaio**. Essa redução caracteriza apenas a sensibilidade dessa representação nodal; não significa redução de erro resistente, de tempo de trabalho ou de custo. A malha mais fina aproximou a posição da resultante, porém os primeiros momentos exatos da linha ideal ainda não foram reproduzidos na exportação N1. Não foi fixada tolerância de aceitação, nem demonstrada convergência com somente duas malhas.

As dez forças de −44,6025 kgf estão em Y=493,36 cm, X de 454,86 a 544,01 cm, Z=320 cm. Não há momentos nodais adicionais nas linhas G2 identificadas. Esses registros são **forças aplicadas**, não reações de apoio. A integral nominal física da W15 continua 4,695 kN/m × 0,95 m = 4,46025 kN; a relação com a exportação usa a convenção de exibição observada na R125 (100 kgf por kN), sem apresentá-la como conversão SI exata.

A distribuição G2 N1 coincide integralmente entre CAD e BIM, inclusive IDs, posições e valores na precisão exportada. A N2 não mudou em nenhuma tabela ante a própria exportação R132/W15. As alterações de tabelas do pórtico e da N1 estão contabilizadas no JSON. Não se conferiram aqui reações ou esforços locais de todas as barras. Não foi executado SAP2000: utilizou-se somente o comando de exportação textual nativa do Eberick.

O controle R132 sem W15 não possuía forças nodais G2, mas **não se processou um controle de 10 cm sem a W15**. Essa limitação impede tratar toda diferença entre modelos como efeito exclusivo da carga; o refinamento também modifica a discretização e a rigidez numérica da laje. A identidade do modelo interno completo com a representação exportada não foi demonstrada.

## Processamento e qualidade da evidência

Executou-se estática linear e deslocamentos do pórtico com rigidez configurada, sem dimensionamento, flechas das lajes, rigidez fissurada ou dinâmica. Ambos terminaram com avisos. O resumo visual permaneceu PP=75,69 tf, G=11,00 tf, Q=17,11 tf, QT=1,78 tf e total=105,59 tf. Área 132,81 m² e relação 795,01 kgf/m²; conserva-se o aviso de relação de carga por área não usual. A coincidência desses números arredondados não demonstra identidade dos esforços locais.

Deslocamentos horizontais exibidos de 0,20 cm e Gama-Z de 1,09/1,08/1,06/1,05 permaneceram iguais na precisão visual. Persiste a divergência de direção do relativo: CAD N1/Y−; BIM TCC-cdd31967-N1/Y+, ambos 0,17 cm. Não se atribuiu causa. O topo completo não foi transcrito nesta revisão e não se afirma sua igualdade.

As imagens JPG foram capturadas e inspecionadas na interface. Parte dos arquivos iniciais UI.txt, incluindo os dois resumos, ficou vazia por falha de captura de acessibilidade: conserva-se essa falha, **não como falta de dados do projeto**. Houve texto nas capturas CAD de grelha original, escopo de análise e exportação; não se generaliza a falha a toda captura. `observacoes-visuais.json` é transcrição visual feita pela IA; não é texto nativo extraído nem OCR automático. A captura conjunta foi ajustada para as próximas consultas. O resumo estruturado não passou pelo parser de acessibilidade usado na R131. As tabelas $2k, ao contrário, foram lidas por parser e auditadas numericamente.

## Esforço e tempo

| Ramo | Sessão exploratória | Comando até registro do término observado |
|---|---:|---:|
| CAD | 14.423 min | 35.293 s |
| BIM | 10.735 min | 41.424 s |

O intervalo do processamento está contido na sessão. Não somar novamente. O registro ocorreu após a primeira captura de conclusão e inclui latência, espera entre consultas e registro; não mede solver isolado. A sessão CAD inclui retomada de contexto, tentativa inicial de localizar o arquivo e correção do conteúdo do campo X antes da confirmação. A sessão BIM inclui consulta de arquivos. Essas condições não são equivalentes para ranking.

A consulta adicional sobre a falha de texto consumiu 1.383 min fora das duas sessões principais; não houve novo processamento nem gravação nessa consulta. A produção do script e relatório não foi cronometrada separadamente como inferência de IA. Tokens, custo e tempo ativo humano não são conhecidos. Os tempos finais dos fluxos permanecem abertos.

## Preservação e aplicação ao TCC

Os 35 arquivos das fontes R131 tiveram hashes conferidos sem alteração. Foram congelados os arquivos das duas cópias experimentais após o processamento; caminhos e SHA-256 estão no JSON. Os artefatos nativos ficam em D:/TCC. O repositório público recebe apenas código e evidência selecionada, sem os projetos binários.

A W15 e o ajuste da grelha foram inseridos no receptor Eberick após a importação. Constituem esforço de complementação e verificação do receptor. Não constituem falha comprovada de transferência do DWG ou IFC, nem benefício específico do CAD ou Revit. Não se alterou a monografia ou os modelos de autoria neste ensaio.

**A W15 permanece experimental, sem aceitação final.** O próximo fechamento exige controle adicional de discretização/alinhamento e efeitos locais; depois, completar paredes, aberturas e respectivos apoios, reservatório/base/acesso, demais ações e combinações, cálculo ELU/ELS completo e sincronização das fontes antes do ensaio final comparável. A referência R116 permanece preservada. Esta revisão não é projeto liberado para execução.

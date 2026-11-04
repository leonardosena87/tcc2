# H03/R208 — Largura da V2 e condição de apoio

Criou-se uma cópia BIM da R207 em D:/TCC/outputs/V2-H03-R208-ESTUDO-NAO-EXECUTAR. A abertura solicitou verificação de projeto danificado; executou-se a verificação interna antes do ensaio. O hash inicial do PRJ coincidiu com o BIM arquivado na R207. A R207 pareada foi preservada.

## Ensaios efetivamente executados no Eberick

| Largura nos dois trechos | Alturas mantidas | Total vertical exibido | Resultado V2 | Processamento nativo |
|---|---|---:|---|---:|
| 40 cm | 16 e 45 cm | 114,34 tf | Armaduras calculadas; três Avisos 38 | 9 s |
| 30 cm | 16 e 45 cm | 113,76 tf | D16 nas células dos três nós; P5 com A07 nas bitolas consultadas | 9 s |

Ambos utilizaram dimensionamento integral e determinação dos deslocamentos do pórtico e das lajes com rigidez fissurada. Os tempos foram extraídos de relatórios emitidos após cada execução e incluem dimensionamento de fundações fora do escopo do TCC. São cenários BIM diferentes, cada um com uma execução documentada. Não se utiliza esta igualdade para concluir produtividade entre Revit e CAD. O tempo de desenvolvimento e de retrabalho desses ensaios não foi cronometrado de forma pareada.

O primeiro ensaio alterou a largura de 20 para 40 cm em ambos os trechos da V2 pela janela de edição. As alturas e elevações permaneceram 16/45 cm e zero, respectivamente. No segundo ensaio, a largura foi reduzida para 30 cm pela planilha de seções, com confirmação das células antes do recálculo. A redução foi testada para avaliar uma alternativa de menor largura; 30 cm continuou sem solução de armadura negativa. Não se demonstrou uma largura mínima entre 30 e 40 cm.

## Armaduras e esforços lidos no ensaio de 40 cm

No painel Nó, leram-se momentos de −7,74 / −37,87 / −30,86 kN.m nos apoios P6/P5/P4. As armaduras superiores exibidas foram 4 phi 8 / 5 phi 16 / 6 phi 8. O apoio P5 também exibiu armadura inferior de 4 phi 12,5, que exige conferir função, posicionamento e ancoragem no detalhamento. No painel Vão, os comprimentos livres foram 190 e 420 cm, com momentos positivos de 2,67 e 45,43 kN.m e armaduras inferiores de 4 phi 8 e 6 phi 8. Esses dados representam a saída do programa para a hipótese, sem liberação para execução.

A árvore de status no N1 exibiu dez vigas dimensionadas e duas com avisos, V2 e V11, sem grupo de vigas com erro. A V2 foi expandida e apresentou três Avisos 38. Assim, o D16 foi eliminado neste ensaio, mas a ligação aos pilares continua pendente.

No ensaio de 30 cm, o painel Nó exibiu −6,84 / −37,73 / −31,14 kN.m e D16 nas células da armadura superior. Consultado o P5, leram-se recusas A07 para 8 / 10 / 12,5 / 16 / 20 mm. Não se alterou o limite de taxa de armadura para eliminar o erro.

## Compatibilização dos apoios

A planilha Nó exibiu larguras transversais de apoio de 30 cm em P6 e 20 cm em P5/P4. Para uma viga de 40 cm centrada, a diferença geométrica corresponde a 5 cm além de cada face em P6 e 10 cm em P5/P4. Esse cálculo pressupõe eixos coincidentes e não substitui a conferência do vão efetivo e dos alinhamentos. A condição deve ser revista no lançamento e no detalhamento, conforme o [procedimento AltoQi para o Aviso 38](https://suporte.altoqi.com.br/hc/pt-br/articles/360007183014).

A alternativa com armadura calculada exige compatibilizar a região de apoio, verificar se eventual mudança de seção dos pilares cabe na arquitetura, conferir sua continuidade entre pavimentos e recalcular a estrutura. Repetir no CAD uma geometria escolhida depende dessa definição. Alargar arbitrariamente o pilar ou desconsiderar o aviso não fecha a verificação da ligação. A revisão das regiões de apoio deve considerar as armaduras superiores e inferiores, a transmissão de esforços e a interferência com portas e circulação.

## Preservação e próximos passos

BIM40-preservado e BIM30-preservado contêm cópias completas dos ensaios salvos; a pasta BIM de trabalho encerra o teste de 30 cm. Os PRJ, hashes, tempos nativos e hipóteses estão em R208-resultado.json. As capturas documentam as seções, os esforços, as armaduras e as mensagens. Os relatórios DOCX nativos permanecem nas pastas dos respectivos ensaios, com extrações TXT identificadas.

O primeiro relatório ficou aberto no Word e bloqueou a segunda emissão. A janela do relatório foi fechada pela interface e a emissão de 30 cm foi repetida com sucesso. Essa ocorrência é uma falha operacional de registro, não um erro estrutural.

A R208 permanece experimental. A próxima revisão deve resolver a ligação V2–P4/P5/P6 e sua compatibilidade arquitetônica, aplicar a mesma decisão ao CAD equivalente e conferir novamente os demais elementos. Permanecem as verificações da V1, dos avisos remanescentes e do apoio do pano inferior W08. O ajuste aproximado da W08 superior continua sujeito às limitações descritas na R207.

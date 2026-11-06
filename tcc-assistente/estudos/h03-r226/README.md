# R226 — Mínimo nativo de12 kN·m e consultas de serviço

Evidências locais: `D:/TCC/outputs/H03-R226-COBERTURA-CONSULTA-NAO-EXECUTAR`. Consultaram-se os projetos R224 derivados da análise R223. Não se alterou a geometria, a armadura ou o cálculo integral nesta consulta; os dois PRJ mantiveram os hashes do manifesto R224. Relatórios novos e capturas ficam preservados separadamente. Não se alterou a monografia.

## Atualização necessária da triagem da V1

Os relatórios detalhados novos da V1, nos dois fluxos, registram seção30×30 cm, C25, Ecs24150 MPa e cobrimento3 cm. O momento utilizado no dimensionamento positivo e nos dois nós é **12 kN·m**. O valor8 kN·m usado na sensibilidade histórica R223 não representa o mínimo atual dessa seção; essa sensibilidade não deve ser usada para concluir a verificação atual.

O modelo auxiliar anterior conservava somente quatro barras de canto. Quando se aplica o mínimo correto12, o índice adicional nesse modelo reduzido atinge1,193. Isso identifica insuficiência desse limite resistente reduzido para a nova sensibilidade; não demonstra falha da armadura real, que tem mais barras.

Reavaliou-se a resistência vertical com as **três barras superiores Ø8 e quatro inferiores Ø8 efetivamente adotadas**, desprezando a armadura de pele. Considerou-se o menor resultado entre os dois sentidos da flexão e os extremos do intervalo axial de cada combinação. Para a resistência horizontal, conservaram-se somente as quatro barras de canto, desprezando as adicionais e a pele. Mantiveram-se os esforços e os intervalos axiais R223, sem inventar novos esforços simultâneos.

O índice linear adicional, com piso vertical12 kN·m, resultou **0,850897 no CAD e0,850892 no BIM**, inferior a1 nesse critério. O piso mínimo é uma sensibilidade de dimensionamento, não um novo vetor de esforços observado. Essa soma linear é uma triagem conservadora adotada no estudo; não se apresenta como a verificação normativa biaxial completa. O resultado não encerra ancoragens, nós, contato com solo, aderência ou efeitos locais.

A integração usa concreto parábola-retângulo, aço elastoplástico e deformação plana de seção. Empregou-se centro de barra a40,3 mm da face, correspondente a30+6,3+4 mm, mais interno que a altura útil26,10 cm informada pelo cálculo nativo. Não se forçou igualdade entre esses dois modelos. Quatro testes controlam a integração por quadratura independente, reproduzem o caso simétrico anterior, distinguem os dois sentidos assimétricos e demonstram o efeito do mínimo12 sobre o modelo reduzido e a armadura adotada.

## Informações nativas de serviço e esforço transversal

Na V1, os relatórios registram fissura **0,00 mm na precisão impressa** para os três pontos apresentados; o diagrama de deslocamentos, em envoltória de aceitabilidade visual, mostra0,00 cm nos dois fluxos. Esses registros não significam ausência física de fissuras ou deslocamentos e não comprovam o ELS da flexão horizontal, a ligação ou a fundação idealizada.

O cálculo transversal nativo da V1 informa Vd18,96 kN, VRd2=339,77 kN e índice de interação cisalhamento/torção0,06; mantém estribos Ø6,3 c/15 e armadura de pele2×2Ø8. O relatório detalhado descreve a flexão reta contemplada pelo programa. O Aviso19 e a necessidade de análise complementar permanecem. O complemento gráfico externo da R224 não modifica a armadura automática nem constitui, sozinho, encerramento da ancoragem.

Para a cobertura CAD V13_1/BIM V3, o relatório detalhado apresenta momentos de dimensionamento8,00/13,16/8,01 kN·m nas posições pertinentes, com nós intermediários sem apoio mostrando0,00; fissuras impressas0,05/0,07/0,05 mm. O cortante de cálculo é27,10 kN no CAD e27,11 kN no BIM. O diagrama visual BIM mostra total−0,11 cm para V3; não se atribui essa observação ao CAD sem captura correspondente. A R224 compara separadamente todos os3.654 valores de casos/combinações. O **Aviso08 continua aberto** para revisão do escalonamento e da ancoragem superior.

## Reprodutibilidade e alcance

`python verificar.py <R223-resultados.json> <saida-json>` refaz a triagem com o mínimo12 e a armadura3/4. `python consolidar.py <pasta-R226>` lê os quatro relatórios, compara campos e verifica os hashes/CRC dos PRJ. O software auxiliar não modifica os projetos nativos. A consulta de relatórios é execução real no Eberick; os testes de integração são verificações do código, não ensaios físicos ou validação independente do programa inteiro.

Não houve novo processamento integral ou cronometragem pareada nessa revisão. Os10/11 s continuam pertencendo à R223. Não se converte a duração da auditoria, o tempo da conversa ou as datas dos arquivos em duração do fluxo. O estudo permanece limitado à superestrutura, com apoios idealizados e sem dimensionamento de fundações. A emissão das ancoragens e interfaces finais continua necessária antes de qualquer liberação executiva.

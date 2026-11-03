# H03/R196 — Reprocessamento da parede W08 sem a janela J4

Revisão acadêmica parcial para conferência pelo orientador. Os dois arquivos PRJ correspondem a cálculos independentes no Eberick 2025 Infinity. O ponto de partida estrutural foi a R188 de cada fluxo e o levantamento geométrico foi a R195.

Na viga V16 do patamar, de seção 20 × 30 cm, adotou-se que todo o pano superior descarrega na viga. A espessura acabada é de 15 cm. A altura de 4,316 m e o peso superficial adotado de 1,565 kN/m² resultam em 6,75454 kN/m. O campo de parede, antes zerado, passou a exibir 6,75 kN/m. O peso próprio da viga foi mantido. Os 7,26 kN associados ao fechamento da abertura já estão contemplados no levantamento da parede inteira.

Ambos os modelos passaram de 111,74 para 113,18 tf de carga vertical total e de 12,58 para 14,02 tf de carga adicional. A leitura após reabertura do BIM mostra 2,13 m entre P9 e P10. Aplicar 6,75454 kN/m nessa extensão representa 14,39 kN, enquanto o pano livre de 1,95 m pesa 13,17 kN. A diferença de 1,22 kN (9,2% do peso do pano superior) requer reconciliação do comprimento de aplicação. Ainda falta identificar o elemento que recebe os 3,83 kN da parede abaixo da V16 e conferir se essa carga já está contemplada em outro lançamento.

Cada relatório registrou 7 s de processamento, incluindo 2 s de dimensionamento. Uma execução por fluxo. A medição exclui preparação, lançamento, correções e inspeção. Ambos os processamentos terminaram com avisos. Para as vigas do N1, o CAD registrou 16 com sucesso. O BIM registrou 11 com sucesso e uma com erro, com V2 destacada em vermelho na planilha. A contagem de vigas difere entre as representações. Esse resultado isolado não permite classificar o retrabalho dos fluxos.

Na envoltória da V16 reaberta no BIM, o Eberick exibiu Vd inicial de 30,52 kN, Vd final de 30,66 kN, Md positivo de 16,95 kN·m, Md negativo de −22,68 kN·m e Mtd de 0,10 kN·m. Essa leitura corresponde à distribuição de parede modelada na R196. A conclusão do processamento não constitui liberação para execução.

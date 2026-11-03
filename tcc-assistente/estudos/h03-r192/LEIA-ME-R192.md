# H03/R192 — Encontro do lance inferior com o patamar

Ensaio diagnóstico no fluxo CAD, sem novos pilares ou viga física. Não executar. A cópia principal pareada R178 foi preservada.

O teste alterou de 0 para 20 cm a largura da barra ordinária no encontro LE3/LE1. Herdou da R191 a largura hipotética de 20 cm da barra inferior, a ancoragem com gancho e a permissão de ancoragem na laje adjacente. Esses campos não comprovam que existe concreto suficiente para ancoragem ou que o apoio tem capacidade resistente.

A abertura apresentou aviso de integridade. Executou-se a verificação nativa e um novo cálculo de controle antes da alteração. Desta vez, a cópia de controle recalculada foi efetivamente salva pelo botão de disco e possui hash diferente da fonte. O PRJ final também possui hash diferente; a largura de 20 cm foi relida depois do processamento. Não se realizou conferência após fechar e reabrir a R192.

O controle e o ensaio mantiveram LE1 e LE2 calculadas e LE3 com D31/A11 nas cinco bitolas: 6,3; 8; 10; 12,5 e 16 mm. A alteração não resolveu o erro e ainda não identifica o bordo governante. O resumo de pilares, vigas e lajes não comprova aprovação da escada.

O relatório nativo registrou 6 s no controle e 7 s no ensaio, com 2 s de dimensionamento já incluídos em cada total. Os intervalos até a primeira confirmação observada foram 19,836 s e 24,495 s. Estes últimos incluem latência de observação; nenhum desses valores mede o fluxo completo ou sustenta uma comparação de produtividade CAD/BIM. Não houve réplica BIM deste ensaio unilateral.

A tabela da LE3 manteve Mdx = 5,46 kN.m/m, Mdy = 1,91 kN.m/m, Ndx = 87,97 kN, Rdx = -1,71 kN e flecha máxima exibida de -0,05 cm. Trata-se do resumo exibido, sem identificação da combinação ou do nó governante; não constitui verificação integral de ELS.

Permanece necessário examinar a distribuição dos esforços nos bordos e o detalhamento físico da ligação. Não se elevou limite para desconsiderar tração ou momento; a dispensa de verificação de cisalhamento herdada continua pendente de revisão. Não houve exportação atualizada IFC/SAP, aprovação estrutural ou conclusão da comparação dos fluxos.

`consolidar_encontro.py` verifica os hashes dos controles R182 e da fonte R191, o CRC dos PRJ, as leituras de largura, as cinco mensagens A11 e os relatórios nativos. Os PRJ ficam apenas em D:/TCC; o manifesto relaciona a evidência arquivada neste diretório.

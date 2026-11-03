# H03/R189 — sensibilidade da largura da barra inferior de LE3

Ensaio preliminar, não executar. Criou-se uma cópia independente do receptor CAD R188 em `D:/TCC/outputs/R189-CAD-SENSIBILIDADE-APOIO-LE3-NAO-EXECUTAR`. Preservaram-se o PRJ fonte R188 CAD e os dois controles R182, conferidos por SHA-256. O projeto escrito e os modelos principais não foram alterados.

## Intervenção efetivamente realizada

Na barra ordinária horizontal do bordo inferior de LE3, no croqui N0, alterou-se apenas o campo **Largura**, de 0 para **20 cm**. A leitura do diálogo reaberto confirmou 20 cm antes e depois do processamento. As cargas de parede e extra permaneceram em zero. O critério de ancoragem por gancho foi herdado da fonte R188; não se elevaram limites de dispensa para suprimir A11.

Os 20 cm constituem uma hipótese de diagnóstico. Não se definiu uma peça física de apoio, não se dimensionou fundação e não se verificou a capacidade ou o detalhamento da ligação inferior. Não se adicionou pilar físico. O teste não deve ser incorporado automaticamente aos modelos de entrega.

## Cálculo e resultado

Mantiveram-se vigas, pilares e lajes de N1/N2 e escadas de N1 selecionados para dimensionamento, com N0 e fundações excluídos. Mantiveram-se deslocamentos do pórtico com rigidez configurada; flechas de lajes, dinâmica, etapas construtivas e verificação dos limites de redistribuição semirrígida permaneceram desativadas. Não se concluiu a verificação de todos os estados-limite.

Após o processamento com avisos, LE1 e LE2 conservaram o status “calculado” na planilha Positivo. **LE3 permaneceu com D31**, com **A11 — largura do apoio insuficiente** para 6,3; 8; 10; 12,5 e 16 mm. Portanto, a alteração isolada dessa barra para 20 cm **não resolveu o erro**. Não se identificou, por esse ensaio, qual bordo governa a ancoragem.

A leitura complementar de LE3 registrou espessura de 14 cm, tipo fundo plano, piso de 28 cm e espelho exibido de 17,82 cm. A planilha Esforços exibiu Mdx = 5,46 kN·m/m, Mdy = 1,91 kN·m/m, Ndx = 87,97 kN e Rdx = −1,71 kN. Esses valores foram transcritos visualmente; ainda não se verificou o mapeamento do eixo local X para os eixos globais. A flecha exibida de −0,05 cm não foi tratada como verificação completa de ELS das lajes.

O relatório manteve N1 com 16 vigas, 11 pilares e 9 lajes com sucesso e N2 com 15 vigas, 11 pilares e 5 lajes com sucesso. Esse resumo não comprova o dimensionamento da escada; a leitura individual de LE3 prevalece para registrar sua pendência.

## Tempos e validade da comparação

O relatório nativo registrou **8 s de processamento total**, dos quais **2 s de dimensionamento**, já incluídos no total. O intervalo entre o comando e o registro de confirmação após a leitura da captura foi de **19,699 s**. Esse intervalo inclui latência de ferramentas, observação e confirmação; não corresponde a tempo ativo nem à duração completa do fluxo.

Executou-se uma observação CAD, sem réplica BIM nesta revisão. Não se utilizou esse ensaio unilateral para classificar produtividade ou qualidade relativa dos fluxos. Não se produziram novos IFC/SAP: arquivos herdados da cópia não constituem exportação R189 nem auditoria completa de retenção de geometria e cargas.

## Continuidade

Deve-se conferir os demais bordos de LE3, seus vínculos, eixos locais, esforços de tração e espaço físico de ancoragem, preservando a hipótese de apoio idealizado da superestrutura. A conclusão exige solução de ligação coerente com a geometria, revisão de armaduras e verificações pendentes; o simples desaparecimento de uma mensagem não constitui aprovação estrutural. O ensaio e suas limitações estão em `R189-sensibilidade-barra.json`, com relatório nativo, capturas, leituras acessíveis e manifesto de hashes.

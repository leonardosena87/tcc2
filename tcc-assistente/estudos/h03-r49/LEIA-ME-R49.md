# H03/R49 — lajes CAD, auditoria inicial

28/10/2026 em Brasília. **ESTUDO NÃO DIMENSIONADO — NÃO EXECUTAR.** Monografia inalterada.

Em cópia independente da R48, lançaram-se cinco lajes internas em N1, cinco em N2 e a varanda de N1. Todas maciças de 14 cm, elevação zero. Os campos de cargas ficaram sem preenchimento e representam pendências. Não se copiou o receptor BIM para completar o CAD.

O contorno da varanda utiliza três barras de largura zero, entre (975;380), (1072,5;380), (1072,5;710) e (975;710) cm, fechando nas faces dos pilares e da viga. Confirmaram-se os avisos de nós livres nos cantos externos. A entrada por colagem deixou de funcionar após aviso; completou-se a coordenada com teclas individuais. O canto externo superior foi capturado no contorno CAD existente; a exportação confirmou sua posição exata. Essas recuperações são operações de interface, não defeitos de transferência do DWG.

A primeira exportação IFC4 contém 22 trechos de pilares, 32 sólidos para 29 vigas lógicas e 11 lajes. As verificações geométricas de pilares/vigas da R48 continuaram aprovadas. Nas lajes, conferiram-se caixas envolventes, cotas, espessuras e área superior triangulada. Dez lajes internas correspondem às faces internas das vigas de 20 cm. A varanda parte de x=9,75 m, face externa da viga; conserva as bordas livres em x=10,725 m, y=3,80/7,10 m, com área líquida de 3,2175 m². A área bruta da proposta por eixos, 3,5475 m², não deve ser usada como área líquida desta laje exportada. A diferença representa desconto da face de apoio, explicitado para ambos os ramos.

Três controles sintéticos detectaram remoção, duplicação e mudança de 1 cm na espessura de uma laje, sem modificar o IFC real. Tolerância computacional de 0,00001 m; não é tolerância normativa. Essa auditoria não comprova conectividade, engastamento da varanda, malha, cargas, armaduras ou ELU/ELS. Não houve cálculo estrutural da H03.

Intervalo monotônico prospectivo de 00:16:58,242 a 00:41:01,966 UTC de 29/10/2026: **24 min 03,725 s brutos**. Inclui interrupções de turnos sem pausa instrumentada, pesquisa auxiliar, recuperação da interface, latências e auditoria. O tempo ativo e a duração das interrupções não estão disponíveis; o intervalo não será tratado como produtividade comparável nem como tempo total do fluxo.

O projeto foi salvo e a cópia desta etapa foi congelada. A conferência após fechar/reabrir ainda está pendente. O ramo BIM permanece na R46, sem lajes nativas; exige complementação própria com cronômetro. Antes do processamento, devem-se harmonizar materiais, cobrimentos, cargas, apoios idealizados e vínculos dos dois receptores. A varanda depende de verificação específica de continuidade/engastamento e capacidade. As instruções operacionais consultadas estão no [suporte oficial AltoQi sobre lajes de beiral](https://suporte.altoqi.com.br/hc/pt-br/articles/115003725214); o uso dessas ferramentas não substitui a análise estrutural.

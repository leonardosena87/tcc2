# H03/R143 — ensaio W05 pelo cadastro nativo de parede

Estudo exploratório parcial, NÃO EXECUTAR. A R116 permanece a referência parcial; este ensaio não foi incorporado a ela.

Criaram-se cópias independentes 68/CAD e 69/BIM das bases R116. Preservaram-se os 35 arquivos-fonte por SHA-256. A cópia BIM não foi aberta, carregada ou processada; seus arquivos permanecem iguais à preparação, exceto o ponteiro de projeto próprio no INI. Não existe par CAD/BIM medido nesta etapa.

## Operação e resultado

No croqui N1/CAD, ampliou-se a região da W05/V8. A tentativa de inserir nó em (965;15) cm foi recusada com a mensagem “Já existe um nó nesta posição no pavimento”. O botão de captura foi alternado uma vez; não se comprovou seu estado por simples alternância nem se identificou a causa da recusa. Não se confirmou nó novo. Não repetir indefinidamente esse procedimento.

Ensaiou-se então o recurso próprio Carga de parede, documentado pela AltoQi: https://suporte.altoqi.com.br/hc/pt-br/articles/360058309854 . A documentação para carga parcial exige nós delimitadores: https://suporte.altoqi.com.br/hc/pt-br/articles/360046158854 . A consulta não forneceu solução comprovada para a recusa junto ao pilar nesta versão/modelo.

A hipótese W05 usa altura 285 cm e espessura acabada 15 cm. A composição de estudo pesa 1,565 kN/m²; seu peso volumétrico equivalente é 1,565/0,15 = 10,433333… kN/m³. Não é peso certificado de um bloco ou produto. Digitou-se 10,433333333; após salvar, fechar e reabrir, o cadastro mostrou 10,4333 e carga 4,46 kN/m. A seção V8 permaneceu 20 × 40 cm, elevação zero e carga extra zero.

A exportação textual nativa mostrou −4,4602 kgf/cm em LOCAL/2, além das duas casas exibidas em kN/m. Essa relação é compatível com a convenção observada na R125; não constitui conversão SI exata ou prova de precisão interna ilimitada. Não se alterou q para forçar a resultante.

| Grandeza | Resultado |
|---|---:|
| Faixa física prevista W05, Y | 15 a 375 cm |
| Faixa distribuída exportada, Y | 3 a 387 cm |
| Comprimento físico livre | 360 cm |
| Comprimento carregado na barra exportada | 384 cm |
| Excesso geométrico em cada extremidade | 12 cm |
| Integral assinada da linha no eixo LOCAL/2 | −1.712,71680 kgf |

A integral acima é a parcela distribuída, não a ação G2 global, reação de apoio ou aprovação do modelo. Não se inferiu o sinal global apenas do nome LOCAL/2.

O controle textual R132/CAD-BASE deriva da R116. Os nós e extremos ordenados coincidem nos três modelos. N1 acrescentou nove registros distribuídos G2; N2 não mudou em nenhuma tabela. No pórtico acrescentou-se um registro distribuído e mudaram 130 registros pontuais e três nodais G2 em cada conjunto removido/adicionado. São registros de tabelas, não 130 defeitos, correções ou cliques. As nove barras da nova linha em N1 formam a faixa Y3→387 cm. Não se confundiu a carga nova com os demais registros G2 preexistentes. Não houve execução no SAP2000 nem balanço completo de reações/momentos.

Processaram-se análise estática linear e deslocamentos do pórtico com rigidez configurada. O programa terminou com avisos; ficaram fora dimensionamento, flechas das lajes, rigidez fissurada e dinâmica. A releitura manteve o SHA-256 do PRJ salvo; a cópia CAD fechada foi congelada e verificada. A integridade ZIP não atesta segurança estrutural.

## Tempo e limites

O intervalo CAD, de início persistido a fechamento após releitura, durou 16.747417 min (1004.845 s). Inclui tentativa recusada, exploração, pesquisa, operação, latência, processamento, exportação e conferência. O intervalo comando→observação de término está contido nele e não deve ser somado. O protocolo real desta sessão não foi igual ao de outro ramo: não há ranking, total final do fluxo ou percentual de economia. Não houve intervenção humana durante o ensaio. Inferência isolada, tempo ativo humano, tokens e custo da IA não foram medidos.

## Encaminhamento

A parede nativa preservou parâmetros e uma intensidade exportada com quatro casas, mas não resolveu a delimitação física pretendida. O lançamento permanece experimental. Não replicar a mesma faixa inadequada em outras paredes nem no BIM apenas para produzir igualdade. Avançar nas frentes independentes, mantendo cargas, compatibilização e ELU/ELS completo em aberto. A monografia e os arquivos de autoria Revit/AutoCAD não foram editados.

Prazo informado pelo usuário: **10/11/2026, 19h, horário de Brasília**. Consultar o planejamento de fechamento na mesma pasta; datas são metas, não etapas concluídas ou garantia de aprovação.

## Ambiente conferido após o ensaio

A janela Ajuda → Sobre confirmou atualização **2025-04 [v. 18.306]**, aplicação Infinity. A consulta foi posterior ao fim do intervalo CAD e está registrada separadamente. Não houve atualização do programa. Não se atribuem a esta instalação os recursos de 2026-05/2026-08 nem conformidade automática com a Emenda 1:2026 da NBR 6118. A identificação da versão e a verificação normativa são itens distintos.

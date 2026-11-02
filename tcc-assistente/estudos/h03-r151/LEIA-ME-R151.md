# H03/R151 — outra configuração de escada, preservando paredes e portas

## Decisão incorporada

O usuário determinou: **“Preservar as paredes e portas; estudar outra configuração de escada”**. A ampliação interna de aproximadamente 55 cm desenhada na R149 fica descartada para aplicação. A R149 permanece como histórico de alternativa rejeitada. Mantêm-se os pisos acabados +0,22 e +3,25 m, a fachada e o limite norte da chegada. Nenhum arquivo arquitetônico ou estrutural nativo foi editado.

## Hipótese geométrica calculada

Estudou-se uma escada em U, com contornos internos e externos curvos, compensando a mudança de direção ao longo de 11 pisadas. Trata-se de uma configuração nova, com **18 espelhos e 17 intervalos de pisada**, distribuídos em **3 retos + 11 compensados + 3 retos**. O piso superior encerra o último espelho. Não se soma um degrau de chegada fictício nem se transforma a proposta em dois lances de nove espelhos com patamar.

O espelho acabado permanece em 16,833 cm. A largura entre os contornos é a faixa gráfica da planta, aproximadamente 91 cm, ainda sem desconto de guardas e corrimãos. Adotou-se uma linha de percurso a 50 cm do contorno interno, como parâmetro de estudo. A extensão reta da transição é 77 cm em cada lado; a linha curva resulta em pisadas de aproximadamente 30,88 cm, com 2e+p aproximadamente 64,55 cm. Os valores exatos constam do JSON.

O método define cinco intervalos de 15,4 cm em cada lado reto do bordo interno e um intervalo central atravessando a meia-volta. As linhas de espelho ligam os pontos internos às divisões iguais da linha de percurso e seguem até o contorno externo. As cordas internas e as estações externas são verificadas. Não se trata de dividir a curva em setores radiais iguais, o que produziria pontas muito estreitas junto ao pequeno vão central.

A envoltória resultante cabe geometricamente no retângulo gráfico reservado à escada, mantendo a chegada. O esquema próprio está em **R151-compensada.png**. A reserva ao sul é espaço remanescente do retângulo, não uma folga estrutural ou um patamar. As paredes e portas não foram redesenhadas, mas a compatibilidade funcional com abertura de folhas, guarda e circulação ainda exige sobreposição e corte. As cordas da linha de percurso variam em relação ao comprimento curvo; o critério correto de medição deve ser confirmado antes de adotar o traçado.

## Limites e base consultada

Esta revisão demonstra **uma possibilidade de encaixe**, não a aprovação arquitetônica, normativa ou estrutural. Os parâmetros de 50 cm de percurso e 15 cm de corda interna são hipóteses de triagem, sem declaração de mínimo legal aplicável à escada privada. O anexo municipal disponibilizado pela [Prefeitura de Vitória da Conquista](https://www.pmvc.ba.gov.br/wp-content/uploads/Lei_1481-2007_Anexos.pdf), já arquivado na R149, distingue o uso coletivo do acesso entre pisos da mesma unidade; isso não dispensa a verificação completa da legislação e das normas aplicáveis. A [página oficial de normas do CBMBA](https://www.ba.gov.br/bombeiros/normas-tecnicas) foi consultada, mas a resposta disponível não forneceu o texto da instrução específica. Não se importaram automaticamente critérios de outro estado.

O [exemplo oficial AltoQi de escada em U com leque](https://suporte.altoqi.com.br/hc/pt-br/articles/115001824894) confirma a existência de um procedimento de modelagem com níveis intermediários e cargas de enchimento. Ele não valida esta geometria e suas dimensões não foram copiadas. Antes de lançar a nova configuração, é necessário definir a solução resistente, os níveis estruturais, as ligações, os apoios e o peso real de lajes/degraus. O modelo de acabamento não é automaticamente o modelo analítico.

**Pendências para aceitação:** corte longitudinal e transversal com altura livre; largura útil após guardas/corrimãos; compatibilidade com portas, janela J4 e laje do hall; necessidade e admissibilidade de patamar; critério de medição e uniformidade das pisadas; enquadramento normativo; geometria e capacidade dos apoios; espessuras e cargas. Não se reaproveita o patamar acabado +1,735 m da R149: nesta hipótese ele não existe. Nenhuma carga de escada foi adicionada aos ensaios comparativos.

## Rastreabilidade e comparação

O cálculo usa dimensões gráficas extraídas na R147, não levantamento físico. O JSON registra a fonte e seu SHA-256, a decisão atual, os pontos dos espelhos, os comprimentos e os limites. Os testes verificam a contagem de espelhos/pisadas, a preservação das cotas, a ordenação dos segmentos, as cordas internas e a reserva gráfica. Esses testes não comprovam segurança nem acessibilidade.

O arquivo de tempo mede somente a execução do script. Não mede pesquisa, autoria, raciocínio, inferência, operações nos programas ou tempo final dos fluxos. Uma configuração aceita deverá ser aplicada de maneira equivalente ao Revit e ao CAD antes da nova transferência para o Eberick; não se atribuirá a um formato uma correção geométrica feita apenas no outro.

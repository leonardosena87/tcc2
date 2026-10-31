# H03/R92 — primeira leitura nativa de materiais

Executou-se o auditor R91 dentro do Revit 2027.2, depois de o usuário autorizar o carregamento na interface. Abriu-se uma cópia byte a byte da autoria R83. Associaram-se os 62 candidatos aos 62 IDs e UniqueIds do mapa de criação, sem candidatos extras. O documento estava salvo e permaneceu sem modificações durante a leitura. Os hashes do RVT original e da cópia continuaram iguais ao início.

| Elementos associados | Quantidade | Compressão do ativo (MPa) | Módulo de Young (MPa) | Densidade (kg/m³) | Poisson |
|---|---:|---:|---:|---:|---:|
| Trechos de pilares e vigas | 51 | 24,13293801 | 23.250 | 2.407,31172 | 0,167 |
| Lajes | 11 | 10 | 20.500 | 2.406,4537 | 0,20 |

A premissa documental é C25. O modelo de origem apresenta valores distintos no cadastro físico; a existência de geometria e categorias corretas não comprova alinhamento dos materiais. O material das lajes se chama “Concreto, Moldado in loco”, com ativo “Concreto 10 MPa”; vigas/pilares usam “Concreto, Moldado in loco, cinza”, com ativo “Concreto(1)”. Os valores foram lidos das propriedades, não inferidos dos nomes.

Esse achado não é prova de perda durante IFC/DWG nem explica retroativamente o cadastro recebido no Eberick R45/R46. A resistência de compressão e o módulo do ativo são propriedades da API: sua interpretação como fck/Eci/Ecs precisa ser explicitada. Não se verificaram armaduras CA-50, cobrimentos, vínculos ou ELU/ELS. A leitura não alterou materiais ou dimensionou a estrutura.

O comando mediu **69,868 ms** para a leitura interna. Esse intervalo exclui abertura, navegação, espera por autorização, serialização do JSON e análise posterior. Não é tempo total BIM nem inferência de IA. A chamada foi local, com zero transações e zero chamadas de inferência.

O próximo passo é alinhar os materiais em uma nova revisão, preservar esta evidência, salvar/reabrir/reler e verificar as propriedades no IFC e no receptor. A frente P08 permanece parcial. O texto acadêmico foi preservado.

Validação: execução nativa do comando, associador R91 executado sobre os dados reais, conferência de identidades e hashes. Não houve mudança de código nem necessidade de repetir os testes simulados já aprovados.

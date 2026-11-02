# H03/R141 — adendo de tempos R125–R140

Foram consolidados **45 registros** de arquivos já arquivados, sem alterar os modelos ou a monografia. Há 45 intervalos com duração utilizável neste recorte, dos quais 4 derivados de limites UTC. Os 12 intervalos comando→observação estão contidos nas respectivas sessões e não devem ser adicionados novamente. Identificaram-se 12 pares com limites sobrepostos; isso não prova execução paralela.

O inventário R124 permanece uma fotografia histórica separada (203 candidatos naquele recorte). Este adendo não atualiza todo o universo do R124, não soma seus registros e não transforma contagens de arquivos em horas completas do projeto. Os arquivos de início, os resultados consolidados e as cópias locais de evidências não são contados novamente.

| Revisão | Ramo | Registro | Segundos | Origem | Relação temporal |
|---|---|---|---:|---|---|
| R125 | BIM | BIM-retomada-tempo.json | 151.343 | registrado | — |
| R126 | CAD | CAD-tentativa-tempo.json | 747.789 | registrado | — |
| R127 | BIM | BIM-consulta-tempo.json | 133.586 | registrado | — |
| R127 | CAD | CAD-consulta-tempo.json | 147.423 | registrado | — |
| R129 | CAD | CAD-tempo-sessao.json | 574.859 | registrado | — |
| R130 | BIM | BIM-tempo-sessao.json | 524.474 | registrado | — |
| R130 | CAD | CAD-tempo-sessao.json | 528.754 | registrado | — |
| R131 | BIM | BIM-processamento-tempo.json | 41.809 | registrado | contido na sessão |
| R131 | BIM | BIM-sessao-tempo.json | 247.264 | registrado | — |
| R131 | CAD | CAD-processamento-tempo.json | 40.673 | registrado | contido na sessão |
| R131 | CAD | CAD-sessao-tempo.json | 211.857 | registrado | — |
| R132 | BIM | BIM-BASE-sessao-tempo.json | 295.859 | registrado | — |
| R132 | BIM | BIM-W15-sessao-tempo.json | 326.232 | registrado | — |
| R132 | CAD | CAD-BASE-sessao-tempo.json | 239.762 | registrado | — |
| R132 | CAD | CAD-W15-sessao-tempo.json | 234.844 | registrado | — |
| R133 | BIM | BIM-processamento-tempo.json | 41.424 | registrado | contido na sessão |
| R133 | BIM | BIM-sessao-tempo.json | 644.102 | registrado | — |
| R133 | CAD | CAD-processamento-tempo.json | 35.293 | registrado | contido na sessão |
| R133 | CAD | CAD-sessao-tempo.json | 865.387 | registrado | — |
| R133 | compartilhado/não atribuído | recuperacao-texto-tempo.json | 82.967 | registrado | — |
| R134 | BIM | BIM-processamento-tempo.json | 40.196 | registrado | contido na sessão |
| R134 | BIM | BIM-sessao-tempo.json | 923.820 | registrado | — |
| R134 | CAD | CAD-processamento-tempo.json | 48.329 | registrado | contido na sessão |
| R134 | CAD | CAD-sessao-tempo.json | 853.623 | registrado | — |
| R135 | BIM | BIM-tempo-sessao.json | 492.347 | registrado | — |
| R135 | CAD | CAD-tempo-sessao.json | 394.488 | registrado | — |
| R135 | compartilhado/não atribuído | recuperacao-capturas-tempo.json | 335.190 | registrado | — |
| R136 | BIM | BIM-processamento-tempo.json | 63.897 | registrado | contido na sessão |
| R136 | BIM | BIM-sessao-tempo.json | 480.946 | registrado | — |
| R136 | CAD | CAD-processamento-tempo.json | 50.966 | registrado | contido na sessão |
| R136 | CAD | CAD-sessao-tempo.json | 436.790 | registrado | — |
| R137 | BIM | BIM-processamento-tempo.json | 32.589 | registrado | contido na sessão |
| R137 | BIM | BIM-sessao-tempo.json | 517.219 | registrado | — |
| R137 | CAD | CAD-processamento-tempo.json | 25.757 | registrado | contido na sessão |
| R137 | CAD | CAD-sessao-tempo.json | 1310.487 | registrado | — |
| R138 | BIM | BIM-processamento-tempo.json | 24.843 | registrado | contido na sessão |
| R138 | BIM | BIM-sessao-tempo.json | 514.192 | registrado | — |
| R138 | CAD | CAD-processamento-tempo.json | 21.852 | registrado | contido na sessão |
| R138 | CAD | CAD-sessao-tempo.json | 442.616 | registrado | — |
| R139 | BIM | BIM-sessao-tempo.json | 211.766 | registrado | — |
| R139 | CAD | CAD-sessao-tempo.json | 294.200 | registrado | — |
| R140 | BIM | BIM-consulta-fim.json | 146.821 | UTC derivado | — |
| R140 | BIM | BIM-controle-consulta-fim.json | 241.359 | UTC derivado | — |
| R140 | CAD | CAD-consulta-fim.json | 722.069 | UTC derivado | — |
| R140 | CAD | CAD-controle-consulta-fim.json | 152.064 | UTC derivado | — |

## Uso nos resultados

As sessões são exploratórias e preservam tentativas descartadas, recuperação de capturas e consulta de controles. A R137 CAD inclui descoberta/retomada da seleção; a R140 CAD inclui descoberta do caminho de consulta, enquanto as seguintes usam o caminho aprendido. A R135 tem recuperação conjunta de capturas e a R133 tem consulta adicional, ambas sem rateio arbitrário entre CAD e BIM. O estado de cada ensaio deve ser lido em seu relatório técnico.

A duração explícita e a diferença dos limites UTC estão preservadas em campos distintos no JSON. Nenhuma duração ausente vira zero. Os quatro intervalos R140 são derivados de UTC, sem precisão monotônica declarada. As diferenças entre relógios não foram ocultadas.

**Não há tempo final comparável CAD/BIM, ranking ou economia percentual.** Também não há inferência isolada da IA, tempo ativo humano, tokens ou custo medidos para a edificação principal. O banco central e as demonstrações da palestra não foram alterados nem incorporados a este adendo.

## Procedimento para o ensaio final

Congelar primeiro uma proposta comum tecnicamente revisada e os arquivos de partida de cada ramo. Usar o mesmo conjunto de elementos, ações e entregáveis como critério de término. Registrar geração/autoria, intercâmbio, conferência, complementos no Eberick, correções, reprocessamento e documentação em intervalos identificados por ramo/etapa, mantendo a preparação comum separada.

Iniciar cada intervalo antes do comando da etapa e encerrá-lo após o critério de término observado. Pausas fora da tarefa exigem parada e novo intervalo na retomada. Falha/retrabalho dentro da tarefa permanece registrado com sua ocorrência e resultado; não se retira tempo para favorecer um ramo. Medidas internas de API/solver são subconjuntos: registrar seus limites e não adicioná-las ao intervalo que as contém. Tempo de raciocínio e operação da IA dentro da sessão não equivale a tempo isolado de inferência.

O cronômetro existente distingue trabalho manual e processamento automático; o registro de evidências deve esclarecer se houve operação pela IA ou pelo usuário, pois a categoria manual do instrumento não comprova autoria humana. Como o instrumento existente também exige um cenário de alteração arquitetônica para permitir comparação final, definir e executar a mesma alteração nos dois ramos ou revisar formalmente esse protocolo antes de usar sua saída como resultado final. Não marcar cenários inexistentes como concluídos.

Alternar a ordem CAD/BIM em repetições, conservar os mesmos critérios de inspeção e arquivar início/fim, proposta, versões, arquivos e ocorrências. Medir tempo junto com retenção de informação, complementos e compatibilização. Um resultado rápido sem o mesmo estado final aceito permanece parcial.

Os números desta tabela são observações históricas, não previsão de duração futura. A consolidação de dados e a redação deste adendo não estão incluídas nos intervalos da tabela.

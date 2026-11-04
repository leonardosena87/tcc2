# H03/R216 — Reabertura e consolidação das medições

Criou-se uma cópia completa do BIM R215 em D:/TCC/outputs/H03-R216-CONSOLIDACAO-NAO-EXECUTAR/BIM. A cópia abriu no Eberick sem pedir recuperação. A consulta da planilha de uniformização confirmou a retenção das armaduras de P3 e P4: As efetivo 4,71 cm² nos três lances, com registro anterior 3,14 cm² nos dois inferiores. Não se recalculou nem se alterou a concepção nesta revisão. O hash do PRJ permaneceu igual ao da R215 após essas consultas. Essa reabertura funcional complementa a verificação de integridade do contêiner feita após a falha anterior; não constitui validação estrutural.

O inventário foi atualizado com 307 arquivos diretos: 209 com duração reconhecida, 79 sem duração principal reconhecida e 19 contêineres não expandidos. Identificaram-se 31 pares de intervalos sobrepostos. Esses números representam arquivos e relações entre registros, não 307 ensaios, 209 atividades independentes ou uma duração total. O escopo da varredura é limitado a arquivos JSON com tempo no nome diretamente nas pastas filhas de outputs e quatro registros técnicos legados. Relatórios nativos e tempos inseridos em texto exigem leitura específica. Um campo de interrupção falso indica ausência de anotação reconhecida, não comprova trabalho contínuo.

Corrigiu-se o leitor para reconhecer wallSeconds e intervalo_observado_s, converter apenas sua unidade para milissegundos e conservar os valores originais. Acrescentou-se o reconhecimento dos limites inicio/fim com fuso declarado. Listas JSON são classificadas como contêineres, sem somar seus itens. O processamento real identificou esse formato em um resumo de cenários; antes, o inventário interrompia nesse arquivo. Oito testes passaram, incluindo ausência de tempo, unidade, limites UTC, sobreposição, contêineres e durações negativas.

## Medições disponíveis para discussão

| Cenário | CAD: cálculo nativo | BIM: cálculo nativo | Limite de interpretação |
|---|---:|---:|---|
| R196: W08 integral | 7 s | 7 s | Uma execução por fluxo; configuração histórica |
| R201: ELS fissurado, dimensionamento selecionado herdado | 9 s | 9 s | Escopo distinto do dimensionamento integral |
| R205: ELS fissurado, dimensionamento integral | 10 s | 10 s | Uma execução por fluxo |
| R207: W08 corrigida | 10 s | 11 s | BIM ainda apresentava D16; estados finais diferentes |
| R210 BIM / R211 CAD: revisão de concepção | 9 s | 9 s | Revisões distintas, agrupamento de vigas diferente |
| R215: controle após recuperação | Não registrado nesta revisão | 10 s | Controle BIM; 3 s de dimensionamento já incluídos nos 10 s |

Fontes: h03-r206/tempos-recentes-por-cenario.json; h03-r207/README.md; h03-r210/R210-final-mensagens.txt; h03-r211/R211-resultado.json; h03-r215/BIM-R215-mensagens.txt. O cálculo integral inclui elementos de fundação fora do escopo de dimensionamento do TCC. Os tempos nativos não medem autoria, transferência, retrabalho, ação humana ou inferência da IA. Não se somam os tempos de dimensionamento aos totais que já os contêm.

| Intervalo observado | Duração | Conteúdo e limite |
|---|---:|---|
| R207 BIM | 250,900 s (4 min 10,900 s) | Edição da W08; inclui navegação, captura e raciocínio; CAD sem início pareado |
| R211 CAD | 1.241,641 s (20 min 41,641 s) | Cópia aberta até salvamento, incluindo correções e dois cálculos |
| R213 CAD | 399,739 s (6 min 39,739 s) | Seleção/unificação de vigas, conferência, exportação e salvamento; exclui abertura e recuperação iniciais |

Não há par CAD/BIM completo com o mesmo início, tarefa e critério de aceitação nesses intervalos. O tempo total comparável, os tokens, o custo e o tempo exclusivo de inferência da IA no experimento principal permanecem desconhecidos. Os dados das demonstrações da palestra ficam separados. Não se calcula percentual de economia a partir destes recortes.

## Pendências para encerramento

| Ordem | Pendência | Evidência atual | Critério para fechar |
|---|---|---|---|
| 1 | V1 do N0, apoio inferior da escada | Aviso19; R215 registra esforços globais de SAE1A/SAE1B por combinação | Obter N e momentos locais simultâneos na seção crítica da viga e verificar resistência/detalhamento. Esforços da base não substituem os da seção |
| 2 | Viga de cobertura CAD V13_1 / BIM V3 | Aviso08; detalhes e carregamentos conferidos na R212 | Verificar inversão de esforços, ancoragens e transferência aos apoios |
| 3 | Rigidez da grelha N1 | R214: I33 20.000 cm⁴ CAD e 18.540 cm⁴ BIM em três segmentos R30x20 | Explicar ou controlar a diferença e sua influência; não editar o arquivo de exportação para forçar igualdade |
| 4 | Compatibilização P6/P11, P12 e W08 | Folga nominal da porta junto a P6 menor que a incerteza da referência; apoio de W08 inferior pendente | Conferir arquitetura, portas, espessuras, apoios e distribuição de cargas; registrar solução comum |
| 5 | Autoria Revit/AutoCAD | Cópias preservadas na R207 são de revisões anteriores à concepção atual | Atualizar ambos com a mesma solução compatibilizada e auditar novas saídas |
| 6 | Comparação de correções e produtividade | Auditorias geométricas existentes; tempos parciais heterogêneos | Congelar entradas e critérios comuns; registrar operações, ocorrências, tempos e interrupções de ensaios pareados |
| 7 | Resultados e entrega | Evidências parciais rastreáveis; ausência de conclusão comparativa final | Incorporar resultados verificados e limitações no texto, revisar e empacotar arquivos finais |

As 14 sapatas com erro permanecem fora do dimensionamento autorizado, por ausência de sondagem. Isso não dispensa conferir as condições idealizadas da base e suas reações. O diagnóstico BIM R215 registra N1 com 12 vigas, 12 pilares, 6 lajes e 3 elementos de escada com sucesso, sem avisos nesses grupos; esse estado não elimina as pendências da tabela. Não há liberação para execução.

## Consulta da V1 no pórtico

Conseguiu-se ampliar a viga no pórtico e selecionar a região colorida do primeiro segmento do diagrama ELU de fletores. Para a combinação exibida 1.4G1+1.4G2+0.7Q+0.84V1+0.84D1+1.4QT, o painel Valores identificou V1 (N0) e mostrou −1,78 e +0,14 kN.m. A captura foi preservada. Esses dois valores de um segmento não são a envoltória da viga nem um conjunto completo de esforços simultâneos. A consulta dos axiais identificou a V1, mas não exibiu números no painel; não se registrou zero por ausência de leitura. A componente horizontal permanece sem verificação nesta revisão.

Procedimentos: [AltoQi — leitura dos diagramas](https://suporte.altoqi.com.br/hc/pt-br/articles/360038283234) e [AltoQi — Aviso19](https://suporte.altoqi.com.br/hc/pt-br/articles/360009988354). A documentação distingue a flexão horizontal não abrangida pelo dimensionamento automático; não se dispensou o aviso pela consulta gráfica.

Reprodução do inventário: `node tcc-assistente/estudos/h03-r216/inventariar.mjs D:/TCC <nova-pasta>`. Validação: `node --test tcc-assistente/tests/timing-inventory.test.mjs`. O relatório não altera o documento acadêmico nem transforma uma revisão exploratória em ensaio final.

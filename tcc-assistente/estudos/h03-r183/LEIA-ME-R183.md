# H03/R183 — leitura dos apoios e dos critérios de dimensionamento

Estudo preliminar, não executar. Consultaram-se os dois receptores R182 no Eberick 2025 Infinity, preservando os arquivos PRJ por SHA-256. Cancelaram-se os diálogos de configuração; recusou-se a gravação das alterações de sessão ao trocar de projeto. Não se processou a estrutura nem se criou elemento nesta revisão.

## Leitura efetiva

| Campo observado | CAD | BIM |
|---|---:|---:|
| Barra horizontal de N0 entre AE1A e AE1B, extremidade inferior de LE3 — largura | 0 cm | 0 cm |
| Detalhamento de lajes — ancoragem | reta | reta |
| Momento positivo mínimo considerado na ancoragem | 100 kgf·m | 100 kgf·m |
| Tração mínima considerada na ancoragem | 100 kgf/m | 100 kgf/m |
| Permitir ancoragem na laje adjacente | desmarcado | desmarcado |
| Dispensar verificação ao cisalhamento de lajes | marcado | marcado |
| Taxa máxima de armadura de vigas | 2% | 2% |

As leituras são transcrições manuais das capturas nativas anexas. O campo de largura da barra também consta nos arquivos AX. A correspondência se restringe aos campos desta tabela, sem afirmar igualdade de todas as configurações dos projetos.

No CAD, a consulta específica Detalhamento → Lajes → Escadas mostrou as quatro opções de criar esperas em apoios superior/inferior com viga/laje desmarcadas. Não se releram essas quatro opções específicas no BIM nesta revisão.

## Interpretação e limitações

A largura nula é um dado do cadastro, não uma demonstração isolada de lançamento inválido: uma barra pode delimitar o contorno sem representar uma viga física. O manual de lançamento da AltoQi admite barras de contorno e distingue o eixo do elemento de apoio. Os marcadores AE1A/AE1B e a condição de vínculo idealizado não comprovam a existência de uma peça de concreto disponível para ancoragem em toda a borda inferior.

O diagnóstico R182 permanece: LE3 com D31/A11 nos dois fluxos, e V2 de N1 no BIM com D16/A07 no nó 2. A R183 não identifica qual extremidade gerou a verificação crítica de A11, nem prova que mudar a largura da barra resolveria a ancoragem. O limite de 2% é um parâmetro cadastrado do programa, não uma conclusão sobre o limite normativo aplicável ao caso. Não se alterou esse valor.

A opção de dispensar cisalhamento estava marcada em ambos. Sua presença deve ser revista antes de concluir o dimensionamento. A obtenção de armaduras de flexão em LE1/LE2 não encerra a verificação da escada. Os limites de momento e tração não foram elevados para eliminar erros; tampouco se habilitou ancoragem em laje adjacente sem comprovação do concreto disponível.

A documentação oficial descreve a alternativa de ancoragem com gancho e a verificação da espessura para acomodá-lo. Um ensaio isolado dessa opção pode ajudar a diagnosticar A11, mantendo geometria, apoios, limites e bitolas; seu resultado não será aprovação física do apoio idealizado. A eventual alteração de configuração possui abrangência geral nas lajes, o que deverá ser explicitado no escopo do ensaio e das recalculações.

## Tempos e continuidade

Não houve novo processamento nesta revisão; o tempo nativo é ausente, não zero medido. O intervalo entre início e conclusão da auditoria inclui interrupções, ferramentas e leitura e não representa tempo ativo de correção de nenhum dos fluxos. Mantêm-se separados os tempos R182 de 7 s por receptor e os 2 s internos de dimensionamento já contidos nesse total.

Permanecem pendentes o ensaio causal de ancoragem, a justificativa física do apoio inferior, cisalhamento/ELS, a reconciliação das vigas contínuas, o conflito V16/J4 e a comparação final dos fluxos com tempos de escopo equivalente. Esta revisão não altera o Revit, o AutoCAD ou a monografia.

## Referências do diagnóstico

- AltoQi. [Erro A11 — Largura do apoio insuficiente em lajes](https://suporte.altoqi.com.br/hc/pt-br/articles/115003202014), 12 set. 2024. Consulta em 3 nov. 2026. Orientação de funcionamento do programa; a referência normativa histórica no artigo não substitui a edição adotada no estudo.
- AltoQi. [Como inserir os lances da escada?](https://suporte.altoqi.com.br/hc/pt-br/articles/115002312454), 6 jul. 2026. Consulta em 3 nov. 2026. Apoios nos eixos, barras de contorno e ajuste dos degraus.

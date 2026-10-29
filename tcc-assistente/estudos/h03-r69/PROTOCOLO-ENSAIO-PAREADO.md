# Protocolo do ensaio final — dois fluxos com automação

Este protocolo define atividades futuras, não declara execução concluída. Fluxos: AutoCAD2027→DWG2D→Eberick2025Infinity e Revit2027.2→IFC adaptado→Eberick2025Infinity. Registrar os números exatos instalados e versões do suplemento/adaptador na abertura de cada ensaio. Os dois fluxos incluem automação. Não apresentar CAD como desenho manual se foi gerado por rotina.

## Condição para começar

Congelar a mesma arquitetura, referência comum de coordenadas/unidades, hipótese estrutural e matriz de propriedades/cargas, com hashes. Fechar antes os níveis, seções, cargas, critérios de apoios idealizados e configuração normativa comum; guardar pendências que impeçam uma conclusão. Não usar uma alternativa ainda em revisão como se fosse uma solução final aprovada. Guardar cópias independentes, sem transferir o PRJ pronto de um ramo ao outro.

Separar desenvolvimento comum do protótipo e treinamento das medições finais. Definir antes do primeiro ensaio os entregáveis e a tolerância por grandeza. Tolerância computacional de caixa IFC, precisão exibida pela UI e tolerância de execução são conceitos distintos. Não selecionar tolerância depois de observar uma divergência para fazê-la desaparecer.

## Unidades de tempo e limites iguais

Usar tempo decorrido prospectivo e iniciar o registro persistente ANTES do comando. Salvar imediatamente início UTC, relógio monotônico quando suportado, identificador da sessão, fluxo, etapa, revisão/hashes e operador. Ao concluir, persistir fim, duração e evidência de término. Se o runtime/servidor cair, preservar o intervalo como interrompido, sem estimar o trecho ausente ou continuar o mesmo relógio monotônico em outro processo.

Etapas para ambos os ramos:

1. Geração nativa: começar com arquitetura/matriz comum já congeladas e aplicativo aberto no estado definido; terminar com esboço nativo salvo e exportação de controle disponível. Incluir seleção/configuração e execução da rotina; registrar falhas/repetições.
2. Preparação do intercâmbio: começar no comando de exportação; terminar no arquivo aceito pelo receptor, incluindo adaptação IFC ou preparação DWG necessárias. Manter subintervalos identificados sem somá-los novamente ao intervalo maior.
3. Transferência e reconstrução no Eberick: começar ao escolher a entrada; terminar quando houver elementos nativos e dados exigidos para a auditoria. Reconstrução prevista no fluxo CAD é trabalho do fluxo, não automaticamente defeito de transferência. A adaptação necessária no BIM também integra o fluxo completo.
4. Auditoria e correções: começar ao confrontar a matriz esperada com o receptor; terminar após corrigir e verificar novamente todos os itens do escopo. Medir o esforço e classificar a causa, preservando valores antes/depois e evidência. Ajustes comuns devem ser aplicados aos dois ramos e separados das perdas de transferência.
5. Processamento e conferência: usar os mesmos critérios de análise/dimensionamento e saída esperada. Separar intervalo observado entre comando e conclusão de tempo puro do solver, se o programa fornecer este último. Resultado com aviso, erro ou verificação incompleta não recebe status de aprovação só porque o processamento terminou.
6. Documentação/compatibilização: verificar mesma lista de produtos e atualização após uma alteração comum predefinida; terminar com nativos salvos, reabertos, produtos e relatórios conferidos. Não contar texto manual desatualizado como dado estrutural corrente.

Manter fora do relógio de produtividade as esperas pessoais, indisponibilidade de licença ou intervenção humana não executada; preservá-las no tempo bruto com motivo e limites reais. Se não houver início/fim da espera, não descontar duração estimada: marcar intervalo contaminado e repetir o ensaio. Navegação e correção normalmente necessárias à tarefa permanecem incluídas. Não excluir uma tentativa simplesmente porque foi lenta ou falhou.

## Repetição e aprendizagem

Planejar pelo menos3 pares completos, com ordem alternada: CAD/BIM, BIM/CAD, CAD/BIM. Manter hardware, versões, arquivos e condições de inicialização. Identificar condição fria/quente e cache sem afirmar limpeza se não foi verificada. Executar familiarização separada e registrar sua duração. Os três pares não tornam a amostra de uma edificação representativa de toda a Engenharia Civil; reportar aprendizagem e limitações. Se não for possível repetir, apresentar um estudo pareado descritivo sem inferência estatística.

## Qualidade da informação e contagem de correções

Antes do ensaio, definir a matriz esperada por classe/elemento e campo: unidade/origem, posição/nível/seção, material, classificação estrutural, carga/ação, identificação e ligação analítica verificável. Atribuir nulo ao não verificado; ausência e valor zero não são equivalentes. Conferir por posição e identidade de origem quando disponível, sem exigir que a numeração nativa CAD/BIM seja igual.

Calcular completude apenas com denominador explícito: campos exigidos presentes e semanticamente válidos/campos exigidos inspecionados; informar separadamente campos não inspecionados. Geometria coincidente de caixas envolventes não prova identidade de malha, conexão analítica ou segurança. Para retenção de atributos, restringir o denominador aos atributos que de fato existiam na origem e estavam no escopo contratado de intercâmbio. Atributo criado só no receptor é complementação, não perda comprovada na exportação.

Contar cada ocorrência uma vez por elemento/campo/regra violada. Separar quantidade de ocorrências, quantidade de operações para corrigi-las e duração. Um comando que corrige10elementos não equivale a uma única perda; dez cliques para corrigir um campo não equivalem a dez defeitos. Classificação mínima: concepção/interpretação comum; transferência/formato demonstrada; representação esperada; operação/instrumentação; causa indeterminada. Guardar justificativa e evidência. Não forçar a categoria para explicar um ranking.

Na compatibilização, confrontar portas/janelas/circulação, faces de paredes, forro, pisos, escada, reservatório e cobertura. Manter ocorrência aberta até a verificação correspondente; corrigir uma referência aproximada não significa alterar a arquitetura original. Verificações ELU/ELS e compatibilidade geométrica têm critérios próprios e precisam ser relatadas separadamente.

## Análise final

Para cada par completo, informar T_CAD, T_BIM e diferença T_CAD−T_BIM, com escopo idêntico e soma de intervalos não sobrepostos. A diferença percentual em relação ao CAD é100×(T_CAD−T_BIM)/T_CAD; calcular somente com T_CAD>0 e ambos concluídos e comparáveis. Valor positivo indica menor duração BIM naquele par; negativo indica maior duração. Não atribuir causalidade ao programa isoladamente quando o fluxo também envolve rotinas, adaptador e operação assistida.

Com repetições válidas, apresentar mediana e faixa mín–máx por etapa e total, além dos valores individuais; manter tentativas inválidas/interrompidas em quadro próprio com motivo. Informar completude, perdas verificadas, complementações e correções ao lado dos tempos. Não produzir um índice único de qualidade com pesos arbitrários. Um fluxo rápido com campos pendentes não é equivalente ao fluxo concluído.

Separar esforço assistido da IA (tarefas e intervenções observadas) de inferência efetivamente medida por log/API, tokens/custo registrados e trabalho humano ativo. Sem fonte, usar “não medido”. Preparação comum não deve ser duplicada no total CAD e BIM. Simulações/testes automatizados validam o instrumento, não constituem uma rodada real em Revit/AutoCAD/Eberick.

## Pacote de evidências

Entregar manifesto, arquitetura/matriz comum referenciadas por hash, versões, sessões/intervalos, ocorrências/correções, nativos com dependências, exportações, relatórios e verificações de reabertura. Preservar os originais e separar o estudo exploratório das rodadas finais. Na ausência de sondagem, manter explícita a delimitação à superestrutura e os apoios idealizados. Este protocolo não altera a monografia ou aprova execução.

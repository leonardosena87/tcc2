# H03/R63 — auditoria e ampliação das cargas permanentes da cobertura

ESTUDO PARCIAL, NÃO EXECUTAR. Os dois ramos apresentaram o mesmo texto de resumo de análise e o conservaram após salvar, fechar e reabrir. Isso comprova coincidência dos valores exibidos neste estado parcial. Não comprova igualdade de todos os esforços, posições, armaduras, combinações ou conformidade normativa integral.

## Desenvolvimento real no Eberick

Utilizou-se o AltoQi Eberick 2025 Infinity instalado. A genealogia permanece AutoCAD 2027/DWG2D e Revit 2027.2/IFC adaptado, conforme os registros anteriores. Nesta revisão não houve nova operação no AutoCAD ou Revit, exportação IFC, alteração dos arquivos de origem ou edição da monografia. Criaram-se cópias independentes dos congelados R62. O CAD partiu do lançamento R62 já ampliado; o BIM partiu da cópia R62 ainda equivalente ao piloto R61.

No CAD, a consulta individual revelou Fz=0 na ação Adicional em RC07, RC08 e RC13. Corrigiu-se cada ponto para -0,807804 kN, confirmando o diálogo de carga e o diálogo do nó. RC12 já continha -0,807804 kN após reabrir, confirmando a correção salva na R62. O resumo R62 de 9,73 tf era anterior à correção de RC12 e permanece histórico. Não se demonstrou a causa técnica da falta de gravação do grupo; classificou-se a ocorrência como correção de lançamento/operação, sem atribuí-la a defeito DWG.

No BIM inseriram-se onze nós RC03..RC13 por coordenadas em centímetros e aplicaram-se seis grupos de Fz, ação Adicional, com seleção 1/2/1/4/2/1. RC01 e RC02 vieram do piloto R61 e não foram duplicados. Conferiu-se o retorno a Comando após cada aplicação. A leitura posterior de RC07 confirmou X732,5 cm/Y390 cm e Fz=-0,807804 kN. Os registros de seleção e a soma global não substituem a leitura individual de todos os treze pontos, ainda pendente.

O conjunto pretendido contém RC01/RC02=1,419551 kN cada; RC03=1,387289; RC04/RC05=2,566112 cada; RC06=2,507791; RC07/RC08/RC12/RC13=0,807804 cada; RC09/RC10=1,146561 cada; RC11=1,120503 kN. Adotou-se sinal Fz negativo para gravidade. A soma dos valores arredondados digitados é 18.511247 kN; trata-se apenas da ação permanente dos trechos A1/A2 do mapa R60, e não da cobertura integral ou do carregamento total do edifício.

## Calibração de unidades e esclarecimento da R62

Na mesma carga RC12, sem alterar a força, mudou-se temporariamente apenas Sistema/Cargas/Concentrada de kN para tf. Leu-se -0,807804 kN e depois -0,0807804 tf. A relação observada nesta interface instalada é 10 kN por tf exibida. Restaurou-se a unidade de entrada para kN. Não se modificaram as forças para ajustar o resumo.

Essa relação observada é uma convenção da interface verificada neste exemplar; não redefine a conversão física de 1 tf=9,80665 kN. A R62 empregara 9,80665 kN/tf na estimativa sem ter confirmado a conversão nativa. A R63 esclarece essa limitação e preserva o relatório anterior. A comparação com os resumos nativos utiliza agora a relação medida, explicitamente identificada.

Os 18,511247 kN correspondem a 1,8511247 tf nessa exibição. O aumento adicional R58→R63 de 8,20 para 10,05 tf é compatível dentro do arredondamento de 0,01 tf de dois resumos. A diferença total 101,00→102,86 tf também é compatível com essa tolerância. O acréscimo R62→R63 de aproximadamente 0,32 tf é compatível com quatro cargas de 0,807804 kN: RC12 corrigida na R62, mais três corrigidas nesta revisão. A compatibilidade global apoia a reconciliação, sem provar todas as posições e forças individualmente.

## Resultados exibidos e qualidade da informação

Nos dois ramos: peso próprio75,69 tf; adicional10,05 tf; acidental17,11 tf; total102,86 tf; área aproximada132,81 m²; relação774,46 kgf/m². O total utiliza a precisão interna do programa e pode diferir da soma de parcelas já arredondadas. O texto completo dos resumos CAD/BIM coincidiu, incluindo Gama-Z X+/X-/Y+/Y-=1,09/1,08/1,06/1,05 e Processo P-Delta. Conferiu-se a persistência de cada resumo após fechamento/reabertura, sem novo processamento nessa consulta.

Processou-se somente a análise estática linear; o resumo indicou P-Delta. Dimensionamento, deslocamentos ELS e análise dinâmica ficaram desmarcados. O Eberick retornou Estrutura processada com avisos, relação carga/área não usual e deslocamentos horizontais não verificados. Gama-Z abaixo do limite exibido não constitui aprovação estrutural ou verificação completa de vento/serviço. A coincidência do resumo não certifica segurança ou equivalência integral dos modelos.

## Tempos e esforço assistido

CAD: 25 min 40.686 s. Escopo: leitura/correção de três pontos, conferência de RC12, investigação de unidades, recálculo, salvamento e fechamento; inclui raciocínio, latência e intervalo entre mensagens. BIM: 23 min 50.756 s. Escopo: inserção dos onze nós, seis grupos de carga, amostra RC07, processamento, salvamento e primeiro fechamento; inclui raciocínio, latência e continuidade entre mensagens. As verificações adicionais após reabrir ficaram fora desses dois intervalos principais.

Intervalos observados de processamento: CAD 0 min 26.044 s; BIM 0 min 18.318 s. Ambos incluem captura e latência até registro da conclusão; não representam tempo puro do solver. No BIM a primeira captura retornou acessibilidade nula e exigiu atualização, sem repetir o comando de processamento. Houve ainda uma tentativa de clique UIA indisponível no diálogo de RC06, recuperada por observação e clique visual, sem alterar a carga.

Os escopos são diferentes: o CAD realizou correção/auditoria de uma tentativa anterior; o BIM realizou ampliação. Não calcular economia percentual ou declarar vencedor com esses intervalos. A IA apoiou análise, preparação de scripts, operação pela interface e organização das evidências; não se mediu separadamente tempo cognitivo, tokens, custo ou trabalho humano ativo. Os testes automatizados não fizeram chamadas reais à API OpenAI e não substituem validação nativa. Para o ensaio final, usar entradas comuns congeladas, critérios de início/fim iguais e registrar separadamente transferência, reconstrução, correções, cálculo, conferência, espera e intervenção humana.

## Preservação e continuidade

Verificaram-se 66 arquivos protegidos R62 por SHA-256. Congelaram-se os conjuntos CAD/BIM após fechar os projetos; verificou-se a integridade ZIP de ambos os PRJ e a igualdade dos hashes entre cópias. Evidência textual da interface, tempos, scripts, estados e manifesto acompanham esta revisão. O congelamento preserva PRJ e seus arquivos associados; não distribuir somente o PRJ sem conferir dependências.

Próxima etapa: completar a auditoria individual dos treze pontos nos dois ramos, conferindo coordenadas, ação e força após reabrir. Depois fechar a ação variável do telhado sem duplicar a sobrecarga já existente nas lajes e resolver P1/varanda e P2/abrigo/altimetria. Permanecem perfis/apoios/ancoragens metálicas, paredes e aberturas, reservatório1000 L/tara/base, escada/bordas, vento/combinações, ELU/ELS e compatibilização das origens RVT/DWG. O estudo continua restrito à superestrutura com apoios idealizados, sem fundações reais dimensionadas. A viga20x30 cm e a folga geométrica ao forro continuam sem aprovação de flecha/execução.

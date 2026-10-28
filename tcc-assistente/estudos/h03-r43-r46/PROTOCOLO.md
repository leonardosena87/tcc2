# Protocolo operacional da comparação H03

28/10/2026. Plano de medição e análise; não é resultado executado. Os ensaios R43–R46 são exploratórios e não possuem duração total comparável. Este protocolo não altera a monografia nem aprova o projeto estrutural.

## Unidade de comparação e controle

A unidade é o desenvolvimento do mesmo esboço estrutural da edificação, sob duas rotas automatizadas. Fixar a arquitetura, a revisão geométrica, níveis, materiais pretendidos, cargas e critérios de análise antes do ensaio comparável. Preservar a arquitetura e a hipótese estrutural por hash. Não permitir mudanças de concepção em apenas um ramo; uma revisão comum exige reaplicação documentada no outro.

Na H03 atual, a referência contém 22 trechos de pilares, 29 vigas lógicas e 11 lajes. Um trecho de pilar por pavimento, uma viga lógica e uma laje são unidades distintas. Os 32 sólidos de viga exportados pelo Eberick não constituem 32 vigas lógicas ou 32 operações de correção.

## Marcos e cronômetros

| Etapa | Início prospectivo | Encerramento verificável |
|---|---|---|
| Preparação comum | Início da interpretação/configuração da arquitetura | Hipótese comum e premissas congeladas |
| Autoria CAD | Entrada comum pronta e ambiente CAD na condição inicial registrada | DWG salvo e conferido |
| Autoria BIM | Mesma entrada comum pronta e ambiente Revit na condição inicial registrada | RVT salvo e conferido |
| Intercâmbio CAD | Início da preparação da referência por pavimento | DWGs recebidos e auditados no receptor |
| Intercâmbio BIM | Início da exportação IFC | Elementos recebidos e auditados, incluindo tratamentos do IFC |
| Complementação/correção CAD ou BIM | Estado recebido congelado | Geometria, parâmetros, ações e vínculos atendem ao critério comum |
| Análise em Eberick | Entrada completa e conferida | Relatórios e verificações definidos no critério comum concluídos |

Registrar separadamente: tempo de parede do ciclo; tempo ativo assistido; espera pelo usuário; processamento interno; interrupção técnica; e tempo de documentação/auditoria. O tempo interno de API contido em um intervalo assistido não se soma novamente. Se dois intervalos se sobrepõem, calcular sua união para o tempo de parede. Trabalho em paralelo não permite somar tempos de parede como se fossem duração sequencial.

O resultado deve informar o escopo da medida. Sem medir a concepção comum, não denominar o tempo observado “tempo total do projeto”. Sem medir autoria/intercâmbio/complementação/análise do ramo, não declarar duração total do fluxo. Datas de arquivos e duração de turnos não substituem cronômetro. Um intervalo interrompido sem encerramento confiável permanece incompleto; não recebe duração inventada.

O registro de cada operação contém identificador, ramo, revisão, software/versão, início e fim UTC, duração monotônica, entradas e saídas por hash, intervenção humana, ação da IA, motivo da correção e evidência de aceitação. Quando custo/tokens não estiverem disponíveis, registrar como indisponíveis. O tempo assistido não mede esforço cognitivo humano ou da IA isoladamente.

## Indicadores e categorias

| Indicador | Regra de contabilização |
|---|---|
| Preservação da geometria | Conferir coordenadas, seções, orientação, cotas e cobertura axial; explicitar tolerância computacional |
| Informação recebida | Contar propriedades esperadas, recebidas corretamente, alteradas e ausentes, por classe e campo |
| Conversão inicial | Identificar objetos calculáveis recebidos, separadamente das referências gráficas |
| Complementação | Contar objetos/campos que o método exige criar no receptor, com operações e duração |
| Correção de transferência | Contar ocorrências demonstradas de valor/geometria incorretos em relação à referência fixada |
| Compatibilização arquitetônica | Registrar interferência, elemento, pavimento, referência arquitetônica, decisão e estado de resolução |
| Qualidade da análise | Conferir modelo analítico, ações, vínculos, combinações e verificações previstas |
| Participação da IA | Classificar leitura, proposição, geração, operação, auditoria, recuperação de erro e documentação |
| Participação humana | Registrar decisão técnica, navegação, confiança de suplemento e correção manual, com tempo conhecido ou indisponível |

Uma referência 2D sem objetos calculáveis não é automaticamente um conjunto de erros de transferência: constitui complementação inerente à rota observada. A ausência de lajes convertidas também deve ser separada de geometria incorreta. Mudança de numeração, TEXT→MTEXT, renomeação de camada e recorte de sólido exigem análise semântica antes de classificação como erro.

Cada ocorrência pode exigir mais de uma ação. Apresentar **número de ocorrências**, **número de operações** e **tempo de retrabalho** separadamente. Não somar os três indicadores como se tivessem a mesma unidade. Atribuir cada ocorrência a concepção comum, tratamento prévio, recepção, complementação, compatibilização ou cálculo. Não atribuir ao AutoCAD/Revit uma falha de controle da interface sem evidência de defeito do programa.

Não calcular uma taxa global misturando pilares, vigas, lajes e propriedades com pesos implícitos. Expor denominadores por classe: por exemplo, 22 trechos de pilares previstos e 22 recebidos. A conclusão de qualidade deve considerar criticidade, e não apenas contagem.

## Aceitação e repetição

O término comum exige geometria conferida, parâmetros e ações completos, apoios idealizados documentados, compatibilização com arquitetura, modelo analítico conferido e verificações estruturais previstas executadas. “Processou sem erro” não basta. A alternativa experimental pode ser rejeitada; essa decisão deve aparecer como resultado de concepção comum, sem ser escondida para favorecer um ramo.

Depois de estabilizar a H03, executar novos ciclos completos, prospectivos, desde as mesmas condições iniciais. Preferir três repetições por ramo, alternando a ordem CAD→BIM / BIM→CAD / CAD→BIM, caso operacionalmente viável. Essas são repetições técnicas de um único caso, não três edificações independentes. Registrar efeito de aprendizagem, cache, arquivos já carregados e intervenção manual. Não apresentar observações exploratórias como repetições controladas realizadas.

Para pares completos e de mesmo escopo, calcular diferença T_CAD − T_BIM e diferença relativa (T_CAD − T_BIM)/T_CAD × 100, explicitando denominador. Resultado negativo indica maior duração BIM naquele par. Apresentar valores individuais e mediana/amplitude quando houver repetição suficiente; não inventar inferência estatística ou generalização a outros projetos.

A ausência de conclusão de um ramo impede declarar vantagem global. Pode-se apresentar comparação por etapa, com a limitação visível. O estudo permanece limitado à superestrutura, sem sondagem ou dimensionamento de fundações reais.

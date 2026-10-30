# Roteiro da palestra: IA aplicada à Engenharia Civil

14 slides, 20 minutos no total. Exposição até 18:00 e perguntas até 20:00. O PowerPoint contém notas de fala por slide. O PDF é uma cópia visual estática.

## Demonstração recomendada

O Revit cria um pórtico didático com quatro pilares, quatro vigas e uma laje. O complemento TCC Assistente e as famílias já recebem preparação prévia. A IA aciona essa infraestrutura. Esse fato deve ser explicado à audiência.

O ensaio real de 30/10/2026 criou os nove elementos em **0,53 s de escrita da API**. O intervalo registrado entre abrir o comando e registrar a confirmação foi **42,19 s**, incluindo interface e latência entre ações. Esse intervalo exclui abrir o Revit/base, preparar entradas, mostrar a vista 3D, salvar e revisar. Nenhum dos dois valores representa o tempo total do fluxo ou uma comparação com CAD.

## Antes de entrar na transmissão

1. Abrir o PowerPoint e conferir o modo de exibição na plataforma da palestra.
2. Deixar o Revit aberto e o complemento carregado. Uma escolha de confiança, se aparecer, deve ser feita pelo usuário antes da transmissão.
3. Reservar uma cópia nova de `demonstracao/DEMO-AO-VIVO-BASE-VAZIA.rvt`. A base reservada permanece vazia. Nunca reutilizar um resultado preenchido como base.
4. Deixar este chat acessível e copiar o texto de `PEDIDO-PARA-COPIAR-NO-CHAT.txt`. O pedido começa com “Estamos ao vivo na palestra”.
5. Combinar a troca da tela do PowerPoint para o chat e o Revit. Evitar que outras janelas pessoais apareçam no compartilhamento.

## Durante a demonstração, no slide 7

Dizer: “Preparei o complemento e a base antes da palestra. Agora vou pedir à IA para acionar essa automação em um exemplo com dimensões explícitas. A tarefa é de modelagem geométrica.”

Enviar o pedido completo. Aguardar a execução e mostrar a vista 3D. Apontar pilares, vigas e laje. Se houver tempo, selecionar uma viga para conferir a seção no tipo. Separar o cronômetro da API do tempo do pedido ao resultado.

Se houver falha de foco, aviso que dependa do usuário ou espera maior que 20 segundos, dizer: “Esta é uma limitação da execução pela interface. Vou mostrar o ensaio que já foi executado.” Abrir `demonstracao/DEMO-ENSAIO.rvt` ou usar a captura do slide 7. Não apresentar o ensaio prévio como execução ao vivo.

## Fala e tempo por slide

### 1. IA aplicada à Engenharia Civil (00:00 a 01:00)

Abertura: apresentar o estudo em desenvolvimento. A palestra mostra o uso de IA generativa para organizar uma automação, operar ferramentas e conferir registros. O objetivo é compartilhar uma experiência prática, sem anunciar um projeto estrutural concluído. O título do TCC compara os fluxos CAD 2D e BIM com o Eberick como receptor comum.

### 2. O problema do nosso TCC (01:00 a 02:00)

Explicar a pergunta do estudo em linguagem simples. O objeto é uma residência unifamiliar em Vitória da Conquista, BA. O estudo delimita a superestrutura com apoios idealizados por ausência de sondagem. Os resultados comparativos finais continuam em desenvolvimento. Não declarar que um programa venceu.

### 3. Dois caminhos para o mesmo receptor (02:00 a 03:30)

Diferenciar uma linha CAD de um elemento BIM e explicar que o cálculo depende do lançamento efetivo no Eberick. O adaptador IFC exige esforço próprio, que faz parte do fluxo. A igualdade de forma visual não garante igualdade de vínculos, cargas ou agrupamentos. Fonte: registros de intercâmbio e matriz R72 em D:/TCC/outputs/Resultados-H03-R72-PARCIAIS-NAO-FINAIS.

### 4. Quem executa cada parte (03:30 a 05:00)

Explicar a separação entre a IA e o código determinístico. O complemento TCC Assistente já foi desenvolvido no estudo. Na demonstração a IA controla sua interface e o importador usa a API. O JSON contém entradas geométricas explícitas. Não apresentar isso como uma função nativa de IA do Revit. A IA nativa do Eberick é outra funcionalidade e não compõe a demonstração. Fonte: tcc-assistente/connectors/Revit/ImportSketch.cs, especialmente validação, transação e registro de IDs.

### 5. O modelo que já foi criado (05:00 a 06:00)

Mostrar que o exemplo nasce de trabalho executado. O filtro do Revit, após salvar e reabrir, apresentou 62 elementos estruturais. Os cinco níveis do template/modelo foram excluídos da seleção. Os 62 IDs coincidiram com o registro de criação e todos os campos da exportação parcial persistiram. Isso comprova a presença e a persistência desses dados, não a conformidade estrutural. Fonte: D:/TCC/outputs/Autoria-H03-R83-SINCRONIZACAO-GEOMETRICA-NAO-EXECUTAR/R83-Revit-criacao-nativa.json e R83-Revit-leitura-apos-reabrir.json.

### 6. O pedido da demonstração (06:00 a 07:00)

Antes de alternar a tela, esclarecer que a base está vazia, as famílias estão carregadas e a proposta geométrica foi preparada e ensaiada. O pedido completo está no roteiro externo. A demonstração usa somente a pasta demonstracao e não modifica H03. Bases em 0,20 e 3,20 m. A laje é nominal, sem recorte de apoios ou detalhamento executivo. Fonte: D:/TCC/palestra-IA-engenharia/demonstracao/DEMO-9-ELEMENTOS.json.

### 7. Demonstração no Revit (07:00 a 10:00)

Alternar para o Revit e para este chat. Usar a base vazia reservada para o evento. Pedir a execução com o prompt do roteiro. A IA abre Complementos > TCC Assistente > Importar esboço, escolhe o JSON, lê a confirmação e cria os elementos. Exibir 3D, selecionar uma viga e conferir o tipo. Reservar no máximo três minutos, incluindo explicação e eventual troca de tela. Se a interface falhar por mais de 20 segundos, usar esta captura e abrir DEMO-ENSAIO.rvt, identificando-o como ensaio prévio. O tempo do pedido ao resultado ao vivo não está garantido. Fonte: captura real do ensaio em Revit 2027.2, 30/10/2026.

### 8. O que o ensaio mediu (10:00 a 11:30)

O registro real informa o valor exato em ensaio-criacao-api.json. Arredondar para duas casas decimais. Não dizer que todo o pedido, a IA ou o projeto levou 0,53 s. O ensaio da interface tem registro separado em .build/ensaio-tempo-interface.json e inclui latência entre ações. Para comparar produtividade, o estudo precisa medir escopos equivalentes, incluindo correções. Fonte: D:/TCC/palestra-IA-engenharia/evidencias/ensaio-criacao-api.json.

### 9. Como conferir o que foi criado (11:30 a 13:00)

Esta captura pertence ao TCC H03/R83, não ao pórtico didático, cujas vigas têm 20 x 40 cm. Explicar que a revisão combina contagem por categoria, IDs de origem, níveis e leitura de dimensões. A revisão R83 harmonizou 12 unidades lógicas de vigas N2 para 20 x 30 cm, deixando todas as 14 vigas lógicas N2 com o mesmo tipo. A exportação do suplemento oferece leitura parcial e não inclui b/h em campos separados. A imagem registra a dimensão no aplicativo.

### 10. Um achado da conferência no Eberick (13:00 a 14:30)

Contextualizar um único achado exploratório. Na cópia BIM R79, V2/N1 reunia um trecho 20 x 45 cm e outro 20 x 16 cm e apresentava D16. No teste isolado R81, dividiu-se o agrupamento no apoio existente P5. Após reprocessamento, o D16 ficou ausente, sem editar explicitamente as seções ou o limite de armadura. Comparou-se a geometria exportada com controle pós-dimensionamento: 89 partes geométricas coincidentes nos critérios auditados. Isso sustenta a influência do agrupamento neste caso. Não prova que o IFC causou a configuração nem valida o projeto completo. Fonte: D:/TCC/outputs/Agrupamento-H03-R81-TESTE-NAO-EXECUTAR/R81-resultado.json, R81-geometria-comparada.json e LEIA-ME-R81.md.

### 11. Como a comparação produz resultados (14:30 a 16:00)

O protocolo R69 prevê pelo menos três pares de execuções completas e equivalentes, com alternância da ordem dos fluxos. A cronometragem usa UTC e relógio monotônico antes da ação. Tempo ausente permanece nulo. Desenvolvimento comum, treinamento e preparação de conectores são identificados separadamente. Revisões de projeto comuns não devem ser classificadas como erro exclusivo de transferência CAD ou BIM. Não contar 29 unidades lógicas, 32 sólidos e 30/20 grupos nativos como se fossem a mesma unidade. Fonte: D:/TCC/outputs, protocolo R69, auditoria R80 e resultados parciais R72.

### 12. O alcance deste protótipo (16:00 a 17:00)

A automação geométrica não atesta a NBR 6118 integralmente. O importador ainda exibe triagem parcial 2023 e informa explicitamente as lacunas de materiais, emenda 2026, cargas, armaduras e ELU/ELS. O estudo dispõe do exemplar 2026, mas isso não significa implementação integral pelo código ou pelo Eberick instalado. A carga Q do telhado segue pendente após cancelamento da tentativa R82. Reservatório, vento e outros caminhos de carga continuam em revisão. Não apresentar o material como projeto para execução.

### 13. A contribuição da experiência (17:00 a 18:00)

Concluir com a experiência demonstrada, sem prometer economia percentual não medida. A IA ajudou a desenvolver e operar ferramentas, mas o estudo encontrou diferenças de agrupamento, lacunas de transferência e dificuldades de interface que precisaram ser investigadas. As evidências e os limites tornam o caso útil para discutir IA na Engenharia Civil.

### 14. Perguntas (18:00 a 20:00)

Reservar dois minutos. Respostas sugeridas: 1) A IA usa complemento próprio, API e controle de interface; não é um comando nativo de IA do Revit. 2) O estudo ainda não concluiu qual fluxo é mais rápido. 3) A demonstração não calcula nem detalha a estrutura. 4) Para reproduzir, é preciso instalar e testar o complemento e preparar as famílias. 5) O tempo de 0,53 s é exclusivamente da escrita da API no ensaio. Encerrar no limite de vinte minutos.

## Respostas rápidas

**A IA calcula a estrutura?** A demonstração cria geometria. O estudo usa o Eberick para análise e mantém verificações estruturais pendentes.

**É uma função nativa de IA do Revit?** O exemplo usa um complemento próprio. A IA coordena a operação e o complemento grava os elementos pela API.

**Qual programa foi mais rápido?** O TCC ainda precisa concluir ensaios completos e equivalentes. O tempo de uma transação não demonstra produtividade total.

**Já atende integralmente à NBR 6118?** Não existe esse atestado neste protótipo. A triagem automática é parcial e a revisão técnica continua necessária.

**Pode mudar as dimensões ao vivo?** Tecnicamente é possível preparar outra proposta, mas isso exige nova conferência e ensaio. Para esta palestra, usar as entradas testadas.

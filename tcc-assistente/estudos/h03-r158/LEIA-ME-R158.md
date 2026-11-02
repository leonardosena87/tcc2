# H03/R158 — candidato comum para compatibilização da escada

**Orientação recebida posteriormente:** o usuário informou que o orientador exige uma viga no patamar. A presença dessa viga passa a ser requisito do estudo. A orientação não foi interpretada como aprovação da posição, da seção 20 x 30 cm, dos novos pilares ou das ligações do candidato. A confirmação está em R158-orientacao-viga-patamar.json. O mesmo requisito vale para os dois fluxos.

O estudo mantém 17 espelhos iguais de 17,823529 cm, distribuição 9 + 8, pisadas de 28 cm, pisos acabados +0,22/+3,25 m e patamar acabado +1,824118 m. A posição longitudinal dos lances e do patamar da R153 foi preservada. Este candidato não substitui a geometria ativa antes de sua implantação e verificação nos aplicativos.

## Restrição da janela J4

A tabela da prancha arquitetônica apresenta J4 como janela fixa de 1,60 x 3,20 m, com peitoril de 0,20 m. A referência R68 a localiza na fachada entre X = 4,70 e 6,30 m, em Y = 0. Uma viga transversal na fachada entre P4/P10, à altura do patamar, atravessaria essa abertura. Essa alternativa foi descartada antes de qualquer lançamento. Interpretou-se o peitoril a partir do piso acabado térreo +0,22 m; mesmo que sua referência fosse o nível externo +0,20 m, a conclusão da interseção com a viga seria a mesma.

O PDF original não foi modificado. O recorte da tabela foi inspecionado localmente para confirmar a leitura; não foi incluído no repositório público.

## Geometria candidata

Adotou-se, apenas para testar o encaixe, acabamento constante de 5 cm sobre os degraus e o patamar. O topo do concreto superior coincide com +3,20 m e o patamar de concreto passa a +1,774118 m. A referência virtual inferior fica em +0,17 m, **3 cm abaixo do nível estrutural N0 +0,20**. Essa referência virtual não é um novo piso: o apoio inferior e seu encaixe devem ser resolvidos no modelo de cálculo. Não se atribuiu peso ao acabamento sem definir suas camadas e densidades.

As faixas nominais dos lances passam a 90 cm, entre faces externas X = 4,50 e 6,45 m, com vão central de 15 cm. Essas dimensões não certificam a largura útil depois de guarda, corrimão e revestimento lateral. Não se deslocaram paredes ou portas. A diferença em relação às faixas gráficas anteriores é registrada, sem considerar a arquitetura como levantamento executivo.

A borda sul de L6 passa a Y = 2,935783 m. A viga de chegada V15 passa a ter eixo Y = 3,035783 m e seção candidata 20 x 16 cm, posicionando sua face sul na chegada do lance. O topo permanece +3,20 m e a face inferior nominal fica em +3,04 m. A diferença de 2 cm para o plano hipotético de forro +3,02 m não comprova espaço construtivo para o sistema do forro ou tolerâncias. Resistência, flecha, ancoragem e conexão com a laje ainda não foram verificadas. A profundidade rasa não deve ser adotada apenas por eliminar a sobreposição gráfica.

Propõem-se dois pilares laterais P12/P13, de seção inicial 20 x 30 cm, em X = 4,40/6,55 m e Y = 0,875783 m, entre N0/N1. Uma viga V16-ESC-PAT, também inicialmente 20 x 30 cm, liga seus eixos e tem a face norte em Y = 0,975783 m, junto aos lances, com topo de concreto +1,774118 m. Essa posição evita avançar sobre a última pisada do lance inferior. O patamar se estende em direção à fachada; sua vinculação à viga, o comportamento em balanço, a torção e a transferência de reações precisam de análise. Não se declarou engaste por haver contato geométrico.

As novas seções de pilares podem sobressair à parede acabada de 15 cm; seus encontros e impactos locais permanecem em revisão. Os retângulos dos pilares não interceptam os vãos catalogados na R68, mesmo incluindo a incerteza de triagem de 5 cm. Isso não substitui a revisão arquitetônica completa, a simulação das folhas e a análise da circulação.

## Verificação e aplicação aos dois fluxos

O candidato conserva 60 elementos originais sem alteração, revisa V15/L6 e acrescenta dois pilares e uma viga: 65 elementos nominais, além da escada. O JSON usa um contrato específico de compatibilização porque a viga intermediária não é aceita pelo importador antigo que restringe vigas aos pavimentos principais. Não se apresenta o arquivo como proposta diretamente executável naquele importador.

A triagem compara somente superfícies horizontais acabadas/descontadas do acabamento com caixas nominais dos elementos. Não encontrou área positiva de superfície dentro dessas caixas. **Isso não prova ausência de interferência dos sólidos da escada**, pois o fundo resistente e a armadura não foram modelados nesse teste. Não se reivindica a eliminação dos cinco pares nativos da R157. O apoio exige conexão resistente comprovada; eliminar contato não é o objetivo do projeto.

O DXF é um desenho parcial do candidato, com 33 faces acabadas, 33 faces superiores do concreto e 30 faces de caixas dos cinco elementos novos/revisados. Não representa um volume fechado da escada, o prédio completo ou o DWG estrutural principal. A espessura resistente de 14 cm continua hipótese; peso próprio e armadura devem resultar da geometria resistente aceita, sem estimativa por esse conjunto de superfícies.

O [suporte oficial AltoQi sobre apoio inadequado](https://suporte.altoqi.com.br/hc/pt-br/articles/115004562614) orienta conferir a vinculação no croqui e na grelha, distinguindo a seleção de eixos e faces. A [criação do patamar](https://suporte.altoqi.com.br/hc/pt-br/articles/115002281074) exige explicitar os contornos e apoios, enquanto a [continuidade entre lances e patamar](https://suporte.altoqi.com.br/hc/pt-br/articles/360000143334) depende do modelo de análise. Esses procedimentos não foram substituídos por um simples teste de sobreposição.

O Eberick instalado anteriormente foi identificado como 2025-04. Não se pressupõe a disponibilidade da melhoria de apoio de escadas em vigas internas de painéis anunciada para 2025-11. O mesmo tratamento de níveis, apoios e ações deve ser aplicado aos dois receptores, com registros das correções realmente necessárias em cada origem.

Não se alteraram RVT, DWG estrutural principal, PRJ ou monografia na geração do candidato. Os tempos de geração e eventual conferência nativa são registrados separadamente. Não há ensaio CAD/BIM pareado concluído nem ranking nesta etapa. NÃO EXECUTAR.

## Conferência nativa interrompida

Abriu-se o DXF parcial R158 em um novo documento do AutoCAD 2027 e observou-se a planta após ZOOM Extents. A primeira tentativa de entrada do caminho acionou a abertura da R153 já em uso; cancelou-se a abertura em modo somente leitura e o caminho da R158 foi preenchido novamente na linha de comando. Uma tentativa posterior de definir a perspectiva iniciou uma colagem fora dessa linha. A tentativa de cancelamento retornou uma captura da janela do Codex; o estado final desse cancelamento não foi confirmado. A rodada foi interrompida pelo usuário antes do salvamento em DWG, reabertura e exportação de controle. Não há afirmação de retorno nativo validado da R158.

O registro de início CAD permanece preservado. A observação UTC de encerramento/interrupção é registrada separadamente; inclui espera e interrupção e não representa tempo ativo ou ensaio comparativo. A geometria ativa continua R153 e o RVT de visualização continua R157. A orientação sobre a viga não altera esses arquivos por si só.

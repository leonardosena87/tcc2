# H03/R153 — 17 espelhos, candidato 9 + 8

A continuação do estudo de17espelhos passou a testar **9espelhos no primeiro lance e8no segundo**, mantendo dois lances retos emU e o patamar. Esse candidato preserva a chegada superior na precisão gráfica e transfere o acréscimo de28cm ao início do lance inferior. A definição anterior8+9/R152 fica preservada; não se reduziu o hall ou o patamar nem se deslocaram paredes/portas. O apontador atual em D:/TCC/dados-pesquisa/escada-h03-atual.json passa a esta geometria como **candidato de estudo**, sem indicar implantação nos modelos.

## Geometria e sentido adotado

O espelho permanece exatamente3,03/17m=17,823529…cm e a pisada de estudo28cm. O patamar acabado passa a **+1,824118m** (cerca de12,4cm acima do patamar+1,70do desenho). O lance inferior tem8pisadas e2,24m de projeção; o superior7pisadas e1,96m. Não usar a cota+1,646m ou o perfil8+9daR152 para este candidato.

Para tornar o percurso inequívoco, o novo esquema assume **lance inferior à esquerda e superior à direita**: sobe-se em direção à fachada no primeiro, cruza-se o patamar e retorna-se ao hall no segundo. Isso é uma hipótese explícita de redesenho da escada. A leitura conjunta das plantas térrea/superior e do corteAA não foi tratada como confirmação automática das setas e projeções originais. As posições gráficas das paredes/portas foram mantidas como restrições.

A chegada fica emYlocal≈2,93578m, com diferença de aproximadamente0,033mm em relação à linha do PDF, decorrente da quantização gráfica. Essa diferença não é tolerância executiva. O hall e o patamar conservam as dimensões gráficas usadas naR147 (aproximadamente0,889m e0,902m). A faixa livre dos lances continua próxima de0,91m antes de guardas, corrimãos e interferências estruturais.

## Triagem das portas e da aproximação

A chegada fica aproximadamente19,1cm ao sul do início longitudinal da aberturaP3superior, enquanto a alternativa8+9entrava nessa faixa. No térreo, o primeiro espelho fica aproximadamente83,4cm ao sul do início longitudinal da aberturaT-P2-01. São distâncias entre coordenadas gráficas, **não larguras de passagem ou folgas de giro de folha comprovadas**. A referênciaR68adota incerteza de triagem de5cm nas aberturas.

O acréscimo inferior ocupa parte da aproximação térrea aberta. Não se aplicou ao térreo, por analogia, o hall fechado do superior e não se declarou uma circulação aprovada a partir da distância até a porta. Aproximação, fluxo de pessoas, sentido final dos lances, guarda, mobiliário e seções de pilares devem ser sobrepostos antes da implantação. A largura de91cm derivada da arquitetura não certifica largura útil com estrutura e corrimão.

## Altura livre: cenários condicionais

Considerando a borda de abertura na posição gráfica atual, com faixa de incerteza de5cm, as duas primeiras pisadas podem ficar sob a projeção do hall. Para uma face inferior horizontal em+3,02m, derivada de piso térreo+0,22e pé-direito2,80do corte, a menor distância vertical calculada é aproximadamente**2,444m**. Para a hipótese de face inferior da laje em+3,06m (planoN1+3,20menos14cm de L5registrados emR145), resulta2,484m. Uma sensibilidade com obstrução em+2,75m resulta2,174m.

Esses resultados dependem da posição e altura assumidas para o obstáculo. **Não se levantaram todas as obstruções reais, nem se verificou a escada completa em um modelo3D compatibilizado.** Para obter2,10m sobre a segunda pisada, a face inferior de um obstáculo nessa posição precisaria estar pelo menos em+2,67647m. Uma viga mais baixa ou outra borda de abertura altera a conclusão. Circulação sob patamar e regiões baixas não foi liberada.

O valor2,10m é referência de triagem geométrica, também apresentada no material didático [Concreto armado: escadas, EESC/USP,1997, seção1.1, hospedado pela Unicamp](https://www.fec.unicamp.br/~almeida/ec802/Escada/19%20Escadas.pdf). Essa fonte histórica não substitui as normas vigentes ou o enquadramento municipal da escada unifamiliar; seus valores antigos de cargas não foram importados. Não há atestado normativo nesta revisão.

## Arquivos e verificação

R153-geometria9mais8.json contém os33quadriláteros das superfícies acabadas:15pisadas,17espelhos e1patamar. Não existe espessura resistente, volume fechado, armadura, guarda ou peso próprio definido nesse modelo de superfícies. R153-planta-e-superficies.png apresenta planta e perspectiva próprias. R153-escada17-superficies3D.dxf é um desenho independente em metros para conferência, não atualização do DWG estrutural do estudo. O parser ezdxf reabriu o arquivo e auditou33faces sem erros; eventual abertura nativa será registrada separadamente.

Foram preservadas as fontesR147,R68,R152,R145porSHA-256. Os modelosRVT/DWG/PRJ e a monografia não foram alterados, nem foram aplicadas cargas ou realizado processamento estrutural. A espessura de patamar/lances e o acabamento sobre a laje ainda devem ser definidos para converter cotas acabadas em planos estruturais; não usar diretamente+1,824118como plano analítico.

O [procedimento oficial AltoQi para lançamento de escadas](https://suporte.altoqi.com.br/hc/pt-br/articles/115001700534) distingue níveis intermediários, apoios, patamares, lances e ajustes geométricos. A revisão não pressupõe que barras de contorno sejam apoios resistentes, nem adota automaticamente a escada como autoportante. A mesma solução aceita deverá ser reproduzida nos dois fluxos antes da nova transferência e comparação.

O relógio do script mede apenas geração/exportação/renderização inicial, incluindo carregamento de bibliotecas. Não mede esforço total de IA, tempo de cálculo estrutural, importação nativa ou duração final deCAD/BIM.

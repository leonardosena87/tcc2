# H03/R181 — ligação geométrica do patamar à V16

Estudo preliminar, não executar. Esta revisão somente lê os IFCs efetivamente exportados e a grelha textual dos receptores R178; não altera Revit, AutoCAD ou Eberick e não representa dimensionamento ou aprovação estrutural. Os projetos nativos atuais continuam sendo as duas cópias R178.

## Resultado local

A diferença de **2,5916667 cm** entre as frentes dos patamares não representa uma folga na face da V16 verificada. No IFC do Revit R160/R161, a frente do patamar está em Y = 7,4083333 cm e entra no volume da viga, cuja face está em Y = 10 cm. Nos IFCs dos dois receptores Eberick R178, a frente do patamar coincide com essa face. Não se deve deslocar a viga ou acrescentar pilares para eliminar essa diferença de representação.

A interseção da malha do patamar com o plano da face da viga foi calculada pelas arestas dos triângulos, recortando a seção ao retângulo real de V16. A seção resultante tem **0,273 m²**, equivalente a 1,95 m × 0,14 m, nos três arquivos. Trata-se de uma **seção vertical de contato/interseção**, não de área horizontal de apoio, comprimento de ancoragem ou capacidade resistente. A caixa envolvente foi usada para identificar o prisma da viga, mas não substituiu a interseção da malha do patamar.

Na grelha de escada exportada por cada receptor, quatro nós conectam barras do patamar de 14 cm às barras da seção R20x30B no eixo Y = 0 e Z = 177,4 cm. A identificação exige o mesmo ID de nó, não apenas coordenadas coincidentes. As posições X são 474,38; 523,13; 571,88 e 620,63 cm, iguais nos dois receptores. Essa verificação caracteriza a conectividade do arquivo exportado; não identifica, por si só, todas as liberações, a transmissão de momento, a rigidez de ligação, o comportamento do modelo interno ou as armaduras.

O controle visual no Eberick foi feito na cópia CAD R178: LE1, E1, espessura 14 cm, elevação zero, carga acidental 2,5 kN/m² e revestimento 1,0 kN/m². O diálogo Grelha indicou espaçamento configurado de 50 × 50 cm, ângulo 90° e opção de plastificação dos apoios desmarcada. Os dois diálogos foram encerrados por Escape, sem confirmar alterações. Esta revisão não contém nova releitura desses diálogos na cópia BIM. As leituras de cargas não justificam automaticamente seus valores normativos; a hipótese de revestimento permanece provisória.

## O que permanece pendente

Não se declarou igualdade integral das malhas Revit/Eberick. A geometria junto aos lances e as diferenças de cota de aproximadamente 0,118 mm continuam documentadas nas fontes; o contorno completo não foi reconciliado nesta etapa. Também permanece a auditoria de uniformidade de R178: primeiro espelho acabado de 17,800 cm, demais de 17,825 cm, em contraste com a divisão teórica de 303/17 = 17,823529 cm. O desvio máximo de 0,023529 cm excede o limite interno de conferência de 0,02 cm. Esse limite é um critério computacional do estudo, não tolerância normativa ou de execução, e não foi ampliado para obter aprovação.

Continuam pendentes a revisão dos acabamentos e da ligação inferior, a justificativa física dos apoios idealizados, o conflito com a janela J4, as cargas provisórias, as liberações/rotações e a armadura do patamar e da viga. A identificação de contato não encerra essas verificações.

## Rastreabilidade, validação e tempos

O JSON registra os hashes de onze fontes: cinco controles de R161, dois PRJ, dois IFC e duas grelhas de escada R178. Todos foram conferidos antes e depois da leitura. O programa rejeita viga não prismática, malha aberta, triângulo degenerado e seção transversal ambígua, aberta ou não convexa. O parâmetro numérico de 10⁻⁹ m e o arredondamento de vértices da seção a nove casas decimais servem apenas à computação da interseção e não estabelecem tolerâncias construtivas.

Dez testes verificam seções interiores, contato, folga, recorte parcial, duplicação de face, malha de seção aberta, falso positivo por caixa envolvente, área de recorte e distinção entre nós compartilhados e nós apenas coincidentes. O desenho R181-ligacao-patamar.png foi inspecionado visualmente. Os testes são verificações dos algoritmos de leitura; não são ensaios estruturais, execução do SAP2000 ou nova análise nativa do Eberick.

Nenhum novo tempo de processamento nativo ou tempo completo de fluxo foi medido nesta revisão. O inventário R180 permanece aplicável; não se acrescentou duração de programação ou de inspeção à comparação CAD/BIM. Os 5 s e 6 s de R178 continuam sendo duas observações de processamento parcial, sem base para concluir vantagem global entre os fluxos.

## Arquivos e reprodução

- `R181-ligacao-patamar.json`: coordenadas, seções calculadas, conectividade por ID e preservação das fontes.
- `R181-ligacao-patamar.png`: comparação local das representações, sem detalhamento executivo.
- `CAD-grelha-patamar-0.png` e `CAD-grelha-patamar-AX.txt`: leitura da interface na cópia CAD.
- `conferir_ligacao.py`, `test_ligacao.py` e `visualizar_ligacao.py`: código da auditoria, testes e figura.

Executar `python conferir_ligacao.py`, `python -m unittest discover -s . -p "test_*.py" -v` e `python visualizar_ligacao.py` a partir desta pasta, com as dependências locais registradas nos scripts. Os caminhos das fontes permanecem em D:/TCC. A auditoria não cria ou edita IFC/PRJ e não executa SAP2000.

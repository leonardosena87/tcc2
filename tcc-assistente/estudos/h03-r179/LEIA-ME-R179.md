# H03/R179 — cargas de barras em referência global comum

**Auditoria somente leitura; estudo preliminar — não executar.** Esta revisão continua a comparação dos receptores CAD/BIM R178. Não cria uma nova versão nativa do Eberick e não altera os arquivos do Revit ou do AutoCAD. Os dois PRJs, dois IFCs e oito arquivos analíticos R178 foram conferidos por SHA-256 antes e depois da leitura.

## Problema e procedimento

A comparação anterior conservava o sentido I–J e, por isso, identificava diferenças entre registros de cargas descritos em eixos locais distintos. Nesta etapa, implementou-se a transformação vetorial dos eixos locais 1/2/3 para X/Y/Z globais, considerando o ângulo de rotação exportado para cada barra. Ordenou-se cada segmento por suas coordenadas e, quando necessário, inverteu-se a estação relativa de aplicação. No caso trapezoidal, também se trocaram as intensidades das extremidades.

A definição de eixos segue a documentação do SAP2000: o eixo 1 acompanha a barra; a orientação transversal utiliza a referência vertical, com tratamento específico de elementos verticais e rotação pela regra da mão direita. O manual define o limiar de verticalidade pelo seno inferior a 10⁻³. A rotina implementa essa convenção para interpretar as tabelas exportadas, sem executar o programa. [CSI — Frame Local Axes](https://docs.csiamerica.com/help-files/sap/Menus/Assign/Frame/Frame_Local_Axes.htm), [CSI Analysis Reference Manual, capítulo The Frame Element](https://docs.csiamerica.com/manuals/sap2000/CSiRefer.pdf).

Somaram-se componentes somente quando coincidiam segmento, padrão e estação ou intervalo. Registrou-se a quantidade de linhas que compõe cada grupo; cargas duplicadas não foram simplesmente descartadas. A rotina aceita apenas forças com sistema LOCAL, direções 1/2/3 e distâncias relativas, que correspondem aos registros encontrados. Uma entrada fora desse escopo provoca erro explícito. O leitor também verifica a declaração `Kgf, cm, C` dos arquivos, sem inferir sua escala.

Utilizou-se arredondamento declarado de oito casas decimais nas componentes e estações canônicas para evitar diferenças de máquina decorrentes da trigonometria. Isso não constitui tolerância normativa nem autorização para modificar cargas. Preservou-se a precisão original das estações relativas e dos ângulos exportados; não se atribuiu precisão adicional aos dados de origem.

## Resultado efetivamente encontrado

| Modelo | Linhas distribuídas por receptor | Grupos após reunir componentes | Resultado global |
| --- | ---: | ---: | --- |
| Pórtico | 92 | 92 | Coincidentes no arredondamento declarado |
| Escada | 868 | 574 | Coincidentes no arredondamento declarado |
| Laje N1 | 2.101 | 2.101 | Coincidentes no arredondamento declarado |
| Laje N2 | 2.001 | 2.001 | Coincidentes no arredondamento declarado |

Na grelha da escada, o número de grupos é menor porque se reuniram componentes em direções locais diferentes no mesmo trecho e intervalo. A igualdade se refere à soma vetorial das forças exportadas, não ao descarte dessas componentes.

Para as forças pontuais em barras do pórtico, identificou-se o mesmo conjunto de 900 estações/padrões nos dois receptores. Treze registros ainda apresentam diferença de componente, com valor absoluto máximo aproximado de 0,0001 kgf. Os valores CAD/BIM e suas diferenças foram mantidos em `R179-cargas-globais.json`; não se declarou igualdade integral dessas cargas. As outras três exportações não contêm cargas pontuais de barras.

As diferenças de cargas nodais registradas na R178 também permanecem: 16 registros no pórtico e nove na laje N2. Esta revisão trata das cargas de barras e não elimina aquelas ocorrências. A coincidência das distribuídas esclarece que parte das diferenças textuais decorria da representação local; não demonstra, isoladamente, equivalência de esforços internos, rigidez, dimensionamento ou comportamento completo.

## Limite do intercâmbio utilizado como evidência

O arquivo textual SAP2000 é uma representação exportada pelo Eberick. A AltoQi informa que a opção de exportar seções pode produzir diferenças de inércia e retirar a hipótese de diafragma rígido no modelo exportado. Como essa opção estava marcada nos dois receptores, a comparação aqui realizada serve para confrontar suas saídas sob a mesma configuração; não se deve confundi-la com uma reprodução integral do modelo interno do Eberick. [AltoQi — Como exportar o projeto do Eberick para o SAP2000?](https://suporte.altoqi.com.br/hc/pt-br/articles/360016037073).

## Verificação e próximos passos

Foram executados nove testes locais: referência horizontal, elemento vertical, coluna orientada para baixo, rotação de 90°, inversão de carga pontual, inversão de carregamento trapezoidal, soma de duplicatas, preservação de pequenos resíduos e rejeição de casos não suportados. São testes matemáticos e de leitura de dados, sem chamada à IA, execução do SAP2000 ou aprovação estrutural.

Para reproduzir, executar `python -m unittest discover -s tcc-assistente/estudos/h03-r179 -p "test_*.py"` e `python tcc-assistente/estudos/h03-r179/normalizar_cargas.py`, com as evidências R178 presentes em D:/TCC. O resultado é salvo em `D:/TCC/outputs/Analise-H03-R179-CARGAS-REFERENCIA-COMUM-NAO-EXECUTAR/R179-cargas-globais.json`.

O trabalho da IA desta etapa foi a elaboração e execução da auditoria, consulta à documentação oficial e interpretação dos resultados. Não se mediu um novo fluxo CAD/BIM; os tempos nativos da R178 continuam 5 s e 6 s para análise parcial, sem conclusão sobre produtividade integral.

Permanecem a conferência dos resíduos pontuais/nodais e das propriedades de rigidez em referência comum; o contorno dianteiro do patamar; as barras externas remanescentes; os acabamentos e a base da escada; a justificativa dos apoios idealizados; a verificação das interferências, altura livre, cargas, dimensionamento, ELS e detalhamento; e a consolidação dos tempos dos dois fluxos. A monografia não foi alterada.

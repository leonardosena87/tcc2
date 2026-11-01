# H03/R112 — envelope do reservatório sob a cobertura P2

O corte BB foi relido visualmente em conjunto com os vetores do PDF original. A dimensão de **1,30 m termina no topo da platibanda**, acima do contorno inclinado da cobertura. Portanto, ela não representa uma altura livre uniforme sobre a base do reservatório. A R71 já mantinha essa dimensão como bruta e não aprovava instalação; a R112 quantifica a restrição do contorno desenhado.

## Método de leitura e resultado

Preservou-se o PDF com SHA-256 `3a57561f03e2c0e92964b19e577a02939b04fc93cdf1ef27cad6f79ad2deb12d`. No corte BB da única prancha, associaram-se os centros das paredes do abrigo aos eixos nominais X = 6,55 e 9,65 m de P2. A dimensão vertical de 1,30 m calibrou a direção vertical. Obtiveram-se aproximadamente 56,671 unidades PDF/m horizontalmente e 56,677 verticalmente, compatíveis com a escala 1:50 da prancha. Essa concordância é controle de leitura, sem atribuir precisão executiva ao desenho.

O contorno inferior selecionado é a reta entre os pontos PDF (1449,600; 1764,320) e (1609,680; 1748,240). A base desenhada possui ordenada PDF 1816,400; o topo da platibanda, 1742,720. O script rejeita outra versão do PDF ou seleção ambígua da reta, verifica inclinação próxima de 10% e impede extrapolação além do trecho medido. O recorte arquitetônico foi mantido em work, sem reproduzir a prancha no repositório público.

Adotou-se a caixa envolvente superior de cada referência dimensional da R71, centrada provisoriamente em X = 8,10 m. Para uma cobertura inclinada, a altura mínima sobre essa caixa ocorre na borda de menor altura, não no centro do tanque. Trata-se de uma triagem bidimensional: a forma real da tampa, os pontos de inspeção e a retirada da tampa não foram modelados.

| Referência dimensional | Altura mínima do contorno sobre a base (m) | Altura do tanque usada (m) | Folga otimista restante (m) |
| --- | ---: | ---: | ---: |
| Circular R71 | 0,978 | 0,970 | 0,008 |
| Retangular baixa R71 | 0,993 | 0,680 | 0,313 |

A primeira folga é da ordem de milímetros e não permite concluir compatibilidade física, considerando a natureza gráfica da referência. A folga da referência baixa é cerca de 31 cm, antes de resolver perfis, ligações, tampa e instalações. **Nenhuma referência satisfaz a reserva superior hipotética de 0,60 m da R71**, mesmo nessa avaliação otimista. Essa reserva é uma hipótese de estudo, sem apresentá-la como exigência universal da ABNT ou dos fabricantes.

Como sensibilidade, deslocou-se a referência retangular para o lado mais alto, até X = 8,36 m, preservando a margem lateral hipotética de 0,60 m até a face interna do abrigo. A folga otimista aumentou somente para aproximadamente 0,339 m. O deslocamento não resolve a reserva superior de estudo e não foi adotado na arquitetura ou no modelo estrutural.

Não se subtraiu uma altura inventada de perfil: a folga efetiva está **nula/desconhecida**, separada da folga otimista calculada. A distância entre os dois traços da cobertura arquitetônica não foi confundida com a espessura de 6 mm da telha adotada. O contorno representa a cobertura desenhada, sem definir as seções reais do conjunto metálico.

## Fontes do reservatório e decisões pendentes

A [página oficial da Bakof](https://www.bakof.com.br/produtos/4) e a tabela da página 3 do [descritivo técnico disponibilizado pelo fabricante](https://bakof.com.br//storage/produtos/4/arquivos/bfe0589dcc022783df21505d82813e26.pdf) reconfirmaram as dimensões da referência retangular: comprimento superior 1,88 m, largura superior 1,23 m e altura 0,68 m. A tabela consultada não informa a tara. O descritivo contém referências normativas históricas; não se usou esse texto para atestar vigência normativa ou certificação atual.

O [manual do fabricante](https://bakof.com.br//storage/produtos/4/arquivos/151d4279da2695905e75d4466da41001.pdf) descreve apoio contínuo e acesso para inspeção. A interpretação dimensional não dimensiona esse apoio nem demonstra condições reais de manutenção. A referência circular permanece baseada nas dimensões históricas registradas na R71; a página do produto não pôde ser reconfirmada nesta consulta por tempo excedido. Não se selecionou marca ou modelo para compra.

Mantêm-se as alturas arquitetônicas e a capacidade de 1.000 L. A alternativa para prosseguir exige estudar acesso lateral ou abertura removível da cobertura, sem presumir que isso soluciona manutenção, estanqueidade ou segurança. O envelope real de retirada da tampa, as tubulações, a base e suas reações continuam pendentes. Não se reduziu silenciosamente a folga de estudo nem se abaixou a base para declarar compatibilidade.

A referência vertical da base do corte ainda não foi ligada a uma cota estrutural absoluta do N2. O ressalto local de 0,60 m não autoriza adotar N2 + 0,60 m sem essa correspondência. Tara e pedestal permanecem desconhecidos; não se aplicou a carga da água ou da base aos receptores. Revit, AutoCAD, Eberick e monografia foram preservados nesta revisão.

## Verificação e registro

Dois testes verificam que o mínimo é tomado na borda baixa e que entradas inválidas/extrapoladas são rejeitadas; também verificam que perfil desconhecido não vira redução zero. O tempo do arquivo de script abrange extração, aritmética e geração da figura, sem representar pesquisa, autoria, inferência ou produtividade dos fluxos. A figura é esquema analítico, não uma nova planta executiva. Os resultados ficam em `D:/TCC/outputs/Reservatorio-H03-R112-ENVELOPE-NAO-EXECUTAR/`.

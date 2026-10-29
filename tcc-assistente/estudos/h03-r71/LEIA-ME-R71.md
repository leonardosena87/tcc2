# H03/R71 — reservatório de1.000L, espaço e cargas de estudo

ALTERNATIVAS NÃO APLICADAS. NÃO EXECUTAR. Mantém-se a capacidade autorizada de1.000L. Não se selecionou marca para compra nem se dimensionou base/apoio. A posição em planta apresentada é candidata de estudo e não localização definitiva. Os arquivos nativos e a monografia não foram alterados.

## Compatibilização dimensional

Na página atual do produto, a referência circular Fortlev informa diâmetro com tampa1,52m, altura0,97m e fundo de diâmetro1,16m. São dimensões aproximadas. [Produto oficial](https://www.fortlev.com.br/produtos/reservatorios/caixa-dagua-de-polietileno-1000l/).

A referência retangular Bakof Tec de1.000L informa comprimento superior1,88m, largura superior1,23m, comprimento inferior1,53m, largura inferior0,88m e altura0,68m. São referências para verificar espaço, sem assumir que o desenho arquitetônico representa esse modelo. [Produto oficial](https://www.bakof.com.br/produtos/4).

| Referência | Dimensões superiores X×Y no estudo (m) | Altura (m) | Sobra aritmética dentro de1,30m bruto (m) |
|---|---:|---:|---:|
| Fortlev | 1.52 × 1.52 | 0.97 | 0.33 |
| Bakof Tec | 1.23 × 1.88 | 0.68 | 0.62 |

O corte BB mostra1.000L, ressalto local de0,60m da base e dimensão vertical local de1,30m sob região de telhado inclinado. Não se converteu1,30m em altura livre de manutenção nem em cota estrutural absoluta. A inclinação, espessura da cobertura, perfis, tampa e elevação real da base precisam entrar no confronto. Não se adotou simplesmente N2+0,60m: o vínculo entre cotas arquitetônicas e estruturais ainda precisa de conferência, preservando as alturas conforme decisão do usuário.

Em planta, utilizou-se provisoriamente P2 R60, X6,55..9,65/Y0..3,90m. Retirando metade da parede acabada15cm de cada lado, a área interior hipotética fica2,95×3,75m. O centro de estudo é X8.100/Y1.950m. Orientando o comprimento maior da referência retangular em Y, ambos os envelopes cabem nessa planta com margem lateral de estudo de0,60m. Essa margem não é levantamento nem prescrição universal. O manual Fortlev consultado pede espaço lateral e apoio integral; o manual Bakof deve ser seguido para seu próprio produto. [Manual Fortlev](https://www.fortlev.com.br/wp-content/uploads/2020/01/Manual_tecnico_fortlev_caixa_dagua_2020-06.pdf), [manual Bakof](https://bakof.com.br//storage/produtos/4/arquivos/151d4279da2695905e75d4466da41001.pdf).

Para testar sensibilidade vertical, reservou-se0,60m ACIMA da tampa como hipótese de estudo, sem atribuir esse número à norma ou aos dois fabricantes. A referência circular exigiria1,57m, superando a dimensão bruta1,30m. A baixa retangular exigiria1,28m, sobrando só2cm antes de considerar o perfil inclinado, as espessuras e as demais folgas. Portanto, nem mesmo essa referência recebeu aprovação de instalação. O modelo mais baixo é candidato para continuar a análise; não se elevou a cobertura para fazê-lo caber.

## Parcelas de carga

1.000L correspondem a1m³. Com densidade de referência hipotética1.000kg/m³ e gravidade convencional9,80665m/s², o peso de referência é9.80665kN. Para a sensibilidade preliminar adotou-se10,00kN de água, arredondamento superior de1.972%. O valor10 não foi apresentado como transcrição normativa e não decorre da conversão de exibição kN/tf do Eberick. A tara permanece desconhecida, campo nulo.

Compararam-se três espessuras hipotéticas de plataforma cheia1,35×2,00m, usando25kN/m³ para concreto, coerente com o peso próprio já utilizado no estudo. Não se escolheu nenhuma espessura por resistência/flecha. O apoio sob toda a base do reservatório é requisito de instalação a considerar; a plataforma e os elementos que a sustentam exigem cálculo.

| Espessura hipotética (cm) | Peso da plataforma (kN) | Água+plataforma, sem tara/pedestal (kN) | Média equivalente sobre2,70m² (kN/m²) |
|---|---:|---:|---:|
| 8 | 5.40 | 15.40 | 5.7037 |
| 10 | 6.75 | 16.75 | 6.2037 |
| 12 | 8.10 | 18.10 | 6.7037 |

A média equivalente não é pressão local real de contato nem pode ser espalhada em toda a laje para ocultar o efeito concentrado. A reação transmitida pelo fundo, a rigidez da plataforma e o suporte por laje/vigas precisam de verificação. A plataforma em cota elevada também pode exigir pedestal/muretas e respectivas cargas, ainda desconhecidas (null) no cadastro, sem serem tratadas como zero.

Não se lançou carga no N2. A classificação final da água como ação permanente ou variável exige explicitar o regime de operação e as situações cheio/vazio, conforme a base normativa adotada; a capacidade sozinha não determina essa escolha. Tara e plataforma são parcelas próprias e não se confundem com peso das telhas ou sobrecarga de manutenção. A ação Água pré-cadastrada do Eberick não foi aceita automaticamente sem conferir seu grupo/fatores.

## Continuidade

Fechar a altimetria P2 e o envelope sob o telhado, escolher uma referência de estudo compatível, obter tara e detalhes do fundo, e definir a base/apoios preservando a arquitetura. Depois calcular efeitos locais, ELU/ELS, reações e combinar cheio/vazio antes de aplicar a mesma hipótese nos dois ramos. O estudo permanece restrito à superestrutura; não se projetou fundação do reservatório. A ausência do peso total não foi preenchida com um valor inventado.

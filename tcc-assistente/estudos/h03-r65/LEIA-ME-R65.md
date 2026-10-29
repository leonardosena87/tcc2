# H03/R65 — plano da carga variável do telhado

PLANO CALCULADO, NÃO APLICADO NO EBERICK. NÃO EXECUTAR. O último estado nativo conferido permanece R64. Nenhuma ação ou combinação foi criada, nenhuma carga nativa foi modificada e nenhum novo processamento foi realizado nesta etapa.

## Parcela calculada

Retomou-se o arranjo hipotético R60 de oito barras metálicas biapoiadas, com reações verticais de extremidade e ausência idealizada de empuxo horizontal. Mantiveram-se os trechos nominais A1/A2, 55,9425 m² em projeção horizontal, e a hipótese de inclinação de 10%. O exemplar local NBR 6120:2019, subseção6.4/páginas impressas29–30, fundamenta a parcela distribuída de manutenção de 0,25 kN/m² para esse recorte. A consulta não confirma por si só a vigência de catálogo nem aprova o arranjo metálico. A tabela10/página19 trata separadamente a laje de cobertura de concreto, para a qual a R53 já lançou Q=1,0 kN/m². Não se substituiu esse Q por 0,25 nem se declarou que ambos representam a mesma carga.

| Ponto | X (cm) | Y (cm) | Fz calculado (kN) | Entrada proposta (kN) |
|---|---:|---:|---:|---:|
| RC01 | 110 | 0 | -1.0725000 | -1.072500 |
| RC02 | 330 | 0 | -1.0725000 | -1.072500 |
| RC03 | 547.5 | 0 | -1.0481250 | -1.048125 |
| RC04 | 110 | 390 | -1.9387500 | -1.938750 |
| RC05 | 330 | 390 | -1.9387500 | -1.938750 |
| RC06 | 547.5 | 390 | -1.8946875 | -1.894688 |
| RC07 | 732.5 | 390 | -0.6103125 | -0.610313 |
| RC08 | 887.5 | 390 | -0.6103125 | -0.610313 |
| RC09 | 110 | 705 | -0.8662500 | -0.866250 |
| RC10 | 330 | 705 | -0.8662500 | -0.866250 |
| RC11 | 547.5 | 705 | -0.8465625 | -0.846563 |
| RC12 | 732.5 | 705 | -0.6103125 | -0.610313 |
| RC13 | 887.5 | 705 | -0.6103125 | -0.610313 |

A soma calculada é 13.985625 kN descendente, igual a 0,25 vezes55,9425 m². Verificaram-se também os primeiros momentos, confrontando as reações com as integrais dos dois retângulos: soma(Fx_coordenada)=57.581953125 kN.m e soma(Fy_coordenada)=54.059765625 kN.m, em que Fx/Fy_coordenada significam força vertical multiplicada pela coordenada, não componentes horizontais de força. No JSON usam-se nomes firstMomentX/firstMomentY para identificar essas somas. O equilíbrio dos três escalares passou com tolerância1e-9. O arredondamento proposto a seis decimais, HALF_UP, soma 13.985628 kN e produz diferença de 0.000003000 kN; não é medição da precisão interna do Eberick.

## Ações e prevenção de duplicação

Propõe-se ação identificável Q_TELHADO_MANUTENCAO para manter rastreabilidade da manutenção do telhado, distinta da Q da laje. Não se escolheu fator de ponderação/combinação nem simultaneidade neste plano. A ausência de uma decisão justificada sobre correlação entre as manutenções não autoriza marcar ações como mutuamente excludentes ou somá-las integralmente por conveniência. Antes de aplicar, deve-se conferir no Eberick a classificação, os grupos, fatores e combinações efetivas dos dois ramos e documentar a decisão com a base normativa adotada. O forro acartonado G2=0,25 kN/m² da R53 é carga permanente: igualdade numérica com Q do telhado não torna as parcelas intercambiáveis.

O item6.4 também exige verificação específica de elemento isolado com força concentrada de1kN na posição desfavorável, além das permanentes e isolada das demais variáveis. Essa verificação local NÃO foi substituída pelas 13 reações distribuídas, NÃO foi aplicada como1kN em todos os nós e permanece pendente com o dimensionamento metálico. A inclinação nominal não substitui projeto de drenagem, rigidez, sucção e ancoragens.

## Procedimento seguinte no receptor

Criar cópias independentes dos congelados R64, verificar as ações e combinações atuais, estabelecer a classificação de Q do telhado e aplicar apenas a parcela aprovada em cada nó existente, preservando G. Conferir coordenadas e ação antes da digitação; salvar/fechar/reabrir e reler cada ponto. Reprocessar e confrontar resumos somente após fechar o escopo de cargas. Registrar os mesmos limites de etapa nos dois ramos e separar esforço de instrumentação, transferência, correção e conferência. A preparação deste mapa não conta como transferência ou resultado de aplicação nativa.

P1/varanda, P2/abrigo e sua altimetria, tanque1000L/tara/base, paredes/aberturas, escada, vento/combinações e ELU/ELS continuam pendentes. Este plano não acrescenta carga de P1/P2 à área A1/A2 nem aprova fundações ou segurança estrutural.

## Fontes e preservação

Exemplar normativo local identificado por hash no JSON; páginas PDF25/35/36 visualmente consultadas. A busca aberta não recuperou confirmação direta do estado atual no catálogo ABNT, portanto não se afirmou vigência confirmada. Documentação operacional oficial consultada: [criar ações](https://suporte.altoqi.com.br/hc/pt-br/articles/115001646393) e [configurações de ações](https://suporte.altoqi.com.br/hc/pt-br/articles/360000624993); seus exemplos normativos não substituem a edição adotada no TCC. Verificaram-se 75 arquivos do manifesto R64 por hash. PDF normativo e imagens de suas páginas permanecem locais e não são copiados para o repositório público. Nenhuma monografia ou origem RVT/DWG foi editada.

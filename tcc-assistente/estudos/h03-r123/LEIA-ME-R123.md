# H03/R123 — comparação estrita e diagnóstico da ordem I/J

Analisaram-se os seis arquivos textuais exportados na R122, preservados por SHA-256. Não se editaram arquivos nativos nem se executou Eberick/SAP2000 nesta etapa. A comparação alcança a representação exportada e sua precisão, sem provar identidade interna do solver ou conformidade normativa.

## Método

Cada nó é identificado por coordenadas, exigindo ausência de posições coincidentes. A ordem I/J das barras é preservada, assim como direção local, sinal e posição relativa de cargas. Formatos numéricos são normalizados sem tolerância por Decimal; zero negativo é unificado também nas coordenadas. Nomes/identificadores de materiais, seções, ações e combinações são preservados.

Usam-se multiconjuntos, conservando repetições. Além da comparação de tabelas, agrupam-se todos os registros associados a cada barra antes da comparação: isso evita aceitar como iguais cargas e propriedades trocadas entre barras paralelas que compartilhem os mesmos extremos.

## Resultado

| Modelo | Pares com identificação geométrica única | Mesma ordem I/J | Ordem I/J invertida | Grupos de barras paralelas sem pareamento individual único |
|---|---:|---:|---:|---:|
| Pórtico | 131 | 63 | 68 | 1 grupo com 2 barras por ramo |
| Grelha N1 | 838 | 762 | 76 | 0 |
| Grelha N2 | 794 | 635 | 159 | 0 |

O nome da seção atribuída coincide em todos os pares únicos de cada modelo. Como as respectivas tabelas de propriedades de seções também coincidem, não se identificou diferença dessas propriedades nesses pares. Não se aplicou transformação de eixos ou cargas para declarar equivalência mecânica de barras invertidas.

No pórtico, 13 das 18 tabelas coincidem após substituição da numeração por posições: coordenadas, apoios, cargas nodais, combinações, padrões/casos/atribuições de carregamento, parâmetros não lineares, atribuições explícitas de ângulos locais, propriedades de seção/material e controle do programa. Nas grelhas N1/N2, coincidem 14 das18 tabelas, incluindo as tabelas de liberações presentes em cada exportação.

As tabelas estritas de conectividade, atribuição de seção e estações diferem porque a identificação mantém a ordem dos extremos. A comparação estrita das cargas distribuídas e, no pórtico, concentradas também difere. Há exemplos de posição relativa r em uma barra que aparece como 1−r na barra invertida do outro ramo. Essa observação explica por que comparação textual direta pode sinalizar diferenças, mas não demonstra sozinha equivalência de todas as cargas.

As contagens de registros diferentes não são contagens de defeitos, correções necessárias ou elementos físicos Revit/AutoCAD. Não devem ser usadas para concluir que um fluxo gerou mais erros. A causa da direção relativa CAD Y− / BIM Y+ permanece não demonstrada. A orientação I/J é uma diferença documentada a investigar, sem nexo causal confirmado.

## Integridade e limites

`R123-resultado-final.json` é a comparação válida; `R123-orientacao.json` conserva seu hash e a classificação complementar. O primeiro rascunho local `R123-resultado.json` antecedeu a correção de normalização de zero negativo em coordenadas; ele permanece local por rastreabilidade e **não é resultado final nem fonte para resultados do TCC**.

Os três testes usam as exportações reais, conservam diferenças de orientação e detectam alteração de intensidade em0,0001, duplicação de registros e identidade ambígua por nós coincidentes. São testes do comparador, sem recálculo estrutural.

A duração em `scriptTime` mede somente a execução Python. Não representa tempo de projeto, operação CAD/BIM, esforço de desenvolvimento ou inferência da IA. Sem ranking de produtividade e sem edição da monografia.

Saída: `D:\TCC\outputs\Comparacao-Analitica-H03-R123-SOMENTE-LEITURA`.

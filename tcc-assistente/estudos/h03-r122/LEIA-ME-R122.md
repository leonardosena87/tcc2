# H03/R122 — extensão analítica exportada da carga W03

Consulta concluída em cópias independentes 38 CAD / 39 BIM, derivadas da R121. As duas foram fechadas sem salvar alterações. Os 35 arquivos de origem R121 e os dois PRJs consultados mantiveram seus hashes; integridade ZIP dos PRJs conferida. Nenhuma carga, geometria, RVT, DWG ou monografia foi alterada nesta revisão.

## Evidência direta

O Eberick exportou seis arquivos textuais `.$2k`: pórtico e grelhas N1/N2 de cada ramo. Não se abriu ou executou SAP2000. A operação foi somente uma exportação nativa do Eberick seguida de leitura textual por Python.

| Campo | CAD | BIM |
|---|---:|---:|
| Barra exportada correspondente à W03 | 31 | 30 |
| Extremos, em cm | (0;705;320) → (440;705;320) | mesmos extremos |
| Comprimento | 440 cm | 440 cm |
| Ação distribuída | G2 | G2 |
| Sistema/direção declarados | LOCAL / 2 | LOCAL / 2 |
| Intervalo relativo | 0 a 1 | 0 a 1 |
| Intensidade inicial/final no arquivo | −4,4400 / −4,4400 | −4,4400 / −4,4400 |
| Unidade declarada pelo exportador | Kgf, cm, C | Kgf, cm, C |
| Integral da carga, em magnitude | 1.953,6 kgf = 1,9536 tf | 1.953,6 kgf = 1,9536 tf |

O trecho vizinho, X=440 a965 cm em Y=705/Z=320 cm, não contém carga G2 distribuída no arquivo. A consulta nativa mostra carga extra zero na CAD V5 e no segundo trecho BIM V1. O nome V1 se repete no BIM; nome isolado não identifica o trecho carregado. A identificação usa posição, pavimento, imagem e conectividade exportada.

## Reconciliação e limites

A faixa livre da parede W03 na matriz R120 estende-se de X=10 a430 cm, com 420 cm. A exportação evidencia aplicação em 440 cm: 10 cm além da faixa livre em cada extremidade, comprimento 4,7619% maior. Isso resolve a extensão **da representação exportada**, sem provar identidade de todos os detalhes internos do solver.

A integral de 1,9536 tf é coerente com o acréscimo exibido de 1,95 tf entre R116 e R121. Essa coerência não foi usada sozinha para deduzir a extensão: coordenadas, conectividade e intervalo da carga foram lidos diretamente.

Há uma convenção de unidades a esclarecer: a interface nativa relê 4,44 kN/m, enquanto o arquivo declara −4,44 kgf/cm. Pela conversão convencional, a magnitude desta última corresponde a 4,3541526 kN/m. Não se demonstrou a regra de conversão interna do aplicativo. Não se atribui isso ao IFC, ao DWG, a erro de transferência ou a defeito do software. Também não se afirma que a precisão interna armazenada seja de apenas duas casas; a evidência alcança a interface e a exportação.

A R121 continua como ensaio parcial, sem aprovação do lançamento definitivo da W03. Não se reduziu a intensidade apenas para ajustar o total do resumo. A representação parcial da alvenaria e a convenção de unidades precisam de solução explícita antes de ampliar o lançamento às outras paredes.

## Comparação geométrica limitada

Sem depender da numeração dos nós/barras, foram comparadas multiconjuntos de coordenadas e de pares de extremos, mantendo multiplicidades e precisão exportada:

| Modelo | Nós por ramo | Barras por ramo | Coordenadas e extremos |
|---|---:|---:|---|
| Pórtico | 110 | 133 | iguais |
| Grelha N1 | 467 | 838 | iguais |
| Grelha N2 | 443 | 794 | iguais |

Isso não compara integralmente seções, eixos locais, liberações, cargas, combinações ou resultados, nem comprova equivalência estrutural completa. As contagens referem-se à discretização analítica, não ao número de elementos físicos Revit/AutoCAD.

O escopo nativo selecionou pórtico, grelhas N1/N2, exportação de seções e de coeficientes redutores. O [fabricante descreve](https://suporte.altoqi.com.br/hc/pt-br/articles/360016037073) esse formato e alerta que a exportação de seções pode alterar a consideração do diafragma e o cálculo externo das inércias. Não se utilizou o arquivo como análise independente nem como validação de dinâmica, resistência ou armadura.

## Tempos e reprodução

Os JSONs de sessão conservam UTC e relógio monotônico. São sessões exploratórias com consulta, navegação, pesquisa e registro, com escopos e interrupções diferentes entre CAD/BIM. Não representam duração pura de exportação, não devem ser somados a intervalos contidos e não sustentam ranking de produtividade.

`consolidar.py` lê os seis arquivos exportados, verifica identificação/extensão/unidades, recusa interpretações não suportadas e confere hashes das fontes e PRJs. `test_exportacao.py` exercita dados reais e rejeita unidade não suportada, intervalo ausente e nó duplicado. Esses testes verificam extração e integridade; não são cálculo independente ou verificação normativa.

Artefatos locais: `D:\TCC\outputs\Extensao-W03-H03-R122-CONSULTA-NAO-EXECUTAR`. Binários nativos permanecem somente em `D:\TCC`. Sem envio remoto nesta etapa.

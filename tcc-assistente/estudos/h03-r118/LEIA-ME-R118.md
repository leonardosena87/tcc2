# H03/R118 — consulta global de barras e bitolas

Consultaram-se novas cópias derivadas da R116 no Eberick 2025 Infinity. Abriram-se Materiais e durabilidade → Barras e as listas de Bitolas de vigas, pilares e lajes, com aplicação em **Projeto inteiro**. Cada consulta foi cancelada; as cópias foram fechadas sem salvar. Não houve edição de propriedades, processamento, dimensionamento ou alteração da monografia.

A grade geral de 24 linhas foi observada no topo e na base. Encontraram-se seis bitolas ativas: **6,3; 8; 10; 12,5; 16 e 20 mm**, todas com classe CA50 e fabricação “barra”. As demais linhas estavam desmarcadas. As linhas CA60 visíveis no cadastro estavam inativas. Não se extraiu a resistência de escoamento, o módulo de elasticidade ou o coeficiente de ponderação do aço a partir do rótulo da classe.

| Elemento | Longitudinais marcadas (mm) | Transversais marcadas (mm) |
| --- | --- | --- |
| Vigas | 8; 10; 12,5; 16; 20 | 6,3; 8; 10 |
| Pilares | 10; 12,5; 16; 20 | 6,3; 8; 10 |
| Lajes | 6,3; 8; 10; 12,5; 16 | 6,3; 8; 10 |

As escolhas coincidiram entre CAD e BIM. A transcrição distingue a bitola oferecida na lista de sua caixa marcada: por exemplo, 6,3 mm aparece como opção longitudinal das vigas, mas está desmarcada; 20 mm aparece como opção longitudinal das lajes, mas está desmarcada. Não se tratou a presença do rótulo como seleção ativa.

A grade Delphi e as listas não expõem adequadamente seus rótulos e marcas na árvore de acessibilidade. Registrou-se, portanto, **transcrição visual do assistente**, acompanhada de imagens e textos nativos. A consolidação compara 80 campos transcritos: classe e estado ativo em 24 linhas, mais 32 estados das listas por elemento e direção. Os 80 pares coincidiram. Essa contagem não significa 80 verificações automáticas de imagem, elementos dimensionados ou validações normativas. Dois testes verificam somente a consistência da transcrição e rejeitam linha ausente, classe ativa divergente ou escolha fora da grade ativa.

Os 35 arquivos fonte R116 mantiveram seus hashes. O PRJ das duas cópias consultadas permaneceu idêntico ao inicialmente copiado. As diferenças de auxiliares estão discriminadas no JSON; incluem o caminho de identificação da própria cópia preparado antes da consulta. Não se extrapola a preservação do PRJ para afirmar identidade de todos os auxiliares.

O cadastro global não comprova exceções por pavimento ou peça, resistência, espaçamentos, estribos, ancoragens e armaduras efetivamente obtidas. Essas verificações continuam vinculadas ao dimensionamento posterior, após completar as cargas. Os custos e fatores de emissão visíveis na grade não foram usados nem validados como dados econômicos ou ambientais da pesquisa.

## Errata de leitura da R100

O texto `h03-r100/LEIA-ME-R100.md` citou 25, 32 e 40 mm entre as bitolas ativas. A releitura das imagens originais **CAD-armadura-inferior.png** e **BIM-armadura-inferior.png** mostra essas três caixas desmarcadas, tal como na consulta R118. Corrige-se aqui a interpretação textual: há seis bitolas ativas, até 20 mm, no cadastro observado. Não se demonstrou alteração do projeto entre as revisões, nem defeito de transferência. Os originais e seus hashes foram preservados; o JSON R118 aponta as fontes da errata. A comparação automatizada de 151 campos da R100 não contava essas linhas visuais e não é ampliada por esta correção.

Os tempos reais de consulta constam de CAD-sessao-tempo.json e BIM-sessao-tempo.json; incluem navegação e evidências, sem inferência IA isolada ou ranking. A fotografia temporal R117 antecede essas medições. Evidências locais: `D:/TCC/outputs/Armadura-H03-R118-CONSULTA-NAO-EXECUTAR/`. As cópias 32 CAD e 33 BIM servem à consulta; os resultados calculados preservados continuam nas cópias 30 CAD e 31 BIM da R116.

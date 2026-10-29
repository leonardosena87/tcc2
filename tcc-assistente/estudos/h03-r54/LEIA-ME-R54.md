# H03/R54 — apoios idealizados da superestrutura

Revisao academica de 29/10/2026, nao dimensionada, nao executar. Partiu-se de copias independentes dos estados congelados R53 em D:\TCC, preservando os dois fluxos e os 42 hashes protegidos do manifesto anterior.

No Eberick 2025 Infinity, selecionaram-se os 11 pilares nascendo em N0 de cada ramo. Aplicou-se Lancamento > Pilares > Converter em pilares de fundacao, com cadastro auxiliar Sapata, apoio Rotulado, altura da barra Fixo 10 cm e profundidade df=0. Esse cadastro permite representar o apoio; nao define nem dimensiona uma sapata real. Nao se adotaram capacidade de suporte, sondagem, recalques ou interacao solo-estrutura.

Ambos os arquivos foram salvos, fechados e reabertos. Foram lidos individualmente tres apoios geometricamente equivalentes em cada ramo:

| Coordenadas de referencia X,Y (m) | CAD | BIM |
|---|---|---|
| 0; 0 | P1 | P8 |
| 9,65; 7,05 | P9 | P3 |
| 6,55; 3,90 | P11 | P6 |

As seis amostras mostraram barra fixa 10 cm, apoio Rotulado, vinculo do pilar Engastado, secao nativa 20 x 30 cm, elevacao zero e df zero. No novo pilar, a rotacao de 90 graus preserva a orientacao 30 cm em X e 20 cm em Y da proposta. Ha um TXT de acessibilidade por leitura e por selecao/parametrizacao. A atribuicao de 11 por ramo foi confirmada pela selecao do lote e pela sequencia da interface; nao se afirma releitura individual dos outros oito de cada ramo. A integridade ZIP dos dois PRJs passou e seus arquivos foram congelados.

O apoio rotulado libera rotacoes e restringe translacoes segundo a definicao do programa. A barra auxiliar de 10 cm faz parte da representacao numerica, portanto nao equivale exatamente a um apoio nodal em N0. Para N0=+0,20 m, a base em +0,10 m e uma inferencia ainda nao conferida no modelo analitico. A sensibilidade ao comprimento da barra e ao vinculo segue pendente, sem garantia de conservadorismo. Excluir cadastros auxiliares e barras abaixo de N0 dos quantitativos comparados da superestrutura.

## Tempos da etapa assistida

| Ramo | Abrir, parametrizar lote, salvar/reabrir e ler 3 amostras |
|---|---:|
| CAD | 12 min 37.827 s |
| BIM | 11 min 8.593 s |

Registro prospectivo UTC e relogio monotonico em JSON. Inclui raciocinio e latencia da interface. CAD inclui localizacao/exploracao de comandos; BIM aproveita procedimento conhecido. Nao mede tempo humano ativo nem inferencia isolada de IA, nao e repeticao controlada e nao permite ranking dos fluxos completos. Complementacao comum de parametrizacao no receptor, nao falha comprovada de transferencia.

Nao se processou calculo, estabilidade ou ELU/ELS. Nao se executou verificacao automatica de lancamento nem nova exportacao IFC nesta revisao; a auditoria pos-conversao da geometria/cargas da superestrutura continua pendente. Nao atribuir a R54 a auditoria IFC realizada na R53. A monografia, RVT e DWG de origem permaneceram inalterados.

Proximo passo: auditoria pos-conversao, releitura complementar dos apoios quando necessaria e cargas de paredes/telhado/tanque/escada/bordas, vento e combinacoes. Manter entradas incompletas como pendencias.

Fontes oficiais consultadas: [vinculo de apoio](https://suporte.altoqi.com.br/hc/pt-br/articles/360012152833), [barra da fundacao](https://suporte.altoqi.com.br/hc/pt-br/articles/115002375753) e [conversao no programa](https://suporte.altoqi.com.br/hc/pt-br/articles/360022925613).

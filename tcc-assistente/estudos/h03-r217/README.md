# H03/R217 — Verificação complementar da V1 do N0

Confrontaram-se os relatórios nativos de combinações CAD e BIM, com 19 casos e 68 combinações em cada documento. Os 14 campos numéricos por registro coincidem na precisão impressa. Reconstruiu-se a grelha de escada R214 para estudar a componente horizontal relacionada ao Aviso 19. A consulta nativa e a geração de relatórios não alteraram os PRJ.

O ensaio de flexão composto fornece índice máximo 0,4583. A sensibilidade com piso vertical de 8 kN.m observado no dimensionamento nativo fornece 0,9670. A calibração de seis momentos verticais por fluxo tem erro máximo inferior a 0,005 kN.m; isso não comprova exatidão horizontal nem identidade integral entre o modelo R214 exportado e o BIM recuperado R215. Os valores são ensaios auxiliares limitados às hipóteses documentadas.

O detalhamento atual, Ø6,3 c/15 cm e dois ramos, não atende à triagem transversal biaxial. O limite longitudinal horizontal calculado é 95,82 mm. A distância entre ramos no plano horizontal é 233,7 mm, acima de 159,7 mm. A hipótese desenhada de Ø6,3 c/9 cm, grampo intermediário e duas barras laterais Ø8 resolve essas duas distâncias no ensaio. **Não foi aplicada ao Eberick e não é detalhe executivo.**

A ancoragem não foi fechada. A triagem conservadora de barra Ø8 reta requer 237,0 mm para uma disponibilidade geométrica nominal de 170 mm. Com fator de gancho, condicionado às exigências normativas, a conta resulta em 165,9 mm, mas a comparação desses comprimentos não comprova distribuição por barra, curvatura, espaço, confinamento ou ligação aos apoios. O estudo preserva essa pendência e não declara aprovação estrutural.

## Artefatos locais

Pasta `D:/TCC/outputs/H03-R217-V1-VERIFICACAO-NAO-EXECUTAR`:

- `R217-verificacao-V1.md`: memória de cálculo, hipóteses, limitações, fontes e critérios de aceitação.
- `R217-resultados.json`: extração nativa, esforços complementares, 68 combinações por fluxo e triagem transversal/ancoragem.
- `R217-V1-revisao-transversal.png`: esquema proporcional inspecionado visualmente.
- `CAD/` e `BIM/`: cópias dos projetos preservados, com identificação na auditoria.
- `R217-integridade.json`: hashes e controle das cópias, fontes e resultados.

O projeto segue limitado à superestrutura e a apoios idealizados. As fundações, contato direto com solo e transferência dos esforços ao terreno não foram verificados. Permanecem o Aviso 19 e as demais pendências da R216. Não se alterou o trabalho acadêmico escrito.

## Reprodução e testes

Python 3.14.7 no ambiente local de ensaio. Dependências em `requirements.txt`; o parser reutilizado está em `../h03-r122/consolidar.py`.

```text
python -m unittest discover -s tcc-assistente/estudos/h03-r217 -p test_verificacao.py -v
python tcc-assistente/estudos/h03-r217/verificar.py D:/TCC/outputs/H03-R217-V1-VERIFICACAO-NAO-EXECUTAR D:/TCC/outputs/H03-R214-INERCIA-BIM-NAO-EXECUTAR
python tcc-assistente/estudos/h03-r217/relatorio.py D:/TCC/outputs/H03-R217-V1-VERIFICACAO-NAO-EXECUTAR
```

Dez testes passaram, incluindo referências analíticas de barras e integração independente da seção. A execução real comparou os documentos e resolveu as duas grelhas. Não se executou SAP2000 nem se reproduziu a análise completa do Eberick. A reconstituição linear e as verificações parciais não validam toda a estrutura.

Norma consultada: exemplar local ABNT NBR 6118:2026, itens 9.4.2.5, 17.2.5, 17.4 e 18.3.3.2. Documentação oficial: [AltoQi — Aviso 19](https://suporte.altoqi.com.br/hc/pt-br/articles/360009988354) e [CSI — eixos de barras](https://docs.csiamerica.com/help-files/sap/Menus/Assign/Frame/Frame_Local_Axes.htm). A norma e os arquivos nativos não são incluídos neste diretório público.

As correções aqui estudadas são comuns aos dois fluxos e não representam falha de interoperabilidade exclusiva de CAD ou BIM. O tempo de cálculo nativo, o intervalo de interação e o esforço de IA permanecem métricas distintas. Não se transforma a duração observada desta revisão em economia de tempo ou tokens consumidos.

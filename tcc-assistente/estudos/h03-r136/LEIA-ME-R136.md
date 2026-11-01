# H03/R136 — análise isolada W20/S58

Processaram-se as cópias 58CAD e 59BIM, derivadas dos lançamentos pareados R135, sem W15 e sem o ensaio W03 de viga inteira. O escopo foi análise estática e deslocamentos do pórtico com rigidez configurada, sem dimensionamento, flechas das lajes, rigidez fissurada ou dinâmica. Ambas terminaram com avisos e foram salvas, fechadas e reabertas antes da exportação do pórtico e das grelhas N1/N2. Não se executou SAP2000.

## Controle e resultados da exportação

O controle próprio de cada ramo corresponde à R116 sem W20, exportada na R132. Conferiram-se os hashes históricos das seis exportações de controle antes da comparação. A geometria mantém IDs, coordenadas e extremos I/J ordenados em todos os modelos: N1 com 467 nós/838 barras, N2 com 443/794 e pórtico com 110/133. Assim, a comparação N1 não confunde a carga com uma mudança de malha.

Na N1, somente JOINT LOADS - FORCE mudou: oito registros G2 acrescentados e nenhum removido. Não havia força nodal G2 no controle. Cada força exportada é −217,8676 kgf, sem componente horizontal ou momento nodal; os oito nós têm X=784,17cm e Y=24,38;73,13;121,88;170,63;219,38;268,13;316,88;365,63cm, em Z=320cm. A distribuição, incluindo os IDs, é igual nos dois ramos. A N2 não apresentou diferença de tabelas.

| Grandeza N1 | CAD e BIM |
|---|---:|
| Soma exportada de Fz | −1.742,9408 kgf |
| Integral nominal sob a convenção exibida R125 | −1.742,9405 kgf |
| Diferença | −0,0003 kgf |
| Centro das forças exportadas | (784,17;195,005) cm |
| Centro ideal da linha gráfica R135 | (810;195) cm |
| Desvio do centro | (−25,83;+0,005) cm |
| Distância entre centros | 25,83000048 cm |
| Mx das forças em relação à origem | −339.882,170704 kgf.cm |
| My das forças em relação à origem | +1.366.761,887136 kgf.cm |
| Mx ideal nominal | −339.873,3975 kgf.cm |
| My ideal nominal | +1.411.781,8050 kgf.cm |

A integral nominal corresponde à hipótese 4,71065kN/m ×3,70m=17,429405kN, sob a convenção de exibição observada na R125 de100kgf/kN; não é conversão SI exata. Como cada força foi escrita com quatro casas, oito arredondamentos ao mais próximo admitem um limite agregado de0,00040kgf. O resíduo de−0,0003 é compatível com essa precisão, mas a causa não foi provada como arredondamento. O código rejeita diferenças maiores; o limite descreve a escrita, não tolerância estrutural.

A distribuição conserva a integral nessa precisão, porém não reproduz os primeiros momentos da linha ideal na exportação N1. Os resíduos nominais são Mx−8,773204 e My−45.019,917864kgf.cm. Não há momento nodal exportado nessa grelha que compense o deslocamento transversal. O lançamento gráfico R135 permanece documentado na posição prevista; não se deslocou ou compensou a linha para forçar igualdade. A origem interna do mapeamento e seus efeitos locais continuam sem demonstração. **A W20 não foi aceita como modelo local final.**

## Pórtico: interpretação condicional

No pórtico mudaram somente FRAME LOADS - POINT (132 registros removidos e132 acrescentados) e JOINT LOADS - FORCE (3/3), todos G2. Esses números são diferenças de registros, não contagem de correções, falhas ou operações.

Reutilizou-se o cálculo auditado na R134: posição de força pontual por rI+t(rJ−rI), preservando I/J, e momento global por r×F+M nodal. As17barras envolvidas são horizontais, sem rotação explícita atribuída; interpretou-se LOCAL/2 como+Z apenas sob a hipótese de eixo padrão SAP. Não se comprovou equivalência dos eixos internos do Eberick nem se importou/executou SAP.

Sob essa hipótese, os dois ramos forneceram: forças pontuais−1.701,9696kgf e incremento nodal global−40,9711kgf; somaFz−1.742,9407kgf, Mx−339.355,454474130 e My+1.368.108,811928166kgf.cm. Contra as forças da N1, permanecem resíduosFz+0,0001kgf, Mx+526,716229870 e My+1.346,924792166kgf.cm. A causa dos resíduos de momento não foi identificada; não se atribui automaticamente a arredondamento, excentricidade, defeito de transferência ou erro do solver. Não são reações de apoio.

Referências da hipótese de eixos, já usadas na R134: [CSI — Frame Local Axes](https://docs.csiamerica.com/help-files/sap/Menus/Assign/Frame/Frame_Local_Axes.htm) e [CSI — Analysis Reference Manual](https://docs.csiamerica.com/manuals/sap2000/CSiRefer.pdf#page=132).

## Resumo visual e tempos

O resumo de ambos exibiu PP75,69tf, adicional12,30tf, acidental17,11tf, Q_TELHADO_MANUTENCAO1,78tf e total106,88tf; área132,81m² e relação804,78kgf/m² com aviso de relação não usual. Contra o controle sem W20 (G10,56tf,total105,14tf), a diferença exibida é1,74tf, compatível com1,7429405tf da integral nominal na precisão mostrada; não substitui a auditoria das forças.

O máximo horizontal exibido permaneceu0,20cm nas quatro direções. O relativo0,17cm conserva direções diferentes (CADN1/Y− e BIMTCC-cdd31967-N1/Y+). O gama-z mostrado foi1,10/1,08/1,06/1,05; X+ aparecia1,09 no controle. A coincidência arredondada1,10 com o limite mostrado não comprova valor interno igual ao limite, atendimento normativo ou segurança. O topo completo não foi transcrito.

| Ramo | Sessão exploratória | Comando até primeira observação do término |
|---|---:|---:|
| CAD | 7.280 min | 50.966 s |
| BIM | 8.016 min | 63.897 s |

O segundo intervalo está contido na sessão e inclui leitura auxiliar, espera e latência; não somá-lo novamente nem tratá-lo como tempo puro do solver. A abertura CAD incluiu navegação e conferência do código do controle; a BIM reutilizou o procedimento e incluiu consultas auxiliares. As sessões não são ensaio prospectivo controlado de produtividade. Não houve intervenção humana registrada. A elaboração posterior de auditoria e relatório não foi cronometrada separadamente. Não se conhece inferência/tokens/custo da IA ou duração final dos fluxos.

As imagens arquivadas correspondem ao estado explicitamente passado à rotina de captura. No resumo, a árvore textual retornada pelo controle ainda descrevia o diálogo anterior; por isso, os números do resumo são transcrições visuais da IA, identificadas em observacoes-visuais.json, sem atribuir a elas extração nativa. A auditoria das tabelas usa os próprios arquivos$2k.

## Preservação e continuidade

Preservaram-se os35arquivos das fontes R135. As cópias R136 foram congeladas após processamento com hashes de todos os arquivos no JSON. A referência R116 e os lançamentos R135 continuam separados. Não houve edição da monografia, dos modelos de autoria RVT/DWG ou nova transferência DWG/IFC.

Esta etapa comprova a mesma resposta exportada dos receptores para a hipótese W20 isolada, com desvio local documentado. Não estabelece convergência de malha, tolerância de momentos, reações locais, capacidade resistente, verificação completa ELU/ELS ou superioridade de um fluxo. O passo seguinte é estudar malha mais fina/alinhada e controle equivalente, além de rever altura atual, composição e apoios. As demais paredes, aberturas, escada, reservatório/base/acesso, vento e combinações permanecem no quadro de pendências. Não há liberação para execução.

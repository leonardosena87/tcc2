# H03/R130 — linha W15 sobre laje

A hipótese W15 foi lançada em cópias independentes dos dois ramos: CAD 44 e BIM 45, derivadas da R116. Trata-se de complementação no receptor Eberick, e não de carga transferida automaticamente de DWG/IFC.

| Item | CAD | BIM |
|---|---:|---:|
| Carga extra relida após salvar/fechar/reabrir | 4,695 kN/m | 4,695 kN/m |
| Carga de parede adicional do comando | 0 | 0 |
| Início gráfico em coordenadas do modelo | (450;495) cm | (450;495) cm |
| Término gráfico em coordenadas do modelo | (545;495) cm | (545;495) cm |
| Extensão | 0,95 m | 0,95 m |
| Sessão exploratória | 8.813 min | 8.741 min |

A intensidade resulta da hipótese 1,565 kN/m² × 3,00 m. A integral prevista é 4,46025 kN; **não é reação calculada**. A composição da vedação continua hipótese sem confirmação de fabricante. Não há vão na faixa W15 da matriz R120.

O comando foi configurado com Parede desmarcado, ação Adicional e definição por dois pontos. O total exato 4,695 foi relido nativamente após reabertura. A grade de ações, inspecionada antes de salvar, exibiu Adicional 4,70 e outras cinco ações 0,00, na precisão de duas casas.

Os DXFs de croqui reaberto contêm uma única linha e um único rótulo no nível CR-Paredes. Os extremos brutos coincidem em (9;9,9) e (10,9;9,9). A escala gráfica 1:50 foi conferida por três centros de pilares de referência, com tolerância de 10⁻⁹ unidade gráfica apenas para resíduos numéricos da escrita. A coordenada Z=0 do DXF pertence ao desenho plano, não ao nível físico N1. O rótulo 4,70 é arredondado; o valor nativo permanece 4,695.

Preservaram-se os hashes de 35 arquivos R116. Os PRJs experimentais foram alterados pelo lançamento e permaneceram iguais aos hashes capturados após salvar durante a consulta e exportação. Não se editou monografia, RVT ou DWG de autoria.

**Não houve processamento nesta etapa.** A geometria gráfica e o valor persistido não comprovam a distribuição analítica na grelha, as reações, a capacidade resistente ou o atendimento a ELU/ELS. A R130 não incorpora o ensaio W03 de viga inteira da R121. A referência R116 continua preservada; as cópias R130 são ensaios parciais.

Os tempos incluem abertura, configuração, entrada, releitura, salvamento, reabertura, exportação e capturas. O CAD incluiu pesquisa e consulta extra de desenho; o BIM reutilizou o procedimento aprendido. Não constituem ranking nem economia percentual; os tempos finais dos fluxos permanecem abertos.

Próximo passo: análise isolada da W15 nos dois ramos, com conferência de integral e caminho de carga, antes de ampliar o lançamento às outras paredes. Procedimento consultado: [AltoQi — carga linear](https://suporte.altoqi.com.br/hc/pt-br/articles/360058309854).

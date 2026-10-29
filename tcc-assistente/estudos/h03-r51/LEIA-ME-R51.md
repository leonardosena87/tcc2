# H03/R51 — parâmetros globais conferidos nos dois receptores

**Estudo não dimensionado — não executar.** A monografia não foi alterada. Os projetos R49/CAD e R50/BIM permanecem preservados; a conferência ocorreu em cópias independentes R51.

## Operação real e resultado

Acessou-se no Eberick 2025 Infinity `Estrutura > Configurações > Projeto > Materiais e durabilidade`, com aplicação ao projeto inteiro. A classe C25, agressividade II e cobrimentos nominais de 2,5 cm para lajes e 3 cm para vigas/pilares da superestrutura já apareciam nos dois ramos. Consultou-se o cadastro da classe C25, sem confundir a seleção inicial C20 da lista com a classe atribuída aos elementos.

Efetuaram-se quatro alterações de campo por ramo:

| Campo | Antes | Depois |
|---|---|---|
| Dimensão do agregado | 19 mm | 25 mm |
| Abatimento nominal C25 | 5 cm | 10 cm |
| Família de cimento C25 | CP-IV | CP-II |
| Bitola global 5 mm CA60 ativa | Sim | Não |

Não se atribuem essas diferenças a defeito de intercâmbio. A procedência dos parâmetros globais não foi demonstrada por transferência IFC/DWG; trata-se de adequação das entradas no receptor às premissas comuns. A lista de aços observada continha CA50 nas bitolas ativas de 6,3, 8, 10, 12,5 e 16 mm; o ramo BIM também teve a linha de 20 mm e os seletores de bitolas por elemento examinados. O cadastro mecânico completo do aço ainda não foi conferido.

Salvou-se, fechou-se e reabriu-se cada projeto. A leitura posterior confirmou agregado de 25 mm, C25 com abatimento 10 cm e cimento CP-II, cobrimentos e CA60 de 5 mm inativa. A leitura da classe C25 mostrou fck=25 MPa, coeficiente 1,4, fcd=17,86 MPa, Eci=28.000 MPa, Ecs=24.150 MPa, peso específico de 25 kN/m³ e agregado granito. Os valores de tração exibidos foram registrados com o arredondamento da interface, sem substituir as fórmulas/documentação por números arredondados.

## Limites

O campo de cimento não distingue CP-II-E; a especificação de subtipo E permanece como premissa documental. O campo de abatimento observado aceita um valor nominal; a tolerância ±2 cm não foi registrada em campo próprio. A escada com 6±2 cm precisa de tratamento específico quando modelada. Nenhuma fundação real foi dimensionada, e os campos de contato com o solo não foram adequados nesta etapa, pois o escopo é a superestrutura.

O tipo granito foi mantido no cadastro e é coerente com o módulo já adotado, mas não foi verificado por caracterização de material real. Custos e carbono do cadastro são valores não auditados e não podem ser apresentados como resultados econômicos ou ambientais. Cobrimentos observados não equivalem a certificação normativa; devem integrar a conferência do projeto completo e da norma aplicável.

## Tempos e evidências

O intervalo BIM abrange preparação da cópia, leitura, alterações, salvamento e reabertura: **9 min 58,707 s** assistidos. O intervalo CAD iniciado anteriormente em 29/10/2026 às 01:45:48,368 UTC foi interrompido sem encerramento monotônico persistido; sua duração é desconhecida. A retomada CAD foi medida separadamente: **5 min 48,833 s**, começando no diálogo de armaduras já aberto e terminando após salvar/reabrir e conferir. Os escopos diferem; não se calcula vantagem percentual nem tempo total de fluxo.

Incluem-se latência de ferramentas/IA e recuperação de foco; não há medição isolada do esforço cognitivo ou inferência da IA. Consultar os JSONs de tempo. Foram congelados oito arquivos BIM e cinco CAD. `R51-parametros-BIM.json` e `R51-parametros-CAD.json` contêm valores observados, alterações, caminhos e hashes. Os scripts de preparação não sobrescrevem pastas existentes. O congelamento pode ser repetido apenas enquanto o estado nativo continuar idêntico; alterações seguintes ficam na R52.

A evidência da leitura é a sequência de operações reais da interface registrada na sessão, junto dos arquivos nativos e relato estruturado; não foram salvas capturas separadas em disco. A geometria após esses ajustes foi controlada nas exportações posteriores R52, sem usá-las para inferir parâmetros de materiais.

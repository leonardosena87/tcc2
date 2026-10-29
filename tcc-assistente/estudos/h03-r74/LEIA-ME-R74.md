# H03/R74 — triagem normativa parcial e versão do Eberick

NÃO DIMENSIONADO. NÃO EXECUTAR. A auditoria usa o exemplar local ABNT NBR6118:2026 e a geometria nominal ortogonal já conferida R56, com preservação R57. Não substitui cálculo, detalhamento ou comprovação de atendimento integral. Nenhum projeto de engenharia ou monografia foi alterado.

## Versão efetivamente instalada

Consultou-se Ajuda→Sobre no aplicativo real, sem projeto aberto: **Eberick2025-04 [v.18.306], Infinity**. A leitura e a identificação UTC estão nos arquivos R74-versao*. Não foi inferida a versão só pelo título2025. Os metadados FileVersion/ProductVersion do executável consultado vieram vazios; essa fonte não foi usada para inventar um número.

A AltoQi informa que a atualização2026-08 incorpora o limite único de redistribuição0,75 da Emenda1:2026, retirando a diferenciação por nós fixos/móveis nessa verificação. A publicação não comprova que a instalação2025-04 já implemente esse critério. [Comunicado oficial de17/09/2026](https://suporte.altoqi.com.br/hc/pt-br/novo-conhe%C3%A7a-a-atualiza%C3%A7%C3%A3o-2026-08-do-altoqi-eberick).

No exemplar local, item14.6.4.3, confirmou-se o limiteδ≥0,75. Para C25, o limite geral de posição relativa da linha neutra é x/d≤0,45; se houver redistribuição, existe condição adicional em função deδ. Não se obteveδ ou x/d dos elementos processados nesta sessão e não se concluiu aprovação de redistribuição. Também não se afirmou que toda a instalação antiga é incompatível: registrou-se precisamente o atendimento que permanece não comprovado.

Não se instalou atualização, entrou em conta/licença ou migrou arquivo automaticamente. Antes de usar resultados finais como atendimento à edição2026, conferir implementação dos critérios aplicáveis ou registrar verificações complementares documentadas. Manter a mesma versão e os mesmos critérios nos dois ramos durante o ensaio pareado; uma futura migração precisa de novo checkpoint.

## Limites geométricos conferidos

Por ramo, examinaram-se22 trechos de pilares,32 sólidos de vigas e11 lajes. Os32 sólidos continuam correspondendo a29 vigas lógicas.

| Verificação limitada | Geometria do checkpoint | Resultado desta triagem |
|---|---|---|
| Pilar: menor dimensão geral≥19cm e área≥360cm², item13.2.3 | Menor dimensão20cm, área600cm² |22/22 por ramo atendem esses dois limites |
| Viga ordinária: largura geral≥12cm, item13.2.2 | Largura20cm |32/32 sólidos por ramo atendem só a largura |
| Laje maciça: espessura mínima pela classificação, item13.2.4.1 |14cm; piso/cobertura/balanço distinguidos |11/11 por ramo atendem só a espessura mínima |

Inferiu-se a largura pela menor extensão XY das caixas dos elementos ortogonais previamente auditados; esse procedimento não vale automaticamente para vigas oblíquas, curvas ou seções variáveis. Área e largura mínimas de pilares não verificam esbeltez, armadura, flexocompressão ou instabilidade. Não existe um mínimo genérico de altura30cm de viga deduzido dessas regras; a altura adotada exige resistência e deformações. A largura20cm também continua maior que a parede acabada15cm, pendência de faces/arquitetura.

## Varanda14cm: coeficiente adicional1,25

A laje da varanda N1 foi identificada pela caixa em X9,75..10,725m e topo+3,20m, nos dois ramos. A tabela13.2, conferida visualmente na página76/PDF94 do exemplar, conduz aγn=1,95−0,05×14=**1,25**. O mínimo geométrico10cm para laje em balanço não elimina essa exigência adicional.

O coeficiente majora os esforços solicitantes finais de cálculo ao dimensionar a laje em balanço. Não se aumenta25% o peso de toda a edificação, nem se aplica novamente sobre resultado já majorado internamente. A continuidade atribuída R52 e a geometria IFC não demonstram que o dimensionamento nativo aplicouγn. Essa leitura deve ser feita nos resultados/configurações apropriados após completar ações e processar dimensionamento. O campo de verificação permanece falso/desconhecido, sem lançar carga artificial.

## Brita25mm e espaço de armadura: exemplo de sensibilidade

O item18.3.2.2 relaciona o espaçamento horizontal livre ao maior valor entre20mm, diâmetro da barra/feixe/luva e1,2vez o agregado máximo. Com agregado25mm e barra hipotética16mm, a triagem exige30mm. Para uma viga de200mm, cobrimento nominal30mm e estribo HIPOTÉTICO de6,3mm, a largura interior nominal disponível entre faces internas do estribo seria127.4mm.

| Barras hipotéticas16mm numa camada | Espaçamento livre resultante (mm) | Atende somente este critério horizontal nominal? |
|---|---:|---|
| 2 | 95.400 | sim |
| 3 | 39.700 | sim |
| 4 | 21.133 | não |

O exemplo explica por que largura mínima aprovada não garante acomodação: quatro barras16mm nessa única camada não atendem essa triagem, enquanto três atendem apenas a condição nominal examinada. Não se selecionou armadura ou estribo por esse cálculo. Tolerâncias, curvaturas, emendas, cruzamentos, ancoragens, espaço vertical, execução, fissuração e resistência continuam fora da verificação. As bitolas são hipóteses do exemplo; não são barras observadas ou lançadas no nativo.

## Registro para os resultados

Mantiveram-se separados: critério normativo consultado; dado efetivamente presente no modelo; regra implementada pelo auditor; e resultado nativo não verificado. O JSON/CSV contém130 registros,65 por ramo, sem pontuação global de conformidade. O complemento da matrizR72 acrescenta aceite explícito paraγn, versão normativa e detalhamento, sem reescrever o checkpoint anterior. O PDF protegido e as imagens da norma ficaram fora do repositório público.

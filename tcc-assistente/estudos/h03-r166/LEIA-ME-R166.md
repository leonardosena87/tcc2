# R166 — níveis estruturais e comparação geométrica dos receptores corrigidos

Experimento de 02/11/2026, sem alteração do trabalho escrito ou do projeto principal calculado.

## Variante derivada e recepção real

Partiu-se da variante IFC R164. Mantiveram-se somente os três níveis estruturais N0=0,20 m, N1=3,20 m e N2=6,39 m. A escada foi atribuída ao N0 e a viga do patamar ao N1, preservando suas posições mundiais. Os seis níveis auxiliares foram removidos da organização espacial desta variante; não se alteraram as cotas arquitetônicas. Foram preservadas, após escrita e reabertura, as nuvens de pontos dos 68 elementos com malha, além das identidades, propriedades e materiais. A validação de esquema permaneceu sem ocorrências.

O arquivo é **explicitamente derivado**, não uma nova exportação nativa do Revit. A escada conserva a base virtual de 0,17 m; essa organização não resolve seu apoio inferior. As propriedades mecânicas ausentes no IFC bruto também não foram recompostas.

No Eberick, criou-se `R166-R160-3NIVEIS-CONFIG-CAD-NAO-EXECUTAR`, escolhendo **Configuração do último projeto aberto**, que era a cópia CAD R165. Isso muda dois fatores em relação à R164 — organização de níveis e origem da configuração. Não se atribuiu o resultado exclusivamente à retirada de níveis. O assistente mostrou os três pavimentos, com níveis 20/320/639 cm. A altura inicial de 100 cm apresentada para N0 é dado do assistente, sem dimensionamento de fundação.

O relatório nativo registra 52 origens únicas: 30 vigas e 22 segmentos de pilares. O IFC4 de controle contém 33 peças de vigas, 22 de pilares e nenhuma laje/escada nativa. O controle exporta dois IfcBuildingStorey, N1 e N2, que contêm os elementos exportados; o croqui nativo conserva os três pavimentos. A contagem de peças não equivale à contagem de pilares físicos.

A viga do patamar aparece como V6, seção preliminar 20×30 cm e elevação **−142,6 cm** em relação ao N1. O topo exportado é 1,774 m, diferença de −0,117647 mm em relação à autoria. A tolerância computacional dessa comparação foi declarada separadamente: 0,1 mm em eixos/seções e 0,2 mm no topo. Não são tolerâncias normativas ou aprovação da seção.

O painel nativo de materiais mostrou C25, CAA II e agregado de 25 mm. Esse registro decorre da configuração herdada do CAD; **não comprova transferência dessas propriedades pelo IFC** nem igualdade de todas as configurações entre os receptores. O PRJ foi salvo, fechado e reaberto, mantendo o primeiro hash salvo `babfb4a5777e72f02957fc74d1123ec7776ceafd76b320c403daabd84712038f`.

## Comparação CAD R165 versus BIM R166

Associaram-se as 46 peças de vigas CAD e as 33 BIM às mesmas 30 origens nominais da autoria R160. As projeções nos vãos fora das regiões ocupadas pelos pilares ficaram iguais dentro da precisão declarada; as caixas/seções/topos cumprem o critério geométrico de associação. Os intervalos verticais das 22 origens de pilares ficam cobertos em ambos os receptores.

Essa comparação se refere aos **receptores corrigidos**, incluindo preparação de IFC derivado e correção CAD. Não transforma o resultado em qualidade do intercâmbio bruto. O ramo CAD contém 11 lajes nativas, enquanto o BIM ainda não contém lajes ou escada nativas. A paridade de cargas, vínculos e configuração ainda não foi demonstrada. Não se validou conectividade analítica, ELU/ELS, dimensionamento, tempo total ou vantagem entre fluxos.

## Tempos e validação

- Preparação, escrita, reabertura e conferência da variante de níveis: **1.917,6358 ms**. Exclui desenvolvimento, pesquisa e operação do receptor.
- Seleção do IFC até observação após Salvar: **171.590 ms = 2min51,590s**, incluindo escolha da configuração CAD, foco e planificação. Exclui preparação da variante e auditorias posteriores. Não representa o fluxo BIM completo.
- Seis testes sintéticos Python R166: quatro guardas de redistribuição espacial e dois critérios de associação geométrica. Releitura dos IFCs e relatórios é evidência distinta dos testes de código.

## Continuidade

PRJ receptor: `D:\TCC\outputs\R166-R160-3NIVEIS-CONFIG-CAD-NAO-EXECUTAR\Projeto Eberick\R166-R160-3NIVEIS-CONFIG-CAD-NAO-EXECUTAR.prj`.

Resultados principais: `R166-derivado-conferencia.json`, `R166-recepcao-auditoria.json` e `R166-comparacao-geometrica-CAD-BIM.json`. Capturas dos níveis, configuração, croqui, V6, materiais e reabertura acompanham os registros. O IFC4 de controle está em `Arquivos do projeto\Modelo 3D.IFC` do receptor.

Prosseguir em nova cópia para lajes, escada, cargas e vínculos. Permanecem o apoio inferior, interferência V16/J4 e verificações estruturais. Preservar controles R161/R162/R164/R165 e a variante R166. Nenhum cálculo novo foi executado nesta etapa.

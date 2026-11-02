# H03/R142 — referência vertical da base do reservatório

**Compatibilização parcial; não executar em obra.** O corte BB permite estimar o topo da base desenhada do reservatório em **aproximadamente +6,81 m**, na mesma referência das cotas de piso da arquitetura. Essa estimativa esclarece a relação vertical, mas não define a plataforma ou seu apoio.

## Como a referência foi obtida

Preservou-se o PDF arquitetônico com SHA-256 `3a57561f03e2c0e92964b19e577a02939b04fc93cdf1ef27cad6f79ad2deb12d`. Conferiu-se visualmente o corte e localizaram-se, nos vetores do PDF, a seta do nível do banheiro **+3,24 m**, sua ponta na ordenada PDF 2018,71997, e a base superior do reservatório na ordenada 1816,40002. A escala vertical é a mesma calibrada na R112 pela dimensão de 1,30 m até o topo da platibanda: aproximadamente 56.677 unidades PDF por metro. Texto e segmentos das setas são verificados pelo script, sem OCR.

A conversão usa `z_alvo = z_referência + (y_referência − y_alvo) / escala`, pois o eixo vertical da página cresce para baixo. O banheiro resulta em 6.809703 m; a conferência independente pelo quarto +3,25 m resulta em 6.807000 m. A diferença entre as leituras é aproximadamente 2.7 mm. Essas casas adicionais servem à auditoria aritmética; a informação de projeto é expressa como **aproximadamente +6,81 m**, sem precisão executiva. O limite interno de 5 mm apenas rejeita uma associação gráfica incompatível neste script; não é tolerância construtiva ou normativa.

O traço superior da laje arquitetônica usado como origem do ressalto local fica em aproximadamente **+6,21 m**. A diferença desenhada até a base é 0.601 m, coerente graficamente com a indicação de 0,60 m. Logo, a dimensão de 0,60 m é relativa a esse traço arquitetônico, não automaticamente ao N2 estrutural.

## Relação com a referência estrutural

As duas exportações analíticas N2 da R138 contêm 443 nós em Z = 639,00 cm e declaram unidades `Kgf, cm, C`. Assim, o plano de referência exportado é **+6,39 m** nos dois ramos. Não se executou SAP2000 e não se reabriu o N2 nativo nesta etapa.

Admitindo o mesmo datum vertical do estudo, a base arquitetônica estimada fica cerca de **0,42 m acima do plano N2**. Usar N2 +0,60 m levaria a +6,99 m, aproximadamente **0,18 m acima da base desenhada**, alterando a folga sob o telhado. Essa diferença não foi classificada como defeito de transferência, pois compara uma referência arquitetônica com o plano analítico de uma hipótese estrutural revisada.

O valor de 0,42 m **não é a altura calculada de um pedestal**. Para definir pedestal/plataforma ainda se deve relacionar o plano analítico às faces físicas, selecionar espessura e materiais, verificar apoio contínuo e calcular as ações e reações. Nenhuma espessura ou tara desconhecida foi preenchida como zero.

## Consequência para continuar o estudo

A ambiguidade da referência vertical foi reduzida: passa-se a dispor de uma cota aproximada extraída do corte para o topo de apoio. Essa cota deve ser confrontada com a geometria física atual antes de qualquer lançamento. A R112 já mostrou que a referência retangular baixa não satisfaz a reserva superior de estudo de 0,60 m, mesmo antes de definir perfis. Esta etapa não muda esse resultado nem aprova manutenção ou retirada da tampa.

A [página oficial da Bakof](https://www.bakof.com.br/produtos/4) foi reconferida: a referência de 1.000 L mantém dimensões superiores de 1,88 × 1,23 m e altura de 0,68 m. Ela permanece apenas referência dimensional; não se selecionou produto para compra e não se confirmou tara. Não se alterou a cobertura, a base, os pisos, o forro, os arquivos Revit/AutoCAD/Eberick ou a monografia.

Próxima decisão técnica: definir uma solução de acesso/tampa e o apoio físico com topo próximo da cota arquitetônica documentada, preservando as alturas. Depois verificar peso completo, casos cheio/vazio, reações e dimensionamento nos dois receptores. A referência absoluta vem do datum do desenho, sem levantamento de implantação ou vínculo geodésico.

## Tempo e verificação

O arquivo R142-tempo-script.json mede somente a execução do extrator e relatório, não pesquisa, autoria, leitura visual ou inferência da IA. Não integra os tempos finais CAD/BIM. Os hashes do PDF, do estudo R112 e das exportações de referência estão no JSON; os arquivos foram somente lidos. O estudo permanece parcial.

# Resultados consolidados do estudo de caso — fechamento R219

## Desenvolvimento e qualidade da informação

Investigou-se a aplicação de dois fluxos automatizados ao desenvolvimento preliminar da superestrutura de uma residência unifamiliar: representação CAD 2D com reconstrução no Eberick e modelagem Revit com intercâmbio IFC para o mesmo ambiente de cálculo. O estudo considerou concreto C25, aço CA-50, laje maciça e paredes cerâmicas com espessura acabada de 15 cm. A ausência de investigação geotécnica delimitou o dimensionamento à superestrutura, com apoios idealizados explicitados nos registros.

Na auditoria histórica de chegada ao Eberick, registrou-se no fluxo CAD a preservação de 62 contornos e 66 conteúdos de texto como referência gráfica. Nesse recorte, a referência não forneceu unidades estruturais nativas calculáveis, exigindo reconstrução de 62 unidades lógicas. No fluxo BIM, após o tratamento documentado do IFC, identificou-se a disponibilidade de 22 trechos de pilar e 29 vigas lógicas nativos, totalizando 51 das 62 unidades previstas, ou 82,26%. A complementação correspondeu às onze lajes ausentes como elementos nativos. O tratamento BIM também envolveu 17 registros geométricos e a remoção de dois pavimentos vazios (registro R90).

Essa disponibilidade inicial indica maior reaproveitamento semântico no recorte BIM estudado. Não representa taxa geral de conformidade, redução de 82,26% do trabalho ou contagem de defeitos. A reconstrução no CAD e a complementação no BIM possuem naturezas diferentes; uma unidade lógica também não equivale a uma operação ou a um intervalo de tempo. A correção comum de materiais e premissas não foi atribuída a perda de intercâmbio sem comprovação do dado na origem.

## Compatibilização e modelo analítico

Na auditoria R212 das exportações analíticas, verificou-se coincidência das coordenadas e dos segmentos sem orientação I–J nos quatro conjuntos examinados: pórtico com 148 nós e 183 barras; escada com 298 nós e 389 barras; grelha N1 com 473 nós e 844 barras; e grelha N2 com 443 nós e 794 barras. A coincidência geométrica não demonstrou identidade integral das cargas, dos vínculos e do comportamento estrutural.

Na grelha N1, registrou-se I33 de 20.000 cm⁴ no CAD e 18.540 cm⁴ no BIM em três segmentos de seção nominal 30 × 20 cm, diferença de −7,3% em relação ao CAD. O controle R214, com exportação de propriedades genéricas e posterior regeneração do BIM, conservou essa divergência. A investigação não demonstrou sua causa. Por esse motivo, não se atribuiu a diferença automaticamente ao IFC, à IA ou a um defeito do programa, nem se alterou a exportação para produzir igualdade artificial.

O desenvolvimento da escada, a revisão de seus apoios, a retirada da janela J4 e as intervenções nas vigas e pilares constituíram revisões de concepção e compatibilização ao longo do estudo. A R218 incorporou quatro barras laterais Ø8 à V1 do N0 nos dois modelos Eberick, com retenção confirmada após fechar e reabrir os arquivos. O complemento externo associado ao N0 registra estribos Ø6,3 com espaçamento máximo de 9 cm e dois grampos por posição. O cálculo automático conserva estribos de 15 cm, e sua relação de aço não incorpora o complemento externo. Permanecem pendentes as ancoragens e a verificação final dos detalhes.

O diagnóstico histórico R212 apresentou, no N1, três elementos de escada, seis lajes e doze pilares com sucesso em cada fluxo. O agrupamento de vigas diferiu entre os ramos, impedindo interpretar diretamente a contagem de grupos como número de elementos físicos ou de erros. Esse diagnóstico pertence à revisão indicada e não substitui uma inspeção integral da R218. A existência de grupos calculados com sucesso também não elimina os avisos de flexão oblíqua, inversão de esforços ou ancoragem.

## Tempos observados

| Cenário | CAD (s) | BIM (s) | Alcance da medição |
|---|---:|---:|---|
| R196 — W08 integral | 7 | 7 | Processamento nativo; uma execução por fluxo |
| R201 — ELS fissurado e dimensionamento selecionado herdado | 9 | 9 | Escopo de dimensionamento distinto do integral |
| R205 — ELS fissurado e dimensionamento integral | 10 | 10 | Processamento nativo; uma execução por fluxo |
| R207 — W08 corrigida | 10 | 11 | BIM ainda apresentava D16; estados finais diferentes |
| R211 CAD / R210 BIM — revisão de concepção | 9 | 9 | Revisões distintas e agrupamento de vigas diferente |
| R215 — controle após recuperação | Não registrado | 10 | Controle apenas BIM |

Os registros nativos mostraram tempos iguais nos cenários R196, R201 e R205, na resolução disponível e sem repetição suficiente para análise estatística. A diferença de um segundo na R207 ocorreu com estados finais diferentes e não permite concluir vantagem de produtividade. Esses tempos incluem o escopo de processamento registrado, com elementos de fundação fora do dimensionamento autorizado do TCC, e não medem o desenvolvimento completo da superestrutura. Não se somou o tempo parcial de dimensionamento ao total que já o contém.

O inventário R216 também preservou intervalos de interação, como 250,900 s na edição BIM R207, 1.241,641 s na revisão CAD R211 e 399,739 s em parte da revisão CAD R213. Esses intervalos possuem tarefas, limites e condições diferentes e incluem navegação, espera, captura e raciocínio. Não constituem pares comparáveis. O intervalo R218 atravessou interrupção entre sessões e não recebeu duração total inferida.

Consequentemente, o tempo total de cada fluxo, o esforço exclusivo de inferência da IA, os tokens, o custo e o retrabalho final comparável permanecem não determinados no experimento principal. Não se substituiu dado ausente por zero. A discussão de produtividade utiliza apenas os tempos efetivamente registrados e seus limites, sem estimativa retrospectiva de economia percentual.

## Síntese interpretativa e limitações

O estudo demonstrou a aplicação local das automações e a possibilidade de auditar diferenças entre representação gráfica, informação semântica e modelo analítico. O fluxo BIM apresentou maior disponibilidade inicial de elementos nativos no recorte documentado, enquanto o fluxo CAD exigiu reconstrução a partir de referência gráfica. A evidência disponível não demonstrou superioridade global de qualidade, menor tempo total ou menor número final de correções de um dos fluxos.

A aplicação da IA apoiou geração de rotinas, operação assistida dos programas, extração, comparação e documentação. A intervenção humana permaneceu necessária em decisões de concepção, autorizações de carregamento e operações de interface. A automação não comprovou autonomia integral nem substituiu a revisão técnica.

O objetivo de desenvolver e aplicar os fluxos foi atendido parcialmente nas etapas documentadas. O objetivo comparativo recebeu resultados iniciais de interoperabilidade e tempos nativos, mas permaneceu incompleto quanto à produtividade total e ao retrabalho final. Limitou-se a investigação a uma edificação, às revisões e configurações preservadas e a apoios idealizados. A pendência de ancoragens, de apoio e compatibilização e de sincronização dos arquivos de autoria impede declarar o conjunto como projeto executivo concluído.

### Rastreabilidade

Síntese elaborada a partir de R90 (qualidade inicial), R212 (diagnóstico e auditoria analítica), R214 (controle de inércia), R216 (consolidação das medições), R217 (verificação complementar da V1) e R218 (aplicação da pele e complemento externo). Trata-se de texto de apoio para adaptação ao trabalho escrito; as remissões Rxxx identificam registros do experimento, não substituem referências bibliográficas ou normativas do TCC.

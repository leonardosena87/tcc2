# H03/R50 — onze lajes complementadas no receptor BIM

**Estudo não dimensionado — não executar.** Esta revisão atua no projeto de engenharia, sem alterar a monografia.

## Resultado observado

No AltoQi Eberick 2025 Infinity, complementaram-se dez lajes internas e uma laje de varanda em cópia independente do receptor BIM R46. O projeto contém 22 trechos de pilares, 29 vigas lógicas representadas por 32 sólidos e 11 lajes maciças preliminares de 14 cm. O projeto nativo é `D:/TCC/outputs/H03_BIM_R50_LAJES_NAO_EXECUTAR/Projeto Eberick/H03_BIM_R46_IFC_NAO_EXECUTAR.prj`. O nome-base R46 foi mantido para os caminhos relativos dos recursos; a pasta e a associação da edificação identificam a R50.

As verificações inicial e após fechar/reabrir/reexportar confirmaram, nos critérios implementados, posição, seção e cotas de pilares/vigas, além de caixas envolventes e áreas superiores trianguladas das onze lajes. Os 65 sólidos conservaram classes, nomes, GUIDs, caixas envolventes e áreas superiores na reabertura. Não houve ausência ou duplicação detectada. Controles sintéticos detectaram retirada, duplicação e alteração de altura de laje; esses controles são testes do auditor, separados da operação real no Eberick.

A varanda nativa L6 no N1 recebeu três barras de largura nula para delimitar os bordos livres: (975;380), (1072,5;380), (1072,5;710), (975;710), em centímetros. O sólido resulta em 3,2175 m², medidos desde a face externa da viga em x=9,75 m. Essa área líquida difere da área nominal entre eixos da proposta. O vínculo/engastamento do balanço ainda não foi configurado ou verificado nesta etapa; o contorno não comprova estabilidade.

## Comparação geométrica com o CAD

O IFC reaberto da R49/CAD e o IFC reaberto da R50/BIM coincidiram no conjunto de classes, caixas envolventes e áreas superiores dos 65 sólidos, incluindo a multiplicidade. A comparação não depende de igualdade de nomes ou GUIDs entre os fluxos. As auditorias individuais conciliam os elementos com a proposta comum H03/R43.

Esse resultado permite prosseguir à comparação das informações e do modelo analítico. Não comprova igualdade de malhas completas, vínculos, materiais, carregamentos ou comportamento estrutural. A numeração nativa dos elementos difere entre os ramos.

## Tempos delimitados

| Ramo e operação | Tempo observado | Limite de interpretação |
|---|---:|---|
| BIM/R50: abertura da cópia, dez lajes internas, salvamento, exportação e auditoria | 11 min 19,697 s | Exclui preparação anterior, varanda e reabertura |
| BIM/R50: três bordos e laje da varanda, salvamento, exportação e auditoria | 3 min 13,001 s | Exclui as dez lajes e a conferência posterior de persistência |
| BIM/R50: salvar, fechar/reabrir, reexportar e conferir persistência | 1 min 33,101 s | Verificação separada do lançamento |
| CAD/R49: complementação e auditoria inicial das onze lajes | 24 min 03,725 s | Intervalo bruto interrompido; não equivale a tempo ativo |
| CAD/R49: conferência de persistência por reabertura/reexportação | 3 min 15,201 s | Etapa assistida delimitada |

Os cronômetros das três etapas BIM foram iniciados prospectivamente e usam duração monotônica, com início/fim UTC nos JSONs. Cada intervalo inclui interação com a interface, latência das ferramentas/IA e preparação/execução da auditoria correspondente. O tempo de raciocínio ou de inferência da IA não foi medido isoladamente. Houve recuperação de foco durante a varanda; não se trata de repetição controlada. O congelamento documental entre etapas e esta consolidação ficam fora desses intervalos.

As linhas não cobrem os fluxos completos e têm escopos/condições distintos. Não somar para declarar tempo total de fluxo nem calcular percentual de vantagem. A comparação de produtividade requer os ciclos equivalentes previstos no protocolo H03.

## Qualidade das informações e pendências

O IFC exportado identifica os 65 materiais apenas como `Concreto`; esse nome não comprova C25, CA-50, CAA II ou cobrimentos. É necessária a conferência dos parâmetros nativos nos dois receptores. Os campos de cargas das lajes permaneceram sem preenchimento nesta etapa; o zero exibido não representa hipótese de carga nula aprovada.

A validação de esquema do IFC4 encontrou oito erros em listas opcionais vazias de identificação/endereços. O arquivo nativo exportado foi preservado sem reparo silencioso. Esses erros de esquema são distintos da auditoria geométrica e da verificação estrutural.

Permanecem pendentes: vínculo do balanço, conectividade analítica, materiais/cobrimentos, cargas de uso e permanentes, paredes, escada, guarda-corpo, telhado/forro, posição e apoio do reservatório de 1.000 L, vento/combinações e apoios idealizados da superestrutura. Só após completar as entradas cabe processar e avaliar ELU, ELS e estabilidade. Não há dimensionamento de fundações sem sondagem.

## Preservação e reprodução

`congelado-dez-lajes` preserva o estado intermediário e `congelado-onze-lajes` preserva o estado completo desta etapa, cada um com dez arquivos nativos/de apoio. Os arquivos IFC das três exportações estão separados. A auditoria parcial deve ser lida contra `R50-dez-lajes.ifc`; o caminho `Modelo 3D.IFC` registrado inicialmente naquele JSON era o arquivo de trabalho antes de evoluir.

`R50-estado-atual.json` registra o estado mais recente; `R50-preparacao.json` e a auditoria de dez lajes são históricos. A consolidação confirmou os hashes de 105 arquivos protegidos dos manifestos R46 e R49/persistência. Não se realizou teste de portabilidade em outra máquina.

Os scripts usam Python com IfcOpenShell/Numpy em `D:/TCC/work/ifc/deps` e reutilizam as regras R48/R49 em `D:/TCC/work`. Executar `auditar-final-h03-r50.py inicial`, `auditar-final-h03-r50.py reaberto` e `conferir-reabertura-h03-r50.py` para reauditar os arquivos preservados. `consolidar-h03-r50.py` exige que o estado nativo corresponda ao congelado; não o executar após novas alterações no projeto. Os manifestos contêm hashes de integridade, sem equivaler a aprovação técnica.

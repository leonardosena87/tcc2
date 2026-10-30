# H03/R78 — fatores Q harmonizados e persistência conferida

ESTUDO PARCIAL. NÃO EXECUTAR. Esta etapa trata do cadastro de ações dos receptores Eberick; não atualiza a monografia nem os autores RVT/DWG.

Nas cópias independentes `02-H03-R78-CAD-NAO-EXECUTAR` e `03-H03-R78-BIM-NAO-EXECUTAR`, a ação existente **Acidental**, indicação **Q**, passou de ψ0/ψ1/ψ2 = 0,70/0,60/0,40 para **0,50/0,40/0,30**. A referência é a tabela 11.2 do exemplar local ABNT NBR 6118:2026, página 67/PDF85, para ocupação residencial e acesso restrito. Essa classificação não define a intensidade de cada carga nem comprova todas as combinações.

O controle automático voltou a retornar campo indisponível na tentativa de editar ψ0 do CAD. O usuário informou a conclusão da entrada manual e do salvamento de cada cópia. Em seguida, cada projeto foi fechado e reaberto no aplicativo real: leu-se novamente a mesma ação e confirmaram-se os três valores. Compararam-se 20 valores de campos da máscara por ramo; apenas os controles 152/153/154 diferiram nas leituras antes/depois. Os demais valores dessa máscara coincidiram entre os ramos. Esse recorte de interface não equivale a uma auditoria semântica de todo o binário ou de todas as configurações.

Os PRJ mudaram em relação ao estado inicial R77 e passaram na verificação de integridade ZIP. As pastas de trabalho fechadas foram congeladas com SHA256. Todos os 68 arquivos protegidos de R77 permaneceram iguais. A intervenção constitui ajuste comum de premissas, sem atribuição de erro de transferência ao CAD ou ao BIM.

## Registro de tempo e participação

Os intervalos prospectivos foram **CAD 4.833 min** e **BIM 2.884 min**, desde a abertura operacional até a confirmação final de fechamento após a conferência. Incluem espera pela entrada humana, navegação, consulta, raciocínio e latência. O CAD inclui a tentativa automática frustrada; o BIM não a repete. São intervalos assistidos exploratórios, de escopos diferentes; não são duração total de cada fluxo, não demonstram produtividade relativa e não entram em ranking. Não se reconstruiu uma duração exclusiva da digitação humana. Dois pedidos de intervenção foram atendidos; observaram-se seis valores de configuração alterados. Quantidade real de teclas, tokens de IA e custos não foi inferida.

## Próxima verificação

As cargas permanecem parciais: a ação específica Q_TELHADO e as 13 reações variáveis planejadas em R65 ainda não foram cadastradas/aplicadas. Não ocorreu reprocessamento nesta revisão. Qualquer resultado anteriormente processado pertence ao estado anterior, não constitui resultado recalculado de R78. A harmonização dos fatores não fecha vento, paredes, varanda coberta, reservatório, escada, apoios e demais verificações de ELU/ELS.

O próximo processamento deve usar novas cópias a partir deste congelamento. A exploração de vigas, com cargas atuais, serve para localizar impedimentos de concepção; não aprova seções nem dispensa o carregamento completo. O estudo continua delimitado à superestrutura com apoios idealizados, sem dimensionamento de fundações reais.

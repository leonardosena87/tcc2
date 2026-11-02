# R173 — patamar no pórtico analítico do receptor BIM

Corrigiu-se em cópia independente do BIM R172 a representação da viga frontal do patamar. O campo Elevação=-142,6 cm posicionava a geometria física, mas a exportação analítica anterior continha a barra na cota **320 cm**. Excluiu-se apenas essa viga de N1 e lançou-se V16, seção **20 × 30 cm**, elevação zero, em nível intermediário de altura **157,4 cm acima de N0**, resultando na cota analítica **177,4 cm**. Mantiveram-se as posições existentes P9/P10 no receptor BIM, correspondentes aos apoios espaciais P4/P10 do CAD. Não se criaram novas posições de pilares.

A [documentação oficial sobre elevação](https://suporte.altoqi.com.br/hc/pt-br/articles/360038789694) e a [orientação de nível intermediário](https://suporte.altoqi.com.br/hc/pt-br/articles/115002186654) fundamentam o tratamento. Não se altera o campo diretamente no PRJ: a operação foi realizada no Eberick.

Salvou-se, fechou-se e reabriu-se o projeto; a consulta nativa confirmou V16 e seus parâmetros no intermediário. A verificação de lançamento desse nível não detectou problemas. Isso não comprova dimensionamento ou compatibilidade integral. A cota 1,774 m é a discretização adotada no Eberick/CAD; difere em cerca de 0,118 mm da cota teórica 1,774117647 m do concreto do patamar. A escada ainda não foi integrada ao receptor e persiste a pendência da janela J4.

## Evidência analítica

Exportaram-se antes e depois o pórtico unifilar e as grelhas N1/N2 pelo exportador SAP2000 do Eberick, com seções e coeficientes redutores. O SAP2000 **não foi executado**. O formato exportado tem suas próprias hipóteses; não representa validação externa do cálculo.

O auditor textual confirma a barra antes em (441; 0; 320)–(654; 0; 320) cm e depois em (441; 0; 177,4)–(654; 0; 177,4) cm, conectada por barras rígidas aos nós dos pilares em X=440/655 cm. Confirma-se a continuidade vertical dos dois apoios nesses nós. As 11 prumadas existentes foram subdivididas no novo nível: o pórtico passou de 123 para 134 barras e de 99 para 110 nós. A cobertura vertical e as 11 posições permaneceram iguais. Todas as diferenças geométricas são explicadas pela mudança da viga com seus dois vínculos rígidos e pela subdivisão das 11 prumadas. As propriedades e atribuições de seções foram preservadas; nomes numéricos de seções auxiliares foram regenerados, por isso a comparação usa propriedades e multiconjuntos de barras coincidentes.

As forças nodais por posição não permaneceram idênticas. A grelha N1 foi regenerada e não se afirmou igualdade completa das cargas analíticas; igualdade dos totais arredondados não substitui essa auditoria. O JSON de forças contém apenas a tabela nodal, sem somar cargas de barras e sem representar o total da estrutura.

## Diagnóstico parcial

Repetiu-se a análise estática e de deslocamentos do pórtico com rigidez configurada, dimensionamento e flechas das lajes desmarcados, tal como no BIM R172. O processamento terminou **com avisos**.

| Valor exibido | BIM R172 | BIM R173 |
|---|---:|---:|
| Peso próprio (tf) | 75,72 | 75,72 |
| Adicional (tf) | 9,65 | 9,65 |
| Acidental (tf) | 17,01 | 17,01 |
| QT | Ausente do resumo | Ausente do resumo |
| Total (tf) | 102,38 | 102,38 |
| Deslocamento X+/X− (cm) | 0,20 / 0,20 | 0,15 / 0,15 |
| Deslocamento Y+/Y− (cm) | 0,20 / 0,20 | 0,20 / 0,20 |
| Máximo relativo N1/Y+ (cm) | 0,17 | 0,16 |
| Gama-Z X+/X− | 1,09 / 1,08 | 1,07 / 1,06 |

Esse resultado caracteriza o efeito observado da correção e da remontagem analítica nesta cópia. Não é prova de que todas as diferenças entre os fluxos tenham uma única causa. As cargas da cobertura ainda não foram recuperadas no novo receptor BIM. Permanecem escada, paredes, reservatório, vento, combinações e verificações ELU/ELS completas.

## Tempo e preservação

O intervalo observado de correção, do início da edição até o primeiro salvamento, foi **626,550 s (10 min 26,550 s)**. Inclui verificações, latência de ferramentas e retomada de contexto; não mede CPU ou inferência isolada. A observação de processamento, do comando OK até o registro da conclusão com avisos, foi **14,863 s**; trata-se de intervalo de observação, não de benchmark do solver. São etapas distintas; não representam o tempo total de um fluxo nem permitem ranking ou economia percentual. Não se mediram tokens/custo da IA. Não houve intervenção humana solicitada nesta correção; houve atualização de foco após sinal de entrada do usuário, sem atribuir autoria à tecla observada.

Os arquivos-fonte R172 permaneceram íntegros por hash. Preservou-se o primeiro PRJ salvo antes da análise e congelou-se o receptor após processamento. Não se modificaram RVT, DWG ou trabalho escrito. Os quatro testes usam a exportação real e rejeitam modelo sem correção, ligação desconectada e posição extra de pilar. NÃO EXECUTAR.

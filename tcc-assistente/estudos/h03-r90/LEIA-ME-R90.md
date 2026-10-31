# H03/R90 — registro de qualidade e interpretação dos resultados

Organizaram-se dez observações com fontes e hashes, separando disponibilidade de dados, complementação, normalização de formato, concepção comum, ocorrências de interface, agrupamento nativo e quantitativos. Elas não são dez erros de cada programa e não devem ser somadas como um índice de qualidade.

## Resultados que já têm evidência

Na chegada inicial ao Eberick, o CAD preservou 62 contornos e 66 conteúdos de texto como referência gráfica. O BIM, depois do tratamento documentado de IFC, apresentou 22 trechos de pilar e 29 vigas lógicas nativos: 51/62 unidades previstas, ou 82,26%. As onze lajes não chegaram como lajes nativas nesse recorte. O CAD iniciou com zero dessas 62 unidades calculáveis, o que não significa perda de seus contornos/textos: a representação gráfica foi recebida e serviu à reconstrução.

As complementações posteriores atenderam 62 unidades lógicas no CAD e onze no BIM. Essas quantidades não são contagens de defeitos ou de operações. O esforço BIM também inclui o tratamento de 17 registros geométricos e a remoção de dois pavimentos vazios; não se omite essa etapa ao relatar o fluxo automatizado.

O ajuste de quatro campos de material em cada ramo R51 foi adequação às premissas comuns. Sem demonstrar o valor no autor e seu contrato de transferência, não se atribui a alteração a perda de IFC ou DWG. A mesma regra vale para os metadados documentais antigos identificados na R87.

No experimento local R81, uma divisão do agrupamento de viga BIM alterou a quantidade de grupos de 20 para 21 e eliminou a mensagem D16 naquele teste. Persistiram avisos e outras pendências. Esse resultado não prova que a importação IFC criou o agrupamento, que o algoritmo interno foi inteiramente identificado ou que a estrutura foi aprovada.

A auditoria R88 mostrou domínio geométrico ocupado coincidente entre a proposta nominal e os quatro IFCs inspecionados. A soma de partes e o volume da união exigem critérios distintos: diferenças de contagem de partes e de atribuição de encontros às classes não são automaticamente novos elementos físicos ou perdas de material. O resultado é geométrico e não verifica o modelo analítico.

## Resultados ainda não disponíveis

Os totais finais de correções e os tempos completos comparáveis permanecem nulos para ambos os ramos. Não se substitui um campo não inspecionado por zero nem se cria um vencedor a partir da disponibilidade inicial ou do teste local. Não se calculou um índice geral com pesos arbitrários.

O registro permite fundamentar resultados parciais e a discussão do desenvolvimento do protótipo. O estudo continua limitado a uma edificação e às versões/configurações registradas; não demonstra superioridade universal de um software. O texto acadêmico permanece inalterado nesta etapa.

O consolidado final desta rodada está em `D:/TCC/outputs/Qualidade-H03-R90-REGISTRO-PARCIAL/verificacao-final/R90-registro-qualidade.json`. O arquivo da primeira passagem foi preservado; a versão final referencia a conferência rigorosa das faces dos cuboides R88.

Reprodução: `node consolidar-qualidade.mjs D:/TCC <nova-pasta-de-saida>`. O script confere os números que sustentam as observações, verifica as fontes e escreve somente na nova pasta.

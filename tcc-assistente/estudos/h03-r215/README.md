# H03/R215 — Esforços simultâneos nos apoios inferiores da escada

Criou-se cópia BIM da R214 em D:/TCC/outputs/H03-R215-ESFORCOS-ESCADA-NAO-EXECUTAR. Na abertura o Eberick informou erro na última edição e ofereceu Verificar projeto danificado. Executou-se a verificação na cópia; os resultados foram invalidados. Reprocessou-se com dimensionamento integral e deslocamentos do pórtico e lajes por rigidez fissurada. O relatório Mensagens da análise, emitido nesta sessão, registra10 segundos totais e3 segundos de dimensionamento incluídos. É uma execução BIM de controle, incluindo elementos de fundação fora do escopo. Não há execução CAD pareada desta revisão.

Emitiu-se Relatórios da análise > Esforços nas fundações, selecionando somente SAE1A e SAE1B, todos os casos/combinações disponíveis e geração por elemento. O documento Pav1_Fundacao_Combinacoes.docx contém19 casos e28 combinações por apoio,94 linhas de esforços ao todo. O script preserva os seis componentes de cada linha, a combinação e os cabeçalhos. Não se montou um vetor artificial pela soma de máximos independentes.

| Apoio/ação | N (kN) | Mx global (kN.m) | My global (kN.m) | Vx (kN) | Vy (kN) |
|---|---:|---:|---:|---:|---:|
| SAE1A / G1 | 6,62 | 0,00 | -0,61 | -8,14 | 0,00 |
| SAE1B / G1 | 8,57 | 0,00 | 0,44 | 8,14 | 0,00 |
| SAE1A / G2 | 0,98 | 0,00 | -0,11 | -1,29 | 0,00 |
| SAE1B / G2 | 1,46 | 0,00 | 0,06 | 1,29 | 0,00 |
| SAE1A / Q | 2,61 | 0,00 | -0,22 | -3,07 | 0,00 |
| SAE1B / Q | 3,17 | 0,00 | 0,17 | 3,07 | 0,00 |

A combinação G1+G2+Q+0.6V2+0.6D2+0.5QT apresenta no SAE1A N10,22 kN, Mx0,00, My−0,97 kN.m e Vx−12,63 kN. No SAE1B, a combinação com V1/D1 apresenta N13,20 kN, Mx0,00, My0,69 kN.m e Vx12,63 kN. Os dois máximos pertencem a combinações diferentes; a tabela JSON conserva também os pares de uma mesma combinação e suas somas. Para os casos G1/G2/Q, os Vx são opostos na precisão do relatório. Essa observação identifica transmissão horizontal relevante aos apoios e não autoriza dimensionar o apoio idealizado ou a fundação.

As combinações deste relatório de fundações não foram classificadas como combinações ELU de verificação da viga. Os esforços globais na base dos apoios não são os esforços locais de uma seção da V1. Ainda falta extrair e conferir, na seção crítica da viga, N/M nos dois eixos para a mesma combinação, verificar sua resistência e o detalhamento. Não se resolveu o Aviso19 por interpretar somente estes números. O cabeçalho nativo de Mt aparece como kN/m, dimensionalmente ambíguo para torção; ele foi mantido no registro, sem conversão silenciosa. Todos os valores Mt exibidos são0,00 na precisão do relatório.

Após a recuperação e o cálculo, o diagnóstico mostrou novamente dois avisos nos pilares P3/P4 do N1. A planilha de prumada confirmou6phi10 em L3 e4phi10 nos lances inferiores. Reaplicou-se Uniformizar abaixo: L2/L1 passaram de3,14 para4,71 cm2, sem alterar seções ou resistência. Preservou-se o diagnóstico anterior, salvaram-se as capturas e o PRJ. O diagnóstico final reemitido confirmou12 pilares do N1 sem aviso/erro, além de12 vigas,6 lajes e3 elementos de escada com sucesso. N2 permanece com8 vigas com sucesso e1 com aviso; N0 com1 viga e11 pilares com aviso e14 sapatas com erro. Não foi listado deslocamento excessivo. Não houve cálculo integral após a uniformização de detalhamento.

O Word manteve o diagnóstico aberto e impediu uma sobrescrita, com a mensagem de arquivo protegido contra gravação. Fechou-se somente o relatório aberto e repetiu-se a emissão; os documentos alheios ao estudo foram preservados. A saída final foi relida do DOCX e conferida.

Depois do salvamento e da conferência dos relatórios, acionou-se Arquivo > Fechar projeto. O Eberick encerrou com falha. O PRJ manteve o hash84ce9482e16afdeac95c3301fbbae63c52dc2555e069c3c7b4a239b0618348b2 e a verificação CRC de seu conteúdo ZIP passou. Isso comprova legibilidade do contêiner salvo, não reabertura funcional do modelo ou ausência de inconsistência interna. A captura e o registro de integridade foram preservados; o relatório de falha não foi enviado a terceiros.

Ao sair da sessão R214 para abrir esta cópia, havia alterações não gravadas, que foram salvas para preservar o trabalho. O PRJ BIM R214 após esse salvamento tem hash e3556b9887c192d26d5c1313663fb894d23582593c8efd1ae35210cb9f4212c7, diferente do arquivo1ac60fa01207ae4b3e4abfd8cbd3296774055665811ddb317404c062ed02ee37 registrado no backup R214. O backup preserva a evidência anterior; não se transfere a validação de hash do backup ao arquivo posterior. Não se atribui a mudança a uma alteração estrutural específica sem comparação adicional.

Reprodução: `python tcc-assistente/estudos/h03-r215/auditar.py "D:/TCC/outputs/H03-R215-ESFORCOS-ESCADA-NAO-EXECUTAR"`. O script valida seleção dos apoios, cabeçalhos, quantidade de componentes, duplicidade e correspondência das combinações. A extração não é um cálculo estrutural independente. Permanecem a revisão do Aviso19, o Aviso08 da cobertura, a diferença de inércia da grelha N1 e a compatibilização dos modelos de autoria. Não se alterou o texto acadêmico ou liberou o estudo para execução.

# H03/R201 — Verificação das deformações nos dois fluxos

Em 03/11/2026, identificou-se no painel nativo que os avisos das três peças da escada eram o Aviso 123, referente à falta de verificação dos deslocamentos. Criaram-se cópias independentes das duas R199 e habilitou-se Determinação dos deslocamentos do pórtico e Determinação dos deslocamentos das lajes, ambas com Calcular rigidez fissurada. Os painéis foram processados em todos os pavimentos. Manteve-se a opção de dimensionamento dos elementos selecionados herdada do cálculo anterior. As capturas das opções estão na pasta de evidências.

No BIM, a abertura da cópia acionou a verificação de projeto danificado oferecida pelo Eberick, que foi executada antes do reprocessamento. O processamento posterior refez a análise estática. Esta ocorrência deve integrar o registro operacional de abertura da cópia.

O diagnóstico detalhado de cada modelo passou a registrar as três peças de escada e as 11 lajes com sucesso, sem avisos nessas categorias. Ambos informam Nenhum elemento com deslocamento excessivo. A leitura integral da árvore de status confirma a ausência do Aviso 123. As magnitudes individuais de flecha e as hipóteses de fluência ainda exigem leitura dos diagramas e das configurações. O resultado corresponde aos carregamentos e vínculos acadêmicos atuais.

## Tempo observado

| Medição nativa, uma execução | CAD | BIM |
|---|---|---|
| Processamento total R201 | 9 s | 9 s |
| Dimensionamento, incluído no total | 2 s | 2 s |

O tempo total inclui a rodada de análise, dimensionamento e verificações selecionadas. Preparação, abertura, leitura, intervenção humana e elaboração dos registros pertencem a outras etapas. O arquivo tempos-observados.json registra também o intervalo externo do clique até a observação de 100%, incluindo latência das ferramentas. Uma execução por fluxo ainda exige cautela na interpretação da produtividade.

## Pendências identificadas no painel nativo

| Elemento e nível | CAD | BIM | Pendência |
|---|---|---|---|
| Apoio inferior N0 | V1 | V1 | Aviso 19, flexão oblíqua sem consideração no dimensionamento |
| Viga N1 | V9 | V11 | Aviso 98, conferir ancoragem da armadura de pele no nó 3 |
| Viga N2 | V13_1 | V3 | Aviso 08, carga negativa |
| Viga N1 | agrupamento distinto | V2 | D16, armadura negativa no nó 2 |
| Pilares N1 | P1/P2/P9 | P3/P4/P8 | Aviso 10, bitola ou quantidade de barras menor que no lance acima |
| Pilares N0 | 11 | 11 | Aviso 07, falta de travamento no nível |
| Marcadores de apoio | 13 sapatas | 13 sapatas | D175/D42, fundações fora do escopo do estudo |

As correspondências de vigas por posição devem ser reconfirmadas antes da comparação final do retrabalho. A igualdade de números de avisos ou erros depende da representação e do agrupamento de vigas. O D16 BIM permanece uma frente de correção e de controle da equivalência do lançamento.

A carga W08 ainda exige reconciliação da extensão aplicada e definição do caminho do pano inferior. A V16 apresenta sucesso no diagnóstico desta rodada. A V1 continua com Aviso 19 e exige tratar o esforço lateral associado à escada. O estudo segue limitado à superestrutura com apoios idealizados e sem aprovação final.

## Evidências e arquivos

D:/TCC/outputs/ELS-H03-R201 contém capturas, árvores completas de status, relatórios nativos DOCX e suas extrações textuais. D:/TCC/entrega-orientador/H03-R201-ELS contém as duas cópias PRJ para conferência. Os hashes dos PRJ e dos relatórios constam de R201-resultado.json.

A IA operou a interface, identificou os avisos, configurou as verificações, iniciou o processamento, extraiu os relatórios e comparou os resultados. As conclusões acima se limitam às leituras nativas registradas. O estudo continua com as pendências listadas.

Referências operacionais consultadas
- https://suporte.altoqi.com.br/hc/pt-br/articles/360049475714
- https://suporte.altoqi.com.br/hc/pt-br/articles/115003468453

As extrações TXT versionadas tiveram apenas os espaços finais de linha removidos. Os DOCX nativos e as extrações originais permanecem na pasta de evidências.

# H03/R52 — hipótese de continuidade da varanda nos dois ramos

**Estudo não dimensionado — não executar.** Atribuição de vínculo para análise posterior; não representa verificação estrutural concluída.

## O que foi feito

Criaram-se cópias independentes dos estados congelados R51/CAD e R51/BIM. Em cada cópia abriu-se o N1, acionou-se `Modelo > Lajes > Engastar`, selecionou-se uma viga comum às lajes nativas L4 (interna) e L6 (varanda) e confirmou-se com Enter. O eixo selecionado corresponde à proposta V12-N1: x=9,65 m, y=3,90 a 7,05 m, nível 3,20 m. Trata-se da continuidade entre lajes, escolhida como hipótese comum, com lançamento e salvamento separados por ramo.

A operação segue a distinção descrita no suporte oficial entre [continuidade com laje adjacente e engaste direto em viga](https://suporte.altoqi.com.br/hc/pt-br/articles/115004249154) e o procedimento de [lajes com bordos livres](https://suporte.altoqi.com.br/hc/pt-br/articles/115003725214). Não se adotou automaticamente engaste direto na viga. Os artigos orientam a operação do software; não substituem a norma nem a análise do caso.

O programa aceitou a seleção de uma barra e retornou ao comando livre. Salvaram-se e reabriram-se ambos os arquivos, observando-se o croqui. O vínculo anterior não foi identificado de forma independente; por isso não se afirma que ele estava incorreto ou ausente, nem se conta a operação como defeito de transferência. Atribuição do comando e alteração do arquivo nativo são evidências operacionais; o parâmetro interno do vínculo e a grelha processada ainda não foram extraídos/verificados.

## Controle geométrico posterior

Exportaram-se IFCs completos, em pastas próprias `IFC-CAD` e `IFC-BIM`, após a reabertura. Cada arquivo manteve os 22 trechos de pilares, 32 sólidos de vigas (29 vigas lógicas) e 11 lajes. Em comparação com os estados reabertos R49/CAD e R50/BIM, conservaram-se classes, nomes, GUIDs, caixas envolventes e áreas superiores trianguladas dos 65 sólidos, com tolerância computacional de 1e-5 m/m². A auditoria não compara malhas completas.

Esses IFCs controlam os efeitos geométricos das revisões R51/R52. Não são usados para comprovar o vínculo analítico ou os materiais lidos na interface. A conectividade global, o comportamento do balanço, a armadura negativa/ancoragem e as deformações permanecem pendentes da análise com entradas completas.

A validação de esquema IFC4 encontrou oito erros em cada saída, relativos a listas opcionais vazias de identificação/endereços. Os IFCs exportados foram mantidos sem reparo silencioso. Esses erros não devem ser confundidos com perda geométrica ou verificação estrutural.

## Intervalos assistidos registrados

| Ramo e escopo delimitado | Duração |
|---|---:|
| CAD: abrir cópia R52, atribuir continuidade, salvar/reabrir e observar croqui | 4 min 38,690 s |
| BIM: abrir cópia R52, atribuir continuidade, salvar/reabrir e observar croqui | 4 min 15,089 s |
| BIM: exportação de controle e auditoria, incluindo preparação do auditor | 2 min 24,818 s |
| CAD: abrir arquivo, exportação de controle e auditoria | 3 min 58,584 s |

Os intervalos incluem operação assistida e latências, não são repetições controladas e não medem tempo ativo ou esforço isolado da IA. A ordem das operações e a preparação de ferramentas influenciam os valores; os controles posteriores também possuem escopos distintos. Não somar essas linhas para declarar tempo total de fluxo ou ranking entre programas.

## Arquivos para continuidade

CAD: `D:/TCC/outputs/H03_CAD_R52_VINCULOS_NAO_EXECUTAR/Projeto Eberick/H03_CAD_R49_LAJES_NAO_EXECUTAR.prj`.

BIM: `D:/TCC/outputs/H03_BIM_R52_VINCULOS_NAO_EXECUTAR/Projeto Eberick/H03_BIM_R46_IFC_NAO_EXECUTAR.prj`.

Os nomes-base anteriores foram mantidos para conservar recursos relativos; a pasta e a associação da edificação identificam a R52. Os estados nativos foram congelados antes das exportações de controle. A alteração de destino IFC posterior ficou fora do salvamento congelado, sem alterar a geometria/vínculo já salvo. Não se realizou teste de portabilidade em outra máquina.

Próximo trabalho: conferir apoios idealizados e conectividade da superestrutura, completar cargas de uso/permanentes/vento, posição e apoio do tanque de 1.000 L e tratamento da escada. Depois processar para conferir grelha, esforços, resistência, estabilidade e deformações. Não alterar a monografia antes de consolidar os resultados do estudo. As hipóteses comuns que mudarem devem ser reaplicadas nos dois ramos.

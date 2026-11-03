# H03/R187 — ensaio de continuidade V2/V14 no CAD

Estudo preliminar, não executar. A cópia experimental está em `D:/TCC/outputs/R187-CAD-ENSAIO-CONTINUIDADE-V2-NAO-EXECUTAR`. Os receptores R182 CAD e BIM foram preservados; a R178 continua como referência de trabalho no ponteiro principal. O projeto escrito não foi alterado.

## Intervenção e resultado

Aplicou-se Lançamento → Vigas → Unificar somente à V2 e à V14 do N1, selecionando primeiro V2. Manteve-se P5 como apoio intermediário e não se incluiu V13. A antiga V14 passou a integrar o segundo vão de V2. A planilha nativa conservou os vãos de 440 e 199,6 cm, as seções de 20×45 e 20×16 cm, respectivamente, e elevação 0 cm nos dois trechos. Não se aumentou seção nem limite de armadura neste ensaio.

Na abertura da cópia houve aviso de possível erro na última edição e foi executada a verificação nativa de integridade, que limpou a análise anterior. Essa preparação é uma variável adicional; não se afirmou que o único estado interno alterado foi o agrupamento. O comando foi aplicado depois dessa verificação e o dimensionamento foi refeito no mesmo escopo da R182: vigas, pilares e lajes de N1/N2 e escadas de N1; N0 e fundações excluídos. Mantiveram-se deslocamentos do pórtico com rigidez configurada; flechas das lajes, dinâmica, etapas construtivas e verificação dos limites de redistribuição semirrígida permaneceram desativadas.

O relatório passou de 16 vigas com sucesso no N1 CAD da R182 para **14 com sucesso e uma com erro**, totalizando 15 grupos após a unificação. A planilha da V2 identificou **D16 — armadura negativa, nó 2**, e **A07 — taxa de armadura maior que a configurada** nas cinco bitolas exibidas: 8; 10; 12,5; 16 e 20 mm. É o mesmo diagnóstico registrado na V2 BIM R182. O nó intermediário é P5, com Md = −36,90 kN·m. Os extremos P2/P11 exibiram −31,17/−5,62 kN·m.

| Valor exibido | V2, vão 1 | V2, vão 2, antiga V14 |
|---|---:|---:|
| Vd inicial, kN | 41,49 | 22,18 |
| Vd final, kN | 46,30 | 15,36 |
| Md positivo, kN·m | 32,22 | 1,69 |
| Md negativo, kN·m | −36,90 | −7,96 |
| Mtd, kN·m | 0,05 | 0,16 |

Os dez valores coincidem, na precisão exibida, com as envoltórias CAD V2/V14 anteriores, registradas na R186. Não se verificaram todos os pontos, casos ou combinações governantes. Os valores de cortante são as magnitudes apresentadas pela planilha, sem interpretação como vetores globais com sinal. O resumo conservou peso próprio 78,93 tf; adicional 12,58 tf; acidental 18,45 tf; manutenção de telhado 1,78 tf; total 111,74 tf e área aproximada 138,18 m². Essa igualdade de totais não prova igualdade de distribuição das cargas.

O ensaio sustenta a influência do agrupamento no diagnóstico deste caso: o erro também ocorre no CAD quando os dois trechos compõem uma viga. Não sustenta vantagem do CAD pelo antigo resultado de zero erros de viga, nem permite calcular uma classificação pelos denominadores 31/21. A R187 alterou apenas um par de grupos e não igualou o agrupamento de todo o edifício. A causa interna exata da falha e a solução de armadura ainda exigem análise.

## Escada e tempos

A planilha Positivo manteve LE1 e LE2 como “calculado” e LE3 com **D31**. Não se releu a causa A11 por bitola nesta revisão; essa leitura pertence à R182/R184. O resumo de lajes não comprova aprovação da escada.

O relatório nativo registrou **7 s de processamento**, com **2 s de dimensionamento já incluídos nesses 7 s**. O intervalo entre o clique em OK e a primeira confirmação observada foi **13,436 s**, incluindo latência do controle e observação. Há uma medição, sem repetição estatística. Esses registros não representam tempo ativo nem duração completa do fluxo CAD. Não se somaram os tempos contidos nem se produziu classificação de produtividade.

## Evidência e limites

Preservaram-se relatório DOCX nativo, texto extraído, capturas das seções, envoltórias e A07, opções e seleção do cálculo, PRJ experimental salvo e hashes dos PRJs R182. O consolidador confere os hashes, a integridade ZIP do PRJ, as contagens nativas e a comparação dos dez valores transcritos. Os testes reutilizados verificam a leitura de evidências, não a segurança da estrutura.

Os IFC/SAP herdados da cópia não são novas exportações R187. A retenção integral de geometria, vínculos e cargas permanece sem auditoria por nova exportação. Permanecem a ancoragem de LE3, a compatibilização V16/J4, os apoios idealizados, a revisão de cargas, os estados-limite ainda não abrangidos e as armaduras. Nenhum arquivo deste ensaio está liberado para execução.

O procedimento de unificação está descrito na [documentação oficial AltoQi](https://suporte.altoqi.com.br/hc/pt-br/articles/360015684234), consultada em 03/11/2026. A documentação explica o comando; o resultado acima decorre das telas e do relatório efetivamente obtidos neste projeto.

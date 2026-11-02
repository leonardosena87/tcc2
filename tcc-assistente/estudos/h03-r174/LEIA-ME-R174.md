# R174 — recuperação de cinco apoios de cobertura no BIM

Em cópia independente da R173, restauraram-se os vetores gravitacionais das hipóteses VP1-A e P2-GRAV-A já estudadas nas R109/R115. Antes de editar, conferiram-se as ações Adicional e Q_TELHADO_MANUTENCAO: as seis componentes estavam zeradas nos cinco apoios. Não se atribui essa constatação automaticamente a todos os demais nós do modelo.

| Apoio | Pilar BIM | X; Y (cm) | Fz G (kN) | My G (kN.m) | Fz QT (kN) | My QT (kN.m) |
|---|---|---|---:|---:|---:|---:|
| VP1-02 | P3 | 965; 705 | −0,521164 | +0,260582 | −0,393750 | +0,196875 |
| RP2-01 | P10 | 655; 0 | −1,000138 | 0 | −0,755625 | 0 |
| RP2-02 | P11 | 965; 0 | −1,000138 | 0 | −0,755625 | 0 |
| RP2-03 | P6 | 655; 390 | −1,000138 | 0 | −0,755625 | 0 |
| RP2-04 | P7 | 965; 390 | −1,521302 | +0,260582 | −1,149375 | +0,196875 |

Todos pertencem a N2, cota 639 cm. Fx, Fy, Mx e Mz são zero para essas ações. RP2-04 contém **uma única vez** a soma da varanda VP1-01 com P2. Não se lançou VP1-01 separadamente nem se adicionou novamente o forro já presente nas lajes. Coordenadas são as posições nominais dos apoios já auditados; as consultas nativas identificam nome e pavimento, complementadas pela seleção no croqui. Não se pressupõe igualdade de nomenclatura CAD/BIM.

O plano geral registra 18 posições de cobertura. Esta revisão conclui **somente cinco apoios**; os 13 nós RC01–RC13 de A1/A2 continuam pendentes. Os vetores totais do plano de 18 posições não representam cargas já lançadas nesta revisão. Reservatório, paredes, vento, combinações e escada permanecem com suas pendências anteriores.

Salvou-se, fechou-se e reabriu-se o PRJ. Releu-se G e QT em cada apoio e fechou-se sem salvar consultas. As 60 componentes finais e as 60 iniciais zeradas passaram no auditor, admitindo apenas a precisão exibida de 0,0000051 para essa conferência numérica; não é tolerância de engenharia. A QT compartilhada aparece como −1,14938 kN e a permanente compartilhada como −1,5213 kN após reabrir. Não se redigitou para perseguir casas ocultas. O PRJ manteve o hash do primeiro salvamento durante a releitura; conferiu-se a integridade ZIP e congelaram-se os arquivos locais.

Houve entradas numéricas recusadas: uma colagem/substituição preservou um zero inicial, gerando texto inválido, e uma tentativa de momento ficou vazia. Nenhuma foi aceita como carga. Substituiu-se integralmente o conteúdo, com Home/Shift+End e digitação, e confirmou-se o vetor por leitura antes de concluir. A tentativa de acionar Cargas por índice de acessibilidade também falhou na consulta; usaram-se capturas atuais e coordenadas. O esforço integra o intervalo observado, sem intervenção humana solicitada.

O intervalo de edição até o primeiro salvamento foi **666,921 s (11 min 6,921 s)**. A sessão com salvar, fechar, reabrir, reler e fechar durou **1.070,144 s (17 min 50,144 s)** e **contém** o intervalo anterior; não se somam. Incluem navegação, tentativas, capturas e documentação, sem medir CPU, inferência isolada, tokens, custo da IA ou fluxo completo. Não permitem ranking de produtividade.

Os dois testes controlam o arredondamento real e a rejeição de ação, projeto, sinal ou momento incorreto. Não são verificações normativas. Não se processou a R174: as edições invalidam a análise herdada da R173. Os arquivos-fonte e planos históricos foram preservados por hash. RVT, DWG e monografia não foram alterados. **NÃO EXECUTAR**.

Próximo: criar os 13 nós de A1/A2 nas vigas correspondentes, lançar e reler G/QT e só então repetir o diagnóstico e a comparação com o CAD, preservando a associação espacial e as hipóteses comuns.

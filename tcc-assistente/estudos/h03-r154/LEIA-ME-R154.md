# H03/R154 — decisão final: manter 17 espelhos

**Decisão posterior que prevalece:** “deixe com 17 mesmo. temos que adiantar”. A referência ativa foi restabelecida para R153, com 17 espelhos uniformes, distribuição 9 + 8 e patamar acabado +1,824118 m. A correção concentrada em dois espelhos não foi aplicada. R154-decisao-final17.json registra essa decisão e R154-estado-interrompido.json preserva o apontador intermediário. A criação nativa posterior no Revit é documentada separadamente na R155.

## Histórico da solicitação substituída

O usuário solicitou inicialmente voltar ao projeto original e subdividir a diferença de altura no primeiro degrau e no patamar. A análise abaixo corresponde à solicitação intermediária, posteriormente substituída pela decisão de manter 17. Não houve edição dos projetos nativos nesta R154.

## Verificação da divisão solicitada

Na hipótese gráfica de 16 espelhos, oito por lance, o valor anotado de 18,5 cm totaliza 2,96 m. O desnível acabado +0,22 → +3,25 m corresponde a 3,03 m; portanto, restam **7 cm**. A hipótese de 16 deriva dos sete intervalos gráficos de pisada de cada lance, não de um levantamento executivo validado.

Dividir o acréscimo igualmente entre dois espelhos representa 3,5 cm adicionais em cada um, produzindo **dois espelhos de 22 cm entre outros de 18,5 cm**. Isso fecha a soma, mas elimina a uniformidade. Não se adotou essa correção como segura, dimensionada ou normativa e não se gerou uma escada nativa com esses degraus.

Há duas leituras distintas para “primeiro degrau e patamar”, ambas registradas no JSON:

| Interpretação matemática | Espelhos aumentados | Cota acabada do patamar | Cota final |
|---|---|---:|---:|
| Primeiro espelho e espelho de chegada ao patamar | 1 e 8 | +1,770 m | +3,250 m |
| Primeiro espelho de cada lance, um deles na saída do patamar | 1 e 9 | +1,735 m | +3,250 m |

As duas geram espelhos de 22 cm e uma variação local de 35 mm. Não foi escolhida silenciosamente uma interpretação. Alterar a cota do patamar é diferente de acrescentar altura a um espelho: a cota incorpora a soma de todos os espelhos anteriores.

O problema de uniformidade tem fundamento de segurança, além do fechamento de cotas. O estudo experimental [Negotiating stairs with an inconsistent riser: Implications for stepping safety](https://pubmed.ncbi.nlm.nih.gov/32501252/) examinou a alteração da passada diante de espelhos inconsistentes. Essa pesquisa não é uma regra normativa brasileira e não foi usada para extrapolar quantitativamente o efeito de 35 mm. O anexo municipal consultado anteriormente exige dimensões constantes no trecho de escadas de uso coletivo; não se declarou automaticamente que todas as disposições desse trecho se aplicam à escada interna unifamiliar.

## Estado intermediário preservado

O apontador intermediário registrava **referência original retomada, com correção altimétrica em aberto**. Esse estado foi preservado em R154-estado-interrompido.json antes de restabelecer a definição R153. Não há aprovação da geometria original inconsistente nem da concentração em dois espelhos.

RVT, DWG, PRJ e monografia não foram modificados; os desenhos de estudo R152/R153 continuam separados e históricos. Nenhuma nova carga foi aplicada e nenhum aplicativo nativo foi operado nesta revisão. Os cálculos usaram aritmética decimal exata e verificações de soma, diferença de alturas e preservação de hashes das três fontes. A execução do script foi cronometrada separadamente, sem representar o tempo dos fluxos CAD/BIM ou esforço total de IA.

Para prosseguir com uma correção adotável, é necessário fechar o desnível com uma distribuição uniforme dos espelhos e verificar o enquadramento aplicável, a circulação e a geometria em planta e corte. Não se deve mascarar a incompatibilidade apenas alterando dois valores de altura.

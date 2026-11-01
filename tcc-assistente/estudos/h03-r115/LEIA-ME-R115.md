# H03/R115 — lançamento pareado da hipótese P2

Aplicou-se a hipótese gravitacional **P2-GRAV-A**, calculada na R114, em cópias independentes do Eberick derivadas da R109. Não se alterou o arquivo arquitetônico, o RVT ou o DWG nesta etapa. Não houve processamento ou dimensionamento R115.

O plano considera a cobertura nominal de 12,09 m² apoiada em quatro cantos, sob distribuição uniforme e esquema articulado idealizado. Água, tara, plataforma e pedestal do reservatório não integram essas parcelas. O aço da cobertura, seus vínculos e suas alturas executivas continuam sem dimensionamento.

| Apoio | Pilar CAD / BIM | Total G: Fz; My (kN; kN.m), digitado | Total QT: Fz; My, digitado |
| --- | --- | ---: | ---: |
| RP2-01 | P10 / P10 | −1,000138; 0 | −0,755625; 0 |
| RP2-02 | P7 / P11 | −1,000138; 0 | −0,755625; 0 |
| RP2-03 | P11 / P6 | −1,000138; 0 | −0,755625; 0 |
| RP2-04 | P8 / P7 | −1,521302; +0,260582 | −1,149375; +0,196875 |

RP2-04 coincide com VP1-01 da varanda: confirmou-se o vetor existente antes de editar; somou-se o incremento vertical de P2 e preservou-se My. Fx, Fy, Mx e Mz permaneceram zero nos quatro apoios para essas duas ações. Nos três primeiros apoios, os vetores iniciais eram zero nas duas ações.

O lançamento utilizou **Pilar → Cargas**, selecionando cada ação e preenchendo o vetor total. Não se pressupôs que o comando de carga concentrada somasse automaticamente uma parcela à carga existente. Os alvos foram associados pela posição nominal e conferidos pelo nome no receptor; o pareamento não depende de igualdade de nomenclatura entre os ramos.

Após salvar, fechar e reabrir cada cópia, releram-se as seis componentes de G e QT em cada apoio. As **48 comparações de componentes CAD/BIM coincidiram na precisão exibida** — 96 leituras finais, 48 por ramo. Fz permanente aparece como −1,00014 nos três primeiros apoios e −1,5213 no compartilhado; QT compartilhada aparece como −1,14938. Os demais valores correspondem aos digitados na tabela. O diálogo reaberto arredonda esses valores; não se afirmou identidade binária dos números internos. A conferência do plano aceita até 0,000005 kN para Fz reaberto neste intervalo, preservando controle estrito do sinal e dos momentos. Não se editou novamente para perseguir casas não exibidas.

Os 33 arquivos fonte R109 permaneceram com os hashes iniciais. O PRJ de cada R115 permaneceu inalterado durante a consulta após reabertura. As alterações de arquivos auxiliares constam do JSON. Congelaram-se e conferiram-se 15 arquivos CAD e 18 BIM com o projeto fechado. O manifesto relaciona os arquivos nativos locais e as evidências públicas; os binários nativos ficam somente em D:/TCC.

As sessões cronometradas de lançamento e releitura foram **CAD: 1.297.000,0656 ms (21min37,000s)** e **BIM: 1.104.471,6217 ms (18min24,472s)**. Incluem navegação, capturas, conferência e documentação; a sessão CAD também inclui retomada de contexto. Uma tentativa de edição indexada na interface CAD falhou e foi substituída por seleção de campo e digitação, com observação do foco. Esses intervalos não medem apenas inferência da IA, tempo de cálculo, tempo ativo humano ou duração completa dos fluxos. Não fundamentam ranking final. Nenhuma intervenção humana foi usada no lançamento P2 desta etapa.

Dois testes controlam o arredondamento exibido, a preservação do momento da varanda e a rejeição de ação, componente, sinal ou soma incorretos. A consolidação das evidências reais confirmou os 48 pares e os hashes. Esses controles verificam registros e aritmética, sem aprovar a estrutura.

Permanecem pendentes o processamento das cargas R115, vento/sucção, caso localizado de manutenção, outras cargas e combinações, além da solução geométrica e estrutural do reservatório. A igualdade obtida após lançar manualmente a mesma hipótese no receptor não prova retenção automática de cargas pelo DWG ou IFC. Demais nós de cobertura e pavimentos não foram integralmente reauditados nesta revisão.

Arquivos de trabalho fechados:

- CAD: `D:/TCC/outputs/28-H03-R115-CAD-P2-NAO-EXECUTAR/`
- BIM: `D:/TCC/outputs/29-H03-R115-BIM-P2-NAO-EXECUTAR/`
- Evidências e congelados: `D:/TCC/outputs/Telhado-P2-H03-R115-SENSIBILIDADE-NAO-EXECUTAR/`

Próxima etapa: processamento parcial em novas cópias, mantendo o mesmo escopo de comparação R111 e os modelos R115 congelados. Não apresentar resultados anteriores como resultados destas cargas.

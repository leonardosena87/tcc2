# R220 — Ganchos da armadura inferior, aplicados no Eberick

Pasta local: `D:/TCC/outputs/H03-R220-ANCORAGENS-NAO-EXECUTAR`. Criaram-se cópias completas CAD e BIM da R218. No Eberick, habilitou-se Projeto → Detalhamento → Vigas → Ancoragem → **Detalhar positivos sempre com gancho**, mantendo “Detalhar armadura sempre até a face do apoio” ligado e ponta reta mínima configurada em 10 cm. A configuração é de detalhamento das vigas do projeto; não se trata de uma opção individual da V1. Não se alteraram cargas, seções, resistências ou limite global dos estribos.

## Correção efetiva e conferência

| Detalhe | Antes R218 | Depois R220, CAD e BIM |
|---|---|---|
| V1 do N0: 2Ø8 inferiores | Reta, C104 | Ganchos de 10 cm nas duas pontas, segmento principal 104 cm, C120 |
| Cobertura CAD V13_1 / BIM V3: 2Ø8 inferiores | Reta, C329 | Ganchos de 10 cm nas duas pontas, segmento principal 329 cm, C345 |

Os comprimentos C foram lidos do detalhamento nativo; consideram a convenção de curvatura do programa e não são a simples soma das cotas externas. Conferiram-se os dois fluxos pela interface, com capturas dos quatro detalhes. Na cobertura, mantiveram-se 2Ø8 superiores C376 e uma barra adicional à esquerda Ø8 C109, seção 20×30 cm e vão livre de 285 cm. O carregamento negativo do terceiro trecho continuou com reação permanente −2,78 e acidental −0,41 kN/m; carga mínima −1,67 e máxima −1,27 kN/m.

A cópia CAD pediu verificação de consistência na primeira abertura. Executou-se a recuperação e o processamento com dimensionamento integral e deslocamentos fissurados do pórtico e lajes. O processamento terminou com avisos. A recuperação desmarcou a opção individual “Sempre adotar armadura de pele” da V1; por isso reaplicou-se essa opção, recalculou-se individualmente e selecionou-se novamente 2×2 Ø8. O detalhe final CAD confirmou quatro barras laterais e os ganchos novos na armadura inferior. No BIM, a pele permaneceu presente e a mudança de detalhamento foi aplicada sem novo processamento global. Não se interpreta essa assimetria de operações como ensaio de produtividade.

Os PRJ foram salvos com o comando nativo Salvar projeto estrutural (Ctrl+B). O CAD foi fechado e reaberto sem solicitar recuperação; a viga de cobertura foi então regenerada, confirmando a retenção dos ganchos. O BIM foi salvo e fechado. A validação do contêiner e o backup constam do registro de integridade.

## Limites e sequência técnica

A R220 corrige a ausência dos ganchos inferiores no detalhamento. A presença do gancho, isoladamente, não comprova a ancoragem: ainda é necessário conferir comprimento necessário, diâmetro de dobramento, espaço, cobrimento, confinamento e ligação aos apoios. Permanecem Aviso 19 na V1 e dois Avisos 98 da pele; o Aviso 08 da cobertura também permanece. Nenhuma mensagem foi desativada.

A [orientação oficial para o Aviso 08](https://suporte.altoqi.com.br/hc/pt-br/articles/360003993253) explica a possível inversão da seção de dimensionamento e a necessidade de adequar o detalhe, inclusive a continuidade da armadura negativa com a dupla. Portanto a adição dos ganchos inferiores não é registrada como encerramento desse aviso. A ajuda local `detalhamento_vigas_ancoragem.htm` documenta a opção aplicada, e `detalhamento_vigas_armadura_de_pele.htm` informa que ganchos na pele geram Aviso 98 para conferência.

Continuam prioritários: fechar o encaixe e a ancoragem das barras da V1 e da cobertura, conferir apoios/compatibilização e sincronizar a geometria de autoria Revit/CAD. O complemento transversal R218 e os desenhos de referência antigos foram preservados com sua identificação; eles não representam a nova armadura inferior nativa. Não se declara liberação executiva.

Não houve nova medição pareada de tempo nativo nem registro confiável de tokens ou inferência. O tempo histórico de 9/10 s de outra revisão não foi atribuído a este processamento. Não se alterou o texto acadêmico nem se reemitiram tabelas globais de resultados nesta etapa.

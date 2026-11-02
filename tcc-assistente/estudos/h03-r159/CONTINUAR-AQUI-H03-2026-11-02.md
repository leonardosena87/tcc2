# Continuação H03 — 02/11/2026 — R159

Entrega informada pelo usuário: **10/11/2026 às 19h, horário de Brasília**. Esta retomada trata do projeto técnico; a monografia permanece sem alterações.

## Arquivos conferidos nesta etapa

Pasta: `D:/TCC/outputs/Escada-H03-R159-IMPLANTACAO-NAO-EXECUTAR`.

- Revit: `H03-R159-Revit-VIGA-PATAMAR-NAO-EXECUTAR.rvt`.
- AutoCAD: `R159-CAD-N1-FORMA-CANDIDATA.dwg`, `R159-CAD-N2-FORMA-CANDIDATA.dwg` e `R159-CAD-PATAMAR-FORMA-CANDIDATA.dwg`.
- Evidência: `R159-resultado-nativo.json`, com releitura nativa após fechamento/reabertura; `R159-CAD-formas-conferidas.json`, com conferência dos retornos DXF dos três DWG.
- Contato nativo: `R159-interferencias-nativas.html`.

Revit confirmou 24 segmentos de pilares, 30 vigas e 11 lajes: 65 elementos nessas categorias, além da escada. A revisão conserva os dados lógicos dos 60 elementos retidos, modifica V15/L6 e acrescenta P12/P13/V16-ESC-PAT. Não se afirma igualdade dos volumes recortados pelas uniões automáticas.

A escada tem 17 espelhos iguais, em 9+8; pisada de 28 cm; largura nominal dos lances de 90 cm, medida pelos contornos; espessura hipotética de 14 cm. O patamar de concreto está em +1,774118 m e o acabamento hipotético de 5 cm leva ao patamar acabado +1,824118 m. A referência inferior de concreto +0,17 m ainda difere de N0 +0,20 m. O apoio inferior permanece pendente.

Criou-se a viga do patamar com seção candidata 20 x 30 cm e dois pilares laterais de 20 x 30 cm. Essas seções ainda não foram dimensionadas. O ensaio nativo de interferências apontou um par entre a escada e V16-ESC-PAT; não foi classificado automaticamente como defeito, apoio válido ou engaste. O aviso de corrimão não contínuo está preservado.

## Próximo passo verificável

A R159 foi reaberta e ficou disponível no Revit. Solicitou-se ao usuário abrir Arquivo → Exportar → IFC, pois a navegação automática fecha o submenu. A solicitação anterior para maximizar a janela foi superada; não é a pendência atual.

Preparou-se `R159-configuracao-IFC-CV.json` com base na configuração R94 Coordination View que reteve propriedades de materiais. Somente o nome da configuração mudou. O arquivo ainda precisa ser importado e relido no diálogo nativo; não é prova de exportação. Manter todo o modelo, sem limitar à vista recortada, sem dividir pilares por níveis e sem gravar GUID no RVT. Conferir as opções reais no diálogo, exportar para arquivo novo e auditar o conteúdo.

A auditoria deve distinguir os 65 elementos de pilares/vigas/lajes dos componentes da escada e corrimãos. Deve conferir especialmente a viga intermediária, as cotas, os níveis adicionais/virtuais, as identidades e a presença de fck=25 MPa nos materiais. Não presumir que o módulo herdado do Revit seja Eci/Ecs ou que um nome C25 prove a transferência de parâmetros ao Eberick.

Só depois preparar cópias independentes dos receptores para incorporar a revisão comum pelos dois caminhos, com congelamento antes de editar. Os projetos Eberick anteriores não foram atualizados nesta etapa. Conferir apoios por eixos/contornos/grelha, continuidade dos lances e patamar e efeitos da viga intermediária. Completar ações e parâmetros, analisar ELU/ELS e documentar as correções de cada rota. O estudo continua limitado à superestrutura, com apoios idealizados e sem dimensionamento de fundações reais.

## Tempos e comparação

O comando Revit bem-sucedido levou 2,287856 s. Isso não inclui três tentativas falhas de software, correções de código, reinicializações, intervenção humana, reabertura ou auditoria. As falhas foram preservadas e não devem virar defeitos de geometria ou importação IFC.

Na etapa anterior, a conferência do CAD parcial mediu 2 min 13,30 s e a sessão das três plantas 2D mediu 3 min 33,65 s. O intervalo de 23,29 s do script nativo está contido nessa última sessão e não deve ser somado novamente. Os escopos são distintos; não há ranking CAD/BIM nem tempo total final. Aplicar os critérios do protocolo comparativo existente, usando agora a contagem candidata de 24/30/11 e distinguindo a escada dos elementos originais.

Foram aprovados 81 testes automatizados do suplemento e cinco do comparador CAD. A compilação do conector teve zero erros/avisos. As gravações/reaberturas em AutoCAD/Revit são evidências nativas separadas dos testes; não se executou inferência paga ou cálculo estrutural por esses testes. A configuração IFC preparada continua pendente de validação no host.

Os originais R93/R157 estão preservados por hash. Os arquivos nativos permanecem em D:/TCC; o código e as evidências foram registrados localmente no Git. Não se enviou arquivo a terceiros nesta etapa. **NÃO EXECUTAR EM OBRA.**

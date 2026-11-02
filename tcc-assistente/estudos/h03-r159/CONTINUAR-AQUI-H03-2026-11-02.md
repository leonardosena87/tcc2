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

O IFC bruto da R159 foi exportado e auditado. O diálogo IFC já foi utilizado; não é pendência atual pedir ao usuário que o abra. Foram conferidas 65 identidades de pilares/vigas/lajes (24/30/11), além do patamar e dois lances da escada. A configuração nativa relida coincide com a preparada, exceto o nome salvo. Contudo, o arquivo contém zero IfcMaterialProperties. Há divergência nos atributos dimensionais dos dois IfcStairFlight, enquanto o Pset_StairFlightCommon preserva 178,235294/280 mm. Os arquivos não foram corrigidos para ocultar essas ocorrências.

Foi criado um receptor experimental bruto no Eberick, com nove níveis e configuração inicial. Caminho real: `D:/TCC/outputs/H03-R159-Revit-VIGA-PATAMAR-NAO-EXECUTARH03_R159_IFC_BRUTO_NAO_E/Projeto Eberick/H03-R159-Revit-VIGA-PATAMAR-NAO-EXECUTARH03_R159_IFC_BRUTO_NAO_E.prj`. O nome foi anexado ao anterior pela interface; usar o caminho real, sem presumir o nome inicialmente pretendido. O relatório confirma 54 origens: 30 vigas e 24 trechos de pilares, sem falta/repetição de origem. A saída IFC4 completa contém 33 partes de vigas, 72 de pilares e nenhuma laje/escada nativa. Não confundir segmentação com duplicação. Os onze arquivos do estado salvo foram congelados; o PRJ ainda coincide com esse estado após as consultas.

A conciliação espacial identificou as 30 origens de vigas em 31 das 33 partes, com tolerância XY de 0,1 mm. Doze partes associadas divergem em topo/altura; duas partes adicionais de V6/V7 excedem limites axiais e permaneceram sem associação. V16-ESC-PAT tem parte associada 20x30 cm no topo candidato, sem validação de apoio ou capacidade. Pilares ainda exigem cobertura física por seção/posição/cotas. A imagem 3D mostra também a referência externa, por isso a escada visível não prova conversão em elemento calculável.

Consultar `R159-IFC-E-RECEPCAO.md`, `R159-IFC-auditoria.json`, `R159-Eberick-recepcao-auditoria.json` e `R159-receptor-bruto-congelamento.json`. Preparar cópias para correção comparáveis às plantas CAD R159. Tratar níveis de referência e conversão nominal sem alterar o bruto; registrar operações/tempo. Os projetos principais CAD/BIM anteriores continuam sem a revisão completa. Conferir apoios por eixos/contornos/grelha, continuidade de lances/patamar e efeitos da viga intermediária. Completar materiais, ações/combinações e análise ELU/ELS. O estudo permanece limitado à superestrutura, com apoios idealizados e sem fundações reais.

## Tempos e comparação

O comando Revit bem-sucedido levou 2,287856 s. Isso não inclui três tentativas falhas de software, correções de código, reinicializações, intervenção humana, reabertura ou auditoria. As falhas foram preservadas e não devem virar defeitos de geometria ou importação IFC.

Na etapa anterior, a conferência do CAD parcial mediu 2 min 13,30 s e a sessão das três plantas 2D mediu 3 min 33,65 s. O intervalo de 23,29 s do script nativo está contido nessa última sessão e não deve ser somado novamente. Os escopos são distintos; não há ranking CAD/BIM nem tempo total final. Aplicar os critérios do protocolo comparativo existente, usando agora a contagem candidata de 24/30/11 e distinguindo a escada dos elementos originais.

Foram aprovados 81 testes automatizados do suplemento e cinco do comparador CAD. A compilação do conector teve zero erros/avisos. As gravações/reaberturas em AutoCAD/Revit são evidências nativas separadas dos testes; não se executou inferência paga ou cálculo estrutural por esses testes. A configuração IFC foi validada por releitura no host; a retenção de propriedades mecânicas não foi confirmada no arquivo exportado. Oito testes sintéticos dos novos auditores passaram. O tempo observado da exportação foi 21,435 s, contido na preparação de 7 min 21,232 s. A recepção bruta até salvamento/observação levou 3 min 6,184 s. São recortes parciais de sessão, sem ranking e sem somar subintervalos contidos.

Os originais R93/R157 estão preservados por hash. Os arquivos nativos permanecem em D:/TCC; o código e as evidências foram registrados localmente no Git. Não se enviou arquivo a terceiros nesta etapa. **NÃO EXECUTAR EM OBRA.**

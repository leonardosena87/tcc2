# H03/R140 — consulta de reações G2 das lajes

**Estudo parcial, não executar em obra.** Foram exportados quatro diagramas nativos de reações das lajes N1: receptores CAD e BIM com W20/R137 e os respectivos controles sem W20/R138, com a mesma malha. Não houve novo processamento nem alteração de cargas, seções ou vínculos.

## Resultado verificável

Cada DXF contém **25 rótulos numéricos de resultado** no nível DI-Textos, 24 rótulos de vigas com q e os seis nomes L1–L6. Os 25 valores coincidem entre CAD e BIM tanto no ensaio com W20 quanto no controle. A inserção de W20 muda 18 dos 25 rótulos nos dois ramos; o maior incremento em módulo nos números exibidos é 1,82. Essa é uma diferença de **rótulos arredondados**, sem interpretação como tolerância ou erro estrutural.

Os nomes das vigas diferem entre CAD e BIM. A comparação usa a posição do texto no desenho, com tolerância gráfica de 0,000001; não trata os pontos de inserção dos textos como coordenadas de aplicação das reações. Os 24 rótulos `Vn[q=...]` são identificadores/cargas lineares indicativas e **não entram** nos 25 resultados. Todos os números têm duas casas decimais.

O painel foi selecionado visualmente em **Adicional (G2)** e a seleção foi capturada nas quatro consultas. O próprio DXF não traz metadado da ação nem unidade física impressa junto aos números. Por isso não se calculou uma integral de força ou momento a partir desses textos. G2 representa a ação inteira; o efeito de W20 é investigado pela diferença entre ensaio e controle de mesma malha.

## Comparação controle → W20

As linhas seguintes são iguais nos ramos CAD e BIM. X e Y são posições **gráficas brutas** dos textos no DXF, sem conversão para pontos físicos de reação. Valores transcritos pela leitura do DXF, sem OCR.

| X, Y gráficos | Controle | Com W20 | Diferença |
|---|---:|---:|---:|
| 0.6354, 3.9 | 1.13 | 1.13 | 0.00 |
| 0.6354, 10.95 | 0.98 | 0.98 | 0.00 |
| 4.4, 0.9531 | 1.02 | 1.02 | 0.00 |
| 4.4, 6.9528 | 0.92 | 0.92 | 0.00 |
| 4.4, 8.7531 | 0.82 | 0.81 | -0.01 |
| 4.4, 13.2528 | 1.07 | 1.07 | 0.00 |
| 7.846900000000002, 2.88 | 1.22 | 1.21 | -0.01 |
| 7.846900000000002, 6.72 | 0.78 | 0.80 | 0.02 |
| 7.846900000000001, 10.95 | 0.81 | 0.82 | 0.01 |
| 9.435400000000001, 6.72 | -0.81 | -0.77 | 0.04 |
| 9.4354, 10.95 | 0.53 | 0.53 | 0.00 |
| 10.9, 6.9528 | 1.07 | 1.24 | 0.17 |
| 10.9, 8.7531 | 1.06 | 1.06 | 0.00 |
| 10.95, 6.6531 | 0.55 | 0.63 | 0.08 |
| 11.9351, 6.6351 | 1.15 | 1.19 | 0.04 |
| 12.1469, 6.75 | -0.25 | -0.80 | -0.55 |
| 13.7354, 2.88 | 1.09 | 2.50 | 1.41 |
| 13.7354, 6.75 | -0.04 | -0.40 | -0.36 |
| 14.05, 13.2528 | 1.00 | 1.03 | 0.03 |
| 16.2, 0.9531 | 0.67 | 1.96 | 1.29 |
| 16.25, 6.9528 | 0.94 | 2.76 | 1.82 |
| 16.25, 8.753099999999998 | 0.53 | 0.13 | -0.40 |
| 18.3469, 3.9 | 1.11 | 2.32 | 1.21 |
| 18.3469, 10.95 | 1.47 | 1.70 | 0.23 |
| 19.9354, 10.95 | 0.95 | 0.94 | -0.01 |

## Consulta da grelha e limite da documentação

Na cópia CAD, a grelha foi consultada em Fletores/G2 e Deslocamentos/G2. Na troca de diagrama, observou-se o retorno da seleção a G1; G2 foi selecionada e conferida novamente. Em Deslocamentos/G2, a legenda exibiu mínimo −0,06 cm e máximo 0,00 cm. Trata-se de valores arredondados da ação completa, não de verificação de flechas em ELS ou de medida isolada do incremento W20.

O duplo clique em uma barra interna da grelha de lajes abriu **Edição da barra**, com multiplicadores 1/1/1; a janela foi cancelada sem edição. As rotações nodais das 11 molas da R139 não foram obtidas. O [artigo oficial da AltoQi](https://suporte.altoqi.com.br/hc/pt-br/articles/360038283234) descreve a consulta de deslocamentos nodais por duplo clique no pórtico, inclusive grelha de paredes; essa descrição não garante a mesma janela na grelha separada de lajes observada nesta versão.

A divergência de momentos da R138 permanece aberta. Esta etapa confirma igualdade dos valores gráficos consultados entre os ramos, mas não identifica sua causa, não fecha o equilíbrio com momentos de molas e não constitui validação normativa ou aprovação estrutural. Não se executou SAP2000. As armaduras anteriormente exibidas na janela de lajes não foram revalidadas nesta consulta.

## Preservação e rastreabilidade

Os 70 arquivos-fonte protegidos de R137/R138 mantiveram seus hashes. Os quatro PRJs consultados também permaneceram idênticos aos respectivos hashes de início. As consultas com W20 usam as cópias 64/65 de R139; os controles usam novas cópias 66/67 de R140. Alterou-se apenas o endereço do PRJ no INI de preparação dos controles. Alterações temporárias dos desenhos gerados foram descartadas ao fechar, mantendo-se os DXFs exportados como evidência independente. Não se editou a monografia nem a autoria RVT/DWG.

As imagens iniciais `CAD-W20-grelha-G2-fletores` foram obtidas enquanto a janela de geração 3D ainda aparecia; ficam somente no arquivo local e não são usadas como prova final. A imagem `CAD-W20-G2-fletores-finalizado` foi capturada depois do término. As demais evidências públicas correspondem às observações concluídas e à janela de edição cancelada.

## Tempos registrados

| Sessão | Minutos decorridos | Início UTC | Fim UTC |
|---|---:|---|---|
| CAD | 12.034 | 2026-11-02T00:41:12.824Z | 2026-11-02T00:53:14.893Z |
| BIM | 2.447 | 2026-11-02T00:53:49.757Z | 2026-11-02T00:56:16.578Z |
| CAD-controle | 2.534 | 2026-11-02T00:58:05.408Z | 2026-11-02T01:00:37.472Z |
| BIM-controle | 4.023 | 2026-11-02T01:01:05.873Z | 2026-11-02T01:05:07.232Z |

São sessões exploratórias de consulta, com navegação, raciocínio, conferência e exportação. A primeira sessão CAD inclui a descoberta do caminho e falhas de interface; as seguintes usam o caminho aprendido. O intervalo CAD inicia antes da abertura do seletor; os demais iniciam após sua seleção, antes de confirmar a abertura. Esses escopos e a ordem de execução impedem interpretar a diferença de duração como vantagem de produtividade. Não houve intervenção humana nesta etapa. Não há tempo puro de solver, tempo isolado de inferência, tokens ou custos medidos. A preparação das cópias e a programação/conferência posterior não estão integralmente incluídas nos quatro intervalos. Os tempos não devem ser somados a contêineres ou intervalos que os englobam.

Na exportação CAD, dois avisos de nome inválido ocorreram durante a correção do caminho e do foco; o DXF final foi gravado e lido. No controle BIM, um comando chegou ao aviso de salvar desenho: cancelou-se e repetiu-se a exportação. Essas ocorrências pertencem ao esforço de operação da interface, não a defeitos de interoperabilidade CAD/BIM.

## Verificação do auditor

Três testes passaram: igualdade dos arquivos reais apesar da renumeração de vigas; detecção de uma mudança de sinal com a mesma quantidade de rótulos; e rejeição de um diagrama com resultado ausente. São testes do leitor/comparador de evidências, não validação estrutural nem ensaio dentro do Revit ou AutoCAD. A abertura, seleção de G2 e exportação dos diagramas foram observadas no Eberick.

## Próxima verificação

Buscar um recurso documentado para rotações/reacções nodais da grelha separada e confrontar o incremento com o controle. Enquanto essa consulta estiver pendente, manter W20 como ensaio parcial. Podem avançar em paralelo lógico, sem mudar os modelos, a organização das evidências, o inventário de pendências e o protocolo prospectivo de tempo dos dois fluxos.

# H03/R161 — recepção e revisão parcial da R160

Data: 02/11/2026. Estudo de superestrutura. NÃO EXECUTAR.

## Resultado efetivamente verificado

A cópia CAD do Eberick recebeu um nível intermediário em N1 e somente a viga V16 entre P4 e P10. A viga conserva a hipótese de seção 20 × 30 cm, com elevação local zero. Não se adicionou P12 ou P13. A gravação foi realizada pelo botão Salvar, seguida de fechamento, reabertura e consulta das propriedades da viga e do nível.

O campo aceitou o separador decimal ponto. A tentativa com vírgula foi recusada e corrigida antes da criação. Pediu-se altura de 157,4117647 cm em relação a N0; a releitura nativa mostra 157,4 cm e nível absoluto 177,4 cm. O IFC4 de controle mostra topo +1,774 m, diferença de −0,117647 mm em relação ao topo do Revit +1,774117647 m. Essa diferença permanece explícita no auditor, com tolerância geométrica declarada de 0,2 mm em Z. A tolerância não constitui aprovação normativa.

O sólido da V16 mede 1,95 m entre faces de pilares; a distância nominal entre os eixos P4–P10 é 2,15 m. O auditor compara as faces correspondentes, sem tratar a diferença como encurtamento indevido e sem inferir conectividade analítica. O IFC contém 22 sólidos de pilares com 11 nomes distintos, P1–P11, dois trechos por nome; 46 sólidos de vigas e 11 lajes. A segmentação das vigas anteriores não foi reclassificada como erro pela contagem. Nenhum IfcStair/IfcStairFlight consta dessa saída do Eberick.

## Arquivos de trabalho

- Eberick CAD parcial: `D:\TCC\outputs\R161-CAD-REVISAO-R160-NAO-EXECUTAR\Projeto Eberick\H03_CAD_R49_LAJES_NAO_EXECUTAR.prj`.
- Cópia BIM ainda intacta: `D:\TCC\outputs\R161-BIM-REVISAO-R160-NAO-EXECUTAR\Projeto Eberick\H03_BIM_R46_IFC_NAO_EXECUTAR.prj`.
- Evidências: `D:\TCC\outputs\Intercambio-H03-R161-R160-NAO-EXECUTAR`.
- IFC4 de controle do Eberick: `IFC-CAD-Eberick\Modelo 3D.IFC` dentro da pasta de evidências. Não é o IFC nativo exportado do Revit.
- Revit e três formas DWG atuais continuam na pasta `D:\TCC\outputs\Escada-H03-R160-SOMENTE-VIGA-NAO-EXECUTAR`.

As duas referências R148 permanecem com os hashes originais. A cópia CAD salva/reaberta foi congelada com manifesto próprio. Antes de salvar o estado pendente do receptor experimental R159 para trocar de projeto, preservou-se uma cópia de seus 15 arquivos. Seu PRJ e BAK mudaram nesse salvamento; não se atribuiu a mudança a alteração estrutural. O congelamento anterior R159 continua preservado.

## Tempo e esforço observados

O intervalo da seleção do arquivo CAD de trabalho até a observação após Salvar pela barra foi 392.668 ms, ou 6 min 32,668 s. Inclui abertura, edição recusada/corrigida, criação do nível, tentativa cancelada de importar DWG, lançamento da V16, navegação, conferências e tentativas de salvar. A primeira observação após Ctrl+S, aos 354.990 ms, não confirmou gravação no disco; não é um segundo intervalo somável.

A cópia técnica dos diretórios levou 667,5686 ms e não representa um fluxo de projeto. O intervalo entre Gerar IFC e a observação de retorno à interface foi 1.413 ms; não mede exclusivamente o exportador e não cobre toda a preparação/conferência da exportação. Os registros UTC e escopos estão em `R161-tempos-parciais.json` e no arquivo de preparação das cópias. Não se calculou vantagem percentual CAD/BIM. Não houve nova chamada paga à IA medida nesta revisão; uso total de créditos não foi medido por esses scripts.

## Etapas ainda pendentes

1. Exportar o IFC nativo da R160 no Revit. A configuração CV preparada não foi aplicada nem relida nesta revisão. O arquivo esperado pelo auditor ainda não existe. A R159 anterior apresentou ausência de propriedades mecânicas, apesar da opção de materiais habilitada; não se presumiu o mesmo resultado para a R160.
2. Importar a referência DWG revisada. O seletor foi aberto por QiCadViewer.exe e o controle recusou o clique por pertencer a outro processo sem janela enumerada. O seletor foi cancelado com Escape. A V16 foi lançada usando os nós P4/P10 já existentes, sem declarar importação DWG concluída.
3. Aplicar a revisão V15/L6 do pavimento superior e a escada/patamar ao modelo de cálculo. A cópia CAD não contém ainda toda a geometria comum R160.
4. Medir a recepção BIM e suas correções a partir do novo IFC, preservando o bruto. A cópia BIM R161 continua sem alteração.
5. Resolver a compatibilização com J4 sem alterar paredes, portas ou janela por iniciativa automática. Conferir apoios, continuidade, torção, altura livre, cargas, ELU/ELS e armaduras. A escada não está integrada ao cálculo. Os resultados herdados foram invalidados na cópia CAD e não se efetuou novo cálculo nesta etapa.

## Validação e reprodução

No diretório deste estudo: `python -m unittest -v test_auditoria` passou 13 testes. Em `tcc-assistente`, `npm test` passou 81 testes, sem falhas ou saltos. Esses testes cobrem código e não substituem o ensaio dentro dos programas.

`auditar_cad_eberick.py` executou sobre o IFC4 real e as releituras nativas, preservando os hashes das fontes. `auditar_exportacao.py` está preparado para o IFC do Revit e ainda não executou sobre uma exportação R160. Usa leitura numérica derivada da R94, com proveniência em `R161-preparacao.json`; ausência de propriedade permanece ausente, sem virar zero.

Referência operacional consultada: AltoQi, [inserção de nível intermediário](https://suporte.altoqi.com.br/hc/pt-br/articles/115002186654). O procedimento foi confirmado na instalação Eberick 2025, e a altura foi relida no arquivo salvo.

Nenhuma parte desta revisão constitui aprovação estrutural, conclusão do TCC ou resultado final de desempenho entre os fluxos.

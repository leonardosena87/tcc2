# Entrega parcial H03 para revisão do orientador — R76

**NÃO DIMENSIONADO — NÃO EXECUTAR.** Pacote local de 29/10/2026, preparado para revisão parcial e ainda não enviado a terceiros. A monografia foi preservada. O conjunto apresenta os dois fluxos com automação e o estado parcial dos receptores no Eberick.

## Arquivos principais

- [Revit H03/R43](outputs/Alternativa-H03-R43-ESTUDO-NAO-EXECUTAR/H03-R43-Revit.rvt)
- [AutoCAD H03/R43](outputs/Alternativa-H03-R43-ESTUDO-NAO-EXECUTAR/H03-R43-AutoCAD.dwg)
- [Eberick CAD/R64](outputs/H03_CAD_R64_CONFERENCIA_INDIVIDUAL_NAO_EXECUTAR/Projeto%20Eberick/H03_CAD_R49_LAJES_NAO_EXECUTAR.prj)
- [Eberick BIM/R64](outputs/H03_BIM_R64_CONFERENCIA_INDIVIDUAL_NAO_EXECUTAR/Projeto%20Eberick/H03_BIM_R46_IFC_NAO_EXECUTAR.prj)
- [Arquitetura original de referência](arquitetura/PROJETO%20ARQUITETONICO-A0.pdf)
- [Resultados parciais e matriz de fechamento R72](outputs/Resultados-H03-R72-PARCIAIS-NAO-FINAIS/LEIA-ME-R72.md)
- [Figura dos dois fluxos](outputs/Resultados-H03-R75-FIGURA-PARCIAL/R75-fluxos-resultados-parciais.png)
- [Conferência normativa e versão instalada R74](outputs/Normativa-H03-R74-TRIAGEM-NAO-DIMENSIONADO/LEIA-ME-R74.md)
- [Tempos exploratórios e limites R69](outputs/Resultados-H03-R69-TEMPOS-EXPLORATORIOS/LEIA-ME-R69.md)

## Revisões e conteúdo dos modelos

O RVT e o DWG correspondem à autoria R43, anterior aos ajustes efetuados no receptor. Os Eberick R64 contêm complementação de lajes, parâmetros de materiais e durabilidade, apoios idealizados, hipótese de continuidade da varanda, vigas N2 com 30 cm na R56 e cargas parciais. Esses ajustes **ainda não foram sincronizados de volta ao Revit e ao AutoCAD**. A altura mostrada na origem ou em texto CAD antigo pode diferir da seção atual do receptor.

As pastas e os manifestos identificam a revisão. Os nomes-base dos PRJ permanecem R49/CAD e R46/BIM para conservar seus recursos associados; a pasta R64 identifica o estado entregue. A estrutura de cada ramo é independente. Não se copiou o receptor de um fluxo para completar o outro.

O programa de cálculo instalado é o **Eberick 2025-04 [v. 18.306], Infinity**, confirmado em Ajuda → Sobre. A autoria utilizou Revit 2027.2 e AutoCAD 2027, conforme as etapas anteriores. Não se comprovou a implementação integral da NBR 6118:2026 nessa instalação do Eberick. A alteração de redistribuição documentada pelo fornecedor em versão posterior está registrada na R74. Não houve atualização do programa nesta entrega.

## Resultados já sustentados pelas evidências

O CAD recebeu 62/62 contornos e 66/66 conteúdos de texto como referência gráfica. Após adaptação explícita do IFC, o BIM recebeu 22 trechos de pilares e 29 vigas lógicas, sem as 11 lajes nativas. Posteriormente, complementaram-se 62 unidades lógicas no CAD e 11 no BIM. Esses números não representam contagem de erros, cliques ou minutos.

O checkpoint R56/R57 apresenta 65 pares geométricos correspondentes: 22 trechos de pilares, 32 sólidos de viga para 29 vigas lógicas e 11 lajes. Os IFC de controle incluídos correspondem a esse checkpoint, sem nova exportação na R64. As 26 leituras individuais da R64 conferiram 13 pontos de carga permanente parcial de telhado em cada ramo, coincidentes nos campos exibidos auditados. O último processamento efetivo foi a R63, com cargas incompletas; a R64 conferiu e preservou esse estado.

Os tempos disponíveis são exploratórios e delimitados. Ainda não existe tempo final completo comparável, percentual de vantagem ou vencedor. Não se somaram intervalos sobrepostos. O inventário R69 é um índice histórico de 112 arquivos no recorte daquela revisão; não corresponde a 112 ensaios e não inclui todos os registros posteriores. Nem todos os arquivos históricos citados nos relatórios estão neste pacote.

## Entradas e verificações ainda abertas

Falta aplicar e conferir a ação variável do telhado e completar P1/P2, paredes, aberturas e vergas, escada e guarda-corpo, vento e combinações, peso completo e apoio do reservatório de 1.000 L, ligações e rigidezes, além dos resultados ELU/ELS. A varanda de 14 cm exige conferir a aplicação única de γn = 1,25 aos esforços finais de dimensionamento; isso não significa aumentar 25% o peso global. O reservatório tem alternativas dimensionais e de base, ainda sem solução selecionada ou dimensionada.

A redução de altura das vigas N2 preserva geometricamente o forro, mas a folga de 4 cm não comprova atendimento de flecha, instalações, faces ou capacidade. A parede W08/J4 da escada requer solução de apoio que preserve o vão. A referência da porta P3 foi refinada na R68, sem deslocar pilar ou alterar a arquitetura. A matriz de 12 frentes da R72, com o complemento R74, estabelece critérios para concluir o estudo; não representa 12 defeitos por ramo.

Sem sondagem, o recorte permanece na superestrutura com apoios idealizados. Os 11 IfcFooting auxiliares por ramo não são fundações dimensionadas. Não se produziram armaduras finais ou liberação para execução.

## Abertura e limites de verificação do pacote

Extrair o ZIP inteiro, preservando a pasta `outputs` e seus subdiretórios. Manter o PRJ com os arquivos associados. O IFC adaptado R44, o cache 3D e o arquivo de vínculo relativo do BIM estão incluídos; o destino relativo foi resolvido e conferido dentro da entrega.

Os metadados do gerenciador em `_DADOS_/ConfigFolder.qib` e `EdificacaoEberick.ini` conservam caminhos absolutos históricos. Foram preservados sem edição do formato binário ou presunção de suporte a caminhos relativos. Ao abrir no Eberick, selecionar o projeto da pasta **extraída** e conferir o caminho ativo. Se o gerenciador apontar para a pasta original em `D:TCC` ou mostrar vínculo ausente, reassociar a cópia pelo próprio programa antes de salvar. A conferência do vínculo por arquivo não equivale a teste de portabilidade em outro computador.

Nesta embalagem, conferiram-se cópias por SHA-256, integridade dos PRJ como contêineres ZIP e CRC e hashes das entradas do ZIP de entrega. **Não se repetiu a abertura dos RVT, DWG e PRJ deste pacote nos aplicativos nem se testou outra máquina.** A dificuldade atual de controlar o seletor do Eberick foi registrada na R73 e essa etapa foi pulada conforme orientação do usuário.

As origens permaneceram intactas. O pacote não contém a coleção de normas, credenciais, dependências instaladas ou logs internos. O manifesto identifica os arquivos e suas fontes para rastreabilidade; não representa aprovação técnica.

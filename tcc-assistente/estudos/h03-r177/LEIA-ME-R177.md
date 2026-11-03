# H03/R177 — integração experimental da escada no Eberick

**Estudo preliminar — não executar.** Esta revisão lança patamar e dois lances nos receptores independentes CAD e BIM. Não conclui o dimensionamento, as verificações normativas ou a comparação integral dos fluxos. SAP2000 não foi executado: foram lidos os arquivos textuais que o Eberick exportou nesse formato.

## Desenvolvimento realizado

Partiu-se das cópias CAD R172 e BIM R175, preservadas por SHA-256. Adicionou-se no Eberick o patamar LE1 na cota de concreto +1,774 m, o lance inferior LE3 e o superior LE2, na escada E1. Adotou-se espessura preliminar de 14 cm, pisada de 28 cm, espelho informado de 17,825 cm, carga acidental de 2,5 kN/m² e revestimento provisório de 1,0 kN/m². A carga de revestimento ainda exige especificação e conferência; não se encerrou a verificação de guarda-corpos e cargas concentradas.

A viga V16 permanece entre as posições existentes dos pilares. Os objetos AE1A e AE1B são marcadores numéricos de apoio inferior, representados pelo comando nativo “Fundação sem pilar de arranque”, com dimensões gráficas de 20 × 20 × 20 cm. Essas dimensões **não constituem projeto de fundação**. Não se adicionou uma nova prumada física de pilar para o patamar. O TCC continua delimitado à superestrutura.

O ensaio inicial BIM com base rotulada apresentou erro de precisão de 8,29% na direção Y do caso 9. O ensaio seguinte com engastamento na base dos dois marcadores processou com avisos; a mesma hipótese foi reproduzida no CAD. A obtenção de solução numérica não justifica, por si só, esse vínculo físico. A hipótese de engastamento e a transmissão de esforços na base continuam sujeitas à revisão e ao estudo de sensibilidade.

## Evidências obtidas

| Exportação por receptor | Nós | Barras |
| --- | ---: | ---: |
| Pórtico | 135 | 170 |
| Grelha da escada | 284 | 375 |
| Grelha da laje N1 | 469 | 840 |
| Grelha da laje N2 | 443 | 794 |

Nos quatro pares, coincidem os conjuntos de coordenadas, os segmentos sem considerar o sentido I–J e as propriedades de seção por segmento. As tabelas de restrições nodais também coincidem após associar os nós pela posição. Permanecem diferenças de orientação I–J, de representação das cargas distribuídas e pontuais e pequenos resíduos em cargas nodais. Portanto, **não se declarou equivalência analítica completa**.

As cinco peças LE1, LE2, LE3, AE1A e AE1B apresentam classes, limites geométricos e cotas das faces horizontais superiores coincidentes nas duas exportações IFC. Essa conferência não compara integralmente a triangulação ou todos os atributos do modelo. Os atributos IFC de número e altura dos degraus foram exportados vazios ou zerados; a contagem foi obtida das faces geométricas, independentemente desses campos.

Foram medidos nove espelhos no lance inferior e oito no superior. Considerando acabamento de 2 cm no térreo e de 5 cm na escada, o primeiro espelho acabado mede 17,800 cm e os demais 17,825 cm. A meta exata para 3,03 m em 17 espelhos é 17,823529 cm. A maior diferença em relação à meta é 0,023529 cm (0,235294 mm). O teste geométrico interno usa tolerância de 0,020 cm e permanece **reprovado**; essa tolerância é um critério de auditoria, não um limite normativo citado. Não se alterou a tolerância para aprovar o resultado.

O patamar exportado pelo Eberick ocupa X = 4,40 a 6,55 m. A referência física do Revit R160 ocupa X = 4,50 a 6,45 m. A leitura nativa das barras laterais confirmou 20 cm, mas essa configuração não corrigiu o contorno exportado. A frente do patamar apresenta ainda diferença aproximada de 2,59 cm em planta. A reconciliação entre eixos analíticos e faces físicas permanece pendente. Preservou-se a versão salva; um relançamento exploratório anterior do BIM foi descartado sem salvar.

Nos resultados nativos de análise parcial, os dois receptores exibiram peso próprio de 78,98 tf, adicional de 12,60 tf, acidental de 18,49 tf e Q_TELHADO_MANUTENCAO de 1,78 tf, total de 111,85 tf. O programa manteve aviso de relação de carga por área não usual. O relatório de precisão da execução com apoios engastados informa “Nenhuma diferença encontrada”. Isso representa apenas a verificação numérica executada pelo programa, sem aprovação estrutural.

## Tempos registrados e limites da comparação

| Registro | CAD | BIM | Uso permitido |
| --- | --- | --- | --- |
| Tempo total nativo da análise parcial documentada | 5 s | 4 s | Uma execução por receptor; resolução de segundos; não mede produtividade integral |
| Segmento observado de lançamento | 3 min 53,658 s | 22 min 8,561 s | Escopos diferentes; **não comparar como total de fluxo** |
| Exportação analítica CAD, incluindo escolha da pasta e observação | 1 min 1,433 s | Sem novo segmento pareado equivalente | Registro operacional parcial |

O segmento CAD começa com patamar, apoios e comando inferior já preparados; inclui conclusão do lance inferior, referências e lançamento superior. O segmento BIM inclui preparação de barras, patamar, dois lances e apoios, além de consultas e interrupções. O intervalo entre retomadas não foi convertido em tempo produtivo. A diferença de 1 s de processamento não permite classificar um fluxo como superior. O tempo integral CAD/BIM e o esforço de correção de ponta a ponta ainda precisam ser consolidados com escopos equivalentes.

## Ocorrências operacionais preservadas

A primeira emissão de mensagens CAD falhou por ausência de pasta da edificação. Salvou-se uma cópia de segurança do PRJ, regravou-se a cópia experimental, criou-se o diretório de documentos, reabriu-se e reprocessou-se o projeto. O relatório novo foi então gerado em `R177-CAD-ESCADA17-NAO-EXECUTAR/Arquivos do projeto/Documentos/Eberick`. Um relatório BIM antigo ainda aberto no Word foi identificado pelo caminho da caixa “Salvar como”; não foi usado para atribuir duração ao CAD. O arquivo de captura dessa tentativa possui nota de origem que o exclui como evidência CAD.

## Conferência reproduzível

Executar `python -m unittest discover -s tcc-assistente/estudos/h03-r177 -p "test_*.py" -v`. Os oito testes exercitam contagem, acabamento, uniformidade, cota efetiva do patamar, ausência de faces, vínculos e distinção entre grelha de escada e laje no mesmo nível. São testes locais de leitura e auditoria; não são execução de IA nem dimensionamento estrutural.

Executar `comparar_escada.py` para ler dois IFCs e oito arquivos textuais nativos, verificar integridade ZIP dos PRJs e preservar 15 arquivos da fonte CAD e 21 da BIM por hash. O resultado é salvo em `D:/TCC/outputs/Escada-H03-R177-INTEGRACAO-EBERICK-NAO-EXECUTAR/R177-comparacao-CAD-BIM.json`. `visualizar_escada.py` gera o recorte da geometria e a sobreposição do patamar em PNG.

## Pendências seguintes

Reconciliar o contorno do patamar com a referência Revit; conferir a interface dos 3 cm e o arredondamento dos espelhos; justificar os vínculos inferiores idealizados; verificar interferência V16/J4, altura livre, apoios e acabamentos; concluir cargas e dimensionamento, incluindo ELS e detalhamento; comparar esforços e cargas em referência comum; consolidar tempos e correções com fronteiras equivalentes. A integração desta revisão não encerra essas verificações.

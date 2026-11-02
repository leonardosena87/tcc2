# R161 — IFC nativo da R160 exportado e auditado

Atualização em 02/11/2026, após a etapa CAD parcial. Estudo não dimensionado; NÃO EXECUTAR.

## Exportação efetivamente concluída

O Revit 2027.2 exportou `H03-R160-Revit-SOMENTE-VIGA-PATAMAR-NAO-EXECUTAR.ifc` para `D:\TCC\outputs\Intercambio-H03-R161-R160-NAO-EXECUTAR`. O diálogo foi aberto pelo usuário. Somente o projeto R160 estava selecionado; a R159 permaneceu desmarcada. Importou-se a configuração preparada e salvou-se sua releitura nativa. Todos os campos funcionais coincidem; o comando Salvar configuração usa o nome do arquivo como Name da cópia JSON relida. O RVT permaneceu com o hash previamente auditado.

Configuração: IFC2x3 Coordination View, propriedades comuns e de materiais habilitadas, sem limitar os elementos à vista atual ou usar sua geometria, sem dividir pilares por nível e sem gravar GUIDs no RVT. Mapeamento de propriedades = configuração na sessão. Nenhum mapeamento novo foi aplicado nesta exportação de controle.

O arquivo bruto preserva 63 identidades da edificação: 22 trechos de pilares, 30 vigas e 11 lajes. A laje adicional exportada como LANDING é o patamar agregado da escada, não uma laje duplicada da edificação. Os IDs dos dois pilares rejeitados estão ausentes. A V16 tem limites X=4,50–6,45 m, Y=−0,10–+0,10 m e Z=1,474117647–1,774117647 m. A comparação das caixas com o Eberick CAD mostra igualdade em planta dentro da precisão numérica e diferença de −0,117647 mm em Z. Isso não verifica as ligações analíticas.

## Qualidade das informações

Há nome de material associado aos 63 elementos, mas nenhuma entidade IfcMaterialProperties e nenhuma resistência de compressão legível e correspondente aos 25 MPa da releitura nativa. Ausência não foi tratada como resistência zero. Essa constatação não identifica, isoladamente, a causa da omissão nem demonstra como o Eberick atribuirá seu próprio concreto.

Os lances mantêm as contagens 9+8 espelhos e 8+7 pisadas, com largura geométrica de 0,90 m. O Pset_StairFlightCommon registra RiserHeight=178,235294117647 mm e TreadLength=280 mm, correspondentes às medidas nativas. Os atributos diretos de IfcStairFlight contêm 0,5847614636405744 e 0,9186351706036745, numericamente compatíveis com pés, enquanto a unidade de comprimento declarada no projeto IFC é milímetro. Aplicada essa unidade, os atributos não correspondem à escada nativa. O bruto foi preservado sem correção silenciosa. Não se inferiu deformação da malha ou comportamento do receptor a partir dessa divergência.

A documentação da Autodesk informa que o painel de [mapeamento de propriedades IFC](https://help.autodesk.com/cloudhelp/2027/ENU/Revit-DocumentPresent/files/GUID-97F362CD-BB45-4609-8EC6-1CCBDE854542.htm) controla conjuntos exportados e mapeamentos entre propriedades IFC/Revit. Uma nova configuração pode ser investigada em variante separada; não se demonstrou que esse painel causou a omissão observada. A referência histórica IFC2x3 indicada no auditor retornou HTTP 403 nesta consulta; a comparação dimensional executada usou o esquema e as unidades efetivamente lidos pelo IfcOpenShell no arquivo local.

## Comparação com a exportação anterior R159

Removeram-se exatamente os dois produtos IfcColumn com Tags 473797 e 473798, sem adicionar produtos às classes examinadas. Entre 66 produtos comuns — elementos da edificação, patamar agregado e dois lances — 63 conservam a nuvem de vértices arredondada a oito casas em metros. Os dois lances mantêm suas nuvens.

Três produtos apresentam diferenças: V16-ESC-PAT (473802), V9-N1 (472976) e V13-N1 (472984). Na V16, o eixo transversal mudou da posição anterior para Y=0, conforme solicitado. Em V9-N1 e V13-N1, os limites externos permanecem iguais, mas a malha exportada difere: o volume absoluto calculado a partir da triangulação aumenta aproximadamente 0,0198 m³ em cada uma. O teste de arestas fechadas e orientação consistente passou nessas malhas. A relação com ajustes automáticos de união/corte é uma hipótese; a causa não foi isolada. Igualdade de nuvens ou fechamento de arestas não prova equivalência completa de sólidos, conectividade ou capacidade estrutural.

## Tempos e limites

Da abertura de Modificar configuração até a observação após a exportação decorreram 200.065 ms (3 min 20,065 s). Dentro desse intervalo, o clique Exportar até a observação de retorno à interface levou 6.302 ms. São intervalos contidos; não devem ser somados. A abertura manual do diálogo ocorreu antes do cronômetro. A auditoria do arquivo levou aproximadamente 0,283 s de script, registrada separadamente. Nenhum desses tempos representa o fluxo BIM completo ou exclusivamente o processamento do exportador.

## Recepção bruta concluída, correções pendentes

O primeiro diálogo apresentado era de edificação simples e foi cancelado sem criar projeto. Em seguida, o submenu correto foi acionado e a R160 foi recebida em `D:\TCC\outputs\R161-R160-IFC-BRUTO-NAO-EXECUTAR`. Utilizou-se a configuração inicial do programa e conservaram-se nove níveis do assistente, com Importar pilares e vigas marcado. O aviso sobre seções retangulares foi preservado. O estado inicial salvo foi congelado antes da exportação de controle.

O relatório nativo lista 52 origens: 30 vigas e 22 trechos de pilares, sem ID ausente, duplicado ou desconhecido nesse conjunto. A V16 consta no relatório; os dois pilares rejeitados não constam. O IFC4 de controle contém 31 partes de vigas e 64 partes de pilares, sem lajes ou escada nativas. A contagem de partes não equivale à contagem de elementos físicos ou erros. A presença de objetos no modelo externo não comprova sua conversão para cálculo.

Associaram-se espacialmente 29 partes a 28 origens de vigas. Duas partes ficam sem associação por ultrapassarem os limites nominais longitudinais; V9-N1 e V13-N1 permanecem sob investigação. Entre as origens associadas, 12 diferem de seus parâmetros nominais em topo/altura. A comparação de três etapas mostrou que os 12 rebaixamentos de topo já existem no IFC bruto do Revit. O receptor conserva esses topos. V4A-N1 e V15-N1 têm caixas de malha de 2 cm de altura no bruto e de 5 cm no receptor, diferença adicional de 3 cm. Não se isolou o algoritmo responsável nem se tomou caixa envolvente de sólido recortado como seção analítica.

A viga do patamar foi renomeada V1 no receptor. Seu croqui e a consulta nativa confirmam 20 × 30 cm, elevação local zero. O IFC de controle apresenta topo +1,77411765 m, correspondente ao topo de origem dentro da precisão observada. Os nomes dos pilares também mudaram: a ligação frontal aparece entre P9/P10 no receptor, embora a origem comum seja P4/P10; essa renumeração não indica novos pilares.

Da seleção do IFC ao primeiro salvamento observado decorreram 204.681 ms (3 min 24,681 s). A abertura/correção do assistente precede esse cronômetro. O clique Gerar IFC4 até a observação da interface levou 1.054 ms; preparação e auditoria não estão nesse intervalo. Esses registros são parciais e não permitem classificar os fluxos.

O auditor de recepção executou sobre relatório e IFC4 reais. O PRJ continuou igual ao primeiro salvamento durante as consultas; a R148 CAD/BIM e a cópia BIM R161 ficaram intactas. O receptor experimental não foi processado estruturalmente nem promovido ao modelo final de cálculo. A lista de pendências está em `R161-pendencias-recepcao-bruta.md`, e a separação entre nominal, bruto e receptor está em `R161-vigas-comparacao-tres-etapas.json`.

A cópia CAD R161 contém somente o nível e a V16 atualizados. A revisão de V15 e da laje de circulação, os elementos nativos da escada e suas cargas permanecem pendentes. A candidata espacial à L6-N1 do Revit é L5 no receptor CAD; a L6 desse receptor está em outra posição. A cópia BIM derivada da R148 continua intacta. Não se concluiu a comparação de correções e tempos dos dois fluxos, nem houve novo cálculo estrutural.

## Evidências e validação

`R161-IFC-auditoria.json`, `R161-resultado-IFC.json`, `R161-IFC-comparacao-R159-R160.json`, `R161-IFC-exportacao-observacao.json` e `R161-configuracao-IFC-releitura-nativa.json` documentam esta etapa. O conjunto de 26 testes Python passou; o teste nativo do Revit e as auditorias sobre os IFCs reais são evidências separadas. Os 81 testes Node passaram na etapa anterior da R161; o código Node não mudou nesta continuação. Não houve chamada paga à IA medida nesta etapa.

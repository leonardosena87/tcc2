# H03/R94 — retenção de propriedades na exportação IFC

A exportação real da mesma autoria R93 produziu três arquivos IFC2X3. Associou-se cada elemento pelo `Tag` ao ID da leitura nativa R93, conferindo a classe e o único material associado. Não se alterou o projeto do Eberick nesta etapa.

| Ensaio | Vista | ExportMaterialPsets | Elementos | Nome do material associado | Compressão / Young / densidade / Poisson iguais ao autor |
|---|---|---:|---:|---:|---:|
| CONTROLE | Coordination View 2.0 | false | 62 | 62 | 0 / 0 / 0 / 0 |
| MATERIAIS | Coordination View 2.0 | true | 62 | 62 | 0 / 0 / 0 / 0 |
| MATERIAIS-CV | Coordination View | true | 62 | 62 | 62 / 62 / 62 / 62 |

Em todos os arquivos há 22 trechos de pilares, 29 vigas e 11 lajes. Os dois primeiros não contêm nenhuma entidade `IfcMaterialProperties`. O terceiro contém 26 entidades dessa família, incluindo conjuntos `Structural`, nos quais se confirmou a compressão de 25 MPa em ambos os materiais. O módulo de Young é 20.500 MPa nas lajes e 23.250 MPa nas vigas/pilares; a densidade é 2.406,4537 e 2.407,31172 kg/m³, respectivamente. São os valores cadastrados, ainda sem alinhamento integral ao cálculo. Não se interpreta Young automaticamente como Eci/Ecs, nem o conjunto de propriedades herdadas como confirmação de aço CA-50.

## Procedimento e controle

Preservou-se a R93 e exportou-se apenas esse documento pelo diálogo IFC do Revit 2027.2, build 27.2.0.39. A cópia histórica R92 aberta na sessão ficou desmarcada. Mantiveram-se coordenadas compartilhadas, mesmo sítio, seleção de todo o modelo, divisão por níveis desativada e armazenamento de GUID no autor desativado.

Após o controle, preparou-se uma variante do JSON alterando somente `Name` e `ExportMaterialPsets`. Importou-se o arquivo pelo diálogo nativo e salvou-se uma leitura de volta (`ATIVA`), que confirmou a opção true. A opção também apareceu marcada no gerenciador de propriedades. O segundo IFC continuou sem propriedades mecânicas. No terceiro ensaio mudou-se a vista de coordenação pelo diálogo; a leitura de volta registra também a mudança dependente de `ExchangeRequirement`, de 0 para 3. Portanto, o terceiro ensaio compara a configuração da vista e seu requisito associado, sem alegar isolamento causal de um único campo interno.

A documentação oficial descreve o mapeamento gráfico de propriedades disponível no Revit 2027 ([Autodesk — IFC Parameter Mapping](https://help.autodesk.com/cloudhelp/2027/ENU/Revit-WhatsNew/files/GUID-C057D715-1571-4D11-8F02-417F3B385577.htm)). O código público do exportador condiciona a exportação de propriedades de materiais à permissão da vista, e a tabela instalada não inclui `IfcExtendedMaterialProperties` na lista da CV2.0. Essa é uma explicação compatível com os resultados, sem prova de equivalência entre a DLL instalada e o código público. O hash local, a revisão pública consultada e o [arquivo-fonte oficial](https://github.com/Autodesk/revit-ifc/blob/7fe314fddf1a6052823bf41ce8cfeeca935efae1/Source/Revit.IFC.Export/Utility/MaterialPropertiesUtil.cs) constam em `R94-metodo-e-limites.json`. Nenhum arquivo da instalação foi alterado.

O auditor usa IfcOpenShell 0.9.0post1, identifica ausência e ambiguidade, lê o tipo da medida e sua unidade explícita ou a unidade de projeto, converte pressão para MPa e densidade para kg/m³ e compara os valores à leitura real R93. A primeira execução do auditor aplicou um fator de massa incorreto: o auxiliar da dependência retornou 1000 para KILO GRAM, cujo destino em kg exige fator 1. Corrigiu-se a conversão recursiva da unidade derivada e incluiu-se teste específico. O relatório preliminar foi preservado com nome explícito na pasta local; **usar somente `R94-auditoria-FINAL.json`**. Essa ocorrência é correção do instrumento de análise, não defeito de unidade demonstrado no IFC.

## Geometria e limites

As 62 malhas foram lidas em coordenadas globais, em metros, verificando fechamento e orientação das faces. A representação canônica dos triângulos, com coordenadas arredondadas a nove casas decimais, coincidiu elemento a elemento entre os três arquivos. A soma dos volumes individuais das malhas é 27,9009 m³ em todos eles. Não se calculou a união dos sólidos nesta revisão; a soma não é apresentada como quantitativo executivo. Igualdade das malhas entre as exportações não valida conexões, modelo analítico, armaduras, cargas ou ELU/ELS.

A descrição exportada do ativo de vigas/pilares ainda menciona o padrão antigo de 3,5 ksi, embora o campo numérico de compressão seja 25 MPa. Há também campos herdados de tensões mínimas. Esses metadados exigem revisão; não se afirma qualidade integral do material apenas pela retenção de quatro números. Os nomes genéricos dos materiais foram preservados.

O teste comprova conteúdo nos arquivos exportados. **Não comprova que o Eberick importe, interprete ou use esses valores.** A vista alternativa permanece ensaio separado e não substitui o intercâmbio principal até a conferência no receptor e da normalização geométrica/espacial exigida pelo estudo. Não se reprocessaram os dois projetos, não se fecharam cargas e não se declarou vencedor CAD/BIM. O texto acadêmico permaneceu intacto.

## Tempos e reprodutibilidade

Os arquivos `R94-tempo-exportacao-*.json` mantêm recortes do clique Exportar até observações posteriores. São limites superiores observados com intervalo entre chamadas, sem duração interna exata e sem todo o preparo dos diálogos. Não se somam ao inventário como novos totais CAD/BIM e não sustentam comparação de velocidade entre as três configurações. `auditScriptSeconds` mede somente a análise local dos arquivos; não é tempo do fluxo nem esforço isolado da IA. Os recortes de correção nativa da R93 permanecem separados.

Executaram-se nove testes IFC sintéticos em memória: associação sem propriedade, pressão em Pa, unidade explícita MPa, ausência de unidade, kg/m³, Tag repetida, material divergente, valor divergente e valor nativo indisponível. Todos passaram. O ensaio real consiste nas três exportações do host e na leitura dos arquivos resultantes; nenhum teste foi executado dentro do Eberick nesta revisão.

Para reproduzir, utilizar Python 3.12 com IfcOpenShell e NumPy compatíveis. Dependências instaladas ficam fora do repositório. Exemplo nesta estação:

```powershell
$env:PYTHONPATH='D:\TCC\work\ifc\deps'
& 'C:\Users\leona\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tcc-assistente/estudos/h03-r94 -p test_intercambio.py -v
& 'C:\Users\leona\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tcc-assistente/estudos/h03-r94/auditar_intercambio.py --deps D:/TCC/work/ifc/deps --native tcc-assistente/estudos/h03-r93/R93-leitura-final.json --folder D:/TCC/outputs/Intercambio-H03-R94-MATERIAIS-IFC --out D:/TCC/outputs/Intercambio-H03-R94-MATERIAIS-IFC/R94-reproducao.json
```

O comando recusa sobrescrever o relatório. A auditoria confirmou os hashes dos quatro arquivos de entrada antes e depois da leitura. Os IFC e RVT permanecem em `D:/TCC`; o repositório contém apenas código, configurações, dados de conferência e instruções.

# Auditor de materiais do Revit 2027

Comando independente, somente de leitura, preparado para fechar a lacuna de procedência R87. Não substitui nem recompila os suplementos existentes. Não inicia transações, não atribui materiais, não salva o RVT e não chama serviços de IA.

O comando coleta os candidatos locais de pilares estruturais, estruturas e pisos. Para famílias, lê `FamilyInstance.StructuralMaterialId`; para pisos, a camada `CompoundStructure.StructuralMaterialIndex`. Materiais usados pela geometria são listados separadamente, sem pressupor que todos sejam o material estrutural. Pavimentos arquitetônicos eventualmente incluídos na categoria Floors exigem classificação posterior. Modelos vinculados não são percorridos.

O catálogo inclui ID/UniqueId, nome, classe e ativo estrutural; lê densidade, resistência de compressão do concreto, módulo de Young e coeficiente de Poisson quando disponíveis. Ausência/erro é registrado com estado e valor nulo, não zero. Um nome contendo C25 não é aceito como comprovação da propriedade. Não se verifica aço CA-50 da armadura.

## Unidades e documentação utilizada

A implementação foi conferida no `RevitAPI.xml` da instalação local 2027, junto ao DLL usado para compilar. O XML documenta `StructuralAsset.Density` em kg/ft³, `ConcreteCompression` e `YoungModulus` em N/(ft·m), e `StructuralMaterialId`/`StructuralMaterialIndex` como referências dos materiais de análise. As conversões usam `UnitUtils`, conservando valores brutos e convertidos em kg/m³ ou MPa. XYZ representa os componentes do ativo, não três módulos distintos presumidos.

Não se equipara automaticamente a compressão cadastrada a fck adotado nem o módulo cadastrado a Eci/Ecs da norma brasileira. A interpretação exige conferir a definição do ativo, o material atribuído, as hipóteses e o contrato de intercâmbio.

## Compilação e execução

`dotnet build TccAssistente.RevitAudit.csproj -c Release -o D:/TCC/work/revit-property-audit-build`

O manifesto `.addin` do tipo `Command` usa a classe `TccAssistente.RevitAudit.AuditMaterials` e aponta ao DLL deste projeto. O pacote local preparado em `D:/TCC/ferramentas/RevitAudit-R91` contém DLL, manifesto e instruções. O registro tem nome próprio em `%APPDATA%/Autodesk/Revit/Addins/2027/TccAssistente.MaterialAudit.addin`; não se substitui o TCC Assistente existente. A aprovação de confiança do Revit, se apresentada, precisa ser feita pelo usuário; a etapa nativa não foi automatizada durante sua ausência. Para remover o registro, excluir somente esse manifesto.

No Revit, abrir o RVT do estudo e executar o comando externo **TCC - auditar materiais**. O relatório vai para uma nova pasta `D:/TCC/outputs/Propriedades-Revit-*`, sem sobrescrever relatórios anteriores. O tempo registrado é apenas da leitura; não representa tempo completo do fluxo.

Depois da execução, associar os UniqueIds exportados ao mapa `R83-Revit-criacao-nativa.json`, conferir presença/ausência e propriedades por elemento e só então confrontar a exportação/recepção. A compilação contra os DLLs instalados não é validação dentro do Revit. O comando ainda precisa ser executado em uma cópia do modelo e conferido no host.

O associador local recusa identidades duplicadas, exige UniqueId e ID nativo coincidentes e conserva ausências. O exportador grava IDs de 64 bits como texto; o associador recusa números fora da precisão segura do JavaScript. Executar `node resumir-materiais.mjs <materiais-revit.json> <R83-Revit-criacao-nativa.json> <novo-resumo.json>`. O resumo não usa nomes ou materiais geométricos como substitutos da atribuição estrutural. Os cinco testes `tests/material-provenance.test.mjs` usam dados simulados e não comprovam leitura do modelo real.

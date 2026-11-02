# H03/R155 — escada nativa no Revit: 17 espelhos, 9 + 8

A escolha final de 17 espelhos foi implementada em uma cópia isolada do modelo Revit R93. O arquivo foi salvo, fechado até a tela inicial do Revit, reaberto pelo caminho completo e relido pelo comando de auditoria. A leitura após reabertura corresponde integralmente à leitura registrada na criação.

Arquivo nativo: `D:/TCC/outputs/Escada-H03-R155-Revit-17-NAO-EXECUTAR/H03-R155-Revit-ESCADA17-NAO-EXECUTAR.rvt`. Os binários RVT, backups, DLL e dependências permanecem fora do repositório público.

## Geometria confirmada pela API dentro do Revit

Confirmaram-se 17 espelhos de 17,823529 cm, pisos acabados +0,22/+3,25 m, pisada de 28 cm, nove espelhos no lance inferior e oito no superior. O patamar acabado está em +1,824118 m. Criaram-se referências próprias para os pisos acabados; não se deslocaram os níveis estruturais +0,20/+3,20 m.

Os tipos monolíticos de lances e patamar foram duplicados para o estudo, com 14 cm como **hipótese geométrica sem dimensionamento**. O material de origem confirmou resistência à compressão de 25 MPa antes de sua atribuição aos tipos. A auditoria de reabertura verifica cotas e contagens; não relê todas as propriedades do material nem realiza cálculo estrutural.

O hash dos IDs, UniqueIds, tipos, caixas envolventes e volumes dos 62 elementos preexistentes foi igual antes e depois da criação e após reabertura. Esse controle é de preservação geométrica, não de igualdade de todos os parâmetros possíveis. O RVT fonte R93 e a definição geométrica R153 mantiveram seus SHA-256 da preparação.

## Tentativas e limites da verificação

A primeira tentativa não confirmou as cotas exigidas e foi revertida sem salvar. A correção utilizou níveis de pisos acabados separados; a segunda tentativa confirmou os valores e salvou o modelo. Os registros de falha foram preservados. A compilação teve zero erros e zero avisos; os cinco controles do validador passaram e a suíte do assistente passou em 81 testes. Esses testes automatizados não substituem a execução nativa, documentada pelos JSONs e capturas próprios.

O Revit gerou dois guarda-corpos automaticamente e registrou um aviso de **corrimão não contínuo**. O aviso foi coletado no relatório antes de dispensar sua apresentação durante a transação; não foi tratado como resolvido. Não se dimensionaram guardas, corrimãos, apoios ou armaduras.

A vista criada herdou a disciplina Estrutural e não apresentou a escada na captura. A seleção de Coordenação pela interface falhou repetidamente por perda de foco da lista; solicitou-se apoio do usuário. Portanto, a inspeção visual da escada e a verificação de interferências físicas permanecem pendentes, apesar da confirmação nativa das contagens e cotas. Também não houve comparação dos sólidos e de todas as coordenadas com o CAD.

O CAD R153 contém somente as superfícies acabadas em um desenho independente, sem espessura resistente. A R155 acrescenta geometria nativa com espessura ao ramo Revit; **ainda não há equivalência estrutural de escada entre os dois fluxos**. Não se atualizou o DWG estrutural principal, não se exportou novo IFC, não se implantou esta escada no Eberick e não se aplicou seu peso próprio aos receptores. A compatibilização dos apoios deve preceder essa inclusão.

## Tempos e rastreabilidade

O comando de criação bem-sucedido registrou 1.851,1269 ms desde seu início até a gravação do relatório após salvar, antes da navegação e dos diálogos posteriores. Não representa tempo de inferência de IA, tempo do fluxo BIM completo ou uma vantagem sobre o CAD. A sessão exploratória é registrada separadamente pelos relógios UTC e monotônico e inclui espera, ajuste do código, reinício, falhas de interface e reabertura. Nenhuma dessas parcelas deve ser somada ao intervalo que já a contém. Não existe par CAD/BIM equivalente concluído nesta revisão; nenhum ranking foi calculado.

A decisão intermediária de concentrar a diferença de altura em dois espelhos foi arquivada na R154 e substituída pela instrução final de manter 17 espelhos. A monografia e os projetos Eberick não foram editados nesta revisão. O conjunto continua sendo estudo acadêmico, não dimensionado e não destinado à execução.

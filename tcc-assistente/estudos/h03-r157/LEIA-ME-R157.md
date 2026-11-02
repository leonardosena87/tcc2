# H03/R157 — escada visível e interferências nativas

A alteração de Disciplina para Coordenação foi feita pelo usuário. Na conferência seguinte, a escada continuava oculta: a categoria **Escadas estava desmarcada** em Visibilidade/Sobreposição de gráficos. Habilitou-se essa categoria, ocultaram-se as anotações somente nesta vista e ajustou-se o enquadramento. A escada apareceu. A explicação anterior, que atribuía a ocultação apenas à disciplina, era insuficiente; as evidências anteriores não foram reescritas.

Arquivo para visualização: `D:/TCC/outputs/Escada-H03-R157-VISUAL-NAO-EXECUTAR/H03-R157-Revit-ESCADA17-VISUAL-NAO-EXECUTAR.rvt`. Foi reaberto no Revit e permaneceu com a escada visível. A perspectiva mostra dois lances, patamar, elementos estruturais próximos e a região de chegada. A caixa de corte continua ativa; não é uma vista integral da edificação. Guarda-corpos não foram conferidos visualmente nesta etapa.

## Preservação e alcance da releitura

Como o menu Salvar como perdeu foco, gravou-se a vista no documento aberto, fechou-se o modelo, copiou-se o arquivo gravado para a R157 e restaurou-se a R155 de um backup byte a byte previamente conferido. Conferiram-se as duas cópias antes e depois dessa operação. A R155 e a fonte R93 conservam seus hashes de preparação. Nenhuma geometria estrutural foi editada nesta revisão.

Antes dessa gravação, a releitura nativa confirmou os mesmos dados da R155: 17 espelhos, 9 + 8, pisada de 28 cm, pisos acabados +0,22/+3,25 m, patamar +1,824118 m e hash geométrico dos 62 elementos existentes. O auditor externo aceita somente o caminho R155; portanto, **não se apresenta essa releitura como extração completa da API depois de reabrir a R157**. Depois da reabertura, registraram-se a vista e o relatório de interferências executado no próprio Revit.

## Verificação de interferências

Selecionou-se Escadas no conjunto A e Pilares estruturais, Pisos e Quadro estrutural no conjunto B, ambos em Projeto atual. Não se incluiu outra categoria ou modelo vinculado. O relatório foi exportado pelo Revit em HTML e contém cinco pares com a escada ID 473597:

| Elemento nativo | ID | Categoria |
|---|---:|---|
| P4-N1 | 472933 | Pilares estruturais |
| P10-N1 | 473097 | Pilares estruturais |
| V13-N1 | 472984 | Quadro estrutural |
| V15-N1 | 472986 | Quadro estrutural |
| L6-N1 | 473020 | Pisos |

Os três elementos V13/V15/L6 coincidem com os elementos nominais apontados na R156. Não se compara a contagem de quatro pares **face/elemento** da R156 diretamente com os cinco pares **escada/elemento** do relatório nativo. A R156 examinava superfícies acabadas horizontais contra caixas nominais de vigas/lajes; não percorria sólidos de pilares. A R157 examinou elementos nativos e acrescentou P4/P10 ao levantamento.

Não se consideram automaticamente os cinco pares como cinco defeitos, cinco correções necessárias ou cinco falhas de IFC. Os contatos com P4/P10 podem participar de ligações de apoio, mas o relatório não prova capacidade, ancoragem ou continuidade resistente. Na chegada, ainda é necessário compatibilizar os acabamentos, a última pisada e a borda L6/V15, além do encontro lateral com V13. Não se alteraram ou uniram sólidos apenas para eliminar o relatório.

A [orientação oficial Autodesk para executar a verificação](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-run-an-interference-check-between-elements-in-Revit.html) e a [lista de categorias da versão 2027](https://help.autodesk.com/cloudhelp/2027/FRA/Revit-Collaborate/files/GUID-24A99D40-A2B5-4FC9-AE18-9D3413258FB4.htm) foram consultadas. O resultado é uma conferência geométrica no modelo de autoria, sem dimensionamento estrutural.

## Medição e pendências

O intervalo comando até observação do relatório foi medido prospectivamente e permanece contido na sessão completa. Inclui retorno/captura da interface; não é tempo isolado do algoritmo. A sessão inclui navegação, tentativa de Salvar como, cópia/restauração, reabertura e análise do agente. Não existe recorte CAD equivalente nesta revisão e não se calcula ranking. A intervenção do usuário na disciplina é registrada separadamente, sem estimativa retroativa de sua duração.

Continuam pendentes a solução de apoios, o desconto de acabamento/espessuras resistentes, o corrimão descontínuo registrado na R155, a reprodução estrutural equivalente no CAD, nova transferência e inclusão no Eberick. Nenhuma carga, armadura, fundação ou geometria do receptor foi alterada. A monografia permanece intacta. Estudo acadêmico, não destinado à execução.

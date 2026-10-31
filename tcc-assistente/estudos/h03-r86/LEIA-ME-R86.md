# H03/R86 — inventário atualizado de tempos

O inventário contém **140 arquivos no recorte definido**: 104 registros com duração principal explícita, 25 registros sem duração principal e 11 contêineres/consolidações não expandidos. A busca abrange arquivos cujo nome contém `tempo` diretamente nas pastas filhas de `D:/TCC/outputs`, mais os quatro processos técnicos CAD da R84. Não é contagem de todo o esforço da pesquisa nem de 140 ensaios independentes.

Os limites UTC e a duração original são conservados separadamente. A diferença entre eles é calculada sem substituir a medida original. Datas sem fuso não recebem fuso presumido. Campo ausente permanece nulo. Contêineres históricos não são expandidos para evitar repetir os intervalos já presentes em arquivos próprios.

Há 11 pares com sobreposição nos limites declarados. Isso indica necessidade de verificar o escopo antes de somar, não comprova erro ou trabalho paralelo. Não se calculou total acumulado CAD/BIM nem percentual de vantagem. Todos os registros deste inventário permanecem inelegíveis para ranking final de fluxo; um intervalo com escopo incompleto não se torna comparável por possuir duração.

## Banco do cronômetro

O banco `D:/TCC/dados-pesquisa/tempos.json` permanece preservado. Suas três sessões são de treinamento. O inventário registra identificadores, quantidade e estados dos intervalos, propostas e flags de conclusão, sem adicionar essas sessões ao conjunto de arquivos históricos ou presumir que constituam novas medições distintas.

## Processos técnicos novos da R84

Conversão DXF→DWG e reabertura/extração no AutoCAD Core Console foram medidos prospectivamente por relógio monotônico. Cada processo tem início, fim, PID, código de saída, estado de limite de tempo e presença da saída esperada. Os quatro processos terminaram com código 0; o AUDIT e a conferência das geometrias estão documentados na R84.

Esses intervalos medem o processo técnico com comandos e entrada/saída; não são CPU puro, tempo completo do fluxo CAD ou tempo de desenvolvimento da automação. Não há equivalente Revit controlado nesta rodada; não se calcula comparação a partir deles.

## Demonstrações da palestra

Foram encontrados quatro registros `created_saved` na pasta de execuções da demonstração: um preparado sem consulta à IA e três com resposta real da API registrada. As demonstrações ficam em coleção separada e não pertencem à edificação H03.

| Execução | Modo | IA (s) | Geometria API (s) | Comando completo (s) | Tokens informados |
|---|---|---:|---:|---:|---:|
| 9a83401e | Preparado | Não consultada | 0,737 | 22,511 | Não aplicável |
| c5c4333f | Consulta real | 3,014 | 0,525 | 72,205 | 815 |
| f53a01ee | Consulta real | 5,836 | 0,566 | 86,035 | 1.121 |
| 68db2509 | Consulta real | 2,959 | 0,581 | 55,707 | 805 |

O comando completo inclui a operação da janela, revisão da prévia, consulta, abertura, geometria, vista e salvamento. As parcelas são subconjuntos e não se somam novamente ao comando completo. O modo preparado não é inferência de IA. O registro adicional 68db2509 foi localizado nos arquivos desta rodada; não se declara uma nova inspeção visual daquele modelo.

Esses tempos e tokens não estimam o esforço generativo de todo o TCC. Tempo de raciocínio, código, operação de interface e chamadas da pesquisa principal não têm um registro único completo. Os campos de inferência, tokens e custo isolados da edificação permanecem desconhecidos. Não se estimou custo sem fonte de preço e dados de cobrança.

## Retomada nativa R85

Criaram-se cópias independentes do CAD e BIM R79. O Eberick abriu, mas o controle do seletor perdeu o alvo da janela. A recuperação retornou captura de outro aplicativo e a automação de entrada foi interrompida, sem novos cliques dirigidos a essa captura. Não se criou ação, não se aplicou Q_TELHADO e não se processou o projeto.

O intervalo R85 é marcado como interrompido e inclui preparação/navegação; não representa tempo de aplicação de cargas. O BIM não foi tentado. Os hashes dos dois PRJ continuam iguais aos congelados R79. O experimento de agrupamento R81 permanece separado.

## Uso no TCC

Usar o inventário para apresentar desenvolvimento e ocorrências do protótipo, com o escopo de cada etapa. Os tempos finais por fluxo continuam nulos. O protocolo R69 exige entradas e entregáveis comuns, início/fim equivalentes e intervalos não sobrepostos antes da comparação final. As 12 frentes históricas de fechamento não são 12 erros por programa.

O script é somente de leitura das fontes; escreve em uma pasta de saída nova. Quatro testes verificam ausência de fuso, ausência de duração, contêineres, diferença UTC/monotônico e sobreposição, sem criar medições empíricas dos programas. O trabalho escrito não foi alterado.

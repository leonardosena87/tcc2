# H03/R77 — auditoria real de Q e vento nos dois receptores

ESTUDO PARCIAL. NÃO EXECUTAR. As duas cópias independentes R77 foram abertas no Eberick2025-04 v.18.306 e fechadas sem salvar alteração de engenharia. A monografia permaneceu intacta. A ação Q_TELHADO e as cargas planejadas R65 continuam NÃO aplicadas.

## Abertura recuperada e edição pulada

Para contornar o seletor textual indisponível, prepararam-se pastas de cópia com prefixos00/01, selecionáveis visualmente no início da lista de edificações. Antes da abertura, alterou-se somente o campo textual ProjetoRecente/Arquivo no EdificacaoEberick.ini da nova cópia, apontando para seu próprio PRJ. Isso evita selecionar a cópia e abrir inadvertidamente o original por um caminho absoluto antigo. Nenhum binário de engenharia foi editado por script. O título da janela confirmou a pasta correta de cada ramo.

No CAD, a tentativa de alterarψ0 por set_value retornou erro de cache; uma tentativa de digitação não alterou o valor exibido. A opção Raise trouxe o diálogo à frente uma vez, mas também falhou posteriormente. Cancelou-se integralmente Ações; não se confirmou ou salvou o ajuste. No BIM a edição não foi repetida. A dificuldade é operacional do controle nesta sessão, não defeito demonstrado de DWG/IFC.

Os dois PRJ permaneceram byte a byte iguais aos respectivos R64 e passaram na integridade ZIP. As diferenças de metadados e a eventual ausência do log do processo anterior na pasta de trabalho estão discriminadas nos estados JSON; os logs originais R64 congelados foram conferidos e preservados. Os arquivos de engenharia associados também foram comparados, sem alteração aceita fora deINI/QIB. Os estados R77 foram congelados depois do fechamento.

## Q e opções de combinações

Nos dois ramos, a ação Acidental/Q mostrouψ0=0,70;ψ1=0,60;ψ2=0,40 eγq normal desfavorável do concreto1,40. Esses dados são leituras reais, sem inferir o BIM a partir do CAD. A referência residencial R66, extraída do exemplar6118:2026, continua a exigir harmonização justificada dos fatores adotados. Não se adotou conservadorismo geral só porque um número é maior.

No BIM, a aba Combinações apresentou geração automática e uso de todas as permanentes habilitados, Combinar entre acidentais desabilitado e Acidental isolada habilitada paraQ,Água eSubpressão. Esses pontos coincidem com a leitura CAD histórica R66. A árvore acessível não fornece todos os estados de seleção; por isso a leitura visual foi preservada em imagem. Isso não é auditoria da lista completa de combinações geradas.

A documentação operacional do fornecedor esclarece que deixar Combinar entre acidentais desmarcado NÃO significa excluir toda simultaneidade: são geradas combinações com as acidentais em conjunto e as isoladas selecionadas. Marcá-lo amplia as possibilidades intermediárias e isoladas. A opção precisa representar as ações do estudo; não se muda só para acelerar ou reduzir mensagens. A explicação operacional não substitui a norma vigente ou a verificação caso a caso. [AltoQi, combinações e dimensionamento](https://suporte.altoqi.com.br/hc/pt-br/articles/15675742914967).

## Hipóteses de vento efetivamente cadastradas

Ambos mostraramV0=42m/s,ângulo0°,quatro casos,vento estático,S1=1,00,S3=1,00,rugosidadeCategoriaII,maior dimensão menor que20m,fator de vizinhança1,00 e amortecimento0,02. Os campos de conforto exibem probabilidade0,63 e período1ano: não se confundem com o período de recorrência que define a velocidade básica para projeto.

Em Forças médias, observaram-se cálculo automático, fachadas do croqui e obtenção de arrasto a partir da estrutura habilitados; turbulênciaBaixa. Adotar valor único para toda a estrutura e Arbitrar altura total acima do solo estavam desabilitados. O campo não adotado de altura exibia639cm; não se afirmou que uma altura arbitrada de639cm estava ativa.

42m/s é o valor CADASTRADO, não uma escolha agora justificada para Vitória da Conquista. Não se demonstrou sua origem nem se declarou o valor local correto. O mapa gráfico fornecido pelo programa foi consultado, sem georreferenciamento/interpolação documentada do ponto. A CAAII de durabilidade não determina a CategoriaII de rugosidade: são classificações diferentes. Permanecem pendentes topografia, entorno, parâmetros da velocidade e exposição da cobertura elevadaP2. O exemplar6123/8681 não foi encontrado na busca nominal da pastaFTC desta sessão; não se simulou consulta ao texto integral dessas normas.

## Oito tabelas,24linhas comparadas

Transcreveram-se visualmente três pavimentos em cada um dos quatro casos, nos dois ramos, com imagens das tabelas preservadas para auditoria. O BIM denomina os níveis TCC-cdd31967-N2/N1/N0; a conciliação utilizou a correspondência comN2/N1/N0 e as cotas639/320/20cm. Conferiram-se fachada, fachada transversal, cota,S2,arrasto,força,força transversal e torção mostradas.

| Caso, independente dos demais | N2(kN) | N1(kN) | N0(kN) | Soma das magnitudes exibidas(kN) |
|---|---:|---:|---:|---:|
| X+ | 11.17 | 18.70 | 2.45 | 32.32 |
| X- | 11.17 | 18.70 | 2.45 | 32.32 |
| Y+ | 17.57 | 32.16 | 4.21 | 53.94 |
| Y- | 17.57 | 32.16 | 4.21 | 53.94 |

Cada linha vale para ambos os ramos no estado lido. Não se somamX+eX−ouY+eY−como ações simultâneas. As magnitudes positivas da tabela não foram convertidas em sinais globais sem consultar o vetor do caso. As somas32,32/53,94kN não são reações de apoio ou comprovação de equilíbrio do pórtico. S2e arrasto são valores arredondados exibidos; não foram usados para reconstruir a pressão interna exata.

EmX, a fachada é705/710/705cm e a transversal965/1072,5/965cm; emY ocorre a troca correspondente. S2mostrou0,95/0,90/0,43 emN2/N1/N0. O arrasto emXfoi1,00/0,96/1,00 e emY1,14nos três níveis. Força transversal e torção da tabela exibiram0,00; isso não prova ausência de torção interna ou excentricidade no modelo. A identidade dessas tabelas é resultado parcial, não validação da ação do vento para o local ou da estrutura.

## Tempo, preservação e continuidade

CAD:503.199s assistidos, incluindo abertura, tentativa de editarQ, recuperações, consulta ao mapa e às tabelas, e fechamento. BIM:262.617s, incluindo abertura, leituraQ/opções de combinações, tabelas e confirmação de fechamento, sem repetir a edição ou o mapa. Os escopos diferem. Não calcular vantagem percentual ou duração total de fluxo. A primeira captura posterior ao comando de fecharBIM tem intervalo parcial arquivado e já contido no encerramento final; não somar os dois.

As imagens foram mantidas como evidência dos valores que a árvore acessível não expõe, sem recorte ou alteração do conteúdo. Não representam inspeção em outro computador. O protocolo de medições finais permanece R69, e a entrega parcial R76 continua disponível sem envio. As leituras R77 complementam essa entrega; nenhum nativo R76 foi modificado.

Próximo: concluir entradas/combinações e verificar os critérios normativos aplicáveis; uma análise exploratória com cargas incompletas, se realizada em outra cópia, deve ser identificada separadamente. Não transformar este resultado de igualdade dos cadastros em aprovação deELU/ELS, fundações ou projeto executivo.

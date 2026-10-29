# H03/R62 — ampliação CAD em diagnóstico

ESTUDO PARCIAL, NÃO EXECUTAR. Esta revisão NÃO constitui par CAD/BIM validado. A referência pareada anterior permanece a R61, com apenas RC01 e RC02 conferidos nos dois ramos. Criou-se a cópia BIM R62, mas ela não foi aberta ou ampliada: os arquivos copiados foram conferidos por hash e permanecem iguais aos congelados R61.

## Operação realizada no CAD

Inseriram-se os onze nós previstos RC03..RC13 em N2, por coordenadas em centímetros. Configuraram-se seis grupos de Fz permanente, ação Adicional, conforme o mapa R60: RC03; RC04/RC05; RC06; RC07/RC08/RC12/RC13; RC09/RC10; RC11. Os registros preservam valores digitados e contagens de seleção 1/2/1/4/2/1. Contagem de seleção não prova que cada força ficou armazenada; a leitura posterior demonstrou essa limitação.

Antes da aplicação de RC09/RC10, detectou-se entrada com sinal duplicado (--1.146561). O Eberick apresentou aviso de número real inválido. Corrigiu-se o campo e conferiu-se -1.146561 antes de prosseguir. A tentativa de definir o campo por UIA set_value falhou com 0x80040200; o valor foi corrigido por teclado após limpar o campo. Registrar como ocorrência operacional de automação, sem atribuir à transferência DWG.

## Divergência detectada

Processou-se apenas Análise estática linear, com P-Delta indicado, sem dimensionamento ou deslocamentos ELS. O programa retornou Estrutura processada com avisos. O resumo dessa PRIMEIRA TENTATIVA mostrou peso próprio75,69tf, adicional9,73tf, acidental17,11tf, total102,53tf, área aproximada132,81m2 e relação772,02kgf/m2. Esse resumo foi gerado ANTES da correção individual de RC12 descrita abaixo. Não utilizar esses valores como resultado do arquivo corrigido salvo.

O acréscimo exibido em relação à R61 foi1,24tf. O plano previa 15.672145kN novos, equivalentes a 1.598114035tf usando explicitamente9,80665kN/tf. A diferença excede o arredondamento dos resumos. Não se confirmou o fator de conversão interno do programa, nem se demonstrou a causa integral dessa diferença; não se ajustaram valores para forçar igualdade.

Consultou-se RC12 individualmente: X732,5cm/Y705cm e Fz0kN na ação Adicional. Portanto, ao menos esse ponto não continha a força prevista, apesar da seleção anterior do grupo. Digitou-se Fz=-0,807804kN, confirmou-se o diálogo Carga concentrada e depois o diálogo Nó, salvou-se o projeto e fechou-se normalmente. Ainda não se reabriu ou reprocessou após essa correção. Não se afirmou que os outros três pontos do grupo estavam zerados; não foram relidos individualmente nesta etapa. Não se demonstrou causa por foco, concorrência de comandos, conectividade ou intercâmbio.

## Tempo e preservação

Tempo CAD prospectivo assistido: 12 min 20.661 s, incluindo abertura, onze nós, tentativa de cargas, processamento, investigação e correção parcial/salvamento. Intervalo observado de processamento: 0 min 24.874 s, incluindo latência até leitura da conclusão. Não há tempo BIM de execução R62, pois o ramo não foi iniciado. Não preencher com zero. Nenhum desses valores autoriza ranking ou economia percentual.

Conferiram-se 71 arquivos protegidos R61. Congelaram-se os conjuntos nativos R62 após o fechamento; PRJ com integridade ZIP verificada. O CAD é diagnóstico com cargas não validadas; BIM é apenas cópia da R61. A monografia e as origens RVT/DWG não foram editadas.

## Próxima ação concreta

Retomar em nova cópia do CAD R62 congelado, sem modificar esta evidência: reler RC07/RC08/RC13 e demais nós/cargas, além de confirmar RC12 após reabrir; corrigir somente o que a consulta demonstrar; reprocessar e reconciliar a soma com unidades/fatores documentados. Só depois ampliar o BIM usando operações confirmadas e comparar o mesmo estado. Preservar os resumos anteriores, identificar sempre qual estado foi processado e separar tempo de tentativa/correção de tempo de transferência.

O escopo permanece parcial: falta Q do telhado, P1/varanda, P2/abrigo, perfis/apoios/ancoragens, paredes, reservatório1000L/tara/base, escada, bordas, vento/com­binações e ELU/ELS. Não há fundação real dimensionada ou aprovação das vigas20x30cm. A igualdade R61 limita-se aos resumos exibidos, não à equivalência integral.

# H03/R138 — controle L3 com a mesma malha, sem W20

Estudo parcial — NÃO EXECUTAR. Sem dimensionamento nem liberação estrutural.

## Procedimento e preservação

Criaram-se 62/CAD e 63/BIM a partir das bases R116 30/CAD e 31/BIM, sem W15 nem W20. Refinou-se somente a L3/N1 para espaçamento individual 10 × 10 cm, ângulo 0°, igual à R137 com W20/S58. Permaneceram maciça, h=14 cm, elevação zero, ambiente Externo, Q=1,5 kN/m² e revestimento=1,0 kN/m². As configurações foram conferidas após salvar, fechar e reabrir nos dois ramos. A localização pelo prefixo numérico da árvore de arquivos funcionou; não houve intervenção humana.

Executou-se o mesmo escopo parcial: análise estática linear e deslocamentos do pórtico com rigidez configurada; sem dimensionamento, flechas das lajes, análise fissurada ou dinâmica. Ambos terminaram com avisos. Após reabertura exportaram-se seis arquivos de texto SAP2000, sem executar ou importar no SAP2000. Conservaram-se os 35 arquivos-fontes R116 e os 35 arquivos das cópias experimentais R137, conferidos por SHA-256. Congelaram-se as árvores dos controles fechados e verificou-se a integridade ZIP dos PRJs. Isso não constitui verificação estrutural.

## Isolamento do efeito W20/S58

A comparação de cada controle sem W20 com seu próprio ramo R137 com W20 confirmou IDs e coordenadas dos nós e extremos ordenados I/J das barras iguais nos três modelos. N1 possui 1.738 nós e 3.325 barras; N2 possui 443 e 794; o pórtico, 110 e 133. Em N1 a única diferença entre todas as tabelas foi a adição de 37 forças nodais G2, sem remoção. Não existe G2 nodal no controle. N2 não apresentou diferença em nenhuma tabela. Portanto, sob esse controle, isolou-se a escrita das 37 cargas em N1, sem atribuir as diferenças à geometria ou a outro carregamento nodal.

As 37 cargas, incluindo IDs, coincidem entre CAD e BIM. A força resultante escrita é −1.742,9405 kgf e seu centro é (810;195) cm. Os primeiros momentos na origem são Mx=−339.873,39750 kgf·cm e My=1.411.781,80500 kgf·cm, iguais aos nominais na precisão do arquivo. A linha permaneceu na posição e intensidade da R135/R137: (810;10)→(810;380) cm, q=4,71065 kN/m, comprimento 3,70 m. A comparação usa a convenção observada R125 de 100 kgf/kN, sem apresentá-la como conversão SI exata. As hipóteses de parede e altura permanecem condicionais; não se representa a parede completa ou os trechos de extremidade sobre vigas.

No pórtico a diferença envolveu 243 registros pontuais removidos e 243 adicionados e três registros nodais em cada conjunto, todos em G2. São diferenças de linhas de tabelas, não 243 correções ou interações de usuário. A leitura das forças pontuais LOCAL/2 adotou condicionalmente os eixos padrão SAP para 17 barras horizontais sem rotação explícita. Não se comprovou a equivalência com os eixos internos do Eberick. Sob essa hipótese, o incremento é:

| Parcela ou grandeza | Valor escrito/calculado |
|---|---:|
| Forças pontuais locais interpretadas como +Z (kgf) | −1.736,9552 |
| Forças nodais globais (kgf) | −5,9858 |
| Fz total do incremento (kgf) | −1.742,9410 |
| Mx na origem (kgf·cm) | −341.229,503175790 |
| My na origem (kgf·cm) | 1.412.443,351155234 |
| Diferença Fz pórtico−N1 (kgf) | −0,0005 |
| Diferença Mx pórtico−N1 (kgf·cm) | −1.356,105675790 |
| Diferença My pórtico−N1 (kgf·cm) | 661,546155234 |

Os dois ramos apresentaram os mesmos incrementos condicionais. A diferença muito pequena de força não autoriza aceitar os momentos: na interpretação adotada, eles não coincidem. Não se atribuiu a causa à exportação, à discretização, à rigidez dos apoios ou a erro do software sem evidência própria. Esses incrementos são cargas exportadas e não reações de apoio. Não se alterou a intensidade ou posição da linha para forçar equilíbrio.

As referências primárias para a hipótese de eixos são o manual CSi Analysis Reference, seção de eixos locais de barras, e a documentação Frame Local Axes do SAP2000, já documentadas na R134: https://docs.csiamerica.com/manuals/sap2000/CSiRefer.pdf e https://docs.csiamerica.com/help-files/sap/Menus/Assign/Frame/Frame_Local_Axes.htm . A hipótese permanece explícita no resultado JSON; não houve execução no SAP.

## Resumo visual e limites

O controle exibiu PP=75,69 tf, G2=10,56 tf, Q=17,11 tf, QT=1,78 tf, total=105,14 tf, área=132,81 m² e relação=791,65 kgf/m², com aviso de relação de carga por área não usual. O modelo com W20 da R137 exibia total=106,88 tf; a diferença arredondada de 1,74 tf é compatível com a integral nominal, mas não demonstra equilíbrio local. γz exibido foi 1,09/1,08/1,06/1,05 no controle, contra 1,10/1,08/1,06/1,05 com W20. Esses números arredondados não aprovam estabilidade ou ELU/ELS completo. Não se transcreveu o quadro completo de deslocamentos do topo. Os dados do resumo foram transcritos visualmente das imagens listadas em observacoes-visuais.json; eventuais textos de acessibilidade defasados não foram tratados como leitura numérica do resumo.

## Tempos e esforço

| Ramo | Sessão exploratória (min) | Comando até término observado (s) |
|---|---:|---:|
| CAD | 7.376933 | 21.852 |
| BIM | 8.569867 | 24.843 |

Os intervalos de processamento estão contidos nas sessões; não somar. Incluem latência, leitura e ferramenta, sem isolar tempo do solver ou da inferência. Preparação de código, auditoria e redação posterior não foram cronometradas separadamente. Não houve intervenção humana nesta etapa. Tokens, energia e custo da IA não foram medidos. Não há ranking final de produtividade nem percentual de economia de tempo autorizado por estas sessões exploratórias.

## Próxima etapa

O controle solicitado na R137 foi concluído. A retenção de força e centro em N1 está documentada sob o controle de mesma malha; a transmissão ao pórtico e as reações locais ainda precisam ser investigadas. A W20 não foi aceita como modelo final, e não se demonstrou convergência de malha. Permanecem as demais cargas, aberturas, reservatório e cobertura, combinações, ELU/ELS completo, sincronização com a autoria e a rodada prospectiva dos dois fluxos. Não se alterou a monografia nem os arquivos RVT/DWG de autoria.

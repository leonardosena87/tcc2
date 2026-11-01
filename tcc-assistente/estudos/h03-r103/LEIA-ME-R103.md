# H03/R103 - apoios efetivos no cadastro do N0

Consultaram-se individualmente os onze elementos N0 do CAD R102 e os onze do BIM R102. Cada janela foi registrada e cancelada, sem salvar. Os projetos foram fechados; ambos os PRJs mantiveram os hashes R102.

Nos 22 dialogos observou-se Pilar de fundacao, altura de barra Fixo/10 cm, vinculo do pilar Engastado e vinculo do apoio Rotulado. Secao retangular 20 x 30 cm, ambiente Externo e elevacao zero. A rotacao foi 90 graus somente no CAD P11/BIM P6; nos demais, zero. Visualmente, Sapata estava selecionada e Manter secao constante na prumada marcado. A acessibilidade nao informa o estado desses radios/checkboxes; nao se deduz esse estado pelo parser.

Os nomes diferem entre ramos. Pareamento pela posicao visual correspondente do croqui N0:

| CAD | BIM |
| --- | --- |
| P1 | P8 |
| P2 | P4 |
| P3 | P1 |
| P4 | P9 |
| P5 | P5 |
| P6 | P2 |
| P7 | P11 |
| P8 | P7 |
| P9 | P3 |
| P10 | P10 |
| P11 | P6 |

Conferiram-se 110/110 pares de campos, excluindo os nomes. Essa correspondencia visual nao substitui uma nova verificacao numerica das coordenadas. O simples pareamento por nomes produziria uma divergencia de rotacao em pilares que ocupam posicoes diferentes.

O TCC continua restrito a superestrutura com apoios idealizados, sem sondagem ou dimensionamento geotecnico. A presenca do tipo Sapata no cadastro nao constitui fundacao projetada. Tampouco permite declarar rigidez real do solo, resistencia ou seguranca da fundacao. O apoio elastico padrao consultado na R101 nao deve ser atribuido a estes elementos: o campo efetivo consultado aqui mostra Rotulado.

A decisao de modelo da base continua aberta: documentar/adequar a representacao para o recorte da superestrutura e avaliar sua sensibilidade antes da analise final. Nao se alterou automaticamente Rotulado para Engastado. Ainda falta conferir as ligacoes nos niveis superiores, liberacoes das vigas, continuidade e estabilidade global.

Ajuda oficial instalada consultada: C:/Program Files/AltoQi/Eberick/Ajuda/Eberick/dialogo_edicao_elemento_pilar.htm. A ajuda descreve a funcao dos vinculos; nao comprova as atribuicoes do projeto. A evidencia destas atribuicoes e a consulta nativa preservada nos 22 arquivos de texto e capturas.

R103-resultado.json registra campos, pareamento, hashes e tempos parciais. Os tempos abrangem abertura, navegacao, consultas e registro intercalado; nao sao tempo ativo isolado nem total final comparavel. Um teste sintetico controla evidencia incompleta/contraditoria; as 22 consultas reais sao verificacao distinta. Nenhum novo processamento, nenhuma alteracao na autoria RVT/DWG ou na monografia.

Proximo: fechar a representacao comum da base e conferir vinculos superiores; continuar cargas P1/P2, reservatorio, paredes/aberturas, escada e vento, antes das combinacoes efetivas e ELU/ELS.

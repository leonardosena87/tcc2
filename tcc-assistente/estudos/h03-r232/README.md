# H03/R232 — pilares do fluxo CAD lançados no Eberick

Em 6 de novembro de 2026, lançou-se a etapa de pilares em cópia independente da recepção CAD R228. A edificação está em `D:/TCC/outputs/H03-R232-CAD-PILARES-NAO-EXECUTAR/CAD`; o nome interno do PRJ continua `R228-CAD-DWG-BRUTO-NAO-EXECUTAR.prj` para conservar a estrutura da cópia. O projeto R228 original permanece preservado.

## Operação executada

Leu-se a geometria dos DXF de retorno do AutoCAD R225, com unidades em metros, camadas por pavimento, polilinhas fechadas, identificação e seção. Usou-se o comando nativo de lançamento de pilares do Eberick, com coordenadas absolutas em centímetros e inserção pelo centro. Lançaram-se 12 posições em N1: 11 de 20 × 30 cm e P11 de 30 × 30 cm. Copiaram-se as prumadas aos demais níveis; P12 termina em N1 e foi retirado somente de N2 após a cópia em lote.

A primeira conferência IFC encontrou 23 sólidos, pois os pilares nasciam em PATAMAR e faltava a continuidade inferior até N0. Corrigiu-se o cadastro mediante cópia das 12 prumadas a N0. A nova exportação contém 35 sólidos: 12 em PATAMAR, 12 em N1 e 11 em N2. Os objetos de início em N0 não produzem trecho inferior exportado nesta configuração. Não se lançou nem dimensionou uma fundação.

## Resultado conferido

O script `auditar_pilares.py` cruza os sólidos exportados pelo Eberick com os próprios DXF de autoria CAD, sem usar o Revit como fonte do lançamento. Confere o retângulo da polilinha com o XDATA e o rótulo de seção, além de exigir associação única, nome, posição, seção, intervalo vertical completo, malha fechada, C-25 e cobrimento de 3 cm. A tolerância geométrica da auditoria é 0,1 mm, sem caráter normativo.

As 23 identidades CAD correspondem aos 35 trechos nativos sem lacuna de projeção vertical. Fechou-se e reabriu-se a cópia CAD; a segunda exportação conservou identificadores IFC, nomes, pavimentos, malhas e conjuntos de propriedades dos 35 sólidos. O controle anterior à correção, com 23 sólidos, permanece guardado como evidência do retrabalho.

## Tempos observados

| Intervalo | Duração | Delimitação |
|---|---:|---|
| Lançamento inicial de pilares e salvamento | 15 min 43,3 s | 16:41:16,649 a 16:56:59,927 UTC; inclui consultas, leitura dos desenhos, recuperação da interface e transição de contexto |
| Correção da continuidade até N0 e salvamento | 50,8 s | 16:59:28,091 a 17:00:18,893 UTC; inicia após detectar a omissão no primeiro controle IFC |

Os intervalos são prospectivos, brutos e assistidos. Exportação, elaboração do script de auditoria, auditoria e reabertura posteriores não estão incluídas nesses dois valores. Não constituem o tempo total CAD. Os 2 min 33,1 s de recepção BIM R231 abrangem vigas e pilares e excluem o preparo do IFC derivado; portanto, não se calcula razão nem percentual entre esses valores de escopos distintos.

## Limites e sequência

A etapa CAD agora contém pilares nativos conferidos. Faltam vigas, lajes, escada, cargas e vínculos nesta nova cópia para atingir o marco comum da comparação. Na recepção BIM R231, a geometria nominal das vigas e pilares foi conferida após tratamento de 18 peças no IFC derivado; lajes, escada e cargas também precisam de complementação. A permanência de C-25 e do cobrimento no receptor não demonstra sua transferência pelo IFC, pois se herdaram configurações de projeto.

Os projetos calculados R227 permanecem separados dessas cópias de recepção e lançamento. A coincidência geométrica e a reabertura não constituem verificação de conectividade analítica, processamento estrutural ou aprovação para execução. Permanecem necessárias as verificações estruturais locais já registradas, inclusive ancoragem na cobertura e detalhamento complementar da V1.

Validação desta alteração: auditoria nos arquivos efetivos e 82 testes automatizados do `tcc-assistente` aprovados. Os testes automatizados não substituem as operações e conferências realizadas no Eberick.

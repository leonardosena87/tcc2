# H03/R135 — W20/S58 sobre L3/N1

Lançou-se uma carga linear experimental em cada cópia independente da R116: 56CAD e 57BIM. A W15 experimental e o ensaio W03 de viga inteira não integram essas cópias. A referência R116 permanece preservada.

| Item conferido | CAD | BIM |
|---|---:|---:|
| Carga extra após salvar, fechar e reabrir | 4,71065 kN/m | 4,71065 kN/m |
| Carga automática de parede | 0 | 0 |
| Início gráfico no modelo | (810;10) cm | (810;10) cm |
| Término gráfico no modelo | (810;380) cm | (810;380) cm |
| Extensão nominal | 3,70 m | 3,70 m |
| Sessão exploratória inicial | 6.575 min | 8.206 min |

A hipótese histórica R120-S58 é de parede sem abertura, com 3,01 m de altura e peso por área de 1,565 kN/m². Obtém-se intensidade de 4,71065 kN/m e integral prevista de 17,429405 kN. **Essa integral não é reação calculada.** A composição depende de confirmação de fabricante; a altura resulta da geometria R56/R57 e o intradorso superior atual não foi revalidado. O recorte de 3,70 m exclui os dois segmentos de 0,10 m sobre as vigas nas extremidades; não representa toda a parede W20. A prontidão falsa da matriz R120 histórica não foi reescrita como aceitação final.

O comando Modelo → Cargas → Linear usou Parede desmarcado, ação Adicional e definição por dois pontos. A releitura textual nativa recuperada confirmou 4,71065 e parede 0,00 em ambos os arquivos reabertos. A grade foi inspecionada visualmente: Adicional 4,71, Solo/Acidental/Água/Subpressão/Q_TELHADO_MANUTENCAO 0,00, na precisão de duas casas. Trata-se de complementação no Eberick após a importação, não de sucesso ou defeito de transferência DWG/IFC.

Os dois DXFs exportados antes da recuperação das capturas contêm uma única linha e um único rótulo CR-Paredes, com extremos brutos (16,2;0,2) e (16,2;7,600000000000001). A escala gráfica 1:50 e a origem foram verificadas por três centros de pilares: (0;0), (440;705) e (965;390) cm. O resíduo decimal do último extremo decorre da representação escrita do DXF; a tolerância de 10⁻⁹ unidade gráfica serve somente à conferência numérica dessa escrita. Não é tolerância de projeto. Z=0 refere-se ao plano do desenho, não ao nível físico da laje.

## Qualidade das evidências e esforço

O salvamento inicial das capturas reteve um estado antigo entre células de automação: 24 grupos, totalizando 72 arquivos de imagem/texto/metadados, repetiram a tela inicial sem projeto. Foram segregados localmente em `capturas-invalidas-repetidas`, identificados por hash no JSON e excluídos do conjunto comprobatório público. Os nomes originais desses arquivos não comprovam a operação indicada. A falha foi do registro auxiliar, não foi classificada como falha do projeto ou da importação.

Corrigiu-se o salvamento passando explicitamente o estado observado. Reabriram-se BIM e CAD, sem salvar alterações durante a consulta, para recapturar croqui, valor exato e grade de ações. O texto de acessibilidade corresponde às novas imagens. Não se recuperaram retrospectivamente as capturas da digitação dos pontos; a extensão é sustentada pelos DXFs. A inspeção inicial ao vivo da L3 apresentou laje maciça, ambiente Externo, h14cm, elevação0, Q1,50 e revestimento1,00 nos dois ramos, mas o arquivo inicial de captura inválido não comprova esses campos. Na tentativa posterior BIM, o rótulo sobreposto à linha abriu a própria carga; essa consulta foi encerrada sem alteração e a recaptura das propriedades da laje permaneceu pendente.

A recuperação pareada de capturas durou 5.587 min, registrada separadamente em `recuperacao-capturas-tempo.json`. As sessões iniciais incluem abertura/seleção, inspeção, configuração, lançamento, salvar/fechar/reabrir, ações, exportação, raciocínio e interface. A sessão CAD inclui consulta de código e recuperação de menus, além de três tentativas de Escape encerradas por clique direito; o BIM reutiliza o procedimento e começa após o seletor aberto. Não são repetições controladas para ranking. Não há tempo final dos dois fluxos, tempo de inferência da IA, tokens ou custo conhecido. Não se registrou intervenção humana nesta etapa. A elaboração posterior de scripts/relatório não foi cronometrada separadamente.

## Preservação e limites

Os 35 arquivos das fontes R116 conservaram seus hashes. Ambos os PRJs R135 diferem das cópias iniciais e mantiveram o hash obtido após salvar durante as consultas e exportações. Congelaram-se 33 arquivos de trabalho persistentes após o lançamento, com manifesto local `R135-congelados.json`; os binários ficam em D:/TCC e não integram o repositório público. Os 2 logs transitórios inicialmente copiados deixaram de existir nas cópias de trabalho após fechar o Eberick; a ausência está registrada e não foi tratada como perda do projeto. Não se alterou monografia, RVT ou DWG de autoria.

Não houve processamento na R135. A persistência e a geometria gráfica não comprovam a distribuição analítica, os momentos, as reações, a capacidade resistente ou o atendimento a ELU/ELS. A análise seguinte deve usar cópias derivadas e um controle compatível de malha, mantendo W20 isolada. As pendências W15 e demais cargas/apoios continuam abertas; não existe liberação para execução.

Procedimento de referência: [AltoQi — carga linear](https://suporte.altoqi.com.br/hc/pt-br/articles/360058309854). O uso do procedimento não constitui validação normativa.

# H03/R97 — ação de manutenção cadastrada nos dois receptores

Criaram-se novas cópias de fechamento a partir dos ramos R85, com dados anteriores R79 preservados. A ação **Q_TELHADO_MANUTENCAO (QT)** foi cadastrada, salva, fechada, reaberta e relida no Eberick 2025 Infinity em ambos os ramos. **As 13 parcelas do plano R65 ainda não foram lançadas. Não houve novo processamento estrutural.**

## Cópias de trabalho e preservação

- CAD: `D:/TCC/outputs/12-H03-R97-CAD-NAO-EXECUTAR/Projeto Eberick/H03_CAD_R49_LAJES_NAO_EXECUTAR.prj`.
- BIM: `D:/TCC/outputs/13-H03-R97-BIM-NAO-EXECUTAR/Projeto Eberick/H03_BIM_R46_IFC_NAO_EXECUTAR.prj`.
- Evidências e congelamento: `D:/TCC/outputs/Fechamento-H03-R97-ENTRADAS-NAO-EXECUTAR`.

Os nomes internos históricos dos PRJ foram mantidos para preservar os recursos associados. A identificação da revisão está nas pastas e nos registros. Não se apresenta R49/R46 como uma nova medição de transferência. Antes de abrir, verificaram-se as cópias e alterou-se somente `ProjetoRecente/Arquivo` no INI para apontar ao PRJ da própria pasta; os vínculos auxiliares QIB não foram integralmente refeitos.

A conferência final preservou os hashes dos **35 arquivos de origem R85**. Os PRJ de trabalho R97 mudaram após a inclusão da ação. Congelaram-se e verificaram-se 36 arquivos das cópias cadastradas antes de inserir cargas. Os resultados de processamento existentes são históricos e não foram recalculados com as novas entradas.

Ao deixar a cópia experimental R96, respondeu-se ao pedido de salvar. O PRJ de trabalho passou a `7f35120b326dff562b5a6fe5273217e653d4f901ad45dcdf52ed0fadfa5263e6`; o estado recebido anterior, com hash `0f71edecb345d51793a02870d603cddaafe9d61e8c72319fc2734c58f40d1033`, permanece congelado. Não se editaram entradas estruturais da R96 nessa saída. Não se realizou comparação semântica de todo esse binário para atribuir cada alteração interna ao salvamento da configuração de exportação.

## Cadastro efetivamente conferido

Na releitura posterior à reabertura, coincidiram os 20 valores distintos dos controles editáveis da máscara QT, incluindo nome, indicação e todos os coeficientes exibidos. Os valores principais foram:

| Campo | CAD | BIM |
|---|---:|---:|
| Indicação | QT | QT |
| Variabilidade, leitura visual | Acidental direta | Acidental direta |
| Normal desfavorável, concreto | 1,40 | 1,40 |
| Normal desfavorável, aço | 1,50 | 1,50 |
| ψ0 / ψ1 / ψ2 | 0,50 / 0,40 / 0,30 | 0,50 / 0,40 / 0,30 |
| Ação ativa / caso isolado | Sim / Sim | Sim / Sim |
| Efeito favorável para QT | Não | Não |

Mantiveram-se a geração automática e a opção geral **Combinar entre acidentais** desmarcada. Marcou-se **Acidental isolada** na linha QT, inicialmente desmarcada. As imagens após reabrir comprovam essas marcas. Não se criou um grupo mutuamente excludente entre Q da laje e QT. A opção **Considerar para as lajes** permaneceu marcada, conforme o cadastro inicial; isso não insere uma carga na laje por si só e ainda deve ser conferido com o lançamento efetivo.

A documentação oficial explica que, com **Combinar entre acidentais** desmarcado, o programa gera casos com as acidentais simultâneas e também os casos isolados expressamente marcados. Não se interpreta a opção desmarcada como exclusão automática de Q e QT. Essa explicação operacional não substitui a conferência das combinações efetivamente geradas com os carregamentos completos. Ações sem cargas podem ser eliminadas da lista pelo programa; cadastrar QT não demonstra contribuição no cálculo.

Não se editou a ação Q existente. Sua máscara foi lida antes da inclusão; não se repetiu uma leitura completa de Q após a alteração. A comparação de 20 campos refere-se à **nova QT** e não a todo o projeto. O aviso de necessidade de reprocessamento foi aceito para gravar a mudança de entrada, sem executar a análise.

Houve assistência humana em ambos os ramos: três solicitações pontuais ao todo, duas no BIM e uma no CAD. A automação encontrou erros de cache dos controles e perda de foco. Nome/indicação foram completados conforme a conferência nativa; os valores só foram considerados persistidos após reabrir. Essa operação não é apresentada como automação integral. A dificuldade de interação com a interface não constitui, por si só, defeito de transferência DWG/IFC.

## Tempos parciais observados

| Recorte: abrir Projeto/Ações até gravar e reler após reabrir | Tempo |
|---|---:|
| CAD | 776,1385952 s — 12 min 56,139 s |
| BIM | 582,3780720 s — 9 min 42,378 s |

Ambos incluem navegação, tentativas, espera pela intervenção humana, conferência e trabalho independente intercalado; excluem a preparação das cópias. Não se mediu o tempo humano ativo nem a inferência isolada da IA. Não se subtraem durações presumidas e não se calcula vantagem percentual entre esses intervalos. Eles não representam os tempos completos dos fluxos ou ensaio pareado controlado.

## Base numérica para alinhar materiais e paredes

Conferiram-se visualmente no exemplar local NBR 6118:2026 os itens 8.2.2, 8.2.5, 8.2.8, 8.2.9, 8.3.3 e 8.3.5, nas páginas PDF 42/44/45/48, impressas 24/26/27/30. Para C25, com αE = 1,0 como hipótese de granito/gnaisse, obtém-se Eci = 28.000 MPa, αi = 0,8625 e **Ecs = 24.150 MPa**. O fator inicialmente informado de 0,86 produziria 24.080 MPa, aproximadamente 24,1 GPa. Conservam-se os valores informados e derivados separadamente; a diferença de 50 MPa em relação a 24,1 GPa não foi corrigida silenciosamente.

Registraram-se as referências de massa específica de 2.500 kg/m³ para concreto armado e 7.850 kg/m³ para aço, além de Es = 210 GPa para a armadura na ausência dos dados de ensaio/fabricante previstos na norma. O coeficiente de Poisson 0,2 e Gc = Ecs/2,4 estão delimitados às condições de tensão do item 8.2.9. O peso específico nominal de 25 kN/m³ foi conferido na NBR 6120:2019, Tabela 1, página PDF 15/impressa 9. Não se tratam esses valores nominais como uma conversão exata usando g = 9,80665 m/s².

A composição de parede já presente na R55/R83 foi conferida na Tabela 2 da NBR 6120:2019, PDF 17/impressa 11: vedação cerâmica com furos horizontais, corpo de 11,5 cm, peso sem revestimento de 0,9 kN/m² e 1,75 cm de argamassa por face, a 19 kN/m³. A composição calculada é **1,565 kN/m²** e totaliza 15 cm. O assentamento já está contemplado no peso da alvenaria sem revestimento e não deve ser adicionado de novo. O valor é hipótese acadêmica comum, não composição/produto confirmado pelo usuário ou fabricante. Não inclui esquadrias, vergas ou acabamentos sobre concreto, nem encerra os caminhos de carga.

`R97-base-materiais-paredes.json` registra valores, fórmulas e hashes dos exemplares. Não se alteraram ativos Revit ou materiais Eberick a partir desse arquivo. O significado de Young no ativo deve ser explicitamente mapeado a Eci/Ecs antes de editar. A tentativa de confirmar a vigência no catálogo ABNT retornou **LINK EXPIRED**; não se afirmou confirmação de catálogo por uma fonte secundária. Os PDFs normativos e suas páginas renderizadas permanecem locais, fora do repositório público.

## Verificação e próxima operação

`consolidar_cadastro.py --root <pasta de evidências>` confere as leituras reais, os 20 campos e os 35 arquivos protegidos. `calcular_base_material.py --out <JSON novo> --norms D:/TCC/materiais/normas` reproduz a base numérica específica, exigindo os mesmos exemplares por hash. Ambos recusam relatório de saída existente. Executaram-se os scripts nos arquivos reais e nove testes Node de procedência/tempos, todos aprovados; não houve chamada real de IA por esses scripts.

A próxima operação é aplicar e reler as 13 parcelas QT do plano R65 em cada ramo, preservando G e verificando unidades, coordenadas e ação. Depois, concluir as demais regiões de cobertura, reservatório, paredes, escada, vento, vínculos e verificações ELU/ELS. Cadastramento da ação não encerra essas frentes. A monografia e os RVT/DWG foram preservados nesta revisão.

Fontes operacionais oficiais: [criação de ações](https://suporte.altoqi.com.br/hc/pt-br/articles/115001646393), [configuração de ações](https://suporte.altoqi.com.br/hc/pt-br/articles/360000624993), [efeito das opções de combinações](https://suporte.altoqi.com.br/hc/pt-br/articles/15675742914967) e [cargas típicas de paredes](https://suporte.altoqi.com.br/hc/pt-br/articles/360050715753). Os exemplos normativos antigos dessas páginas não substituem o exemplar local adotado no estudo.

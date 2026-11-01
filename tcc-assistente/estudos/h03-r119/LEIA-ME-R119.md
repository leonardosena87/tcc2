# H03/R119 — cargas uniformes das onze lajes, conferidas individualmente

Em cópias independentes derivadas dos receptores R116, consultaram-se no Eberick 2025 Infinity todas as onze lajes de cada ramo. Os diálogos foram cancelados e os projetos fechados sem salvar. O campo Nome e o pavimento ativo documentam a identidade de cada leitura. A consulta complementa a amostragem nativa pós-reabertura da R53; os IFC daquela revisão já continham uma conferência exportada mais abrangente.

| Pavimento e lajes | Q exibido (kN/m²) | Revestimento/G2 parcial exibido (kN/m²) | Espessura (cm) | Elevação (cm) |
| --- | ---: | ---: | ---: | ---: |
| N1 L1–L4 | 1,5 | 1,0 | 14 | 0 |
| N1 L5–L6 | 2,5 | 1,0 | 14 | 0 |
| N2 L1–L5 | 1,0 | 0,25 | 14 | 0 |

Os quatro campos numéricos coincidiram nos onze pares: **44 comparações de campos**, das quais 22 correspondem às parcelas Q/G2. Não são 44 verificações estruturais independentes. As 22 leituras de lajes corresponderam ao cadastro parcial da R53. As imagens permitem conferir o conteúdo extraído das árvores de acessibilidade. O parser rejeita identidade errada, campos ausentes e valores contraditórios, inclusive quando a árvore repete o mesmo diálogo.

O revestimento de N1 continua como hipótese parcial de pacote de piso, enquanto N2 contempla somente o forro nessa parcela. Essas leituras não demonstram lançamento de paredes, impermeabilização, esquadrias, vergas ou cargas finais de borda. As reações de telhado já lançadas em nós pertencem a outra parcela e não devem ser novamente somadas ao campo Revestimento. O campo Q de L5/N1 não substitui a modelagem e as reações da escada. Não se consultaram integralmente listas de cargas extras ou a transferência das cargas pela grelha.

As sessões observadas foram **319,154779 s no CAD (5min19s)** e **363,849926 s no BIM (6min04s)**. Incluem abertura, navegação, raciocínio, evidências e fechamento. No CAD ocorreram duas escolhas entre Texto/Laje e uma tentativa sobre a seta que não abriu a propriedade. Não se atribui isso a defeito de DWG. O procedimento BIM beneficiou-se do conhecimento anterior; a duração também depende de latência e condução da sessão. Não se calcula vencedor ou vantagem percentual a partir desses intervalos. Tempo ativo humano e inferência isolada da IA permanecem desconhecidos.

Os 35 arquivos fonte R116 conservaram seus hashes e os dois PRJs consultados permaneceram byte a byte iguais aos copiados. Diferenças auxiliares de INI/interface são discriminadas no JSON; não se afirma identidade de todos os arquivos das cópias. Não houve processamento, edição de propriedades, modificação de RVT/DWG ou alteração da monografia. Dois testes verificam as evidências reais e a rejeição de identidades/valores conflitantes; não são testes de capacidade estrutural.

Os binários ficam exclusivamente em `D:/TCC/outputs/34-H03-R119-CAD-LAJES-NAO-EXECUTAR` e `35-H03-R119-BIM-LAJES-NAO-EXECUTAR`. Evidências e resultados ficam em `D:/TCC/outputs/Lajes-H03-R119-CONSULTA-NAO-EXECUTAR`. Os receptores processados de referência seguem sendo R116. A consulta R119 não deve ser promovida a dimensionamento final ou aprovação das cargas.

Próxima frente: preparar matriz de paredes superiores por trecho, com correspondência geométrica CAD/BIM e caminho de apoio explicitado. A massa de parede não deve ser convertida automaticamente em carga uniforme de todas as lajes. Reservatório, escada, vento, combinações, demais cargas e verificações completas ELU/ELS continuam pendentes.

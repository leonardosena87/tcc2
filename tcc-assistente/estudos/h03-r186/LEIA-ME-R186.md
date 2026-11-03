# H03/R186 — nós e envoltórias da V2/V14

Estudo preliminar, não executar. Consultaram-se os resultados **já salvos nos PRJ R182** em nova sessão do Eberick 2025 Infinity. Não se recalculou, não se editaram seções/vínculos/armaduras e não se salvou alteração de projeto nesta revisão. Os dois PRJ mantiveram os hashes registrados antes da leitura.

## Correspondência e orientação

A R185 associou os prismas do CAD V2 e V14 aos dois trechos do BIM V2 nos IFCs R178. Nesta revisão, também se conferiram nesses IFCs os três pilares de referência por prismas fechados: CAD P2 corresponde a BIM P4, CAD P5 a BIM P5 e CAD P11 a BIM P6. Essa identidade geométrica refere-se à referência exportada R178, sem substituir nova exportação dos PRJ R182.

O CAD apresenta V2 de P2 para P5, seção 20×45 cm, e V14 de P5 para P11, seção 20×16 cm. O BIM apresenta V2 com primeiro vão P6→P5, seção 20×16 cm, e segundo vão P5→P4, seção 20×45 cm. Portanto, a direção de leitura de cada vão corresponde ao sentido inverso no CAD. Os comprimentos exibidos nos esquemas são 199,6 e 440 cm; não se confundem os comprimentos de esquema/eixo com o comprimento de cada sólido entre faces de pilares no IFC.

## Envoltórias efetivamente exibidas

Os valores abaixo foram transcritos manualmente das capturas nativas; não são cálculo independente nem leitura por OCR. As cortantes são os valores positivos apresentados pela tabela, tratados na comparação como magnitudes, sem alegar equivalência de vetores locais com sinal.

| Registro nativo | Vd inicial (kN) | Vd final (kN) | Md positivo (kN·m) | Md negativo (kN·m) | Mtd exibido (kN·m) |
|---|---:|---:|---:|---:|---:|
| CAD V14 | 22,18 | 15,36 | 1,69 | −7,96 | 0,16 |
| BIM V2, vão 1 | 15,36 | 22,18 | 1,69 | −7,96 | 0,16 |
| CAD V2 | 41,49 | 46,30 | 32,22 | −36,90 | 0,05 |
| BIM V2, vão 2 | 46,30 | 41,49 | 32,22 | −36,90 | 0,05 |

Após inverter as extremidades das cortantes, **os dez valores escalares apresentados coincidem à precisão de duas casas da tabela**. Isso não prova igualdade dos esforços internos em todos os pontos, dos casos/combinações que comandam cada extremo ou de todo o modelo analítico. A comparação mantém o sinal dos momentos e não elimina diferenças pequenas por uma tolerância arbitrária.

## A tabela de nós não tem a mesma unidade de agrupamento

No CAD, V2 apresenta Md de −31,17 kN·m em P2 e −36,90 em P5; V14 apresenta −7,96 em P5 e −5,62 em P11. O BIM apresenta uma única V2 com três linhas: P6 (−5,62), P5 (−36,90) e P4 (−31,17). Assim, a linha do nó P5 do grupo contínuo não repete separadamente os dois registros vistos nas vigas CAD.

Essa diferença de apresentação não significa, por si, que o esforço do trecho baixo tenha aumentado de −7,96 para −36,90: a própria envoltória do vão 1 BIM ainda mostra −7,96. O erro D16/A07 do nó 2 da V2 BIM, documentado na R182, permanece. Deve-se investigar como o detalhamento da armadura negativa trata o nó comum, a continuidade e a mudança de altura de 45 para 16 cm. A R186 **não prova que o programa aplicou o maior momento integralmente à seção baixa**, nem que separar as vigas seja uma correção estrutural admissível.

Não se alterou o limite de 2% de armadura observado na R183 para eliminar A07. As armaduras eventualmente visíveis nas capturas CAD são resultados experimentais não revisados e não são aqui adotadas como detalhamento executivo. A contagem de um erro BIM contra zero CAD continua insuficiente para ranquear a qualidade dos fluxos antes da revisão dessa ligação.

## Registro e continuidade

As nove capturas mostram nós, seções e envoltórias. O JSON contém as transcrições, os pares e as diferenças escalares calculadas com decimais, além dos hashes das fontes. Os cinco testes de código verificam a inversão das extremidades, preservação do sinal, diferença na última casa exibida, dado ausente e valor não finito.

Não houve novo processamento nativo nem nova medição de duração do fluxo. O tempo de consulta não foi acrescentado aos 7 s dos ensaios anteriores. Permanecem pendentes a revisão da continuidade/detalhamento em P5, o apoio e a ancoragem de LE3, cisalhamento/ELS, o conflito V16/J4, novas exportações de retenção e a comparação integral dos tempos e correções. Esta revisão não altera o Revit, AutoCAD ou a monografia.

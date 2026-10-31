# H03/R99 — QT13 gravada e conferida em CAD e BIM

Concluiu-se o lançamento das 13 parcelas de manutenção da cobertura A1/A2 nas duas cópias R98 do Eberick 2025 Infinity. Cada cópia foi salva, fechada, reaberta e consultada. A auditoria aceitou **52 de 52 leituras**, sem ausência ou rejeição: 13 pontos × duas ações × dois ramos. Os 26 pares CAD/BIM apresentaram a mesma ação, coordenadas e seis componentes exibidos. O resultado comprova igualdade desse cadastro; não comprova equivalência de todo o modelo, combinações corretas ou segurança estrutural.

## Arquivos nativos e procedência

- CAD: `D:/TCC/outputs/14-H03-R98-CAD-QT-NAO-EXECUTAR/Projeto Eberick/H03_CAD_R49_LAJES_NAO_EXECUTAR.prj`.
- BIM: `D:/TCC/outputs/15-H03-R98-BIM-QT-NAO-EXECUTAR/Projeto Eberick/H03_BIM_R46_IFC_NAO_EXECUTAR.prj`.
- Histórico operacional, estados intermediários e cópias nativas congeladas: `D:/TCC/outputs/Cargas-H03-R98-QT-NAO-EXECUTAR/retomada-apos-crash`.

Na retomada, a primeira abertura do BIM interrompido mostrou aviso de erro da última edição e propôs verificação de projeto danificado. Recusou-se a verificação; não se executou limpeza ou reparação. O estado anterior e o estado após fechar foram preservados em pastas separadas. Restaurou-se a cópia de trabalho a partir da R97, com conferência de 19 arquivos antes de ajustar apenas o apontamento do INI para o próprio PRJ. `R98-restauracao.json` registra essa genealogia. A cópia restaurada abriu sem o aviso; os 13 lançamentos foram efetuados nela. O CAD abriu sem aviso de recuperação.

Confirmou-se a carga e o nó em cada edição. Após salvar e fechar, congelaram-se 18 arquivos BIM e 15 CAD, todos com cópia byte a byte conferida. Depois da releitura e do fechamento sem salvar alterações, os PRJ conservaram os hashes dos respectivos congelamentos: CAD `e2dc1d91fda030a981e8562d7c3d46318b8e6c262f9c4300415d4078027ca122`; BIM `41735ed0fdd0e2c0424dd84ef0b272418947b5c8bdb0cd1abcfa62c852917ccf`. Conferiram-se também os 35 arquivos de origem R97: todos mantiveram os hashes. Nenhum resultado de processamento antigo foi promovido a resultado desta revisão.

## Critério e limites da conferência

Utilizou-se o plano R65 preservado por hash e o auditor `h03-r98/conferir_qt.py`, sem alterar seus critérios. Em cada ponto, releram-se **Adicional (G)** e **Q_TELHADO_MANUTENCAO (QT)**, X/Y, Fx/Fy/Fz e Mx/My/Mz, com unidades kN e kN.m. A ação G foi conservada no recorte observado. A unidade cm de X/Y vem do contexto conferido da interface, não do texto isolado da árvore.

A resultante analítica QT é 13,985625 kN descendente; os valores de entrada com seis casas totalizam 13,985628 kN. A diferença é 0,000003 kN. A tolerância de leitura de 0,0000051 kN acomoda a precisão exibida, sem representar tolerância estrutural. Em RC03 e RC06, por exemplo, a releitura exibiu −1,04812 e −1,89469 kN, respectivamente, nos dois ramos.

As 52 árvores reais estão em `leituras/`; `R98-auditoria-leituras.json` registra o resultado individual e os hashes. `R99-comparacao-cadastros.json` compara os 26 pares. O manifesto associa as leituras às fontes e aos PRJ conferidos. O texto da árvore e o nome dos arquivos não provam sozinhos a sequência operacional; o registro de salvar/fechar/reabrir e os congelamentos complementam essa evidência. A leitura final RC01 BIM foi feita novamente no estado com as 13 cargas; a leitura anterior, feita no estado com uma carga, permanece no histórico separado.

O recorte cobre somente A1/A2. P1/P2, a verificação localizada da cobertura, perfis e ligações metálicas continuam pendentes. Não se substituiu a sobrecarga da laje por QT. Nesta revisão não houve novo processamento estrutural, alteração de geometria, edição de RVT/DWG ou da monografia.

## Tempos observados

| Intervalo exploratório | Relógio monotônico |
|---|---:|
| BIM: recuperação, lançamento e conferência | 7.353,9160671 s — aproximadamente 2 h 02 min 34 s |
| CAD: lançamento e conferência | 8.550,817726 s — aproximadamente 2 h 22 min 31 s |

Os JSON preservam horários UTC e duração monotônica separadamente. Os intervalos incluem recuperação da interface, raciocínio, trabalho intercalado e lacunas de conversa. A janela CAD atravessou a interrupção da conversa e a retomada; não se estimou nem subtraiu esse período. Os limites também diferem pela recuperação do BIM. Não se mediu esforço humano ativo nem inferência isolada da IA; não se calcula vantagem percentual entre esses intervalos. A R98 interrompida anterior permanece separada, sem substituição retroativa do seu resultado.

O inventário atualizado, em `inventario-tempos/R86-inventario-tempos.json`, reconheceu 152 arquivos candidatos: 114 intervalos com duração, 26 registros sem duração principal e 12 contêineres não expandidos. Mantiveram-se 11 pares sobrepostos sem soma, quatro demonstrações separadas e três sessões do banco central resumidas. A revisão R86 identifica o formato da ferramenta. Os totais completos CAD/BIM continuam nulos e o ranking final continua desautorizado pelos dados.

## Validação e continuidade

Os sete controles Python do auditor passaram; incluem casos sintéticos e recusa de evidência inválida. Não são sete operações nativas nem sete verificações de engenharia. O auditor foi executado também nas 52 leituras reais, todas aceitas. Os scripts de consolidação não fizeram chamadas adicionais à API da IA.

`R99-matriz-fechamento-atualizada.json` mantém as 12 frentes abertas: QT13 é um marco concluído dentro da frente de ações, mas simultaneidade e combinações efetivas ainda precisam de conferência. Seguem cobertura P1/P2, reservatório de 1.000 L e apoio, paredes/aberturas, escada, vento, materiais completos, vínculos e ELU/ELS. Só depois cabe a transferência final e o ensaio pareado com limites iguais. O estudo permanece restrito à superestrutura com apoios idealizados, sem dimensionar fundações reais.

Para reproduzir a auditoria das leituras preservadas, a partir do repositório:

```text
python tcc-assistente/estudos/h03-r98/conferir_qt.py --out <nova-pasta> --reads D:/TCC/outputs/Fechamento-H03-R99-QT-CONFERIDA-NAO-EXECUTAR/leituras
```

O gerador recusa uma pasta de saída existente. Os arquivos R97/R98 anteriores permanecem como registros históricos do estado observado em cada etapa.

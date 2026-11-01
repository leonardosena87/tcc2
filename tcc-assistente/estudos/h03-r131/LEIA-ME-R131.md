# H03/R131 — análise isolada com a linha W15

Processaram-se cópias CAD 46 e BIM 47, derivadas da R130. A única nova parcela em relação à referência R116 é a linha W15, 4,695 kN/m por 0,95 m, na laje L4/N1. O ensaio W03 em toda a viga da R121 não foi incorporado.

| Parcela exibida | CAD | BIM |
|---|---:|---:|
| Peso próprio | 75,69 tf | 75,69 tf |
| Adicional | 11,00 tf | 11,00 tf |
| Acidental | 17,11 tf | 17,11 tf |
| Q_TELHADO_MANUTENCAO | 1,78 tf | 1,78 tf |
| Total | 105,59 tf | 105,59 tf |

Ante a própria R116, o total exibido aumentou 0,45 tf e a ação Adicional aumentou 0,44 tf. Essa diferença de 0,01 tf entre os deltas é conservada: os dois resumos são arredondados. A integral nominal é 4,46025 kN; pela convenção de exibição observada R125, o acréscimo esperado é 0,446025 tf. Ambos os deltas cabem no intervalo de erro de até 0,01 tf da subtração de duas leituras com duas casas. Isso não é conversão SI exata nem auditoria completa de equilíbrio ou das reações locais.

**Ambos terminaram com avisos**, inclusive relação de carga por área não usual para edifícios. Não se considerou esse aviso resolvido por concluir a análise. As demais cargas da edificação continuam incompletas.

Os deslocamentos horizontais exibidos permanecem 0,20 cm nas quatro direções; o relativo é 0,17 cm. A direção relativa continua CAD N1/Y− e BIM TCC-cdd31967-N1/Y+. Gama-Z exibido: 1,09 X+; 1,08 X−; 1,06 Y+; 1,05 Y−. Limites mostrados no software não representam aprovação normativa.

No acréscimo percentual de topo por Desaprumo X+, registrou-se CAD 14,41% e BIM 14,40%, diferença −0,01 ponto percentual. Os outros campos de topo comparados coincidem na precisão exibida. Não se comprovou a causa ou um defeito de transferência.

| Ramo | Sessão observada | Comando até observação do término |
|---|---:|---:|
| CAD | 3.531 min | 40.673 s |
| BIM | 4.121 min | 41.809 s |

O intervalo do comando está contido na sessão e não deve ser somado novamente. Inclui espera e latência de captura; não mede solver isolado, inferência da IA ou produtividade final. A navegação e o aprendizado diferem entre sessões. Tempos finais CAD/BIM e ranking continuam abertos.

Executou-se estática linear e ELS-DEF do pórtico com rigidez configurada. Não houve dimensionamento, flechas de lajes, cálculo de rigidez fissurada ou análise dinâmica. A distribuição local da linha na grelha e as reações individuais ainda não foram auditadas. A etapa não encerra ELU/ELS nem aprova seções.

Preservaram-se 35 arquivos das fontes R130 e congelaram-se os arquivos calculados, com hashes verificados, em `congelados-apos-processamento/CAD` e `BIM`, neste diretório local. Monografia e arquivos de autoria Revit/AutoCAD não foram alterados.

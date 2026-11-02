# R168 — verificação nativa de lançamento nos modelos corrigidos

Executou-se **Lançamento → Outros → Verificar lançamento** no Eberick 2025 Infinity, nos pavimentos principais N1/N2 dos receptores CAD R165 e BIM R167. O comando foi identificado também no manual instalado do fabricante. Não se processou ou dimensionou a estrutura.

| Ramo e pavimento | Resultado observado |
|---|---|
| CAD R165 — N1 | Mensagem: não foram detectados problemas no lançamento deste pavimento. |
| CAD R165 — N2 | Mesma mensagem. |
| BIM R167 — N1 | Um aviso, 1/1: L10, laje L6, laje em balanço não engastada. |
| BIM R167 — N2 | Mensagem: não foram detectados problemas no lançamento deste pavimento. |

O aviso BIM se refere à varanda. As 11 lajes apresentaram propriedades IFC exportadas coincidentes com o CAD na R167; a divergência de vínculo localizada pela verificação nativa demonstra que essa igualdade de propriedades/geometrias não esgota a qualidade do modelo de análise. Antes de corrigir, preservaram-se o PRJ e as evidências do aviso.

Esse quadro descreve **modelos já corrigidos e recompostos**, não a comparação dos intercâmbios brutos nem o total de correções CAD/BIM. Não é uma classificação conclusiva de superioridade. Os pavimentos N0 e o croqui intermediário CAD do patamar não foram diagnosticados nesta série. A ausência de mensagem em um pavimento não aprova cargas, rigidez, ligações, armaduras, estabilidade, ELU/ELS ou compatibilização arquitetônica.

`R168-observacoes-nativas.json` registra os intervalos entre o clique do comando e a observação do resultado. Incluem execução e captura pela automação; excluem navegação entre projetos/pavimentos. Não representam tempo puro do processador, fluxo completo ou medições repetidas controladas de desempenho. Os quatro resultados possuem capturas PNG e leituras da interface.

Os hashes dos dois PRJs e dos IFCs de controle foram conferidos após as consultas. Não se salvou modificação de projeto nesta etapa. O trabalho escrito e os arquivos de autoria Revit/AutoCAD permanecem preservados.

Próxima ação: em nova cópia do BIM R167, rever/modelar o vínculo da varanda e confirmar o aviso novamente, sem confundir sua eliminação com dimensionamento aprovado. Permanecem a escada nativa, seu apoio inferior, interferência V16/J4 e conferência completa de cargas/vínculos para cálculo pareado.

# H03/R188 — teste de gancho nos receptores CAD e BIM

Estudo preliminar, não executar. Criaram-se duas cópias independentes, `D:/TCC/outputs/R188-CAD-ANCORAGEM-LE3-NAO-EXECUTAR` e `D:/TCC/outputs/R188-BIM-ANCORAGEM-LE3-NAO-EXECUTAR`, a partir dos controles R184. Não se incorporou a unificação V2/V14 da R187 a esse teste da escada. Preservaram-se os PRJs fontes R184 e R182, conferidos por SHA-256. O projeto escrito não foi alterado.

## Procedimento efetivamente realizado

Em cada receptor, alterou-se Projeto → Detalhamento → Lajes → Ancoragem da armadura de **reta** para **gancho** pelo campo nativo. A leitura acessível e a captura confirmaram a seleção. A captura do diálogo reaberto confirmou a retenção; no CAD essa releitura ocorreu antes do cálculo e no BIM depois do cálculo. A opção “Evitar o traspasse de 100% das barras na mesma direção” permaneceu desmarcada nas capturas. Não se elevaram limites de dispensa para eliminar o erro.

Executou-se o dimensionamento de vigas, pilares e lajes de N1/N2 e de escadas de N1. N0 e fundações permaneceram excluídos. Mantiveram-se o cálculo dos deslocamentos do pórtico com rigidez configurada e as mesmas opções dos controles: flechas de lajes, dinâmica, etapas construtivas e verificação dos limites de redistribuição semirrígida desativadas. Portanto, o ensaio não conclui a verificação de todos os estados-limite.

## Resultado observado

Nos dois receptores, LE1 e LE2 permaneceram como “calculado” na planilha Positivo. **LE3 permaneceu com D31**, e a janela de resultados da armadura identificou **A11 — largura do apoio insuficiente** para todas as bitolas exibidas: 6,3; 8; 10; 12,5 e 16 mm.

Assim, a seleção de gancho, isoladamente, não resolveu a ancoragem na condição testada. Não se concluiu que qualquer solução com gancho seja inviável, nem se identificou automaticamente o bordo que governa o erro. Deve-se conferir a largura física disponível, o cobrimento, o espaço para a dobra e a ligação ao apoio idealizado. Os marcadores de apoio não comprovam uma peça física contínua de ancoragem.

As contagens do relatório de vigas, pilares e lajes conservaram o padrão dos controles: N1 CAD com 16 vigas com sucesso; N1 BIM com 11 com sucesso e uma com erro. Essa diferença pertence aos agrupamentos originais, cujo efeito foi investigado separadamente na R187. O resumo de lajes não comprova aprovação da escada.

## Tempos

| Registro deste ensaio | CAD | BIM |
|---|---:|---:|
| Processamento nativo total | 7 s | 7 s |
| Dimensionamento, contido no total | 2 s | 2 s |
| Comando até primeira confirmação observada | 19,170 s | 20,149 s |

Há uma observação por receptor, CAD antes de BIM, no mesmo computador. Os intervalos observados incluem latência do controle e da observação; não são tempo ativo nem duração completa dos fluxos. Não se somaram novamente os 2 s aos 7 s. A diferença entre intervalos observados não foi usada como vantagem de produtividade.

## Evidência e continuidade

Preservaram-se relatórios DOCX nativos, textos extraídos, seleção do cálculo, opções, confirmação de gancho e resultados de A11. O consolidador confere a integridade ZIP dos PRJs experimentais salvos, os hashes dos controles, o registro de término e as cinco mensagens por receptor. O ensaio é real no Eberick; a conferência automatizada de evidências não substitui revisão estrutural.

Não se produziram novos IFC/SAP nesta revisão. Os arquivos herdados das cópias não são exportações R188 e não comprovam retenção integral de geometria e cargas. Permanecem a identificação do apoio/bordo de LE3, o detalhamento da ligação inferior, V16/J4, cargas e estados-limite pendentes, a revisão das armaduras e a comparação final de tempos e correções com fronteiras equivalentes. As fontes principais não foram substituídas por estas cópias de diagnóstico.

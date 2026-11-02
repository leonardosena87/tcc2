# R164 — teste de continuidade geométrica dos pilares

Resultado experimental de 02/11/2026. O receptor foi criado, salvo, fechado e reaberto no Eberick 2025 Infinity. O projeto de cálculo principal e o trabalho escrito não foram alterados.

## Alteração isolada

Partiu-se do IFC explicitamente derivado R162, com as 30 vigas nominais. Recompuseram-se somente as representações e colocações de quatro segmentos existentes de pilares — IDs 472934/473029/473143/473144 — até as cotas nominais lidas no Revit. Não se criou posição adicional de pilar. As identidades, materiais, propriedades, níveis e outras 64 geometrias de elementos foram preservadas e verificadas após reabrir o IFC. A validação de esquema não apontou ocorrências novas; isso não é aprovação de engenharia.

O arquivo resultante é **derivado**, não uma exportação nativa Autodesk. O IFC bruto R160 e o receptor R162 permanecem preservados. A intervenção recompõe continuidade nominal para um teste de conversão; não isola a causa dos cortes na autoria nem substitui a avaliação das uniões entre pilares, vigas e lajes.

## Recepção real e efeito observado

Foi utilizada a configuração inicial do programa, mantendo os nove níveis brutos e habilitando a importação de pilares e vigas. O mesmo aviso de seções retangulares foi registrado. O relatório nativo reconhece 52 origens: 30 vigas e 22 segmentos de pilares, uma ocorrência por ID.

No croqui N1, P12(NASCE) e P13(NASCE) foram substituídos por P5 e P6 nas mesmas posições, sem os dois rótulos NASCE. O resultado persistiu após fechar e reabrir o PRJ; o hash permaneceu igual ao primeiro estado salvo. O diálogo do P5 foi lido: 20 × 30 cm, elevação zero. Trata-se de evidência nativa localizada, ainda sem leitura integral da topologia dos nós.

O IFC4 de controle apresenta 33 peças de vigas e 66 de pilares. A segmentação entre níveis não foi contada como criação de 66 pilares físicos. As 33 peças foram associadas às 30 origens, com cobertura dos trechos fora dos pilares e seções/topos compatíveis com os valores nominais dentro da tolerância geométrica declarada. Os intervalos verticais nominais das 22 origens de pilares ficam cobertos, ante 18 de 22 na R162.

**As caixas das vigas receptoras não ficaram todas idênticas à R162.** Doze origens tiveram os limites longitudinais recortados de outra forma. A diferença de projeção ficou restrita às projeções dos pilares; as projeções fora dessas regiões permaneceram iguais. Não se transformou essa alteração em doze novos erros ou em validação da ligação analítica.

## Tempos e validação

- Geração, reabertura e conferência automática do IFC derivado: 2.269,6161 ms. Exclui desenvolvimento do código e revisão.
- Seleção do IFC até observação após Salvar no Eberick: **157.740 ms = 2 min 37,740 s**, incluindo foco e espera da planificação. Exclui desenvolvimento, geração da variante, auditoria e releitura posterior.
- Clique Gerar até a observação seguinte: ver `R164-exportacao-observacao.json`; esse intervalo não representa a etapa completa de exportação.
- Sete testes Python R163, três testes Python R164 e 81 testes Node aprovados. Os testes sintéticos de código não substituem a importação, os relatórios e a reabertura reais documentados.

Essas medições parciais não determinam o tempo total CAD/BIM, esforço total da IA, número final de correções ou vantagem percentual. As sessões anteriores permanecem separadas para evitar soma de tentativas alternativas como um único fluxo final.

## Arquivos principais e continuidade

- Receptor: `D:\TCC\outputs\R164-R160-CONTINUIDADE-PILARES-NAO-EXECUTAR\Projeto Eberick\R164-R160-CONTINUIDADE-PILARES-NAO-EXECUTAR.prj`.
- IFC de entrada derivado: `D:\TCC\outputs\Intercambio-H03-R164-CONTINUIDADE-PILARES-NAO-EXECUTAR\H03-R160-R164-DERIVADO-VIGAS-E-4-PILARES-NAO-EXECUTAR.ifc`.
- IFC4 de controle: `Arquivos do projeto\Modelo 3D.IFC`, sob o receptor.
- `R164-recepcao-auditoria.json`, `R164-derivado-conferencia.json`, `R164-receptor-congelamento.json` e `R164-reabertura-observacao.json`: rastreabilidade e limites do ensaio.
- PNGs N1 antes/depois da reabertura e leitura P5: evidência nativa.

Prosseguir em uma nova cópia: rever níveis auxiliares, conferir materiais/configurações e topologia, lançar lajes/escada/cargas, aplicar a mesma revisão geométrica ao CAD e realizar as verificações estruturais. Apoio inferior da escada e interferência da viga frontal com J4 continuam pendentes. O IFC receptor não contém lajes ou escada nativas nem relações IfcRelConnectsElements. Não houve novo processamento estrutural ou aprovação ELU/ELS. A seção 20 × 30 cm da viga de patamar permanece preliminar.

Não executar novamente `preparar_colunas.py` sobre o arquivo já existente; a proteção recusa sobrescrita. Não usar este receptor como versão final calculada.

# R162 — teste de intercâmbio com vigas nominais

02/11/2026. Variante acadêmica derivada; NÃO EXECUTAR. Não constitui exportação nativa do Revit nem dimensionamento.

## Mudança e preservação

O IFC bruto da R160, exportado na R161, contém 12 vigas cuja caixa de malha tem topo/altura diferentes dos parâmetros nominais do Revit. A variante R162 substitui a representação geométrica e a colocação das 30 vigas por prismas definidos pelos eixos e seções da releitura nativa R160. O objetivo é testar uma correção automatizada de intercâmbio, preservando o bruto como controle. A reconstrução não dimensiona elementos nem resolve suas ligações.

Preservaram-se GUIDs, Tags, nomes, associações de materiais, propriedades, níveis e geometria dos outros 38 elementos com malha. Isso inclui lajes, patamar e lances da escada; não se corrigiu sua conversão no Eberick. As propriedades mecânicas dos materiais continuam ausentes. O cabeçalho do derivado declara a transformação. As funções geométricas derivam do adaptador R95, com origem e hashes registrados. Não foram removidos níveis auxiliares.

A variante foi escrita e reaberta. As caixas das 30 vigas correspondem ao alvo nominal com tolerância numérica de 1e−7 m. A validação do esquema IFC antes/depois não apresentou erros. A verificação não prova adequação estrutural nem conectividade. Os quatro testes Python passaram, e o ensaio real está documentado separadamente.

## Teste real no Eberick

Criou-se `D:\TCC\outputs\R162-R160-VIGAS-NOMINAIS-NAO-EXECUTAR`, usando configuração inicial, nove níveis originais e Importar pilares e vigas marcado. O aviso de seções retangulares também apareceu. O receptor foi salvo e congelado antes da exportação de controle. O PRJ bruto R161 conservou seu hash inicial: ao trocar de projeto, descartou-se apenas o estado posterior das consultas, já que a importação inicial e o IFC de controle estavam preservados. Os projetos R148 e os arquivos autorais não foram substituídos.

O relatório do derivado confirmou as mesmas 52 origens: 30 vigas e 22 trechos de pilares. O IFC4 de controle contém 33 partes de vigas e 64 de pilares, sem lajes/escada nativas. Conseguiu-se associação espacial de 28 partes a 26 origens de vigas. Nenhuma dessas partes associadas apresentou diferença de topo, largura ou altura frente ao nominal. Restaram cinco partes sem associação segura por limites longitudinais; V3-N1, V4A-N1, V4B-N1 e V10-N1 não tiveram origem integralmente associada por esse critério. Não se forçou a associação nem se concluiu que as extensões estão corretas.

Para comparar a mesma amostra, 24 origens foram associadas tanto no receptor bruto quanto no derivado. Nessa amostra comum, oito apresentavam diferenças de topo/altura frente ao nominal no bruto e nenhuma manteve essas diferenças no derivado. Esse é um resultado geométrico parcial da correção de intercâmbio. Não equivale a oito erros exclusivos do importador: os desvios de topo já existiam no IFC bruto do Revit. Tampouco permite declarar as 30 vigas corrigidas integralmente ou o modelo pronto para cálculo.

## Tempos observados

| Registro | Intervalo | Escopo |
|---|---:|---|
| Geração e conferência do derivado | 1.905,0525 ms | Execução do script, incluindo abertura, reconstrução, escrita, releitura e validações |
| Recepção no Eberick | 275.661 ms = 4 min 35,661 s | Seleção da variante até observação após Salvar; inclui tentativas de foco/nome |
| Geração do IFC4 de controle | 1.191 ms | Clique Gerar até observação de retorno; exclui preparação e auditoria |

O desenvolvimento e a depuração do código não foram cronometrados integralmente. A geração de 1,905 s não representa todo o esforço da IA, do operador ou da correção. Os intervalos parciais não constituem tempo completo do fluxo BIM e não devem ser comparados diretamente ao tempo CAD parcial R161 para calcular vantagem percentual. Não houve chamada paga à IA medida nesses scripts.

## Pendências para avançar

- Conferir comprimento/cobertura axial e conectividade das vigas, incluindo as cinco partes sem associação segura. A geometria prismática nominal pode produzir encontros ou sobreposições que exigem tratamento no receptor.
- Conferir a continuidade e as seções dos pilares segmentados pelos níveis auxiliares. A contagem de 64 partes não prova duplicidade.
- Tratar níveis auxiliares, dados de concreto e parâmetros do programa em cópia apropriada, com a mesma base dos dois fluxos.
- Integrar lajes, escada, apoios e cargas. Resolver a interferência com J4 e o apoio inferior da escada, sem mudar a arquitetura por iniciativa automática.
- Aplicar as revisões equivalentes ao ramo CAD e depois realizar a comparação controlada de correções e tempos. O receptor R162 é experimental e não substitui a cópia BIM de cálculo derivada da R148.
- Efetuar processamento, ELU/ELS, detalhamento e conferência técnica antes de qualquer conclusão estrutural. Nenhum cálculo estrutural foi executado neste receptor.

## Arquivos

Pasta de evidências: `D:\TCC\outputs\Intercambio-H03-R162-SECOES-NOMINAIS-NAO-EXECUTAR`.

- `H03-R160-R162-DERIVADO-VIGAS-NOMINAIS-NAO-EXECUTAR.ifc`: variante, distinta do bruto.
- `R162-derivado-conferencia.json`: transformação e preservação verificadas.
- `R162-recepcao-auditoria.json`: relatório nativo e IFC4 real do receptor.
- `R162-comparacao-associacoes-comuns.json`: comparação das mesmas 24 origens.
- `R162-recepcao-observacao.json`, `R162-exportacao-observacao.json`: intervalos e limites.
- `R162-receptor-congelamento.json`, `R162-controle-congelamento.json`: hashes dos estados preservados.

Para reproduzir a geração em nova pasta de saída, usar `preparar_derivado.py`; o script recusa sobrescrever a variante existente. Para reler a recepção salva, usar `auditar_receptor.py`. Este depende das funções de leitura/associação da R161, cujos hashes constam em `R162-dependencias-auditoria.json`. `python -m unittest -v test_derivado` executa os quatro testes de limites/escopo geométrico.

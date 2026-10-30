# Demonstração 2 — Duas formas, a mesma área

A primeira demonstração cria o pórtico inicial. Esta segunda gera outra proporção por linguagem natural, mantendo a área em planta e as seções ilustrativas. Cada alternativa é criada em um arquivo independente. O botão não lê o modelo aberto para deduzir dados e não altera o primeiro pórtico.

## Como apresentar em aproximadamente 2 minutos

1. Mostrar a vista inicial de 6 × 4 m: “Esta alternativa tem 24 m² de área em planta”.
2. Abrir **Complementos → IA • Palestra TCC → Demonstração IA** e colar `alternativa-8x3-pedido.txt`: “Agora será gerada outra proporção, de 8 × 3 m, mantendo a área e as seções informadas”.
3. Clicar em **Gerar prévia com IA**, aguardar e conferir as dimensões. Explicar que a IA interpreta o texto e que o complemento cria os elementos pela API do Revit.
4. Clicar em **Criar no Revit**. Alternar entre as duas vistas 3D para mostrar a mudança de forma.
5. Mostrar a conferência: ambos têm quatro pilares, quatro vigas e uma laje de 24 m²; o somatório dos comprimentos dos eixos das vigas muda de 20 para 22 m.

Usar o pedido completo: não basta escrever “mude para 8 × 3”, pois a janela não mantém contexto dos pedidos anteriores. **Exemplo ensaiado** repõe o exemplo local de 6 × 4 m; a alternativa de 8 × 3 m usa o pedido e a consulta real à IA.

## Ensaio real conferido em 30/10/2026

| Verificação | Base 6 × 4 m | Alternativa 8 × 3 m |
|---|---:|---:|
| Área nativa da laje | 24 m² | 24 m² |
| Elementos físicos conferidos | 9 | 9 |
| Comprimentos nativos das vigas | 6, 4, 6, 4 m | 8, 3, 8, 3 m |
| Interpretação pela API de IA | 3,01 s | 5,84 s |
| Criação geométrica pela API Revit | 0,53 s | 0,57 s |
| Comando completo registrado | 72,21 s | 86,03 s |

O comando completo inclui digitação, revisão, consulta, abertura da cópia, geometria, vista e salvamento. Os tempos não constituem comparação controlada de produtividade. Não somar novamente parcelas já incluídas no total. O JSON guarda os valores sem arredondamento e o uso efetivo de tokens; não se estimou custo.

Os nove elementos foram conferidos por ID e UniqueId, além da área da laje e dos comprimentos das vigas, por uma exportação de leitura do conector existente. Cada seleção continha também uma caixa de corte da vista, excluída da contagem física. A conferência ocorreu no documento após o salvamento, sem reabertura nesta rodada.

A área e a quantidade de elementos iguais não demonstram equivalência de desempenho. Vãos, solicitações e flechas exigem análise estrutural. O somatório dos eixos não representa comprimento de fabricação. Esta variação não é otimização estrutural nem resultado da comparação CAD/BIM do TCC.

## Arquivos locais

Base: `D:/TCC/palestra-IA-engenharia/demonstracao/execucoes/20261030-161839-c5c4333f/DEMO-IA-RESULTADO.rvt`.

Alternativa: `D:/TCC/palestra-IA-engenharia/demonstracao/execucoes/20261030-182943-f53a01ee/DEMO-IA-RESULTADO.rvt`.

As vistas aparecem na sessão como `DEMO-c5c4333f - 3D` e `DEMO-f53a01ee - 3D`. Capturas dos modelos, prévia e mensagem de conclusão ficam em `D:/TCC/palestra-IA-engenharia/demonstracao-2-alternativas` e servem como apoio se a internet falhar. São enquadramentos diferentes; a conferência dimensional usa os parâmetros nativos.

Os RVT permanecem fora do repositório público. Esta segunda demonstração utiliza o botão existente, sem alteração de código. O modelo H03 e o trabalho escrito não foram usados como destino.

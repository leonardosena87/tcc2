# R167 — lançamento das 11 lajes no receptor BIM

Revisão real no Eberick 2025 Infinity em 02/11/2026, sobre cópia independente da R166. O projeto foi salvo, fechado e reaberto. O trabalho escrito não foi alterado.

## Desenvolvimento

Lançaram-se seis lajes no N1 e cinco no N2, todas maciças de 14 cm, elevação zero, ambiente Externo e grupo Nenhum. Reaplicaram-se os parâmetros registrados no ramo CAD R165: N1 L1–L4, acidental 1,5 kN/m² e revestimento 1,25 kN/m²; N1 L5 e varanda L6, acidental 2,5 kN/m² e revestimento 1 kN/m²; N2 L1–L5, acidental 1 kN/m² e revestimento 0,25 kN/m². Esses valores foram copiados como referência de comparação, sem nova aprovação normativa das cargas.

O IFC não forneceu as barras de contorno nativas da varanda. Inseriram-se três barras de largura zero entre (965;380), (1072,5;380), (1072,5;710) e (965;710), em centímetros. São elementos de delimitação de bordo livre, sem criação de vigas físicas ou pilares. Mantiveram-se os limites do perfil de varanda da autoria R160: X externo 10,725 m; Y=3,80–7,10 m. Os avisos de vértices livres e as tentativas de entrada numérica foram incluídos no intervalo observado.

## Conferência independente

O IFC4 de controle contém 33 peças de vigas, 22 segmentos de pilares e 11 lajes. As geometrias das vigas e pilares permaneceram iguais às do receptor R166. As 11 lajes foram associadas espacialmente, de forma única, às lajes CAD R165. Não se utilizou apenas o nome para associar os pavimentos.

Dez pares têm a mesma nuvem de pontos arredondada a 10⁻⁸ m. No par L3 do N1, dois vértices do BIM apresentam X=6,65001 m, enquanto o CAD registra 6,65000 m: diferença de 0,01 mm. Os 11 pares ficaram dentro da tolerância computacional declarada de 0,1 mm, com correspondência única dos pontos mais próximos. Não se declarou igualdade exata de todas as malhas. A comparação das caixas utiliza 0,01 mm e não substitui a comparação dos vértices.

Os conjuntos de propriedades exportados das 11 lajes coincidiram entre os receptores, retirando-se apenas os IDs internos dos conjuntos. Isso inclui os valores brutos exportados das ações. Não se converteu silenciosamente a unidade desses valores IFC; as entradas em kN/m² estão documentadas nas leituras da interface. Coincidência de propriedades exportadas não verifica todas as configurações, direções de grelha, vínculos, cargas de vigas ou adequação normativa.

O PRJ reaberto conservou o hash `936da7d187905771b918a906481f5d4149887928083a618fec6eb59dfc106e24`. Os arquivos registrados da R166 foram conferidos por hash e permanecem preservados.

## Tempo

Comando inicial de laje até observação após salvar as 11 lajes e o contorno da varanda: **722.648 ms = 12min02,648s**. Inclui parametrização, cliques, foco, tentativas, consulta ao manual local e conferências da sessão. Exclui a cópia preparatória e as auditorias posteriores.

Os intervalos N1 e N2 são subdivisões sobrepostas a esse intervalo total da etapa: não somá-los novamente. Não é o tempo total do fluxo BIM, tempo de cálculo estrutural ou esforço computacional puro da IA.

Três testes sintéticos do comparador de pontos passaram, incluindo mudança de ponto com a mesma caixa e correspondência não única. A auditoria dos arquivos reais e a reabertura nativa são evidências separadas.

## Arquivos e pendências

PRJ: `D:\TCC\outputs\R167-BIM-LAJES-NAO-EXECUTAR\Projeto Eberick\R166-R160-3NIVEIS-CONFIG-CAD-NAO-EXECUTAR.prj`. O nome interno herdado R166 não significa que se deva abrir o controle R166 em seu diretório original.

IFC4: `Arquivos do projeto\Modelo 3D.IFC`, sob a cópia R167. Auditoria: `R167-lajes-auditoria.json`. As capturas de N1/N2, parâmetros de lançamento e reabertura acompanham os registros.

Permanecem a escada nativa no Eberick, seu apoio inferior, interferência V16/J4, conferência de vínculos e cargas, processamento ELU/ELS e consolidação final dos dois fluxos. Não houve novo cálculo estrutural ou conclusão de superioridade CAD/BIM nesta revisão.

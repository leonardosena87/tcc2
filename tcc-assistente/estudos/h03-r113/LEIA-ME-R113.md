# H03/R113 — referências verticais do receptor e do corte BB

Consultaram-se os três pavimentos de cada ramo em cópias independentes da R111. Todos os diálogos foram cancelados; fecharam-se os projetos sem salvar ou processar. Os 35 arquivos fontes R111 permaneceram inalterados e os PRJs das cópias consultadas conservaram os hashes iniciais. Diferenças auxiliares estão discriminadas no JSON, incluindo o apontamento INI ajustado durante a preparação.

| Pavimento comum | Nome no CAD | Nome no BIM | Altura de pavimento (cm) | Nível absoluto cadastrado (cm) |
| --- | --- | --- | ---: | ---: |
| N0 | N0 | TCC-cdd31967-N0 | 100 | 20 |
| N1 | N1 | TCC-cdd31967-N1 | 300 | 320 |
| N2 | N2 | TCC-cdd31967-N2 | 319 | 639 |

Os seis campos numéricos pareados coincidiram. Altura de pavimento e nível são grandezas diferentes: a soma de 100 + 300 + 319 cm é 719 cm, enquanto o nível cadastrado de N2 é +639 cm. A soma corresponde aritmeticamente a uma origem −80 cm em relação ao datum dos níveis. Isso não comprova, por si só, qual origem o módulo de vento usa ou a adequação desse parâmetro. Não se alterou o nível de N2 para fazê-lo coincidir com uma altura acumulada.

## Registro gráfico da arquitetura

No corte BB, identificou-se a ponta do marcador +3,25 m do quarto em PDF (1092,240; 2018,000). Utilizou-se essa ponta, não a posição do texto, como âncora de altura. A escala vertical da leitura de 1,30 m da R112 foi mantida. A transformação inverte a direção Y do PDF: `Z = 3,25 + (2018,00 − Ypdf)/escala`.

| Referência desenhada no corte | Cota derivada aproximada (m) |
| --- | ---: |
| Piso acabado do quarto, âncora | +3,25 |
| Forro superior | +6,05 |
| Topo da laje principal desenhada | +6,21 |
| Base elevada do reservatório | +6,81 |
| Topo da platibanda elevada | +8,11 |

Conferiram-se dois controles independentes da operação de soma: o forro fica aproximadamente 2,80 m acima do piso acabado e o ressalto entre o topo da laje principal desenhada e a base do reservatório é aproximadamente 0,60 m. Os resíduos gráficos ficaram abaixo de 5 mm; esse limiar é um controle aritmético da leitura, sem representar tolerância de execução ou precisão de levantamento.

A base gráfica está aproximadamente **0,42 m acima do N2 estrutural cadastrado**, não 0,60 m. Usar N2 + 0,60 m produziria +6,99 m, cerca de 18 cm acima da base interpretada do corte, reduzindo ainda mais o espaço superior. Essa diferença é relevante para conceber o suporte preservando a arquitetura. A leitura preliminar de +6,81 m ainda não constitui uma cota executiva adotada ou um elemento criado no modelo.

O topo da laje estrutural N2 de +6,39 m não coincide com o topo da laje desenhada no corte, próximo de +6,21 m. A hipótese H03 preserva o forro com a geometria estrutural já estudada; a diferença precisa entrar no desenho do apoio e da cobertura, sem ser ocultada por um deslocamento global de coordenadas. Não se corrigiu a arquitetura nem se declarou compatibilização integral por coincidência do forro.

## Limites e continuidade

Não se criou plataforma, pedestal, novo pavimento ou carga do tanque. A solução de acesso e a tara continuam pendentes. Os perfis de P2 e as ligações precisam ser compatibilizados com o contorno da R112 e as referências agora relacionadas. A parte gravitacional do telhado P2 pode ser estudada separadamente do reservatório, conservando explícita a hipótese de transmissão aos nós existentes e os limites do esquema metálico.

As sessões de consulta constam em arquivos próprios com UTC e duração monotônica. Incluem navegação e evidências, não inferência isolada, produtividade ou tempo completo dos fluxos. Dois controles verificam a separação entre altura e nível, a recusa de campos contraditórios e o sentido da transformação vertical. Não substituem verificação estrutural. Os arquivos permanecem em `D:/TCC/outputs/Altimetria-H03-R113-CONSULTA-NAO-EXECUTAR/`.

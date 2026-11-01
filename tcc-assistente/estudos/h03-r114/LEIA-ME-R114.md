# H03/R114 — hipótese gravitacional do telhado P2

Definiu-se o esquema P2-GRAV-A para o abrigo elevado nominal X6,55..9,65/Y0..3,90 m, área de 12,09 m². O esquema separa o telhado do reservatório: água, tara, plataforma e pedestal não estão incluídos. Preservam-se as referências arquitetônicas R112/R113; não se elevou o telhado.

Como idealização gravitacional, dois quadros transversais na direção X, em Y0 e Y3,90, recebem terças na direção Y. Quatro montantes alinhados aos nós de concreto N2 transmitem as cargas verticais. Sob carga distribuída uniforme e simetria desse esquema articulado, cada canto recebe um quarto da resultante. O esquema não acrescenta rigidez metálica ao modelo de concreto e não define empuxo horizontal, altura final dos perfis, estabilidade lateral ou vento.

| Ponto | X;Y nominal (m) | Pilar histórico CAD/BIM | Incremento G, Fz (kN) | Incremento QT, Fz (kN) |
| --- | --- | --- | ---: | ---: |
| RP2-01 | 6,55; 0,00 | P10 / P10 | −1,000138483 | −0,755625000 |
| RP2-02 | 9,65; 0,00 | P7 / P11 | −1,000138483 | −0,755625000 |
| RP2-03 | 6,55; 3,90 | P11 / P6 | −1,000138483 | −0,755625000 |
| RP2-04 | 9,65; 3,90 | P8 / P7 | −1,000138483 | −0,755625000 |

Mantiveram-se G = 0,330897761180176 kN/m² horizontal e QT = 0,25 kN/m² horizontal da R59. O incremento soma G = 4,000553933 kN e QT = 3,022500000 kN descendentes. Força vertical e primeiros momentos em X/Y coincidiram com a resultante distribuída no retângulo nominal. Esse equilíbrio valida apenas a aritmética da idealização.

O G mantém a reserva de 0,15 kN/m² para a estrutura metálica, sem levantamento dos perfis ou dos montantes altos. A reserva pode exigir revisão quando o sistema for dimensionado. O caimento de 10% pertence à geometria arquitetônica; não se usou a soma do peso para afirmar capacidade dos quadros ou das ancoragens. A transmissão colinear de uma força puramente vertical aos nós inferiores não gera momento adicional pelo deslocamento vertical, mas isso não representa os efeitos reais das ligações, vento ou excentricidades construtivas.

RP2-04 coincide com VP1-01 da varanda. O lançamento posterior deve **preservar as parcelas anteriores de Fz e My**, somando apenas o incremento P2. Não se deve substituir a força total existente pelo incremento nem zerar o momento da varanda. A correspondência histórica por caixas R56, vinculada à R60 por hash, precisa de conferência no receptor; nomes não são suficientes para parear os ramos.

O plano R114 não lançou cargas nativas. Na aplicação, devem-se confirmar as cargas existentes, usar cópias independentes, salvar, fechar, reabrir e reler todas as componentes por ação nos quatro apoios. O arredondamento de G para seis casas deve permanecer explícito. A cobertura completa A1/A2/P1/P2 possui área nominal de 71,1825 m²; a consideração dessas quatro parcelas ainda não encerra vento, caso localizado de manutenção, platibandas, calhas, policarbonato, tanque ou combinações.

Permanecem indefinidas a geometria executiva e a compatibilidade dos perfis sob a cobertura, o acesso ao reservatório e as ligações. Não se dimensionou o metal, o concreto ou suas ancoragens. Dois controles verificam o equilíbrio e rejeitam dados inválidos; o tempo de script mede somente a aritmética e identificação histórica. Os arquivos ficam em `D:/TCC/outputs/Cobertura-H03-R114-P2-HIPOTESE-NAO-EXECUTAR/`.

# R203 — Apoios da escada, largura da V2 e extensão da W08

Em 03/11/2026 foi lida a cópia experimental BIM R202. O relatório nativo por elemento foi gerado para todos os casos e combinações selecionados, juntamente com uma exportação SAP do pórtico, da grelha da escada e dos dois painéis de lajes. Os quatro arquivos são dados de entrada. Não houve nova rodada de dimensionamento nem cronometragem de processamento na R203.

## Apoios da V2

A seção de 60 cm da R202 foi projetada sobre as caixas geométricas dos pilares nos IFCs de referência R178. Os eixos dos trechos coincidem em Y = 3,90 m. A hipótese de projeção centrada resulta na tabela abaixo. As dimensões são transversais ao eixo longitudinal da V2. O Eberick registrou Aviso 38 exatamente nos três apoios da R202. O levantamento utiliza uma referência geométrica anterior e não substitui a verificação do detalhamento e da transferência de esforços.

| Apoio BIM | Apoio CAD | Largura do pilar | Projeção da viga além de cada face |
|---|---|---:|---:|
| P4 | P2 | 30 cm | 15 cm |
| P5 | P5 | 30 cm | 15 cm |
| P6 | P11 | 20 cm | 20 cm |

A alternativa de 60 cm continua experimental. Um ajuste de eixo por si só não permite conter uma seção de 60 cm em apoios transversais de 20 ou 30 cm. O ensaio CAD equivalente precisa preservar a continuidade dos trechos V2 e V14 no apoio P5. A comparação de retrabalho continua referenciada no par R201.

## Esforços no pé da escada

A barra 14 do pórtico tem seção R20x30B, nós 85 e 86, comprimento de 88 cm e eixo paralelo a X. Seus extremos são (451, 321,58, 20) e (539, 321,58, 20) cm. As barras 120 e 121 ligam as extremidades aos nós 76 e 81 com trechos de 1 cm. A carga distribuída G1 e as 12 cargas pontuais G1/G2/Q na própria barra correspondem à direção local 2. O relatório por elemento dos apoios SAE1A e SAE1B usa eixos globais. Para G1, Vx é -8,03 e +8,03 kN, respectivamente. Nas combinações exportadas, os máximos em módulo de Vx são 12,47 kN em cada apoio, sob combinações diferentes. O maior |Vy| exibido em cada apoio é 0,34 kN. Os máximos de componentes isoladas não formam um caso simultâneo.

A envoltória nativa da V1 indica Vd inicial/final de 14,14/18,14 kN, Md positivo/negativo de 0,89/-2,34 kN.m e Mtd exibido de 0,00 kN.m. A componente horizontal de flexão da seção não é discriminada nessa planilha. O aviso 19 continua aberto. É preciso extrair ou calcular os esforços internos simultâneos nos dois eixos e conferir a capacidade da seção e a ligação aos apoios idealizados.

## Extensão efetiva da W08 superior

A barra 42 da V16 está em Y=0 e Z=177,4 cm, de X=441 até 654 cm. A exportação recém-gerada registra uma carga G2 uniforme em toda a extensão relativa 0 a 1, e G1 separadamente. Assim, a extensão efetiva do lançamento é 213 cm. O pano livre levantado na R195 vai de X=450 a 645 cm. A diferença é 9 cm em cada ponta. O fator geométrico de excesso é 213/195 - 1 = 9,23%. Utilizando a intensidade de projeto de 6,75454 kN/m, a resultante nominal é 14,39 kN para o lançamento atual e 13,17 kN para o trecho livre. A diferença nominal é 1,22 kN. Esses produtos usam a intensidade de projeto no SI. O SAP declara kgf e cm no cabeçalho e registra a intensidade numérica -6,7545 na direção local 2. O fator geométrico independe da conversão de unidades.

Para corrigir a carga na cópia de estudo, substituir o lançamento integral por uma carga restrita às faces reais e auditar a resultante depois de reprocessar. O pano inferior de 3,83 kN requer confirmação independente do apoio. A localização da V1 (Y=321,58 cm) difere da posição da W08 (Y=0), portanto não se justifica lançar automaticamente esse peso sobre a V1.

## Evidências

O diretório D:/TCC/outputs/Apoios-H03-R203 contém as quatro exportações SAP, o relatório nativo Pav1_Fundacao_Combinacoes.docx, as linhas dos dois apoios em JSON, a captura da envoltória da V1 e a medição IFC de cada ramo com hash do arquivo. As alterações de geometria e cargas descritas como pendentes ainda não foram executadas.

[Critério do Eberick para o Aviso 38](https://suporte.altoqi.com.br/hc/pt-br/articles/360007183014) e [Aviso 19](https://suporte.altoqi.com.br/hc/pt-br/articles/360009988354).

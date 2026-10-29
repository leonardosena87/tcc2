# H03/R53 — cargas uniformes parciais nos dois fluxos

Revisao de 29/10/2026. Arquivos em D:\TCC. Modelo academico preliminar, nao dimensionado, nao executar.

Aplicaram-se separadamente, no Eberick 2025 Infinity, as mesmas parcelas uniformes nas 11 lajes de cada ramo. Cada copia deriva do seu proprio estado R52 congelado, sem transplantar o PRJ de um fluxo ao outro. A monografia, RVT e DWG de origem nao foram alterados nesta etapa.

| Nivel e lajes nativas | Uso/hipotese | Q (kN/m2) | G2 parcial (kN/m2) |
|---|---|---:|---:|
| N1 L1 a L4 | Residencial | 1,5 | 1,00 |
| N1 L5 | Faixa junto a escada, hipotese provisoria de uso restrito | 2,5 | 1,00 |
| N1 L6 | Varanda residencial | 2,5 | 1,00 |
| N2 L1 a L5 | Cobertura de concreto, acesso apenas para manutencao | 1,0 | 0,25 |

Q fundamenta-se na Tabela 10 da ABNT NBR 6120:2019, exemplar local: PDF 24 (varanda), 25 (cobertura), 26 (residencial), 27 (escada). G2 do N1 e hipotese de pacote de piso de 5 cm a 20 kN/m3, parcial e revisavel; nao inclui automaticamente forro de pavimentos inferiores, paredes ou impermeabilizacao. G2 do N2 inclui somente a parcela de forro acartonado, cuja hipotese de sistema foi autorizada pelo usuario; o telhado e demais camadas nao estao incluidos. L5 nao substitui a modelagem da escada e suas reacoes. A varanda ainda exige guarda-corpo, carga de borda e camadas finais. O peso proprio de referencia da laje de 14 cm e 3,50 kN/m2; nao foi duplicado no campo de revestimento. A geracao do peso proprio e seus resultados ainda devem ser verificados no processamento.

Usou-se Lancamento > Outros > Copiar dados, marcando apenas Grupo de Carga (Nenhum), que leva as parcelas Q e G2. Geometria, elevacao, grelha, cargas extras e efeitos termicos permaneceram desmarcados. Aplicou-se a cada pavimento isolado; depois ajustaram-se L5 e L6 de N1 para 2,5. No CAD, a escolha da entidade em algumas anotacoes exigiu selecionar Laje em vez de Texto. Trata-se de esforco de interface observado, sem atribui-lo como defeito de intercambio.

## Verificacao real realizada

Ambos os PRJs foram salvos, fechados e reabertos. Leram-se apos reabrir as amostras L4/N1, L6/N1 e L4/N2 em cada ramo, com registros de acessibilidade TXT e observacao dos dialogos. Nao se afirma leitura nativa individual de todas as 11 apos reabrir. Exportou-se IFC4 de cada projeto reaberto para pastas exclusivas desta revisao. Os campos brutos Q e G2 das 11 lajes coincidiram com o padrao planejado nos dois arquivos. A razao empirica entre UI e esses campos e 100; o Pset nao informa unidade explicita. Isso nao autoriza conversao geral de outros campos IFC.

Cada exportacao contem 22 IfcColumn, 32 IfcBeam (29 vigas logicas) e 11 IfcSlab. Em relacao a propria R52, preservaram-se classes, nomes, GUIDs, caixas envolventes e areas superiores, com tolerancia computacional de 0,00001 m nos comprimentos. O confronto entre ramos tambem coincide para geometria das lajes e campos de carga. Nao se verificou identidade de malha completa nem ligacao analitica por esse controle. A integridade ZIP dos PRJs passou. Conferiram-se os hashes de 33 arquivos protegidos do manifesto R52; os estados nativos R53 foram congelados em separado.

## Tempos prospectivos desta etapa

| Ramo | Intervalo assistido de aplicacao, salvar/reabrir e amostragem |
|---|---:|
| CAD | 9 min 8.857 s |
| BIM | 10 min 50.100 s |

Os arquivos R53-tempo-CAD/BIM.json guardam inicio/fim UTC e duracao por relogio monotonico. Incluem raciocinio, latencia e operacao de interface. CAD incluiu descoberta e exploracao da copia de dados e ambiguidades Texto/Laje; BIM utilizou procedimento ja conhecido. Portanto, ha efeito de aprendizagem e nao houve repeticao controlada, mensuracao de tempo humano ativo ou isolamento de inferencia da IA. Nao calcular superioridade percentual nem ranking de fluxos completos a partir desses intervalos. Exportacao e execucao do auditor possuem registros adicionais, com escopos distintos explicitados e sem soma indiscriminada.

## Pendencias para calculo

- Paredes por trecho e aberturas.
- Telhado e caminho de suas reacoes.
- Reservatorio 1000 L: posicao, apoio, tara e base.
- Guarda-corpo e borda da varanda.
- Impermeabilizacao e camadas finais.
- Escada e reacoes.
- Vento e combinacoes.
- Apoios idealizados N0 e ligacoes analiticas.
- Verificacao ELU/ELS e alturas.

Mantem-se o recorte da superestrutura sem sondagem, com apoios idealizados ainda a conferir. Nao houve processamento estrutural, dimensionamento, comprovacao de estabilidade, ELU/ELS ou liberacao de execucao. Esta revisao e complementacao comum de acoes no receptor, nao contagem de falhas comprovadas da transferencia. Os proximos ajustes devem partir de novas copias, preservando R53.

Referencia operacional consultada: https://suporte.altoqi.com.br/hc/pt-br/articles/115003144013 (cargas tipicas e copia de dados). Nao se adotou um grupo padrao de uso sem verificar os valores.

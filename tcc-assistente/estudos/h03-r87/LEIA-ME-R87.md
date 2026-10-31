# H03/R87 — matriz comum de premissas e procedência

Consolidaram-se decisões já confirmadas pelo usuário em uma matriz de dados separada. Nenhum RVT, DWG, PRJ, configuração nativa ou texto acadêmico foi alterado. A proposta histórica R83 permanece preservada com seus metadados originais e hashes.

## Decisões incorporadas

- Município: Vitória da Conquista/BA; não se presumiram coordenadas do terreno nem parâmetros de vento.
- Parede: bloco cerâmico com 15 cm **acabados**. A espessura do corpo do bloco, a espessura de cada revestimento e o peso superficial completo permanecem nulos. Não se tratou uma parede acabada de 15 cm como bloco de 15 cm.
- Abatimento: centímetros confirmados, 10 ± 2 cm para lajes/vigas/pilares e 6 ± 2 cm para escadas. O valor nominal observado no Eberick e a tolerância documental são campos distintos.
- Reservatório: capacidade de 1.000 L confirmada. Posição, apoio, tara, pedestal e peso completo ainda não estão fechados; as alternativas R71 não foram promovidas a solução aceita.
- Escopo: superestrutura, sem sondagem e sem dimensionamento de fundações reais.
- Cobertura: telha de fibrocimento ondulada de 6 mm, inclinação de 10%, estrutura metálica leve, acesso de manutenção e forro acartonado como hipóteses aceitas no estudo. Isso não dimensiona os apoios metálicos ou encerra as regiões P1/P2.
- Preservação das alturas arquitetônicas. Não se elevou a cobertura para acomodar a estrutura.

## Valores documentais e leituras nativas

A classe C25, CA-50, CAA II, cobrimentos e dimensão máxima de agregado permanecem como premissas comuns. As leituras de materiais depois de salvar/fechar/reabrir R51 ficam identificadas como observações históricas; não foram apresentadas como nova inspeção dos PRJ R79 ou R85.

Preservaram-se separadamente Ecs informado de 24,1 GPa e Ecs exibido R51 de 24,150 GPa. O cadastro observado usava granito, enquanto a natureza petrográfica não foi confirmada pelo usuário ou por ensaio. O campo de cimento observado era CP-II, sem comprovar registro do subtipo E. A presença de CA50 nas linhas de bitolas não comprova a conferência de todo o cadastro mecânico do aço.

O padrão global `beamH=0,55 m` do gerador não descreve todas as vigas atuais. A matriz lista as seções das 29 unidades lógicas por elemento; as vigas N2 da R83 têm 0,30 m. Esse valor global não deve sobrescrever a lista nem ser usado isoladamente no levantamento.

O arquivo ainda contém referências históricas H02-R12 e pendências antigas de unidade/reservatório. Elas foram identificadas, sem reescrever o histórico ou atribuir essas inconsistências a um defeito de IFC/DWG. A versão da proposta é determinada pelo runId, eventos e hashes; nomes históricos não substituem essa procedência.

## Critério de qualidade da informação

A documentação oficial descreve a conversão automática de vigas e pilares IFC e o intercâmbio de propriedades estruturais. Essa capacidade do produto não comprova que um material específico tenha sido preenchido no autor e recebido no arquivo deste estudo. A classificação de uma diferença como perda exige evidência de origem, escopo de transferência e valor no receptor. [Recurso IFC do Eberick](https://www.altoqi.com.br/recursos/importacao-e-exportacao-ifc-openbim).

O importador geométrico do estudo utiliza os tipos da base; a releitura R83 usada na R84 não contém propriedades mecânicas de materiais. A matriz conserva como não conferida a procedência nativa dessas propriedades no Revit. Não se declara C25 transferido apenas porque existe C25 no cadastro do Eberick ou no JSON documental.

Conferir fatores de uma ação não demonstra que todas as ações estejam ativas, com grupos/simultaneidade e combinações adequados. O roteiro operacional distingue essas configurações; sua referência normativa histórica não substitui a edição adotada no estudo. [Configurações de ações](https://suporte.altoqi.com.br/hc/pt-br/articles/360000624993).

A menção à NBR 6118:2026 no arquivo não atualiza automaticamente um verificador que ainda identifica regras de 2023 nem comprova implementação integral no software instalado. Permanecem explícitos os limites R74. A matriz está **parcial e não liberada para o ensaio final**; cargas completas, ELU/ELS, vínculos e compatibilização ainda exigem fechamento.

Reprodução: `node consolidar-premissas.mjs D:/TCC <nova-pasta-de-saida>`. O script verifica fontes e escreve somente na nova pasta.

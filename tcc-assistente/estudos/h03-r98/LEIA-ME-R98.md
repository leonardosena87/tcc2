# H03/R98 — preparação de QT e recuperação da interface

Prepararam-se cópias independentes da R97 para aplicar as 13 reações de manutenção do telhado A1/A2. **Nenhuma nova carga QT ficou confirmada como gravada. Não houve processamento estrutural.** O Eberick indicou falta de resposta durante a interação, sua janela deixou de aparecer e a reabertura automática retornou `accessibility window-opened handler did not become ready`. Solicitou-se a reabertura manual. Não se atribui esse episódio a um defeito DWG/IFC ou à concepção estrutural.

## Arquivos preservados

- CAD: `D:/TCC/outputs/14-H03-R98-CAD-QT-NAO-EXECUTAR/Projeto Eberick/H03_CAD_R49_LAJES_NAO_EXECUTAR.prj`.
- BIM: `D:/TCC/outputs/15-H03-R98-BIM-QT-NAO-EXECUTAR/Projeto Eberick/H03_BIM_R46_IFC_NAO_EXECUTAR.prj`.
- Evidências: `D:/TCC/outputs/Cargas-H03-R98-QT-NAO-EXECUTAR`.

Conferiram-se novamente os 35 arquivos de origem R97: todos permaneceram com os hashes previstos. Os dois PRJ das cópias R98 permaneceram idênticos aos PRJ R97. O INI de cada cópia aponta para o próprio PRJ, conforme a preparação. Um log transitório copiado no ramo BIM deixou de existir na cópia; seu original R97 permanece preservado. Isso não constitui alteração de carga. A primeira listagem de hashes omitiu essa ausência após erro e foi preservada localmente como `R98-hashes-captura-INCOMPLETA.json`; a conferência válida está em `R98-estado-interrompido.json`, com as 35 linhas e a ausência explícita.

Não se editaram a monografia nem os modelos RVT/DWG nesta revisão. A R97 permanece a referência do cadastro QT salvo e relido. R98 é preparação, sem nova entrada estrutural persistida confirmada.

## Observação nativa e roteiro

No nó BIM RC01, X=110 cm e Y=0 cm, conferiu-se a ação **Adicional**, Fz=-1,41955 kN e os demais componentes nulos. A captura real anterior à edição está em `BIM-RC01-G-antes-UI.txt`. A seleção posterior de **Q_TELHADO_MANUTENCAO** exibiu Fz=0; essa observação está transcrita no registro estruturado, sem arquivo bruto de acessibilidade salvo. A edição pretendida era Fz=-1,072500 kN. O controle retornou erro de elemento indisponível; não se confirmou edição, OK do carregamento, OK do nó, salvamento ou releitura de QT.

`conferir_qt.py` confere o hash do plano R65, os 13 pontos, as coordenadas e os registros G históricos dos dois ramos. Recalcula resultante e primeiros momentos e gera um roteiro comum. A resultante analítica é 13,985625 kN descendente; os valores com seis casas totalizam 13,985628 kN, diferença de 0,000003 kN. Esse roteiro conserva o recorte A1/A2; P1/P2 e o caso localizado da cobertura continuam pendentes. Não se altera a sobrecarga existente das lajes, nem se confunde QT com a carga permanente do forro.

O auditor exige ação, coordenadas, unidades kN/kN.m e os seis componentes. Recusa carga zero, sinal trocado, ramo incorreto, unidade não comprovada, campos ausentes, valores não finitos e leituras conflitantes. A tolerância de 0,0000051 kN corresponde à precisão de leitura observada, não à aceitação estrutural. Os campos X/Y seguem a unidade cm conferida no contexto da interface; não se deduz a unidade de comprimento apenas do texto isolado da árvore.

Para a conferência posterior, utiliza arquivos `CAD|BIM-RCnn-G|QT-apos-reabrir-UI.txt`: 13 pontos × duas ações × dois ramos = **52 leituras previstas**. O estado atual é zero leituras pós-reabertura disponíveis e 52 pendentes, não 52 erros. O nome do arquivo e o texto não provam sozinhos a sequência de salvar/fechar/reabrir; essa sequência também precisa de registro operacional e identificação dos arquivos nativos. Nenhum CSV alimenta o Eberick automaticamente.

## Tempos e correção do inventário

O intervalo interrompido BIM foi de 16:30:37,340 UTC a 18:27:41,789 UTC em 31/10/2026. O relógio monotônico registrou **7.024.446,3451 ms**; a diferença dos horários UTC é **7.024.449 ms**. Ambos são preservados; a pequena diferença de relógios não é corrigida silenciosamente. O intervalo inclui navegação, recuperação da interface, raciocínio, trabalho intercalado e lacunas entre mensagens. Exclui a preparação das cópias e a abertura inicial do projeto. Não representa tempo ativo, inferência da IA, etapa concluída ou tempo total BIM. Não se estima nem subtrai a duração das lacunas.

Corrigiu-se o leitor de tempos `h03-r86/inventariar-tempos.mjs` para reconhecer `wallMs`, usado nas R97/R98, e a indicação de interrupção em inglês, lacuna declarada ou espera humana explícita. Mantêm-se os valores brutos e todos os demais campos de duração, sem promover qualquer registro a ranking final. Os registros históricos não foram sobrescritos.

Gerou-se um novo inventário local em `inventario-tempos-conferido/R86-inventario-tempos.json`; o nome/revisão R86 identifica o formato da ferramenta histórica. `R98-resumo-inventario-conferido.json` registra seu hash, data e limites. A primeira geração em `inventario-tempos-atualizado` foi mantida como preliminar, anterior ao reconhecimento da marca `includesHumanWait` da R97. Foram lidos 150 arquivos candidatos: 112 intervalos com duração, 26 registros sem duração principal e 12 contêineres não expandidos. Identificaram-se 11 pares de intervalos sobrepostos; não se somaram esses intervalos. Quatro demonstrações da palestra e três sessões do banco central permanecem separadas. O levantamento não representa todo o esforço da pesquisa. Os totais CAD/BIM continuam ausentes, sem vencedor.

## Validação e continuidade

Executaram-se sete controles Python, incluindo recusa de unidades, sinal, ação, ambiguidade, componente extra e aprovação por ausência de evidência. Há dados sintéticos nesses controles; não são sete operações no Eberick. Nos arquivos reais, o auditor aceitou G de RC01 e recusou essa mesma leitura como evidência QT. O roteiro real reproduziu as resultantes e manteve todas as leituras posteriores pendentes. Onze testes Node de procedência de material e inventário de tempos passaram. Não houve chamada adicional à API da IA por esses scripts nem validação ELU/ELS.

Reprodução a partir do repositório, com Python 3.12:

```text
python -m unittest discover -s tcc-assistente/estudos/h03-r98 -p test_*.py -v
python tcc-assistente/estudos/h03-r98/conferir_qt.py --out <nova-pasta> --reads D:/TCC/outputs/Cargas-H03-R98-QT-NAO-EXECUTAR
```

O gerador recusa pasta de saída existente. `registrar_interrupcao.py --root <pasta-de-evidências>` registra a ocorrência específica desta revisão e recusa sobrescrita; suas observações operacionais não são inferidas dos binários e não servem de roteiro genérico para futuras ocorrências.

Após recuperar o Eberick, abrir a cópia BIM R98 e conferir se há diálogo de recuperação, sem assumir salvamento. Aplicar QT aos nós existentes e validar cada coordenada/ação; confirmar carga e nó, salvar, fechar, reabrir e reler QT e G. Repetir no CAD com o mesmo plano e critério. Depois fechar demais cargas, materiais, vínculos, vento, ELU/ELS e o ensaio pareado final. Mantém-se o estudo de superestrutura com apoios idealizados, sem dimensionamento de fundações reais.

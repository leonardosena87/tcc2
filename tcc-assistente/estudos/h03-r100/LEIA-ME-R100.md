# H03/R100 — consulta comparativa de materiais no Eberick

Consultaram-se as cópias R98 CAD e BIM no Eberick 2025 Infinity, sem editar propriedades. O projeto inteiro e os três pavimentos foram lidos individualmente, seguidos da classe C25 e da tabela de armadura. Todas as consultas foram canceladas e os projetos foram fechados sem salvar. Os hashes PRJ mantiveram-se iguais ao encerramento da R99.

O consolidado encontrou **151 comparações de campos coincidentes**: 34 controles em quatro vistas de materiais (geral, N2, N1 e N0) e 15 controles da classe C25. A contagem se refere a campos comparados, não a elementos, defeitos ou verificações normativas. A seleção individual dos pavimentos foi observada na interface; a árvore não registra de forma suficiente todas as marcas visuais da seleção.

## Cadastro observado nos dois ramos

| Dado | Valor exibido |
|---|---:|
| Classe de agressividade | II (moderada) |
| Dimensão do agregado | 25 mm |
| Concreto de vigas, pilares e lajes | C25 |
| Cobrimento externo/interno de vigas e pilares | 3,0 cm |
| Cobrimento das lajes fora do contato com o solo | 2,5 cm |
| fck / coeficiente γc / fcd | 25 MPa / 1,4 / 17,86 MPa |
| Peso específico | 25 kN/m³ |
| Abatimento da classe C25 | 10 cm |
| Agregado selecionado | granito |
| Eci / Ecs derivados do fck | 28.000 / 24.150 MPa |
| fctm / fctk,inf / fctk,sup / fctd exibidos | 2,56 / 1,8 / 3,33 / 1,28 MPa |
| Cimento, campo de tipo | CP-II |
| Limites de fissura: solo / água / demais peças | 0,2 / 0,1 / 0,3 mm |
| Combinações para o controle de fissuração | Frequentes |

A coincidência de Eci/Ecs com a base R97 é compatível com a hipótese de granito, mas não confirma o agregado do fornecedor. A tração inferior aparece arredondada a 1,8 MPa na interface; não se substitui silenciosamente o valor original informado pelo usuário. O programa exibe somente CP-II nesse campo; não se comprovou o subtipo CP II-E. O abatimento de 10 cm da classe C25 não demonstra parametrização separada de 6 cm para escadas. Fundações reais permanecem fora do escopo.

A tabela Armadura foi examinada visualmente em duas posições de rolagem. Nos trechos observados, as bitolas ativas 6,3; 8; 10; 12,5; 16; 20; 25; 32 e 40 mm aparecem como CA50 nos dois ramos. As linhas CA60 observadas aparecem desativadas. O texto de acessibilidade não expõe o conteúdo completo dessa grade: as imagens preservadas complementam a transcrição visual. O script não conta essas linhas nem comprova armadura efetiva de cada peça.

## Preservação e limites

CAD PRJ: `e2dc1d91fda030a981e8562d7c3d46318b8e6c262f9c4300415d4078027ca122`. BIM PRJ: `41735ed0fdd0e2c0424dd84ef0b272418947b5c8bdb0cd1abcfa62c852917ccf`. Ambos foram conferidos após fechar. As árvores nativas, imagens disponíveis, relatório e tempos estão nesta pasta. Não se alterou a monografia, RVT, DWG ou entrada estrutural nesta consulta.

O cadastro de solo mostra 4,5 cm para pilares/fundações e 3 cm para vigas/lajes; isso foi registrado, sem aplicar a estudo de fundações ou promover a aprovação da hipótese inicial de 5 cm para contato direto com o solo. Preserva-se essa diferença para revisão se o escopo voltar a incluí-lo. Não se usa o aviso do programa de que os dados estão definidos corretamente como validação normativa independente.

As configurações consultadas não comprovam todas as atribuições por elemento, exceções locais, armaduras, estribos, ancoragens, fluência, retração ou verificações ELU/ELS. Também não demonstram transferência causal pelo IFC: a R96 continua o controle específico desse caminho. A frente de materiais permanece parcialmente concluída.

## Tempos e reprodução

O intervalo CAD registrado foi 395.153,6377 ms (6 min 35,154 s). O BIM foi 6.251.155,9748 ms (1 h 44 min 11,156 s), atravessando uma lacuna de conversa e retomada. Incluem navegação, conferência e trabalho intercalado; excluem abertura inicial e consolidação posterior. Não se mediu esforço ativo ou inferência isolada, nem se calcula vantagem entre esses intervalos.

`consolidar_materiais.py` extrai controles editáveis por identificador estável, exige ausência de conflito, confere os cadastros gerais e por pavimento e os hashes dos PRJ. Recusa relatório de saída existente. A execução nos dados reais confirmou 151 comparações; três controles automatizados com dados sintéticos passaram. Esses controles não constituem verificações de engenharia ou chamadas reais à IA.

```text
python -m unittest discover -s tcc-assistente/estudos/h03-r100 -p test_*.py -v
python tcc-assistente/estudos/h03-r100/consolidar_materiais.py --root <copia-da-pasta-sem-relatorio-de-saida>
```

Para reproduzir, mantêm-se as cópias PRJ nos destinos identificados, ou adapta-se explicitamente o local da conferência; sua ausência não é tratada como preservação confirmada. Próxima frente: conferir exceções de materiais e modelo analítico, completar cargas e compatibilidade de P1/P2, reservatório, paredes, escada e vento antes do processamento final e do ensaio pareado.

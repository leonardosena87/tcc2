# H03/R125 — convenção observada de unidade da carga linear

Na cópia39 BIM/R122, alternou-se temporariamente somente o seletor de **cargas distribuídas lineares**, de kN/m para kgf/m. Nenhuma carga foi editada. O primeiro trecho V1/N1, seção20×45cm e elevação0, exibiu444kgf/m. Reposta e aplicada a unidade original kN/m, a mesma peça exibiu4,44kN/m. Cancelaram-se os diálogos da viga e fechou-se o projeto sem salvar.

A relação entre os valores exibidos corresponde a100kgf por kN nessa leitura. A exportação R122, −4,44kgf/cm, corresponde em magnitude aos444kgf/m nativos. Isso esclarece a convenção observada entre interface e exportação, sem afirmar conversão metrológica exata, calibração universal ou conhecimento da precisão interna de armazenamento. Não se modificou a intensidade para compensar a diferença em relação à conversão SI convencional.

Conferiram-se13 seletores de unidade antes e na configuração de restauração; apenas o seletor102 mudou temporariamente. O retorno efetivo a kN/m foi confirmado pela releitura da viga. Os35 arquivos de origem R121 e os dois PRJs das cópiasR122 mantiveram os hashes da preparação R122. Essa verificação não abrange imutabilidade de todos os auxiliares globais do aplicativo.

A seleção do trecho usa pavimento, posição na imagem e seção; o nomeV1 é repetido no BIM e não identifica sozinho a peça. As imagens e textos preservam a evidência. A carga W03 continua experimental: a exportação anterior ocupa4,40m e a faixa livre mede4,20m. A consulta de unidades não resolve essa diferença geométrica nem aprova o lançamento.

O registro temporal cobre somente o segmento retomado com alternância/releitura/restauração, não a consulta preliminar e interrupção ocorrida na ajuda do navegador. Não se somou espera sem medição nem se classificou produtividade. Sem processamento, alterações de geometria/cargas ou edição da monografia.

Saída: `D:\TCC\outputs\Unidades-H03-R125-CONSULTA-NAO-EXECUTAR`. Próximo: testar a delimitação por nós em cópias independentes, conferindo ferramenta de captura e posição antes de lançar outras faixas.

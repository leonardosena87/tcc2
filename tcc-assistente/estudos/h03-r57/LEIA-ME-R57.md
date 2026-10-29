# H03/R57 — verificacao nativa do lancamento

Revisao de 29/10/2026 em copias independentes dos estados R56 congelados. Nao executar: modelo academico com cargas parciais, sem dimensionamento. A monografia, RVT e DWG de origem nao foram alterados.

Executou-se Lancamento > Outros > Verificar lancamento no N2, N1 e N0 de cada ramo. As seis consultas retornaram "Nao foram detectados problemas no lancamento deste pavimento". Cada consulta possui TXT de acessibilidade com identificacao do croqui e mensagem do programa. O retorno se limita ao conjunto de verificacoes desse comando; nao constitui comprovacao de ligacoes analiticas, resistencia, estabilidade, deformacoes, cargas completas ou atendimento integral a normas.

Na abertura CAD R57 apareceu aviso de possivel inconsistencia na ultima edicao. Executou-se Verificar projeto danificado na copia de estudo, cujo calculo ainda nao havia sido processado nesta H03. Depois verificaram-se os tres croquis e salvou-se. Na reabertura do CAD, o aviso nao voltou a aparecer. O BIM abriu sem esse aviso. Nao foi determinada a causa; nao contar como defeito comprovado de transferencia DWG/IFC. O intervalo CAD inclui essa ocorrencia e a localizacao do comando (a primeira selecao de barras foi cancelada sem executar, ampliou-se a janela para acessar o comando correto). A verificacao de integridade e uma operacao nativa de consistencia, nao um processamento estrutural bem-sucedido.

Exportou-se IFC4 de ambos apos as consultas; o CAD foi reaberto antes da exportacao. A comparacao com a propria R56 manteve 76 objetos por ramo: 22 IfcColumn, 32 IfcBeam, 11 IfcSlab e 11 IfcFooting. Nos 65 objetos da superestrutura preservaram-se nomes, GUIDs, caixas envolventes arredondadas a seis casas decimais em metros, areas superiores arredondadas a seis casas e todas as propriedades exportadas retornadas por get_psets, excluindo apenas o identificador interno numerico "id". Os 11 IfcFooting de cada ramo receberam novos GUIDs. Cada auxiliar foi associado de forma unica por nome e caixa; todos os demais campos extraidos permaneceram iguais. As correspondencias e os GUIDs antigos/novos estao nos JSONs R57-identidade-auxiliares. Trata-se de variacao de identidade observada entre exportacoes; a causa nao foi determinada e nao se comprovou perda geometrica ou erro de transferencia. As cargas Q/G2 parciais das lajes permanecem identicas. Nao se comparou malha integral, nem se certificou que todo parametro nativo e exportado. Os auxiliares continuam excluidos dos quantitativos da superestrutura e nao representam fundacoes executivas. Integridade ZIP dos dois PRJs aprovada; preservados os 45 hashes R56. Estados nativos R57 congelados em separado.

## Tempos prospectivos da consulta assistida

| Ramo | Abrir, consultar N2/N1/N0 e salvar |
|---|---:|
| CAD | 5 min 22.321 s |
| BIM | 3 min 43.229 s |

Incluem raciocinio/latencia; CAD inclui verificacao de integridade, consulta de suporte e descoberta do comando; BIM usa procedimento conhecido e janela ja ampliada. Nao e repeticao controlada e nao mede tempo humano ativo ou inferencia de IA isolada. Nao gerar ranking dos fluxos completos. A reabertura adicional CAD e as exportacoes posteriores nao pertencem a esses intervalos; nao foram cronometradas como etapas completas. O auditor tem duracao propria de execucao, sem preparacao/revisao.

## Pendencias

Nenhuma carga nova foi aplicada. Permanecem a matriz bruta de paredesR56 (W08/base da escada desconhecida), as acoes do telhado/camadas, reservatorio1000L/apoio, escada, bordas/guarda-corpo, vento/combinacoes, confirmacao de apoios/ligacoes analiticas e sensibilidade da barra auxiliar. As vigas de cobertura20x30 sao apenas alternativa geometrica sem ELU/ELS. Faltam processamento, estabilidade e deformacoes; depois selecionar concepcao e atualizar arquivos de origem e textos manuais CAD. Usar novas copias a partir da R57 para completar acoes e diagnosticar.

Referencias operacionais oficiais: [verificacao por pavimento](https://suporte.altoqi.com.br/hc/pt-br/articles/115004249733) e [verificacao/recuperacao de arquivo](https://suporte.altoqi.com.br/hc/pt-br/articles/115002084993). Nenhum envio de relatorio para terceiros foi realizado.

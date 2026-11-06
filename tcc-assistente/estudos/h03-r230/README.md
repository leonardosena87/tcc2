# H03/R230–R231 — recomposição geométrica na recepção BIM

Em 6 de novembro de 2026, executou-se uma sequência de dois ensaios para corrigir as ocorrências geométricas identificadas na recepção R229. A referência nominal corresponde à releitura do Revit R225. O processamento intermediário empregou IfcOpenShell 0.9.0.post1 para produzir cópias IFC4 derivadas. A conversão foi executada no AltoQi Eberick 2025 Infinity, em novos projetos, com a configuração do último projeto CAD R227 e a opção de importar pilares e vigas.

| Verificação | R230 | R231 |
|---|---:|---:|
| Corpos de viga recompostos nesta etapa | 13 | 0 |
| Corpos de pilar recompostos nesta etapa | 2 superiores | 3 inferiores |
| Origens de viga registradas no relatório | 32/32 | 32/32 |
| Origens de pilar registradas no relatório | 23/23 | 23/23 |
| Trechos de viga no IFC de controle | 35 | 35 |
| Segmentos de pilar no IFC de controle | 33 | 35 |
| Origens com parte geometricamente associada | 53/55 | 55/55 |
| Origens com intervalo nominal sem cobertura na verificação | 5 pilares | 0 |
| Tempo assistido da confirmação do IFC ao salvamento | 2 min 12,5 s | 2 min 33,1 s |
| Tempo interno do script de preparação | 2,25 s | 2,36 s |

Na R230, recompôs-se o prisma das 13 vigas que apresentaram seções divergentes e dos trechos superiores P5-N2 e P11-N2. A auditoria confirmou as seções e os topos nominais nas 32 vigas de origem, representadas por 35 trechos no receptor. A recomposição apenas dos trechos superiores dos pilares ainda produziu a ausência geométrica observada na R229. A avaliação dos eixos nominais completos também identificou recortes de 14 cm no topo dos trechos inferiores P5-N1, P11-N1 e P12-N1.

Na R231, recompôs-se o corpo desses três trechos inferiores até +3,20 m. A nova recepção apresentou partes correspondentes às 55 peças de origem. A união dos intervalos verticais cobriu os 23 trechos de pilar. Nas vigas, comparou-se eixo, largura, altura, topo e extensão entre os apoios de extremidade. Os intervalos ocupados pelos pilares foram considerados na cobertura da projeção, incluindo o eixo da V2-N2. A tolerância de comparação de seção e cota é de até 0,2 mm. Esses critérios são computacionais.

O controle R231 contém 70 sólidos, associados individualmente a uma única origem. Os 12 segmentos adicionais de pilar decorrem da divisão no nível do patamar. O projeto foi salvo, fechado, reaberto e novamente exportado. A comparação preservou GUIDs, nomes, conjuntos de propriedades e caixas geométricas dos 70 sólidos.

Os quantitativos associados aos corpos recortados foram removidos dos 18 elementos recompostos. Os campos antigos de volume e comprimento de corte também foram retirados dessas ocorrências. Os quantitativos nominais futuros dependem da geometria efetivamente aceita no receptor. A conferência preservou identidades, propriedades remanescentes, materiais, tipos e quatro níveis. As cópias derivadas apresentaram zero ocorrência na validação do esquema IFC, antes e depois da transformação.

A preparação substituiu os corpos recortados por prismas conforme os eixos e as dimensões da autoria. O resultado deve ser identificado na metodologia como tratamento adicional do IFC, com 18 ocorrências geométricas tratadas em duas etapas. Essa operação representa esforço de correção da rota BIM. Uma contagem de sólidos pode mudar após a conversão mesmo quando todas as origens possuem correspondência geométrica.

Os tempos de recepção incluem navegação assistida, espera entre comandos, planificação, conversão e salvamento. O cronômetro começa na confirmação do seletor do IFC e termina na observação após o comando de salvar. A duração de preparação automática fica fora desse intervalo. A elaboração do código, diagnóstico, auditoria, reabertura e complementação possuem escopos próprios. Os dois ensaios são sequenciais, realizados com entradas diferentes, sem equivalência a repetições de um fluxo completo.

O próximo marco comum da comparação exige lançar os elementos a partir dos DWGs na cópia CAD, complementar lajes e escada na recepção BIM e conferir as ações e ligações antes do recálculo. A R231 corresponde a uma recepção de vigas e pilares. Os modelos calculados da R227 contêm as complementações anteriores e os avisos de verificação já documentados.

A API empregada permite criar geometrias e alterar suas representações. A conferência independente das dimensões e das posições é necessária para verificar o resultado da transformação. [Documentação de geometria do IfcOpenShell](https://docs.ifcopenshell.org/ifcopenshell-python/geometry_creation.html)

Os programas desta pasta operam sobre os dados locais em D:/TCC. Executar `preparar_geometria.py` para gerar a R230 e `preparar_continuidade.py` para gerar a R231. Ambos recusam sobrescrever um IFC existente. A auditoria do estado salvo usa `conferir_receptor.py --revision R231`. A opção padrão audita a R230. A conectividade analítica, a completude das cargas, as armaduras e a aprovação estrutural permanecem pendentes nesta nova recepção.

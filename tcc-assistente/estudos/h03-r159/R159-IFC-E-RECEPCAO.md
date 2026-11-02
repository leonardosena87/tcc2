# H03/R159 — exportação e recepção bruta conferidas em 02/11/2026

Esta etapa sucedeu a aplicação/reabertura nativa R159. Não substitui o histórico `R159-resultado-nativo.json`, que corretamente registrava exportação e recepção ainda pendentes naquele instante. A monografia não foi alterada.

## Exportação Revit

Exportou-se `H03-R159-Revit-VIGA-PATAMAR-NAO-EXECUTAR.ifc`, na pasta desta revisão em `D:/TCC/outputs/Escada-H03-R159-IMPLANTACAO-NAO-EXECUTAR`. Utilizou-se IFC2X3 Coordination View, IFCVersion=10, ExchangeRequirement=3, propriedades de materiais habilitadas e todo o modelo. Não se limitou à vista com caixa de corte, não se dividiram pilares por nível nem se gravaram GUIDs no RVT. A configuração foi importada e salva novamente pelo diálogo nativo. O JSON relido coincide com o preparado em todos os campos funcionais; o nome salvo passou a derivar do nome do arquivo. O cabeçalho do IFC declara CoordinationView.

A auditoria associou por Tag as 65 identidades nativas: 24 segmentos de pilares, 30 vigas e 11 lajes da edificação, sem falta nesse conjunto. Há uma 12ª IfcSlab, corretamente identificada como LANDING e agregada à escada. Não foi tratada como duplicação de uma das onze lajes. A escada contém dois lances, 9+8 espelhos, e dois corrimãos. As malhas puderam ser lidas; isso não demonstra equivalência integral com o sólido nativo, fechamento ou qualidade de vínculo resistente.

Os 65 elementos possuem associação a material nomeado, mas a saída tem **zero entidades IfcMaterialProperties**. Portanto, não se confirmou transferência de fck, Young, densidade ou Poisson por essa via. A ausência nesta exportação contrasta com o ensaio R94 de mesma configuração funcional, no qual essas propriedades apareceram. A causa ainda não foi isolada; não se atribuiu automaticamente a ausência à edição do modelo, à configuração ou ao programa receptor. O cadastro nativo de 25 MPa, já conferido na R159, não equivale à sua retenção neste IFC. A R159 não releu independentemente os nomes, Young, densidade e Poisson nativos, por isso não se declarou igualdade desses campos atuais com a R93.

Também se encontrou inconsistência interna nos dois IfcStairFlight: os atributos RiserHeight/TreadLength contêm aproximadamente 0,584761/0,918635 em um projeto cuja unidade de comprimento é milímetro. Ao aplicar essa unidade, os valores divergem da leitura Revit. O Pset_StairFlightCommon contém 178,235294/280 mm e coincide com o espelho de 17,823529 cm e a pisada de 28 cm. A quantidade de espelhos/pisadas está correta. Não se alterou o arquivo para esconder a divergência, nem se inferiu que ela mudou a malha ou o comportamento do Eberick. A declaração de IfcStairFlight foi consultada no esquema IFC2X3 distribuído com IfcOpenShell; a [referência oficial buildingSMART](https://standards.buildingsmart.org/IFC/RELEASE/IFC2x3/FINAL/HTML/ifcsharedbldgelements/lexical/ifcstairflight.htm) foi localizada, mas o acesso direto retornou HTTP 403 nesta sessão.

## Receptor bruto Eberick

Criou-se um receptor independente, com Configuração inicial do programa, a partir do IFC bruto e com “Importar pilares e vigas” marcado. Mantiveram-se os nove níveis do assistente, inclusive referências de acabamento e níveis vazios. Preservou-se solo=0 e altura inicial de 100 cm como estado do assistente, sem interpretar isso como fundação real ou apoio validado. O nome inicialmente pretendido foi anexado ao preenchimento anterior pela interface e truncado; o caminho real é registrado abaixo, sem confundir com o nome pretendido.

Projeto real: `D:/TCC/outputs/H03-R159-Revit-VIGA-PATAMAR-NAO-EXECUTARH03_R159_IFC_BRUTO_NAO_E/Projeto Eberick/H03-R159-Revit-VIGA-PATAMAR-NAO-EXECUTARH03_R159_IFC_BRUTO_NAO_E.prj`.

O relatório nativo `Relatorio_de_importacao_de_elementos_IFC.docx` lista **54 origens**, conciliadas com IDs Revit: 30 vigas e 24 trechos de pilares, incluindo V16-ESC-PAT/473802. Não há origem esperada ausente, repetida ou desconhecida nesse relatório. O Eberick apresentou aviso de importação com seção retangular e necessidade de conferir o lançamento. O estado salvo foi congelado em onze arquivos antes de qualquer correção.

A saída de controle foi gerada como IFC4, edificação completa, PropertySets habilitados, sem quantitativos, agrupamento de trechos ou armaduras 3D. Ela contém **72 sólidos IfcColumn e 33 IfcBeam, zero IfcSlab e zero IfcStair/IfcStairFlight**. A quantidade de sólidos não pode ser comparada diretamente com 24/30 origens, pois há segmentação. A presença da escada na vista 3D com referência externa não prova conversão em elemento calculável.

A conciliação espacial nominal identificou as 30 origens de vigas em 31 das 33 partes. Duas partes adicionais de V6/V7 do receptor excedem os limites axiais do critério utilizado e permaneceram sem associação, em vez de receberem correspondência forçada. Empregou-se tolerância XY de 0,1 mm para acomodar o arredondamento observado de cerca de 0,0167 mm. Doze partes associadas apresentam diferenças de topo e altura em relação aos dados nativos; cada ocorrência está individualizada no JSON. Não se concluiu cobertura axial completa nem conectividade, e os 72 segmentos de pilares ainda exigem conciliação física por posição, seção e intervalo vertical. A viga do patamar tem parte associada com largura/altura de 20/30 cm e topo próximo de +1,774118 m nesse controle, sem provar vínculo, continuidade, armadura ou capacidade.

O IFC4 apresenta identificação C-25 e campos de armadura “Não calculado”. A identificação C-25 pode corresponder à configuração inicial; não prova que fck tenha sido importado do IFC de origem. Os projetos principais CAD/BIM anteriores não foram modificados por este ensaio. O PRJ experimental ainda coincide por hash com o estado salvo antes das consultas/exportação de controle.

## Medições desta etapa

| Recorte observado | Duração | Alcance |
|---|---:|---|
| Preparação do diálogo IFC até observação após exportação | 7 min 21,232 s | Navegação, configuração, releitura, exportação e deliberação |
| Clique em Exportar até observação posterior | 21,435 s | Subintervalo contido no anterior; não somar novamente; não é CPU |
| Criação do receptor bruto até Ctrl+S/observação | 3 min 6,184 s | Assistente, planificação, avisos, conferências e deliberação |

Os tempos são prospectivos de sessão, com escopos explícitos. Não representam tempo total CAD/BIM, esforço isolado de inferência ou ensaio pareado; não sustentam ranking. A auditoria posterior, exportação de controle e congelamento são recortes distintos e não foram embutidos retroativamente na recepção. O registro de clique/observação da exportação de controle inclui deliberação e leitura posteriores; tampouco equivale ao tempo de processamento.

## Evidências e continuidade

`R159-IFC-auditoria.json` e `R159-Eberick-recepcao-auditoria.json` mantêm fontes, hashes, unidades, geometrias e limites. `R159-receptor-bruto-congelamento.json` identifica os onze arquivos preservados. O IFC bruto e o RVT permaneceram inalterados durante as leituras. `auditar_ifc.py` e `auditar_receptor_bruto.py` reproduzem as auditorias somente leitura. Oito testes sintéticos verificam a detecção de unidade inconsistente, duplicação, classe divergente, patamar adicional, escolha do pavimento, alteração de seção/eixo e extensão não explicada. Esses testes não substituem a observação nativa nem executam dimensionamento estrutural.

A próxima etapa é preparar cópias de correção comparáveis às plantas CAD R159, tratar referências de níveis sem perder a geometria, conferir a conversão nominal de todas as vigas/pilares e lançar as lajes e a escada resistentes. Devem-se contar separadamente ocorrências, operações e tempo de complementação. Prosseguem pendentes apoio inferior, continuidade do patamar, materiais completos, cargas/combinações e análise ELU/ELS. **Não executar em obra.**

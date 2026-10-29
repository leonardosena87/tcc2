"""Triagem de espaco e parcelas de carga do tanque1000L, sem lancamento."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,ast,math
root=Path('D:/TCC');out=root/'outputs/Reservatorio-H03-R71-ALTERNATIVAS-NAO-APLICADO'
dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r71')
assert not out.exists() and not dest.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(root/'outputs/Compatibilizacao-H03-R70-W08-J4-ESTUDO/R70-manifesto.json')['files']
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
roofpath=root/'outputs/Cobertura-H03-R60-REACOES-PARCIAIS-NAO-EXECUTAR/R60-arranjo-reacoes.json';roof=read(roofpath)
p2=next(p for p in roof['planes'] if p['id']=='P2');assert p2['box']==[6.55,0,9.65,3.9]
wallHalf=.075;clear=[6.55+wallHalf,wallHalf,9.65-wallHalf,3.9-wallHalf];cx=(clear[0]+clear[2])/2;cy=(clear[1]+clear[3])/2
models=[dict(id='ref-circular',manufacturer='Fortlev',capacityL=1000,heightWithLidM=.97,topXDimensionM=1.52,topYDimensionM=1.52,baseDimensionsM=[1.16,1.16],baseShape='circular',url='https://www.fortlev.com.br/produtos/reservatorios/caixa-dagua-de-polietileno-1000l/'),dict(id='ref-retangular-baixa',manufacturer='Bakof Tec',capacityL=1000,heightWithLidM=.68,topXDimensionM=1.23,topYDimensionM=1.88,baseDimensionsM=[.88,1.53],baseShape='retangular',url='https://www.bakof.com.br/produtos/4')]
margin=.60;architectGrossHeight=1.30
for m in models:
    m.update(referenceOnlyNotSelected=True,dimensionsApproximate=True,tareKN=None,referenceCenterM=[cx,cy],candidatePlanEnvelopeM=[cx-m['topXDimensionM']/2,cy-m['topYDimensionM']/2,cx+m['topXDimensionM']/2,cy+m['topYDimensionM']/2],studySideClearancesM=[(clear[2]-clear[0]-m['topXDimensionM'])/2,(clear[3]-clear[1]-m['topYDimensionM'])/2],studyVerticalServiceReserveM=margin,nominalGrossRemainingHeightM=architectGrossHeight-m['heightWithLidM'],heightPlusStudyServiceReserveM=m['heightWithLidM']+margin,roofSlopeProfileAndMemberDepthIncluded=False,verticalInstallationApproved=False)
    m['studyLateralClearanceCheck']=min(m['studySideClearancesM'])>=margin
    m['grossVerticalReserveFitsNominal130']=m['heightPlusStudyServiceReserveM']<=architectGrossHeight
assert all(m['studyLateralClearanceCheck'] for m in models)
volume=1000/1000;physicalWater=volume*1000*9.80665/1000;nominalWater=10.0
baseArea=1.35*2.0;baseOptions=[]
for t in (.08,.10,.12):
    g=baseArea*t*25
    baseOptions.append(dict(thicknessHypothesisM=t,areaM2=baseArea,concreteUnitWeightKNm3=25,baseSelfWeightKN=g,fullWaterPlusBaseKN=nominalWater+g,totalIncludingTareAndPedestalKN=None,waterPlusBaseEquivalentKNm2=(nominalWater+g)/baseArea,dimensionsArePreliminaryNotDesigned=True,nativeApplied=False))
out.mkdir()
def write(n,v):(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write('R71-protegidos-R70.json',protected)
result=dict(revision='H03/R71',atUtc=datetime.now(timezone.utc).isoformat(),status='Duas referencias dimensionais e tres bases de estudo; nao selecionadas ou aplicadas',sourceRoofMap=dict(path=str(roofpath),sha256=sha(roofpath)),planRegionP2=p2,clearPlanHypothesisM=clear,clearPlanHypothesisSource='Eixos P2 R60 menos metade de parede acabada15cm; nao detalhe executivo ou nova medicao',candidateCenterM=[cx,cy],candidateCenterSelectedForStudyOnly=True,models=models,visualSectionReadings=dict(reservoirCapacityL=1000,localRaisedBaseDifferenceM=.60,localGrossHeightDimensionM=architectGrossHeight,localRoofSloped=True,absoluteStructuralBaseElevationM=None,dimension130IsClearServiceEnvelope=False),water=dict(volumeM3=volume,referenceDensityHypothesisKgM3=1000,standardGravityMS2=9.80665,physicalReferenceWeightKN=physicalWater,nominalStudyWeightKN=nominalWater,nominalStudyIsNormativeCitation=False,nominalRoundingPercent=(nominalWater/physicalWater-1)*100,notNativeTfConversion=True),baseAlternatives=baseOptions,candidateBasePlanM=[cx-1.35/2,cy-2.0/2,cx+1.35/2,cy+2.0/2],fullAssemblyWeightKN=None,pedestalWeightKN=None,tareConfirmed=False,loadActionClassificationFinalized=False,nativeLoadsApplied=False,supportLoadPathDesigned=False,architecturalHeightsChanged=False,modelSelected=False,eluElsApproved=False,operationalSources=[dict(url='https://www.fortlev.com.br/wp-content/uploads/2020/01/Manual_tecnico_fortlev_caixa_dagua_2020-06.pdf',consulted='Base continua/rígida/nivelada e espaco lateral; nao se transferiu prescricao de uma marca a outra'),dict(url='https://bakof.com.br//storage/produtos/4/arquivos/151d4279da2695905e75d4466da41001.pdf',consulted='Apoio integral, plano, rigido e nivelado; nao dimensiona a estrutura de apoio')])
write('R71-reservatorio-alternativas.json',result)
table='\n'.join(f'| {m["manufacturer"]} | {m["topXDimensionM"]:.2f} × {m["topYDimensionM"]:.2f} | {m["heightWithLidM"]:.2f} | {m["nominalGrossRemainingHeightM"]:.2f} |' for m in models)
loads='\n'.join(f'| {b["thicknessHypothesisM"]*100:.0f} | {b["baseSelfWeightKN"]:.2f} | {b["fullWaterPlusBaseKN"]:.2f} | {b["waterPlusBaseEquivalentKNm2"]:.4f} |' for b in baseOptions)
(out/'LEIA-ME-R71.md').write_text(f'''# H03/R71 — reservatório de1.000L, espaço e cargas de estudo

ALTERNATIVAS NÃO APLICADAS. NÃO EXECUTAR. Mantém-se a capacidade autorizada de1.000L. Não se selecionou marca para compra nem se dimensionou base/apoio. A posição em planta apresentada é candidata de estudo e não localização definitiva. Os arquivos nativos e a monografia não foram alterados.

## Compatibilização dimensional

Na página atual do produto, a referência circular Fortlev informa diâmetro com tampa1,52m, altura0,97m e fundo de diâmetro1,16m. São dimensões aproximadas. [Produto oficial](https://www.fortlev.com.br/produtos/reservatorios/caixa-dagua-de-polietileno-1000l/).

A referência retangular Bakof Tec de1.000L informa comprimento superior1,88m, largura superior1,23m, comprimento inferior1,53m, largura inferior0,88m e altura0,68m. São referências para verificar espaço, sem assumir que o desenho arquitetônico representa esse modelo. [Produto oficial](https://www.bakof.com.br/produtos/4).

| Referência | Dimensões superiores X×Y no estudo (m) | Altura (m) | Sobra aritmética dentro de1,30m bruto (m) |
|---|---:|---:|---:|
{table}

O corte BB mostra1.000L, ressalto local de0,60m da base e dimensão vertical local de1,30m sob região de telhado inclinado. Não se converteu1,30m em altura livre de manutenção nem em cota estrutural absoluta. A inclinação, espessura da cobertura, perfis, tampa e elevação real da base precisam entrar no confronto. Não se adotou simplesmente N2+0,60m: o vínculo entre cotas arquitetônicas e estruturais ainda precisa de conferência, preservando as alturas conforme decisão do usuário.

Em planta, utilizou-se provisoriamente P2 R60, X6,55..9,65/Y0..3,90m. Retirando metade da parede acabada15cm de cada lado, a área interior hipotética fica2,95×3,75m. O centro de estudo é X{cx:.3f}/Y{cy:.3f}m. Orientando o comprimento maior da referência retangular em Y, ambos os envelopes cabem nessa planta com margem lateral de estudo de0,60m. Essa margem não é levantamento nem prescrição universal. O manual Fortlev consultado pede espaço lateral e apoio integral; o manual Bakof deve ser seguido para seu próprio produto. [Manual Fortlev](https://www.fortlev.com.br/wp-content/uploads/2020/01/Manual_tecnico_fortlev_caixa_dagua_2020-06.pdf), [manual Bakof](https://bakof.com.br//storage/produtos/4/arquivos/151d4279da2695905e75d4466da41001.pdf).

Para testar sensibilidade vertical, reservou-se0,60m ACIMA da tampa como hipótese de estudo, sem atribuir esse número à norma ou aos dois fabricantes. A referência circular exigiria1,57m, superando a dimensão bruta1,30m. A baixa retangular exigiria1,28m, sobrando só2cm antes de considerar o perfil inclinado, as espessuras e as demais folgas. Portanto, nem mesmo essa referência recebeu aprovação de instalação. O modelo mais baixo é candidato para continuar a análise; não se elevou a cobertura para fazê-lo caber.

## Parcelas de carga

1.000L correspondem a1m³. Com densidade de referência hipotética1.000kg/m³ e gravidade convencional9,80665m/s², o peso de referência é{physicalWater:.5f}kN. Para a sensibilidade preliminar adotou-se10,00kN de água, arredondamento superior de{result['water']['nominalRoundingPercent']:.3f}%. O valor10 não foi apresentado como transcrição normativa e não decorre da conversão de exibição kN/tf do Eberick. A tara permanece desconhecida, campo nulo.

Compararam-se três espessuras hipotéticas de plataforma cheia1,35×2,00m, usando25kN/m³ para concreto, coerente com o peso próprio já utilizado no estudo. Não se escolheu nenhuma espessura por resistência/flecha. O apoio sob toda a base do reservatório é requisito de instalação a considerar; a plataforma e os elementos que a sustentam exigem cálculo.

| Espessura hipotética (cm) | Peso da plataforma (kN) | Água+plataforma, sem tara/pedestal (kN) | Média equivalente sobre2,70m² (kN/m²) |
|---|---:|---:|---:|
{loads}

A média equivalente não é pressão local real de contato nem pode ser espalhada em toda a laje para ocultar o efeito concentrado. A reação transmitida pelo fundo, a rigidez da plataforma e o suporte por laje/vigas precisam de verificação. A plataforma em cota elevada também pode exigir pedestal/muretas e respectivas cargas, ainda desconhecidas (null) no cadastro, sem serem tratadas como zero.

Não se lançou carga no N2. A classificação final da água como ação permanente ou variável exige explicitar o regime de operação e as situações cheio/vazio, conforme a base normativa adotada; a capacidade sozinha não determina essa escolha. Tara e plataforma são parcelas próprias e não se confundem com peso das telhas ou sobrecarga de manutenção. A ação Água pré-cadastrada do Eberick não foi aceita automaticamente sem conferir seu grupo/fatores.

## Continuidade

Fechar a altimetria P2 e o envelope sob o telhado, escolher uma referência de estudo compatível, obter tara e detalhes do fundo, e definir a base/apoios preservando a arquitetura. Depois calcular efeitos locais, ELU/ELS, reações e combinar cheio/vazio antes de aplicar a mesma hipótese nos dois ramos. O estudo permanece restrito à superestrutura; não se projetou fundação do reservatório. A ausência do peso total não foi preenchida com um valor inventado.
''',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name);ast.parse(Path(__file__).read_text(encoding='utf-8'))
write('R71-validacao.json',dict(twoManufacturerReferencesConsulted=True,sourceSectionVisuallyRead=True,planBoundsChecksPassed=True,waterVolumeAndBaseWeightArithmeticPassed=True,protectedR70FilesChecked=len(protected),nativeApplied=False,fullAssemblyWeightKnown=False))
write('R71-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file()]))
dest.mkdir()
for p in out.iterdir():shutil.copy2(p,dest/p.name);assert sha(p)==sha(dest/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
guide.write_text('''# Atualizacao R71 — tanque1000L: alternativas, sem selecao/aplicacao

Duas referencias oficiais circular/retangular baixa e tres plataformas hipoteticas comparadas. Centro candidatoP2 X8,10/Y1,95m, nao definitivo. Dimensao bruta1,30m do corte NAO comprova folga livre; cota absoluta elevada nao fixada. Agua nominal de estudo10kN, tara/pedestal desconhecidos; pesos de plataforma8/10/12cm calculados sem dimensionar. Nenhuma carga nativa aplicada. Ler outputs/Reservatorio-H03-R71-ALTERNATIVAS-NAO-APLICADO/LEIA-ME-R71.md. NativosR64, Q_R65 e acoesR66pendentes. ReferenciaP3R68 e fachadaW08R70 devem ser consideradas antes de fechar cargas. Monografia/origens preservadas. NAO EXECUTAR.

---
Historico anterior:

'''+old,encoding='utf-8')
print(json.dumps(dict(status=result['status'],candidateCenter=[cx,cy],nominalWaterKN=10,baseAlternatives=baseOptions),ensure_ascii=False))

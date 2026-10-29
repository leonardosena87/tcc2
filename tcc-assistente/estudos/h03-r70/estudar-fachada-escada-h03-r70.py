"""Enquadra W08/J4 como fachada da caixa da escada; nao cria apoio/carga."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,ast
root=Path('D:/TCC');out=root/'outputs/Compatibilizacao-H03-R70-W08-J4-ESTUDO'
dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r70')
assert not out.exists() and not dest.exists()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(root/'outputs/Resultados-H03-R69-TEMPOS-EXPLORATORIOS/R69-manifesto.json')['files']
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
refp=root/'outputs/Compatibilizacao-H03-R68-PORTA-P3-ESTUDO/R68-referencia-arquitetonica-estudo.json';ref=read(refp)
geop=root/'outputs/Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR/R56-geometria-exportada.json';geo=read(geop)
arch=root/'PROJETO ARQUITETONICO-A0.pdf';assert sha(arch)==ref['sourceSha256']
op=next(o for f in ref['floors'] if f['id']=='T' for o in f['openings'] if o['id']=='T-J4-01')
assert op['tag']=='J4' and abs(op['x2']-op['x']-1.6)<1e-6
base=.22;sill=.20;windowHeight=3.20;bottom=base+sill;top=bottom+windowHeight
assert bottom<3.2<top
def length(a,b,c,d):return max(0,min(b,d)-max(a,c))
def hit(o):return o['min'][1]-1e-6<=0<=o['max'][1]+1e-6 and length(op['x'],op['x2'],o['min'][0],o['max'][0])>1e-6 and length(bottom,top,o['min'][2],o['max'][2])>1e-6
checks={}
for b,rr in geo.items():
    collisions=[o for o in rr if o['type'] in ('IfcBeam','IfcColumn','IfcSlab') and hit(o)]
    n1=[o for o in rr if o['type']=='IfcBeam' and abs(o['max'][2]-3.2)<1e-6 and o['min'][1]<=0<=o['max'][1] and length(4.5,6.45,o['min'][0],o['max'][0])>1e-6]
    checks[b]=dict(windowBoxIntersections=collisions,beamsAtN1UnderW08=n1)
assert all(not c['windowBoxIntersections'] and not c['beamsAtN1UnderW08'] for c in checks.values())
knownClearLength=6.45-4.5;roofSoffit=6.09
grossArea=knownClearLength*(roofSoffit-base);windowArea=1.6*3.2;net=grossArea-windowArea;weight=net*1.565
out.mkdir()
def write(n,v):(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write('R70-protegidos-R69.json',protected)
result=dict(revision='H03/R70',atUtc=datetime.now(timezone.utc).isoformat(),status='W08/J4 identificada como fachada especial; apoio/carga nativa continuam pendentes',sources=[dict(path=str(p),sha256=sha(p)) for p in (arch,refp,geop)],visualReadings=dict(windowSchedule=dict(tag='J4',widthM=1.6,heightM=3.2,sillM=.2),sectionAA=dict(stairGroundFinishedM=.22,landingFinishedM=1.70,upperFinishedM=3.25),visualReadingNotSurvey=True),conditionalWindowVerticalEnvelope=dict(baseFinishedHypothesisM=base,bottomM=bottom,topM=top,crossesStructuralN1Plane=True),windowPlanReference=op,nativeBoundingBoxChecks=checks,conditionalMasonryTakeoff=dict(knownLengthExcludingColumnsM=knownClearLength,baseFinishedHypothesisM=base,roofSoffitM=roofSoffit,grossAreaM2=grossArea,openingAreaM2=windowArea,netMasonryAreaM2=net,areaWeightHypothesisKNm2=1.565,weightKN=weight,includesJoineryLintelsFinishesOnConcrete=False,baseIsAdoptedNativeWallDatum=False,notApprovedLoad=True),w08BaseResolved=False,analyticalSupportDefined=False,nativeLoadValue=None,nativeFilesEdited=False,intersectionsAbsentProveAnalyticalCompatibility=False,foundationDesigned=False,designApproved=False)
write('R70-W08-J4.json',result)
(out/'LEIA-ME-R70.md').write_text(f'''# H03/R70 — fachada W08 e janela J4 da escada

ESTUDO, NÃO EXECUTAR. A leitura visual da tabela de esquadrias da prancha confirma J4 fixa em alumínio,1,60×3,20m, peitoril0,20m. O corte AA indica piso da escada no térreo em+0,22m, patamar em+1,70m e piso superior em+3,25m. A referência T-J4-01 está na fachada Y0, X4,70..6,30m, dentro da faixa W08. A posição em planta continua aproximada; não foi feita medição executiva.

## Por que W08 não recebe automaticamente a altura das demais paredes superiores

Se o peitoril0,20m for referido ao piso interno+0,22m do corte, o vão ocupa Z{bottom:.2f}..{top:.2f}m e atravessa o plano estrutural N1+3,20m. Portanto, a janela não se limita a uma parede iniciada no piso superior. Adotar diretamente a base+3,25m e descontar uma janela de3,20m nessa faixa seria geometricamente incoerente. A base efetiva e o apoio de W08 continuam não resolvidos no modelo; a altura não foi preenchida artificialmente.

Na geometria exportada R56, preservada R57, não há viga N1 cruzando o trecho livre W08 X4,50..6,45/Y0. O teste de caixas também não encontrou viga, pilar ou laje interceptando a caixa condicional do vão J4 em nenhum dos dois ramos. Isso esclarece que o modelo não deve receber uma viga nesse trecho apenas para transformar a parede em um lançamento padrão: uma solução assim precisa preservar J4. Ausência de interseção de caixas não comprova caminho de carga, ligações ou compatibilidade executiva completa.

## Quantificação condicional, sem lançamento

Para compreender a ordem geométrica da fachada, considerou-se somente a faixa livre de pilares1,95m, entre X4,50 e6,45m, da base hipotética+0,22m ao intradorso N2+6,09m. A área bruta seria{grossArea:.4f}m²; o vão J4 representa{windowArea:.4f}m²; a área líquida de alvenaria seria{net:.4f}m². Na composição hipotética1,565kN/m², o peso dessa parcela seria{weight:.6f}kN. O número NÃO foi aplicado ao Eberick e não inclui esquadria, verga/contraverga, encontros ou acabamento sobre concreto.

Essa quantificação não define onde o peso entra na estrutura de concreto. Uma fachada contínua com apoio inferior e uma fachada apoiada em verga/viga intermediária produzem caminhos de carga distintos. Nenhuma dessas soluções foi adotada ou dimensionada. O recorte sem sondagem permanece na superestrutura; não se criou fundação real para resolver a parede. No JSON, nativeLoadValue é nulo, nunca zero.

## Continuidade

Definir o suporte e o detalhamento da fachada preservando J4, patamar e passagem da escada; conferir a referência vertical do peitoril e as faces. Quantificar esquadria/vergas e só então decidir as ações sobre o pórtico e o que permanece fora do recorte. Não transformar o peso condicional acima em carga linear uniforme no N1, onde não existe apoio geométrico neste trecho. Não apagar a parede da lista de pendências por ter calculado uma área.

Os recortes originais de leitura ficaram em work, sem copiar a prancha ao repositório público. Os registros R55/R56/R67 continuam históricos. Nenhum PRJ/RVT/DWG, arquitetura original ou monografia foi editado, e não houve processamento ou aprovação ELU/ELS.
''',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name);ast.parse(Path(__file__).read_text(encoding='utf-8'))
write('R70-validacao.json',dict(windowScheduleAndSectionVisuallyRead=True,bothBranchBoxChecksPassed=True,protectedR69FilesChecked=len(protected),nativeLoadApplied=False,sourceArchitectureHashPassed=True))
write('R70-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file()]))
dest.mkdir()
for p in out.iterdir():shutil.copy2(p,dest/p.name);assert sha(p)==sha(dest/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
guide.write_text('''# Atualizacao R70 — fachada W08/J4 enquadrada, apoio pendente

Tabela J4=1,60x3,20m/peitoril0,20m e corteAA conferidos visualmente. Hipotese de piso+0,22 leva vaoZ0,42..3,62, cruzandoN1. Sem viga N1 sob faixa livreW08 em ambos ramos e sem intersecoes de caixas do vao condicional. Nao preencher W08 como parede superior padrao e nao criar viga que cruzeJ4. Area/peso condicional da fachada calculado sem aplicar carga; apoio/vergas/tara/base continuam pendentes. Ler outputs/Compatibilizacao-H03-R70-W08-J4-ESTUDO/LEIA-ME-R70.md. NativoR64 permanece; Q_R65 e acoesR66 nao aplicados. Sem monografia/origens alteradas. NAO EXECUTAR.

---
Historico anterior:

'''+old,encoding='utf-8')
print(json.dumps(dict(status=result['status'],conditionalNetAreaM2=net,conditionalMasonryWeightKN=weight,windowBoxConflicts=0),ensure_ascii=False))

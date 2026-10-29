"""Congela evidencias BIM R50, preserva predecessores e compara geometrias CAD/BIM."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,hashlib,shutil,sys
sys.path.insert(0,'D:/TCC/work/ifc/deps')
import ifcopenshell,ifcopenshell.validate,ifcopenshell.util.element
root=Path('D:/TCC');out=root/'outputs/Complementacao-H03-R50-LAJES-BIM-NAO-EXECUTAR'
native=root/'outputs/H03_BIM_R50_LAJES_NAO_EXECUTAR'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,r:p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert load(out/'R50-reabertura.json')['sameGeometryNamesGuidsAndTopAreas']
preserved=[]
for manifest in (root/'outputs/Intercambio-H03-R46-BIM-NAO-EXECUTAR/R46-manifesto.json',root/'outputs/Complementacao-H03-R49-LAJES-CAD-NAO-EXECUTAR/R49-manifesto-persistencia.json'):
    for e in load(manifest)['files']:
        p=Path(e['path']);assert sha(p)==e['sha256'],str(p)
        preserved.append(dict(path=str(p),sha256=e['sha256']))
frozen=[]
for folder in ('Projeto Eberick','_DADOS_'):
    for p in (native/folder).rglob('*'):
        if not p.is_file() or p.suffix.lower() in ('.bak','.lck','.tmp'):continue
        dest=out/'congelado-onze-lajes'/p.relative_to(native);dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists():assert sha(dest)==sha(p),str(dest)
        else:shutil.copy2(p,dest)
        frozen.append(dict(path=str(p),frozen=str(dest),sha256=sha(p)))
rules=root/'work/conferir-reabertura-h03-r49.py'
ns={};exec(compile(rules.read_text(encoding='utf-8').split("a=out/'R49-primeira-exportacao.ifc'")[0],str(rules),'exec'),ns)
cad=root/'outputs/Complementacao-H03-R49-LAJES-CAD-NAO-EXECUTAR/R49-apos-reabrir.ifc'
bim=out/'R50-onze-lajes-reaberto.ifc'
rows={name:ns['extract'](path) for name,path in (('CAD',cad),('BIM',bim))}
def signature(r):return (r['type'],*(round(x,5) for k in ('min','max') for x in r[k]),round(r['topAreaM2'],5))
spatial={k:Counter(signature(r) for r in rr) for k,rr in rows.items()}
comparison=dict(cadIfc=str(cad),bimIfc=str(bim),cadSha256=sha(cad),bimSha256=sha(bim),
    counts={name:dict(Counter(r['type'] for r in rr)) for name,rr in rows.items()},
    sameSpatialMultiset=spatial['CAD']==spatial['BIM'],
    cadOnlySignatures=[dict(signature=list(k),count=v) for k,v in (spatial['CAD']-spatial['BIM']).items()],
    bimOnlySignatures=[dict(signature=list(k),count=v) for k,v in (spatial['BIM']-spatial['CAD']).items()],
    tolerance='Assinaturas arredondadas a cinco casas em m e m2; auditorias por origem usam tolerancia absoluta 1e-5.',
    limits=['Compara classe, caixas envolventes e areas superiores, com multiplicidade; nao compara malhas completas.',
    'Nomes/GUIDs diferem entre fluxos; cada fluxo preservou a propria identidade na reabertura.',
    'Equivalencia geometrica nao comprova equivalencia de modelo analitico, materiais, cargas ou calculo.',
    'Ensaio exploratorio; tempos de escopos distintos nao sustentam ranking geral.'])
write(out/'R50-comparacao-geometrica-CAD-BIM.json',comparison)
m=ifcopenshell.open(str(bim));logger=ifcopenshell.validate.json_logger();ifcopenshell.validate.validate(m,logger)
diagnostic=dict(schema=m.schema,statementCount=len(logger.statements),
    statements=[{k:str(v) if k in ('instance','attribute') else v for k,v in e.items()} for e in logger.statements],
    limits='Validacao de esquema IFC; nao corresponde a validacao estrutural nem normativa da edificacao.')
write(out/'R50-diagnostico-esquema-IFC.json',diagnostic)
materialRows=[]
for cls in ('IfcColumn','IfcBeam','IfcSlab'):
    for o in m.by_type(cls):
        material=ifcopenshell.util.element.get_material(o)
        materialRows.append(dict(type=cls,name=o.Name,guid=o.GlobalId,materialType=material.is_a() if material else None,
            materialName=getattr(material,'Name',None) if material else None))
write(out/'R50-materiais-exportados.json',dict(elements=materialRows,
    limits='Nomes de material no IFC sao triagem; nao comprovam fck, aço, cobrimentos ou parametros nativos. Conferir na interface do Eberick.'))
for name in ('auditar-parcial-h03-r50.py','auditar-final-h03-r50.py','conferir-reabertura-h03-r50.py','congelar-parcial-h03-r50.py','consolidar-h03-r50.py'):
    shutil.copy2(root/'work'/name,out/name)
state=dict(atUtc=datetime.now(timezone.utc).isoformat(),revision='H03/R50',nativeProject=str(native/'Projeto Eberick/H03_BIM_R46_IFC_NAO_EXECUTAR.prj'),
    softwareObserved='AltoQi Eberick 2025 Infinity; versao completa ainda nao consultada no Sobre.',
    columns=22,logicalBeams=29,beamSolids=32,slabs=11,initialGeometryPass=True,reopenedGeometryPass=True,
    sameGeometryNamesGuidsAndTopAreas=True,cadBimSpatialComparisonPass=comparison['sameSpatialMultiset'],
    balconySupportVerified=False,materialsVerifiedInNativeUI=False,structuralCalculationPerformed=False,
    frozenFiles=frozen,preservedFiles=preserved,
    timingFiles=['R50-tempo-dez-lajes.json','R50-tempo-varanda.json','R50-tempo-reabertura.json'],
    nextSteps=['Criar copias seguintes antes de alterar vinculos, materiais ou cargas.',
    'Verificar vinculo/engastamento da varanda e conectividade analitica nos dois ramos.',
    'Harmonizar materiais, cobrimentos, cargas e apoios idealizados da superestrutura.',
    'Somente apos entradas completas processar e avaliar ELU/ELS/estabilidade.',
    'Comparar esforcos por escopos equivalentes no protocolo; sem ranking de tempos parciais.'])
write(out/'R50-estado-atual.json',state)
write(out/'R50-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in out.rglob('*') if p.is_file() and p.name!='R50-manifesto.json']))
print(json.dumps(dict(frozenFiles=len(frozen),preservedFiles=len(preserved),sameSpatialMultiset=comparison['sameSpatialMultiset'],schemaStatements=len(logger.statements),materials=dict(Counter(r['materialName'] for r in materialRows)))))

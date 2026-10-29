"""Finaliza registros de controle sem modificar estados nativos congelados."""
from pathlib import Path
from collections import Counter
import json,hashlib,shutil,sys
sys.path.insert(0,'D:/TCC/work/ifc/deps')
import ifcopenshell,ifcopenshell.validate
root=Path('D:/TCC');out=root/'outputs/Conferencia-H03-R52-VINCULOS-NAO-EXECUTAR'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,r:p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
schema={}
for branch in ('CAD','BIM'):
    control=load(out/f'R52-controle-geometria-{branch}.json');assert control['sameGeometryNamesGuidsAndTopAreas']
    model=ifcopenshell.open(control['source']);logger=ifcopenshell.validate.json_logger();ifcopenshell.validate.validate(model,logger)
    schema[branch]=dict(schema=model.schema,count=len(logger.statements),statements=[{k:str(v) if k in ('instance','attribute') else v for k,v in e.items()} for e in logger.statements])
write(out/'R52-esquema-IFC.json',dict(branches=schema,limits='Erros de esquema nao equivalem a reprovacao/aprovacao estrutural. IFC original nao reparado.'))
rules=root/'work/conferir-reabertura-h03-r49.py';ns={}
exec(compile(rules.read_text(encoding='utf-8').split("a=out/'R49-primeira-exportacao.ifc'")[0],str(rules),'exec'),ns)
def signature(r):return (r['type'],*(round(v,5) for k in ('min','max') for v in r[k]),round(r['topAreaM2'],5))
rows={b:ns['extract'](out/f'IFC-{b}/Modelo 3D.IFC') for b in ('CAD','BIM')}
same=Counter(map(signature,rows['CAD']))==Counter(map(signature,rows['BIM']));assert same
write(out/'R52-comparacao-geometrica.json',dict(sameSpatialMultiset=same,counts={b:dict(Counter(r['type'] for r in rr)) for b,rr in rows.items()},
    limits='Compara classes, caixas envolventes e areas superiores com multiplicidade, nao vinculos, malhas completas ou calculo.'))
state=load(out/'R52-estado-atual.json');state['geometryControlledAfterParametersAndAssignedLink']=True
protected=load(root/'outputs/Conferencia-H03-R51-PARAMETROS-NAO-EXECUTAR/R51-manifesto.json')['files']
for row in protected:assert sha(Path(row['path']))==row['sha256'],row['path']
state['preservedR51Files']=len(protected)
state['sameSpatialMultisetCADBIM']=same;state['schemaErrorsByBranch']={b:r['count'] for b,r in schema.items()}
state['nextSteps']=[s for s in state['nextSteps'] if not s.startswith('Reexportar geometria')]
write(out/'R52-estado-atual.json',state)
for branch in ('CAD','BIM'):
    s=load(out/f'R52-vinculo-{branch}.json')
    for row in s['frozenFiles']:assert sha(Path(row['frozen']))==row['sha256']
    assert sha(Path(s['nativeProject']))==s['afterNativeSha256'],'Projeto salvo divergiu do estado atribuido.'
for name in ('auditar-geometria-h03-r52.py','finalizar-h03-r52.py'):shutil.copy2(root/'work'/name,out/name)
write(out/'R52-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in out.rglob('*') if p.is_file() and p.name!='R52-manifesto.json']))
print(json.dumps(dict(sameSpatialMultiset=same,schemaErrorsByBranch=state['schemaErrorsByBranch'],analyticalLinkVerified=False)))

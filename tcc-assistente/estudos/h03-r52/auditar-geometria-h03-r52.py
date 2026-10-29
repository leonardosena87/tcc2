"""Controla geometria apos parametros/vinculo; nao audita engaste por IFC."""
from pathlib import Path
import json,hashlib,sys
root=Path('D:/TCC');out=root/'outputs/Conferencia-H03-R52-VINCULOS-NAO-EXECUTAR'
branch=sys.argv[1];assert branch in ('CAD','BIM')
source=out/f'IFC-{branch}/Modelo 3D.IFC'
baseline=root/('outputs/Complementacao-H03-R49-LAJES-CAD-NAO-EXECUTAR/R49-apos-reabrir.ifc' if branch=='CAD' else 'outputs/Complementacao-H03-R50-LAJES-BIM-NAO-EXECUTAR/R50-onze-lajes-reaberto.ifc')
rules=root/'work/conferir-reabertura-h03-r49.py';ns={}
exec(compile(rules.read_text(encoding='utf-8').split("a=out/'R49-primeira-exportacao.ifc'")[0],str(rules),'exec'),ns)
before=ns['extract'](baseline);after=ns['extract'](source)
old={r['guid']:r for r in before};new={r['guid']:r for r in after};changes=[]
for guid,r in new.items():
    p=old.get(guid)
    if not p or r['type']!=p['type'] or r['name']!=p['name'] or any(abs(x-y)>1e-5 for k in ('min','max') for x,y in zip(r[k],p[k])) or abs(r['topAreaM2']-p['topAreaM2'])>1e-5:changes.append(guid)
result=dict(branch=branch,source=str(source),baseline=str(baseline),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    counts={c:sum(r['type']==c for r in after) for c in ('IfcColumn','IfcBeam','IfcSlab')},
    changedGuids=changes,missingGuids=sorted(set(old)-set(new)),sameGeometryNamesGuidsAndTopAreas=not changes and set(old)==set(new),
    computationalToleranceM=1e-5,analyticalLinkVerified=False,structuralCalculationPerformed=False,
    limits=['Compara geometria nominal exportada por caixas envolventes e areas superiores, nomes e GUIDs.',
    'Geometria inalterada nao comprova ligacao analitica nem os parametros globais conferidos na interface.'])
assert result['sameGeometryNamesGuidsAndTopAreas'] and len(after)==65
(out/f'R52-controle-geometria-{branch}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))

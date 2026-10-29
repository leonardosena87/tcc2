"""Compara geometria e identidade da R50 antes/depois da reabertura."""
from pathlib import Path
import json,hashlib
root=Path('D:/TCC');out=root/'outputs/Complementacao-H03-R50-LAJES-BIM-NAO-EXECUTAR'
rules=root/'work/conferir-reabertura-h03-r49.py'
ns={};exec(compile(rules.read_text(encoding='utf-8').split("a=out/'R49-primeira-exportacao.ifc'")[0],str(rules),'exec'),ns)
a=out/'R50-onze-lajes-inicial.ifc';b=out/'R50-onze-lajes-reaberto.ifc'
old={r['guid']:r for r in ns['extract'](a)};new={r['guid']:r for r in ns['extract'](b)}
changes=[]
for guid,r in new.items():
    p=old.get(guid)
    if not p or r['type']!=p['type'] or r['name']!=p['name'] or any(abs(x-y)>1e-5 for k in ('min','max') for x,y in zip(r[k],p[k])) or abs(r['topAreaM2']-p['topAreaM2'])>1e-5:changes.append(guid)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
result=dict(firstSha256=sha(a),reopenedSha256=sha(b),counts={c:sum(r['type']==c for r in new.values()) for c in ('IfcColumn','IfcBeam','IfcSlab')},
    changedGuids=changes,missingGuids=sorted(set(old)-set(new)),sameGeometryNamesGuidsAndTopAreas=not changes and set(old)==set(new),computationalToleranceM=1e-5,
    limits='Identidade e geometria exportadas; nao comprova materiais, cargas, conectividade, vinculo do balanco ou calculo.')
assert result['sameGeometryNamesGuidsAndTopAreas']
(out/'R50-reabertura.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))

"""Auditoria R50 com as mesmas regras geometricas usadas no ramo CAD R49."""
from pathlib import Path
import json,hashlib,shutil,copy,sys
root=Path('D:/TCC');out=root/'outputs/Complementacao-H03-R50-LAJES-BIM-NAO-EXECUTAR'
suffix=sys.argv[1] if len(sys.argv)>1 else 'reaberto'
assert suffix in ('inicial','reaberto')
source=out/'Modelo 3D.IFC'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,r:p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
archive=out/f'R50-onze-lajes-{suffix}.ifc'
if archive.exists():
    source=archive # reauditoria usa o historico proprio sem substituir o IFC de trabalho
rules=root/'work/auditar-lajes-h03-r49.py'
code=rules.read_text(encoding='utf-8').split('r=audit(rows)')[0]
code=code.replace("out=Path('D:/TCC/outputs/Complementacao-H03-R49-LAJES-CAD-NAO-EXECUTAR')",'out=provided_out')
code=code.replace("source=out/'Modelo 3D.IFC'",'source=provided_source')
ns=dict(provided_out=out,provided_source=source);exec(compile(code,str(rules),'exec'),ns)
slabs=ns['audit'](ns['rows'])
changed=copy.deepcopy(ns['rows']);changed[0]['min'][2]-=.01
controls=dict(missingDetected=not ns['audit'](ns['rows'][1:])['geometryPass'],
    duplicateDetected=not ns['audit'](ns['rows']+[ns['rows'][0]])['geometryPass'],
    heightChangeDetected=not ns['audit'](changed)['geometryPass'])
slabs.update(source=str(source),sha256=sha(source),computationalToleranceM=1e-5,syntheticControls=controls,
    limits=['Caixas envolventes, espessura, cota e area superior triangulada; mesmas regras R49.',
    'Varanda de 3.2175 m2 a partir da face externa da viga; geometria nao comprova vinculo de apoio.',
    'Materiais, cargas, conectividade analitica, ELU/ELS e estabilidade nao verificados por este script.'])
assert slabs['geometryPass'] and all(controls.values())
write(out/f'R50-auditoria-lajes-{suffix}.json',slabs)
rules2=root/'work/auditar-vigas-h03-r48.py'
code2=rules2.read_text(encoding='utf-8').split("if suffix=='reaberto':")[0]
code2=code2.replace("source=Path(sys.argv[1]); suffix=sys.argv[2]","source=provided_source; suffix='inicial'")
bs=dict(provided_source=source);exec(compile(code2,str(rules2),'exec'),bs)
beams=bs['result'];assert beams['geometryPass']
beams['missingSlabIds']=[]
beams['limits']=['Escopo: 22 trechos de pilares e 29 vigas logicas (32 solidos).',
    'Onze lajes presentes e conferidas por auditoria especifica.',
    'Nao verifica materiais, cargas, conectividade analitica, ELU/ELS ou estabilidade.']
write(out/f'R50-auditoria-pilares-vigas-{suffix}.json',beams)
if archive.exists():assert sha(archive)==sha(source),'Arquivo historico diferente; nao sobrescrever.'
else:shutil.copy2(source,archive)
print(json.dumps(dict(stage=suffix,columns=22,logicalBeams=29,beamSolids=32,slabs=len(ns['rows']),geometryPass=True,syntheticControls=controls,ifcSha256=sha(source))))

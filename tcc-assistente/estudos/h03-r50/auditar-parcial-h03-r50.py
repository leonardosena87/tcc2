"""Reaplica regras R49/R48 ao IFC parcial BIM, sem alterar os historicos."""
from pathlib import Path
import json,hashlib,shutil,collections
root=Path('D:/TCC');out=root/'outputs/Complementacao-H03-R50-LAJES-BIM-NAO-EXECUTAR'
source=out/'R50-dez-lajes.ifc' # evidencia parcial preservada; Modelo 3D.IFC ja evoluiu
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,r:p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rules=root/'work/auditar-lajes-h03-r49.py'
code=rules.read_text(encoding='utf-8').split('r=audit(rows)')[0]
code=code.replace("out=Path('D:/TCC/outputs/Complementacao-H03-R49-LAJES-CAD-NAO-EXECUTAR')",'out=provided_out')
code=code.replace("source=out/'Modelo 3D.IFC'",'source=provided_source')
ns=dict(provided_out=out,provided_source=source);exec(compile(code,str(rules),'exec'),ns)
slabs=ns['audit'](ns['rows'])
ids=[r['sourceIds'][0] for r in slabs['slabs'] if len(r['sourceIds'])==1]
slabs.update(source=str(source),sha256=sha(source),matchedSlabs=len(ids),
    presentSlabsPass=len(ids)==10 and len(set(ids))==10 and len(ns['rows'])==10,
    limits=['Auditoria parcial: varanda ainda ausente, geometria completa nao aprovada.',
            'Mesmas regras geometricas R49 de faces de vigas, espessura e area.',
            'Nao confere conectividade, apoio, materiais, cargas ou calculo.'])
assert slabs['presentSlabsPass'] and slabs['missingIds']==['L7-VARANDA-N1']
write(out/'R50-auditoria-dez-lajes.json',slabs)
rules2=root/'work/auditar-vigas-h03-r48.py'
code2=rules2.read_text(encoding='utf-8').split("if suffix=='reaberto':")[0]
code2=code2.replace("source=Path(sys.argv[1]); suffix=sys.argv[2]","source=provided_source; suffix='inicial'")
bs=dict(provided_source=source);exec(compile(code2,str(rules2),'exec'),bs)
assert bs['result']['geometryPass']
bs['result']['missingSlabIds']=['L7-VARANDA-N1']
bs['result']['limits']=['Verificacao geometrica apenas dos 22 trechos de pilares e 29 vigas logicas (32 solidos).',
    'BIM R50 parcial: dez lajes presentes; varanda ausente conforme auditoria especifica.',
    'Nao verifica cargas, materiais, conectividade analitica, apoio, ELU/ELS ou estabilidade.']
write(out/'R50-auditoria-pilares-vigas.json',bs['result'])
print(json.dumps(dict(columns=22,logicalBeams=29,slabs=10,presentSlabsPass=True,missingSlabs=slabs['missingIds'])))

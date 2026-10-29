from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
root=Path('D:/TCC');out=root/'outputs/Complementacao-H03-R49-LAJES-CAD-NAO-EXECUTAR'
native=root/'outputs/H03_CAD_R49_LAJES_NAO_EXECUTAR'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Reutilizar somente definicoes R48, sem sobrescrever arquivos historicos.
script=root/'work/auditar-vigas-h03-r48.py'
code=script.read_text(encoding='utf-8').split("if suffix=='reaberto':")[0]
code=code.replace("source=Path(sys.argv[1]); suffix=sys.argv[2]","source=provided_source; suffix='inicial'")
ns={'provided_source':out/'Modelo 3D.IFC'}
exec(compile(code,str(script),'exec'),ns)
r=ns['result'];assert r['geometryPass']
write(out/'R49-auditoria-pilares-vigas.json',r)
assert load(out/'R49-auditoria-lajes-inicial.json')['geometryPass']
preserved=[]
for e in load(root/'outputs/Complementacao-H03-R48-VIGAS-CAD-NAO-EXECUTAR/R48-manifesto.json')['files']:
    p=Path(e['path']);assert sha(p)==e['sha256'];preserved.append(str(p))
frozen=[]
for folder in ('Projeto Eberick','_DADOS_'):
    for p in (native/folder).rglob('*'):
        if not p.is_file() or p.suffix.lower() in ('.bak','.lck','.tmp'):continue
        dst=out/'congelado'/p.relative_to(native);dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,dst);frozen.append(dict(path=str(p),frozen=str(dst),sha256=sha(p)))
for name in ('auditar-lajes-h03-r49.py','consolidar-h03-r49.py'):
    shutil.copy2(root/'work'/name,out/name)
state=dict(atUtc=datetime.now(timezone.utc).isoformat(),revision='H03/R49',
    nativeProject=str(native/'Projeto Eberick/H03_CAD_R49_LAJES_NAO_EXECUTAR.prj'),
    columns=22,logicalBeams=29,beamSolids=32,slabs=11,initialGeometryPass=True,
    reopenedAndReexported=False,balconySupportVerified=False,structuralCalculationPerformed=False,
    frozenFiles=frozen,preservedR48Files=preserved,
    nextSteps=['Reabrir R49 e reexportar IFC para conferir persistencia.',
               'Verificar vinculo/engastamento da varanda nos dois ramos, sem presumir estabilidade pela geometria.',
               'Complementar 11 lajes no receptor BIM em copia independente e tempo prospectivo.',
               'Harmonizar materiais cobrimentos cargas apoios e conectividade antes do calculo.'])
write(out/'R49-estado-parcial.json',state)
write(out/'R49-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in out.rglob('*') if p.is_file() and p.name!='R49-manifesto.json']))
print(json.dumps(dict(columns=22,beams=29,slabs=11,initialGeometryPass=True,frozenFiles=len(frozen),preservedR48Files=len(preserved))))

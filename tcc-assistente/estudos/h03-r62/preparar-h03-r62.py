"""Prepara ampliacao G RC03..RC13, sem alterar o piloto protegido R61."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
root=Path('D:/TCC')
src=root/'outputs/Cargas-H03-R61-TELHADO-G-PARCIAL-NAO-EXECUTAR'
r60=root/'outputs/Cobertura-H03-R60-REACOES-PARCIAIS-NAO-EXECUTAR'
out=root/'outputs/Cargas-H03-R62-TELHADO-G-PARCIAL-NAO-EXECUTAR'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(src/'R61-manifesto.json')['files']
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
nodes=read(r60/'R60-arranjo-reacoes.json')['reactionNodes']
pending=read(src/'R61-resultado.json')['pendingGPointIds']
plan=[dict(id=n['id'],xCm=n['xM']*100,yCm=n['yM']*100,fzKN=-round(n['gDownKN'],6),action='Adicional',targets=n['nativeTargets']) for n in nodes if n['id'] in pending]
assert len(plan)==11
out.mkdir(exist_ok=False)
(out/'R62-protegidos-R61.json').write_text(json.dumps(protected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for b in ('CAD','BIM'):
    state=read(src/f'R61-estado-{b}.json')
    dst=root/f'outputs/H03_{b}_R62_TELHADO_G_PARCIAL_NAO_EXECUTAR'
    dst.mkdir(exist_ok=False)
    for r in state['frozenFiles']:
        p=Path(r['frozen']);assert sha(p)==r['sha256'];q=dst/p.relative_to(src/f'congelado-{b}')
        q.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(p,q);assert sha(q)==r['sha256']
    data=dict(branch=b,nativeProject=str(dst/'Projeto Eberick'/Path(state['nativeProject']).name),sourceState=str(src/f'R61-estado-{b}.json'),plannedPoints=plan,alreadyPresent=['RC01','RC02'],plannedNewGDownKN=-sum(n['fzKN'] for n in plan),roofVariableLoadsApplied=False,applied=False)
    (out/f'R62-preparacao-{b}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name)
print(json.dumps(dict(preparedAtUtc=datetime.now(timezone.utc).isoformat(),points=11,newGDownKN=-sum(n['fzKN'] for n in plan),out=str(out)),ensure_ascii=False))

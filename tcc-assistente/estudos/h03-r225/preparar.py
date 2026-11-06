"""Prepara retorno geometrico das correcoes Eberick; nao substitui ensaio de transferencia."""
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[1]
ROOT = Path('D:/TCC/outputs/H03-R225-AUTORIA-COORDENACAO-NAO-EXECUTAR')
sys.path.insert(0, str(BASE/'h03-r122'))
from consolidar import parse, number


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(plan):
    return sum((plan[k] for k in ('retainedExistingElements','changedExistingElements','addedElements')), [])


def candidate(old):
    entries=copy.deepcopy(rows(old)); by={e['id']:e for e in entries}
    if len(by)!=63: raise ValueError('Referencia R160 divergente')
    for key in ('P11-N1','P11-N2'):
        if (by[key]['x'],by[key]['y'],by[key]['b'],by[key]['h'])!=(6.55,3.9,.3,.2):
            raise ValueError('Prumada de referencia divergente')
        by[key]['h']=.3
    if (by['V3-N1']['x'],by['V3-N1']['x2'],by['V3-N1']['y'])!=(0,4.4,3.9):
        raise ValueError('Linha da V3 mudou')
    by['V3-N1'].update(x2=3.55,b=.3,h=.45)
    by['V4A-N1'].update(b=.3)
    additions=[dict(id='P12-N1',kind='column',level=0,x=3.55,y=3.9,z0=.2,z1=3.2,b=.2,h=.3),
               dict(id='V3B-N1',kind='beam',level=0,x=3.55,y=3.9,x2=4.4,y2=3.9,z=3.2,b=.3,h=.2),
               dict(id='V17-BASE-ESC',kind='beam',level=0,x=4.5,y=3.2158,x2=5.4,y2=3.2158,z=.2,b=.3,h=.3)]
    entries.extend(additions)
    changed={'P11-N1','P11-N2','V3-N1','V4A-N1'}
    return dict(schema='tcc-coordenacao-autoria/1',revision='H03/R225',units='m',
        status='RETORNO GEOMETRICO DA HIPOTESE ANALITICA - NAO EXECUTAR',
        sourceCandidateRevision='R160',sourceAnalyticalRevision='R223/R224',
        retainedExistingElements=[e for e in entries if e['id'] not in changed and e not in additions],
        changedExistingElements=[e for e in entries if e['id'] in changed],addedElements=additions,
        counts=dict(column=23,beam=32,slab=11),elementCount=66,
        stairsGeometryModified=False,stairsInheritedRevision='R160:17 espelhos (9+8), concreto patamar+1,774117647 m',
        sourceStairBaseConcreteM=.17,lowerBeamTopM=.2,lowerStairInterfaceResolved=False,
        windowJ4RemovedInherited=True,materialsModified=False,reinforcementModeled=False,
        analyticalModelCreated=False,nativeAuthoringApplied=False,structuralApproval=False,
        pending=['Ligacao e ancoragens V1; ELS local','Aviso08 cobertura',
                 'Apoio W08 inferior','P11/P6 e porta P3; saliencia P12',
                 'Conferencia completa dos perfis/lajes/ligacoes e novas exportacoes',
                 'Medicao prospectiva dos fluxos; retorno geometrico nao e ensaio de recepcao'])


def beam_audit(plan, path):
    model=parse(path.read_text(encoding='cp1252'))
    props={r['SectionName']:r for r in model['tables']['FRAME SECTION PROPERTIES 01 - GENERAL']}
    assign={r['Frame']:props[r['AnalSect']] for r in model['tables']['FRAME SECTION ASSIGNMENTS']}
    result=[]
    for e in rows(plan):
        if e['kind']!='beam': continue
        a=tuple(100*e[k] for k in ('x','y','z')); b=(100*e['x2'],100*e['y2'],a[2])
        axis=next(i for i in range(3) if abs(b[i]-a[i])>.01)
        lo,hi=sorted((a[axis],b[axis])); expected=(100*e['b'])*(100*e['h'])**3/12
        selected=[]
        for key,(p,q) in model['frames'].items():
            if any(abs(p[j]-a[j])>.02 or abs(q[j]-a[j])>.02 for j in range(3) if j!=axis): continue
            left,right=sorted((p[axis],q[axis]))
            if min(right,hi)-max(left,lo)<=.001: continue
            inertia=number(assign[key]['I33'])
            if inertia>1.e9 or inertia==0: continue
            selected.append(dict(frame=key,intervalCm=[max(left,lo),min(right,hi)],I33cm4=inertia,
                                 matchesExpected=abs(inertia-expected)<=.011))
        result.append(dict(id=e['id'],expectedI33cm4=expected,nativeSegments=selected,
                           allSelectedI33Match=bool(selected) and all(v['matchesExpected'] for v in selected),
                           scope='Controle parcial de eixo e I33; nao confere largura/altura/solidos separadamente'))
    return result


def main():
    if ROOT.exists(): raise FileExistsError(ROOT)
    old_path=BASE/'h03-r160/R160-candidato-comum.json'
    if sha(old_path)!='ab2812be217fe6f68e49c2d034f136d07999c1034d785174c1d847a964c600da':
        raise ValueError('Candidato R160 alterado')
    old=json.loads(old_path.read_text(encoding='utf-8')); plan=candidate(old)
    audits={b:beam_audit(plan,Path('D:/TCC/outputs/H03-R223-V1-30X30-ENSAIO-NAO-EXECUTAR')/(b+'-generico')/'portico_SAP2000_elastico.$2k') for b in ('CAD','BIM')}
    # O controle informa divergencias em vez de impor igualdade ao arquivo nativo.
    ROOT.mkdir()
    def write(name,data): (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    write('R225-candidato-comum.json',plan)
    write('R225-controle-parcial-eixos-inercia.json',audits)
    src=Path('D:/TCC/outputs/W08-H03-R207-ENSAIO/Autoria-salva/H03-R195-SEM-J4.rvt')
    dest=ROOT/'H03-R225-REVIT-COORDENACAO-NAO-EXECUTAR.rvt'
    dest.write_bytes(src.read_bytes())
    write('R225-config.json',dict(CopyPath=str(dest),CopySha256Before=sha(dest),
        CandidatePath=str(ROOT/'R225-candidato-comum.json'),CandidateSha256=sha(ROOT/'R225-candidato-comum.json'),
        SourcePath=str(src),SourceSha256=sha(src),PreparedAtUtc=datetime.now(timezone.utc).isoformat()))
    print(json.dumps({b:[r['id'] for r in audits[b] if not r['allSelectedI33Match']] for b in audits}))


if __name__=='__main__': main()

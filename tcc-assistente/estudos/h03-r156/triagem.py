"""Triagem nominal da chegada da escada; não calcula sólidos nativos ou apoios."""
import json
import hashlib
import shutil
import sys
from datetime import datetime,timezone
from pathlib import Path
from time import perf_counter

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R156-APOIOS-CHEGADA-NAO-EXECUTAR')
PROPOSAL=Path('D:/TCC/outputs/Autoria-H03-R83-SINCRONIZACAO-GEOMETRICA-NAO-EXECUTAR/H03-R83-proposta.json')
PLAN=Path('D:/TCC/outputs/Escada-H03-R153-17-9MAIS8-NAO-EXECUTAR/R153-geometria9mais8.json')
NATIVE=Path('D:/TCC/outputs/Escada-H03-R155-Revit-17-NAO-EXECUTAR/R155-resultado.json')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def box(e):
    if e['kind']=='slab':return [e['x'],e['y'],e['z']-e['h'],e['x2'],e['y2'],e['z']]
    if e['kind']!='beam':raise ValueError('Somente viga ou laje')
    if abs(e['y2']-e['y'])<1e-9:
        return [min(e['x'],e['x2']),e['y']-e['b']/2,e['z']-e['h'],max(e['x'],e['x2']),e['y']+e['b']/2,e['z']]
    if abs(e['x2']-e['x'])<1e-9:
        return [e['x']-e['b']/2,min(e['y'],e['y2']),e['z']-e['h'],e['x']+e['b']/2,max(e['y'],e['y2']),e['z']]
    raise ValueError('Viga obliqua exige geometria explicita')

def inside_horizontal_face(face,b):
    points=face['vertices'];z=points[0][2]
    if not all(abs(p[2]-z)<1e-9 for p in points):raise ValueError('Face nao horizontal')
    x1=max(min(p[0] for p in points),b[0]);x2=min(max(p[0] for p in points),b[3])
    y1=max(min(p[1] for p in points),b[1]);y2=min(max(p[1] for p in points),b[4])
    if b[2]+1e-9<z<b[5]-1e-9 and x2-x1>1e-9 and y2-y1>1e-9:
        return dict(xMinM=x1,xMaxM=x2,yMinM=y1,yMaxM=y2,zM=z,areaM2=(x2-x1)*(y2-y1),yOverlapM=y2-y1)
    return None

def main():
    tick=perf_counter();start=datetime.now(timezone.utc).isoformat()
    if OUT.exists():raise FileExistsError(OUT)
    sources=[dict(path=str(p),sha256=sha(p)) for p in (PROPOSAL,PLAN,NATIVE)]
    proposal=json.loads(PROPOSAL.read_text(encoding='utf-8'));plan=json.loads(PLAN.read_text(encoding='utf-8'));native=json.loads(NATIVE.read_text(encoding='utf-8'))
    assert proposal['units']=='m' and len(proposal['elements'])==62
    assert native['nativeCreatedSavedReopenedReadbackMatched'] and native['readback']['TotalRisers']==17
    elements={e['id']:e for e in proposal['elements']}
    floor=elements['L6-N1'];edge=elements['V15-N1']
    assert floor['role']=='circulacao' and edge['role']=='borda-abertura-escada'
    rows=[]
    for face in plan['finishedSurfaceFaces']:
        if face['kind'] not in ('tread','landing'):continue
        for e in proposal['elements']:
            if e['kind'] not in ('beam','slab') or e['level']!=0:continue
            overlap=inside_horizontal_face(face,box(e))
            if overlap:rows.append(dict(finishedFaceKind=face['kind'],riserNumber=face.get('number'),nominalElementId=e['id'],nominalBoxM=box(e),**overlap))
    arrival=plan['clearEnvelope']['upperArrivalYM'];landing=native['readback']['Landings'][0]['FinishedM']
    assert {(r['riserNumber'],r['nominalElementId']) for r in rows}=={(15,'V13-N1'),(16,'V13-N1'),(16,'V15-N1'),(16,'L6-N1')}
    assert abs(arrival-floor['y']-.0857833333333322)<1e-9
    landingBottom=landing-.14
    intermediate=[e['id'] for e in proposal['elements'] if e['kind']=='beam' and box(e)[2]<=landing and box(e)[5]>=landingBottom]
    assert not intermediate
    result=dict(revision='H03/R156',createdAtUtc=datetime.now(timezone.utc).isoformat(),sources=sources,
        scope='Superficies acabadas R153 versus caixas nominais da proposta R83; nao e teste de solidos nativos R155/Eberick',
        nominalUpperHallEdgeYM=floor['y'],finishedStairArrivalYM=arrival,
        arrivalBeyondNominalHallEdgeM=arrival-floor['y'],finishedUpperM=3.25,nominalConcreteFloorTopM=floor['z'],
        upperFinishAllowanceUnspecifiedM=3.25-floor['z'],
        overlaps=rows,nativeBooleanClashTestExecuted=False,overlapsAutomaticallyClassifiedAsDefects=False,
        finishedLandingM=landing,landingStructuralDepthHypothesisM=.14,landingBottomUnderNoFinishHypothesisM=landingBottom,
        beamsAtLandingVerticalBandInNominalProposal=intermediate,
        candidateExistingColumnsAtFacade=['P4-N1','P10-N1'],columnConnectionOrCapacityVerified=False,
        supportSchemeAdopted=False,loadsApplied=False,nativeFilesEdited=False,structuralApproval=False,
        nextSteps=['Distinguir superficies acabadas da geometria resistente; fechamento superior possui diferenca de5cm ainda sem camada definida.',
        'Rever conjuntamente a borda L6/V15 e a chegada, verificando se existe uniao de apoio prevista ou interferencia; nao apagar a sobreposicao sem detalhar.',
        'Definir apoio do patamar e transmissao de reacoes; duas colunas proximas nao demonstram apoio continuo ou autoportancia.',
        'Conferir fisicamente as mesmas alteracoes na autoria CAD/Revit e nos receptores antes de contabilizar correcoes de intercambio.'],
        officialMethodSource='https://suporte.altoqi.com.br/hc/pt-br/articles/115001700534')
    OUT.mkdir();(OUT/'R156-triagem.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    render(plan,elements,rows)
    assert all(sha(Path(r['path']))==r['sha256'] for r in sources)
    (OUT/'R156-tempo-script.json').write_text(json.dumps(dict(startUtc=start,endUtc=datetime.now(timezone.utc).isoformat(),scriptMs=(perf_counter()-tick)*1000,isFlowTime=False),indent=2),encoding='utf-8')
    shutil.copyfile(HERE/'LEIA-ME-R156.md',OUT/'LEIA-ME-R156.md')
    for p in OUT.iterdir():
        if p.is_file():shutil.copyfile(p,HERE/p.name)
    (HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    manifest=[dict(path=p.name,sha256=sha(p)) for p in sorted(HERE.iterdir()) if p.is_file() and 'manifesto' not in p.name]
    for folder in (HERE,OUT):(folder/'R156-manifesto.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(dict(nominalOverlaps=len(rows),arrivalBeyondHallEdgeMm=(arrival-floor['y'])*1000,intermediateSupportDefined=False)))

def render(plan,elements,rows):
    sys.path.insert(0,'D:/TCC/work/plot-deps')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig,(ax,side)=plt.subplots(1,2,figsize=(12,6))
    floor=elements['L6-N1'];beam=elements['V15-N1'];env=plan['clearEnvelope']
    ax.add_patch(Rectangle((floor['x'],floor['y']),floor['x2']-floor['x'],floor['y2']-floor['y'],color='#c3dced',label='L6 nominal'))
    b=box(beam);ax.add_patch(Rectangle((b[0],b[1]),b[3]-b[0],b[4]-b[1],fill=False,edgecolor='#283947',hatch='///',label='V15 nominal'))
    b=box(elements['V13-N1']);ax.add_patch(Rectangle((b[0],b[1]),b[3]-b[0],b[4]-b[1],fill=False,edgecolor='#573e65',hatch='...',label='V13 nominal'))
    for f in plan['finishedSurfaceFaces']:
        if f['kind'] not in ('tread','landing'):continue
        v=f['vertices']+[f['vertices'][0]];ax.plot([p[0] for p in v],[p[1] for p in v],color='#c17316',lw=1)
    ax.axhline(env['upperArrivalYM'],color='#b52329',ls='--',label='Chegada acabada')
    ax.set(xlim=(4.2,6.8),ylim=(-.1,4.05),xlabel='X local (m)',ylabel='Y local (m)',title='Planta: geometria nominal e superfícies acabadas')
    ax.set_aspect('equal');ax.legend(fontsize=8,loc='lower left')
    for e,c,label in ((floor,'#8ab5d4','L6 nominal'),(beam,'#536873','V15 nominal')):
        q=box(e);side.add_patch(Rectangle((q[1],q[2]),q[4]-q[1],q[5]-q[2],color=c,alpha=.65,label=label))
    for f in plan['finishedSurfaceFaces']:
        if f['kind']!='tread' or f.get('number',0)<10:continue
        ys=[p[1] for p in f['vertices']];z=f['vertices'][0][2];side.plot([min(ys),max(ys)],[z,z],color='#c17316',lw=2)
    side.axhline(3.25,color='#b52329',ls='--',label='Piso acabado +3,25')
    side.axvline(env['upperArrivalYM'],color='#b52329',ls=':')
    side.set(xlim=(2.15,3.25),ylim=(2.65,3.4),xlabel='Y local (m)',ylabel='Cota (m)',title='Chegada superior: triagem nominal')
    side.legend(fontsize=8);side.grid(alpha=.2)
    fig.suptitle('H03/R156 — escada 17 (9 + 8): conferência de borda e apoio\nSobreposição nominal não prova defeito nem união resistente',fontsize=12)
    fig.text(.5,.012,'ESTUDO — NÃO EXECUTAR | Geometria resistente, acabamentos e apoios ainda precisam de compatibilização.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.04,1,.90));fig.savefig(OUT/'R156-chegada-nominal.png',dpi=160);plt.close(fig)

if __name__=='__main__':main()

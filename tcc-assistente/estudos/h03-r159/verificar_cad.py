"""Confere o retorno DXF do DWG salvo, fechado e reaberto no AutoCAD.

Não calcula volumes resistentes, cargas ou capacidade estrutural.
"""
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,'D:/TCC/work/dxf-deps')
import ezdxf

OUT=Path('D:/TCC/outputs/Escada-H03-R159-IMPLANTACAO-NAO-EXECUTAR')
CAD=Path('D:/TCC/outputs/Escada-H03-R158-CANDIDATO-COMUM-NAO-EXECUTAR')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def compare(expected,actual,tolerance=1e-9):
    if len(expected)!=len(actual):raise ValueError('Contagem de faces divergente')
    if {f['id'] for f in expected}!={f['id'] for f in actual}:raise ValueError('Identidades divergentes')
    if len({f['id'] for f in actual})!=len(actual):raise ValueError('Identidade duplicada')
    index={f['id']:f for f in actual};maximum=0
    for e in expected:
        a=index[e['id']]
        if a['layer']!=e['layer']:raise ValueError('Camada divergente: '+e['id'])
        if len(a['vertices'])!=4 or len(e['vertices'])!=4:raise ValueError('Face irregular')
        choices=[]
        for vertices in (a['vertices'],list(reversed(a['vertices']))):
            for k in range(4):
                rotated=vertices[k:]+vertices[:k]
                delta=[abs(v-w) for p,q in zip(e['vertices'],rotated) for v,w in zip(p,q)]
                if any(not math.isfinite(x) for x in delta):raise ValueError('Coordenada não finita')
                choices.append(max(delta))
        best=min(choices)
        if best>tolerance:raise ValueError('Coordenada/topologia divergente: '+e['id'])
        maximum=max(maximum,best)
    return maximum

def main():
    source=CAD/'R158-escada-apoios-CANDIDATO.dxf';dwg=CAD/'R158-escada-apoios-CANDIDATO.dwg';returned=CAD/'R158-retorno-DWG-reaberto.dxf'
    expected=json.loads((CAD/'R158-dxf-gerado.json').read_text(encoding='utf-8'))['faces']
    d=ezdxf.readfile(returned);audit=d.audit()
    assert d.units==6 and not audit.has_errors
    assert len(d.modelspace().query('3DSOLID'))==0
    rows=[]
    for entity in d.modelspace().query('3DFACE'):
        tags=[t.value for t in entity.get_xdata('TCC_R158') if t.code==1000]
        assert len(tags)==2 and tags[1]=='CANDIDATO - NAO EXECUTAR'
        rows.append(dict(id=tags[0],layer=entity.dxf.layer,vertices=[list(entity.dxf.get('vtx'+str(i))) for i in range(4)]))
    delta=compare(expected,rows)
    assert len(rows)==96
    start=json.loads((CAD/'CAD-retomada-inicio.json').read_text(encoding='utf-8'));end=json.loads((CAD/'CAD-retomada-fim.json').read_text(encoding='utf-8'))
    result=dict(revision='H03/R159 - conferência CAD R158',sourceDxfPath=str(source),sourceDxfSha256=sha(source),dwgPath=str(dwg),dwgSha256=sha(dwg),returnDxfPath=str(returned),returnDxfSha256=sha(returned),
        savedClosedReopened=True,faceCount=len(rows),countsByLayer=dict(Counter(r['layer'] for r in rows)),allFaceIdentitiesAndLayersRetained=True,maxCoordinateDeltaM=delta,units='m',
        partialCandidateOnly=True,completeBuildingRepresented=False,closedStairWaistVolume=False,structuralApproval=False,eberickImported=False,
        sessionStart=start,sessionEnd=end,sessionElapsedMs=end['mono']-start['mono'],includesNavigationReasoningAndCapture=True,usableForPairedFlowRanking=False)
    (OUT/'R159-CAD-conferencia.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('faceCount','maxCoordinateDeltaM','sessionElapsedMs','usableForPairedFlowRanking')}))

if __name__=='__main__':main()

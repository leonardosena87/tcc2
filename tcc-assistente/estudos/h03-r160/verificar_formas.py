"""Verifica geometria e dados das plantas após retorno nativo pelo DWG."""
import json
from collections import Counter
from verificar_cad import OUT,sha,compare,ezdxf

def read(path):
    doc=ezdxf.readfile(path)
    assert doc.units==6 and not doc.audit().has_errors
    rows=[];data={};anonymous=0
    for entity in doc.modelspace().query('LWPOLYLINE'):
        assert entity.closed and entity.dxf.elevation==0
        if entity.has_xdata('TCC_R160'):
            tags=[t.value for t in entity.get_xdata('TCC_R160') if t.code==1000]
            assert len(tags)==2 and tags[0] not in data
            key=tags[0];data[key]=json.loads(tags[1]);assert data[key]['id']==key
        else:key='contexto-sem-id-'+str(anonymous);anonymous+=1
        rows.append(dict(id=key,layer=entity.dxf.layer,vertices=[[p[0],p[1],0] for p in entity.get_points('xy')]))
    texts=Counter(e.dxf.text for e in doc.modelspace().query('TEXT'))
    lines=[(e.dxf.layer,tuple(e.dxf.start),tuple(e.dxf.end)) for e in doc.modelspace().query('LINE')]
    return rows,data,texts,lines

def main():
    preparation=json.loads((OUT/'R160-formas-CAD-geradas.json').read_text(encoding='utf-8'))
    results=[];unique=set()
    for item in preparation['files']:
        source=OUT/(item['path'].replace('\\','/').split('/')[-1]);dwg=source.with_suffix('.dwg');returned=source.with_name(source.stem+'-retorno.dxf')
        assert sha(source)==item['sha256'] and dwg.read_bytes()[:6]==b'AC1032'
        before=read(source);after=read(returned)
        delta=compare(before[0],after[0]);assert before[1:3]==after[1:3]
        assert len(before[3])==len(after[3])
        line_delta=0
        for a,b in zip(before[3],after[3]):
            assert a[0]==b[0]
            line_delta=max(line_delta,max(abs(x-y) for p,q in zip(a[1:],b[1:]) for x,y in zip(p,q)))
        assert line_delta<=1e-9
        assert all(key in after[1] for key in item['selectedElementIds'])
        unique.update(item['selectedElementIds'])
        results.append(dict(level=item['level'],dwgPath=str(dwg),dwgSha256=sha(dwg),returnPath=str(returned),returnSha256=sha(returned),sourceSha256=item['sha256'],
            savedClosedReopenedByNativeScript=True,polylineCount=len(after[0]),selectedElementCount=item['selectedCount'],maxCoordinateDeltaM=delta,xdataJsonRetainedExactly=True,
            textContentAndAxisLinesRetained=True,maxAxisCoordinateDeltaM=line_delta,units='m',zIs2DZero=True,eberickImported=False))
    assert len(unique)==63
    result=dict(files=results,uniqueBuildingElementCount=63,allThreeSavedClosedReopened=True,sourceIsSameR160Candidate=True,stairsResistantVolumeIncluded=False,
        analyticalModelCreated=False,eberickTransferred=False,structuralApproval=False,pairedComparisonComplete=False,
        nativeSessionEnd=json.loads((OUT/'R160-CAD-formas-fim.json').read_text(encoding='utf-8')))
    (OUT/'R160-CAD-formas-conferidas.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(files=len(results),uniqueElements=len(unique),maxDeltaM=max(r['maxCoordinateDeltaM'] for r in results))))

if __name__=='__main__':main()

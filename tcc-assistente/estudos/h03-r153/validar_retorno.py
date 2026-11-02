"""Compara superfícies de origem com exportação feita após reabrir DWG no AutoCAD."""
import json
import sys
from collections import Counter
from conferir import OUT,sha,archive

def normalized_faces(rows):
    return Counter((layer,tuple(sorted(tuple(round(float(v),9) for v in p) for p in vertices))) for layer,vertices in rows)

def read(path):
    sys.path.insert(0,'D:/TCC/work/dxf-deps');import ezdxf
    doc=ezdxf.readfile(path);audit=doc.audit()
    if audit.has_errors:raise ValueError('DXF com erros de auditoria')
    return doc,[(f.dxf.layer,[tuple(f.dxf.get('vtx'+str(i))) for i in range(4)]) for f in doc.modelspace().query('3DFACE')]

def main():
    target=OUT/'R153-retorno-AutoCAD.json'
    if target.exists():raise FileExistsError(target)
    src=OUT/'R153-escada17-superficies3D.dxf';ret=OUT/'R153-AutoCAD-DWG-reaberto.dxf'
    dwg=OUT/'R153-escada17-9mais8-ESTUDO-NAO-EXECUTAR.dwg'
    a,af=read(src);b,bf=read(ret)
    assert len(af)==len(bf)==33
    assert a.units==b.units==6
    assert normalized_faces(af)==normalized_faces(bf)
    # Igualdade exata após ordenar vértices; canonização9casas apenas identifica o par.
    def key(row):return row[0],tuple(sorted(tuple(round(v,9) for v in p) for p in row[1]))
    bmap={key(row):row for row in bf};max_error=0.
    for row in af:
        other=bmap[key(row)]
        for p,q in zip(sorted(row[1]),sorted(other[1])):
            max_error=max(max_error,max(abs(x-y) for x,y in zip(p,q)))
    assert max_error<1e-9
    assert dwg.read_bytes()[:6]==b'AC1032'
    session=json.loads((OUT/'CAD-sessao-tempo.json').read_text(encoding='utf-8'))
    result=dict(nativeAutoCad2027OpenedSourceDxf=True,independentDwgSavedClosedReopened=True,
        sourceFaces=33,returnedFaces=33,unitsCode=6,units='metres',maximumCoordinateDeltaM=max_error,
        canonicalPairingDecimalPlaces=9,faceOrientationOrNormalsNotCompared=True,
        layerNamesAndVertexSetsPreserved=True,
        fileEvidence=[dict(path=p.name,bytes=p.stat().st_size,sha256=sha(p)) for p in (src,ret,dwg)],
        nativeDwgRemainsLocalOnly=True,existingBuildingProjectsEdited=False,
        stairIntegratedInExistingBuilding=False,structuralAnalysisPerformed=False,
        cadSessionWallMs=session['wallMs'],cadSessionNotFinalFlowTime=True,
        warnings=['Arquivo de superfícies sem espessura; não define volume/peso próprio.',
            'Recuperação de sessão anterior foi informada no início; arquivos de recuperação H02/H03 não foram abertos/editados.',
            'AtalhosCtrl+O/Ctrl+Shift+S não acionaram o resultado esperado na tela inicial; usaram-se Abrir e SAVEAS.',
            'ZOOM recebeu comando como opção em uma tentativa; opçãoExtents foi repetida e conferida. VPOINT abriu diálogo, cancelado; usou-se -VPOINT.',
            'Tempo inclui inicialização, aviso, tentativas, navegação, capturas e exportação, sem tempo de autoria/script ou comparaçãoBIM.'])
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');archive()
    print(json.dumps(dict(faces=33,maxDeltaM=max_error,wallMs=session['wallMs'])))

if __name__=='__main__':main()

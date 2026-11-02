"""Registra consulta nativa e verifica preservação, sem reprocessar modelos."""
import hashlib
import json
import re
import shutil
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Diagnostico-H03-R150-D16-NAO-EXECUTAR')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def parse(text):
    if '77-H03-R150-BIM-CONSULTA-D16' not in text or 'armadura negativa (nó 2)' not in text:
        raise ValueError('Projeto ou nó diferente')
    found=re.findall(r'ø ([\d.]+) - Erro (A\d+) - ([^\r\n]+)',text)
    if len(found)!=5 or len({float(x[0]) for x in found})!=5:raise ValueError('Lista incompleta/duplicada')
    return [dict(diameterMm=float(d),code=c,message=m) for d,c,m in found]

def main():
    target=OUT/'R150-diagnostico.json'
    if target.exists():raise FileExistsError(target)
    prep=json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    preserved=[dict(source=r['source'],unchanged=sha(Path(r['source']))==r['sha256Before']) for r in prep['files']]
    assert all(r['unchanged'] for r in preserved)
    projects=[dict(branch=r['branch'],path=r['copy'],unchanged=sha(Path(r['copy']))==r['sha256Before'])
              for r in prep['files'] if Path(r['copy']).suffix.lower()=='.prj']
    assert len(projects)==2 and all(r['unchanged'] for r in projects)
    rows=parse((OUT/'BIM-V2-No2-bitolas-UI.txt').read_text(encoding='utf-8'))
    timing=json.loads((OUT/'BIM-sessao-tempo.json').read_text(encoding='utf-8'))
    data=dict(revision='H03/R150',branchAudited='BIM',cadCopyOpened=False,
        floor='TCC-cdd31967-N1',beamNativeName='V2',selectedNode=2,supportNativeName='P5',
        perDiameterNativeAccessibilityReading=rows,
        visualTranscription=dict(automaticallyParsed=False,
            nodes=[dict(node=1,support='P6',supportWidthCm=30,negativeMomentKNm=-6.71,error='D16'),
                   dict(node=2,support='P5',supportWidthCm=20,negativeMomentKNm=-39.26,error='D16'),
                   dict(node=3,support='P4',supportWidthCm=20,negativeMomentKNm=-34.02,error='D16')],
            rectangularSpansCm=[dict(span=1,bw=20,h=16,elevation=0),dict(span=2,bw=20,h=45,elevation=0)]),
        configuredMaximumReinforcementRatioRead=False,reinforcementAreaNumericallyRead=False,
        sourceFilesPreserved=preserved,consultationProjects=projects,timing=timing,
        screenshots=[dict(path=p.name,sha256=sha(p)) for p in sorted(OUT.glob('*.jpg'))],
        nativeDataEdited=False,reprocessed=False,ifcCausalityEstablished=False,
        nativeNamesAreNotGeometricMapping=True,finalStructuralApproval=False)
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(protectedSources=len(preserved),projectsPreserved=len(projects),diameters=len(rows))))

def archive():
    for p in OUT.iterdir():
        if p.is_file() and p.suffix in {'.json','.txt','.jpg'} and 'manifesto' not in p.name:
            shutil.copyfile(p,HERE/p.name)
    shutil.copyfile(HERE/'LEIA-ME-R150.md',OUT/'LEIA-ME-R150.md')
    (HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    files=[dict(path=p.name,sha256=sha(p)) for p in sorted(HERE.iterdir()) if p.is_file() and 'manifesto' not in p.name]
    for folder in (HERE,OUT):(folder/'R150-manifesto.json').write_text(json.dumps(files,indent=2),encoding='utf-8')

if __name__=='__main__':main();archive()

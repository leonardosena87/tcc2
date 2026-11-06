"""Consolida documentos nativos e a triagem auxiliar sem modificar fontes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from zipfile import ZipFile

W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
FIELDS=('Md','fiss','Vd','VRd2','Td','TRd2')


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def read_report(path):
    with ZipFile(path) as z:
        root=ET.fromstring(z.read('word/document.xml'))
    text='\n'.join(''.join(p.itertext()) for p in root.findall('.//'+W+'p'))
    if 'fck = 25.00 MPa' not in text or 'Cobrimento = 3.00 cm' not in text:
        raise ValueError('Material ou cobrimento divergente no relatorio')
    values={k:[float(v) for v in re.findall(r'(?<!\w)'+k+r'\s*=\s*([-+]?\d+(?:\.\d+)?)',text)] for k in FIELDS}
    if any(not a for a in values.values()):raise ValueError('Campo nativo ausente')
    return dict(file=path.name,sha256=sha(path),fields=values)


def main(root):
    reports={
        'CAD-V1':read_report(root/'CAD-V1-N0-calculo-detalhado.docx'),
        'BIM-V1':read_report(root/'BIM-V1-N0-calculo-detalhado.docx'),
        'CAD-cobertura':read_report(root/'CAD-V13_1-calculo-detalhado.docx'),
        'BIM-cobertura':read_report(root/'BIM-V3-calculo-detalhado.docx')}
    differences={}
    for item in ('V1','cobertura'):
        a,b=reports['CAD-'+item]['fields'],reports['BIM-'+item]['fields'];rows=[]
        for field in FIELDS:
            if len(a[field])!=len(b[field]):raise ValueError('Quantidade de campos divergente')
            for i,(x,y) in enumerate(zip(a[field],b[field],strict=True),1):
                if x!=y:rows.append(dict(field=field,occurrence=i,CAD=x,BIM=y,difference=abs(x-y)))
        differences[item]=rows
    if reports['CAD-V1']['fields']['Md']!=[12.,12.,12.] or reports['BIM-V1']['fields']['Md']!=[12.,12.,12.]:
        raise ValueError('Minimo12 nao confirmado nos tres pontos da V1')
    triage=json.loads((root/'R226-triagem-V1-minimo12.json').read_text(encoding='utf-8'))
    local=root.parent/'H03-R224-FECHAMENTO-DETALHES-NAO-EXECUTAR'
    audit=json.loads((local/'R224-integridade.json').read_text(encoding='utf-8'))
    sources=[]
    for row in audit['projects']:
        path=local/row['path']
        if sha(path)!=row['sha256']:raise ValueError('PRJ R224 mudou na consulta')
        with ZipFile(path) as z:
            if z.testzip():raise ValueError('CRC do projeto invalido')
        sources.append(dict(branch=row['branch'],path=str(path),sha256=row['sha256'],unchanged=True,crc='OK'))
    out=dict(revision='R226',nativeReports=reports,nativeFieldsDifferences=differences,
        V1MinimumConfirmedKNm=12,
        V1AuxiliaryLinearIndex={b:triage[b]['governing']['additionalConservativeLinearIndex'] for b in ('CAD','BIM')},
        oldFourCornerModelWith12Index={b:triage[b]['maxOldFourBarIndexWith12KNm'] for b in ('CAD','BIM')},
        V1VisualDeflectionEnvelopeDisplayed=dict(CAD='0.00',BIM='0.00',unit='cm',roundedDisplayNotExactZero=True),
        coverBIMVisualDeflectionEnvelopeDisplayed=dict(value='-0.11',unit='cm',CADObservedThisRevision=False),
        nativeProjects=sources,newFullProcessingPerformed=False,
        coversWarning08Resolved=False,V1Warning19Resolved=False,
        connectionsAnchorageAndFullELSApproved=False,fullVerificationComplete=False)
    (root/'R226-consolidacao.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k in ('nativeFieldsDifferences','V1AuxiliaryLinearIndex','V1MinimumConfirmedKNm')}))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);args=ap.parse_args();main(args.root)

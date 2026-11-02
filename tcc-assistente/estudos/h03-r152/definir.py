"""Define 17 espelhos como opção atual e gera perfil de estudo independente."""
import hashlib
import importlib.util
import json
import shutil
import sys
from datetime import datetime,timezone
from pathlib import Path
from time import perf_counter

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R152-17-ESPELHOS-NAO-EXECUTAR')
CURRENT=Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
spec=importlib.util.spec_from_file_location('r144',HERE.parent/'h03-r144/estudar_escada.py')
r144=importlib.util.module_from_spec(spec);spec.loader.exec_module(r144)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def profile(a,landing):
    x=0.;z=a['finishedGroundM'];points=[(x,z)];risers=[]
    n=a['totalRisers'];lower=a['lowerFlightRisers'];p=a['treadHypothesisM'];e=a['uniformRiserM']
    for i in range(1,n+1):
        before=z;z=a['finishedGroundM']+i*e
        points.append((x,z));risers.append(dict(number=i,xM=x,bottomM=before,topM=z))
        if i==lower:x+=landing;points.append((x,z))
        elif i<n:x+=p;points.append((x,z))
    return points,risers

def main():
    if OUT.exists() or CURRENT.exists():raise FileExistsError('Definição existente: preservar e versionar antes de substituir')
    tick=perf_counter();start=datetime.now(timezone.utc).isoformat()
    basep=HERE.parent/'h03-r147/R147-planta.json';refp=HERE.parent/'h03-r68/R68-referencia-arquitetonica-estudo.json'
    base=json.loads(basep.read_text(encoding='utf-8'));ref=json.loads(refp.read_text(encoding='utf-8'))
    m=base['graphicalMeasurementsM'];a=r144.alternative(17,8)
    pts,risers=profile(a,m['landingDepth'])
    scale=base['pdfUnitsPerM'];origin=ref['coordinateSystem']['upperOriginPdf']
    front=(origin['y']-1494.8)/scale
    arrival=front+m['landingDepth']+a['upperTreadRunM']
    doors=[]
    for floor in ref['floors']:
        if floor['id']!='S':continue
        for o in floor['openings']:
            if o['id']=='S-P3-01':
                low,high=sorted([o['y'],o['y2']])
                doors.append(dict(id=o['id'],openingYMinM=low,openingYMaxM=high,
                    arrivalWithinLongitudinalOpeningRange=low<arrival<high,
                    significance='Triagem da faixa da porta na lateral do lance superior; conferir faces e cortes, não é colisão 3D automaticamente provada.'))
    data=dict(revision='H03/R152',createdAtUtc=datetime.now(timezone.utc).isoformat(),
        userDecision=dict(exactText='coloque com 17 espelhos',
            adoptedForCurrentStudy=True,configuration='U com dois lances retos e patamar',
            supersedesStudyOptions=['R149: 18 espelhos com patamar','R151: 18 espelhos com compensados'],
            priorPreserveWallsDoorsFacadeAndFinishedFloorsStillApplies=True),
        geometry=a,landingDepthGraphicalReferenceM=m['landingDepth'],
        sources=[dict(path=str(p),sha256=sha(p)) for p in (basep,refp)],
        fit=dict(extraUpperRunM=a['upperTreadRunM']-m['upperTreadRun'],
            hallRemainingIfLandingAndSouthWallPreservedM=m['hallDepth']-(a['upperTreadRunM']-m['upperTreadRun']),
            landingRemainingIfHallPreservedM=m['landingDepth']-(a['upperTreadRunM']-m['upperTreadRun']),
            arrivalLocalYM=arrival,doorScreening=doors,placementResolved=False,
            automaticHallOrLandingReductionAuthorized=False),
        profile=dict(description='Perfil acabado desdobrado; não é corte espacial da escada em U.',
            pointsM=pts,risers=risers,notStructuralWaistGeometry=True),
        cadProfileIsIndependentStudyDrawing=True,nativeRevitAutoCadEberickProjectsEdited=False,
        newLoadsApplied=False,headroomVerified=False,finalStructuralOrNormativeApproval=False)
    OUT.mkdir();(OUT/'R152-escada17.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    draw(data);dxf(pts)
    for s in data['sources']:assert sha(Path(s['path']))==s['sha256']
    (OUT/'R152-tempo-script.json').write_text(json.dumps(dict(startUtc=start,endUtc=datetime.now(timezone.utc).isoformat(),
        durationMs=(perf_counter()-tick)*1000,scope='execução inicial de cálculo e geração; não esforço total nem tempo de fluxo'),ensure_ascii=False,indent=2),encoding='utf-8')
    CURRENT.write_text(json.dumps(dict(activeRevision='H03/R152',activeChoice='17 espelhos; U com patamar',
        definitionPath=str(OUT/'R152-escada17.json'),definitionSha256=sha(OUT/'R152-escada17.json'),
        nativePlacementResolved=False,nativeProjectsUpdated=False),ensure_ascii=False,indent=2),encoding='utf-8')
    archive()
    print(json.dumps(dict(risers=17,lower=8,upper=9,riserM=a['uniformRiserM'],landingM=a['proposedFinishedLandingM'],extraRunM=data['fit']['extraUpperRunM'])))

def draw(data):
    a=data['geometry'];pts=data['profile']['pointsM'];k=116
    mapped=' '.join(f'{65+x*k:.3f},{610-(z-.22)*k:.3f}' for x,z in pts)
    s=['<svg xmlns="http://www.w3.org/2000/svg" width="1220" height="740" viewBox="0 0 1220 740">',
       '<rect width="1220" height="740" fill="#f3f6f8"/><g font-family="Arial,sans-serif" fill="#173246">',
       '<text x="28" y="38" font-size="26" font-weight="bold">Escada · definição atual com 17 espelhos</text>',
       '<text x="28" y="70" font-size="18">Dois lances retos em U + patamar · pisos acabados +0,22 e +3,25 m preservados</text>',
       '<rect x="28" y="100" width="1164" height="540" rx="12" fill="white" stroke="#c6d3dc"/>',
       '<text x="50" y="136" font-size="20" font-weight="bold">Perfil acabado desdobrado (não é corte espacial)</text>',
       f'<polyline points="{mapped}" fill="none" stroke="#1b786b" stroke-width="3"/>']
    for r in data['profile']['risers']:
        x=65+r['xM']*k;y=610-(r['topM']-.22)*k
        s.append(f'<text x="{x+3}" y="{y-6}" font-size="11">{r["number"]}</text>')
    for x,z,label in [(0,.22,'+0,220 m'),(a['lowerTreadRunM'],a['proposedFinishedLandingM'],'+1,646 m'),(pts[-1][0],3.25,'+3,250 m')]:
        s.append(f'<text x="{65+x*k}" y="{635-(z-.22)*k}" font-size="16">{label}</text>')
    labels=['17 espelhos iguais: 17,8235 cm','1º lance: 8 espelhos / 7 pisadas','2º lance: 9 espelhos / 8 pisadas','Pisada adotada para estudo: 28 cm','Lances: 1,96 m / 2,24 m','Patamar acabado: +1,6459 m','Altura do patamar cai cerca de 5,4 cm']
    for i,line in enumerate(labels):s.append(f'<text x="760" y="{194+i*38}" font-size="18">{line}</text>')
    s += ['<text x="28" y="677" font-size="21" font-weight="bold" fill="#a34a20">ENCAIXE PENDENTE: lance superior precisa de aproximadamente 28 cm adicionais.</text>',
        '<text x="28" y="709" font-size="17">Paredes e portas preservadas como restrição · não se reduziu hall ou patamar automaticamente.</text>',
        '<text x="28" y="733" font-size="15">Perfil de estudo independente; sem lançamento de cargas ou alterações nos modelos. NÃO EXECUTAR.</text></g></svg>']
    raw='\n'.join(s);(OUT/'R152-escada17-perfil.svg').write_text(raw,encoding='utf-8')
    sys.path.insert(0,'D:/TCC/work/pdf-deps');import pymupdf
    pymupdf.open(stream=raw.encode(),filetype='svg')[0].get_pixmap().save(str(OUT/'R152-escada17-perfil.png'))

def dxf(pts):
    lines=['0','SECTION','2','HEADER','9','$ACADVER','1','AC1015','9','$INSUNITS','70','6','0','ENDSEC','0','SECTION','2','ENTITIES']
    for a,b in zip(pts,pts[1:]):
        lines += ['0','LINE','8','TCC_ESTUDO_ESCADA17_NAO_EXECUTAR','10',f'{a[0]:.12f}','20',f'{a[1]:.12f}','30','0','11',f'{b[0]:.12f}','21',f'{b[1]:.12f}','31','0']
    lines += ['0','TEXT','8','TCC_AVISO','10','0','20','3.65','30','0','40','0.12','1','PERFIL DESDOBRADO - 17 ESPELHOS - ESTUDO NAO EXECUTAR','0','ENDSEC','0','EOF']
    (OUT/'R152-escada17-perfil.dxf').write_text('\n'.join(lines)+'\n',encoding='ascii')

def archive():
    for p in OUT.iterdir():
        if p.is_file() and 'manifesto' not in p.name:shutil.copyfile(p,HERE/p.name)
    shutil.copyfile(HERE/'LEIA-ME-R152.md',OUT/'LEIA-ME-R152.md')
    (HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    manifest=[dict(path=p.name,sha256=sha(p)) for p in sorted(HERE.iterdir()) if p.is_file() and 'manifesto' not in p.name]
    for folder in (HERE,OUT):(folder/'R152-manifesto.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

if __name__=='__main__':main()

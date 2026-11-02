"""Reavalia 18 espelhos e prepara alternativas de encaixe, sem alterar a autoria."""
import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R149-18-ESPELHOS-NAO-EXECUTAR')
spec=importlib.util.spec_from_file_location('r144',HERE.parent/'h03-r144/estudar_escada.py')
r144=importlib.util.module_from_spec(spec);spec.loader.exec_module(r144)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def evaluate(tread,old_run,old_landing,old_hall):
    a=r144.alternative(18,9,tread=tread)
    extra=a['upperTreadRunM']-old_run
    return dict(geometry=a,extraRunM=extra,landingIfHallPreservedM=old_landing-extra,
                hallIfLandingPreservedM=old_hall-extra,
                planFitsWithoutChangingHallOrLanding=abs(extra)<1e-9)


def main():
    if OUT.exists():raise FileExistsError(OUT)
    tick=perf_counter();start=datetime.now(timezone.utc).isoformat()
    basep=HERE.parent/'h03-r147/R147-planta.json'
    base=json.loads(basep.read_text(encoding='utf-8'))
    measures=base['graphicalMeasurementsM']
    old_run,old_landing,old_hall=[measures[k] for k in ('upperTreadRun','landingDepth','hallDepth')]
    options={str(p):evaluate(p,old_run,old_landing,old_hall) for p in (.28,.30)}
    legal=Path('D:/TCC/work/r149-escada18/Lei_1481-2007_Anexos.pdf')
    sys.path.insert(0,'D:/TCC/work/pdf-deps')
    import pymupdf as f
    doc=f.open(legal)
    assert 'uso coletivo' in doc[92].get_text() and '0,63m' in doc[92].get_text()
    assert 'mesma unidade' in doc[95].get_text()
    ref=HERE.parent/'h03-r68/R68-referencia-arquitetonica-estudo.json'
    arq=json.loads(ref.read_text(encoding='utf-8'))
    ground_origin=arq['coordinateSystem']['upperOriginPdf']
    y_front=(ground_origin['y']-1494.8)/base['pdfUnitsPerM']
    proposed=dict(treadM=.30,flightTreadRunM=2.40,landingDepthM=.95,hallDepthM=.95,
                  totalLengthM=4.30,existingTotalLengthM=measures['totalClearNorthSouth'],
                  extensionM=4.30-measures['totalClearNorthSouth'],clearWidthRetainedGraphicallyM=measures['stairwellWidth'],
                  localYFrontM=y_front,localYNorthM=y_front+4.30,
                  upperLastRiserLocalYM=y_front+.95+2.40,
                  status='PROPOSTA GEOMETRICA PARA REVISAO; NAO APROVADA OU APLICADA',
                  landingAndHallDepthsAreStudyHypothesesNotLegalMinima=True)
    openings=next(fl for fl in arq['floors'] if fl['id']=='S')['openings']
    affected=[dict(id=o['id'],x=o['x'],yMin=min(o['y'],o['y2']),yMax=max(o['y'],o['y2']),
                   intersectsArrivalBoundary=min(o['y'],o['y2'])<proposed['upperLastRiserLocalYM']<max(o['y'],o['y2']))
              for o in openings if o['id'] in {'S-P2-01','S-P3-01'}]
    result=dict(revision='H03/R149',createdAtUtc=datetime.now(timezone.utc).isoformat(),
        userDecision=dict(exactText='continue, reavaliar 18 espelhos',effect='Estudo atual passa a 18; historico de 17 preservado',
                          permission='Reavaliacao, nao aprovacao de alteracoes de paredes, portas ou arquitetura executiva'),
        sources=[dict(path=str(p),sha256=sha(p)) for p in (basep,ref,legal)],
        finishedFloorLevelsPreservedM=[.22,3.25],options=options,
        forcedFitAtExistingRun=dict(treadM=old_run/8,
            twoRisersPlusTreadM=2*(3.03/18)+old_run/8,
            adopted=False,reason='Nao se reduz pisada para mascarar falta de espaco.'),
        proposedExpandedLayout=proposed,doorsRequiringReview=affected,
        additionalArchitectureConflicts=['W17 no eixo Y3,90 e W16 no eixo X5,45 ocupam parte da caixa ampliada; rever contornos do hall/suite.',
            'Portas S-P2-01 e S-P3-01 atravessam a nova linha de chegada de estudo Y≈3,424m; acessos e giro exigem redesenho.',
            'Se a escada/patamar superior mudar de posicao, L5 e os apoios estruturais precisam ser revistos nos dois fluxos.'],
        legislativeReading=dict(url='https://www.pmvc.ba.gov.br/wp-content/uploads/Lei_1481-2007_Anexos.pdf',
            downloadSucceeded=True,pdfPagesOneBased=[92,93,96],printedPages=[154,155,158],
            referenceForCollectiveStairs=dict(pMinStrictM=.28,pMaxStrictM=.32,eMinStrictM=.16,eMaxStrictM=.18,
                                             twoEplusPMinStrictM=.63,twoEplusPMaxStrictM=.65),
            applicationToThisPrivateStairOrConsolidatedLegalValidityApproved=False,
            interpretation='M3 explicita uso publico/coletivo; nao se afirma incidencia automatica dos limites na escada interna unifamiliar. p30 avaliado como hipotese geometrica adicional.'),
        structuralLandingPlaneM=None,waistThicknessM=None,headroomVerified=False,
        newStairNativeLoadsApplied=False,modelsOrMonographEdited=False,finalStructuralApproval=False,
        conclusion='18 espelhos fecha a altura com simetria 9+9, mas nao resolve o encaixe atual. p28 exige +28cm; p30 exige +44cm de lance. Proposta p30 com hall/patamar .95 exige caixa +≈55cm e revisao de paredes/portas.')
    OUT.mkdir()
    (OUT/'R149-estudo18.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'R149-decisao-usuario.json').write_text(json.dumps(result['userDecision'],ensure_ascii=False,indent=2),encoding='utf-8')
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1240" height="700" viewBox="0 0 1240 700">',
         '<rect width="1240" height="700" fill="#f3f6f8"/><g font-family="Arial,sans-serif" fill="#173246">',
         '<text x="28" y="36" font-size="25" font-weight="bold">Escada · reavaliação com 18 espelhos</text>',
         '<text x="28" y="65" font-size="17">9 + 9 espelhos de 16,833 cm · patamar acabado +1,735 m · pisos +0,22 / +3,25 m mantidos</text>']
    cards=[('Traçado atual',old_hall,old_run,old_landing,'#3c688d','Referência gráfica'),
           ('18 espelhos · pisada 28 cm',old_hall,2.24,old_landing-(2.24-old_run),'#af5b24','Patamar reduzido: não adotado'),
           ('Proposta · pisada 30 cm',.95,2.40,.95,'#166b64','Exige rever paredes e portas')]
    for i,(title,ha,run,la,c,note) in enumerate(cards):
        x=28+406*i;y=145;k=73;w=146
        svg.extend([f'<rect x="{x}" y="90" width="386" height="477" rx="12" fill="white" stroke="#c6d3dc"/>',
            f'<text x="{x+14}" y="122" font-size="19" font-weight="bold">{title}</text>',
            f'<rect x="{x+24}" y="{y}" width="{w}" height="{ha*k}" fill="#dbe9f3" stroke="{c}"/>',
            f'<rect x="{x+24}" y="{y+ha*k}" width="{w}" height="{run*k}" fill="#f4f7f9" stroke="{c}"/>',
            f'<line x1="{x+97}" y1="{y+ha*k}" x2="{x+97}" y2="{y+(ha+run)*k}" stroke="{c}" stroke-width="4"/>',
            f'<rect x="{x+24}" y="{y+(ha+run)*k}" width="{w}" height="{la*k}" fill="#f9e4ce" stroke="{c}"/>',
            f'<text x="{x+186}" y="{y+ha*k/2+5}" font-size="16">Hall ≈ {ha:.3f} m</text>',
            f'<text x="{x+186}" y="{y+(ha+run/2)*k}" font-size="16">Lances {run:.2f} m</text>',
            f'<text x="{x+186}" y="{y+(ha+run+la/2)*k+5}" font-size="15">Patamar ≈ {la:.3f} m</text>',
            f'<text x="{x+20}" y="492" font-size="15">Comprimento: {ha+run+la:.3f} m</text>',
            f'<text x="{x+20}" y="520" font-size="14" fill="{c}">{note}</text>'])
        if i==2:svg.append(f'<text x="{x+20}" y="545" font-size="15" font-weight="bold">Caixa precisa de ≈ 55 cm adicionais</text>')
    svg.extend(['<text x="28" y="605" font-size="18" font-weight="bold">18 espelhos fecha a altura; a caixa atual ainda precisa de revisão.</text>',
        '<text x="28" y="633" font-size="16">Proposta de 30 cm: 2e + p = 63,67 cm. É hipótese de estudo, sem aprovação normativa ou executiva.</text>',
        '<text x="28" y="667" font-size="16">Altura livre, patamar estrutural, apoios e cargas pendentes · nenhum arquivo de autoria foi alterado</text></g></svg>'])
    raw='\n'.join(svg)
    (OUT/'R149-reavaliacao18.svg').write_text(raw,encoding='utf-8')
    f.open(stream=raw.encode(),filetype='svg')[0].get_pixmap().save(str(OUT/'R149-reavaliacao18.png'))
    (OUT/'R149-tempo-script.json').write_text(json.dumps(dict(startUtc=start,endUtc=datetime.now(timezone.utc).isoformat(),
        durationMs=(perf_counter()-tick)*1000,notFlowOrWholeAiEffort=True),indent=2),encoding='utf-8')
    print(json.dumps(dict(riserM=3.03/18,landingM=1.735,extraRun28=options['0.28']['extraRunM'],proposal=proposed)))


if __name__=='__main__':main()

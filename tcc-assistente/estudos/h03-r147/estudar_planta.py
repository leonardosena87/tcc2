"""Triagem geométrica em planta da alternativa de escada autorizada na R144."""
import hashlib
import importlib.util
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Escada-H03-R147-PLANTA-NAO-EXECUTAR')
PDF = Path('D:/TCC/PROJETO ARQUITETONICO-A0.pdf')
spec = importlib.util.spec_from_file_location('r144', HERE.parent/'h03-r144/estudar_escada.py')
r144 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r144)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def redistribution(existing_run, landing, hall, required_run):
    if any(not math.isfinite(x) or x <= 0 for x in (existing_run, landing, hall, required_run)):
        raise ValueError('Medida inválida')
    extra = required_run - existing_run
    return dict(extraRunM=extra, keepHallLandingDepthM=landing-extra,
                keepLandingHallDepthM=hall-extra,
                simultaneousPreservationPossible=abs(extra)<1e-9)


def main():
    if OUT.exists():
        raise FileExistsError(OUT)
    tick=perf_counter(); started=datetime.now(timezone.utc).isoformat()
    ref=HERE.parent/'h03-r68/R68-referencia-arquitetonica-estudo.json'
    datum=json.loads(ref.read_text(encoding='utf-8'))
    assert sha(PDF)==datum['sourceSha256']
    scale=datum['coordinateSystem']['pdfUnitsPerM']
    sys.path.insert(0,'D:/TCC/work/pdf-deps')
    import pymupdf as f
    p=f.open(PDF)[0]
    lines=[]
    for d in p.get_drawings():
        if d.get('color') != (0.,0.,0.):
            continue
        for item in d['items']:
            if item[0]=='l':
                a,b=item[1:3]
                lines.append([float(a.x),float(a.y),float(b.x),float(b.y)])
    required=[(801.84,1332.56,915.36,1332.56),
              (915.36,1494.80,801.84,1494.80),
              (852.96,1282.16,919.68,1282.16),
              (801.84,1443.68,858.72,1443.68)]
    selected=[]
    for wanted in required:
        match=[line for line in lines if max(abs(a-b) for a,b in zip(line,wanted))<.002]
        if not match:
            raise ValueError('Linha de referência não encontrada: '+str(wanted))
        selected.append(match[0])
    # Valores gráficos quantizados no PDF, não levantamento nem tolerância executiva.
    north,top,landing_y,front=1282.16,1332.56,1443.68,1494.80
    run=(landing_y-top)/scale
    landing=(front-landing_y)/scale
    hall=(top-north)/scale
    alt=r144.alternative(17,8)
    cases=redistribution(run,landing,hall,alt['upperTreadRunM'])
    y_new_top=landing_y-alt['upperTreadRunM']*scale
    y_new_landing=top+alt['upperTreadRunM']*scale
    result=dict(revision='H03/R147',createdAtUtc=datetime.now(timezone.utc).isoformat(),
                sources=[dict(path=str(s),sha256=sha(s)) for s in (PDF,ref,HERE.parent/'h03-r144/R144-decisao-usuario.json')],
                userAuthorizedAlternative=alt, pdfUnitsPerM=scale, selectedPlanLinesPdf=selected,
                graphicalMeasurementsM=dict(stairwellWidth=(915.36-801.84)/scale,
                    flightStripWidth=(853.44-801.84)/scale, upperTreadRun=run,
                    landingDepth=landing, hallDepth=hall, totalClearNorthSouth=(front-north)/scale),
                cases=cases, proposedPdfCoordinates=dict(keepLandingTopY=y_new_top,keepHallLandingStartY=y_new_landing),
                conclusions=['A alternativa mantém as cotas acabadas, mas ainda não cabe preservando simultaneamente hall e patamar desenhados.',
                             'Se mantiver o hall, a profundidade gráfica do patamar cai para cerca de 0,622 m.',
                             'Se mantiver o patamar, a profundidade gráfica do hall cai para cerca de 0,609 m, exigindo rever portas/circulação.',
                             'Não se aprovou nenhuma dessas redistribuições nem se alterou arquitetura ou modelo nativo.'],
                legalReview=dict(officialMunicipalEntry='https://www.pmvc.ba.gov.br/alvara-simplificado/',
                    annexPdf='https://www.pmvc.ba.gov.br/wp-content/uploads/Lei_1481-2007_Anexos.pdf',
                    annexRetrieval='Falha 502 na ferramenta web; trecho indexado não estabelece aplicação final à escada privativa. Não se fixou mínimo legal neste estudo.'),
                headroomVerified=False, finalStructuralApproval=False, nativeGeometryOrLoadsApplied=False,
                limits=['Linhas selecionadas por leitura visual prévia; confirmação de existência não é reconhecimento automático completo de arquitetura.',
                        'Largura de faixa gráfica não certifica largura útil após corrimãos, acabamento e tolerâncias.',
                        'A relação n−1 pisadas usa patamar/piso como última subida; conferir faces e apoio efetivos no lançamento.',
                        'Acabamento do patamar, espessura resistente e apoios continuam indefinidos.'])
    OUT.mkdir()
    (OUT/'R147-planta.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="670" viewBox="0 0 1200 670">',
         '<rect width="1200" height="670" fill="#f4f6f8"/><g font-family="Arial,sans-serif" fill="#173146">',
         '<text x="28" y="38" font-size="25" font-weight="bold">Escada de 17 espelhos · conferência em planta</text>',
         '<text x="28" y="68" font-size="16">Patamar acabado +1,646 m · pisadas de 28 cm · esquema próprio derivado da arquitetura</text>']
    cards=[('Desenho de referência',hall,run,landing,'#37618a'),
           ('A: manter o hall',hall,alt['upperTreadRunM'],cases['keepHallLandingDepthM'],'#af5a21'),
           ('A: manter o patamar',cases['keepLandingHallDepthM'],alt['upperTreadRunM'],landing,'#a33147')]
    for i,(title,ha,ru,la,color) in enumerate(cards):
        x=28+392*i;y=142;k=83;w=166
        svg += [f'<rect x="{x}" y="92" width="370" height="480" rx="12" fill="white" stroke="#c7d1d9"/>',
                f'<text x="{x+18}" y="122" font-size="20" font-weight="bold">{title}</text>',
                f'<rect x="{x+24}" y="{y}" width="{w}" height="{ha*k}" fill="#d6e5f2" stroke="#547c9d"/>',
                f'<rect x="{x+24}" y="{y+ha*k}" width="{w}" height="{ru*k}" fill="#f5f7fa" stroke="{color}"/>',
                f'<line x1="{x+107}" y1="{y+ha*k}" x2="{x+107}" y2="{y+(ha+ru)*k}" stroke="#455d6e" stroke-width="5"/>',
                f'<rect x="{x+24}" y="{y+(ha+ru)*k}" width="{w}" height="{la*k}" fill="#fbe2ca" stroke="{color}"/>',
                f'<text x="{x+204}" y="{y+ha*k/2+5}" font-size="16">Hall ≈ {ha:.3f} m</text>',
                f'<text x="{x+204}" y="{y+(ha+ru/2)*k}" font-size="16">Lance {ru:.2f} m</text>',
                f'<text x="{x+204}" y="{y+(ha+ru+la/2)*k+5}" font-size="15">Patamar ≈ {la:.3f} m</text>',
                f'<text x="{x+24}" y="490" font-size="15">Caixa: largura gráfica ≈ 2,00 m</text>',
                f'<text x="{x+24}" y="519" font-size="15">Faixas dos lances ≈ 0,91 m</text>',
                f'<text x="{x+24}" y="548" font-size="14" fill="{color}">{"Referência com sete intervalos gráficos" if i==0 else "Redistribuição ainda não aprovada"}</text>']
    svg += ['<text x="28" y="607" font-size="17" font-weight="bold">O lance superior exige aproximadamente 28 cm adicionais.</text>',
            '<text x="28" y="635" font-size="16">Rever encaixe, portas, altura livre e apoios antes do lançamento · NÃO EXECUTAR</text></g></svg>']
    raw='\n'.join(svg)
    (OUT/'R147-encaixe-escada.svg').write_text(raw,encoding='utf-8')
    f.open(stream=raw.encode(),filetype='svg')[0].get_pixmap().save(str(OUT/'R147-encaixe-escada.png'))
    (OUT/'R147-tempo-script.json').write_text(json.dumps(dict(startUtc=started,endUtc=datetime.now(timezone.utc).isoformat(),
        durationMs=(perf_counter()-tick)*1000,notFlowOrWholeAiEffort=True),indent=2),encoding='utf-8')
    print(json.dumps(result['graphicalMeasurementsM']|cases))


if __name__=='__main__':
    main()

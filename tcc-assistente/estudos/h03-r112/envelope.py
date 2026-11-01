"""Triagem dimensional do corte BB, sem escolher produto ou alterar arquitetura."""
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

ROOT = Path('D:/TCC')
OUT = ROOT / 'outputs/Reservatorio-H03-R112-ENVELOPE-NAO-EXECUTAR'
PDF_SHA = '3a57561f03e2c0e92964b19e577a02939b04fc93cdf1ef27cad6f79ad2deb12d'


def linear_height(x, line):
    (x0, h0), (x1, h1) = line
    if not all(math.isfinite(v) for v in [x, x0, h0, x1, h1]) or x1 <= x0 or not x0 <= x <= x1:
        raise ValueError('Ponto fora do trecho medido ou reta invalida')
    return h0 + (h1-h0)*(x-x0)/(x1-x0)


def envelope(center_x, width, tank_height, line, member_reduction=None):
    if not all(math.isfinite(v) for v in [center_x, width, tank_height]) or width <= 0 or tank_height <= 0:
        raise ValueError('Envelope invalido')
    if member_reduction is not None and (not math.isfinite(member_reduction) or member_reduction < 0):
        raise ValueError('Reducao invalida')
    left, right = center_x-width/2, center_x+width/2
    minimum = min(linear_height(left, line), linear_height(right, line))
    optimistic = minimum-tank_height
    return {'xRangeM': [left, right], 'minimumDrawnContourHeightAboveBaseM': minimum,
            'tankHeightM': tank_height, 'optimisticVerticalClearanceM': optimistic,
            'memberReductionM': member_reduction,
            'effectiveClearanceM': None if member_reduction is None else optimistic-member_reduction,
            'installationApproved': False}


def main():
    start = perf_counter()
    start_utc = datetime.now(timezone.utc).isoformat()
    sys.path.insert(0, str(ROOT/'work/pdf-deps'))
    import pymupdf as fitz
    architecture = ROOT/'PROJETO ARQUITETONICO-A0.pdf'
    if hashlib.sha256(architecture.read_bytes()).hexdigest() != PDF_SHA:
        raise ValueError('Arquitetura diferente da referencia')
    if OUT.exists():
        raise FileExistsError('Nao substituir estudo anterior')
    r71_path = ROOT/'outputs/Reservatorio-H03-R71-ALTERNATIVAS-NAO-APLICADO/R71-reservatorio-alternativas.json'
    r71 = json.loads(r71_path.read_text(encoding='utf-8'))
    page = fitz.open(architecture)[0]
    expected = [[1449.5999755859375, 1764.320068359375], [1609.6800537109375, 1748.239990234375]]
    candidates = []
    for d in page.get_drawings():
        if d['color'] != (0., 0., 0.):
            continue
        for item in d['items']:
            if item[0] != 'l':
                continue
            points = sorted([list(item[1]), list(item[2])])
            if all(abs(a-b)<0.001 for p, q in zip(points, expected) for a, b in zip(p, q)):
                candidates.append(points)
    if len(candidates) != 1:
        raise ValueError('Contorno inferior desenhado nao unico')
    # Registro horizontal pelo centro das paredes do abrigo, associado a P2/R60.
    x_left_pdf = (1434.0+1442.4000244140625)/2
    x_right_pdf = (1609.6800537109375+1618.0799560546875)/2
    x_scale = (x_right_pdf-x_left_pdf)/(9.65-6.55)
    base_y_pdf, parapet_y_pdf = 1816.4000244140625, 1742.719970703125
    y_scale = (base_y_pdf-parapet_y_pdf)/1.30
    line = [[6.55+(x-x_left_pdf)/x_scale, (base_y_pdf-y)/y_scale] for x, y in candidates[0]]
    if abs((line[1][1]-line[0][1])/(line[1][0]-line[0][0])-.1) > .002:
        raise ValueError('Inclinacao vetorial incompativel com leitura de10%')
    models = []
    for model in r71['models']:
        result = envelope(r71['candidateCenterM'][0], model['topXDimensionM'], model['heightWithLidM'], line)
        result.update(referenceId=model['id'], manufacturer=model['manufacturer'],
                      source=model['url'], historicalDimensionsFromR71=True,
                      studyServiceReserveM=.60,
                      studyReserveShortfallM=max(0, .60-result['optimisticVerticalClearanceM']),
                      upperEnvelopeIsPrismaticBoundingBox=True,
                      effectiveLidRemovalEnvelopeUnknown=True)
        models.append(result)
    low = next(m for m in models if m['referenceId']=='ref-retangular-baixa')
    max_center = r71['clearPlanHypothesisM'][2]-.60-1.23/2
    shifted = envelope(max_center, 1.23, .68, line)
    shifted['centerXM'] = max_center
    shifted['studySideReserveM'] = .60
    result = {'revision': 'H03/R112', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
              'architecture': {'path': str(architecture), 'sha256': PDF_SHA, 'pageOneBased': 1,
                               'section': 'BB', 'sourceCropLocal': str(ROOT/'work/r112-corte-BB.png')},
              'measurement': {'roofLowerDrawnContourPdf': candidates[0], 'baseYpdf': base_y_pdf,
                              'parapetTopYpdf': parapet_y_pdf, 'dimensionToParapetM': 1.30,
                              'sectionWallCentersPdfX': [x_left_pdf, x_right_pdf],
                              'assignedNominalWallAxesXM': [6.55, 9.65],
                              'pdfUnitsPerMhorizontal': x_scale, 'pdfUnitsPerMvertical': y_scale,
                              'roofLowerDrawnContourRelativeM': line,
                              'drawnRoofThicknessIsNotSixMmSheetSpecification': True,
                              'absoluteStructuralBaseElevationM': None,
                              'memberDepthsAndConnectionsResolved': False,
                              'dimension130IsUniformRoofClearance': False},
              'models': models, 'lowRectangularMovedTowardHighSideWithStudySideReserve': shifted,
              'sourceR71': {'path': str(r71_path), 'sha256': hashlib.sha256(r71_path.read_bytes()).hexdigest()},
              'manufacturerTechnicalDocument': {
                  'url': 'https://bakof.com.br//storage/produtos/4/arquivos/bfe0589dcc022783df21505d82813e26.pdf',
                  'localPath': str(ROOT/'work/r112/bakof-descritivo.pdf'),
                  'sha256': hashlib.sha256((ROOT/'work/r112/bakof-descritivo.pdf').read_bytes()).hexdigest(),
                  'page3VisuallyRead': True, 'lowModelDimensionsReconfirmed': True,
                  'tarePublishedInConsultedTable': False},
              'nativeLoadsApplied': False, 'architecturalHeightsChanged': False,
              'productChosen': False, 'finalStructuralApproval': False,
              'limits': ['Contorno arquitetonico e envelope de triagem, nao geometria executiva da telha/perfis.',
                         'Reserva superior0,60m e hipotese R71, nao exigencia normativa demonstrada.',
                         'Envelope de tanque e caixa envolvente; tampa/acesso/tubos nao modelados.',
                         'Folga efetiva desconhecida, pois perfil/ligacao permanecem indefinidos.',
                         'A correspondencia vertical da base com N2 segue pendente; nao usar N2+0,60 automaticamente.',
                         'Nao reduzir base/cobertura/folga para declarar compatibilidade sem justificacao.',
                         'Tara do reservatorio continua desconhecida; capacidade nao e seu peso proprio.']}
    OUT.mkdir()
    (OUT/'R112-envelope-reservatorio.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    draw(result)
    (OUT/'R112-tempo-script.json').write_text(json.dumps({'startUtc': start_utc,
        'endUtc': datetime.now(timezone.utc).isoformat(), 'durationMs': (perf_counter()-start)*1000,
        'scope': 'Extracao vetorial, aritmetica e desenho; nao pesquisa, autoria ou inferencia IA'}, indent=2), encoding='utf-8')
    print(json.dumps({'relativeRoofLineM': line, 'modelClearancesM': {m['referenceId']:m['optimisticVerticalClearanceM'] for m in models},
                      'lowMovedHighClearanceM': shifted['optimisticVerticalClearanceM'], 'nativeApplied': False}))


def draw(result):
    sys.path.insert(0, str(ROOT/'work/plot-deps'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    fig, axes = plt.subplots(1,2,figsize=(12,5), sharey=True)
    line = result['measurement']['roofLowerDrawnContourRelativeM']
    for ax, model in zip(axes, result['models']):
        xs, hs = zip(*line)
        ax.plot(xs, hs, color='#126477', lw=3, label='Contorno inferior desenhado da cobertura')
        ax.axhline(1.30, color='#69747c', ls=':', label='Topo da platibanda: +1,30 m')
        ax.axhline(0, color='#3c4c57', lw=2)
        left, right = model['xRangeM']; height=model['tankHeightM']
        ax.add_patch(Rectangle((left,0),right-left,height,facecolor='#c8e4ec',edgecolor='#126477'))
        ax.add_patch(Rectangle((left,height),right-left,.60,facecolor='#f9d6c9',edgecolor='#b04d32',linestyle='--',alpha=.7))
        ax.text((left+right)/2,height/2,'Envelope dimensional\ndo tanque',ha='center',va='center',fontsize=9)
        ax.text(.5,.94,'Faixa tracejada: reserva superior de 0,60 m',transform=ax.transAxes,
                ha='center',va='top',fontsize=8,color='#843b28',bbox={'facecolor':'white','edgecolor':'none','alpha':.9})
        ax.set_title(model['manufacturer']+' - referencia dimensional',fontsize=11)
        ax.set_xlim(6.55,9.65);ax.set_ylim(-.08,1.75);ax.set_xlabel('X nominal no estudo (m)')
        ax.grid(alpha=.15)
    axes[0].set_ylabel('Altura relativa acima da base desenhada (m)')
    fig.suptitle('H03/R112 | Reservatorio de 1.000 L sob cobertura inclinada',fontsize=14)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.5,.075),ncol=2,fontsize=9)
    fig.text(.5,.02,'Triagem por caixa envolvente. Sem perfis, ligacoes, tampa ou acesso modelados. Nao aprova instalacao.',ha='center',fontsize=9)
    fig.subplots_adjust(bottom=.24,top=.84,wspace=.12)
    fig.savefig(OUT/'R112-envelope-reservatorio.png',dpi=180)
    fig.savefig(OUT/'R112-envelope-reservatorio.svg')
    svg = OUT/'R112-envelope-reservatorio.svg'
    svg.write_text('\n'.join(s.rstrip() for s in svg.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8')
    plt.close(fig)


if __name__ == '__main__':
    main()

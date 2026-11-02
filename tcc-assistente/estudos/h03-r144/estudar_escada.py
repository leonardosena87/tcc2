"""Confronta cotas da escada e prepara alternativas; não altera arquitetura/modelos."""
import hashlib
import json
import math
import sys
from datetime import datetime,timezone
from pathlib import Path
from time import perf_counter

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R144-COMPATIBILIZACAO-NAO-EXECUTAR')
PDF=Path('D:/TCC/PROJETO ARQUITETONICO-A0.pdf')
NORM=Path('D:/TCC/materiais/normas/ABNT NBR 6120-2019.pdf')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def alternative(total,lower,ground=.22,upper=3.25,old_landing=1.70,tread=.28):
    if any(not math.isfinite(x) for x in [ground,upper,old_landing,tread]) or upper<=ground or tread<=0:
        raise ValueError('Cotas/pisada inválidas')
    if not isinstance(total,int) or not isinstance(lower,int) or not 2<=lower<=total-2:
        raise ValueError('Número de espelhos inválido')
    e=(upper-ground)/total
    return {'totalRisers':total,'lowerFlightRisers':lower,'upperFlightRisers':total-lower,
        'uniformRiserM':e,'finishedGroundM':ground,'finishedUpperM':upper,
        'proposedFinishedLandingM':ground+lower*e,'landingChangeM':ground+lower*e-old_landing,
        'treadHypothesisM':tread,'twoRisersPlusTreadM':2*e+tread,
        'lowerTreadsIfLandingIsLastRiser':lower-1,'upperTreadsIfFloorIsLastRiser':total-lower-1,
        'lowerTreadRunM':(lower-1)*tread,'upperTreadRunM':(total-lower-1)*tread,
        'nativeGeometryApplied':False,'acceptedArchitectureChange':False,
        'footprintHeadroomStructuralCapacityOrAccessibilityApproved':False}


def main():
    started=datetime.now(timezone.utc).isoformat();tick=perf_counter()
    if OUT.exists():raise FileExistsError(OUT)
    if sha(PDF)!='3a57561f03e2c0e92964b19e577a02939b04fc93cdf1ef27cad6f79ad2deb12d':raise ValueError('Arquitetura diferente')
    sys.path.insert(0,'D:/TCC/work/pdf-deps')
    import pymupdf as f
    page=f.open(PDF)[0]
    words=page.get_text('words',clip=f.Rect(150,1730,710,2240))
    selected={t:[list(w[:4]) for w in words if w[4]==t] for t in ['0,22','1,70','3,25','185','28']}
    if any(not x for x in selected.values()):raise ValueError('Referência gráfica ausente')
    norm=f.open(NORM)
    p27=norm[26].get_text();p32=norm[31].get_text();p33=norm[32].get_text();p34=norm[33].get_text()
    for needle,text in [('Escadas e',p27),('2,5 kN',p32),('1,1 m',p33),('Escadas privativas',p34)]:
        if needle not in text:raise ValueError('Referência normativa ausente')
    alts=[alternative(17,8),alternative(18,9)]
    original={'finishedGroundM':.22,'finishedLandingM':1.70,'finishedUpperM':3.25,
        'lowerRiseM':1.48,'upperRiseM':1.55,'dimensionRiserInterpretedVisuallyM':.185,
        'rawPdfRiserText':'185','superscriptHalfCentimetreNot185Centimetres':True,
        'dimensionTreadM':.28,'riseDividedByAnnotatedRiser':3.03/.185,
        'lowerRisersAtAnnotatedRiser':1.48/.185,'upperRisersAtAnnotatedRiser':1.55/.185,
        'allRisersSameAsAnnotatedClosesLevels':False,'dimensionReadingNotSurvey':True}
    OUT.mkdir()
    result={'revision':'H03/R144','createdAtUtc':datetime.now(timezone.utc).isoformat(),
        'sources':[{'path':str(p),'sha256':sha(p)} for p in [PDF,NORM]],
        'pdfPageOneBased':1,'section':'AA','labelPositionsPdf':selected,'architecture':original,
        'alternatives':alts,'normativeLoadReference':{'standard':'ABNT NBR 6120:2019, exemplar local',
            'table10PdfPage':27,'printedPage':21,'privateResidentialStairLiveKNm2':2.5,
            'footnoteTOnPdfPage32':{'cantileverAlternatingCasesRequiredIfApplicable':True,
                'isolatedStepPointKN':2.5,'pointCaseSeparateFromUniformLiveCase':True},
            'barrierHorizontalKNm':1.0,'barrierLoadHeightAboveFinishedFloorM':1.1,
            'barrierTable12PdfPage':34,'applicationRulePdfPage':33,
            'noStructuralNativeApplicationOrFullNormComplianceAsserted':True},
        'nativeModellingSources':['https://suporte.altoqi.com.br/hc/pt-br/articles/115002281074',
            'https://suporte.altoqi.com.br/hc/pt-br/articles/115003584493'],
        'unresolved':['Escolha geométrica e referência de acabamentos do patamar.',
            'Contagem e posição executiva dos espelhos/pisadas e folga de circulação/altura livre.',
            'Largura útil, espessura estrutural e peso próprio; não adotar os acabamentos como seção resistente.',
            'Apoio inferior, vinculação ao hall e eventual patamar autoportante com continuidade comprovada.',
            'Guarda-corpo/peso/ancoragem e transferência de reações para o modelo integrado.'],
        'newStructuralLoadsApplied':False,'modelsOrMonographChanged':False,
        'finalStructuralApproval':False,'timingIsScriptOnlyNotResearchOrFlow':True}
    (OUT/'R144-escada.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    profiles=[('Cotas da arquitetura',1.70,'Espelho indicado: 18,5 cm','O desnível total não fecha com essa medida.'),
        ('Alternativa A · 17 espelhos',alts[0]['proposedFinishedLandingM'],'Espelho uniforme: 17,824 cm','Patamar: −5,41 cm em relação ao desenho.'),
        ('Alternativa B · 18 espelhos',alts[1]['proposedFinishedLandingM'],'Espelho uniforme: 16,833 cm','Patamar: +3,50 cm em relação ao desenho.')]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1260" height="500" viewBox="0 0 1260 500">',
        '<rect width="1260" height="500" fill="#f4f6f8"/><g font-family="Arial, sans-serif" fill="#172c3b">',
        '<text x="28" y="35" font-size="24" font-weight="bold">Escada · alternativas geométricas para revisão</text>',
        '<text x="28" y="62" font-size="15">Pisos acabados +0,22 m e +3,25 m preservados · esquema desdobrado, sem escala em planta</text>']
    for i,(title,z,desc,note) in enumerate(profiles):
        x=26+i*412;y=lambda v:350-(v-.22)*64
        svg.extend([f'<rect x="{x}" y="86" width="388" height="326" rx="12" fill="white" stroke="#c6d2db"/>',
            f'<text x="{x+18}" y="119" font-size="18" font-weight="bold">{title}</text>',
            f'<path d="M{x+25} {y(.22)} L{x+137} {y(z)} H{x+179} L{x+315} {y(3.25)} H{x+350}" fill="none" stroke="{["#a36223","#13796c","#345b9a"][i]}" stroke-width="4"/>',
            f'<text x="{x+18}" y="{y(.22)+22}" font-size="13">+0,22 m</text>',
            f'<text x="{x+120}" y="{y(z)-12}" font-size="14">+{z:.3f} m</text>',
            f'<text x="{x+278}" y="{y(3.25)-12}" font-size="13">+3,25 m</text>',
            f'<text x="{x+18}" y="385" font-size="14">{desc}</text>',
            f'<text x="{x+12}" y="437" font-size="13">{note}</text>'])
    svg.append('<text x="28" y="478" font-size="15" font-weight="bold">ESTUDO · sem mudança aprovada na arquitetura · sem dimensionamento ou carga nova aplicada</text></g></svg>')
    (OUT/'R144-alternativas-escada.svg').write_text('\n'.join(svg),encoding='utf-8')
    doc=f.open(stream='\n'.join(svg).encode(),filetype='svg')
    doc[0].get_pixmap().save(str(OUT/'R144-alternativas-escada.png'))
    (OUT/'R144-tempo-script.json').write_text(json.dumps({'startUtc':started,'endUtc':datetime.now(timezone.utc).isoformat(),
        'scriptDurationMs':(perf_counter()-tick)*1000,'notFlowOrWholeAiEffort':True},indent=2),encoding='utf-8')
    print(json.dumps({'architectureMismatch':True,'alternatives':alts,'nativeLoadsApplied':False}))

if __name__=='__main__':main()

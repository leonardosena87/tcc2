"""Relaciona níveis arquitetônicos desenhados, sem definir apoio do tanque."""
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Reservatorio-H03-R142-ALTIMETRIA-NAO-EXECUTAR')
PDF=Path('D:/TCC/PROJETO ARQUITETONICO-A0.pdf')
PDF_SHA='3a57561f03e2c0e92964b19e577a02939b04fc93cdf1ef27cad6f79ad2deb12d'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def altitude(datum_z,datum_y,target_y,scale):
    if not all(isinstance(v,(int,float)) and math.isfinite(v) for v in [datum_z,datum_y,target_y,scale]) or scale<=0:
        raise ValueError('Referência vertical inválida')
    return datum_z+(datum_y-target_y)/scale

def relation(base_z,reference_z):
    if reference_z is None:return {'referencePlaneM':None,'baseAboveReferenceM':None,'physicalPedestalHeightM':None}
    if not math.isfinite(reference_z):raise ValueError('Plano inválido')
    return {'referencePlaneM':reference_z,'baseAboveReferenceM':base_z-reference_z,
            'physicalPedestalHeightM':None}

def main():
    started=datetime.now(timezone.utc).isoformat();tick=perf_counter()
    if OUT.exists():raise FileExistsError(OUT)
    if sha(PDF)!=PDF_SHA:raise ValueError('PDF diferente da referência R112')
    sys.path.insert(0,'D:/TCC/work/pdf-deps')
    import pymupdf as fitz
    page=fitz.open(PDF)[0]
    ref_path=HERE.parent/'h03-r112/R112-envelope-reservatorio.json'
    ref=json.loads(ref_path.read_text(encoding='utf-8'))
    scale=ref['measurement']['pdfUnitsPerMvertical']
    base_y=ref['measurement']['baseYpdf']
    slab_y=1850.47998046875
    controls=[
        {'name':'W.C.','zM':3.24,'arrowTipPdf':[1458.,2018.719970703125],
         'verticalLineStart':[1458.,2008.4000244140625],'label':'3,24 m','textRegion':[1461,2004.5,1492,2014]},
        {'name':'Quarto','zM':3.25,'arrowTipPdf':[1092.239990234375,2018.],
         'verticalLineStart':[1092.239990234375,2007.9200439453125],'label':'3,25 m','textRegion':[1095,2004.2,1127,2014]},
    ]
    lines=[]
    for d in page.get_drawings():
        if d['color']!=(0.,0.,0.):continue
        for item in d['items']:
            if item[0]=='l':lines.append([list(item[1]),list(item[2])])
    def has_line(a,b):
        return sum(all(abs(x-y)<.001 for p,q in zip(sorted(v),sorted([a,b])) for x,y in zip(p,q)) for v in lines)>0
    for r in controls:
        if not has_line(r['arrowTipPdf'],r['verticalLineStart']):raise ValueError('Seta de nível não encontrada')
        label=page.get_textbox(fitz.Rect(*r['textRegion'])).strip()
        if label!=r['label']:raise ValueError('Texto de nível inesperado: '+label)
        r['labelReadFromPdf']=label
        r['baseElevationFromThisDatumM']=altitude(r['zM'],r['arrowTipPdf'][1],base_y,scale)
        r['architecturalSlabTopFromThisDatumM']=altitude(r['zM'],r['arrowTipPdf'][1],slab_y,scale)
    if not has_line([1064.4000244140625,slab_y],[1440.719970703125,slab_y]):
        raise ValueError('Traço da laje arquitetônica não encontrado')
    spread=abs(controls[0]['baseElevationFromThisDatumM']-controls[1]['baseElevationFromThisDatumM'])
    if spread>.005:raise ValueError('Referências gráficas incompatíveis para esta triagem')
    sap=[]
    for b in ['CAD','BIM']:
        directory=HERE.parent/'h03-r138'/f'SAP-{b}'
        files=list(directory.glob('*N2.$2k'))
        if len(files)!=1:raise ValueError('Exportação N2 não única')
        p=files[0];raw=p.read_text(encoding='cp1252')
        rows=re.findall(r'^Joint=\d+\s+CoordSys=GLOBAL\s+CoordType=Cartesian\s+XorR=[^\r\n]+?\s+Z=([\d,.-]+)\s*$',raw,re.M)
        if len(rows)!=443 or set(rows)!={'639,00'}:raise ValueError('Plano analítico N2 diferente da referência')
        if 'Kgf, cm, C' not in raw:raise ValueError('Unidade da exportação desconhecida')
        sap.append({'branch':b,'path':str(p),'sha256':sha(p),'nodeCount':len(rows),'zCm':'639.00',
                    'referencePlaneM':6.39,'isAnalyticalPlaneNotSurvey':True})
    base=controls[0]['baseElevationFromThisDatumM']
    diff=relation(base,6.39)
    result={'revision':'H03/R142','createdAtUtc':datetime.now(timezone.utc).isoformat(),
        'architecture':{'path':str(PDF),'sha256':PDF_SHA,'pageOneBased':1,'section':'BB'},
        'r112Source':{'path':str(ref_path),'sha256':sha(ref_path)},
        'scalePdfUnitsPerM':scale,'scaleOrigin':'Cota bruta 1,30 m até a platibanda, preservada da R112',
        'baseTopPdfY':base_y,'architecturalSlabTopPdfY':slab_y,'levelControls':controls,
        'datumSpreadM':spread,'graphicalAgreementCheckM':.005,
        'graphicalAgreementIsConstructionOrNormativeTolerance':False,
        'primaryDatum':'W.C. +3,24 m no próprio corte BB; Quarto +3,25 m como conferência independente',
        'baseElevationApproxM':round(base,2),'architecturalSlabTopApproxM':round(controls[0]['architecturalSlabTopFromThisDatumM'],2),
        'drawnLocalRaisedDifferenceM':(slab_y-base_y)/scale,
        'structuralReferenceExports':sap,'relationAssumingCommonVerticalDatum':diff,
        'differenceIfIncorrectlyUsingN2Plus060M':6.39+.60-base,
        'absoluteOriginSurveyed':False,'currentNativeN2PlaneReopenedThisStage':False,
        'physicalPedestalHeightM':None,'platformThicknessSelectedM':None,
        'approximateTankBearingTopEstablishedFromDrawing':True,'finalTankElevationApproved':False,
        'maintenanceAccessApproved':False,'tankModelSelected':False,'completeAssemblyWeightKN':None,
        'supportDesigned':False,'nativeLoadsApplied':False,'nativeProjectsEdited':False,'monographEdited':False,
        'limits':[
            'Cota aproximada extraída do desenho e de seu datum; não é levantamento ou detalhamento executivo.',
            'Comparação com +6,39 m assume a mesma referência vertical do estudo; não confirma implantação ou datum geodésico.',
            'Plano analítico exportado N2 não define sozinho face física de apoio, acabamento, espessura da plataforma ou altura do pedestal.',
            'A folga efetiva sob o telhado e o acesso da R112 seguem pendentes; estabelecer cota não resolve manutenção.',
            'O valor 0,60 m do corte não deve ser transferido diretamente como N2+0,60 m.',
            'Tara, plataforma, pedestal, cargas cheio/vazio e dimensionamento de apoio não foram definidos.'
        ],
        'manufacturerDimensionsRechecked':{'dateUtc':datetime.now(timezone.utc).date().isoformat(),
            'url':'https://www.bakof.com.br/produtos/4','capacityL':1000,'upperLengthM':1.88,'upperWidthM':1.23,'heightM':.68,
            'tareConfirmed':False,'productSelected':False},
        'finalStructuralApproval':False,'finalProductivityRankingAllowed':False}
    OUT.mkdir()
    (OUT/'R142-altimetria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    report(result)
    (OUT/'R142-tempo-script.json').write_text(json.dumps({'startUtc':started,'endUtc':datetime.now(timezone.utc).isoformat(),
        'durationMs':(perf_counter()-tick)*1000,'scope':'Somente execução de extração, checagem e relatório; exclui autoria, leitura visual, pesquisa e inferência IA',
        'eligibleForFinalFlowRanking':False},indent=2),encoding='utf-8')
    print(json.dumps({'baseApproxM':round(base,2),'aboveN2ReferenceM':diff['baseAboveReferenceM'],
        'twoDatumSpreadM':spread,'nativeApplied':False}))

def report(r):
    wc,bed=r['levelControls']
    text=f'''# H03/R142 — referência vertical da base do reservatório

**Compatibilização parcial; não executar em obra.** O corte BB permite estimar o topo da base desenhada do reservatório em **aproximadamente +6,81 m**, na mesma referência das cotas de piso da arquitetura. Essa estimativa esclarece a relação vertical, mas não define a plataforma ou seu apoio.

## Como a referência foi obtida

Preservou-se o PDF arquitetônico com SHA-256 `{PDF_SHA}`. Conferiu-se visualmente o corte e localizaram-se, nos vetores do PDF, a seta do nível do banheiro **+3,24 m**, sua ponta na ordenada PDF 2018,71997, e a base superior do reservatório na ordenada 1816,40002. A escala vertical é a mesma calibrada na R112 pela dimensão de 1,30 m até o topo da platibanda: aproximadamente {r['scalePdfUnitsPerM']:.3f} unidades PDF por metro. Texto e segmentos das setas são verificados pelo script, sem OCR.

A conversão usa `z_alvo = z_referência + (y_referência − y_alvo) / escala`, pois o eixo vertical da página cresce para baixo. O banheiro resulta em {wc['baseElevationFromThisDatumM']:.6f} m; a conferência independente pelo quarto +3,25 m resulta em {bed['baseElevationFromThisDatumM']:.6f} m. A diferença entre as leituras é aproximadamente {r['datumSpreadM']*1000:.1f} mm. Essas casas adicionais servem à auditoria aritmética; a informação de projeto é expressa como **aproximadamente +6,81 m**, sem precisão executiva. O limite interno de 5 mm apenas rejeita uma associação gráfica incompatível neste script; não é tolerância construtiva ou normativa.

O traço superior da laje arquitetônica usado como origem do ressalto local fica em aproximadamente **+6,21 m**. A diferença desenhada até a base é {r['drawnLocalRaisedDifferenceM']:.3f} m, coerente graficamente com a indicação de 0,60 m. Logo, a dimensão de 0,60 m é relativa a esse traço arquitetônico, não automaticamente ao N2 estrutural.

## Relação com a referência estrutural

As duas exportações analíticas N2 da R138 contêm 443 nós em Z = 639,00 cm e declaram unidades `Kgf, cm, C`. Assim, o plano de referência exportado é **+6,39 m** nos dois ramos. Não se executou SAP2000 e não se reabriu o N2 nativo nesta etapa.

Admitindo o mesmo datum vertical do estudo, a base arquitetônica estimada fica cerca de **0,42 m acima do plano N2**. Usar N2 +0,60 m levaria a +6,99 m, aproximadamente **0,18 m acima da base desenhada**, alterando a folga sob o telhado. Essa diferença não foi classificada como defeito de transferência, pois compara uma referência arquitetônica com o plano analítico de uma hipótese estrutural revisada.

O valor de 0,42 m **não é a altura calculada de um pedestal**. Para definir pedestal/plataforma ainda se deve relacionar o plano analítico às faces físicas, selecionar espessura e materiais, verificar apoio contínuo e calcular as ações e reações. Nenhuma espessura ou tara desconhecida foi preenchida como zero.

## Consequência para continuar o estudo

A ambiguidade da referência vertical foi reduzida: passa-se a dispor de uma cota aproximada extraída do corte para o topo de apoio. Essa cota deve ser confrontada com a geometria física atual antes de qualquer lançamento. A R112 já mostrou que a referência retangular baixa não satisfaz a reserva superior de estudo de 0,60 m, mesmo antes de definir perfis. Esta etapa não muda esse resultado nem aprova manutenção ou retirada da tampa.

A [página oficial da Bakof](https://www.bakof.com.br/produtos/4) foi reconferida: a referência de 1.000 L mantém dimensões superiores de 1,88 × 1,23 m e altura de 0,68 m. Ela permanece apenas referência dimensional; não se selecionou produto para compra e não se confirmou tara. Não se alterou a cobertura, a base, os pisos, o forro, os arquivos Revit/AutoCAD/Eberick ou a monografia.

Próxima decisão técnica: definir uma solução de acesso/tampa e o apoio físico com topo próximo da cota arquitetônica documentada, preservando as alturas. Depois verificar peso completo, casos cheio/vazio, reações e dimensionamento nos dois receptores. A referência absoluta vem do datum do desenho, sem levantamento de implantação ou vínculo geodésico.

## Tempo e verificação

O arquivo R142-tempo-script.json mede somente a execução do extrator e relatório, não pesquisa, autoria, leitura visual ou inferência da IA. Não integra os tempos finais CAD/BIM. Os hashes do PDF, do estudo R112 e das exportações de referência estão no JSON; os arquivos foram somente lidos. O estudo permanece parcial.
'''
    (OUT/'LEIA-ME-R142.md').write_text(text,encoding='utf-8')

if __name__=='__main__':main()

"""Compara as saidas nativas CAD/BIM da R177, sem aprovar dimensionamento."""
from pathlib import Path
from datetime import datetime, timezone
import importlib.util, json, re, zipfile
from xml.etree import ElementTree as ET
from auditar_escada import OUT, sha, inspect_ifc, check_risers, fully_fixed_supports


def module(name, path):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def model_kind(name):
    if name.startswith('portico_'): return 'portico'
    if name.startswith('grelha_SAP2000_escada_'): return 'escada'
    if name.startswith('grelha_SAP2000_laje_'):
        m=re.search(r'(?:_|-)(N[12])[.]',name)
        if m: return m[1]
    raise ValueError('Exportacao desconhecida: '+name)


def report_text(path):
    with zipfile.ZipFile(path) as z:
        root=ET.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    return '\n'.join(
        ''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in root.findall('.//w:p',ns))


def main():
    here=Path(__file__).parent
    comp=module('comp176',here.parent/'h03-r176/comparar_receptores.py')
    prep=json.loads((OUT/'R177-preparacao.json').read_text(encoding='utf-8'))
    branches={};models={}
    for branch, filename in [('CAD','R177-CAD-ESCADA-CONTROLE.IFC'),('BIM','R177-BIM-ESCADA-CORRIGIDA.IFC')]:
        ifc=OUT/f'{branch}-IFC'/filename
        elements, counts=inspect_ifc(ifc)
        models[branch]={};exports={}
        for path in sorted((OUT/f'{branch}-SAP').glob('*.$2k')):
            kind=model_kind(path.name)
            if kind in exports: raise ValueError('Tipo duplicado: '+kind)
            parsed=comp.sap.parse(path.read_text(encoding='cp1252'))
            models[branch][kind]=parsed
            exports[kind]=dict(path=str(path),sha256=sha(path),bytes=path.stat().st_size,
                joints=len(parsed['joints']),frames=len(parsed['frames']),fullyFixedSupports=fully_fixed_supports(parsed))
        if set(exports)!={'portico','escada','N1','N2'}: raise ValueError('Saida incompleta: '+branch)
        entry=prep['branches'][branch]
        for source in entry['sourceFiles']:
            if sha(Path(entry['sourceRoot'])/source['relativePath'])!=source['sha256']:
                raise ValueError('Fonte alterada: '+branch+' '+source['relativePath'])
        with zipfile.ZipFile(entry['projectPath']) as z:
            if z.testzip(): raise ValueError('PRJ corrompido')
        report=OUT/f'{branch}-mensagens-segunda-analise.docx'
        text=report_text(report)
        (OUT/f'{branch}-mensagens-segunda-analise.txt').write_text(text,encoding='utf-8')
        duration=re.findall(r'Tempo total de processamento:\s*(\d\d:\d\d:\d\d)',text)
        if len(duration)!=1: raise ValueError('Duracao nativa ausente ou ambigua')
        branches[branch]=dict(ifc=dict(path=str(ifc),sha256=sha(ifc),classCounts=counts),elements=elements,
            finishedGeometry=check_risers(elements['LE3']['measuredUpperHorizontalLevelsM'],elements['LE2']['measuredUpperHorizontalLevelsM']),
            exports=exports,prj=dict(path=entry['projectPath'],sha256=sha(entry['projectPath'])),
            sourceFilesPreserved=len(entry['sourceFiles']),report=dict(path=str(report),sha256=sha(report),
            nativeProcessingDuration=duration[0],precisionCheckNoDifference='Nenhuma diferença encontrada.' in text))
    comparisons={kind:comp.compare(models['CAD'][kind],models['BIM'][kind]) for kind in ['portico','escada','N1','N2']}
    for comparison in comparisons.values():
        differences=comparison['nodalLoadDifferences']
        comparison['nodalDifferenceMagnitudeSummary']=dict(
            maxForceDifferenceKgf=max((abs(d['bimMinusCad'][k]) for d in differences
                if d['bimMinusCad'] is not None for k in ['F1','F2','F3']),default=0),
            maxMomentDifferenceKgfCm=max((abs(d['bimMinusCad'][k]) for d in differences
                if d['bimMinusCad'] is not None for k in ['M1','M2','M3']),default=0),
            unmatchedPositionPatternRows=sum(d['bimMinusCad'] is None for d in differences))
    geometry={name:{key:branches['CAD']['elements'][name][key]==branches['BIM']['elements'][name][key]
        for key in ['ifcClass','minM','maxM','measuredUpperHorizontalLevelsM']} for name in ['LE1','LE2','LE3','AE1A','AE1B']}
    result=dict(revision='H03/R177',recordedAtUtc=datetime.now(timezone.utc).isoformat(),branches=branches,
        stairElementGeometryComparisonAtExportPrecision=geometry,analyticComparisons=comparisons,
        scope='Lancamento assistido dos dois lances e patamar no receptor Eberick; IFC e quatro modelos textuais por fluxo.',
        lowerFixedBaseIsAnUnvalidatedIdealization=True,physicalFoundationDesigned=False,
        originalRevitLandingContourReconciliationPending=True,uniformFinishedRiserStrictAuditPending=True,
        noFullDimensioningReview=True,fullPairedFlowTimeMeasured=False,finalRankingAllowed=False,structuralApproval=False)
    (OUT/'R177-comparacao-CAD-BIM.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(geometry=geometry,branches={b:dict(duration=v['report']['nativeProcessingDuration'],
        finishedGeometry=v['finishedGeometry'],exports={k:(e['joints'],e['frames']) for k,e in v['exports'].items()}) for b,v in branches.items()},
        analytical={k:dict(joints=v['jointCoordinateMultisetsEqual'],edges=v['frameUndirectedEndpointMultisetsEqual'],
            sections=v['sectionPropertiesByUndirectedSegmentEqual'],nodalDifferences=len(v['nodalLoadDifferences']),
            unequalTables=[t for t,r in v['tables'].items() if not r['equal']]) for k,v in comparisons.items()}),indent=2))


if __name__=='__main__': main()

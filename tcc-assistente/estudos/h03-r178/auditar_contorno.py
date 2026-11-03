"""Confere exportacoes reais R178; leitura apenas, sem dimensionar a estrutura."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import sys, json, re, zipfile

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent/'h03-r177'))
from auditar_escada import inspect_ifc, check_risers, sha
from comparar_escada import model_kind, module, report_text

OUT = Path('D:/TCC/outputs/Escada-H03-R178-CONTORNO-PATAMAR-NAO-EXECUTAR')


def triangle_signature(vertices, faces, precision=7):
    """Multiconjunto espacial de triangulos, independente de IDs e ordem I/J."""
    return Counter(tuple(sorted(tuple(round(float(x), precision) for x in vertices[i])
                                for i in triangle)) for triangle in faces)


def physical_meshes(path):
    sys.path.insert(0, 'D:/TCC/work/ifc/deps')
    import ifcopenshell, ifcopenshell.geom
    import numpy as np
    model = ifcopenshell.open(str(path))
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    meshes = {}
    for element in model.by_type('IfcElement'):
        if element.Name not in {'LE1', 'LE2', 'LE3', 'AE1A', 'AE1B'}:
            continue
        shape = ifcopenshell.geom.create_shape(settings, element)
        vertices = np.asarray(shape.geometry.verts).reshape(-1, 3)
        faces = np.asarray(shape.geometry.faces).reshape(-1, 3)
        if not np.isfinite(vertices).all():
            raise ValueError('Malha nao finita')
        if element.Name in meshes:
            raise ValueError('Elemento duplicado')
        meshes[element.Name] = triangle_signature(vertices, faces)
    if set(meshes) != {'LE1', 'LE2', 'LE3', 'AE1A', 'AE1B'}:
        raise ValueError('Conjunto fisico incompleto')
    return meshes


def main():
    prep = json.loads((OUT/'R178-preparacao.json').read_text(encoding='utf-8'))
    comp = module('comp178', HERE.parent/'h03-r176/comparar_receptores.py')
    branches, models, meshes = {}, {}, {}
    for branch, entry in prep['branches'].items():
        changed = [f['relativePath'] for f in entry['sourceFiles']
                   if sha(Path(entry['sourceRoot'])/f['relativePath']) != f['sha256']]
        if changed:
            raise ValueError('Fonte R177 alterada: '+str(changed))
        prj = Path(entry['projectPath'])
        with zipfile.ZipFile(prj) as z:
            if z.testzip():
                raise ValueError('PRJ corrompido')
        ifc = Path(entry['targetRoot'])/'Arquivos do projeto'/f'r178-{branch.lower()}-patamar-controle.IFC'
        elements, counts = inspect_ifc(ifc)
        meshes[branch] = physical_meshes(ifc)
        report = OUT/f'{branch}-mensagens-analise.docx'
        text = report_text(report)
        (OUT/f'{branch}-mensagens-analise.txt').write_text(text, encoding='utf-8')
        times = re.findall(r'Tempo total de processamento:\s*(\d\d:\d\d:\d\d)', text)
        if len(times) != 1:
            raise ValueError('Duracao nativa ausente ou ambigua')
        models[branch], exports = {}, {}
        for p in sorted((OUT/f'{branch}-SAP').glob('*.$2k')):
            kind = model_kind(p.name)
            if kind in models[branch]:
                raise ValueError('Modelo duplicado')
            models[branch][kind] = comp.sap.parse(p.read_text(encoding='cp1252'))
            exports[kind] = dict(path=str(p), sha256=sha(p), bytes=p.stat().st_size)
        if set(models[branch]) != {'portico', 'escada', 'N1', 'N2'}:
            raise ValueError('Exportacao analitica incompleta')
        bounds = elements['LE1']
        if abs(bounds['minM'][0]-4.5) > 1e-6 or abs(bounds['maxM'][0]-6.45) > 1e-6:
            raise ValueError('Largura do patamar nao corrigida')
        start = json.loads((OUT/f'{branch}-correcao-inicio.json').read_text(encoding='utf-8'))
        saved = json.loads((OUT/f'{branch}-correcao-primeiro-save.json').read_text(encoding='utf-8'))
        elapsed = (datetime.fromisoformat(saved['savedAt'])-datetime.fromisoformat(start['startedAt'])).total_seconds()
        branches[branch] = dict(projectPath=str(prj), projectSha256=sha(prj), projectZipValid=True,
            ifcPath=str(ifc), ifcSha256=sha(ifc), elements=elements, classCounts=counts,
            sourceR177FilesUnchanged=len(entry['sourceFiles']), exports=exports,
            nativePartialAnalysisTime=times[0], nativeAnalysisProcessedWithWarnings=True,
            finishedRisers=check_risers(elements['LE3']['measuredUpperHorizontalLevelsM'],
                                       elements['LE2']['measuredUpperHorizontalLevelsM']),
            observedCorrectionIntervalSeconds=elapsed,
            observedCorrectionIntervalIsActiveWorkTime=False,
            observedCorrectionIntervalIsFullFlowTime=False,
            observedCorrectionIntervalIncludesConversationPauses=branch=='BIM',
            correctionScope='Exclusao de LE1, duas barras comuns de largura zero, relancamento de LE1; CAD inicia apos exclusao',
            fullDimensioningReviewed=False, structuralApproval=False)
    comparison = {kind: comp.compare(models['CAD'][kind], models['BIM'][kind])
                  for kind in ('portico', 'escada', 'N1', 'N2')}
    result = dict(revision='H03/R178', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        branches=branches, analyticalComparison=comparison,
        physicalTriangulatedMeshesEqualAt1eMinus7M={name: meshes['CAD'][name]==meshes['BIM'][name]
                                                   for name in meshes['CAD']},
        landingWidthBeforeM=2.15, landingWidthAfterM=1.95,
        landingFrontFaceDifferenceFromRevitCm=2.59166667,
        landingFullContourReconciliationCompleted=False,
        originalOuterBoundaryBarsStillPresent=True,
        boundaryBarsAreNotAdditionalPhysicalBeams=True,
        additionalPhysicalColumnsIntroduced=False,
        baseFixityPhysicalJustificationPending=True,
        stairLoadHypothesesReviewPending=True,
        IFCStairAttributesMissingDespiteMeasuredGeometry=True,
        analyticalLoadOrientationReconciliationPending=True,
        nativeProcessingSingleObservationEach=True,
        correctionTimingCannotRankCadAgainstBim=True,
        fullPairedFlowTimeMeasured=False, fullPairedFlowComparisonFinished=False,
        completeNativeModelEquivalenceVerified=False, structuralApproval=False)
    (OUT/'R178-comparacao-CAD-BIM.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(dict(meshes=result['physicalTriangulatedMeshesEqualAt1eMinus7M'],
        models={k:{f:v[f] for f in ('jointCoordinateMultisetsEqual','frameUndirectedEndpointMultisetsEqual',
            'sectionPropertiesByUndirectedSegmentEqual','counts')} for k,v in comparison.items()},
        times={b:entry['nativePartialAnalysisTime'] for b,entry in branches.items()}), indent=2))


if __name__ == '__main__':
    main()

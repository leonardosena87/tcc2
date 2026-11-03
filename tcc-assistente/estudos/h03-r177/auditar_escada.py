"""Auditoria de geometria e registro analitico; nao dimensiona nem aprova.

IfcOpenShell somente le IFCs exportados. SAP2000 nao e executado.
O patamar e os apoios permanecem hipoteses explicitas de um ensaio BIM.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib, importlib.util, json, math, sys

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Escada-H03-R177-INTEGRACAO-EBERICK-NAO-EXECUTAR')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def finished_risers(levels_m, floor_finished_m, finish_m):
    """Recebe as faces superiores medidas, sem preencher degraus ausentes."""
    if not levels_m or not all(math.isfinite(z) for z in levels_m):
        raise ValueError('Faces superiores ausentes ou nao finitas')
    if any(b <= a for a, b in zip(levels_m, levels_m[1:])):
        raise ValueError('Faces superiores devem ser estritamente crescentes')
    finished = [floor_finished_m] + [z + finish_m for z in levels_m]
    return [(b-a)*100 for a, b in zip(finished, finished[1:])]


def check_risers(lower, upper, tolerance_cm=0.02):
    a = finished_risers(lower, 0.22, 0.05)
    b = finished_risers(upper, lower[-1] + 0.05, 0.05)
    target_cm = (3.25-0.22)*100/17
    return dict(lowerCount=len(a), upperCount=len(b), lowerFinishedRisersCm=a,
                upperFinishedRisersCm=b, targetCm=target_cm,
                maxDifferenceCm=max(abs(v-target_cm) for v in a+b),
                geometry17FinishedRisersWithinTolerance=(len(a)==9 and len(b)==8
                    and all(abs(v-target_cm)<=tolerance_cm for v in a+b)),
                toleranceCm=tolerance_cm)


def fully_fixed_supports(model):
    rows = model['tables'].get('JOINT RESTRAINT ASSIGNMENTS', [])
    return [dict(positionCm=model['joints'][r['Joint']], restraints=r)
            for r in rows if all(r.get(k)=='YES' for k in ('U1','U2','U3','R1','R2','R3'))]


def inspect_ifc(ifc):
    sys.path.insert(0, 'D:/TCC/work/ifc/deps')
    import ifcopenshell, ifcopenshell.geom
    import numpy as np
    model = ifcopenshell.open(str(ifc))
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    elements = {}
    for element in model.by_type('IfcElement'):
        if element.Name not in {'LE1','LE2','LE3','AE1A','AE1B'}:
            continue
        if element.Name in elements:
            raise ValueError('Nome duplicado: '+element.Name)
        shape = ifcopenshell.geom.create_shape(settings, element)
        vertices = np.asarray(shape.geometry.verts).reshape(-1,3)
        faces = np.asarray(shape.geometry.faces).reshape(-1,3)
        if not np.isfinite(vertices).all():
            raise ValueError('Geometria nao finita')
        horizontal = set()
        for ids in faces:
            tri = vertices[ids]
            normal = np.cross(tri[1]-tri[0],tri[2]-tri[0])
            if normal[2] > 1e-10 and np.ptp(tri[:,2]) < 1e-7:
                horizontal.add(round(float(tri[0,2]),8))
        entry = dict(ifcClass=element.is_a(), globalId=element.GlobalId,
                     minM=vertices.min(0).tolist(), maxM=vertices.max(0).tolist(),
                     measuredUpperHorizontalLevelsM=sorted(horizontal))
        if element.is_a('IfcStairFlight'):
            entry['exportedAttributes'] = {k:element.get_info()[k] for k in
                ('NumberOfRisers','NumberOfTreads','RiserHeight','TreadLength')}
        elements[element.Name] = entry
    if set(elements) != {'LE1','LE2','LE3','AE1A','AE1B'}:
        raise ValueError('Conjunto de escada incompleto')
    return elements, dict(Counter(e.is_a() for e in model.by_type('IfcElement')))


def main():
    ifc = OUT/'BIM-IFC/R177-BIM-ESCADA-CORRIGIDA.IFC'
    elements, class_counts = inspect_ifc(ifc)
    geometry = check_risers(elements['LE3']['measuredUpperHorizontalLevelsM'],
                            elements['LE2']['measuredUpperHorizontalLevelsM'])
    spec = importlib.util.spec_from_file_location('sap177', HERE.parent/'h03-r122/consolidar.py')
    sap = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sap)
    exports = {}
    for path in sorted((OUT/'BIM-SAP').glob('*.$2k')):
        parsed = sap.parse(path.read_text(encoding='cp1252'))
        exports[path.name] = dict(sha256=sha(path), bytes=path.stat().st_size,
            joints=len(parsed['joints']), frames=len(parsed['frames']),
            fullyFixedSupports=fully_fixed_supports(parsed),
            zLevelsCm=sorted(set(p[2] for p in parsed['joints'].values())))
    if len(exports) != 4:
        raise ValueError('Exportacao analitica incompleta: esperados 4 arquivos')
    prep = json.loads((OUT/'R177-preparacao.json').read_text(encoding='utf-8'))
    preservation = {}
    for branch, paths in prep['branches'].items():
        mismatches = [entry['relativePath'] for entry in paths['sourceFiles']
            if sha(Path(paths['sourceRoot'])/entry['relativePath']) != entry['sha256']]
        if mismatches:
            raise ValueError('Fonte alterada: '+str(mismatches))
        preservation[branch] = dict(sourceFiles=len(paths['sourceFiles']), unchanged=True)
    prj = Path(prep['branches']['BIM']['projectPath'])
    result = dict(revision='H03/R177', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        scope='Auditoria isolada do receptor BIM com lancamento assistido; nao inclui comparacao CAD',
        ifc=dict(path=str(ifc),sha256=sha(ifc),classCounts=class_counts),
        prj=dict(path=str(prj),sha256=sha(prj)),elements=elements,finishedGeometry=geometry,
        exports=exports,sourcePreservation=preservation,
        lowerSupport=dict(authorizedIdealization=True, physicalFoundationDesigned=False,
            nativeObjects=['AE1A','AE1B'],nativeClass='Fundacao sem pilar de arranque / IfcFooting',
            markerDimensionsCm=[20,20,20],markerDimensionsAreNotAFoundationDesign=True,
            nativeStubBaseZCm=0,nativeStubTopZCm=20,
            firstTrial='Rotulado; erro de precisao de 8.29% em Y no caso 9',
            secondTrial='Engastado na base dos dois marcadores; processado com avisos',
            fixedBaseHypothesisNeedsReview=True),
        landingContour=dict(expectedRevitXBoundsM=[4.5,6.45],measuredEberickXBoundsM=[4.4,6.55],
            sideBarWidthsReadbackCm=20,ifcContourStillDifferent=True,
            axisVersusPhysicalFaceReconciliationPending=True),
        loads=dict(accidentalKnM2=2.5,finishGKnM2=1.0,finishGIsProvisionalHypothesis=True,
            guardrailAndPointLoadVerificationPending=True),
        nativePartialAnalysisProcessedWithWarnings=True,fullDimensioningReviewed=False,
        implicitStairWindowAutomaticReinforcementNotValidated=True,
        fullCadBimComparisonCompleted=False,fullPairedFlowTimeMeasured=False,
        structuralApproval=False)
    (OUT/'R177-BIM-resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(finishedGeometry=geometry,sourcePreservation=preservation,
        exports={k:dict(joints=v['joints'],frames=v['frames']) for k,v in exports.items()}),indent=2))


if __name__=='__main__':
    main()

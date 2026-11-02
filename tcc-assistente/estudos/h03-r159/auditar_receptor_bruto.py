"""Concilia relatório nativo e IFC4 de controle do receptor bruto R159.

Os sólidos do receptor podem dividir uma origem em várias partes. Contagens
de sólidos não são contagens automáticas de erros. Não altera PRJ, IFC ou DOCX.
"""
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from auditar_ifc import OUT, NATIVE, read, sha, mesh, ifcopenshell, get_psets

ROOT = Path('D:/TCC/outputs/H03-R159-Revit-VIGA-PATAMAR-NAO-EXECUTARH03_R159_IFC_BRUTO_NAO_E')
REPORT = ROOT/'Arquivos do projeto/Documentos/Eberick/Relatorio_de_importacao_de_elementos_IFC.docx'
RECEIVER = ROOT/'Arquivos do projeto/Modelo 3D.IFC'
PRJ = ROOT/'Projeto Eberick'/(ROOT.name+'.prj')
XY_TOLERANCE_M = 1e-4  # 0,1 mm: inclui arredondamento observado de 0,0167 mm.


def parse_report(path):
    with ZipFile(path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    rows=[]; group=None
    for p in tree.findall('.//w:p',ns):
        text=''.join(p.itertext()).strip()
        if text in ('Vigas','Pilares'): group=text
        if text.startswith('Nome IFC:'):
            match=re.fullmatch(r'Nome IFC: (.+):(\d+) - Pavimento IFC: (.+)',text)
            if match is None or group is None: raise ValueError('Linha nativa não prevista: '+text)
            rows.append(dict(group=group,revId=match[2],level=match[3],nativeText=text))
    return rows


def beam_candidates(box, source):
    """Associação espacial nominal; eixos ortogonais, sem validar conectividade."""
    lo,hi=box['minM'],box['maxM']; results=[]
    for src in source:
        if src['Kind'] != 'beam': continue
        a=src['AxisM']; along=0 if abs(a[3]-a[0])>abs(a[4]-a[1]) else 1; cross=1-along
        center=(lo[cross]+hi[cross])/2
        start,end=sorted((a[along],a[along+3]))
        if abs(center-a[cross])>XY_TOLERANCE_M or lo[along]<start-XY_TOLERANCE_M or hi[along]>end+XY_TOLERANCE_M:continue
        if hi[along]-lo[along]<1e-5:continue
        delta=abs(hi[2]-a[2])
        if delta<=.5:results.append((delta,src,along,cross))
    results.sort(key=lambda r:r[0])
    if not results or (len(results)>1 and abs(results[0][0]-results[1][0])<1e-6):return None
    _,src,along,cross=results[0]
    return dict(nativeMark=src['Mark'],nativeId=src['Id'],nativeTopM=src['AxisM'][2],
        receiverTopM=hi[2],topDeltaM=hi[2]-src['AxisM'][2],
        nativeWidthM=src['BM'],receiverWidthM=hi[cross]-lo[cross],
        nativeHeightM=src['HM'],receiverHeightM=hi[2]-lo[2],
        heightDeltaM=(hi[2]-lo[2])-src['HM'])


def main():
    files=[REPORT,RECEIVER,PRJ,NATIVE]
    before={str(p):sha(p) for p in files}
    native=read(NATIVE);rows=parse_report(REPORT)
    expected={str(e['Id']):e for e in native['Elements'] if e['Kind'] in ('beam','column')}
    ids=Counter(r['revId'] for r in rows)
    missing=sorted(set(expected)-set(ids));unknown=sorted(set(ids)-set(expected))
    duplicated=[k for k,v in ids.items() if v!=1]
    group_mismatch=[r for r in rows if r['revId'] in expected and r['group']!={'beam':'Vigas','column':'Pilares'}[expected[r['revId']]['Kind']]]
    assert not missing and not unknown and not duplicated and not group_mismatch
    model=ifcopenshell.open(str(RECEIVER));assert model.schema=='IFC4'
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    parts=[]
    for cls in ('IfcColumn','IfcBeam','IfcSlab','IfcStair','IfcStairFlight'):
        for obj in model.by_type(cls):
            geom=mesh(obj,settings)
            psets=get_psets(obj)
            parts.append(dict(ifcClass=cls,name=obj.Name,guid=obj.GlobalId,geometry=geom,
                psets=psets,nominalBeamAssociation=beam_candidates(geom,native['Elements']) if cls=='IfcBeam' else None))
    beams=[r for r in parts if r['ifcClass']=='IfcBeam']
    matched=[r['nominalBeamAssociation'] for r in beams if r['nominalBeamAssociation']]
    assert before=={str(p):sha(p) for p in files}
    frozen=read(OUT/'R159-receptor-bruto-congelamento.json')
    original_prj=next(e for e in frozen['entries'] if e['relativePath'].endswith('.prj'))
    result=dict(revision='H03/R159',recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        receiverRoot=str(ROOT),receiverProject=str(PRJ),receiverInputWasUnmodifiedNativeIfc=True,
        nominalSpatialAssociationXYToleranceM=XY_TOLERANCE_M,
        initialProgramConfiguration=True,nineWizardLevelsRetained=True,importColumnsAndBeamsChecked=True,
        sourceHashes=before,sourceHashesUnchangedAfterRead=True,
        prjStillMatchesInitialSavedSnapshot=sha(PRJ)==original_prj['sha256'],
        importedOriginsByReport=dict(Counter(r['group'] for r in rows)),importedOriginCount=len(rows),
        missingReportOriginIds=missing,unknownReportOriginIds=unknown,duplicatedReportOriginIds=duplicated,
        stairLandingBeamOriginReported=any(r['revId']=='473802' for r in rows),reportRows=rows,
        receiverIfcProductCounts=dict(Counter(o.is_a() for o in model.by_type('IfcProduct'))),
        buildingSlabsOrStairConvertedInThisOutput=bool(model.by_type('IfcSlab') or model.by_type('IfcStair') or model.by_type('IfcStairFlight')),
        beamSolidsWithNominalSpatialAssociation=len(matched),unmatchedBeamSolids=len(beams)-len(matched),
        distinctBeamOriginsSpatiallyAssociated=len({r['nativeId'] for r in matched}),
        beamPartsWithDifferentTop=sum(abs(r['topDeltaM'])>1e-5 for r in matched),
        beamPartsWithDifferentHeight=sum(abs(r['heightDeltaM'])>1e-5 for r in matched),
        distinctBeamOriginsWithDifferentTop=sorted({r['nativeMark'] for r in matched if abs(r['topDeltaM'])>1e-5}),
        distinctBeamOriginsWithDifferentHeight=sorted({r['nativeMark'] for r in matched if abs(r['heightDeltaM'])>1e-5}),
        columnSegmentationNotAutomaticallyClassifiedAsDuplication=True,
        geometricAssociationIsNotAnalyticalConnectivity=True,fullBeamCoverageNotVerified=True,
        columnsPhysicalCoverageAndSectionsNotVerified=True,materialTransferCausalityNotProved=True,
        structuralAnalysisPerformed=False,fullCompatibilityReviewCompleted=False,structuralApproval=False,
        mainCadBimProjectsUpdated=False,pairedFlowComparisonCompleted=False,parts=parts)
    (OUT/'R159-Eberick-recepcao-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['importedOriginsByReport','importedOriginCount','receiverIfcProductCounts','distinctBeamOriginsSpatiallyAssociated','beamPartsWithDifferentTop','beamPartsWithDifferentHeight','prjStillMatchesInitialSavedSnapshot']}))


if __name__=='__main__':main()

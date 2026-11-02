"""Confere identidades do relatorio e geometria do IFC4 receptor R161.

Funcoes parse_report e beam_candidates derivadas da auditoria R159.
Nao altera PRJ/IFC/DOCX nem transforma segmentacao em erro automaticamente.
"""
import argparse
from collections import Counter
from datetime import datetime,timezone
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from auditar_exportacao import OUT,NATIVE,IFC,EXPECTED_NATIVE_SHA,read,sha,mesh,ifcopenshell,get_psets
XY_TOLERANCE_M=1e-4


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



def main(root,receiver):
    root=Path(root).resolve();receiver=Path(receiver).resolve()
    report=root/'Arquivos do projeto/Documentos/Eberick/Relatorio_de_importacao_de_elementos_IFC.docx'
    projects=list((root/'Projeto Eberick').glob('*.prj'))
    if len(projects)!=1:raise ValueError('Projeto receptor ausente ou ambiguo')
    prj=projects[0]
    files=[report,receiver,prj,NATIVE,IFC];before={str(p):sha(p) for p in files}
    assert before[str(NATIVE)]==EXPECTED_NATIVE_SHA
    export_audit=read(OUT/'R161-IFC-auditoria.json')
    assert before[str(IFC)]==export_audit['sources'][str(IFC)]
    frozen=read(OUT/'R161-receptor-bruto-congelamento.json')
    initial_prj=next(e for e in frozen['entries'] if e['relativePath'].lower().endswith('.prj'))
    assert before[str(prj)]==initial_prj['sha256']
    native=read(NATIVE); rows=parse_report(report)
    expected={str(e['Id']):e for e in native['Elements'] if e['Kind'] in ('beam','column')}
    ids=Counter(r['revId'] for r in rows)
    missing=sorted(set(expected)-set(ids));unknown=sorted(set(ids)-set(expected))
    duplicated=[k for k,v in ids.items() if v!=1]
    group_mismatch=[r for r in rows if r['revId'] in expected and r['group']!={'beam':'Vigas','column':'Pilares'}[expected[r['revId']]['Kind']]]
    if missing or unknown or duplicated or group_mismatch:
        raise ValueError(json.dumps(dict(missing=missing,unknown=unknown,duplicated=duplicated,groupMismatch=group_mismatch)))
    model=ifcopenshell.open(str(receiver))
    if model.schema!='IFC4':raise ValueError('Saida receptora esperada em IFC4')
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    parts=[]
    for cls in ('IfcColumn','IfcBeam','IfcSlab','IfcStair','IfcStairFlight'):
        for obj in model.by_type(cls):
            box=mesh(obj,settings)
            parts.append(dict(ifcClass=cls,name=obj.Name,guid=obj.GlobalId,geometry=box,psets=get_psets(obj),
                nominalBeamAssociation=beam_candidates(box,native['Elements']) if cls=='IfcBeam' else None))
    beams=[p for p in parts if p['ifcClass']=='IfcBeam']
    matched=[p['nominalBeamAssociation'] for p in beams if p['nominalBeamAssociation']]
    matched_ids={r['nativeId'] for r in matched}
    unassociated=[dict(nativeId=e['Id'],nativeMark=e['Mark'],axisM=e['AxisM']) for e in native['Elements'] if e['Kind']=='beam' and e['Id'] not in matched_ids]
    assert before=={str(p):sha(p) for p in files}
    result=dict(revision='H03/R161',recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        sourceAuthoringRevision='H03/R160',receiverRoot=str(root),receiverProject=str(prj),
        sourceHashes=before,sourceHashesUnchangedAfterRead=True,
        rawNativeIfcStillMatchesExportAudit=True,prjStillMatchesFirstSavedSnapshot=True,
        expectedOriginCount=len(expected),importedOriginCount=len(rows),
        importedOriginsByReport=dict(Counter(r['group'] for r in rows)),reportRows=rows,
        missingReportOriginIds=missing,unknownReportOriginIds=unknown,duplicatedReportOriginIds=duplicated,
        stairLandingBeamOriginReported=any(r['revId']=='473802' for r in rows),
        removedColumnOriginsAbsent=not any(r['revId'] in ('473797','473798') for r in rows),
        receiverIfcProductCounts=dict(Counter(o.is_a() for o in model.by_type('IfcProduct'))),
        stairOrSlabNativeSolidsPresent=bool(model.by_type('IfcSlab') or model.by_type('IfcStair') or model.by_type('IfcStairFlight')),
        nominalSpatialAssociationXYToleranceM=XY_TOLERANCE_M,
        beamSolidsWithNominalSpatialAssociation=len(matched),unmatchedBeamSolids=len(beams)-len(matched),
        distinctBeamOriginsSpatiallyAssociated=len({r['nativeId'] for r in matched}),
        originsWithoutNominalSpatialAssociation=unassociated,
        unmatchedReceiverBeamParts=[p for p in beams if p['nominalBeamAssociation'] is None],
        beamPartsWithDifferentTop=sum(abs(r['topDeltaM'])>1e-5 for r in matched),
        beamPartsWithDifferentHeight=sum(abs(r['heightDeltaM'])>1e-5 for r in matched),
        distinctBeamOriginsWithDifferentTop=sorted({r['nativeMark'] for r in matched if abs(r['topDeltaM'])>1e-5}),
        distinctBeamOriginsWithDifferentHeight=sorted({r['nativeMark'] for r in matched if abs(r['heightDeltaM'])>1e-5}),
        columnSegmentationNotAutomaticallyClassifiedAsDuplication=True,
        geometricAssociationIsNotAnalyticalConnectivity=True,fullBeamCoverageNotVerified=True,
        columnsPhysicalCoverageAndSectionsNotVerified=True,materialTransferCausalityNotProved=True,
        newStructuralAnalysisPerformed=False,fullCompatibilityReviewCompleted=False,structuralApproval=False,
        mainCadBimProjectsUpdated=False,pairedFlowComparisonCompleted=False,parts=parts)
    (OUT/'R161-Eberick-recepcao-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('importedOriginsByReport','receiverIfcProductCounts','distinctBeamOriginsSpatiallyAssociated','beamPartsWithDifferentTop','beamPartsWithDifferentHeight')}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',required=True);parser.add_argument('--receiver-ifc',required=True)
    args=parser.parse_args();main(args.root,args.receiver_ifc)

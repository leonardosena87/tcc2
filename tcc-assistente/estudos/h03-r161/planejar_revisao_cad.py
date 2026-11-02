"""Diagnostico geometricamente delimitado; nao altera nomes, contornos ou PRJ."""
import json
from datetime import datetime, timezone

from auditar_exportacao import OUT,NATIVE,read,sha,mesh,ifcopenshell
from auditar_cad_eberick import IFC,PRJ


def unique_slab_candidate(rows,target):
    xs=[p[0] for p in target['ProfileM']]
    ys=[p[1] for p in target['ProfileM']]
    xmin,xmax=min(xs),max(xs);ymin,ymax=min(ys),max(ys)
    candidates=[]
    for row in rows:
        lo,hi=row['geometry']['minM'],row['geometry']['maxM']
        if (abs(hi[2]-target['AxisM'][0])<=.001 and
            abs(hi[2]-lo[2]-target['HM'])<=1e-6 and
            abs((lo[0]+hi[0])/2-(xmin+xmax)/2)<=1e-6 and
            lo[0]>=xmin-1e-6 and hi[0]<=xmax+1e-6 and
            min(hi[1],ymax)-max(lo[1],ymin)>0):
            candidates.append(row)
    if len(candidates)!=1:
        raise ValueError('Correspondencia espacial ausente ou ambigua; nao associar por nome')
    return candidates[0]


def main():
    files=[IFC,PRJ,NATIVE]; before={str(p):sha(p) for p in files}
    native=read(NATIVE);model=ifcopenshell.open(str(IFC))
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    slabs=[dict(name=o.Name,guid=o.GlobalId,geometry=mesh(o,settings)) for o in model.by_type('IfcSlab')]
    source_slab=next(e for e in native['Elements'] if e['Mark']=='L6-N1')
    candidate=unique_slab_candidate(slabs,source_slab)
    source_beam=next(e for e in native['Elements'] if e['Mark']=='V15-N1')
    beams=[o for o in model.by_type('IfcBeam') if o.Name=='V15']
    assert len(beams)==1
    box=mesh(beams[0],settings);lo,hi=box['minM'],box['maxM']
    result=dict(revision='H03/R161',recordedAtUtc=datetime.now(timezone.utc).isoformat(),sources=before,
        slab=dict(revitMark=source_slab['Mark'],revitId=source_slab['Id'],revitProfileM=source_slab['ProfileM'],
            eberickSpatialCandidate=candidate,namesDiffer=candidate['name']!=source_slab['Mark'].split('-')[0],
            sameNameOtherSlabs=[r for r in slabs if r['name']=='L6'],
            associationByIndependentIdentityProved=False,contourEquivalenceApproved=False,
            comparisonRule='Unico candidato no nivel, espessura e faixa X correspondentes com intersecao Y. Contornos de faces livres no Eberick e perfil Revit nao se equiparam por area de caixa.'),
        beam=dict(revitMark=source_beam['Mark'],revitId=source_beam['Id'],eberickName=beams[0].Name,
            eberickGeometry=box,revitAxisM=source_beam['AxisM'],
            eberickCurrentCenterYM=(lo[1]+hi[1])/2,
            requiredCenterYChangeM=source_beam['AxisM'][1]-(lo[1]+hi[1])/2,
            eberickCurrentHeightM=hi[2]-lo[2],revitCandidateHeightM=source_beam['HM'],
            structuralAdequacyOfCandidateProved=False),
        sourceHashesUnchangedAfterRead=before=={str(p):sha(p) for p in files},
        nativeChangesApplied=False,quantityDifferenceFromBoundingBoxesReportedAsError=False,
        finalPairedComparisonCompleted=False,structuralApproval=False)
    assert result['sourceHashesUnchangedAfterRead']
    (OUT/'R161-planejamento-revisao-CAD.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(slabCandidate=candidate['name'],beamDeltaYM=result['beam']['requiredCenterYChangeM'],beamHeightM=result['beam']['eberickCurrentHeightM'])))


if __name__=='__main__':main()

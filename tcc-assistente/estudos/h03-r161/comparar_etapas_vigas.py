"""Separa parametro nominal, caixa da malha IFC bruta e caixa receptora.

Nao atribui causalidade de algoritmo nem trata caixa como secao analitica.
"""
import json
from datetime import datetime,timezone
from auditar_exportacao import OUT,read,sha


def dimensions(box):
    return dict(topM=box['maxM'][2],heightM=box['maxM'][2]-box['minM'][2])


def compare_three(nominal,raw_box,receiver_box,tolerance=1e-5):
    raw=dimensions(raw_box);receiver=dimensions(receiver_box)
    d1={k:raw[k]-nominal[k] for k in nominal}
    d2={k:receiver[k]-raw[k] for k in raw}
    return dict(nominal=nominal,rawIfcMeshBox=raw,receiverMeshBox=receiver,
        rawMinusNominal=d1,receiverMinusRaw=d2,
        rawTopDiffersFromNominal=abs(d1['topM'])>tolerance,
        rawHeightDiffersFromNominal=abs(d1['heightM'])>tolerance,
        receiverTopDiffersFromRaw=abs(d2['topM'])>tolerance,
        receiverHeightDiffersFromRaw=abs(d2['heightM'])>tolerance,
        comparisonToleranceM=tolerance)


def main():
    paths=[OUT/'R161-IFC-auditoria.json',OUT/'R161-Eberick-recepcao-auditoria.json']
    hashes={str(p):sha(p) for p in paths}
    raw=read(paths[0]);reception=read(paths[1]);by_id={r['revitId']:r for r in raw['rows']}
    rows=[]
    for p in reception['parts']:
        a=p['nominalBeamAssociation']
        if a is None:continue
        source=by_id[str(a['nativeId'])]
        values=compare_three(dict(topM=a['nativeTopM'],heightM=a['nativeHeightM']),source['geometry'],p['geometry'])
        rows.append(dict(nativeId=a['nativeId'],nativeMark=a['nativeMark'],receiverName=p['name'],receiverGuid=p['guid'],
            sourceIfcGuid=source['ifcGuid'],**values))
    assert hashes=={str(p):sha(p) for p in paths}
    raw_top={r['nativeId'] for r in rows if r['rawTopDiffersFromNominal']}
    new_height={r['nativeId'] for r in rows if r['receiverHeightDiffersFromRaw']}
    result=dict(revision='H03/R161',recordedAtUtc=datetime.now(timezone.utc).isoformat(),sources=hashes,
        associatedPartCount=len(rows),associatedOriginCount=len({r['nativeId'] for r in rows}),
        originsWithRawTopDifferentFromNominal=len(raw_top),
        originsWithAdditionalReceiverTopDifference=len({r['nativeId'] for r in rows if r['receiverTopDiffersFromRaw']}),
        originsWithAdditionalReceiverHeightDifference=len(new_height),
        additionalReceiverHeightDifferenceMarks=sorted({r['nativeMark'] for r in rows if r['receiverHeightDiffersFromRaw']}),
        rawExportDifferenceCauseNotIsolated=True,receiverHeightChangeAlgorithmNotIsolated=True,
        bboxHeightIsNotAnalyticalSectionForNonPrismaticSolids=True,
        unmatchedOriginsNotForceAssociated=reception['originsWithoutNominalSpatialAssociation'],
        completeBeamCoverageNotVerified=True,structuralApproval=False,rows=rows)
    (OUT/'R161-vigas-comparacao-tres-etapas.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('associatedOriginCount','originsWithRawTopDifferentFromNominal','originsWithAdditionalReceiverTopDifference','originsWithAdditionalReceiverHeightDifference','additionalReceiverHeightDifferenceMarks')}))


if __name__=='__main__':main()

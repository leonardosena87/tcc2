"""Consolida o ensaio real bruto sem promover o receptor a modelo aprovado."""
import json
import shutil
from datetime import datetime,timezone
from pathlib import Path

from auditar_exportacao import OUT,read,sha


def main():
    audit_path=OUT/'R161-Eberick-recepcao-auditoria.json'
    a=read(audit_path);native=read(OUT/'R161-IFC-auditoria.json')
    freeze=read(OUT/'R161-receptor-bruto-congelamento.json')
    copies=read(OUT/'R161-copias-receptores-preparadas.json')
    original_checks={b:sha(e['sourceProject'])==e['sourceProjectSha256'] for b,e in copies['branches'].items()}
    assert all(original_checks.values())
    bim=copies['branches']['BIM'];assert sha(bim['workingProject'])==bim['initialWorkingProjectSha256']
    assert sha(a['receiverProject'])==next(e['sha256'] for e in freeze['entries'] if e['relativePath'].endswith('.prj'))
    expected_beam=next(r for r in native['rows'] if r['mark']=='V16-ESC-PAT')
    landing_parts=[p for p in a['parts'] if p['nominalBeamAssociation'] and p['nominalBeamAssociation']['nativeId']==473802]
    assert len(landing_parts)==1
    raw_name=landing_parts[0]['name']
    ax=OUT/'R161-receptor-viga-patamar-AX.txt'
    text=ax.read_text(encoding='utf-8-sig')
    assert all(s in text for s in (f'Nome Value: {raw_name}','bw Value: 20','h Value: 30','/ Value: 0'))
    changed=[p for p in a['parts'] if p['nominalBeamAssociation'] and
        (abs(p['nominalBeamAssociation']['topDeltaM'])>1e-5 or abs(p['nominalBeamAssociation']['heightDeltaM'])>1e-5)]
    ids={p['nominalBeamAssociation']['nativeId'] for p in changed}
    obs=read(OUT/'R161-Eberick-recepcao-observacao.json')
    stage_path=OUT/'R161-vigas-comparacao-tres-etapas.json'
    stages=read(stage_path)
    result=dict(revision='H03/R161',recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        receiverRoot=a['receiverRoot'],receiverProject=a['receiverProject'],receiverProjectSha256=sha(a['receiverProject']),
        rawIfcInputSha256=next(v for p,v in native['sources'].items() if p.lower().endswith('.ifc')),
        importedOriginsByNativeReport=a['importedOriginsByReport'],importedOriginCount=a['importedOriginCount'],
        removedColumnsAbsentInReport=a['removedColumnOriginsAbsent'],
        landingBeamOriginReported=a['stairLandingBeamOriginReported'],
        landingBeamNativeName=raw_name,landingBeamRevitName=expected_beam['mark'],
        landingBeamNativeSectionReadBack=True,landingBeamReceiverPart=landing_parts[0],
        sourceNamedMaterials=native['buildingElementsWithNamedMaterial'],sourceMaterialMechanicalPropertiesAbsent=True,
        receiverProductCounts=a['receiverIfcProductCounts'],
        noNativeSlabOrStairSolidsInReceiverOutput=not a['stairOrSlabNativeSolidsPresent'],
        changedAssociatedBeamParts=len(changed),distinctOriginsWithChangedAssociatedBeamParts=len(ids),
        changedAssociatedBeamPartsDetails=changed,
        nominalDifferencesAreNotAllReceiverIntroduced=True,
        originsWithTopDifferenceAlreadyInRawIfc=stages['originsWithRawTopDifferentFromNominal'],
        originsWithAdditionalReceiverTopDifference=stages['originsWithAdditionalReceiverTopDifference'],
        originsWithAdditionalReceiverHeightDifference=stages['originsWithAdditionalReceiverHeightDifference'],
        unassociatedOrigins=a['originsWithoutNominalSpatialAssociation'],unmatchedReceiverBeamParts=a['unmatchedReceiverBeamParts'],
        unmatchedPartsNotCountedAsConfirmedCorrection=True,
        sourceR148ProjectsPreserved=original_checks,bimWorkingR161StillUnmodified=True,
        firstSavedReceiverPrjPreserved=True,
        partialReceptionElapsedMs=obs['savedObservation']['elapsedMs'],
        timeScope=obs['scope'],nativeReceiverClosedReopened=False,
        receptionTestCompleted=True,completeFlowComparisonCompleted=False,structuralCalculationPerformed=False,
        structuralApproval=False,correctionCountAndTimeNotFinal=True,
        sourceEvidence={str(audit_path):sha(audit_path),str(ax):sha(ax),str(stage_path):sha(stage_path)})
    target=OUT/'R161-recepcao-resultado.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    # Mantem estados historicos em arquivos datados, sem reescrever a preparacao.
    pointer=Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    backup=OUT/'R161-apontador-antes-recepcao.json'
    if not backup.exists():shutil.copy2(pointer,backup)
    p=read(pointer);p.update(currentNativeIfcR160EberickReceptionVerified=True,
        latestExperimentalR160ReceiverRoot=a['receiverRoot'],latestExperimentalR160ReceiverResultPath=str(target),
        latestExperimentalR160ReceiverResultSha256=sha(target),experimentalR160ReceiverIsMainCalculationModel=False,
        experimentalR160LandingBeamConverted=True,experimentalR160StairConverted=False,
        experimentalR160ReceiverCorrectionReviewPending=True)
    pointer.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
    shutil.copy2(pointer,OUT/'R161-apontador-apos-recepcao.json')
    lines=['# R161 — pendencias observadas na recepcao bruta','',
        'O conjunto abaixo e parcial: 12 origens associadas com diferencas em relacao aos parametros nominais do Revit. Os 12 desvios de topo ja existem na malha IFC bruta; nao representam 12 novos erros introduzidos pelo Eberick. Duas origens apresentam diferenca adicional de altura no receptor: V4A-N1 e V15-N1, de 0,02 m na caixa da malha bruta para 0,05 m na caixa receptora. Nao e o total final de correcoes. A associacao espacial nao prova conectividade analitica.', '',
        '| Origem Revit | Parte Eberick | Topo fonte (m) | Topo receptor (m) | Altura fonte (m) | Altura receptor (m) |',
        '|---|---|---:|---:|---:|---:|']
    for part in sorted(changed,key=lambda p:p['nominalBeamAssociation']['nativeMark']):
        b=part['nominalBeamAssociation']
        lines.append(f"| {b['nativeMark']} | {part['name']} | {b['nativeTopM']:.6f} | {b['receiverTopM']:.6f} | {b['nativeHeightM']:.6f} | {b['receiverHeightM']:.6f} |")
    lines+=['','## Investigacoes adicionais','',
        '- V9-N1 e V13-N1 nao foram associadas pelo criterio nominal: duas partes permanecem sem associacao devido aos limites longitudinais. Nao foram forcadas nem contadas como correcoes confirmadas.',
        '- 64 solidos de pilares correspondem a segmentacao do receptor; nao equivalem automaticamente a 64 pilares fisicos nem a duplicidades.',
        '- Nenhuma laje ou escada nativa aparece no IFC de controle; conferir lancamento e cargas na etapa de correcao.',
        '- Nove niveis recebidos pelo assistente, com seis IfcBuildingStorey na saida de controle; conferir funcao dos niveis auxiliares antes de simplificar.',
        '- Nome C25 no receptor nao comprova transferencia causal da resistencia: o IFC de entrada nao contem propriedades mecanicas de material.',
        '- Viga do patamar renomeada V1 no receptor. Seus 20 x 30 cm e elevacao zero foram relidos sem editar; a associacao por ID do relatorio e geometria evita comparar apenas os nomes.',
        '- Preservar bruto; executar correcoes em outra copia, medir intervalos e reexportar para conferir os efeitos.',
        '', 'Nenhum calculo estrutural foi executado neste receptor. Apoios, ancoragem, J4, cargas e ELU/ELS permanecem pendentes.']
    (OUT/'R161-pendencias-recepcao-bruta.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('importedOriginCount','changedAssociatedBeamParts','distinctOriginsWithChangedAssociatedBeamParts','landingBeamNativeName','partialReceptionElapsedMs')}))


if __name__=='__main__':main()

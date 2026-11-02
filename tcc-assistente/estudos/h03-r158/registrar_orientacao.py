"""Registra o requisito informado pelo usuário, sem presumir aprovação de seções."""
import json
import shutil
from datetime import datetime,timezone
from pathlib import Path
from preparar import OUT,archive,sha

def main():
    target=OUT/'R158-orientacao-viga-patamar.json'
    if target.exists():raise FileExistsError(target)
    candidate=OUT/'R158-candidato-comum.json'
    d=json.loads(candidate.read_text(encoding='utf-8'))
    beams=[e for e in d['addedElements'] if e['id']=='V16-ESC-PAT' and e['kind']=='beam']
    assert len(beams)==1 and len(d['retainedExistingElements'])==60
    record=dict(recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        exactUserMessage='o orientador disse que vai precisar de uma viga no patamar',
        source='Relato do usuário sobre orientação do orientador; não é aprovação técnica assinada',
        landingBeamRequired=True,appliesToBothCadAndBim=True,
        existingCandidatePath=str(candidate),existingCandidateSha256=sha(candidate),
        candidateBeam=beams[0],candidatePositionApprovedByAdvisor=False,
        candidateSectionApprovedByAdvisor=False,candidateColumnsApprovedByAdvisor=False,
        connectionsAndAnchorageVerified=False,structuralDimensioningCompleted=False,
        nativeGeometryAppliedByThisRecord=False,monographEdited=False,
        nextStep='Implantar e conferir solução comum de viga e apoios nos dois ramos; calcular e verificar ligações/ELU/ELS no Eberick.')
    target.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    current=Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    before=json.loads(current.read_text(encoding='utf-8'));assert before['activeRevision']=='H03/R153'
    backup=OUT/'R158-apontador-antes-orientacao.json';assert not backup.exists()
    shutil.copyfile(current,backup)
    before.update(landingBeamRequired=True,landingBeamRequirementSource=str(target),
        landingBeamRequirementSourceSha256=sha(target),landingBeamCandidatePath=str(candidate),
        landingBeamNativePlacementConfirmed=False,landingBeamStructuralDimensioningCompleted=False)
    current.write_text(json.dumps(before,ensure_ascii=False,indent=2),encoding='utf-8')
    shutil.copyfile(current,OUT/'R158-apontador-apos-orientacao.json')
    # O relógio monotônico final não foi observado antes da interrupção; não reconstruir.
    start=json.loads((OUT/'CAD-inicio.json').read_text(encoding='utf-8'))
    now=datetime.now(timezone.utc)
    elapsed=(now-datetime.fromisoformat(start['utc'].replace('Z','+00:00'))).total_seconds()*1000
    session=dict(start=start,endObservationUtc=now.isoformat(),elapsedUtcMs=elapsed,
        endMonotonicUnknown=True,status='Interrompida; aberturaDXF e zoom2D observados; sem DWG/reabertura/exportacao de retorno',
        includesHumanWaitingAndInterruption=True,lastCancelOutcomeNotConfirmed=True,
        cadNativeReturnValidated=False,usableForFlowRanking=False)
    (OUT/'CAD-sessao-interrompida.json').write_text(json.dumps(session,ensure_ascii=False,indent=2),encoding='utf-8')
    archive()
    print('Requisito de viga no patamar registrado nos dois fluxos; posição/seções continuam candidatas.')

if __name__=='__main__':main()

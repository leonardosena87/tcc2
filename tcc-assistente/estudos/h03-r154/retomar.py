"""Retoma referência original e verifica a proposta de concentrar o desnível."""
import hashlib
import json
import shutil
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
from time import perf_counter

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Escada-H03-R154-RETOMADA-ORIGINAL-NAO-EXECUTAR')
CURRENT=Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def split(indices):
    heights=[D('.185')]*16
    remainder=D('3.25')-D('.22')-sum(heights)
    for i in indices:heights[i-1]+=remainder/len(indices)
    elevations=[];z=D('.22')
    for h in heights:z+=h;elevations.append(z)
    assert z==D('3.25')
    return dict(enlargedRiserNumbers=indices,riserHeightsM=[float(h) for h in heights],
        finishedLandingM=float(elevations[7]),finishedUpperM=float(z),
        riserSpreadM=float(max(heights)-min(heights)),uniform=False,adopted=False)

def main():
    tick=perf_counter();start=datetime.now(timezone.utc).isoformat()
    if OUT.exists():raise FileExistsError(OUT)
    previous=json.loads(CURRENT.read_text(encoding='utf-8'))
    if previous['activeRevision']!='H03/R153':raise ValueError('Estado atual mudou; reler decisão antes de substituir')
    sources=[HERE.parent/'h03-r144/R144-escada.json',HERE.parent/'h03-r147/R147-planta.json',Path(previous['definitionPath'])]
    arq=json.loads(sources[0].read_text(encoding='utf-8'))['architecture']
    assert arq['finishedGroundM']==.22 and arq['finishedUpperM']==3.25 and arq['dimensionRiserInterpretedVisuallyM']==.185
    cases=[split([1,8]),split([1,9])]
    assert all(max(c['riserHeightsM'])==.22 and c['riserSpreadM']==.035 for c in cases)
    result=dict(revision='H03/R154',createdAtUtc=datetime.now(timezone.utc).isoformat(),
        userInstruction='faz o seguinte, volte como era antes no projeto original e subdivida a diferença na altura no primeiro degrau e no patamar.',
        decision=dict(currentReference='Traçado original com dois lances retos e patamar',
            previousSeventeenRiserCandidatesActive=False,originalFilesPreserved=True,
            requestedConcentratedCorrectionAcceptedAsSafeOrCompliant=False),
        originalAnnotation=arq,
        countHypothesis=dict(totalRisers=16,lower=8,upper=8,
            status='Hipótese compatível com sete intervalos de pisada por lance da referência gráfica; não levantamento executivo validado.'),
        arithmetic=dict(totalFinishedRiseM=3.03,annotatedRiseForSixteenM=2.96,unclosedDifferenceM=.07,
            equalShareAtTwoRisersM=.035,ordinaryRiserM=.185,enlargedRisersM=.22,
            firstPlusLandingMeaningRequiresClarification=True),
        interpretations=[dict(meaning='Primeiro espelho inferior e espelho que chega ao patamar',**cases[0]),
                         dict(meaning='Primeiro espelho de cada lance, incluindo a saída do patamar',**cases[1])],
        consequence='Ambas as interpretações fecham a soma criando dois espelhos de22cm entre outros de18,5cm. Fechamento altimétrico não equivale a adequação geométrica ou segurança.',
        requiredNextStep='Rever geometria com espelhos uniformes e critérios aplicáveis; não aprovar automaticamente concentrar35mm em dois pontos.',
        sourceFiles=[dict(path=str(p),sha256=sha(p)) for p in sources],
        researchReference=dict(url='https://pubmed.ncbi.nlm.nih.gov/32501252/',
            relevance='Pesquisa experimental sobre alteração de segurança de passada com espelhos inconsistentes; não é regra normativa local nem previsão quantitativa para35mm.'),
        nativeProjectsEdited=False,newStairOrLoadsApplied=False,nativeAppsUsed=False,finalApproval=False)
    OUT.mkdir();shutil.copyfile(CURRENT,OUT/'R154-definicao-anterior.json')
    target=OUT/'R154-retomada-original.json';target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    CURRENT.write_text(json.dumps(dict(activeRevision='H03/R154',activeChoice='Retomada da referência original; correção altimétrica em aberto',
        definitionPath=str(target),definitionSha256=sha(target),previousDefinitionPreservedAt=str(OUT/'R154-definicao-anterior.json'),
        concentratedCorrectionAdopted=False,nativePlacementResolved=False,nativeProjectsUpdated=False,finalApproval=False),ensure_ascii=False,indent=2),encoding='utf-8')
    assert all(sha(Path(s['path']))==s['sha256'] for s in result['sourceFiles'])
    assert json.loads(CURRENT.read_text(encoding='utf-8'))['definitionSha256']==sha(target)
    (OUT/'R154-tempo-script.json').write_text(json.dumps(dict(startUtc=start,endUtc=datetime.now(timezone.utc).isoformat(),durationMs=(perf_counter()-tick)*1000,
        scope='cálculo e atualização de definição; não tempo de fluxo ou esforço total da IA'),ensure_ascii=False,indent=2),encoding='utf-8')
    (HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    for p in OUT.iterdir():
        if p.is_file():shutil.copyfile(p,HERE/p.name)
    shutil.copyfile(HERE/'LEIA-ME-R154.md',OUT/'LEIA-ME-R154.md')
    manifest=[dict(path=p.name,sha256=sha(p)) for p in sorted(HERE.iterdir()) if p.is_file() and 'manifesto' not in p.name]
    for folder in (HERE,OUT):(folder/'R154-manifesto.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(dict(originalReferenceActive=True,unclosedDifferenceM=.07,twoRisersWouldBeCm=22,concentratedCorrectionApplied=False)))

if __name__=='__main__':main()

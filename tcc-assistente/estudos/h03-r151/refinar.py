"""Sensibilidade à posição da linha de percurso; preserva primeira hipótese R151."""
import json
from datetime import datetime,timezone
from estudar import HERE,OUT,candidate,draw,archive

def main():
    target=OUT/'R151-refinamento.json'
    if target.exists():raise FileExistsError(target)
    m=json.loads((HERE.parent/'h03-r147/R147-planta.json').read_text(encoding='utf-8'))['graphicalMeasurementsM']
    rows=[]
    for n,a in ((11,.77),(13,1.00)):
        for offset in (.50,.55):
            c=candidate(m['stairwellWidth'],m['flightStripWidth'],a,offset,n)
            c['availableLengthWithoutHallM']=m['upperTreadRun']+m['landingDepth']
            c['southGraphicalReserveM']=c['availableLengthWithoutHallM']-c['requiredStairLengthM']
            c['envelopeFitsGraphicalBox']=c['southGraphicalReserveM']>=0
            c['screeningBand63To65Cm']=.63<c['twoRisersPlusPitchM']<.65
            rows.append(c)
    selected=rows[3]
    data=dict(createdAtUtc=datetime.now(timezone.utc).isoformat(),
        reason='Primeira hipótese de 11 compensados é sensível à linha de percurso: a 55 cm, 2e+p ultrapassa a faixa de triagem de 65 cm. Esta faixa não é declaração de enquadramento legal.',
        selection='13 compensados + 2 retos em cada lado; extensão interna reta 1,00 m. Figura principal representa percurso a 55 cm.',
        scenarios=rows,candidateForFurtherChecks=selected,
        initialElevenWindersRetainedAsHistory=True,nativeApplied=False,legalApproval=False,
        remarks='50/55 cm são cenários paramétricos. Não são prova de posição normativa ou de atendimento após corrimão. A folga varia entre cenários pois a chegada é mantida e a extensão de lance acompanha a pisada.')
    target.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    draw(selected,m,'R151-compensada-refinada')
    archive()
    print(json.dumps([dict(winders=r['compensatedTreadIntervals'],offset=r['walklineOffsetFromInnerRailM'],pitch=r['walkingPitchAlongCurveM'],blondel=r['twoRisersPlusPitchM'],inner=r['minimumInnerBoundaryChordM'],reserve=r['southGraphicalReserveM']) for r in rows]))
if __name__=='__main__':main()

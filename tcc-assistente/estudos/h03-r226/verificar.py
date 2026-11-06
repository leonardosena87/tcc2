"""Reavalia a triagem com Md minimo nativo12 e armadura3/4; nao aprova ligacoes."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq

FCD=25/1.4
FYD=500/1.15
CENTRE=40.3
AREA=math.pi*8**2/4
GAUSS,WEIGHTS=np.polynomial.legendre.leggauss(4)


def capacity(near_count,far_count,n):
    """Flexao reta com concreto parabola-retangulo; pele desconsiderada."""
    b=h=300.;d=h-CENTRE
    def response(x):
        slope=min(.0035/x,.010/(d-x))
        lo=max(0.,x-.002/slope)
        def stress(y):
            eps=np.clip(slope*(x-y),0,.002)
            return .85*FCD*(1-(1-eps/.002)**2)
        y=(GAUSS+1)*(x-lo)/2+lo
        fc=b*(.85*FCD*lo+sum(WEIGHTS*stress(y))*(x-lo)/2)
        mc=b*(.85*FCD*lo*(h/2-lo/2)+sum(WEIGHTS*stress(y)*(h/2-y))*(x-lo)/2)
        for ybar,count in ((CENTRE,near_count),(d,far_count)):
            fs=count*AREA*(np.clip(210000*slope*(x-ybar),-FYD,FYD)-stress(ybar))
            fc+=fs;mc+=fs*(h/2-ybar)
        return fc/1000,mc/1e6
    x=brentq(lambda x:response(x)[0]-n,.001,d-1e-5)
    return response(x)[1]


def evaluate(source):
    result={}
    for branch in ('CAD','BIM'):
        checks=[]
        for old in source[branch]['checks']:
            lo,hi=old['n_interval']
            # Os dois sentidos verticais sao considerados porque3 e4 barras nao sao simetricos.
            positive=min(capacity(3,4,n) for n in (lo,hi))
            negative=min(capacity(4,3,n) for n in (lo,hi))
            vertical=min(positive,negative)
            # Somente os quatro cantos para resistencia horizontal; extras e pele ignorados.
            horizontal=min(capacity(2,2,n) for n in (lo,hi))
            minimum=12.
            index=max(minimum,old['mv_bound'])/vertical+old['mh_bound']/horizontal
            old_fourbar_index=max(minimum,old['mv_bound'])/horizontal+old['mh_bound']/horizontal
            checks.append(dict(combination=old['combination'],nIntervalKN=[lo,hi],
                positiveVerticalResistanceKNm=positive,negativeVerticalResistanceKNm=negative,
                horizontalFourCornerResistanceKNm=horizontal,
                mvBoundKNm=old['mv_bound'],mhBoundKNm=old['mh_bound'],nativeMinimumKNm=minimum,
                additionalConservativeLinearIndex=index,
                oldFourBarModelWithCorrected12KNmIndex=old_fourbar_index))
        result[branch]=dict(checks=checks,governing=max(checks,key=lambda r:r['additionalConservativeLinearIndex']),
            maxOldFourBarIndexWith12KNm=max(c['oldFourBarModelWithCorrected12KNmIndex'] for c in checks))
    result.update(nativeMinimumSource='R226 relatorios detalhados V1; piso12 nos dois sentidos',
        verticalResistanceModel='3/4 barras8, sem pele; menor resistencia dos dois sentidos e dos extremos axiais',
        horizontalResistanceModel='Somente4 barras de canto; armadura adicional desprezada',
        purpose='Triagem adicional linear; nao se atribui esta expressao a verificacao normativa biaxial completa',
        skinPositionAssumed=False,anchorageApproved=False,fullVerificationComplete=False,
        actualDemandChanged=False,minimumIsSensitivityFloorNotObservedSimultaneousDemand=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('out',type=Path);args=ap.parse_args()
    result=evaluate(json.loads(args.source.read_text(encoding='utf-8')))
    args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({b:dict(index=result[b]['governing']['additionalConservativeLinearIndex'],
        oldFourBarIndex=result[b]['maxOldFourBarIndexWith12KNm']) for b in ('CAD','BIM')}))

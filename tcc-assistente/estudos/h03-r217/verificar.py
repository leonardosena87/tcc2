"""Confronta a V1 de ambas as origens. Unidades de seção: N, mm, MPa; resultados: kN, kN.m."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import numpy as np
from scipy.optimize import brentq
from grelha import solve, parse, number, CASES

XML={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
FIELDS=('q','n_t','n_c','mvi','mvf','mvpos','mhi','mhf','mhpos','vvi','vvf','vhi','vhf','mt')
FCD=25/1.4
FYD=500/1.15
AS_FACE=2*math.pi*8**2/4
CENTRE=30+6.3+4  # Face externa do estribo, mm.
GAUSS,W=np.polynomial.legendre.leggauss(4)


def records(file):
    with ZipFile(file) as z:
        t=ET.fromstring(z.read('word/document.xml'))
    result={}
    for table in t.findall('.//w:tbl',XML):
        rows=table.findall('w:tr',XML)
        assert len(rows)==3
        label=''.join(rows[0].itertext()).removeprefix('CASO: ').strip()
        headers=[''.join(c.itertext()) for c in rows[1].findall('w:tc',XML)]
        assert [v.split('(')[0].replace(' ','') for v in headers]==['Elemento','Carga','NmáxNegNmáxPos','MxiMxf','MxMáx','MyiMyf','MyMáx','VxiVxf','VyiVyf','Mt']
        cells=rows[2].findall('w:tc',XML)
        assert ''.join(cells[0].itertext())=='V1'
        nums=[[''.join(p.itertext()).strip() for p in c.findall('w:p',XML)] for c in cells[1:]]
        assert list(map(len,nums))==[1,2,2,1,2,1,2,2,1] and label not in result
        result[label]=dict(zip(FIELDS,[number(v) for a in nums for v in a],strict=True))
    assert len(result)==87
    return result


def capacity(h,b,n):
    """Equilíbrio com concreto parábola-retângulo, dois pares simétricos de barras."""
    d=h-CENTRE
    def response(x):
        slope=min(.0035/x,.010/(d-x))
        lo=max(0.,x-.002/slope)
        # Integração exata das duas parcelas polinomiais, descontando concreto ocupado por aço.
        def stress(y):
            eps=np.clip(slope*(x-y),0,.002)
            return .85*FCD*(1-(1-eps/.002)**2)
        y=(GAUSS+1)*(x-lo)/2+lo
        fc=b*(.85*FCD*lo+sum(W*stress(y))*(x-lo)/2)
        mc=b*(.85*FCD*lo*(h/2-lo/2)+sum(W*stress(y)*(h/2-y))*(x-lo)/2)
        for ybar in (CENTRE,d):
            fs=AS_FACE*(np.clip(210000*slope*(x-ybar),-FYD,FYD)-stress(ybar))
            fc+=fs
            mc+=fs*(h/2-ybar)
        return fc/1000,mc/1e6
    x=brentq(lambda x:response(x)[0]-n,.001,d-1e-5)
    return response(x)[1]


def branch(grillage,doc,width_mm=200,height_mm=300,v1_bounds_cm=(451,539)):
    model=parse(grillage.read_text(encoding='cp1252'))
    rows=records(doc)
    combos={}
    for r in model['tables']['COMBINATION DEFINITIONS']:
        combos.setdefault(r['ComboName'],{})[r['CaseName']]=number(r['ScaleFactor'])
    if set(combos)!={k for k in rows if '+' in k and not k.endswith(')')}:
        raise ValueError('Combinações diferentes entre relatório e exportação')
    grid=solve(grillage,expected_v1_area_cm2=width_mm*height_mm/100,v1_bounds_cm=v1_bounds_cm)
    # A calibração nominal histórica e a conversão física diferem 1,93%.
    # Para a solicitação usar a maior das duas escalas. Não recalibrar por caso.
    force_factor=max(.01,.00980665)
    moment_factor=force_factor*.01
    errors=[]
    for c in ('G1','G2','Q'):
        row=next(v for k,v in rows.items() if k.endswith('('+c+')'))
        a=grid['segments'][0]['case_end_local'][c]; b=grid['segments'][-1]['case_end_local'][c]
        errors.extend([abs(-a[5]*moment_factor-row['mvi']),abs(b[11]*moment_factor-row['mvf'])])
    if max(errors)>.015:raise ValueError('Não reproduziu os momentos verticais de controle')
    checks=[]
    for label,co in combos.items():
        native=rows[label]
        points=[]
        for seg in grid['segments']:
            v=sum(co.get(c,0)*np.asarray(seg['case_end_local'][c]) for c in CASES)
            # A solicitação horizontal é linear em cada barra sem carga transversal distribuída.
            for i,vals in enumerate((v[:6],v[6:])):
                sign=-1 if i==0 else 1
                points.append(dict(x_cm=seg['x_cm'][i],mh=sign*vals[4]*moment_factor,
                                   vh=sign*vals[2]*force_factor,grid_axial=sign*vals[0]*force_factor,
                                   grid_torsion=sign*vals[3]*moment_factor))
        # Envoltória por combinação para uma seção constante. Magnitudes podem ocorrer em seções
        # distintas: trata-se de limite superior, nunca um vetor simultâneo observado.
        mh=max(abs(p['mh']) for p in points)+max(abs(native[k]) for k in ('mhi','mhf','mhpos'))+.005
        vh=max(abs(p['vh']) for p in points)+max(abs(native[k]) for k in ('vhi','vhf'))+.005
        axial_buffer=max(abs(p['grid_axial']) for p in points)+.005
        torsion_bound=max(abs(p['grid_torsion']) for p in points)+abs(native['mt'])+.005
        nlo=-abs(native['n_t'])-axial_buffer
        nhi=abs(native['n_c'])+axial_buffer
        mv=max(abs(native[k]) for k in ('mvi','mvf','mvpos'))+.005
        # Verificação do ramo de baixa compressão/tração. A linha de interação
        # usa um domínio convexo conservador com os mínimos dos dois extremos.
        rv=min(capacity(height_mm,width_mm,n) for n in (nlo,nhi))
        rh=min(capacity(width_mm,height_mm,n) for n in (nlo,nhi))
        checks.append(dict(combination=label,mv_bound=mv,mh_bound=mh,vv_bound=max(abs(native['vvi']),abs(native['vvf']))+.005,
                           vh_bound=vh,n_interval=[nlo,nhi],mrv_lower=rv,mrh_lower=rh,
                           utilization=mv/rv+mh/rh,with_native_min=max(8,mv)/rv+mh/rh,
                           torsion_bound=torsion_bound,
                           section_values=points))
    sensitivity=solve(grillage,shear_factor=5/6,expected_v1_area_cm2=width_mm*height_mm/100,v1_bounds_cm=v1_bounds_cm)
    sensitive_mh=0.
    sensitive_vh=0.
    for co in combos.values():
        for seg in sensitivity['segments']:
            v=sum(co.get(c,0)*np.asarray(seg['case_end_local'][c]) for c in CASES)
            sensitive_mh=max(sensitive_mh,abs(v[4])*moment_factor,abs(v[10])*moment_factor)
            sensitive_vh=max(sensitive_vh,abs(v[2])*force_factor,abs(v[8])*force_factor)
    return dict(reportSha256=hashlib.sha256(doc.read_bytes()).hexdigest(),
                grillageSha256=hashlib.sha256(grillage.read_bytes()).hexdigest(),rows=rows,checks=checks,
                controls=dict(vertical_abs_error_kNm=max(errors),relativeResidual=grid['relative_residual'],
                              shearSensitivity_kappa_5_over_6=dict(gridMhMax=sensitive_mh,gridVhMax=sensitive_vh)),
                governing=max(checks,key=lambda c:c['utilization']),
                governingWithMin=max(checks,key=lambda c:c['with_native_min']))


def detailing(branches):
    """Triagem normativa nas duas direções. Não gera aprovação nem detalhamento executivo."""
    checks=[c for b in branches for c in b['checks']]
    dv,dh=300-CENTRE,200-CENTRE
    av=math.pi*6.3**2/4
    fctm=.3*25**(2/3)
    fctd=.7*fctm/1.4
    # Modelo I, bielas a 45 graus. Valores em N/mm2 e mm.
    vrd2v=.27*(1-25/250)*FCD*200*dv/1000
    vrd2h=.27*(1-25/250)*FCD*300*dh/1000
    vv=max(c['vv_bound'] for c in checks)
    vh=max(c['vh_bound'] for c in checks)
    assert vv<.2*vrd2v and vh<.2*vrd2h
    smax=min(.6*dv,.6*dh,300)
    transverse_v=200-2*(30+6.3/2)
    transverse_h=300-2*(30+6.3/2)
    # Somente dois ramos, mesmo na hipótese com grampo intermediário.
    vswv=2*av/90*.9*dv*FYD/1000
    vswh=2*av/90*.9*dh*FYD/1000
    lb=8/4*FYD/(2.25*fctd)
    anchor_force_bound=max(c['vv_bound']+c['vh_bound']+max(0,-c['n_interval'][0]) for c in checks)
    anchor_ratio=anchor_force_bound*1000/(AS_FACE*FYD)
    lbmin=max(.3*lb,10*8,100)
    return dict(status='DETALHE_ATUAL_NAO_ATENDE_A_TRIAGEM_TRANSVERSAL',
                fullVerificationComplete=False, nativeModelChanged=False,
                dv_mm=dv,dh_mm=dh,vrd2_vertical_kN=vrd2v,vrd2_horizontal_kN=vrd2h,
                max_vv_kN=vv,max_vh_kN=vh,spacing_limit_mm=smax,current_spacing_mm=150,
                current_spacing_passes=150<=smax,trial_spacing_mm=90,trial_spacing_passes=90<=smax,
                transverse_leg_spacing_vertical_mm=transverse_v,
                transverse_leg_spacing_horizontal_mm=transverse_h,
                transverse_horizontal_limit_mm=dh,current_horizontal_leg_spacing_passes=transverse_h<=dh,
                trial_midheight_leg_spacing_mm=transverse_h/2,
                trial_midheight_leg_spacing_passes=transverse_h/2<=dh,
                trial_concrete_ignored_shear_index=max(c['vv_bound']/vswv+c['vh_bound']/vswh for c in checks),
                vrd2_linear_envelope_index=max(c['vv_bound']/vrd2v+c['vh_bound']/vrd2h for c in checks),
                anchorage=dict(fbd_MPa=2.25*fctd,basic_mm=lb,minimum_mm=lbmin,
                               trial_force_bound_kN=anchor_force_bound,trial_area_ratio=anchor_ratio,
                               straight_trial_required_mm=max(lb*anchor_ratio,lbmin),
                               hooked_trial_required_mm=max(.7*lb*anchor_ratio,lbmin),
                               nominal_available_mm=170,
                               status='NAO_FECHADA; triagem conservadora, sem comprovar distribuicao por barra, dobras, nos e apoios'),
                limitations=['Grelha R214 reconstruida linearmente; calibracao vertical nao valida a componente horizontal.',
                             'Sem verificacao completa de ELS, nos, ancoragens, compatibilidade de apoio ou contato com solo.',
                             'Envoltoria de flexao por combinacao; nao e vetor simultaneo de uma secao.',
                             'Indice com piso de momento vertical 8 kN.m e sensibilidade ao valor nativo, nao substitui todas as exigencias normativas.'])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('exports',type=Path);args=ap.parse_args()
    root=args.root
    files={'CAD':root/'CAD/Arquivos do projeto/Documentos/Eberick/Pav1_Vigas_Combinacoes.docx',
           'BIM':root/'Pav1_Vigas_Combinacoes.docx'}
    data={b:branch(next((args.exports/(b+'-generico')).glob('*escada*')),p) for b,p in files.items()}
    assert data['CAD']['rows'].keys()==data['BIM']['rows'].keys()
    diff=max(abs(v-data['BIM']['rows'][k][field]) for k,row in data['CAD']['rows'].items() for field,v in row.items())
    data['max_difference_printed_CAD_BIM']=diff
    data['detailing']=detailing([data['CAD'],data['BIM']])
    for b in files:
        g=data[b]['governing'];s=data[b]['governingWithMin']
        print(b,len(data[b]['checks']),'max_control_error',data[b]['controls'],'util',round(g['utilization'],4),
              'with_min',round(s['with_native_min'],4),'mh',round(g['mh_bound'],3),'vh',round(g['vh_bound'],3),
              'resistances',round(g['mrv_lower'],3),round(g['mrh_lower'],3),'combo',g['combination'])
    (root/'R217-resultados.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('max_native_difference',diff)


if __name__=='__main__':main()

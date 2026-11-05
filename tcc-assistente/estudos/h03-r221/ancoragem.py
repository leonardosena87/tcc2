"""Triagem complementar de ancoragem; nao aprova nem altera arquivos nativos."""
import argparse
import hashlib
import json
import math
from pathlib import Path


def force_bound(row):
    """Soma limites por combinacao; nao e vetor observado nem formula biaxial normativa.

    Inclui M/z nos dois planos, alem dos cortantes e tracao axial. Adota
    al/d=1 na triagem de Modelo I a 45 graus. A R217 somava apenas V+N.
    """
    return (row['mv_bound'] / (.9 * .2597)
            + row['mh_bound'] / (.9 * .1597)
            + row['vv_bound'] + row['vh_bound']
            + max(0., -row['n_interval'][0]))


def anchorage(force_kN, count, phi=8., normal_cover=30.):
    if force_kN < 0 or count < 2 or phi <= 0:
        raise ValueError('Forca, quantidade ou diametro invalido')
    fyd = 500 / 1.15
    fctd = .7 * .3 * 25**(2/3) / 1.4
    fbd = 2.25 * fctd  # Boa aderencia, a confirmar para cada barra.
    area = count * math.pi * phi**2 / 4
    ratio = force_kN * 1000 / (area * fyd)
    lb = max(phi/4 * fyd/fbd, 25*phi)
    alpha = .7 if normal_cover >= 3*phi else 1.
    minimum = max(.3*lb, 10*phi, 100.)
    centre = 30 + 6.3 + phi/2
    available = 200-centre  # Ate o eixo da dobra: nao ate o inicio da curva.
    clear = (200-2*centre)/(count-1)-phi
    clear_limit = max(20., phi, 1.2*25)
    required = max(alpha * lb * ratio, minimum)
    return dict(force_kN=force_kN, count=count, phi_mm=phi, area_mm2=area,
                area_utilization=ratio, fbd_MPa=fbd, basic_mm=lb,
                minimum_mm=minimum, hook_factor=alpha, required_mm=required,
                available_to_bend_axis_mm=available,
                projected_length_screen_pass=required<=available and ratio<=1,
                clear_spacing_mm=clear, clear_spacing_limit_mm=clear_limit,
                clear_spacing_pass=clear>=clear_limit,
                CA50_minimum_bend_pin_mm=5*phi, minimum_90deg_straight_tail_mm=8*phi,
                anchorage_approved=False)


def analyze(source):
    data=json.loads(source.read_text(encoding='utf-8'))
    branches={}
    for name in ('CAD','BIM'):
        checks=data[name]['checks']
        governing=max(checks,key=force_bound)
        force=force_bound(governing)
        branches[name]=dict(combinations=len(checks), governing=governing['combination'],
                            bounds={k:governing[k] for k in ('mv_bound','mh_bound','vv_bound','vh_bound','n_interval')},
                            trials=[anchorage(force,n) for n in (2,3,4)])
    return dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                source_revision='R217: esforcos nativos e grelha R214; nao e novo processamento R221',
                fullVerificationComplete=False, nativeProjectModifiedByScript=False,
                nativeRetainedChange='V1: 4 barras inferiores de 8 mm; superiores nativas preservadas',
                rejectedTrial='4 barras positivas superiores: nativo gerou 2 barras C90 sem continuidade completa nos apoios; opcao revertida',
                branches=branches,
                limitations=[
                    'Limite conservador que soma planos e posicoes por combinacao; nao representa distribuicao por barra.',
                    'Os comprimentos ate o eixo da dobra nao comprovam o desenvolvimento dentro do no.',
                    'Nao fecha armadura superior, pele, confinamento, dobras, contato com solo ou transferencia aos apoios.',
                    'Complemento transversal R218 continua externo e nao atualiza relacao nativa de aco.',
                    'Sem novo cronometro pareado ou contabilizacao de tokens nesta revisao.',
                ])


if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('source',type=Path); ap.add_argument('output',type=Path)
    args=ap.parse_args(); result=analyze(args.source)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,b in result['branches'].items():
        print(name, b['governing'])
        for t in b['trials']:
            print(t['count'], 'barras: indice',round(t['area_utilization'],4),'lbnec',round(t['required_mm'],2),'mm; aprovacao',t['anchorage_approved'])

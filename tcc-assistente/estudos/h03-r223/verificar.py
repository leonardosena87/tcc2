"""Reproduz a triagem R223, sem editar projetos nem aprovar a estrutura."""
import argparse
import importlib.util
import json
import math
import re
import sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / 'h03-r217'))
spec = importlib.util.spec_from_file_location('verificacao_r217', BASE / 'h03-r217/verificar.py')
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)

FYD = 500 / 1.15
FCD = 25 / 1.4
CENTRE = 30 + 6.3 + 4


def force_bound(row, horizontal_only=False):
    """Limites adicionais conservadores; nao e formula normativa biaxial."""
    value = row['mh_bound'] / (.9 * .2597) + row['vh_bound']
    if not horizontal_only:
        value += row['mv_bound'] / (.9 * .2597) + row['vv_bound']
    return value + max(0., -row['n_interval'][0])


def anchor(force, count, good_bond=True):
    if force < 0 or count < 2:
        raise ValueError('Forca ou quantidade invalida')
    fctd = .7 * .3 * 25 ** (2 / 3) / 1.4
    fbd = 2.25 * fctd * (1 if good_bond else .7)
    lb = max(8 / 4 * FYD / fbd, 25 * 8)
    ratio = force * 1000 / (count * math.pi * 8 ** 2 / 4 * FYD)
    minimum = max(.3 * lb, 10 * 8, 100)
    radius = (5 * 8 + 8) / 2
    # Mais conservador que comparar ate o eixo da dobra: desconta toda a curva.
    available = 300 - CENTRE - radius
    required = max(.7 * lb * ratio, minimum)
    return dict(force_bound_kN=force, count=count, steel_utilization=ratio,
                basic_mm=lb, minimum_mm=minimum, hooked_required_mm=required,
                available_before_bend_mm=available,
                screening_pass=bool(required <= available and ratio <= 1),
                straight_required_mm=max(lb * ratio, minimum),
                full_yield_hooked_mm=max(.7 * lb, minimum),
                bend_pin_mm=40, bend_axis_radius_mm=radius,
                straight_tail_min_mm=64,
                native_upper_hook_projection_mm=270,
                proposed_upper_hook_projection_mm=95,
                proposed_straight_tail_mm=95-radius,
                opposite_hook_tip_clearance_mm=300-2*CENTRE-95-100,
                opposite_hook_tip_clearance_limit_mm=20,
                one_stirrup_leg_yield_kN=math.pi*6.3**2/4*FYD/1000,
                anchorage_transverse_force_per_bar_kN=.25*math.pi*8**2/4*FYD/1000,
                good_bond_assumed=good_bond,
                anchorage_approved=False)


def transverse(checks):
    if not checks:
        raise ValueError('Sem combinacoes')
    d = 300 - CENTRE
    area = math.pi * 6.3 ** 2 / 4
    vrd2 = .27 * (1 - 25 / 250) * FCD * 300 * d / 1000
    vsw = 2 * area / 150 * .9 * d * FYD / 1000
    vv = max(c['vv_bound'] for c in checks)
    vh = max(c['vh_bound'] for c in checks)
    if max(vv, vh) >= .2 * vrd2:
        raise ValueError('Rever limite entre ramos para o nivel de cortante')
    shear_index = max((c['vv_bound'] + c['vh_bound']) / vsw for c in checks)
    leg_gap = 300 - 2 * (30 + 6.3 / 2)
    return dict(d_mm=d, current_spacing_mm=150, spacing_limit_mm=min(.6*d,300),
                spacing_pass=150 <= min(.6*d,300),
                leg_gap_mm=leg_gap, leg_gap_limit_mm=d, leg_gap_pass=leg_gap <= d,
                max_Vv_kN=vv, max_Vh_kN=vh, Vrd2_each_kN=vrd2,
                concrete_ignored_shear_capacity_each_kN=vsw,
                concrete_ignored_shear_linear_index=shear_index,
                concrete_strut_linear_index=max((c['vv_bound']+c['vh_bound'])/vrd2 for c in checks),
                screening_pass=bool(150 <= .6*d and leg_gap <= d and shear_index <= 1),
                extra_R218_cross_ties_required_by_this_screen=False)


def native_time(path):
    with ZipFile(path) as z:
        t = ET.fromstring(z.read('word/document.xml'))
    text = '\n'.join(''.join(p.itertext()) for p in t.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'))
    matches = re.findall(r'Tempo total de processamento:\s*(\d+):(\d+):(\d+)', text)
    if len(matches) != 1:
        raise ValueError('Duracao nativa ausente ou ambigua')
    h, m, s = map(int, matches[0])
    return dict(seconds=3600*h+60*m+s, source='Mensagens_da_analise.docx',
                metric='processamento nativo ELU + dimensionamento + ELS',
                full_workflow_time=False, sample_count=1)


def analyze(root):
    result = {}
    for name in ('CAD', 'BIM'):
        docs = root / name / 'Arquivos do projeto/Documentos/Eberick'
        grids = list((root / (name+'-generico')).glob('*escada*'))
        if len(grids) != 1:
            raise ValueError('Exportacao da escada ausente ou ambigua')
        b = previous.branch(grids[0], docs / 'Pav1_Vigas_Combinacoes.docx', 300, 300, (456,534))
        # O calculo resistente mantem somente os dois cantos por face, desprezando
        # o aco adicional nativo. Nao muda a armadura real 3/4/2x2.
        b['resistance_assumption'] = '2 barras de canto por face; aco adicional desprezado'
        b['native_time'] = native_time(docs / 'Mensagens_da_analise.docx')
        b['transverse'] = transverse(b['checks'])
        full = max(force_bound(c) for c in b['checks'])
        horizontal = max(force_bound(c, True) for c in b['checks'])
        b['anchor_screens'] = dict(upper_3=anchor(full,3), lower_4=anchor(full,4),
                                   side_2_each=anchor(horizontal,2),
                                   upper_3_poor_bond_sensitivity=anchor(full,3,False))
        b['minimum_steel'] = dict(minimum_mm2=.0015*300*300,
                                  upper_mm2=3*math.pi*16, lower_mm2=4*math.pi*16,
                                  horizontal_face_including_corners_mm2=4*math.pi*16)
        result[name] = b
    a, b = result['CAD']['rows'], result['BIM']['rows']
    if a.keys() != b.keys():
        raise ValueError('Casos e combinacoes nao equivalentes')
    result['max_native_printed_difference'] = max(abs(v-b[k][f]) for k,row in a.items() for f,v in row.items())
    result['status'] = 'TRIAGEM_30X30_FAVORAVEL; DETALHE_DE_ANCORAGEM_E_INTERFACES_NAO_LIBERADOS'
    result['fullVerificationComplete'] = False
    result['nativeProjectModifiedByScript'] = False
    result['limitations'] = [
        'A reconstrução linear da grelha exportada não reproduz toda a análise do Eberick.',
        'A calibração vertical não valida independentemente a componente horizontal.',
        'O gancho superior nativo de 27 cm não foi aceito como detalhe geométrico final.',
        'O gancho superior proposto de 9,5 cm é estudo complementar; não foi aplicado à armadura nativa.',
        'Boa aderência pressupõe concretagem convencional da seção de 30 cm e juntas compatíveis.',
        'Apoios AE1A/AE1B são idealizados; sapatas nativas de 30x30x20 não são fundações dimensionadas.',
        'Falta fechar nós, interferência entre barras, contato com solo, apoios e estados de serviço locais.',
        'Tempos nativos isolados não demonstram superioridade nem duração total de cada fluxo.',
    ]
    return result


if __name__ == '__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);args=ap.parse_args()
    data=analyze(args.root)
    (args.root/'R223-resultados.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name in ('CAD','BIM'):
        b=data[name]
        print(name,'native_seconds',b['native_time']['seconds'],'flex',b['governing']['utilization'],
              'flex_min8',b['governingWithMin']['with_native_min'],
              'shear',b['transverse']['concrete_ignored_shear_linear_index'])
    print('native_difference',data['max_native_printed_difference'])

"""Prepara cópia independente e plano CAD para lançar as vigas N2."""
from pathlib import Path
import hashlib
import json
import shutil
import sys

sys.path.insert(0,'D:/TCC/work/dxf-deps')
import ezdxf

OUT = Path('D:/TCC/outputs/H03-R233-CAD-VIGAS-N2-NAO-EXECUTAR')
SOURCE = OUT.parent/'H03-R232-CAD-PILARES-NAO-EXECUTAR/CAD'
DWG_ROOT = OUT.parent/'H03-R225-AUTORIA-COORDENACAO-NAO-EXECUTAR'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    path, = DWG_ROOT.glob('R225-CAD-N2-*-retorno.dxf')
    model = ezdxf.readfile(path)
    if model.units != 6:
        raise ValueError('Unidade CAD diferente de metro')
    beams = []
    for e in model.modelspace():
        if e.dxf.layer != 'N2_VIGAS':
            continue
        if e.dxftype() != 'LWPOLYLINE' or not e.closed:
            raise ValueError('Viga CAD não é polilinha fechada')
        tags = e.get_xdata('TCC_R225')
        record = json.loads(next(t.value for t in tags if t.code == 1000 and t.value.startswith('{')))
        if record['id'] != tags[0].value or record['kind'] != 'beam':
            raise ValueError('Identidade de viga inconsistente')
        if abs(record['b']-.2) > 1e-9 or abs(record['h']-.3) > 1e-9 or abs(record['z']-6.39) > 1e-9:
            raise ValueError('Seção/cota diferente da rodada N2')
        beams.append(record)
    if len(beams) != 14 or len({b['id'] for b in beams}) != 14:
        raise ValueError('Esperadas 14 vigas N2')
    if OUT.exists():
        raise FileExistsError(OUT)
    OUT.mkdir()
    shutil.copytree(SOURCE, OUT/'CAD')
    original, = (SOURCE/'Projeto Eberick').glob('*.prj')
    copied, = (OUT/'CAD/Projeto Eberick').glob('*.prj')
    if sha(original) != sha(copied):
        raise ValueError('Cópia inicial diferente')
    plan = dict(source=str(SOURCE),target=str(OUT/'CAD'),sourcePrjSha256=sha(original),
                cadDxf=str(path),cadDxfSha256=sha(path),beams=beams,
                scope='Lançamento das 14 vigas N2 a partir do CAD, sem alterar as demais cotas')
    (OUT/'R233-preparacao.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in plan.items() if k != 'beams'},ensure_ascii=False))


if __name__ == '__main__':
    prepare()

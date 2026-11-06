"""Consolida o ensaio nativo de continuidade; nao dimensiona nem aprova ancoragens."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def doc_text(path):
    with ZipFile(path) as archive:
        root = ET.fromstring(archive.read('word/document.xml'))
    return '\n'.join(''.join(p.itertext()) for p in root.findall('.//' + W + 'p'))


def processing(text):
    times = re.findall(r'Tempo total de processamento:\s*(\d{2}):(\d{2}):(\d{2})', text)
    if len(times) != 1:
        raise ValueError('Tempo total nativo ausente ou ambiguo')
    h, m, s = map(int, times[0])
    if m >= 60 or s >= 60:
        raise ValueError('Tempo nativo invalido')
    sizing = text.split('DIMENSIONAMENTO DOS ELEMENTOS', 1)[1].split('CÁLCULO DAS FLECHAS', 1)[0]
    status = re.findall(r'(Pilares|Vigas|Lajes|Sapatas):\s*(\d+)\s*(Com sucesso|com erro)', sizing)
    if not status:
        raise ValueError('Situacao de dimensionamento ausente')
    return dict(nativeTotalSeconds=3600*h+60*m+s,
                sizingRows=[dict(kind=k, count=int(n), status=v) for k, n, v in status],
                successfulAutomaticSizingIsStructuralApproval=False)


def detail(text):
    if 'fck = 25.00 MPa' not in text or 'Cobrimento = 3.00 cm' not in text:
        raise ValueError('Material ou cobrimento divergente')
    md = [float(x) for x in re.findall(r'\bMd\s*=\s*([-+]?\d+\.\d+)', text)]
    if md != [8., 13.16, 0., 0., 8.01]:
        raise ValueError('Momentos de dimensionamento mudaram; requer nova avaliacao')
    positive, negative = text.split('DIMENSIONAMENTO DA ARMADURA NEGATIVA', 1)
    negative = negative.split('DIMENSIONAMENTO DA ARMADURA TRANSVERSAL', 1)[0]
    if len(re.findall(r'2ø10\.0\s*-\s*1\.57 cm²', negative)) != 2:
        raise ValueError('Dois apoios com 2phi10 nao confirmados')
    if '(2ø8.0 - 1.01 cm²)' not in positive:
        raise ValueError('Armadura inferior esperada nao confirmada')
    areas = [float(x) for x in re.findall(r"(?<!\w)As\s*=\s*(\d+\.\d+) cm²", negative)]
    if len(areas) != 6 or areas[0] != areas[1] or areas[2:4] != [0., 0.]:
        raise ValueError('Estrutura dos campos de area negativa mudou')
    return dict(materialMPa=25, coverCm=3, MdKNm=md,
                upperAtBothSupports='2phi10 - 1.57 cm2', lower='2phi8 - 1.01 cm2',
                upperBendingRequiredCm2=[areas[0], areas[4]],
                upperFinalRequiredCm2=[areas[1], areas[5]],
                printedCrackMm=[float(x) for x in re.findall(r'\bfiss\s*=\s*(\d+\.\d+)', text)],
                VdKN=[float(x) for x in re.findall(r'\bVd\s*=\s*(\d+\.\d+)', text)],
                continuousBarGeometrySource='Capturas nativas apos detalhar, nao deduzida somente do relatorio')


def anchorage_screen(report):
    """Triagem da projeção horizontal da barra até o início da curva."""
    diameter = 10.
    provided_area = 2*math.pi*diameter**2/4
    fctd = .7*.3*report['materialMPa']**(2/3)/1.4
    radius = 3*diameter  # Pino de 5φ, mais meia bitola para obter o raio de eixo.
    results = {}
    for condition, bond_factor in [('good', 1.), ('poor', .7)]:
        fbd = 2.25*bond_factor*fctd
        basic = max(diameter*500/1.15/(4*fbd), 25*diameter)
        rows = {}
        for i, (side, width) in enumerate([('left', 300.), ('right', 200.)]):
            available = width - 10*report['coverCm'] - 6.3 - diameter/2 - radius
            minimum = max(.3*basic, 10*diameter, 100., radius+5.5*diameter, 60.)
            bending = max(minimum, .7*basic*100*report['upperBendingRequiredCm2'][i]/provided_area)
            final = max(minimum, .7*basic*100*report['upperFinalRequiredCm2'][i]/provided_area)
            rows[side] = dict(availableToStartOfBendMm=available,
                              bendingAreaRequiredLengthMm=bending,
                              finalAreaSensitivityLengthMm=final,
                              bendingAreaMarginMm=available-bending,
                              finalAreaSensitivityMarginMm=available-final)
        results[condition] = dict(basicStraightMm=basic, sides=rows)
    return dict(bondConditions=results, assumedCoverNormalToHookAtLeast3Phi=True,
                assumedBendPinMm=5*diameter, actualCageAndPourJointVerified=False,
                finalAreaSensitivityIsNotNormativeAdoption=True,
                includesSupportNodeForceTransferVerification=False,
                references=['NBR 6118:2026 9.3, 9.4.2, 18.3.2.4.1',
                            'R227 Eberick: áreas de flexão e finais em cada nó'],
                conclusion='Conferir apoio direito de 20 cm e interferência das dobras no nó')


def main(root):
    source = root.parent/'H03-R224-FECHAMENTO-DETALHES-NAO-EXECUTAR'
    reference = json.loads((source/'R224-integridade.json').read_text(encoding='utf-8'))
    branches = {}
    for original in reference['projects']:
        b = original['branch']
        if sha(source/original['path']) != original['sha256']:
            raise ValueError('Original R224 alterado')
        project = root/original['path']
        with ZipFile(project) as archive:
            if archive.testzip():
                raise ValueError('CRC do PRJ invalido')
        report = root/f'{b}-cobertura-calculo-pos-processamento.docx'
        messages = root/f'{b}-mensagens-analise-R227.docx'
        d, p = doc_text(report), doc_text(messages)
        report.with_suffix('.txt').write_text(d, encoding='utf-8')
        messages.with_suffix('.txt').write_text(p, encoding='utf-8')
        verified_detail = detail(d)
        native_results = (root/f'{b}-resultados-nativos.txt').read_text(encoding='utf-8')
        if 'Total = 114.47 tf' not in native_results:
            raise ValueError('Resultado global desta rodada nao confirmado')
        branches[b] = dict(project=original['path'], sha256=sha(project), crc='OK',
                           sourceR224Preserved=True, sourceR224Sha256=original['sha256'],
                           sizingReportSha256=sha(report), processingReportSha256=sha(messages),
                           detail=verified_detail, processing=processing(p),
                           upperAnchorageScreen=anchorage_screen(verified_detail),
                           nativeGlobalObserved=dict(totalVerticalTf=114.47, maxGammaZ=1.06,
                               maxHorizontalWindDisplacementCm={'CAD':.15,'BIM':.16}[b],
                               nativeLoadPerAreaWarningStillDisplayed=True))
    out = dict(revision='R227', branches=branches,
        appliedThroughNativeInterface=True, binaryEngineeringFilesPatched=False,
        observedGeometry='20x30cm, topo6.39m, comprimento335cm, vao livre285cm',
        nativeDrawing='2N3phi10 C375, trecho329, ganchos29/22cm; 2N2phi8 C345; 19N1phi6.3c15',
        improvement='Armadura superior continua; removida a interrupcao da barra adicional curta',
        coverWarning08StillDisplayed=True, anchorageAndNodeCongestionApproved=False,
        independentCompleteInvertedMomentEnvelopeVerification=False,
        globalWorkflowTimingSeconds=None, pairedProductivityRankingComplete=False,
        aiTokensMeasured=None, exclusiveHumanEditingTimeSeconds=None,
        fullVerificationComplete=False, structuralApproval=False)
    (root/'R227-consolidacao.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({b:dict(time=v['processing']['nativeTotalSeconds'], detail=v['detail']) for b,v in branches.items()}, ensure_ascii=False))
    return out


def preserve(root, target, result):
    files = {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob('*'))
             if p.is_file() and not p.name.startswith('~$')
             and not p.name.endswith(('.tmp', '-tmp'))
             and p.name not in {'R227-manifesto.json', 'R227-backup.json'}}
    for branch in result['branches'].values():
        if files.get(branch['project']) != branch['sha256']:
            raise ValueError('PRJ mudou antes do backup')
    manifest = json.dumps(files, indent=2, ensure_ascii=False)+'\n'
    with ZipFile(target, 'x', ZIP_DEFLATED) as archive:
        for name in files:
            archive.write(root/name, name)
        archive.writestr('R227-manifesto.json', manifest)
    with ZipFile(target) as archive:
        if archive.testzip():
            raise ValueError('CRC do backup invalido')
        for name, digest in files.items():
            if hashlib.sha256(archive.read(name)).hexdigest() != digest:
                raise ValueError(f'Arquivo divergente no backup: {name}')
    (root/'R227-manifesto.json').write_text(manifest, encoding='utf-8')
    backup = dict(path=str(target), bytes=target.stat().st_size, sha256=sha(target),
                  verifiedFiles=len(files), crc='OK', bothNativeProjectsIncluded=True)
    (root/'R227-backup.json').write_text(json.dumps(backup, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(backup))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('--backup', type=Path)
    args = parser.parse_args()
    result = main(args.root)
    if args.backup is not None:
        preserve(args.root, args.backup, result)

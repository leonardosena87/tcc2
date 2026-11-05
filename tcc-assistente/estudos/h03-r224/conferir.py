"""Compara os relatorios nativos da cobertura; nao altera PRJ nem dimensiona barras."""
import argparse
import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
FIELDS = ('q', 'n_t', 'n_c', 'mvi', 'mvf', 'mvpos', 'mhi', 'mhf', 'mhpos',
          'vvi', 'vvf', 'vhi', 'vhf', 'mt')
HEADERS = ('Elemento', 'Carga', 'NmáxNegNmáxPos', 'MxiMxf', 'MxMáx',
           'MyiMyf', 'MyMáx', 'VxiVxf', 'VyiVyf', 'Mt')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def records(path, element):
    with ZipFile(path) as z:
        document = ET.fromstring(z.read('word/document.xml'))
    result = {}
    for table in document.findall('.//' + W + 'tbl'):
        rows = table.findall(W + 'tr')
        if len(rows) != 5:
            raise ValueError('Esperavam-se tres trechos em cada tabela')
        label = ''.join(rows[0].itertext()).removeprefix('CASO: ').strip()
        if not label or label in result:
            raise ValueError('Caso vazio ou repetido')
        headers = [''.join(c.itertext()).split('(')[0].replace(' ', '')
                   for c in rows[1].findall(W + 'tc')]
        if tuple(headers) != HEADERS:
            raise ValueError('Cabecalho ou unidades do relatorio mudaram')
        segments = []
        for index, row in enumerate(rows[2:], 1):
            cells = row.findall(W + 'tc')
            if ''.join(cells[0].itertext()) != f'{element} - {index}':
                raise ValueError('Elemento ou ordem de trechos inesperados')
            numbers = [[''.join(p.itertext()).strip()
                        for p in c.findall(W + 'p')] for c in cells[1:]]
            if list(map(len, numbers)) != [1, 2, 2, 1, 2, 1, 2, 2, 1]:
                raise ValueError('Quantidade de valores inesperada')
            values = [float(v.replace(',', '.')) for cell in numbers for v in cell]
            segments.append(dict(zip(FIELDS, values, strict=True)))
        result[label] = segments
    # Vento X+ tambem contem '+': casos simples terminam com o codigo entre parenteses.
    if len(result) != 87 or sum(not label.endswith(')') for label in result) != 68:
        raise ValueError('Esperavam-se 19 casos e 68 combinacoes')
    return result


def compare(cad, bim):
    if cad.keys() != bim.keys():
        raise ValueError('Casos ou combinacoes diferentes')
    differences = []
    for label in cad:
        if len(cad[label]) != len(bim[label]):
            raise ValueError('Quantidade de trechos diferente')
        for i, (a, b) in enumerate(zip(cad[label], bim[label], strict=True), 1):
            for field in FIELDS:
                value = abs(a[field] - b[field])
                if value:
                    differences.append(dict(case=label, segment=i, field=field,
                                            CAD=a[field], BIM=b[field], difference=value))
    return dict(comparedValues=len(cad)*3*len(FIELDS),
                differingValues=len(differences),
                maxPrintedAbsoluteDifference=max((d['difference'] for d in differences), default=0.),
                differences=differences, samePrintedValues=not differences,
                normativeOrStructuralApproval=False)


def analyze(root):
    data = {}
    for name, element in [('CAD', 'V13_1'), ('BIM', 'V3')]:
        path = root / name / 'Arquivos do projeto/Documentos/Eberick/Pav3_Vigas_Combinacoes.docx'
        rows = records(path, element)
        combos = {k: v for k, v in rows.items() if not k.endswith(')')}
        extrema = {}
        for field in FIELDS:
            values = [(r[field], label, i) for label, segments in combos.items()
                      for i, r in enumerate(segments, 1)]
            low, high = min(values), max(values)
            extrema[field] = dict(minimum=low[0], minimumCase=low[1], minimumSegment=low[2],
                                  maximum=high[0], maximumCase=high[1], maximumSegment=high[2])
        data[name] = dict(element=element, report=path.relative_to(root).as_posix(),
                          sha256=sha(path), cases=19, combinations=68,
                          segmentsPerCase=3, rows=rows, extrema=extrema)
    data['comparison'] = compare(data['CAD']['rows'], data['BIM']['rows'])
    data['scope'] = 'Tres subdivisoes de carregamento de um vao; nao tres vaos independentes'
    data['nativeReinforcement'] = dict(upperContinuous='2 N4 fi8 C376; trecho329; ganchos24/27cm',
        upperLeftAdditional='1 N3 fi8 C109; trecho87; gancho24cm',
        lower='2 N2 fi8 C345; trecho329; ganchos10/10cm', stirrups='19 N1 fi6.3 C88 c15')
    data['nativeReinforcementSource'] = 'Capturas CAD/BIM-cobertura-antes.png; leitura visual, nao extracao do PRJ'
    data['warning08Resolved'] = False
    data['nativeReinforcementModified'] = False
    data['fullVerificationComplete'] = False
    data['newNativeProcessingTimingSeconds'] = None
    return data


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('root', type=Path); args = ap.parse_args()
    result = analyze(args.root)
    (args.root/'R224-cobertura-comparacao.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result['comparison'], ensure_ascii=False))

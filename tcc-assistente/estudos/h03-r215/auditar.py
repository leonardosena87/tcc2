"""Extrai esforços simultâneos dos apoios; não dimensiona a viga ou fundações."""
import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
FIELDS = ('N', 'Mx', 'My', 'Vx', 'Vy', 'Mt')


def cell_text(cell):
    return ''.join(t.text or '' for t in cell.findall('.//w:t', NS)).strip()


def run(root):
    source = root / 'BIM/Arquivos do projeto/Documentos/Eberick/Pav1_Fundacao_Combinacoes.docx'
    with ZipFile(source) as archive:
        document = ET.fromstring(archive.read('word/document.xml'))
    elements = {}
    text = []
    for table in document.findall('.//w:tbl', NS):
        rows = [[cell_text(c) for c in row.findall('w:tc', NS)]
                for row in table.findall('w:tr', NS)]
        if not rows or not rows[0] or not rows[0][0].startswith('Fundação '):
            continue
        name = rows[0][0].removeprefix('Fundação ')
        if name in elements:
            raise ValueError('Elemento duplicado')
        if len(rows[1]) != 7 or rows[1][0] != 'Combinação':
            raise ValueError('Cabeçalho inesperado')
        expected = ['N', 'Mx', 'My', 'Vx', 'Vy', 'Mt']
        if any(not header.startswith(field) for header, field in zip(rows[1][1:], expected)):
            raise ValueError('Ordem de colunas inesperada')
        parsed = []
        for row in rows[2:]:
            if len(row) != 7:
                raise ValueError('Linha incompleta')
            entry = dict(label=row[0], kind='combination' if row[0].startswith('G1+') else 'case',
                         **dict(zip(FIELDS, (float(v.replace(',', '.')) for v in row[1:]))))
            if any(x['label'] == entry['label'] for x in parsed):
                raise ValueError('Caso/combinação repetido')
            parsed.append(entry)
        elements[name] = dict(headers=rows[1], rows=parsed,
                              caseCount=sum(x['kind'] == 'case' for x in parsed),
                              combinationCount=sum(x['kind'] == 'combination' for x in parsed),
                              extrema={field: max(parsed, key=lambda x: abs(x[field])) for field in FIELDS})
        text.extend(' | '.join(row).rstrip() for row in rows)
    if set(elements) != {'SAE1A', 'SAE1B'}:
        raise ValueError('Seleção diferente dos dois apoios da escada')
    a, b = (elements[name]['rows'] for name in ('SAE1A', 'SAE1B'))
    if [x['label'] for x in a] != [x['label'] for x in b]:
        raise ValueError('Conjuntos de combinações não correspondentes')
    pairs = [dict(label=x['label'], kind=x['kind'],
                  summedComponents={f: round(x[f] + y[f], 8) for f in FIELDS}) for x, y in zip(a, b)]
    record = dict(revision='H03-R215', sourceName=source.name,
                  sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  elements=elements, simultaneousPairs=pairs,
                  componentsUseGlobalAxes=True,
                  nativeMtHeaderKeptDespiteDimensionalAmbiguity=True,
                  foundationCombinationsNotSilentlyClassifiedAsBeamELU=True,
                  beamBiaxialSectionVerified=False, geotechnicalValidation=False,
                  structuralApproval=False)
    (root / 'R215-esforcos-apoios.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (root / 'BIM-R215-esforcos-base.txt').write_text('\n'.join(text) + '\n', encoding='utf-8')
    print(json.dumps({k: dict(cases=v['caseCount'], combinations=v['combinationCount'],
                             maxAbsVx=v['extrema']['Vx'], maxAbsMy=v['extrema']['My'])
                      for k, v in elements.items()}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    run(parser.parse_args().folder)

"""Compara tabelas geradas pelo Eberick sem reconciliar direcoes por suposicao."""
import hashlib
import importlib.util
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path('D:/TCC/outputs')
OUT = ROOT / 'Relatorios-H03-R107-CONSULTA-NAO-EXECUTAR'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
FLOORS = {'CAD': {'N0': 'N0', 'N1': 'N1', 'N2': 'N2'},
          'BIM': {'TCC-cdd31967-N0': 'N0', 'TCC-cdd31967-N1': 'N1', 'TCC-cdd31967-N2': 'N2'}}
DIRECTIONS = ['X+', 'X-', 'Y+', 'Y-']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tables(path):
    with ZipFile(path) as z:
        body = ET.fromstring(z.read('word/document.xml')).find('w:body', NS)
    tables = [[[ ' '.join(t.text or '' for t in cell.findall('.//w:t', NS))
                for cell in row.findall('w:tc', NS)] for row in table.findall('w:tr', NS)]
              for table in body.findall('w:tbl', NS)]
    return [t for t in tables if any(cell.strip() for row in t for cell in row)]


def normalize_tables(tables, branch):
    """Somente os tres nomes de pavimento explicitamente conhecidos sao pareados."""
    if len(tables) != 4:
        raise ValueError('Esperadas quatro tabelas de dados')
    expected_sizes = [(6, 5), (5, 6), (5, 6), (5, 7)]
    result = []
    for i, (table, (nrows, ncols)) in enumerate(zip(tables, expected_sizes)):
        if len(table) != nrows or any(len(row) != ncols for row in table):
            raise ValueError('Estrutura de tabela inesperada')
        if i == 0:
            if table[0][1:] != ['Vento ' + d for d in DIRECTIONS]:
                raise ValueError('Cabecalho de direcoes inesperado')
        elif i in (1, 2):
            start = 2 if i == 1 else 1
            if table[1][start:start+4] != ['Vento ' + d for d in DIRECTIONS]:
                raise ValueError('Direcoes ausentes ou reordenadas')
        normalized = [list(row) for row in table]
        if i:
            seen = []
            for row in normalized[2:]:
                if row[0] not in FLOORS[branch]:
                    raise ValueError('Pavimento sem correspondencia explicita')
                seen.append(FLOORS[branch][row[0]])
                row[0] = FLOORS[branch][row[0]]
            if seen != ['N2', 'N1', 'N0']:
                raise ValueError('Ordem ou conjunto de pavimentos inesperado')
        result.append(normalized)
    return result


def literal_check(normalized, relative, branch):
    floor = FLOORS[branch][relative['floorNative']]
    row = next(r for r in normalized[2][2:] if r[0] == floor)
    value = float(row[1 + DIRECTIONS.index(relative['direction'])])
    maxima = max(float(c) for r in normalized[2][2:] for c in r[1:5])
    return {'floor': floor, 'summaryDirection': relative['direction'], 'summaryValueCm': relative['valueCm'],
            'sameLabelTableValueCm': value, 'sameLabelDisplayedValueMatches': value == relative['valueCm'],
            'tableDisplayedMaximumCm': maxima, 'interpretation': 'Comparacao literal de rotulos; causa e semantica nao reconciliadas.',
            'softwareBugDemonstrated': False}


def main():
    if (OUT / 'R107-resultado.json').exists():
        raise FileExistsError('Nao substituir resultado anterior')
    spec = importlib.util.spec_from_file_location('r106', Path(__file__).parents[1] / 'h03-r106/consolidar.py')
    r106 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r106)
    original = json.loads((ROOT / 'Deslocamentos-H03-R106-EXPLORATORIO-NAO-EXECUTAR/R106-resultado.json').read_text(encoding='utf-8'))
    branches = {}
    frozen = OUT / 'congelados-apos-relatorios'
    frozen.mkdir()
    for branch in ['CAD', 'BIM']:
        docx = OUT / f'{branch}-DeslocamentosHorizontais-nativo.docx'
        tables = read_tables(docx)
        normalized = normalize_tables(tables, branch)
        summary = r106.summary((OUT / f'{branch}-resumo-regenerado-UI.txt').read_text(encoding='utf-8'))
        src = ROOT / ('R107-' + branch)
        dst = frozen / branch
        shutil.copytree(src, dst)
        hashes = [{'relativePath': p.relative_to(src).as_posix(), 'sha256': sha(p)} for p in src.rglob('*') if p.is_file()]
        if not all(sha(dst / row['relativePath']) == row['sha256'] for row in hashes):
            raise ValueError('Copia congelada divergente')
        branches[branch] = {'tablesNative': tables, 'tablesNormalized': normalized, 'docxPath': str(docx),
                            'docxSha256': sha(docx), 'summary': summary,
                            'summaryMatchesOwnR106': summary == original['branches'][branch]['summary'],
                            'literalSummaryTableComparison': literal_check(normalized, summary['relative'], branch),
                            'projectPath': str(src / f'H03-{branch}-NAO-EXECUTAR.prj'),
                            'prjSha256': sha(src / f'H03-{branch}-NAO-EXECUTAR.prj'), 'frozenFiles': hashes,
                            'sessionTime': json.loads((OUT / f'{branch}-sessao-tempo.json').read_text()),
                            'processingTimeObservation': json.loads((OUT / f'{branch}-processamento-tempo.json').read_text())}
    protected = []
    for row in json.loads((OUT / 'R107-antes.json').read_text(encoding='utf-8')):
        p = Path(row['path'])
        current = sha(p) if p.exists() else None
        protected.append({**row, 'afterSha256': current, 'unchanged': current == row['sha256']})
    if not all(r['unchanged'] for r in protected if r['path'].endswith('.prj')):
        raise ValueError('PRJ original R106 alterado')
    cad, bim = branches['CAD']['tablesNormalized'], branches['BIM']['tablesNormalized']
    cells = [{'table': i+1, 'row': j+1, 'column': k+1, 'CAD': x, 'BIM': y, 'equal': x == y}
             for i, (ct, bt) in enumerate(zip(cad, bim)) for j, (cr, br) in enumerate(zip(ct, bt))
             for k, (x, y) in enumerate(zip(cr, br)) if re.fullmatch(r'\d+\.\d+', x)]
    result = {'revision': 'H03/R107', 'createdAtUtc': datetime.now(timezone.utc).isoformat(), 'branches': branches,
              'allFourTablesEqualAfterExplicitFloorMapping': cad == bim, 'numericCellComparisons': cells,
              'originalR106Files': protected, 'originalR106PrjsUnchanged': True,
              'reprocessingReason': 'Relatorio bloqueado por pasta da edificacao; salvar como nova copia desativou resultados. Regeneracao somente nas copias R107.',
              'criticalDirectionReconciled': False, 'transferDefectDemonstrated': False,
              'finalStructuralApproval': False, 'finalRankingAllowed': False,
              'limits': ['Cargas e vento ainda parciais; rigidez configurada, sem dimensionamento final.',
                         'Igualdade de quatro tabelas arredondadas nao demonstra equivalencia global.',
                         'Relatorio e resumo preservados sem correcao de seus rotulos; causa desconhecida.',
                         'Centros de rigidez em branco nao sao zero nem validacao de diafragma rigido.',
                         'Sessao CAD inclui lacuna de conversa de varias horas. Tempos de recuperacao nao sao produtividade.']}
    (OUT / 'R107-resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'tablesEqual': cad == bim, 'numericCellsEqual': sum(r['equal'] for r in cells), 'numericCells': len(cells),
                      'originalPrjsUnchanged': True, 'otherOriginalFilesChanged': [r['path'] for r in protected if not r['unchanged']],
                      'literalChecks': {b: v['literalSummaryTableComparison'] for b, v in branches.items()}}, ensure_ascii=False))


if __name__ == '__main__':
    main()

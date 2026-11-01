"""Compara registros textuais exportados preservando associação por barra e multiplicidade."""
import importlib.util
import json
import re
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from time import perf_counter

HERE = Path(__file__).parent
SOURCE = HERE.parent / 'h03-r122'
OUT = Path('D:/TCC/outputs/Comparacao-Analitica-H03-R123-SOMENTE-LEITURA')
spec = importlib.util.spec_from_file_location('r122', SOURCE / 'consolidar.py')
r122 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r122)
NUM = re.compile(r'^[+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+)(?:[eE][+-]?\d+)?$')
IDENTIFIERS = {'SectionName', 'AnalSect', 'Material', 'LoadPat', 'LoadName', 'CaseName', 'Case', 'ComboName', 'ProgramName', 'Version'}


def normalize_value(value):
    if NUM.fullmatch(value):
        number = Decimal(value.replace(',', '.'))
        return '0' if number == 0 else format(number.normalize(), 'f')
    return value


def encode(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def canonical(model):
    # Coordinates must uniquely identify joints before replacing ids with positions.
    if len(set(model['joints'].values())) != len(model['joints']):
        raise ValueError('Nós coincidentes: posição isolada não identifica o nó')
    joints = {key: tuple(0.0 if value == 0 else value for value in coords) for key, coords in model['joints'].items()}
    ends_by_id = {row['Frame']: (joints[row['JointI']], joints[row['JointJ']]) for row in model['tables']['CONNECTIVITY - FRAME']}
    frames = {key: {'endpointsOrderedCm': ends, 'tables': {}} for key, ends in ends_by_id.items()}
    tables = {}
    for table, rows in model['tables'].items():
        normalized = []
        for raw in rows:
            row = {}
            for key, value in raw.items():
                if key in {'Joint', 'JointI', 'JointJ'}:
                    row[key] = joints[value]
                elif key != 'Frame':
                    row[key] = value if key in IDENTIFIERS else normalize_value(value)
            if 'Frame' in raw:
                frames[raw['Frame']]['tables'].setdefault(table, []).append(row)
                # Diagnostic by table alone does not preserve cross-table correlation.
                row = {**row, 'frameEndpointsOrderedCm': ends_by_id[raw['Frame']]}
            normalized.append(encode(row))
        tables[table] = Counter(normalized)
    for frame in frames.values():
        frame['tables'] = {k: sorted(encode(row) for row in v) for k, v in frame['tables'].items()}
    return {'tables': tables, 'frameObjects': Counter(encode(v) for v in frames.values())}


def diff(a, b, limit=3):
    only_a, only_b = a - b, b - a
    return {'equal': a == b, 'CADCount': sum(a.values()), 'BIMCount': sum(b.values()),
            'onlyCADCount': sum(only_a.values()), 'onlyBIMCount': sum(only_b.values()),
            'onlyCADExamples': [{'record': json.loads(k), 'multiplicity': v} for k, v in list(sorted(only_a.items()))[:limit]],
            'onlyBIMExamples': [{'record': json.loads(k), 'multiplicity': v} for k, v in list(sorted(only_b.items()))[:limit]]}


def compare(a, b):
    aa, bb = canonical(a), canonical(b)
    tables = {k: diff(aa['tables'].get(k, Counter()), bb['tables'].get(k, Counter())) for k in sorted(aa['tables'].keys() | bb['tables'].keys())}
    return {'perTable': tables, 'wholeFrameObjects': diff(aa['frameObjects'], bb['frameObjects'], limit=1),
            'allTableRecordsEqualAfterRenumbering': all(v['equal'] for v in tables.values()),
            'frameAssociationsEqualAfterRenumbering': aa['frameObjects'] == bb['frameObjects']}


def main():
    if (OUT / 'R123-resultado-final.json').exists():
        raise FileExistsError('Não substituir análise existente')
    started = datetime.now(timezone.utc).isoformat()
    mono = perf_counter()
    models, hashes = {}, []
    for branch in ['CAD', 'BIM']:
        models[branch] = {}
        for file in sorted((SOURCE / ('SAP-' + branch)).glob('*.$2k')):
            kind = 'portico' if file.name.startswith('portico') else ('N1' if '-N1.' in file.name or '_N1.' in file.name else 'N2')
            models[branch][kind] = r122.parse(file.read_text(encoding='cp1252'))
            hashes.append({'path': str(file), 'sha256Before': r122.sha(file)})
    results = {kind: compare(models['CAD'][kind], models['BIM'][kind]) for kind in ['portico', 'N1', 'N2']}
    for row in hashes:
        row['sha256After'] = r122.sha(Path(row['path']))
        if row['sha256After'] != row['sha256Before']:
            raise ValueError('Fonte alterada')
    result = {'revision': 'H03/R123', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Comparação de registros dos seis arquivos analíticos exportados R122; sem leitura de resultados do solver ou edição nativa.',
              'models': results, 'protectedTextExports': hashes, 'sourceFilesUnchanged': True,
              'rules': ['Ids de nós substituídos por coordenadas, exigindo unicidade de posição.',
                        'Extremos I/J mantidos em ordem, sem inverter eixos, sinais ou distâncias de carga.',
                        'Números normalizados com Decimal, sem tolerância; apenas formato decimal e zero negativo unificados.',
                        'Repetições preservadas por multiconjuntos.',
                        'Registros associados à mesma barra agrupados em objeto completo antes da comparação, inclusive barras paralelas coincidentes.',
                        'Nomes de materiais, seções, ações e combinações preservados; não presumir equivalência de nomes diferentes.'],
              'scriptTime': {'startedAtUtc': started, 'completedAtUtc': datetime.now(timezone.utc).isoformat(), 'durationMs': (perf_counter() - mono) * 1000,
                             'scope': 'Somente execução Python; não é tempo de desenvolvimento CAD/BIM ou esforço isolado da IA.'},
              'nativeModelsEdited': False, 'SAP2000Executed': False, 'structuralSolverExecuted': False,
              'normativeValidationPerformed': False, 'relativeDisplacementDirectionCauseIdentified': False,
              'finalProductivityRankingAllowed': False,
              'limits': ['Igualdade é da representação textual exportada, limitada à precisão e ao escopo da exportação.',
                         'Não demonstra identidade interna dos modelos Eberick, resultado de cálculo independente ou segurança estrutural.',
                         'A exportação não substitui auditoria de opções omitidas pelo exportador ou validação de cargas/combinações frente às normas.',
                         'Divergência CAD Y-/BIM Y+ permanece sem causa demonstrada, mesmo se os registros exportados coincidirem.']}
    OUT.mkdir(exist_ok=True)
    (OUT / 'R123-resultado-final.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({kind: {'allTablesEqual': r['allTableRecordsEqualAfterRenumbering'], 'wholeFramesEqual': r['frameAssociationsEqualAfterRenumbering'],
                            'differentTables': [k for k, v in r['perTable'].items() if not v['equal']]} for kind, r in results.items()}))


if __name__ == '__main__':
    main()

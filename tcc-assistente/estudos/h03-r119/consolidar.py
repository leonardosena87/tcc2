"""Lê as 22 evidências UIA reais e preserva procedência e escopo parcial."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Lajes-H03-R119-CONSULTA-NAO-EXECUTAR')
FIELDS = {'QkNm2': 'Acidental', 'G2kNm2': 'Revestimento',
          'thicknessCm': 'Espessura', 'elevationCm': 'Elevação'}
KEYS = [('N1', f'L{i}') for i in range(1, 7)] + [('N2', f'L{i}') for i in range(1, 6)]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def field(text, label):
    found = set(re.findall(r'editar \(settable, string\) ' + re.escape(label) + r' Value: (.*?) ID:', text))
    if len(found) != 1:
        raise ValueError('Campo ausente ou contraditório: ' + label)
    return found.pop()


def parse(text, branch, floor, name):
    prefix = '34-H03-R119-CAD' if branch == 'CAD' else '35-H03-R119-BIM'
    if prefix not in text or 'diálogo Laje Secondary Actions' not in text:
        raise ValueError('Projeto ou diálogo incorreto')
    active = re.search(r'tabulação Croqui-(?:TCC-cdd31967-)?(N[12])\b', text)
    if not active or active[1] != floor or field(text, 'Nome') != name:
        raise ValueError('Pavimento ou laje incorreto')
    if 'kN/m²' not in text or 'text cm ID:' not in text:
        raise ValueError('Unidades não documentadas')
    return {key: float(field(text, label)) for key, label in FIELDS.items()}


def expected(floor, name):
    return {'QkNm2': 1.0 if floor == 'N2' else (2.5 if name in {'L5', 'L6'} else 1.5),
            'G2kNm2': 0.25 if floor == 'N2' else 1.0, 'thicknessCm': 14.0, 'elevationCm': 0.0}


def main():
    target = OUT / 'R119-resultado.json'
    if target.exists():
        raise FileExistsError('Não substituir resultado')
    prep = json.loads((OUT / 'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = [{**r, 'afterSha256': sha(Path(r['source']))} for r in prep['files']]
    if any(r['afterSha256'] != r['sha256Before'] for r in protected):
        raise ValueError('Fonte R116 alterada')
    branches, comparisons = {}, []
    for branch in ['CAD', 'BIM']:
        source_rows = [r for r in protected if r['branch'] == branch]
        original_prj = next(r for r in source_rows if r['copy'].endswith('.prj'))
        prj = Path(original_prj['copy'])
        if sha(prj) != original_prj['sha256Before']:
            raise ValueError('PRJ alterado na consulta')
        readings = []
        for floor, name in KEYS:
            txt = OUT / f'{branch}-{floor}-{name}-UI.txt'
            jpg = OUT / f'{branch}-{floor}-{name}.jpg'
            values = parse(txt.read_text(encoding='utf-8'), branch, floor, name)
            readings.append({'floor': floor, 'name': name, 'values': values,
                             'referenceR53': expected(floor, name),
                             'matchesReferenceR53': values == expected(floor, name),
                             'evidence': [{'path': p.name, 'sha256': sha(p)} for p in [txt, jpg]]})
        time = json.loads((OUT / f'{branch}-sessao-tempo.json').read_text(encoding='utf-8'))
        if time['elapsedMs'] <= 0 or datetime.fromisoformat(time['endedAtUtc']) <= datetime.fromisoformat(time['startedAtUtc']):
            raise ValueError('Intervalo inválido')
        branches[branch] = {'projectPath': str(prj), 'projectSha256': sha(prj),
                           'prjUnchangedDuringConsultation': True, 'readings': readings,
                           'sessionTime': time,
                           'auxiliaryDifferences': [{**r, 'afterCopySha256': sha(Path(r['copy']))}
                                                    for r in source_rows if not r['copy'].endswith('.prj')
                                                    and sha(Path(r['copy'])) != r['sha256Before']]}
    for cad, bim in zip(branches['CAD']['readings'], branches['BIM']['readings']):
        for key in FIELDS:
            comparisons.append({'floor': cad['floor'], 'name': cad['name'], 'field': key,
                                'CAD': cad['values'][key], 'BIM': bim['values'][key],
                                'equalDisplayed': cad['values'][key] == bim['values'][key]})
    result = {'revision': 'H03/R119', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
              'method': 'Consulta individual nativa após abrir cópias R116; extração UIA conferida em imagens; cancelamento e fechamento sem salvar.',
              'branches': branches, 'pairedComparisons': comparisons,
              'allComparedDisplayedFieldsEqual': all(r['equalDisplayed'] for r in comparisons),
              'allMatchPartialR53Register': all(r['matchesReferenceR53'] for b in branches.values() for r in b['readings']),
              'protectedR116Files': protected, 'sourceR116FilesUnchanged': True,
              'scope': 'Q, G2 parcial, espessura e elevação das onze lajes em cada ramo; 44 pares de campos, dos quais 22 de cargas.',
              'propertiesEdited': False, 'processingPerformed': False, 'monographEdited': False,
              'finalStructuralApproval': False, 'finalRankingAllowed': False,
              'limits': ['Valores iguais não encerram o modelo de cargas ou validam ELU/ELS.',
                         'G2 N1 é hipótese parcial de piso; G2 N2 contempla forro, não impermeabilização/telhado/paredes.',
                         'Não se inspecionaram listas completas de cargas extras, transferência da grelha ou forças em todas as peças.',
                         'L5 N1 não substitui cálculo da escada; L6 não encerra guarda-corpo e cargas de borda.',
                         'Não se conclui incorporação das paredes aos modelos por essa leitura.',
                         'Sessões incluem raciocínio, interface, evidências e latência; não são tempos integrais ou inferência isolada IA.']}
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'protectedFiles': len(protected), 'pairedFields': len(comparisons),
                      'allEqual': result['allComparedDisplayedFieldsEqual'], 'matchesR53': result['allMatchPartialR53Register']}))


if __name__ == '__main__':
    main()

"""Consolida transcricao visual, sem fingir extracao automatica da grade Delphi."""
import json
import hashlib
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Armadura-H03-R118-CONSULTA-NAO-EXECUTAR')


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def validate_table(table):
    rows = table['bars']
    if len(rows) != 24 or len({r['diameterMm'] for r in rows}) != 24:
        raise ValueError('Grade incompleta ou duplicada')
    active = {r['diameterMm']: r for r in rows if r['active']}
    if not active or any(r['steel'] != 'CA50' for r in active.values()):
        raise ValueError('Classe ativa diferente da observada')
    for groups in table['elementChoices'].values():
        for name, group in groups.items():
            if len(group['offeredMm']) != len(set(group['offeredMm'])):
                raise ValueError('Lista duplicada: ' + name)
            if not set(group['selectedMm']) <= set(group['offeredMm']) <= set(active):
                raise ValueError('Escolha fora da grade ativa')


def main():
    if (OUT / 'R118-resultado.json').exists(): raise FileExistsError('Nao substituir resultado')
    transcription = json.loads((HERE / 'transcricao-visual.json').read_text(encoding='utf-8'))
    prep = json.loads((OUT / 'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = [{**r, 'afterSha256': sha(Path(r['source']))} for r in prep['files']]
    if any(r['afterSha256'] != r['sha256Before'] for r in protected): raise ValueError('Fonte R116 alterada')
    branches = {}
    for branch, table in transcription['branches'].items():
        validate_table(table)
        rows = [r for r in prep['files'] if r['branch'] == branch]
        original_prj = next(r for r in rows if r['copy'].endswith('.prj'))
        prj = Path(original_prj['copy'])
        if sha(prj) != original_prj['sha256Before']: raise ValueError('PRJ mudou durante consulta')
        evidences = []
        for name in ['materiais-geral', 'barras-topo', 'barras-base', 'bitolas-vigas', 'bitolas-pilares', 'bitolas-lajes']:
            txt = OUT / f'{branch}-{name}-UI.txt'
            text = txt.read_text(encoding='utf-8')
            expected_folder = '32-H03-R118-CAD' if branch == 'CAD' else '33-H03-R118-BIM'
            if expected_folder not in text: raise ValueError('Projeto incorreto na evidencia')
            for p in [txt, OUT / f'{branch}-{name}.jpg']:
                if not p.is_file(): raise FileNotFoundError(p)
                evidences.append({'path': str(p), 'sha256': sha(p)})
        aux_changes = [{'path': r['copy'], 'beforeSha256': r['sha256Before'], 'afterSha256': sha(Path(r['copy']))}
                       for r in rows if not r['copy'].endswith('.prj') and sha(Path(r['copy'])) != r['sha256Before']]
        branches[branch] = {'projectPath': str(prj), 'projectSha256': sha(prj),
                            'prjUnchangedDuringConsultation': True, 'tableVisual': table,
                            'evidence': evidences, 'auxiliaryDifferencesFromSource': aux_changes,
                            'sessionTime': json.loads((OUT / f'{branch}-sessao-tempo.json').read_text(encoding='utf-8'))}
    cad, bim = [branches[b]['tableVisual'] for b in ['CAD', 'BIM']]
    comparisons = []
    for a, b in zip(cad['bars'], bim['bars']):
        assert a['diameterMm'] == b['diameterMm']
        for field in ['active', 'steel']:
            comparisons.append({'kind': 'globalBar', 'diameterMm': a['diameterMm'], 'field': field,
                                'CAD': a[field], 'BIM': b[field], 'equalVisual': a[field] == b[field]})
    for element, groups in cad['elementChoices'].items():
        for direction, group in groups.items():
            other = bim['elementChoices'][element][direction]
            if group['offeredMm'] != other['offeredMm']: raise ValueError('Listas oferecidas diferentes')
            for diameter in group['offeredMm']:
                a, b = diameter in group['selectedMm'], diameter in other['selectedMm']
                comparisons.append({'kind': 'elementChoice', 'element': element, 'direction': direction,
                                    'diameterMm': diameter, 'CAD': a, 'BIM': b, 'equalVisual': a == b})
    old = HERE.parent / 'h03-r100'
    errata_sources = [{'path': str(old / name), 'sha256': sha(old / name)}
                     for name in ['LEIA-ME-R100.md', 'CAD-armadura-inferior.png', 'BIM-armadura-inferior.png']]
    result = {'revision': 'H03/R118', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
              'method': 'Consulta nativa, transcricao visual pelo assistente das imagens e controle automatico de consistencia. Grade nao extraida por UIA/OCR.',
              'branches': branches, 'pairedVisualComparisons': comparisons,
              'visualSelectionsEqual': all(r['equalVisual'] for r in comparisons),
              'protectedSourceR116Files': protected, 'sourceR116FilesUnchanged': True,
              'erratumR100': {'text': 'R100 citou 25/32/40 mm como ativos. Imagens originais CAD/BIM mostram caixas desmarcadas. R118 registra errata sem afirmar alteracao nativa entre revisoes.',
                              'sources': errata_sources},
              'propertiesEdited': False, 'processingPerformed': False, 'monographEdited': False,
              'finalStructuralApproval': False, 'finalRankingAllowed': False,
              'limits': ['Consulta global; excecoes por pavimento/elemento nao integralmente verificadas.',
                         'A grade define opcoes; nao comprova armadura efetivamente dimensionada.',
                         'Nao extraiu fyk, Es, gama-s, ductilidade, ancoragens, espacamentos ou estribos de cada peca.',
                         'Custos e emissoes presentes na grade nao foram validados ou usados nos resultados.',
                         'Igualdade transcrita visual nao e teste automatizado da imagem ou validacao normativa.',
                         'Tempos incluem navegacao e evidencias, sem inferencia IA isolada ou ranking.']}
    (OUT / 'R118-resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'sourceFilesUnchanged': len(protected), 'visualComparisons': len(comparisons),
                      'equal': sum(r['equalVisual'] for r in comparisons)}))


if __name__ == '__main__': main()

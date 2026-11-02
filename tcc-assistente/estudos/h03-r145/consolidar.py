"""Confere leituras nativas do cadastro de forro; não dimensiona estruturas."""
import hashlib
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Forro-N1-H03-R145-NAO-EXECUTAR')
FIELDS = {'G2kNm2': 'Revestimento', 'QkNm2': 'Acidental',
          'thicknessCm': 'Espessura', 'elevationCm': 'Elevação', 'extra': 'Extra'}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def field(text, label):
    values = set(re.findall(r'editar \((?:disabled, )?settable, string\) '
                           + re.escape(label) + r' Value: (.*?) ID:', text))
    if len(values) != 1:
        raise ValueError('Campo ausente ou contraditório: ' + label)
    return values.pop()


def parse(text, branch, name):
    prefix = {'CAD': '70-H03-R145-CAD', 'BIM': '71-H03-R145-BIM'}[branch]
    if prefix not in text or 'diálogo Laje Secondary Actions' not in text:
        raise ValueError('Projeto ou diálogo incorreto')
    active = re.search(r'tabulação Croqui-(?:TCC-cdd31967-)?(N[12])\b', text)
    if not active or active[1] != 'N1' or field(text, 'Nome') != name:
        raise ValueError('Pavimento ou laje incorreto')
    if 'kN/m²' not in text or 'text cm ID:' not in text:
        raise ValueError('Unidades não documentadas')
    return {k: float(field(text, label)) for k, label in FIELDS.items()}


def expected(name, after):
    interior = name in {'L1', 'L2', 'L3', 'L4'}
    return dict(G2kNm2=1.25 if after and interior else 1.0,
                QkNm2=1.5 if interior else 2.5, thicknessCm=14., elevationCm=0., extra=0.)


def main():
    result_path = OUT / 'R145-resultado.json'
    if result_path.exists():
        raise FileExistsError(result_path)
    prep = json.loads((OUT / 'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = [{**r, 'sha256After': sha(Path(r['source']))} for r in prep['files']]
    assert all(r['sha256After'] == r['sha256Before'] for r in protected)
    branches = {}
    for branch in ('CAD', 'BIM'):
        readings = []
        for i in range(1, 7):
            name = f'L{i}'
            if i <= 4:
                before = OUT / f'{branch}-N1-{name}-antes-UI.txt'
                assert parse(before.read_text(encoding='utf-8'), branch, name) == expected(name, False)
            else:
                before = None
            stage = 'reaberta' if i <= 4 else 'controle'
            after = OUT / f'{branch}-N1-{name}-{stage}-UI.txt'
            values = parse(after.read_text(encoding='utf-8'), branch, name)
            assert values == expected(name, True), (branch, name, values)
            readings.append(dict(name=name, values=values, before=before.name if before else None,
                                 after=after.name, afterSha256=sha(after)))
        prj = Path(next(r['copy'] for r in protected if r['branch'] == branch and r['copy'].endswith('.prj')))
        saved = json.loads((OUT / f'{branch}-prj-salvo.json').read_text(encoding='utf-8'))
        assert saved['sha256'] == sha(prj)
        with zipfile.ZipFile(prj) as z:
            assert z.testzip() is None
        time = json.loads((OUT / f'{branch}-tempo-sessao.json').read_text(encoding='utf-8'))
        assert time['prjUnchangedDuringReadback'] and time['durationMs'] > 0
        assert datetime.fromisoformat(time['end']['utc']) > datetime.fromisoformat(time['start']['utc'])
        frozen = OUT / 'congelados-apos-cadastro' / branch
        if frozen.exists():
            raise FileExistsError(frozen)
        shutil.copytree(prj.parent.parent, frozen)
        tree = []
        for p in sorted(prj.parent.parent.rglob('*')):
            if p.is_file():
                rel = p.relative_to(prj.parent.parent)
                assert sha(p) == sha(frozen / rel)
                tree.append(dict(path=rel.as_posix(), sha256=sha(p)))
        branches[branch] = dict(projectPath=str(prj), projectSha256=sha(prj), readings=readings,
                               prjZipIntegrity=True, readbackHashUnchanged=True,
                               sessionTime=time, frozenPath=str(frozen), frozenFiles=tree)
    assert all(
        a['values'] == b['values'] for a, b in zip(branches['CAD']['readings'], branches['BIM']['readings']))
    references = [HERE.parent / 'h03-r53/R53-matriz-planejada.json',
                  HERE.parent / 'h03-r119/R119-resultado.json', Path('D:/TCC/PROJETO ARQUITETONICO-A0.pdf')]
    result = dict(revision='H03/R145', createdAtUtc=datetime.now(timezone.utc).isoformat(),
                  protectedR116Files=protected, sourcesUnchanged=True, branches=branches,
                  nativeFieldChanges=8, nativePostSaveSlabReadings=12, pairedDisplayedFields=30,
                  comparedFieldsEqual=True, newG2Hypothesis={'ceiling_kNm2': .25, 'floor_kNm2': 1.,
                                                          'total_kNm2': 1.25, 'slabs': ['N1-L1','N1-L2','N1-L3','N1-L4']},
                  references=[dict(path=str(p), sha256=sha(p)) for p in references],
                  processingPerformed=False, nativeExportPerformed=False,
                  authoringRvtDwgEdited=False, monographEdited=False, finalStructuralApproval=False,
                  finalFlowRankingAllowed=False,
                  limits=['Forro de 0,25 kN/m² é hipótese do estudo, não especificação de produto.',
                          'N2 não foi relido nesta sessão; L5/L6 N1 são controles sem alteração.',
                          'Resultados processados preexistentes pertencem à R116; não representam recálculo R145.',
                          'BIM foi operado depois de CAD e beneficiou-se de aprendizagem e agrupamento de ações.',
                          'BIM L3/L4 editada contém valores transitórios no texto AX; leitura após reabertura é a evidência do cadastro.',
                          'Igualdade de campos não demonstra igualdade integral dos modelos nem segurança estrutural.'])
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(dict(protected=len(protected), changes=8, readings=12, pairedFields=30, equal=True)))


if __name__ == '__main__':
    main()

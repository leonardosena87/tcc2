"""Conserva resultados parciais e diferenças CAD/BIM após incluir forro N1."""
import importlib.util
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Analise-H03-R146-FORRO-N1-NAO-EXECUTAR')
spec = importlib.util.spec_from_file_location('r116', HERE.parent / 'h03-r116/consolidar.py')
r116 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r116)
sha, extract, check_time = r116.sha, r116.extract, r116.check_time


def read_summary(branch):
    text = (OUT / f'{branch}-resumo-analise-UI.txt').read_text(encoding='utf-8')
    prefix = {'CAD': '72-H03-R146-CAD', 'BIM': '73-H03-R146-BIM'}[branch]
    if prefix not in text:
        raise ValueError('Projeto incorreto')
    return extract(text)


def main():
    target = OUT / 'R146-resultado.json'
    if target.exists():
        raise FileExistsError(target)
    prep = json.loads((OUT / 'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = [{**r, 'sha256After': sha(Path(r['source']))} for r in prep['files']]
    assert all(r['sha256Before'] == r['sha256After'] for r in protected)
    basepath = HERE.parent / 'h03-r116/R116-resultado.json'
    baseline = json.loads(basepath.read_text(encoding='utf-8'))
    branches = {}
    for branch in ('CAD', 'BIM'):
        summary = read_summary(branch)
        status = (OUT / f'{branch}-processamento-estado-UI.txt').read_text(encoding='utf-8')
        assert 'Estrutura processada com avisos' in status
        session = json.loads((OUT / f'{branch}-sessao-tempo.json').read_text(encoding='utf-8'))
        command = json.loads((OUT / f'{branch}-processamento-tempo.json').read_text(encoding='utf-8'))
        check_time(session, command)
        prj = Path(next(r['copy'] for r in protected if r['branch'] == branch and r['copy'].endswith('.prj')))
        with zipfile.ZipFile(prj) as z:
            assert z.testzip() is None
        frozen = OUT / 'congelados-apos-processamento' / branch
        if frozen.exists():
            raise FileExistsError(frozen)
        src = prj.parent.parent
        shutil.copytree(src, frozen)
        hashes = []
        for p in sorted(src.rglob('*')):
            if p.is_file():
                rel = p.relative_to(src)
                assert sha(p) == sha(frozen / rel)
                hashes.append(dict(path=rel.as_posix(), sha256=sha(p)))
        previous = baseline['branches'][branch]['summary']
        branches[branch] = dict(projectPath=str(prj), projectSha256=sha(prj), summary=summary,
                               frozenPath=str(frozen), frozenFiles=hashes, sessionTime=session,
                               processingTimeObservation=command,
                               deltaDisplayedVerticalLoadsTfFromOwnR116={
                                   k: round(v - previous['verticalLoadsDisplayedTf'][k], 6)
                                   for k, v in summary['verticalLoadsDisplayedTf'].items()})
    cad, bim = [branches[b]['summary'] for b in ('CAD','BIM')]
    diffs = []
    for case, a in cad['topDisplacementsRawUnitNotExplicit'].items():
        b = bim['topDisplacementsRawUnitNotExplicit'][case]
        for field in a:
            if a[field] != b[field]:
                diffs.append(dict(case=case, field=field, CAD=a[field], BIM=b[field],
                                  deltaBIMminusCAD=round(b[field]-a[field], 6)))
    comparison = {**r116.r111.r106.comparison(cad, bim),
                  'verticalDisplayedValuesEqual': cad['verticalLoadsDisplayedTf'] == bim['verticalLoadsDisplayedTf'],
                  'gammaZDisplayedValuesAndLimitsEqual': cad['gammaZDisplayed'] == bim['gammaZDisplayed'],
                  'topDisplayedDifferences': diffs}
    result = dict(revision='H03/R146', createdAtUtc=datetime.now(timezone.utc).isoformat(),
                  branches=branches, comparison=comparison, protectedR145Files=protected,
                  sourceR145FilesUnchanged=True, baselineR116Sha256=sha(basepath),
                  processingPerformed=True, dimensioningPerformed=False, slabDeflectionPerformed=False,
                  crackedStiffnessCalculationPerformed=False, finalStructuralApproval=False,
                  finalRankingAllowed=False,
                  limits=['Cargas ainda parciais; paredes, escada, tanque e vento/combinacoes nao encerrados.',
                          'Limites sao exibidos; nao se confirmou adequacao normativa final de parametros/acoes.',
                          'Igualdade arredondada nao demonstra equivalencia interna, equilibrio ou seguranca.',
                          'Direcao critica relativa diverge; causa desconhecida, sem defeito de transferencia demonstrado.',
                          'CAD comando-ate-registro inclui intervalo de uma rodada do assistente apos a primeira imagem de termino; BIM foi registrado na propria chamada. Sem ranking de solver.',
                          'Sessao e comando se sobrepoem; nao somar. Nao mediu inferencia isolada, tokens ou custo da IA.'])
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(dict(comparison=comparison, deltasTf={b:r['deltaDisplayedVerticalLoadsTfFromOwnR116'] for b,r in branches.items()})))


if __name__ == '__main__':
    main()

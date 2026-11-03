"""Registra teste pareado real, inclusive a persistencia do erro de apoio."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys
import zipfile

HERE = Path(__file__).resolve().parent
OUT = Path('D:/TCC/outputs/Escada-H03-R188-ANCORAGEM-LE3-NAO-EXECUTAR')
sys.path.insert(0, str(HERE.parent / 'h03-r182'))
from consolidar_diagnostico import text_docx, parse_report


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))


def write(p, data):
    Path(p).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    branches = {}
    for branch, prep_name in [('CAD', 'R188-preparacao.json'), ('BIM', 'R188-BIM-preparacao.json')]:
        prep = read(OUT / prep_name)
        if sha(prep['sourceProjectPath']) != prep['sourceProjectSha256']:
            raise ValueError('Fonte R184 alterada: ' + branch)
        prj = Path(prep['projectPath'])
        with zipfile.ZipFile(prj) as z:
            if z.testzip():
                raise ValueError('PRJ experimental corrompido')
        if sha(prj) == prep['initialProjectSha256']:
            raise ValueError('PRJ experimental nao foi gravado: ' + branch)
        selected = (OUT / f'{branch}-gancho-selecionado-AX.txt').read_text(encoding='utf-8')
        if 'Ancoragem da armadura Value: gancho' not in selected:
            raise ValueError('Gancho nao confirmado: ' + branch)
        error_ax = (OUT / f'{branch}-LE3-A11-AX.txt').read_text(encoding='utf-8')
        if error_ax.count('Erro A11 - Largura do apoio insuficiente.') != 5:
            raise ValueError('Diagnostico por bitola incompleto: ' + branch)
        report = OUT / f'{branch}-mensagens.docx'
        parsed = parse_report(text_docx(report))
        timing = read(OUT / f'{branch}-tempo-observado.json')
        interval = (datetime.fromisoformat(timing['firstConfirmedUtc']) - datetime.fromisoformat(timing['startUtc'])).total_seconds()
        if abs(interval - timing['elapsedSeconds']) > 0.0001:
            raise ValueError('Intervalo observado inconsistente')
        if 'Estrutura processada com avisos' not in (OUT / f'{branch}-fim-AX.txt').read_text(encoding='utf-8'):
            raise ValueError('Termino do calculo nao confirmado')
        branches[branch] = dict(sourceProjectPath=prep['sourceProjectPath'],
            sourceProjectSha256=prep['sourceProjectSha256'], sourceUnchanged=True,
            experimentalProjectPath=str(prj), experimentalProjectSha256=sha(prj),
            reportPath=str(report), reportSha256=sha(report), nativeReport=parsed,
            anchorage='gancho', lap100PercentAvoidanceUncheckedInCapturedDialog=True,
            hookAppliedAndRecalculated=True, hookRetainedInReopenedDialogScreenshot=True,
            stairsPositiveTable=dict(LE1='calculado', LE2='calculado', LE3='D31'),
            LE3DiameterErrors={str(d): 'A11' for d in (6.3, 8.0, 10.0, 12.5, 16.0)},
            observedInterval=timing, completeFlowMeasured=False,
            geometryAndLoadRetentionAuditedByFreshExport=False)
    refs = read(HERE.parent / 'h03-r183/R183-inicio.json')['sourceProjects']
    for ref in refs.values():
        if sha(ref['path']) != ref['sha256']:
            raise ValueError('Fonte R182 alterada')
    result = dict(revision='H03/R188', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        branches=branches, R182ReferenceProjectHashesPreserved=True,
        experimentOrder=['CAD', 'BIM'], pairedHookExperimentCompleted=True,
        LE3StillD31A11Both=True, specificFailingSupportEdgeNotYetIdentified=True,
        interpretation='Selecionar gancho nao foi suficiente para eliminar A11 na condicao testada em nenhum receptor. Nao se conclui que gancho seja inviavel em toda configuracao.',
        thresholdsNotRaisedToSuppressError=True, structuralApproval=False,
        fullPairedFlowComparisonFinished=False, wholeFlowProductivityRankingPermitted=False)
    write(OUT / 'R188-ensaio-gancho-pareado.json', result)
    pointer = Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    if not (OUT / 'R188-ponteiro-anterior.json').exists():
        shutil.copy2(pointer, OUT / 'R188-ponteiro-anterior.json')
    current = read(pointer)
    current.update(latestHookExperimentRevision='H03/R188',
        latestHookExperimentPath=str(OUT / 'R188-ensaio-gancho-pareado.json'),
        latestHookExperimentSha256=sha(OUT / 'R188-ensaio-gancho-pareado.json'),
        hookAnchorageTestCompleted=True, hookAloneResolvesLE3=False,
        allStructuralElementsSuccessfullyDesigned=False)
    write(pointer, current)
    write(OUT / 'R188-ponteiro-atualizado.json', current)
    selected = ['R188-preparacao.json', 'R188-BIM-preparacao.json',
        'R188-ensaio-gancho-pareado.json', 'R188-ponteiro-atualizado.json']
    for branch in branches:
        selected += [f'{branch}-{suffix}' for suffix in ('mensagens.docx', 'mensagens.txt',
            'gancho-selecionado-AX.txt', 'LE3-A11-AX.txt', 'fim-AX.txt', 'tempo-observado.json')]
        selected += [p.name for p in OUT.glob(f'{branch}-*-0.png') if '-LE3-erro-' not in p.name]
    for name in selected:
        shutil.copy2(OUT / name, HERE / name)
    shutil.copy2(HERE / 'LEIA-ME-R188.md', OUT / 'LEIA-ME-R188.md')
    files = [p for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'R188-manifesto.json']
    manifest = dict(revision='H03/R188', files=[dict(relativePath=p.name,
        bytes=p.stat().st_size, sha256=sha(p)) for p in files])
    write(HERE / 'R188-manifesto.json', manifest)
    shutil.copy2(HERE / 'R188-manifesto.json', OUT / 'R188-manifesto.json')
    print(json.dumps(dict(evidenceFiles=len(files), LE3='D31/A11 em ambos',
        nativeSeconds={b:r['nativeReport']['nativeTotalSeconds'] for b,r in branches.items()},
        sourceProjectHashesPreserved=True)))


if __name__ == '__main__':
    main()

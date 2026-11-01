"""Sensibilidade de malha L4: forças e primeiros momentos, sem aprovação estrutural."""
import importlib.util
import json
import math
import shutil
import zipfile
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Grelha-W15-H03-R133-SENSIBILIDADE-NAO-EXECUTAR')
OLD = HERE.parent/'h03-r132'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

audit = load('r132_audit', OLD/'auditar.py')
sha = audit.sha

def models(folder):
    paths = sorted(folder.glob('*.$2k'))
    if len(paths) != 3:
        raise ValueError('Exportação incompleta')
    result = {}
    for p in paths:
        kind = 'N1' if p.stem.endswith('N1') else 'N2' if p.stem.endswith('N2') else 'portico'
        if kind in result:
            raise ValueError('Modelo duplicado')
        result[kind] = {'data': audit.r122.parse(p.read_text(encoding='cp1252')),
                        'path': str(p), 'sha256': sha(p)}
    return result

def compare(a, b):
    changed = {}
    for name in sorted(set(a['tables']) | set(b['tables'])):
        before = Counter(audit.encode(r) for r in a['tables'].get(name, []))
        after = Counter(audit.encode(r) for r in b['tables'].get(name, []))
        if before != after:
            changed[name] = {'removedCount': sum((before-after).values()),
                             'addedCount': sum((after-before).values())}
    return {'geometry': audit.r122.geometry_comparison(a, b), 'changedTables': changed}

def time_check(session, process):
    values = [session['wallMs'], process['elapsedSeconds']]
    if any(not math.isfinite(v) or v <= 0 for v in values):
        raise ValueError('Duração inválida')
    dates = [datetime.fromisoformat(v.replace('Z', '+00:00')) for v in
             [session['startUtc'], process['utc'], process['endUtc'], session['endUtc']]]
    if not dates[0] <= dates[1] < dates[2] <= dates[3]:
        raise ValueError('Processamento fora da sessão')

def main():
    target = OUT/'R133-resultado.json'
    if target.exists():
        raise FileExistsError(target)
    prep = json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = []
    for row in prep['files']:
        digest = sha(Path(row['source']))
        if digest != row['sha256Before']:
            raise ValueError('Fonte R131 alterada')
        protected.append({'path': row['source'], 'sha256': digest})
    old_result = json.loads((OLD/'R132-resultado.json').read_text(encoding='utf-8'))
    previous_summary = json.loads((HERE.parent/'h03-r131/R131-resultado.json').read_text(encoding='utf-8'))
    branches = {}
    for branch, prefix in [('CAD', '52'), ('BIM', '53')]:
        before, after = models(OLD/f'SAP-{branch}-W15'), models(OUT/f'SAP-{branch}')
        parsed = after['N1']['data']
        rows = audit.nodal(parsed)
        force = audit.resultant(rows)
        if len(rows) != 10 or D(force['signedFzKgf']) != D('-446.0250'):
            raise ValueError('Carga nodal não corresponde ao ensaio W15 esperado')
        # Sem mudar a malha, o controle R132 sem W15 não possuía forças nodais G2.
        # Não existe controle de 10 cm sem W15; essa limitação é conservada no relatório.
        if audit.nodal(models(OLD/f'SAP-{branch}-BASE')['N1']['data']):
            raise ValueError('Há forças nodais G2 no controle sem W15')
        observations = json.loads((HERE/'observacoes-visuais.json').read_text(encoding='utf-8'))
        summary = observations['branches'][branch]
        expected_name = f'{prefix}-H03-R133-{branch}-W15-GRELHA-NAO-EXECUTAR'
        if summary['projectName'] != expected_name:
            raise ValueError('Identificação visual divergente')
        visual_evidence = []
        for label in ['resumo-analise', 'processamento-concluido', 'Grelha-50cm-antes',
                      'Grelha-10cm-editada', 'Grelha-10cm-reaberta', 'L4-reaberta', 'escopo-analise']:
            p = OUT/f'{branch}-{label}.jpg'
            if not p.is_file() or p.stat().st_size < 1000:
                raise ValueError('Imagem de evidência ausente')
            visual_evidence.append({'file': p.name, 'sha256': sha(p)})
        session = json.loads((OUT/f'{branch}-sessao-tempo.json').read_text(encoding='utf-8'))
        process = json.loads((OUT/f'{branch}-processamento-tempo.json').read_text(encoding='utf-8'))
        time_check(session, process)
        prjrow = next(r for r in prep['files'] if r['branch'] == branch and r['copy'].endswith('.prj'))
        prj = Path(prjrow['copy'])
        with zipfile.ZipFile(prj) as archive:
            if archive.testzip() is not None:
                raise ValueError('PRJ corrompido')
        if sha(prj) == prjrow['sha256Before']:
            raise ValueError('Cópia experimental não mudou')
        frozen = OUT/'congelados-apos-processamento'/branch
        if frozen.exists():
            raise FileExistsError(frozen)
        shutil.copytree(prj.parent.parent, frozen)
        files = [{'path': p.relative_to(prj.parent.parent).as_posix(), 'sha256': sha(p)}
                 for p in sorted(prj.parent.parent.rglob('*')) if p.is_file()]
        if not all(sha(frozen/r['path']) == r['sha256'] for r in files):
            raise ValueError('Congelamento divergente')
        prior = old_result['branches'][branch]['resultant']
        ratio = D(force['centroidDistanceCm'])/D(prior['centroidDistanceCm'])
        comparisons = {kind: compare(before[kind]['data'], after[kind]['data']) for kind in before}
        if comparisons['N2']['changedTables']:
            raise ValueError('N2 mudou no ensaio exclusivo de L4/N1')
        branches[branch] = {'projectPath': str(prj), 'projectSha256': sha(prj), 'frozenFiles': files,
            'exports': {k: {t: v[t] for t in ['path', 'sha256']} for k, v in after.items()},
            'nodalG2N1': rows, 'resultant': force, 'coarseResultantR132': prior,
            'centroidDistanceReductionPercent': str((1-ratio)*100),
            'N1JointCountBefore': len(before['N1']['data']['joints']), 'N1JointCountAfter': len(parsed['joints']),
            'modelComparisonsToOwn50cm': comparisons, 'summary': summary, 'visualEvidence': visual_evidence,
            'summaryMethod': 'Transcrição visual pela IA das capturas JPG; não extração textual nativa nem OCR automático.',
            'verticalDisplayedUnchangedFromOwnR131': summary['verticalLoadsDisplayedTf'] == previous_summary['branches'][branch]['summary']['verticalLoadsDisplayedTf'],
            'sessionTime': session, 'processingTimeObservation': process}
    paired = branches['CAD']['nodalG2N1'] == branches['BIM']['nodalG2N1']
    if not paired:
        raise ValueError('Distribuição nodal CAD/BIM divergente')
    result = {'revision': 'H03/R133', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Sensibilidade isolada L4/N1 de 50x50 para 10x10 cm, ângulo 90 graus; cópias dos dois ramos R131.',
        'protectedR131Files': protected, 'sourceFilesUnchanged': True,
        'configurationVisuallyVerifiedAfterReopeningBothCopies': True,
        'initialSummaryUIAccessibilityTextCaptureAvailable': False,
        'initialEmptyTextFilesPreservedAsCaptureFailureNotEvidenceOfMissingProjectData': True,
        'pairedNodalLoadsEqualIncludingIds': paired, 'branches': branches,
        'gridChangesAreAfterImportReceiverComplements': True, 'CADorBIMTransferDefectProven': False,
        'finerGridWithoutWallControlPerformed': False, 'forceIntegralRetainedUnderObservedConvention': True,
        'exactFirstMomentsRetainedInN1Export': False, 'meshConvergenceOrToleranceAcceptanceDemonstrated': False,
        'internalModelIdenticalToExportProven': False, 'W15AcceptedAsFinalLocalModel': False,
        'processingPerformed': True, 'dimensioningPerformed': False, 'slabDeflectionPerformed': False,
        'SAP2000Executed': False, 'monographEdited': False, 'finalStructuralApproval': False,
        'finalProductivityRankingAllowed': False,
        'nextStep': 'Verificar sensibilidade adicional/alinhamento e efeitos locais antes de aceitar W15; completar demais cargas e só então ELU/ELS completo.'}
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'pairedNodal': paired, 'protectedFiles': len(protected),
                      'centroid': branches['CAD']['resultant'],
                      'nodeCounts': [branches['CAD']['N1JointCountBefore'], branches['CAD']['N1JointCountAfter']],
                      'reductionPercent': branches['CAD']['centroidDistanceReductionPercent'],
                      'summaryEqual': {b: r['verticalDisplayedUnchangedFromOwnR131'] for b, r in branches.items()}}, ensure_ascii=False))

if __name__ == '__main__':
    main()

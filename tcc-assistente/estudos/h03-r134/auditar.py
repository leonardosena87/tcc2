"""Controle de mesma malha, com diferenças de tabelas e interpretação condicional do pórtico."""
import importlib.util
import json
import shutil
import zipfile
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Controle-Grelha-H03-R134-SEM-W15-NAO-EXECUTAR')
spec = importlib.util.spec_from_file_location('r133', HERE.parent/'h03-r133/consolidar.py')
r133 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r133)
sha = r133.sha
AXIS_TABLE = 'FRAME LOCAL AXES ASSIGNMENTS 1 - TYPICAL'

def number(value):
    result = D(str(value).replace(',', '.'))
    if not result.is_finite():
        raise ValueError('Número não finito')
    return result

def differences(before, after):
    result = {}
    for name in sorted(set(before['tables']) | set(after['tables'])):
        a = Counter(r133.audit.encode(r) for r in before['tables'].get(name, []))
        b = Counter(r133.audit.encode(r) for r in after['tables'].get(name, []))
        if a != b:
            result[name] = {'added': [json.loads(r) for r in (b-a).elements()],
                            'removed': [json.loads(r) for r in (a-b).elements()]}
    return result

def horizontal_point(model, row):
    """Somente hipótese de eixo SAP padrão, sem rotação atribuída; não converter silenciosamente."""
    if (row['CoordSys'], row['Type'], row['Dir'], row['DistType']) != ('LOCAL', 'Force', '2', 'RelDist'):
        raise ValueError('Carga pontual fora da hipótese de eixo padrão')
    key = row['Frame']
    rotations = [r for r in model['tables'].get(AXIS_TABLE, []) if r['Frame'] == key]
    if rotations and (len(rotations) != 1 or number(rotations[0]['Angle']) != 0):
        raise ValueError('Rotação explícita não suportada')
    if any('LOCAL AXES' in name and name != AXIS_TABLE for name in model['tables']):
        raise ValueError('Tabela adicional de eixos exige análise própria')
    a, b = [tuple(number(v) for v in xyz) for xyz in model['frames'][key]]
    if a[2] != b[2] or a == b:
        raise ValueError('Barra não horizontal ou nula')
    t = number(row['RelDist'])
    if not 0 <= t <= 1:
        raise ValueError('Estação relativa inválida')
    xyz = tuple(x+(y-x)*t for x, y in zip(a, b))
    return xyz, number(row['Force']), not rotations

def portico_increment(before, after, diff):
    """r × F + M dos incrementos G2; eixos ausentes interpretados como padrão SAP, condicionalmente."""
    totals = {'Fz': D(0), 'Mx': D(0), 'My': D(0)}
    component_forces = {'jointGlobal': D(0), 'pointLocal2UnderDefaultAssumption': D(0)}
    frames_without_rotation = set()
    for name, changes in diff.items():
        if name not in {'JOINT LOADS - FORCE', 'FRAME LOADS - POINT'}:
            raise ValueError('Diferença não suportada no pórtico')
        for kind, sign, model in [('removed', -1, before), ('added', 1, after)]:
            for row in changes[kind]:
                if row['LoadPat'] != 'G2':
                    raise ValueError('Outro padrão de carga mudou')
                if name == 'JOINT LOADS - FORCE':
                    if row['CoordSys'] != 'GLOBAL' or any(number(row[k]) for k in ['F1', 'F2', 'M3']):
                        raise ValueError('Componente global adicional exige transformação completa')
                    x, y, _ = [number(v) for v in model['joints'][row['Joint']]]
                    force, mx, my = [number(row[k]) for k in ['F3', 'M1', 'M2']]
                    component_forces['jointGlobal'] += sign*force
                else:
                    (x, y, _), force, implicit = horizontal_point(model, row)
                    mx = my = D(0)
                    component_forces['pointLocal2UnderDefaultAssumption'] += sign*force
                    if implicit:
                        frames_without_rotation.add(row['Frame'])
                totals['Fz'] += sign*force
                totals['Mx'] += sign*(y*force+mx)
                totals['My'] += sign*(-x*force+my)
    return {'interpretationConditionalOnSAPDefaultForUnassignedAxes': True,
            'SAPImportExecutionPerformed': False, 'EberickInternalAxesProvenEquivalent': False,
            'frameIdsWithoutExplicitRotation': sorted(frames_without_rotation, key=int),
            'signedComponentForcesKgf': {k: str(v) for k, v in component_forces.items()},
            'signedTotals': {k: str(v) for k, v in totals.items()},
            'units': {'Fz': 'kgf', 'Mx': 'kgf.cm', 'My': 'kgf.cm'}}

def main():
    if (OUT/'R134-resultado.json').exists():
        raise FileExistsError('Resultado existente')
    prep = json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = []
    for row in prep['files']:
        digest = sha(Path(row['source']))
        if digest != row['sha256Before']:
            raise ValueError('Fonte R116 alterada')
        protected.append({'path': row['source'], 'sha256': digest})
    old = json.loads((HERE.parent/'h03-r133/R133-resultado.json').read_text(encoding='utf-8'))
    old_protected = []
    for branch, data in old['branches'].items():
        base = Path(data['projectPath']).parent.parent
        for row in data['frozenFiles']:
            p = base/row['path']
            if sha(p) != row['sha256']:
                raise ValueError('Cópia R133 alterada')
            old_protected.append({'path': str(p), 'sha256': row['sha256']})
    observations = json.loads((HERE/'observacoes-visuais.json').read_text(encoding='utf-8'))
    branches = {}
    for branch in ['CAD', 'BIM']:
        control = r133.models(OUT/f'SAP-{branch}')
        wall = r133.models(HERE.parent/'h03-r133'/f'SAP-{branch}')
        comparison = {}
        for kind in control:
            a, b = control[kind]['data'], wall[kind]['data']
            comparison[kind] = {'controlJointCount': len(a['joints']), 'wallJointCount': len(b['joints']),
                'controlFrameCount': len(a['frames']), 'wallFrameCount': len(b['frames']),
                'sameJointIdsAndCoordinates': a['joints'] == b['joints'],
                'sameFrameIdsAndOrderedEndpoints': a['frames'] == b['frames'],
                'changedTables': differences(a, b)}
            if not comparison[kind]['sameJointIdsAndCoordinates'] or not comparison[kind]['sameFrameIdsAndOrderedEndpoints']:
                raise ValueError('Geometria ordenada mudou no controle de mesma malha')
        if comparison['N2']['changedTables']:
            raise ValueError('N2 mudou')
        diff = comparison['N1']['changedTables']
        if set(diff) != {'JOINT LOADS - FORCE'} or diff['JOINT LOADS - FORCE']['removed'] or len(diff['JOINT LOADS - FORCE']['added']) != 10:
            raise ValueError('N1 não isola dez forças adicionadas')
        if r133.audit.nodal(control['N1']['data']):
            raise ValueError('Controle possui força nodal G2')
        nodal = r133.audit.nodal(wall['N1']['data'])
        resultant = r133.audit.resultant(nodal)
        if resultant != old['branches'][branch]['resultant']:
            raise ValueError('Resultado nodal não reproduz R133')
        portico = portico_increment(control['portico']['data'], wall['portico']['data'], comparison['portico']['changedTables'])
        nodal_m = resultant['originMomentFromNodalForcesKgfCm']
        portico['differenceFromN1AppliedForces'] = {
            'FzKgf': str(D(portico['signedTotals']['Fz'])-D(resultant['signedFzKgf'])),
            'MxKgfCm': str(D(portico['signedTotals']['Mx'])-D(nodal_m['Mx'])),
            'MyKgfCm': str(D(portico['signedTotals']['My'])-D(nodal_m['My']))}
        row = next(r for r in prep['files'] if r['branch'] == branch and r['copy'].endswith('.prj'))
        prj = Path(row['copy'])
        with zipfile.ZipFile(prj) as archive:
            if archive.testzip() is not None:
                raise ValueError('Arquivo PRJ inválido')
        session = json.loads((OUT/f'{branch}-sessao-tempo.json').read_text(encoding='utf-8'))
        process = json.loads((OUT/f'{branch}-processamento-tempo.json').read_text(encoding='utf-8'))
        if not session['start']['mono'] <= process['start']['mono'] < process['end']['mono'] <= session['end']['mono']:
            raise ValueError('Tempos não aninhados')
        frozen = OUT/'congelados-apos-processamento'/branch
        if frozen.exists():
            raise FileExistsError(frozen)
        shutil.copytree(prj.parent.parent, frozen)
        files = [{'path': p.relative_to(prj.parent.parent).as_posix(), 'sha256': sha(p)}
                 for p in sorted(prj.parent.parent.rglob('*')) if p.is_file()]
        if not all(sha(frozen/r['path']) == r['sha256'] for r in files):
            raise ValueError('Congelamento divergente')
        branches[branch] = {'projectPath': str(prj), 'projectSha256': sha(prj), 'frozenFiles': files,
            'controlExports': {k: {t: v[t] for t in ['path', 'sha256']} for k, v in control.items()},
            'wallExportsR133': {k: {t: v[t] for t in ['path', 'sha256']} for k, v in wall.items()},
            'modelComparisonsControlToWall': comparison, 'addedNodalG2N1': nodal,
            'resultantOfN1AddedForces': resultant, 'conditionalPorticoIncrement': portico,
            'visualSummary': observations['branches'][branch], 'sessionTime': session, 'processingTimeObservation': process}
    paired = branches['CAD']['addedNodalG2N1'] == branches['BIM']['addedNodalG2N1']
    data = {'revision': 'H03/R134', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Controle L4/N1 malha10x10cm sem W15 em cópias R116, comparado às cópias R133 com W15.',
        'protectedR116Files': protected, 'protectedR133Files': old_protected, 'sourceFilesUnchanged': True,
        'branches': branches, 'pairedN1AddedLoadsEqual': paired, 'finerGridWithoutWallControlPerformed': True,
        'sameMeshControlIsolatesW15InN1Export': True, 'localSupportReactionsIndividuallyVerified': False,
        'meshConvergenceDemonstrated': False, 'firstMomentToleranceAcceptanceEstablished': False,
        'W15FinalAccepted': False, 'finalStructuralApproval': False, 'finalProductivityRankingAllowed': False,
        'SAP2000Executed': False, 'dimensioningPerformed': False, 'slabDeflectionPerformed': False,
        'monographEdited': False, 'CADorBIMTransferDefectProven': False,
        'axisReferences': ['https://docs.csiamerica.com/help-files/sap/Menus/Assign/Frame/Frame_Local_Axes.htm',
                           'https://docs.csiamerica.com/manuals/sap2000/CSiRefer.pdf#page=132']}
    (OUT/'R134-resultado.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'protectedR116': len(protected), 'protectedR133': len(old_protected), 'pairedNodal': paired,
                      'conditionalPortico': {b: r['conditionalPorticoIncrement'] for b, r in branches.items()}}, ensure_ascii=False))

if __name__ == '__main__':
    main()

"""Confere a seção nominal e a projeção entre apoios no controle Eberick."""
from collections import Counter
import argparse
import json
from pathlib import Path
import sys

from preparar_geometria import OUT, TARGET, NATIVE, read, sha
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'h03-r166'))
from auditar_receptor import association
from auditar_cobertura import (beam_frame, column_box, column_intervals, coverage,
                               endpoint_supports, ifcopenshell, rectangular_mesh)
from auditar_recepcao import parse_report
from ifcopenshell.util.element import get_container, get_psets


def audit(output=OUT, input_ifc=TARGET, revision='R230'):
    root = output / f'{revision}-BIM-SECOES-NOMINAIS-NAO-EXECUTAR'
    control = root / 'Arquivos do projeto/Modelo 3D.IFC'
    report = root / 'Arquivos do projeto/Documentos/Eberick/Relatorio_de_importacao_de_elementos_IFC.docx'
    project = root / 'Projeto Eberick' / (root.name + '.prj')
    timing = output / f'{revision}-tempo-observado.json'
    files = [control, report, project, timing, input_ifc, NATIVE]
    hashes = {p: sha(p) for p in files}
    native = read(NATIVE)['Readback']['Elements']
    sources = [e for e in native if e['Kind'] in ('beam', 'column')]
    rows = parse_report(report)
    model = ifcopenshell.open(str(control))
    if model.schema != 'IFC4':
        raise ValueError('Controle deve ser IFC4')
    origin_ifc = ifcopenshell.open(str(input_ifc))
    objects = {o.Tag: o for cls in ('IfcBeam', 'IfcColumn') for o in origin_ifc.by_type(cls)}
    expected = Counter((str(e['Id']), 'Vigas' if e['Kind'] == 'beam' else 'Pilares',
                        get_container(objects[str(e['Id'])]).Name) for e in sources)
    if Counter((r['revId'], r['group'], r['level']) for r in rows) != expected:
        raise ValueError('Relatório não corresponde às identidades/classes/níveis de origem')
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    parts = []
    for cls, kind in (('IfcBeam', 'beam'), ('IfcColumn', 'column')):
        for obj in model.by_type(cls):
            box = rectangular_mesh(obj, settings)
            props = get_psets(obj)
            concrete = props.get('Pset_ConcreteElementGeneral', {})
            matches = []
            for e in sources:
                if e['Kind'] != kind:
                    continue
                if kind == 'beam':
                    found = association(dict(geometry=box), e, endpoint_supports(e, native))
                    if found:
                        matches.append(e['Id'])
                else:
                    nominal = column_box(e)
                    if (all(abs(box[s][i] - nominal[s][i]) < 1e-4
                            for s in ('minM', 'maxM') for i in (0, 1))
                            and min(box['maxM'][2], nominal['maxM'][2])
                            - max(box['minM'][2], nominal['minM'][2]) > 1e-4):
                        matches.append(e['Id'])
            parts.append(dict(guid=obj.GlobalId, name=obj.Name, level=get_container(obj).Name,
                              kind=kind, candidates=matches, geometry=box,
                              concreteClass=concrete.get('StrengthClass'),
                              coverCm=concrete.get('ConcreteCover')))
    checked = []
    for e in sources:
        hits = [p for p in parts if p['candidates'] == [e['Id']]]
        if e['Kind'] == 'beam':
            along, _, start, end = beam_frame(e)
            supports = endpoint_supports(e, native)
            start = max([start] + [p['alongIntervalM'][1] for p in supports[0]])
            end = min([end] + [p['alongIntervalM'][0] for p in supports[1]])
            intervals = [(p['geometry']['minM'][along], p['geometry']['maxM'][along]) for p in hits]
            # Exclui somente intervalos ocupados por apoios de pilares nominais.
            support_intervals = [p['alongIntervalM'] for p in column_intervals(e, native)]
        else:
            start, end = e['AxisM'][2:]
            intervals = [(p['geometry']['minM'][2], p['geometry']['maxM'][2]) for p in hits]
            support_intervals = []
        checked.append(dict(id=e['Id'], mark=e['Mark'], kind=e['Kind'], parts=len(hits),
                            coverage=coverage(intervals + support_intervals, start, end)))
    if hashes != {p: sha(p) for p in files}:
        raise ValueError('Arquivo alterado durante auditoria')
    result = dict(
        revision=revision, reportCounts=dict(Counter(r['group'] for r in rows)),
        reportIdsClassesAndLevelsMatch=True,
        controlCounts=dict(Counter(o.is_a() for o in model.by_type('IfcElement'))),
        uniquePartMatches=dict(Counter(p['kind'] for p in parts if len(p['candidates']) == 1)),
        unmatchedOrAmbiguousParts=[p for p in parts if len(p['candidates']) != 1],
        originsWithMissingProjection=[p['mark'] for p in checked if not p['coverage']['noGapAboveTolerance']],
        originsWithParts=sum(p['parts'] > 0 for p in checked),
        receptionTiming=read(timing), nativeReopened=(output / f'{revision}-reaberto.png').is_file(),
        sectionAndTopToleranceM=.0002, meshToleranceM=1e-8,
        criteria='Configuração do último projeto aberto, CAD R227',
        analyticalConnectivityVerified=False, loadsApplied=False, structuralApproval=False,
        hashes={p.relative_to(output.parent).as_posix(): h for p, h in hashes.items()},
        parts=parts, origins=checked,
    )
    (output / f'{revision}-auditoria.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n',
                                                     encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('parts', 'origins', 'hashes')},
                     ensure_ascii=False))
    return result


def persistence(output):
    """Compara metadados e todas as caixas antes e depois da reabertura nativa."""
    first = output / 'R231-primeiro-controle.ifc'
    current = next((output / 'R231-BIM-SECOES-NOMINAIS-NAO-EXECUTAR').rglob('Modelo 3D.IFC'))
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    def snapshot(path):
        model = ifcopenshell.open(str(path))
        return {o.GlobalId: dict(cls=o.is_a(), name=o.Name, psets=get_psets(o),
                                geometry=rectangular_mesh(o, settings))
                for o in model.by_type('IfcElement')}
    before = snapshot(first)
    after = snapshot(current)
    if before != after:
        raise ValueError('O controle após reabertura difere do primeiro controle')
    result = dict(retainedElements=len(before), identitiesNamesGeometryAndPropertiesEqual=True,
                  firstIfcSha256=sha(first), reopenedIfcSha256=sha(current))
    (output / 'R231-persistencia.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--revision', choices=('R230', 'R231'), default='R230')
    args = parser.parse_args()
    if args.revision == 'R231':
        from preparar_continuidade import OUT as output, TARGET as target
        audit(output, target, args.revision)
        persistence(output)
    else:
        audit()

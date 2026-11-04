"""Confronta exportações genéricas e controle regenerado, sem editar PRJ."""
import argparse
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('compare', Path(__file__).parent.parent / 'h03-r176/comparar_receptores.py')
comp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(comp)


def models(folder):
    result = {}
    for path in folder.glob('*.$2k'):
        kind = ('portico' if path.name.startswith('portico_') else
                'escada' if 'escada' in path.name else
                'N1' if path.name.endswith('N1.$2k') else
                'N2' if path.name.endswith('N2.$2k') else None)
        if kind is None or kind in result:
            raise ValueError('Exportação desconhecida ou repetida')
        result[kind] = (path, comp.sap.parse(path.read_text(encoding='cp1252')))
    if set(result) != {'portico', 'escada', 'N1', 'N2'}:
        raise ValueError('Exportação incompleta')
    return result


def run(root):
    branches = {b: models(root / (b + '-generico')) for b in ('CAD', 'BIM')}
    regenerated = models(root / 'BIM-regerado')
    summary = {}
    for kind in ('portico', 'escada', 'N1', 'N2'):
        result = comp.compare(*(branches[b][kind][1] for b in ('CAD', 'BIM')))
        (root / f'R214-generico-{kind}.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        summary[kind] = {k: v for k, v in result.items() if k not in ('tables', 'nodalLoadDifferences')}
        summary[kind]['sectionDifferences'] = result['tables']['FRAME SECTION PROPERTIES 01 - GENERAL']
    section = [r for r in regenerated['N1'][1]['tables']['FRAME SECTION PROPERTIES 01 - GENERAL']
               if r['SectionName'] == 'R30x20']
    if len(section) != 1:
        raise ValueError('Seção de controle ausente ou ambígua')
    record = dict(revision='H03-R214', genericComparisons=summary,
                  regeneratedBimN1Section=section[0],
                  provenance=[dict(group=b, kind=k, name=p.name, sha256=comp.sha(p))
                              for b, entries in {**branches, 'BIM-regerado': regenerated}.items()
                              for k, (p, _) in entries.items()],
                  internalCauseProved=False, nativeSAPSolverExecuted=False,
                  structuralApproval=False, fullPairedFlowTimeMeasured=False)
    (root / 'R214-auditoria.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(genericN1=summary['N1']['sectionDifferences'], regeneratedSection=section[0]), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    run(parser.parse_args().folder)

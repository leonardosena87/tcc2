"""Reproduz a preparacao R95 com adaptador historico preservado; nao controla apps."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import sys
import time


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    p = argparse.ArgumentParser()
    for key in ('deps', 'source', 'proposal', 'registry', 'native', 'out'):
        p.add_argument('--'+key, type=Path, required=True)
    args = p.parse_args()
    sys.path.insert(0, str(args.deps))
    here = Path(__file__).resolve().parent
    a = module('historic_adapter', here/'adaptador_base_historico.py')
    audit = module('retention', here.parent/'h03-r94/auditar_intercambio.py')
    if args.out.exists():
        raise ValueError('Pasta de saida precisa ser nova, sem sobrescrita')
    protected = {str(path): a.sha(path) for path in
                 (args.source, args.proposal, args.registry, args.native, here/'adaptador_base_historico.py')}
    started, tick = datetime.now(timezone.utc).isoformat(), time.perf_counter()
    proposal = json.loads(args.proposal.read_text(encoding='utf-8-sig'))
    registry = json.loads(args.registry.read_text(encoding='utf-8-sig'))
    native = json.loads(args.native.read_text(encoding='utf-8-sig'))
    model = a.ifcopenshell.open(str(args.source))
    expected, objects = a.references(model, proposal, registry)
    before = a.audit(model, expected, objects)
    removed = a.remove_empty_storeys(model, [0., 3.])
    if a.audit(model, expected, objects) != before or len(model.by_type('IfcBuildingStorey')) != 3:
        raise ValueError('Normalizacao alterou produtos/nao produziu tres niveis')
    args.out.mkdir(parents=True)
    normalized = args.out/'H03-R95-3niveis.ifc'
    adapted = args.out/'H03-R95-geometria-nominal.ifc'
    model.write(str(normalized))
    result = a.adapt(normalized, args.proposal, args.registry, adapted)
    retention = audit.inspect_model(a.ifcopenshell.open(str(adapted)), native)
    if retention['unmatchedNativeIds'] or retention['matchingPropertyCounts'] != dict.fromkeys(audit.FIELDS, 62):
        raise ValueError('Retencao das quatro propriedades nao confirmada nos 62 elementos')
    if any(a.sha(path) != value for path, value in protected.items()):
        raise ValueError('Fonte mudou durante a preparacao')
    report = dict(revision='H03/R95', startedAtUtc=started,
                  endedAtUtc=datetime.now(timezone.utc).isoformat(), technicalScriptSeconds=time.perf_counter()-tick,
                  scriptTimeIsNotFlowTime=True, sources=protected, removedEmptyStoreys=removed,
                  adaptedGeometryCount=len(result['changes']), changedElementIds=[x['id'] for x in result['changes']],
                  matched=result['after']['matchedElements'], schemaValidationPassed=result['schemaValidationPassed'],
                  output=str(adapted), outputSha256=a.sha(adapted), propertyRetentionAfterAdapter=retention,
                  receiverImported=False, structuralApproval=False,
                  warning='Derivado com geometria nominal, nao IFC bruto. Limite textual C25 nao comprovado '
                          'do adaptador historico nao substitui R93/R94: compressao25 confirmada, material integral pendente.')
    (args.out/'R95-preparacao.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(matched=report['matched'], adapted=report['adaptedGeometryCount'],
                         matches=retention['matchingPropertyCounts'], outputSha256=report['outputSha256'])))


if __name__ == '__main__':
    main()

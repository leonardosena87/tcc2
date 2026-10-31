"""Auditoria de caixas/cobertura axial do IFC recebido, com regras derivadas R17."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys


def main():
    p = argparse.ArgumentParser()
    for key in ('deps', 'ifc', 'proposal', 'out'):
        p.add_argument('--'+key, type=Path, required=True)
    p.add_argument('--revision', default='H03/R95')
    args = p.parse_args()
    if args.out.exists():
        raise ValueError('Relatorio de saida precisa ser novo')
    sys.path.insert(0, str(args.deps))
    import ifcopenshell
    import ifcopenshell.geom as geom
    import ifcopenshell.validate
    from ifcopenshell.util.element import get_psets
    import regras_geometricas_derivadas as rules
    digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    hashes = {str(path): digest(path) for path in (args.ifc, args.proposal)}
    proposal = json.loads(args.proposal.read_text(encoding='utf-8-sig'))
    model = ifcopenshell.open(str(args.ifc))
    if model.schema != 'IFC4':
        raise ValueError('Ensaio delimitado ao IFC4 do receptor')
    settings = geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    rows = []
    for cls in ('IfcColumn', 'IfcBeam', 'IfcSlab'):
        for obj in model.by_type(cls):
            shape = geom.create_shape(settings, obj)
            verts = shape.geometry.verts
            rows.append(dict(ifcClass=cls, name=obj.Name, guid=obj.GlobalId,
                min=[min(verts[i::3]) for i in range(3)], max=[max(verts[i::3]) for i in range(3)],
                psets=get_psets(obj)))
            rows[-1]['class'] = rows[-1].pop('ifcClass')
    rules.TOL = 1e-5
    rules.close = lambda a,b: abs(a-b) <= rules.TOL
    rules.same = lambda a,b: len(a)==len(b) and all(rules.close(x,y) for x,y in zip(a,b))
    rules.columns = [e for e in proposal['elements'] if e['kind']=='column']
    rules.beams = [e for e in proposal['elements'] if e['kind']=='beam']
    result = rules.audit(rows)
    removed = next(r for r in rows if r['class']=='IfcBeam')
    altered = copy.deepcopy(rows)
    next(r for r in altered if r['class']=='IfcBeam')['min'][2] -= .01
    controls = dict(missingBeamPartDetected=not rules.audit([r for r in rows if r is not removed])['geometryPass'],
                    changedBeamHeightDetected=not rules.audit(altered)['geometryPass'],
                    duplicatedBeamPartDetected=not rules.audit(rows+[removed])['geometryPass'])
    if not all(controls.values()):
        raise ValueError('Controle de sensibilidade falhou')
    logger = ifcopenshell.validate.json_logger()
    ifcopenshell.validate.validate(model, logger)
    result.update(revision=args.revision, sources=hashes,
                  exportedCounts={c: len(model.by_type(c)) for c in ('IfcColumn','IfcBeam','IfcSlab')},
                  schema=model.schema, comparisonToleranceM=rules.TOL, sensitivityControls=controls,
                  schemaValidationMessages=[dict(level=s['level'], attribute=s.get('attribute'), message=s['message'])
                                            for s in logger.statements],
                  allExportedPartsStrengthClassC25=bool(rows) and all(r['psets'].get('Pset_ConcreteElementGeneral',{}).get('StrengthClass')=='C-25' for r in rows),
                  nativeGeometryRows=rows, structuralCalculationPerformed=False,
                  limits=['Caixas envolventes/cobertura axial, nao conectividade analitica.',
                          'Classe C25 no receptor nao prova transferencia causal a partir do IFC.',
                          'Ausencia de IfcSlab refere-se a saida estrutural completa, nao ao modelo externo vinculado.',
                          '1e-5m e criterio computacional, nao tolerancia normativa.'])
    if any(digest(Path(path)) != value for path,value in hashes.items()):
        raise ValueError('Fonte mudou durante a auditoria')
    result['sourcesUnchangedAfterRead'] = True
    with args.out.open('x', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps(dict(geometryPass=result['geometryPass'], columns=result['columnSegmentsMatching'],
                         beams=result['logicalBeamsPassing'], counts=result['exportedCounts'],
                         schemaValidationMessages=len(logger.statements), sensitivityControls=controls)))


if __name__ == '__main__':
    main()

"""Controle isolado25->30MPa no IFC derivado; nao altera especificacao do projeto."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def main():
    p=argparse.ArgumentParser()
    for k in ('deps','source','out'):p.add_argument('--'+k,type=Path,required=True)
    args=p.parse_args()
    if args.out.exists() or args.source.resolve()==args.out.resolve():
        raise ValueError('Saida deve ser nova e diferente da origem')
    sys.path.insert(0,str(args.deps))
    import ifcopenshell
    import ifcopenshell.validate
    digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
    source_hash=digest(args.source)
    m=ifcopenshell.open(str(args.source))
    before={e.id():str(e) for e in m}
    props=[e for e in m.by_type('IfcPropertySingleValue') if e.Name=='Compressão do concreto']
    if len(props)!=1 or props[0].NominalValue.is_a()!='IfcPressureMeasure' or props[0].NominalValue.wrappedValue!=25e6:
        raise ValueError('Origem nao corresponde ao controle esperado')
    if props[0].Unit is not None:raise ValueError('Unidade explicita nao prevista')
    pressure=[u for a in m.by_type('IfcUnitAssignment') for u in a.Units if getattr(u,'UnitType',None)=='PRESSUREUNIT']
    if len(pressure)!=1 or not pressure[0].is_a('IfcSIUnit') or pressure[0].Name!='PASCAL' or pressure[0].Prefix is not None:
        raise ValueError('Unidade de pressao deve ser Pascal sem prefixo')
    props[0].NominalValue=m.create_entity('IfcPressureMeasure',30e6)
    changed=[i for i in before if str(m.by_id(i))!=before[i]]
    if changed!=[props[0].id()] or len(list(m))!=len(before):raise ValueError('Mudanca adicional imprevista')
    logger=ifcopenshell.validate.json_logger();ifcopenshell.validate.validate(m,logger)
    if logger.statements:raise ValueError('Mensagens de validacao de esquema')
    args.out.parent.mkdir(parents=True,exist_ok=True);m.write(str(args.out))
    n=ifcopenshell.open(str(args.out))
    if {e.id():str(e) for e in n}!={e.id():str(e) for e in m}:raise ValueError('Releitura divergiu')
    if digest(args.source)!=source_hash:raise ValueError('Origem mudou')
    print(json.dumps(dict(sourceSha256=source_hash,outputSha256=digest(args.out),changedStepIds=changed,
                         allOtherRecordsIdentical=True,schemaValidationMessages=0,
                         projectSpecificationStillC25=True,experimentalControlOnly=True)))


if __name__=='__main__':main()

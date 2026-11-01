"""Confere controles das consultas reais R100; nao altera o Eberick."""
import argparse
import hashlib
import json
import re
from pathlib import Path

GENERAL_IDS = (102,103,164,163,165,179,106,110,107,120,125,129,121,126,130,
               124,131,162,123,122,127,190,128,276,277,278,279,285,112,109,108,111,191,113)
CLASS_IDS = (203,303,308,310,403,406,410,413,604,607,704,707,710,713,807)


def controls(text, ids):
    result = {}
    for control in ids:
        values = set()
        for line in text.splitlines():
            if re.search(r'\b(?:editar|caixa de combinação)\b', line):
                match = re.search(r' Value: (.*?) ID: ' + str(control) + r'$', line)
                if match:
                    values.add(match.group(1))
        if len(values) != 1:
            raise ValueError(f'Controle {control}: ausente ou ambiguo: {values}')
        result[str(control)] = values.pop()
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    args = ap.parse_args()
    out = args.root/'R100-cadastros-conferidos.json'
    if out.exists():
        raise SystemExit('Relatorio existente; nao sobrescrever')
    states = {}
    for branch, title in (('CAD','14-H03-R98-CAD-QT'), ('BIM','15-H03-R98-BIM-QT')):
        states[branch] = {}
        for view in ('materiais-geral', 'N2-materiais', 'N1-materiais', 'N0-materiais', 'classe-C25'):
            p = args.root/f'{branch}-{view}-UI.txt'
            data = p.read_bytes(); text = data.decode('utf-8-sig')
            if title not in text:
                raise ValueError('Copia incorreta: '+p.name)
            ids = CLASS_IDS if view=='classe-C25' else GENERAL_IDS
            states[branch][view] = dict(file=p.name,sha256=hashlib.sha256(data).hexdigest(),controls=controls(text,ids))
    comparisons = []
    for view in states['CAD']:
        a = states['CAD'][view]['controls']; b = states['BIM'][view]['controls']
        if a != b:
            raise ValueError('Cadastros diferentes: '+view)
        comparisons.append(dict(view=view,controlsMatched=len(a)))
    for branch in states:
        general = states[branch]['materiais-geral']['controls']
        for view in ('N2-materiais','N1-materiais','N0-materiais'):
            if states[branch][view]['controls'] != general:
                raise ValueError('Diferenca por pavimento: '+branch+'/'+view)
        expected = {'203':'C-25','303':'25','308':'1.4','403':'25','406':'10',
                    '413':'granito','604':'24150','607':'28000','807':'CP-II'}
        actual = states[branch]['classe-C25']['controls']
        for k,v in expected.items():
            if actual[k] != v:
                raise ValueError('Premissa C25 divergente: '+branch+'/'+k)
    prjs = []
    for folder,name,h in (
        ('14-H03-R98-CAD-QT-NAO-EXECUTAR','H03_CAD_R49_LAJES_NAO_EXECUTAR.prj','e2dc1d91fda030a981e8562d7c3d46318b8e6c262f9c4300415d4078027ca122'),
        ('15-H03-R98-BIM-QT-NAO-EXECUTAR','H03_BIM_R46_IFC_NAO_EXECUTAR.prj','41735ed0fdd0e2c0424dd84ef0b272418947b5c8bdb0cd1abcfa62c852917ccf')):
        p=args.root.parent/folder/'Projeto Eberick'/name
        actual=hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != h:
            raise ValueError('PRJ alterado: '+str(p))
        prjs.append(dict(path=str(p),sha256=actual,matched=True))
    result=dict(revision='H03/R100',states=states,comparisons=comparisons,
                matchedFieldComparisons=sum(r['controlsMatched'] for r in comparisons),
                prjs=prjs,uiQueriesCancelledAndProjectsClosedObserved=True,
                tableSteelRowsNotParsedByThisScript=True,elementOverridesVerified=False,
                structuralProcessingPerformed=False,structuralApproval=False,fullFlowRankingAllowed=False)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(matchedFieldComparisons=result['matchedFieldComparisons'],prjHashesMatched=2)))


if __name__=='__main__':
    main()

"""Confere leituras reais da UI e preservacao de fontes; nao interpreta o PRJ."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fields(path):
    result = {}
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        match = re.search(r'\beditar .*?Value: (.*?) ID: (\d+)$', line)
        if match:
            value, key = match.groups()
            if key in result and result[key] != value:
                raise ValueError('Valores conflitantes no mesmo controle')
            result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    out = args.root/'R97-cadastro-conferido.json'
    if out.exists():
        raise ValueError('Relatorio precisa ser novo')
    prep = read(args.root/'R97-preparacao.json')
    readings, protection = {}, []
    expected = {'121':'Q_TELHADO_MANUTENCAO','122':'QT','131':'1.40','216':'1.50',
                '152':'0.50','153':'0.40','154':'0.30'}
    for branch in ('CAD','BIM'):
        path = args.root/f'{branch}-QT-apos-reabrir-UI.txt'
        values = fields(path)
        if len(values) != 20 or any(values.get(k) != v for k,v in expected.items()):
            raise ValueError('Cadastro relido nao corresponde ao esperado')
        timing_path = args.root/f'R97-tempo-{branch}.json'
        readings[branch] = dict(fieldsByControlId=values, uiTextSha256=sha(path), timing=read(timing_path),
            savedClosedReopened=True, combinationsVisualRead=dict(active=True, isolated=True,
                favorableEffect=False, automaticGeneration=True, combineBetweenAccidentals=False),
            combinationImageSha256=sha(args.root/f'{branch}-combinacoes-apos-reabrir.png'))
        copy = next(c for c in prep['copies'] if c['branch']==branch)
        for item in copy['sourceFiles']:
            source = Path(copy['source'])/item['relativePath']
            protection.append(dict(branch=branch, path=str(source), preserved=sha(source)==item['sha256']))
        prj = Path(copy['prj'])
        old = next(f['sha256'] for f in copy['sourceFiles'] if f['relativePath'].endswith('.prj'))
        readings[branch]['prj'] = dict(path=str(prj),beforeSha256=old,afterSha256=sha(prj),
                                      binaryChanged=sha(prj)!=old)
    if not all(row['preserved'] for row in protection):
        raise ValueError('Fonte protegida foi modificada')
    if readings['CAD']['fieldsByControlId'] != readings['BIM']['fieldsByControlId']:
        raise ValueError('Campos CAD/BIM divergem')
    result = dict(revision='H03/R97',atUtc=datetime.now(timezone.utc).isoformat(),
        status='Acao QT cadastrada e relida nos dois ramos; cargas pontuais ainda nao aplicadas.',
        branches=readings,equalDistinctUiFields=20,sourceFilesProtected=protection,
        qtNodalLoadsApplied=False,plannedQtNodesPerBranch=13,structuralProcessingPerformed=False,
        analysisInvalidatedByActionChange=True,humanInterventionRequests=3,humanAssistedBranches=2,
        originalQEdited=False,originalQPostChangeReadBack=False,finalFlowTimesAvailable=False,
        monographChanged=False,rankingAllowed=False,
        limits=['Leitura da interface e hashes; nao auditoria semantica integral do binario.',
                'Estado das caixas registrado visualmente nas imagens; nao inferido da arvore textual.',
                'Casos efetivos e combinacoes precisam ser relidos apos aplicacao das cargas.',
                'Cadastro com assistencia humana; nao demonstracao de automacao integral.',
                'Tempos incluem esperas e trabalho independente; nao comparar produtividade.',
                'Saidas de processamento anteriores nao sao resultados recalculados desta revisao.'])
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(equalFields=20,sourceFilesPreserved=len(protection),
                         actionReadBackBothBranches=True,qtNodalLoadsApplied=False)))


if __name__ == '__main__':
    main()

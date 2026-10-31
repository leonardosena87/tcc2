"""Consolida arquivos reais R96; nao automatiza nem substitui a leitura da UI."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    for key in ('root', 'native', 'previous'):
        parser.add_argument('--'+key, type=Path, required=True)
    args = parser.parse_args()
    out = args.root/'R96-estado-final.json'
    if out.exists():
        raise ValueError('Saida deve ser nova')
    prep = read(args.root/'R96-preparacao.json')
    geometry = read(args.root/'R96-auditoria-receptor-FINAL.json')
    frozen = read(args.root/'R96-congelamento.json')
    timing = read(args.root/'R96-tempo-recepcao.json')
    previous = read(args.previous)
    observed = read(args.root/'R96-leitura-UI.json')
    if digest(Path(prep['source'])) != prep['sourceSha256'] or digest(Path(prep['output'])) != prep['outputSha256']:
        raise ValueError('IFC de entrada ou origem mudou')
    rows = prep['retentionAudit']['rows']
    if len(rows) != 62 or any(r['properties']['compressionMPa']['value'] != 30 for r in rows):
        raise ValueError('Entrada nao corresponde ao controle 30MPa nos62 elementos')
    if not geometry['geometryPass'] or not geometry['allExportedPartsStrengthClassC25']:
        raise ValueError('Resultado divergiu da hipotese observada; revisar conclusao')
    native = read(args.native)
    origins = {str(e['id']): e for e in native['elements'] if e['category'] in ('Quadro estrutural', 'Pilares estruturais')}
    report = args.root/'R96-relatorio-importacao.txt'
    ids = re.findall(r'^Nome IFC: .+:(\d+) - Pavimento IFC:', report.read_text(encoding='utf-8-sig'), re.M)
    if len(ids) != 51 or len(set(ids)) != 51 or set(ids) != set(origins):
        raise ValueError('Origens do relatorio nao conciliam com as51 origens nativas')
    preservation = []
    for item in frozen['files']:
        working = Path(frozen['source'])/item['relativePath']
        copy = Path(frozen['copy'])/item['relativePath']
        preservation.append(dict(relativePath=item['relativePath'], frozenCopyMatches=digest(copy)==item['sha256'],
                                 workingExists=working.exists(), workingMatches=working.exists() and digest(working)==item['sha256']))
    if not all(p['frozenCopyMatches'] for p in preservation):
        raise ValueError('Congelamento nao preservado')
    prj = next(p for p in preservation if p['relativePath'].endswith('.prj'))
    if not prj['workingMatches']:
        raise ValueError('PRJ mudou apos leitura/exportacao; registrar antes de concluir')
    if observed['strengthClass'] != 'C-25' or observed['fckMPa'] != 25 or not previous['allExportedPartsStrengthClassC25']:
        raise ValueError('Leitura ou comparador nao corresponde ao ensaio')
    result = dict(revision='H03/R96', consolidatedAtUtc=datetime.now(timezone.utc).isoformat(),
        purpose='Controle experimental25->30MPa; especificacao do projeto continuaC25.',
        entryElementsAt30MPa=len(rows), matchedOriginIds=len(ids),
        originCategoryCounts=dict(Counter(origins[i]['category'] for i in ids)),
        sourceEntityChangedOnly=prep['changedStepIds'], allOtherStepRecordsIdentical=prep['allOtherStepRecordsIdentical'],
        nativeGeometry=dict(columnSegments=geometry['columnSegmentsMatching'], logicalBeams=geometry['logicalBeamsPassing'],
                            exportedCounts=geometry['exportedCounts'], geometryPass=geometry['geometryPass'],
                            scope='Caixas e cobertura axial; nao conectividade analitica.',
                            schemaValidationMessages=len(geometry['schemaValidationMessages'])),
        materialObservation=observed,
        comparison=dict(previousRevision=previous['revision'], previousOutputClass='C-25', controlInputMPa=30,
                        controlOutputClass='C-25', nativeExportPartsWithC25=len(geometry['nativeGeometryRows']),
                        conclusion='A propriedade de compressao alterada noIFC nao atualizou a classe nativa exportada neste caminho/configuracao.'),
        receptionTiming=timing, preservation=preservation, nativePrjUnchangedAfterReadAndExport=True,
        sources={str(p):digest(p) for p in (args.native,args.previous,report,args.root/'R96-leitura-UI.json',
                 args.root/'R96-preparacao.json',args.root/'R96-auditoria-receptor-FINAL.json')},
        interventionCount=None, correctionTimeMs=None, flowTotalMs=None, rankingAllowed=False,
        structuralCalculationPerformed=False,
        limits=['Leitura daUI registrada manualmente a partir do controle nativo; nao e parse do PRJ.',
                'Uma configuracao/importador/edificacao e uma propriedade perturbada; nao generalizar a toda interoperabilidade.',
                'Nao se altera C25 do projeto principal nem se aprova dimensionamento.',
                '54partes observadas nao equivalem a54erros ou54correcoes.',
                'Lajes ausentes na saida estrutural nao significam ausencia no vinculo externo.',
                'Tempo e recorte prospectivo, inclui trabalho intercalado; nao e total ou ranking.'])
    with out.open('x', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps(dict(matchedOriginIds=len(ids), outputClass='C-25', nativePrjUnchanged=prj['workingMatches'],
                         frozenFilesVerified=len(preservation), wallMs=timing['wallMs'])))


if __name__ == '__main__':
    main()

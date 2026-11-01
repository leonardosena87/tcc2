"""Lê exportações textuais nativas, sem editar o modelo ou executar SAP2000."""
import hashlib
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import zipfile

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Extensao-W03-H03-R122-CONSULTA-NAO-EXECUTAR')
TOKEN = re.compile(r'(\w+)=("[^"]*"|\S+)')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse(text):
    tables, current = {}, None
    for line in text.splitlines():
        if not line.strip():
            continue
        if line.strip() == 'END TABLE DATA':
            current = None
            continue
        heading = re.fullmatch(r'TABLE:\s+"([^"]+)"', line.strip())
        if heading:
            current = heading[1]
            if current in tables:
                raise ValueError('Tabela repetida: ' + current)
            tables[current] = []
        else:
            row = {m[1]: m[2].strip('"') for m in TOKEN.finditer(line)}
            if current is None or not row:
                raise ValueError('Linha não reconhecida: ' + line)
            tables[current].append(row)
    control = tables.get('PROGRAM CONTROL', [])
    if len(control) != 1 or control[0].get('CurrUnits') != 'Kgf, cm, C':
        raise ValueError('Unidade não suportada; não inferir escala')
    joints = {}
    for row in tables['JOINT COORDINATES']:
        if row['Joint'] in joints or row['CoordSys'] != 'GLOBAL' or row['CoordType'] != 'Cartesian':
            raise ValueError('Nó duplicado ou coordenada não global cartesiana')
        joints[row['Joint']] = tuple(number(row[k]) for k in ['XorR', 'Y', 'Z'])
    frames = {}
    for row in tables['CONNECTIVITY - FRAME']:
        key = row['Frame']
        if key in frames:
            raise ValueError('Barra duplicada')
        frames[key] = (joints[row['JointI']], joints[row['JointJ']])
    return {'tables': tables, 'joints': joints, 'frames': frames, 'units': control[0]['CurrUnits']}


def number(value):
    result = float(value.replace(',', '.'))
    if not math.isfinite(result):
        raise ValueError('Número não finito')
    return result


def span(model, a, b):
    matches = [(key, ends) for key, ends in model['frames'].items() if sorted(ends) == sorted([a, b])]
    if len(matches) != 1:
        raise ValueError('Extensão analítica ausente ou ambígua')
    key, ends = matches[0]
    rows = [r for r in model['tables']['FRAME LOADS - DISTRIBUTED'] if r['Frame'] == key and r['LoadPat'] == 'G2']
    length = math.dist(*ends)
    loads = []
    for row in rows:
        if (row['CoordSys'], row['Type'], row['Dir'], row['DistType']) != ('LOCAL', 'Force', '2', 'RelDist'):
            raise ValueError('Representação de carga não suportada')
        start, end, qa, qb = [number(row[k]) for k in ['RelDistA', 'RelDistB', 'FOverLA', 'FOverLB']]
        if not 0 <= start < end <= 1:
            raise ValueError('Intervalo relativo inválido')
        integral = (qa + qb) / 2 * length * (end - start)
        loads.append({'raw': row, 'relativeStart': start, 'relativeEnd': end,
                      'qStartExportedKgfPerCm': qa, 'qEndExportedKgfPerCm': qb,
                      'loadedLengthCm': length * (end - start),
                      'signedIntegralInLocalDirection2Kgf': integral,
                      'magnitudeTf': abs(integral) / 1000})
    return {'frameId': key, 'endpointsCm': ends, 'lengthCm': length, 'G2DistributedLoads': loads}


def geometry_comparison(a, b):
    points = [Counter(m['joints'].values()) for m in [a, b]]
    edges = [Counter(tuple(sorted(v)) for v in m['frames'].values()) for m in [a, b]]
    return {'jointCoordinateMultisetEqualAtExportPrecision': points[0] == points[1],
            'frameEndpointMultisetEqualAtExportPrecision': edges[0] == edges[1],
            'jointCount': {k: len(m['joints']) for k, m in [('CAD', a), ('BIM', b)]},
            'frameCount': {k: len(m['frames']) for k, m in [('CAD', a), ('BIM', b)]},
            'doesNotCompareSectionsReleasesAxesLoadsOrResults': True}


def main():
    if (OUT / 'R122-resultado.json').exists():
        raise FileExistsError('Não substituir resultado existente')
    preparation = json.loads((OUT / 'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = []
    for row in preparation['files']:
        item = {**row, 'sourceSha256After': sha(Path(row['source']))}
        if item['sourceSha256After'] != item['sha256Before']:
            raise ValueError('Fonte R121 alterada')
        protected.append(item)
    branches, models = {}, {}
    for branch in ['CAD', 'BIM']:
        prj_row = next(r for r in preparation['files'] if r['branch'] == branch and r['copy'].endswith('.prj'))
        prj = Path(prj_row['copy'])
        if sha(prj) != prj_row['sha256Before']:
            raise ValueError('PRJ mudou durante consulta/exportação')
        with zipfile.ZipFile(prj) as archive:
            if archive.testzip() is not None:
                raise ValueError('Falha no arquivo PRJ')
        files = sorted((OUT / ('SAP-' + branch)).glob('*.$2k'))
        if len(files) != 3:
            raise ValueError('Exportação incompleta')
        models[branch] = {}
        for file in files:
            parsed = parse(file.read_text(encoding='cp1252'))
            kind = 'portico' if file.name.startswith('portico') else ('N1' if '-N1.' in file.name or '_N1.' in file.name else 'N2')
            if kind in models[branch]:
                raise ValueError('Tipo de exportação repetido')
            models[branch][kind] = parsed
        target = span(models[branch]['portico'], (0, 705, 320), (440, 705, 320))
        neighbor = span(models[branch]['portico'], (440, 705, 320), (965, 705, 320))
        if len(target['G2DistributedLoads']) != 1 or neighbor['G2DistributedLoads']:
            raise ValueError('Distribuição G2 não corresponde ao ensaio isolado')
        q = target['G2DistributedLoads'][0]
        if q['relativeStart'] != 0 or q['relativeEnd'] != 1 or q['qStartExportedKgfPerCm'] != -4.44 or q['qEndExportedKgfPerCm'] != -4.44:
            raise ValueError('Carga exportada inesperada; requer revisão')
        ui_name = 'CAD-trecho-vizinho-V5-UI.txt' if branch == 'CAD' else 'BIM-trecho-vizinho-segundo-V1-UI.txt'
        ui = (OUT / ui_name).read_text(encoding='utf-8')
        project_prefix = '38-H03-R122-CAD' if branch == 'CAD' else '39-H03-R122-BIM'
        if project_prefix not in ui or not re.search(r'editar \(disabled, settable, string\) Carga extra Value: 0 ID:', ui):
            raise ValueError('Consulta nativa do vizinho sem identificação/carga zero')
        timer = json.loads((OUT / f'{branch}-sessao-tempo.json').read_text(encoding='utf-8'))
        if timer['durationMs'] <= 0 or not math.isclose(timer['end']['mono'] - timer['start']['mono'], timer['durationMs']):
            raise ValueError('Intervalo temporal inválido')
        branches[branch] = {'projectPath': str(prj), 'projectSha256': sha(prj),
                            'prjUnchangedSinceCopyPreparation': True, 'targetW03': target,
                            'neighborW04': neighbor, 'neighborNativeExtraDisplayedKNm': 0,
                            'exportUnits': models[branch]['portico']['units'],
                            'exportFiles': [{'path': p.relative_to(OUT).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size} for p in files],
                            'sessionTime': timer}
    # kgf/cm * cm -> kgf. This identity does not calibrate SI units in the Eberick UI.
    integral_tf = branches['CAD']['targetW03']['G2DistributedLoads'][0]['magnitudeTf']
    result = {'revision': 'H03/R122', 'createdAtUtc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Consulta da extensão de carga G2 no arquivo analítico exportado pelo Eberick, sem importação/análise no SAP2000.',
              'branches': branches,
              'geometryOnlyComparison': {kind: geometry_comparison(models['CAD'][kind], models['BIM'][kind]) for kind in ['portico', 'N1', 'N2']},
              'reconciliation': {'exportedLoadedLengthM': 4.4, 'freeMasonryLengthMFromR120': 4.2,
                  'differenceM': 0.2, 'endOverrunsM': [0.1, 0.1],
                  'lengthExcessPercentRelativeToFree': (4.4 / 4.2 - 1) * 100,
                  'exportedSignedQKgfPerCm': -4.44, 'exportedMagnitudeTf': integral_tf,
                  'R121DisplayedAdditionalDeltaTf': 1.95, 'arithmeticFitsR121RoundedDifferenceInterval': 1.94 <= integral_tf <= 1.96,
                  'displayedDifferenceAloneWasNotUsedToIdentifyLength': True,
                  'interfaceExtraDisplayKNm': 4.44,
                  'exportedQConvertedConventionallyToKNm': 4.44 * 100 * 9.80665 / 1000,
                  'SIConversionBetweenNativeUIAndExportVerified': False,
                  'internalStoredPrecisionVerified': False,
                  'nativeAnalyticalModelInternalsIdenticalToExportProved': False},
              'protectedSourceR121Files': protected, 'sourceR121FilesUnchanged': True,
              'exportPerformedInEberick': True, 'SAP2000Executed': False,
              'nativeLoadOrGeometryEditsPerformed': False, 'processingPerformed': False,
              'finalWallLoadApplicationAccepted': False, 'finalStructuralApproval': False,
              'finalProductivityRankingAllowed': False, 'monographEdited': False,
              'limitations': ['Igualdade geométrica é limitada à precisão de coordenadas exportadas e não compara propriedades/solturas/eixos/resultados.',
                  'Opção Exportar seções estava ativa; documentação do fabricante alerta diferenças de inércia e hipótese de diafragma na utilização externa.',
                  'Não se executou SAP2000, nem análise independente ou dinâmica.',
                  'Equivalência de 4,44 kN/m exibidos para 4,44 kgf/cm exportados exige reconciliar a convenção de unidades; não tratar como falha IFC/CAD demonstrada.',
                  'Consulta do vizinho confirma soma extra exibida zero e ausência de G2 distribuída no trecho exportado, sem auditar todas as outras ações nativas.',
                  'Tempos incluem exploração, pesquisa e interface; não somar a intervalos contidos e não classificar produtividade.'],
              'nextStep': 'Resolver a representação parcial da alvenaria e convenção de unidades em cópia isolada. Não reduzir q apenas para forçar resumo. Preservar as R116 e R121.',
              'technicalSource': 'https://suporte.altoqi.com.br/hc/pt-br/articles/360016037073'}
    (OUT / 'R122-resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'protectedFiles': len(protected), 'prjsUnchanged': True, 'reconciliation': result['reconciliation'], 'geometryOnlyComparison': result['geometryOnlyComparison']}))


if __name__ == '__main__':
    main()

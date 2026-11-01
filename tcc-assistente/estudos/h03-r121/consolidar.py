"""Conserva sensibilidade da carga linear sem promovê-la a parede resolvida."""
import importlib.util
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Parede-W03-H03-R121-ESTUDO-NAO-EXECUTAR')
spec = importlib.util.spec_from_file_location('r116', HERE.parent / 'h03-r116/consolidar.py')
r116 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r116)
sha = r116.sha


def unique_field(text, label, disabled=False):
    modifier = 'disabled, ' if disabled else ''
    matches = set(re.findall(r'editar \(' + modifier + r'settable, string\) ' + re.escape(label) + r' Value: (.*?) ID:', text))
    if len(matches) != 1: raise ValueError('Campo ausente ou conflitante: ' + label)
    return matches.pop()


def load_extent_diagnostic(before_tf, after_tf, q_entered=4.4446, free_length=4.2, axis_length=4.4):
    delta = round(after_tf - before_tf, 6)
    interval = [round(delta - 0.01, 6), round(delta + 0.01, 6)]
    hypotheses = []
    for factor in [10.0, 9.80665]:
        for length, label in [(free_length, 'faixa livre de alvenaria'), (axis_length, 'entre eixos de pilares')]:
            prediction = q_entered * length / factor
            hypotheses.append({'lengthM': length, 'lengthMeaning': label,
                               'kNPerTfHypothetical': factor, 'predictedTf': prediction,
                               'fallsInDisplayedDifferenceInterval': interval[0] <= prediction <= interval[1]})
    return {'displayedDeltaTf': delta, 'differenceIntervalTfAssumingNearestHundredthRounding': interval,
            'hypotheses': hypotheses, 'effectiveLengthVerified': False, 'unitConversionCalibrated': False,
            'note': 'Diferença entre resumos arredondados não identifica sozinha extensão/sinal/unidade internos; valores são hipóteses aritméticas, não calibração.'}


def main():
    if (OUT / 'R121-resultado.json').exists(): raise FileExistsError('Não substituir resultado')
    prep = json.loads((OUT / 'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = [{**r, 'afterSha256': sha(Path(r['source']))} for r in prep['files']]
    if any(r['sha256Before'] != r['afterSha256'] for r in protected): raise ValueError('Fonte R116 alterada')
    baseline_path = HERE.parent / 'h03-r116/R116-resultado.json'
    baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
    branches = {}
    for branch, name in [('CAD','V3'), ('BIM','V1')]:
        folder = '36-H03-R121-CAD' if branch == 'CAD' else '37-H03-R121-BIM'
        before_path, after_path = [OUT / f'{branch}-{name}-{suffix}-UI.txt' for suffix in ['antes','reaberto']]
        before, after = [p.read_text(encoding='utf-8') for p in [before_path, after_path]]
        for text in [before, after]:
            if folder not in text or unique_field(text,'Nome') != name: raise ValueError('Projeto ou peça incorretos')
        if float(unique_field(before,'Carga extra',True)) != 0: raise ValueError('Carga prévia diferente de zero')
        if float(unique_field(after,'Carga extra',True)) != 4.44: raise ValueError('Retenção exibida divergente')
        before_section = {k: float(unique_field(before,k)) for k in ['bw','h','/']}
        after_section = {k: float(unique_field(after,k)) for k in ['bw','h','/']}
        if before_section != after_section: raise ValueError('Seção/elevação mudaram')
        evidence = OUT / f'{branch}-resumo-analise-UI.txt'
        text = evidence.read_text(encoding='utf-8')
        if folder not in text: raise ValueError('Resumo incorreto')
        summary = r116.extract(text)
        status = (OUT / f'{branch}-processamento-estado-UI.txt').read_text(encoding='utf-8')
        if folder not in status or 'Estrutura processada com avisos' not in status: raise ValueError('Término não confirmado')
        session = json.loads((OUT / f'{branch}-sessao-tempo.json').read_text(encoding='utf-8'))
        command = json.loads((OUT / f'{branch}-processamento-tempo.json').read_text(encoding='utf-8'))
        r116.check_time(session, command)
        prj = Path(next(r['copy'] for r in prep['files'] if r['branch']==branch and r['copy'].endswith('.prj')))
        saved = json.loads((OUT / f'{branch}-prj-antes-consulta.json').read_text(encoding='utf-8'))
        if sha(prj) != saved['sha256']: raise ValueError('PRJ mudou durante releitura')
        with zipfile.ZipFile(prj) as z:
            if z.testzip() is not None: raise ValueError('PRJ com falha ZIP')
        old = baseline['branches'][branch]['summary']
        branches[branch] = {'projectPath':str(prj), 'projectSha256':sha(prj),
            'prjUnchangedDuringReadback':True, 'prjReadbackHashScope':saved['scope'],
            'beam':name, 'floor':'N1' if branch=='CAD' else 'TCC-cdd31967-N1',
            'beforeExtraDisplayedKNm':0.0, 'typedExtraKNm':4.4446, 'afterExtraDisplayedKNm':4.44,
            'internalStoredExtraKNm':None,
            'sectionBeforeAfterCm':before_section,
            'actionRowsTranscription':{'method':'Transcrição visual de imagens; a grade não expõe valores por UIA.',
                'before':{'Adicional':0,'Solo':0,'Acidental':0,'Água':0,'Subpressão':0,'Q_TELHADO_MANUTENCAO':0},
                'after':{'Adicional':4.44,'Solo':0,'Acidental':0,'Água':0,'Subpressão':0,'Q_TELHADO_MANUTENCAO':0}},
            'summary':summary, 'deltaVerticalDisplayedTfFromOwnR116':{k:round(v-old['verticalLoadsDisplayedTf'][k],6) for k,v in summary['verticalLoadsDisplayedTf'].items()},
            'loadExtentDiagnostic':load_extent_diagnostic(old['verticalLoadsDisplayedTf']['Adicional'],summary['verticalLoadsDisplayedTf']['Adicional']),
            'sessionTime':session, 'processingTimeObservation':command,
            'evidence': [{'path':p.name,'sha256':sha(p)} for p in sorted(OUT.glob(f'{branch}-*')) if p.suffix in {'.txt','.jpg','.json'}]}
    frozen = OUT / 'congelados-apos-ensaio'
    if frozen.exists(): raise FileExistsError('Congelado existente')
    frozen.mkdir()
    for branch,b in branches.items():
        src=Path(b['projectPath']).parents[1]; dst=frozen/branch
        shutil.copytree(src,dst)
        files=[{'path':p.relative_to(src).as_posix(),'sha256':sha(p)} for p in sorted(src.rglob('*')) if p.is_file()]
        if not all(sha(dst/r['path'])==r['sha256'] for r in files): raise ValueError('Congelamento divergente')
        b['frozenFiles']=files
    cad,bim=[branches[b]['summary'] for b in ['CAD','BIM']]
    comparison = r116.r111.r106.comparison(cad,bim)
    comparison.update({'verticalDisplayedEqual':cad['verticalLoadsDisplayedTf']==bim['verticalLoadsDisplayedTf'],
        'gammaZDisplayedEqual':cad['gammaZDisplayed']==bim['gammaZDisplayed'],
        'topDisplayedEqual':cad['topDisplacementsRawUnitNotExplicit']==bim['topDisplacementsRawUnitNotExplicit'],
        'actionRowsVisualEqual':branches['CAD']['actionRowsTranscription']==branches['BIM']['actionRowsTranscription']})
    result={'revision':'H03/R121','createdAtUtc':datetime.now(timezone.utc).isoformat(),
        'scope':'Ensaio de carga extra Adicional no trecho N1 CAD V3 / BIM primeiro trecho V1; extensão efetiva ainda não reconciliada à faixa W03.',
        'branches':branches,'comparison':comparison,
        'protectedSourceR116Files':protected,'sourceR116FilesUnchanged':True,
        'baseline':{'path':str(baseline_path),'sha256':sha(baseline_path)},
        'analysisScope':'Estática + ELS-DEF pórtico com rigidez configurada, sem dimensionamento, fissuração, flechas de lajes ou dinâmica.',
        'CADNodeAttempt':{'typedCm':'10,705','nativeMessage':'Já existe um nó nesta posição no pavimento.',
                          'duplicateCreated':False,'doesNotProveExactEndpointOrTolerance':True},
        'processingPerformed':True,'finalWallLoadApplicationAccepted':False,
        'dimensioningPerformed':False,'monographEdited':False,'rvtDwgEdited':False,
        'finalStructuralApproval':False,'finalRankingAllowed':False,
        'nextStep':'Definir extensão analítica carregada e unidade/precisão sem calibrar cargas apenas para igualar resumo; conferir trecho vizinho BIM com mesmo nome, preservar seção e ligações.',
        'limits':['Ensaio isolado, não lançamento definitivo de W03 ou outras paredes.',
                  'Acrescimo exibido 1,95tf não corresponde diretamente à magnitude livre 18,66732kN; extensão/unidade/precisão ainda não comprovadas.',
                  'Gama-Z X+ 1,10 igual ao limite exibido não constitui aprovação normativa por arredondamento.',
                  'Direção relativa CAD Y-/BIM Y+ permanece sem causa demonstrada.',
                  'Nenhuma resistência de elementos/armaduras, fundação, metal, tanque ou vento definitivo verificada.',
                  'Tempos incluem pesquisa/interface/aprendizagem e retomada; comando contido na sessão, sem soma e sem ranking.']}
    (OUT/'R121-resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'protectedFiles':len(protected),'frozenFiles':{b:len(v['frozenFiles']) for b,v in branches.items()},'comparison':comparison,'deltas':{b:v['deltaVerticalDisplayedTfFromOwnR116'] for b,v in branches.items()}}))


if __name__=='__main__':main()

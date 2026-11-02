"""Compara rótulos numéricos de diagramas G2; não calcula reações/molas."""
import hashlib
import importlib.util
import json
import re
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Reacoes-Grelha-H03-R140-CONSULTA-NAO-EXECUTAR')
spec = importlib.util.spec_from_file_location('r130dxf', HERE.parent/'h03-r130/ler_dxf.py')
dxf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dxf)
EPS = D('0.000001')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def labels(path):
    es = dxf.entities(path)
    numeric, beam_labels, slab_names = {}, [], []
    for e in es:
        if dxf.one(e,0) != 'MTEXT':
            continue
        text = dxf.one(e,1)
        if re.fullmatch(r'L[1-6]',text):
            slab_names.append(text)
        if re.fullmatch(r'V\d+\[q=-?\d+\.\d+\]',text):
            beam_labels.append(text)
        if dxf.one(e,8) != 'DI-Textos' or not re.fullmatch(r'-?\d+\.\d{2}',text):
            continue
        xyz = tuple(D(dxf.one(e,c)) for c in [10,20,30])
        key = tuple(v.quantize(EPS) for v in xyz)
        if key in numeric:
            raise ValueError('Posição de rótulo numérico não única')
        numeric[key] = {'text':text,'value':D(text),'xyz':xyz}
    if sorted(slab_names) != ['L1','L2','L3','L4','L5','L6'] or len(numeric) != 25 or len(beam_labels) != 24:
        raise ValueError('Diagrama fora do escopo ou incompleto')
    return numeric, beam_labels

def compare(a,b):
    left, right = labels(a)[0], labels(b)[0]
    if set(left) != set(right):
        raise ValueError('Posições de rótulos não correspondentes')
    rows=[]
    for key in sorted(left):
        x,y=left[key],right[key]
        if max(abs(p-q) for p,q in zip(x['xyz'],y['xyz'])) > EPS:
            raise ValueError('Desenhos desalinhados')
        rows.append({'positionDrawingRaw':[str(v) for v in x['xyz']],
            'left':x['text'],'right':y['text'],'deltaRightMinusLeft':str(y['value']-x['value'])})
    return {'numericLabelCount':len(rows),'changedLabelCount':sum(D(r['deltaRightMinusLeft']) != 0 for r in rows),
        'maxAbsDeltaDisplayed':str(max(abs(D(r['deltaRightMinusLeft'])) for r in rows)),
        'labels':rows,'matching':'Posição no desenho 2D, tolerância 1e-6 de unidade gráfica; nomes V ignorados',
        'unitPrintedInDXF':False,'forceOrMomentIntegralCalculated':False}

def main():
    target=OUT/'R140-resultado.json'
    if target.exists():
        raise FileExistsError(target)
    prep=json.loads((OUT/'R140-preparacao.json').read_text(encoding='utf-8'))
    r139=json.loads((HERE.parent/'h03-r139/R139-resultado.json').read_text(encoding='utf-8'))
    protected=[]
    for r in prep['files']:
        if sha(r['source']) != r['sha256']:
            raise ValueError('Fonte R138 alterada')
        protected.append({'path':r['source'],'sha256':r['sha256'],'revision':'R138'})
    for r in r139['protectedR137Files']:
        if sha(r['path']) != r['sha256']:
            raise ValueError('Fonte R137 alterada')
        protected.append({**r,'revision':'R137'})
    sessions={}
    for label in ['CAD','BIM','CAD-controle','BIM-controle']:
        s=json.loads((OUT/f'{label}-consulta-fim.json').read_text(encoding='utf-8'))
        first=json.loads((OUT/f'{label}-consulta-inicio.json').read_text(encoding='utf-8'))
        if s['inicio_utc'] != first['inicio_utc'] or s['path'] != first['path'] or s['sha256Before'] != first['sha256Before']:
            raise ValueError('Registro de início incompatível')
        if not s['unchanged'] or s['sha256After'] != s['sha256Before'] or sha(s['path']) != s['sha256Before']:
            raise ValueError('PRJ de consulta alterado')
        elapsed=(datetime.fromisoformat(s['fim_utc'])-datetime.fromisoformat(s['inicio_utc'])).total_seconds()
        if elapsed <= 0:
            raise ValueError('Intervalo não positivo')
        sessions[label]={**s,'durationSeconds':elapsed,'durationMinutes':elapsed/60,
            'category':'consulta exploratória de resultados já processados',
            'humanInteractionRequired':False,'pureSolverTime':False,'aiInferenceTimeIsolated':False}
    def file(b,case):return OUT/f'{b}-{case}-reacoes-N1-G2.dxf'
    comparisons={
        'withW20CADversusBIM':compare(file('CAD','W20'),file('BIM','W20')),
        'controlCADversusBIM':compare(file('CAD','controle'),file('BIM','controle')),
        'CADcontrolToW20':compare(file('CAD','controle'),file('CAD','W20')),
        'BIMcontrolToW20':compare(file('BIM','controle'),file('BIM','W20'))}
    if comparisons['withW20CADversusBIM']['changedLabelCount'] or comparisons['controlCADversusBIM']['changedLabelCount']:
        raise ValueError('Valores exibidos CAD/BIM divergentes')
    if comparisons['CADcontrolToW20']['labels'] != comparisons['BIMcontrolToW20']['labels']:
        raise ValueError('Incrementos gráficos divergentes')
    files=[{'path':str(file(b,c)),'sha256':sha(file(b,c))} for b in ['CAD','BIM'] for c in ['W20','controle']]
    result={'revision':'H03/R140','createdAtUtc':datetime.now(timezone.utc).isoformat(),
        'scope':'Reações gráficas das lajes N1 na ação Adicional G2; R137 com W20 e controle R138 de mesma malha',
        'protectedSourceFiles':protected,'sourceFilesUnchanged':True,'sessions':sessions,
        'exportedReactionDrawings':files,'comparisons':comparisons,
        'actionSelectionEvidence':'Seleção visual Adicional (G2) registrada nas quatro imagens; o DXF não contém metadado de ação',
        'observations':[
            'A troca de Fletores para Deslocamentos na grelha CAD retornou a seleção a G1; G2 foi selecionada novamente e conferida.',
            'Deslocamentos CAD/G2: legenda visual mínima -0.06 cm e máxima 0.00 cm; ação completa, não incremento exclusivo W20; sem avaliação ELS.',
            'Duplo clique em barra interna da grelha abriu Edição da barra (multiplicadores 1/1/1), cancelada sem edição; não abriu tabela de rotações.',
            'Botão Vista superior foi inicialmente confundido com tabela; apenas mudou a projeção.',
            'Quatro diagramas de Reações das lajes foram abertos pelo botão de setas opostas na janela Lajes.',
            'Os nomes das vigas diferem entre os receptores; a comparação usa coordenadas dos rótulos numéricos.',
            'Dois avisos de nome inválido na exportação CAD decorreram do caminho com barras mistas e foco não confirmado; corrigido por caminho Windows e campo conferido.',
            'No controle BIM, uma tentativa de exportação chegou ao aviso de salvar desenho; foi cancelada e a exportação repetida com sucesso.'
        ],
        'units':'Rótulos numéricos preservados sem atribuir unidade física ausente no DXF; coordenadas referem-se ao desenho, não à posição da reação física.',
        'springRotationsObtained':False,'springMomentsCalculated':False,'completeMomentBalanceClosed':False,
        'residualCauseProven':False,'processingPerformed':False,'SAP2000Executed':False,
        'W20AcceptedAsFinal':False,'finalStructuralApproval':False,'finalProductivityRankingAllowed':False,
        'monographEdited':False,'authorshipRVTorDWGEdited':False,
        'timingLimit':'Sessão CAD inclui descoberta do caminho, consulta de diagramas e diagnóstico de UI; demais sessões usam caminho aprendido. Sem comparação de produtividade ou soma a solver.',
        'primaryReference':'https://suporte.altoqi.com.br/hc/pt-br/articles/360038283234',
        'referenceApplicability':'O artigo descreve duplo clique para deslocamentos dos nós no pórtico, inclusive grelha de paredes. Não garante a mesma janela na grelha separada de lajes desta versão.',
        'nextStep':'Investigar rotações e reações nodais por recurso documentado; enquanto isso, manter a divergência de momentos aberta e avançar em tarefas independentes.'}
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'protected':len(protected),'queryPRJsUnchanged':len(sessions),
        'comparisons':{k:{f:v[f] for f in ['numericLabelCount','changedLabelCount','maxAbsDeltaDisplayed']} for k,v in comparisons.items()},
        'sessionMinutes':{k:v['durationMinutes'] for k,v in sessions.items()}}))

if __name__ == '__main__':
    main()

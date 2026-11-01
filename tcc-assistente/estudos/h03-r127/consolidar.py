"""Confere a seção W17 nos receptores, sem dimensionar ou aplicar cargas."""
import hashlib
import json
import re
from datetime import datetime,timezone
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Apoio-W17-H03-R127-CONSULTA-NAO-EXECUTAR')
PREP=HERE.parent/'h03-r126/R102-preparacao.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def parse(text,branch):
    project,name,floor=('40-H03-R126-CAD','V14','Croqui-N1') if branch=='CAD' else ('41-H03-R126-BIM','V2','Croqui-TCC-cdd31967-N1')
    if project not in text or floor not in text:raise ValueError('Projeto/pavimento incorreto')
    def field(label,ident,disabled=False):
        modifier='disabled, ' if disabled else ''
        values=set(re.findall(r'editar \('+modifier+r'settable, string\) '+re.escape(label)+r' Value: (\S+) ID: '+str(ident)+r'\b',text))
        if len(values)!=1:raise ValueError('Campo ausente/conflitante')
        return values.pop()
    if field('Nome',801)!=name:raise ValueError('Viga diferente')
    walls=set(re.findall(r'text ([\d.]+) kN/m ID: 508',text))
    if len(walls)!=1:raise ValueError('Carga de parede não identificada')
    return {'beam':name,'floor':'N1' if branch=='CAD' else 'TCC-cdd31967-N1',
            'bwCm':float(field('bw',810)),'hCm':float(field('h',811)),
            'elevationCm':float(field('/',507)),
            'extraSumDisplayedKNm':float(field('Carga extra',564,True)),
            'wallDisplayedKNm':float(walls.pop())}

def main():
    if (OUT/'R127-resultado.json').exists():raise FileExistsError('Resultado existente')
    prep=json.loads(PREP.read_text(encoding='utf-8'));protected=[];prjs=[]
    for row in prep['files']:
        after=sha(Path(row['source']))
        if after!=row['sha256Before']:raise ValueError('Fonte R116 alterada')
        protected.append({'path':row['source'],'sha256':after})
        if row['copy'].endswith('.prj'):
            after_copy=sha(Path(row['copy']))
            if after_copy!=row['sha256Before']:raise ValueError('PRJ consultado alterado')
            prjs.append({'path':row['copy'],'sha256':after_copy,'unchangedSincePreparation':True})
    readings={branch:parse((OUT/name).read_text(encoding='utf-8'),branch) for branch,name in [('CAD','CAD-W17-V14-secao-UI.txt'),('BIM','BIM-W17-V2-secao-UI.txt')]}
    keys=['bwCm','hCm','elevationCm','extraSumDisplayedKNm','wallDisplayedKNm']
    equal={key:readings['CAD'][key]==readings['BIM'][key] for key in keys}
    if not all(equal.values()):raise ValueError('Leitura pareada diverge; revisar antes de consolidar')
    if [readings['CAD'][k] for k in keys]!=[20,16,0,0,0]:raise ValueError('Valores distintos da evidência inspecionada')
    result={'revision':'H03/R127','createdAtUtc':datetime.now(timezone.utc).isoformat(),
      'scope':'Consulta do apoio W17 nas cópias40CAD/41BIM preparadas R126 e derivadas R116; sem editar, salvar ou processar.',
      'readings':readings,'pairedDisplayedComparisons':equal,
      'editingCheckboxVisualTranscription':{'label':'Manter seção constante na viga','CAD':True,'BIM':False,
        'numericOrStructuralDifferenceInThisReadbackProved':False,'method':'Inspeção visual das imagens; estado não exposto na árvore UIA.'},
      'wallReference':{'revision':'R120','freeWallSegmentXYM':[[5.45,3.9],[6.4,3.9]],'freeWallLengthM':0.95,
        'conditionalLineMagnitudeKNm':4.4446,'conditionalForceMagnitudeKN':4.22237,
        'applied':False,'geometryCurrentExportPerformed':False},
      'protectedR116Files':protected,'copyPrjs':prjs,'sourcesUnchanged':True,
      'times':{b:json.loads((OUT/f'{b}-consulta-tempo.json').read_text(encoding='utf-8')) for b in ['CAD','BIM']},
      'loadsEdited':False,'geometryEdited':False,'processingPerformed':False,'dimensioningPerformed':False,
      'monographEdited':False,'structuralSectionApproved':False,'finalProductivityRankingAllowed':False,
      'limits':['Seção20x16cm confirmada nativamente nos dois ramos, sem comprovar capacidade resistente ou atendimento de flecha/fissuração.',
        'Carga de parede e soma extra exibidas zero não substituem auditoria de todas as ações/reação de lajes.',
        'Não se conclui perda na transferência porque a seção coincide com a referência prévia e entre os dois ramos.',
        'Checkbox de constância de seção diverge visualmente; não foi alterado, nem classificado como defeito ou diferença de resistência.',
        'Tempos incluem abertura, seleção/evidências e fechamento; CAD teve seleção entre poligonais, BIM abriu diretamente, sem desenho experimental de produtividade.']}
    (OUT/'R127-resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'pairedScalarsEqual':len(equal),'sectionCm':[20,16],'protectedSourceFiles':len(protected),'copyPrjsUnchanged':len(prjs)}))

if __name__=='__main__':main()

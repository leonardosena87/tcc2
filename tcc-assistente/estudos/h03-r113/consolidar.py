"""Confronta cotas consultadas e leitura grafica sem ajustar automaticamente modelos."""
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('D:/TCC/outputs')
OUT = ROOT/'Altimetria-H03-R113-CONSULTA-NAO-EXECUTAR'


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def floor(text):
    result = {}
    for label, key in [('Nome','name'),('Altura','heightCm'),('Nível','levelCm')]:
        values=set(re.findall(r'editar \((?:disabled, )?settable, string\) '+label+r' Value: (\S+) ID:',text))
        if len(values)!=1: raise ValueError('Campo de pavimento ausente ou ambiguo')
        value=values.pop(); result[key]=value if key=='name' else float(value)
    return result


def architectural_level(y, anchor_y, anchor_z, pdf_per_m):
    if pdf_per_m<=0: raise ValueError('Escala invalida')
    return anchor_z+(anchor_y-y)/pdf_per_m


def main():
    if (OUT/'R113-resultado.json').exists(): raise FileExistsError('Nao sobrescrever resultado')
    prep=json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected=[{**r,'afterSha256':sha(Path(r['source']))} for r in prep['files']]
    if any(r['afterSha256']!=r['sha256Before'] for r in protected): raise ValueError('Fonte R111 alterada')
    branches={}
    for b in ['CAD','BIM']:
        readings={n:floor((OUT/f'{b}-{n}-pavimento-UI.txt').read_text(encoding='utf-8')) for n in ['N0','N1','N2']}
        for n, r in readings.items():
            if r['name'] != (n if b=='CAD' else 'TCC-cdd31967-'+n): raise ValueError('Pavimento incorreto')
        rows=[r for r in prep['files'] if r['branch']==b]
        changes=[]
        for r in rows:
            p=Path(r['copy']);current=sha(p)
            if p.suffix=='.prj' and current!=r['sha256Before']: raise ValueError('PRJ consultado alterado')
            if current!=r['sha256Before']: changes.append({'path':str(p),'preparationSha256':r['sha256Before'],'afterSha256':current,
                                                          'iniOwnPathChangedDuringPreparation':p.name=='EdificacaoEberick.ini'})
        branches[b]={'floors':readings,'prjUnchanged':True,'copyAuxiliaryDifferencesFromSource':changes,
                     'sessionTime':json.loads((OUT/f'{b}-sessao-tempo.json').read_text(encoding='utf-8'))}
    r112path=ROOT/'Reservatorio-H03-R112-ENVELOPE-NAO-EXECUTAR/R112-envelope-reservatorio.json'
    r112=json.loads(r112path.read_text(encoding='utf-8'))
    arch=Path(r112['architecture']['path'])
    if sha(arch)!=r112['architecture']['sha256']: raise ValueError('Arquitetura mudou')
    sys.path.insert(0,'D:/TCC/work/pdf-deps');import pymupdf as fitz
    page=fitz.open(arch)[0]
    # Ponta do marcador de nivel3,25 no quarto do corte BB, nao topo do texto.
    marker_y=2018.0; marker_x=1092.239990234375
    matches=[]
    for d in page.get_drawings():
        for item in d['items']:
            if item[0]=='l':
                a,b=item[1:]
                if any(abs(p.x-marker_x)<.001 and abs(p.y-marker_y)<.001 and abs(q.y-2014.8800048828125)<.001
                       for p,q in [(a,b),(b,a)]): matches.append(item)
    if len(matches)!=2: raise ValueError('Marcador de nivel do corte nao identificado')
    scale=r112['measurement']['pdfUnitsPerMvertical']
    ys={'floorFinished':marker_y,'upperCeiling':1859.3599853515625,
        'mainRoofDeckTopDrawn':1850.47998046875,'raisedTankBase':1816.4000244140625,
        'raisedParapetTop':1742.719970703125}
    levels={k:architectural_level(y,marker_y,3.25,scale) for k,y in ys.items()}
    if abs((levels['upperCeiling']-3.25)-2.80)>.005: raise ValueError('Controle forro2,80 divergente')
    if abs((levels['raisedTankBase']-levels['mainRoofDeckTopDrawn'])-.60)>.005: raise ValueError('Controle ressalto0,60 divergente')
    paired=[{'floor':n,'field':k,'CAD':branches['CAD']['floors'][n][k],'BIM':branches['BIM']['floors'][n][k],
             'equal':branches['CAD']['floors'][n][k]==branches['BIM']['floors'][n][k]}
            for n in ['N0','N1','N2'] for k in ['heightCm','levelCm']]
    n2=branches['CAD']['floors']['N2']['levelCm']/100
    result={'revision':'H03/R113','createdAtUtc':datetime.now(timezone.utc).isoformat(),'branches':branches,
            'pairedFields':paired,'protectedSourceR111Files':protected,'sourceR111FilesUnchanged':True,
            'architectureSource':{'path':str(arch),'sha256':sha(arch),'section':'BB'},
            'architecturalGraphicRegistration':{'anchorMarkerPdf':[marker_x,marker_y],'anchorFinishedLevelM':3.25,
                'ordinatesPdf':ys,'scalePdfUnitsPerM':scale,'derivedLevelsM':levels,
                'derivedRaisedTankBaseAboveNativeN2M':levels['raisedTankBase']-n2,
                'nativeN2Plus060ExcessOverDrawnBaseM':n2+.60-levels['raisedTankBase'],
                'datumRegistrationIsPreliminaryNotExecutiveSurvey':True},
            'nativeFloorHeightSumCm':sum(r['heightCm'] for r in branches['CAD']['floors'].values()),
            'nativeFloorLevelN2Cm':639,'heightSumAndAbsoluteLevelAreDistinct':True,
            'nativeEdited':False,'processingPerformed':False,'architecturalHeightsChanged':False,
            'tankBaseModelCreated':False,'finalStructuralApproval':False,
            'limits':['Cotas arquitetonicas graficas aproximadas, ancoradas no marcador3,25 e controladas por2,80/0,60.',
                      'Base candidata cerca de+6,81m, nao uma nova cota executiva adotada.',
                      'Nao usar N2+0,60: diferenca para base grafica e cerca de18cm.',
                      'Altura acumulada7,19m nao e nivel absoluto6,39m; origem da altura de vento requer leitura propria.',
                      'Sem concepcao/dimensionamento dos apoios, base ou acesso do reservatorio.']}
    (OUT/'R113-resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'pairedFields':len(paired),'equal':sum(r['equal'] for r in paired),'graphicLevelsM':levels,
                      'baseAboveN2M':levels['raisedTankBase']-n2,'protectedFiles':len(protected)}))


if __name__=='__main__':main()

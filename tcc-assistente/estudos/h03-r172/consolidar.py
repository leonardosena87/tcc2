"""Consolida diagnóstico parcial real; ausência de QT não vira zero."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,re,shutil,zipfile

OUT=Path('D:/TCC/outputs/Analise-H03-R172-DIAGNOSTICO-PARCIAL-NAO-EXECUTAR')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def extract(text,branch):
    if f'R172-{branch}-DIAGNOSTICO-PARCIAL-NAO-EXECUTAR' not in text:raise ValueError('Projeto incorreto')
    rows=set(re.findall(r'editar Value: (Cargas verticais:[^\n]+)',text))
    if len(rows)!=1:raise ValueError('Resumo ausente ou contraditorio')
    raw=rows.pop()
    loads={}
    for label in ('Peso próprio','Adicional','Acidental','Q_TELHADO_MANUTENCAO','Total'):
        values=re.findall(re.escape(label)+r' = ([0-9]+\.[0-9]+) tf',raw)
        if label=='Q_TELHADO_MANUTENCAO' and not values:loads[label]=None;continue
        if len(values)!=1:raise ValueError('Parcela ausente ou duplicada: '+label)
        loads[label]=float(values[0])
    fields={}
    for label,stop,unit in [('horizontal','Deslocamento relativo máximo','cm'),('gamma','Análise de 2ª ordem:',None)]:
        start='Deslocamento horizontal máximo do centro de massa (Vento):' if label=='horizontal' else 'Verificação de estabilidade (Gama-Z):'
        section=raw.split(start,1)[1].split(stop,1)[0]
        pattern=r'([XY][+-]) = ([0-9]+\.[0-9]+)'+(' cm' if unit else '')+r' \(limite ([0-9]+\.[0-9]+)\)'
        parsed=re.findall(pattern,section)
        if len(parsed)!=4 or len({r[0] for r in parsed})!=4:raise ValueError('Direcoes ausentes ou duplicadas')
        fields[label]={d:dict(value=float(v),displayedLimit=float(limit),unit=unit) for d,v,limit in parsed}
    relative=re.search(r'Deslocamento relativo máximo do centro de massa \(Vento\): (.+?) - ([XY][+-]) = ([0-9.]+) cm \(limite ([0-9.]+)\)',raw)
    if not relative:raise ValueError('Relativo ausente')
    return dict(raw=raw,verticalLoadsDisplayedTf=loads,horizontalDisplayedCm=fields['horizontal'],gammaZDisplayed=fields['gamma'],
        relativeDisplayed=dict(floor=relative[1],direction=relative[2],valueCm=float(relative[3]),displayedLimitCm=float(relative[4])),
        containsUnusualLoadAreaWarning='Relação de carga por área não usual' in raw)

def main():
    prep=read(OUT/'R172-preparacao-copias.json');branches={}
    protected=[]
    for branch,source in prep['branches'].items():
        root=Path(source['sourceRoot']);target=Path(source['targetRoot'])
        for e in source['sourceFiles']:
            assert sha(root/e['relativePath'])==e['sha256'];protected.append(dict(branch=branch,source=str(root/e['relativePath']),sha256=e['sha256']))
        text=(OUT/f'{branch}-resumo-analise.txt').read_text(encoding='utf-8');summary=extract(text,branch)
        session=read(OUT/f'{branch}-sessao-tempo.json')
        assert session['elapsedMs']==session['end']['ms']-session['start']['ms']>0
        attempts=[OUT/f'{branch}-processamento-tempo.json']
        if branch=='CAD':attempts.append(OUT/'CAD-reprocessamento-tempo.json')
        durations=[]
        for p in attempts:
            entry=read(p);end=entry.get('observation',entry.get('observationRecorded'))
            assert session['start']['ms']<=entry['start']['ms']<end['ms']<=session['end']['ms']
            durations.append(entry)
        prjs=list(target.rglob('*.prj'));assert len(prjs)==1
        with zipfile.ZipFile(prjs[0]) as z:assert z.testzip() is None
        frozen=OUT/'congelados-apos-processamento'/branch;assert not frozen.exists()
        frozen_entries=[]
        for src in sorted(target.rglob('*')):
            if not src.is_file() or src.suffix.lower() in ('.log','.errlog'):continue
            rel=src.relative_to(target);dst=frozen/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);assert sha(src)==sha(dst)
            frozen_entries.append(dict(relativePath=str(rel),sha256=sha(src),bytes=src.stat().st_size))
        branches[branch]=dict(projectPath=str(prjs[0]),projectSha256=sha(prjs[0]),summary=summary,sessionTime=session,
            processingObservations=durations,frozenRoot=str(frozen),frozenFiles=frozen_entries,
            summaryEvidenceSha256=sha(OUT/f'{branch}-resumo-analise.txt'))
    cad,bim=(branches[b]['summary'] for b in ('CAD','BIM'))
    result=dict(revision='H03/R172',recordedAtUtc=datetime.now(timezone.utc).isoformat(),branches=branches,protectedSourceFiles=protected,
        displayedTotalDifferenceCadMinusBimTf=round(cad['verticalLoadsDisplayedTf']['Total']-bim['verticalLoadsDisplayedTf']['Total'],2),
        displayedAdditionalDifferenceCadMinusBimTf=round(cad['verticalLoadsDisplayedTf']['Adicional']-bim['verticalLoadsDisplayedTf']['Adicional'],2),
        bimRoofMaintenanceParcelMissingInDisplayedSummary=bim['verticalLoadsDisplayedTf']['Q_TELHADO_MANUTENCAO'] is None,
        missingParcelImputedAsZero=False,staticAnalysisPerformed=True,porticoDeflectionsWithConfiguredStiffnessPerformed=True,
        dimensioningPerformed=False,slabDeflectionsPerformed=False,crackedStiffnessCalculated=False,dynamicAnalysisPerformed=False,
        sourceFilesUnchanged=True,allLoadsAndBoundaryConditionsEqual=False,analyticalModelEquivalenceVerified=False,
        fullPairedFlowTimesMeasured=False,pureSolverBenchmark=False,finalRankingAllowed=False,finalStructuralApproval=False,
        cadFirstReportAttemptHadDirectoryError=True,cadSecondProcessingPerformedAfterSaveAs=True,
        pendingAnalyticalLandingBeamIssue='BIM V16/V6 esta em N1 com elevacao -142.6 cm, campo que o manual informa nao afetar a montagem do portico; corrigir em nivel intermediario e conferir modelo analitico.',
        deflectionDifferenceAttributedSolelyToThatIssue=False)
    (OUT/'R172-resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(deltaTotalTf=result['displayedTotalDifferenceCadMinusBimTf'],deltaAdditionalTf=result['displayedAdditionalDifferenceCadMinusBimTf'],
        loads={b:r['summary']['verticalLoadsDisplayedTf'] for b,r in branches.items()},sessionMs={b:r['sessionTime']['elapsedMs'] for b,r in branches.items()},sourceFilesPreserved=len(protected))))

if __name__=='__main__':main()

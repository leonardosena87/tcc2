"""Consolida evidencias selecionadas da R178; preserva fontes e historico."""
from pathlib import Path
import json, shutil
from auditar_contorno import OUT, HERE
from auditar_escada import sha


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    result_path = OUT/'R178-comparacao-CAD-BIM.json'
    data = json.loads(result_path.read_text(encoding='utf-8'))
    if not all(data['physicalTriangulatedMeshesEqualAt1eMinus7M'].values()):
        raise ValueError('Malha fisica divergente')
    timings = dict(revision='H03/R178', source='Relatorios nativos e registros UTC de observacao',
        nativePartialProcessingSeconds={'CAD':5, 'BIM':6},
        nativeProcessingSingleObservationEach=True, fullFlowMeasured=False,
        intervalsComparableAsProductivity=False, includeInFinalFlowTotals=False,
        reasons=['CAD inicia depois da exclusao do patamar',
                 'BIM inclui exclusao e pausa entre retomadas',
                 'BIM sucede o aprendizado do procedimento CAD'])
    for branch in ('CAD','BIM'):
        native = data['branches'][branch]['nativePartialAnalysisTime']
        if native != f'00:00:0{timings["nativePartialProcessingSeconds"][branch]}':
            raise ValueError('Tempo nativo inesperado')
        timings[branch] = dict(
            start=json.loads((OUT/f'{branch}-correcao-inicio.json').read_text(encoding='utf-8')),
            firstSave=json.loads((OUT/f'{branch}-correcao-primeiro-save.json').read_text(encoding='utf-8')),
            observedIntervalSeconds=data['branches'][branch]['observedCorrectionIntervalSeconds'])
    write(OUT/'R178-tempos.json',timings)
    shutil.copy2(HERE/'LEIA-ME-R178.md',OUT/'LEIA-ME-R178.md')

    pointer = Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    backup = OUT/'R178-ponteiro-anterior.json'
    if not backup.exists():
        shutil.copy2(pointer,backup)
    current = json.loads(pointer.read_text(encoding='utf-8-sig'))
    proof = dict(Path=str(result_path),Sha256=sha(result_path))
    for prefix in ('latestExperimentalStairIntegration','latestCorrectedReceiverComparison'):
        current[prefix+'Revision']='H03/R178'
        current[prefix+'Path']=proof['Path']
        current[prefix+'Sha256']=proof['Sha256']
    current['latestEberickCadWorkingCopyPath']=data['branches']['CAD']['projectPath']
    bim=data['branches']['BIM']
    current['latestBimWorkingCopyRoot']=str(Path(bim['projectPath']).parent.parent)
    for key in ('latestBimWorkingProject','latestBimReceiverWorkingCopyPath'):
        current[key]=bim['projectPath']
    current['latestBimWorkingRevision']='H03/R178 - correcao lateral experimental do patamar'
    current['latestPartialAnalysisRevision']='H03/R178 - CAD e BIM; analise parcial experimental'
    current['latestPartialAnalysisResultPath']=proof['Path']
    current['latestPartialAnalysisResultSha256']=proof['Sha256']
    current['latestPartialAnalysisProjectPaths']={b:r['projectPath'] for b,r in data['branches'].items()}
    current['experimentalStairLandingWidthReconciledBothBranches']=True
    current['experimentalStairLandingContourNeedsReconciliation']=True
    current['experimentalStairPhysicalFivePieceMeshesEqual']=True
    current['experimentalStairUniformityStrictAuditPassed']=False
    current['fullPairedFlowComparisonFinished']=False
    current['fullAnalyticalEquivalenceVerified']=False
    current['analyticalModelEquivalenceVerified']=False
    current['currentCorrectedReceiverLoadsEqual']=False
    write(pointer,current)
    shutil.copy2(pointer,OUT/'R178-ponteiro-atualizado.json')

    selected=['R178-preparacao.json','R178-comparacao-CAD-BIM.json','R178-tempos.json',
              'R178-ponteiro-atualizado.json','R178-contorno-patamar.png']
    for branch in ('CAD','BIM'):
        selected += [f'{branch}-{suffix}' for suffix in ('correcao-inicio.json',
            'correcao-primeiro-save.json','mensagens-analise.txt','resultados-analise.txt',
            'patamar-parametros-relancamento.txt')]
        destination=HERE/f'{branch}-IFC'
        destination.mkdir(exist_ok=True)
        shutil.copy2(data['branches'][branch]['ifcPath'],destination)
        destination=HERE/f'{branch}-SAP'
        destination.mkdir(exist_ok=True)
        for path in (OUT/f'{branch}-SAP').glob('*.$2k'):
            shutil.copy2(path,destination)
    for name in selected:
        shutil.copy2(OUT/name,HERE/name)
    files=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts
           and p.name!='R178-manifesto.json']
    write(HERE/'R178-manifesto.json',dict(revision='H03/R178',files=[dict(
        relativePath=p.relative_to(HERE).as_posix(),bytes=p.stat().st_size,sha256=sha(p))
        for p in sorted(files)]))
    shutil.copy2(HERE/'R178-manifesto.json',OUT/'R178-manifesto.json')
    print(json.dumps(dict(files=len(files),resultSha256=proof['Sha256'],
                         totalBytes=sum(p.stat().st_size for p in files)),indent=2))


if __name__=='__main__':
    main()

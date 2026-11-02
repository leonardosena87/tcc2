"""Documenta correção nativa localizada; não calcula nem aprova a estrutura."""
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'h03-r167'))
from auditar_lajes import read, sha, ifcopenshell, cloud, properties
import ifcopenshell.geom

OUT=Path('D:/TCC/outputs/Intercambio-H03-R169-VINCULO-VARANDA-NAO-EXECUTAR')
ROOT=Path('D:/TCC/outputs/R169-BIM-VINCULO-VARANDA-NAO-EXECUTAR')
PRJ=ROOT/'Projeto Eberick/R166-R160-3NIVEIS-CONFIG-CAD-NAO-EXECUTAR.prj'
IFC=ROOT/'Arquivos do projeto/Modelo 3D.IFC'

def main():
    prep=read(OUT/'R169-preparacao-copia.json')
    source=Path(prep['sourceRoot'])
    preserved={e['relativePath']:sha(source/e['relativePath'])==e['sha256'] for e in prep['sourceFiles']}
    assert all(preserved.values())
    before=source/'Arquivos do projeto/Modelo 3D.IFC'
    hashes={str(p):sha(p) for p in (PRJ,IFC,before)}
    assert hashes[str(PRJ)]=='112485c07b92c6448e896ab9463e4e9063f1da03f1e1d01105f7d5ac8bbdadfe'
    diagnostic=(OUT/'R169-reabertura-verificacao.txt').read_text(encoding='utf-8')
    assert 'Não foram detectados problemas no lançamento deste pavimento.' in diagnostic
    models=[ifcopenshell.open(str(p)) for p in (before,IFC)]
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    comparison={}
    for cls in ('IfcBeam','IfcColumn','IfcSlab'):
        def signatures(model):
            return Counter((o.Name,cloud(o,settings)['pointsSha256'],
                json.dumps(properties(o),sort_keys=True,ensure_ascii=False)) for o in model.by_type(cls))
        comparison[cls]=dict(beforeCount=len(models[0].by_type(cls)),afterCount=len(models[1].by_type(cls)),
            exportedGeometryAndPropertySetsUnchanged=signatures(models[0])==signatures(models[1]))
    assert all(r['exportedGeometryAndPropertySetsUnchanged'] for r in comparison.values())
    assert hashes=={str(p):sha(p) for p in (PRJ,IFC,before)}
    result=dict(revision='H03/R169',recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        sourceFilesPreserved=preserved,sourceHashes=hashes,nativeProject=str(PRJ),
        nativeCommand='Modelo > Lajes > Engastar',
        scope='Continuidade entre L4 e L6 pela borda comum V12, pavimento N1; nao comando Engastar em viga.',
        previousDiagnostic='L10: Laje L6 em balanco nao engastada',
        diagnosticAfterSaveAndReopen='Nao foram detectados problemas no lancamento deste pavimento.',
        nativeProjectClosedAndReopened=True,nativeDiagnosticPassedForN1=True,
        exportedComparison=comparison,ifcDoesNotEvidenceThisNativeBoundaryChange=True,
        allBoundaryConditionsComparedToCad=False,restraintDesignApproved=False,
        newStructuralCalculationPerformed=False,structuralApproval=False,
        stairMissingInCalculationModel=True,fullPairedComparisonFinished=False,
        partialCorrectionElapsedMs=read(OUT/'R169-correcao-observacao.json')['elapsedMs'],fullFlowTime=False)
    (OUT/'R169-vinculo-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('sourceHashes','sourceFilesPreserved')},ensure_ascii=False))

if __name__=='__main__':main()

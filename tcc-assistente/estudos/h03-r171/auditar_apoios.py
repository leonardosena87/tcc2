"""Relê apoios idealizados e geometria; não dimensiona fundações."""
from collections import Counter
from datetime import datetime,timezone
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'h03-r167'))
from auditar_lajes import read,sha,ifcopenshell,cloud,properties
import ifcopenshell.geom

OUT=Path('D:/TCC/outputs/Intercambio-H03-R171-APOIOS-NAO-EXECUTAR')
ROOT=Path('D:/TCC/outputs/R171-BIM-APOIOS-IDEALIZADOS-NAO-EXECUTAR')
PRJ=ROOT/'Projeto Eberick/R166-R160-3NIVEIS-CONFIG-CAD-NAO-EXECUTAR.prj'
IFC=ROOT/'Arquivos do projeto/Modelo 3D.IFC'

def main():
    prep=read(OUT/'R171-preparacao-copia.json');source=Path(prep['sourceRoot'])
    assert all(sha(source/e['relativePath'])==e['sha256'] for e in prep['sourceFiles'])
    assert sha(PRJ)=='f23410596511c1d301e71567015628faf8a45bfa5a143202a2e8ebfeb8346fb3'
    supports=[]
    for i in range(1,12):
        file=OUT/f'R171-reabertura-P{i}.txt';ax=file.read_text(encoding='utf-8')
        assert f'Nome Value: P{i} ID:' in ax and 'diálogo Pilar de fundação' in ax
        for value in ('Vínculo apoio Value: Rotulado','Vínculo pilar Value: Engastado','Altura barra Value: Fixo','Value: 10 ID: 803','Profundidade (df) Value: 0'):
            assert value in ax,(i,value)
        supports.append(dict(name=f'P{i}',support='Rotulado',columnConnection='Engastado',fixedBarHeightCm=10,dfCm=0,evidence=file.name,sha256=sha(file)))
    floors={}
    for floor in ('N0','N1','N2'):
        file=OUT/f'R171-reabertura-{floor}-verificacao.txt';ax=file.read_text(encoding='utf-8')
        assert f'Croqui-TCC-7a6267fd-{floor}' in ax and 'Não foram detectados problemas no lançamento deste pavimento.' in ax
        floors[floor]=dict(noProblemsDetectedByLaunchCheck=True,evidence=file.name,sha256=sha(file))
    paths=[source/'Arquivos do projeto/Modelo 3D.IFC',IFC,PRJ];hashes={str(p):sha(p) for p in paths}
    models=[ifcopenshell.open(str(p)) for p in paths[:2]]
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    compare={}
    for cls in ('IfcBeam','IfcColumn','IfcSlab'):
        def signatures(m):return Counter((o.Name,cloud(o,settings)['pointsSha256'],json.dumps(properties(o),sort_keys=True,ensure_ascii=False)) for o in m.by_type(cls))
        compare[cls]=dict(previousCount=len(models[0].by_type(cls)),newCount=len(models[1].by_type(cls)),exportedGeometryAndPropertiesUnchanged=signatures(models[0])==signatures(models[1]))
    assert all(row['exportedGeometryAndPropertiesUnchanged'] for row in compare.values())
    assert len(models[1].by_type('IfcFooting'))==11
    assert hashes=={str(p):sha(p) for p in paths}
    result=dict(revision='H03/R171',recordedAtUtc=datetime.now(timezone.utc).isoformat(),sourceHashes=hashes,
        sourceR169FilesPreserved=True,nativeProject=str(PRJ),nativeProjectSavedClosedAndReopened=True,
        supportsConfirmedAfterReopen=supports,launchCheckAfterReopen=floors,superstructureIfcComparison=compare,
        nativeFootingPlaceholders=11,foundationTypeIsOnlySupportRepresentation=True,
        soilBearingCapacityAssessed=False,foundationDesignInScope=False,foundationDesignPerformed=False,
        supportIdealizationMatchesCadFieldsObservedInR170=True,supportIdealizationIsGeotechnicallyApproved=False,
        newPhysicalColumnPositionsAdded=False,newStructuralCalculationPerformed=False,structuralApproval=False,
        fullLoadsAndInternalRestraintsParityVerified=False,stairStillMissingInCalculationModel=True,
        partialCorrectionElapsedMs=read(OUT/'R171-correcao-tempo.json')['elapsedMs'],fullFlowTime=False)
    (OUT/'R171-apoios-auditoria.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('sourceHashes','supportsConfirmedAfterReopen','launchCheckAfterReopen')},ensure_ascii=False))

if __name__=='__main__':main()

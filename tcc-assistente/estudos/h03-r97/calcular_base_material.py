"""Base numerica especifica C25/CA50/parede15cm; nao altera modelos nativos."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--norms',type=Path,required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise ValueError('Saida precisa ser nova')
    standards = []
    expected = [('ABNT NBR 6118-2026.pdf','3fb0ef6a7600593e3f0c1991f73ecffe08da7cb7543b5ac80290dd7dfd7b791e',[42,44,45,48]),
                ('ABNT NBR 6120-2019.pdf','807c22009de912321bf743704cc4b5ad454ef0a68721b50f8d34bf2182f567b7',[15,17])]
    for name,expected_hash,pages in expected:
        source=args.norms/name
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        if digest!=expected_hash:
            raise ValueError('Exemplar normativo difere do inspecionado visualmente')
        standards.append(dict(path=str(source),sha256=digest,pdfPagesVisuallyRead=pages))
    fck=25.0
    alpha_e=1.0
    alpha_i=min(.8+.2*fck/80,1.0)
    eci=alpha_e*5600*math.sqrt(fck)
    ecs=alpha_i*eci
    fctm=.3*fck**(2/3)
    wall=.9+2*.0175*19
    result=dict(revision='H03/R97',atUtc=datetime.now(timezone.utc).isoformat(),
        purpose='Valores de referencia para alinhamento comum; nao cadastro aplicado ou ensaio de material.',
        sources=standards,currentCatalogStatusVerified=False,catalogLookupResult='Links do catalogo retornaram LINK EXPIRED.',
        concrete=dict(className='C25',fckMPa=fck,gammaCNormalInformed=1.4,fcdNormalMPa=fck/1.4,
            aggregateHypothesis='granito/gnaisse, alphaE=1; nao caracterizacao de material real',
            alphaE=alpha_e,alphaI=alpha_i,EciMPa=eci,EcsMPa=ecs,
            EciFormula='alphaE*5600*sqrt(fck)',alphaIFormula='min(0.8+0.2*fck/80,1)',
            userEcsGPaInformed=24.1,userAlphaInformed=.86,EcsFromRoundedAlphaMPa=.86*eci,
            differenceToUserEcsMPa=ecs-24100,
            fctmMPa=fctm,fctkInfMPa=.7*fctm,fctkSupMPa=1.3*fctm,
            poissonLinearReference=.2,poissonCondition='Compressao<0.5fc e tracao<fct; item8.2.9.',
            GcLinearReferenceMPa=ecs/2.4,massDensityRCReferenceKgM3=2500,
            unitWeightRCReferenceKNM3=25,
            densityAndUnitWeightMeaning='Valores nominais de referencias distintas; nao conversao exata por g=9.80665.',
            revitYoungMappingApplied=False,revitYoungMappingMeaning='Definir explicitamente Eci/Ecs e papel do ativo antes de editar.',
            referenceItems=['6118:2026,8.2.2','6118:2026,8.2.5','6118:2026,8.2.8','6118:2026,8.2.9']),
        steel=dict(className='CA-50',fykMPa=500,gammaSNormalInformed=1.15,fydNormalMPa=500/1.15,
                   EsMPa=210000,yieldStrainDesign=(500/1.15)/210000,massDensityKgM3=7850,
                   referenceItems=['6118:2026,8.3.3','6118:2026,8.3.5'],completeNativeRegisterVerified=False),
        wall=dict(finishedThicknessM=.15,finishedThicknessConfirmedByUser=True,
            body='Bloco ceramico de vedacao com furos horizontais',bodyThicknessM=.115,
            finishThicknessEachFaceM=.0175,uncoatedWallKNM2=.9,finishUnitWeightKNM3=19,
            areaWeightKNM2=wall,calculation='.9+2*.0175*19',
            adoptedAsStudyHypothesis=True,compositionConfirmedByUser=False,manufacturerVerified=False,
            reference='6120:2019,Tabela2,pagina impressa11/PDF17,composicao explicita sem interpolar valores arredondados.',
            includesMortarBedding=True,includesFinishesOnConcrete=False,includesLintelsJoinery=False,
            readyForNativeWallLoads=False),
        nativeModelsChanged=False,loadsApplied=False,structuralComplianceAttested=False,
        limits=['Hipoteses academicas comuns aos dois fluxos; nao medições ou laudos.',
                'Parametros isolados nao verificam carregamentos, rigidez, detalhamento ou ELU/ELS.',
                'Geometria, aberturas e caminhos de carga das paredes continuam pendentes.',
                '24.1GPa deriva da premissa arredondada; 24.15GPa usa alphaI=.8625, sem alterar silenciosamente o valor informado.'])
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x',encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
        f.write('\n')
    print(json.dumps(dict(EciMPa=eci,EcsMPa=ecs,wallAreaWeightKNM2=wall,nativeModelsChanged=False)))


if __name__=='__main__':
    main()

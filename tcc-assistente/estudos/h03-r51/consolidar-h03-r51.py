"""Registra observacoes na interface nativa; nao deduz parametros pelo nome do IFC."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
root=Path('D:/TCC');out=root/'outputs/Conferencia-H03-R51-PARAMETROS-NAO-EXECUTAR'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,r:p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
observed=dict(application='Projeto inteiro',concreteClass='C-25',fckMpa=25,gammaC=1.4,fcdMpaDisplayed=17.86,
    EciMpaDisplayed=28000,EcsMpaDisplayed=24150,fctmMpaDisplayed=2.56,fctkInfMpaDisplayed=1.8,
    fctkSupMpaDisplayed=3.33,fctdMpaDisplayed=1.28,unitWeightKnM3=25,aggregateType='granito',
    environmentalClass='II (moderada)',aggregateDimensionMm=25,slumpNominalCm=10,cementFamily='CP-II',
    nominalCoverCm=dict(beamExternal=3,beamInternal=3,columnExternal=3,columnInternal=3,slab=2.5),
    steelClassesInObservedActiveRows=['CA50'],observedActiveDiametersCommonMm=[6.3,8,10,12.5,16],ca60Diameter5Active=False,
    displayedCrackWidthsMm=dict(soil=.2,water=.1,other=.3),crackCombination='Frequentes')
changes=[dict(field='aggregateDimensionMm',before=19,after=25),
    dict(field='C25.slumpNominalCm',before=5,after=10),dict(field='C25.cementFamily',before='CP-IV',after='CP-II'),
    dict(field='CA60.5mm.active',before=True,after=False)]
states=[]
for branch in ('BIM','CAD'):
    native=root/f'outputs/H03_{branch}_R51_PARAMETROS_NAO_EXECUTAR'
    preparation=json.loads((out/f'R51-preparacao-{branch}.json').read_text(encoding='utf-8-sig'))
    frozen=[]
    for folder in ('Projeto Eberick','_DADOS_'):
        for p in (native/folder).rglob('*'):
            if not p.is_file() or p.suffix.lower() in ('.bak','.lck','.tmp','.errlog'):continue
            dest=out/f'congelado-{branch}'/p.relative_to(native);dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.exists():assert sha(dest)==sha(p),str(dest)
            else:shutil.copy2(p,dest)
            frozen.append(dict(path=str(p),frozen=str(dest),sha256=sha(p)))
    state=dict(branch=branch,revision='H03/R51',atUtc=datetime.now(timezone.utc).isoformat(),nativeProject=preparation['nativeProject'],
        evidenceMethod='Leitura visual na interface Materiais e durabilidade, Classes e Barras do Eberick; salvar, fechar, reabrir e ler novamente.',
        screenshotFilesSaved=False,observedAfterReopen=observed,changes=changes,classification='Adequacao de parametros no receptor; nao atribuida a erro de transferencia sem evidencia.',
        changedFieldCount=4,parameterPersistenceChecked=True,geometryReexportedThisRevision=False,structuralCalculationPerformed=False,
        balconySupportVerified=False,frozenFiles=frozen,
        limits=['C25 e cobrimentos 2.5/3 cm foram observados, nao constituem certificacao normativa.',
            'Nao se comprova origem por IFC/DWG de valores globais; ha valores do receptor nos dois ramos.',
            'Agregado granito mantido conforme cadastro e modulos ja adotados; origem/material real nao ensaiado.',
            'Programa oferece CP-II sem subtipo E; especificacao CP-II-E permanece documentada fora deste campo.',
            'Abatimento 10 e nominal; tolerancia +/-2 nao possui campo separado observado. Escada com 6+/-2 pendente de modelagem/classe propria.',
            'Fundacoes e parametros de contato com solo nao alterados; escopo limitado a superestrutura.',
            'Aco CA50 identificado no cadastro; propriedades mecanicas completas e selecoes particulares ainda exigem conferencia.',
            'Custos e carbono padrao nao foram conferidos; nao utilizar como resultado economico/ambiental.',
            'Geometria R49/R50 foi auditada antes; R51 ainda nao reexportada apos alterar parametros.'])
    if branch=='BIM':state['bitolaSelectionsObserved']=dict(beamLongitudinal=[8,10,12.5,16,20],beamTransverse=[6.3,8,10],columnLongitudinal=[10,12.5,16,20],columnTransverse=[6.3,8,10],slabLongitudinal=[6.3,8,10,12.5,16],slabTransverse=[6.3,8,10])
    else:state['bitolaSelectionsObserved']=None
    write(out/f'R51-parametros-{branch}.json',state);states.append(state)
protected=[]
for path in (root/'outputs/Complementacao-H03-R50-LAJES-BIM-NAO-EXECUTAR/R50-manifesto.json',root/'outputs/Complementacao-H03-R49-LAJES-CAD-NAO-EXECUTAR/R49-manifesto-persistencia.json'):
    for row in json.loads(path.read_text(encoding='utf-8-sig'))['files']:
        assert sha(Path(row['path']))==row['sha256'],row['path'];protected.append(row['path'])
write(out/'R51-comparacao-parametros.json',dict(sameObservedGlobalParameters=states[0]['observedAfterReopen']==states[1]['observedAfterReopen'],
    changedFieldsByBranch={s['branch']:s['changedFieldCount'] for s in states},preservedFiles=len(protected),
    wholeNativeModelEquivalent=False,limits='Igualdade apenas dos campos globais lidos; nao comprova calculo, vinculos ou totalidade dos parametros. Tempos distintos/incompletos sem ranking.'))
for name in ('preparar-h03-r51.py','consolidar-h03-r51.py'):shutil.copy2(root/'work'/name,out/name)
write(out/'R51-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in out.rglob('*') if p.is_file() and p.name!='R51-manifesto.json']))
print(json.dumps(dict(frozenByBranch={s['branch']:len(s['frozenFiles']) for s in states},preservedFiles=len(protected),sameObservedGlobalParameters=True)))

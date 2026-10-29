"""Congela R48 CAD sem alterar os estados recebidos ou o ramo BIM."""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, json, shutil
ROOT=Path('D:/TCC'); OUT=ROOT/'outputs/Complementacao-H03-R48-VIGAS-CAD-NAO-EXECUTAR'
NATIVE=ROOT/'outputs/H03_CAD_R48_VIGAS_NAO_EXECUTAR'
R47=ROOT/'outputs/Complementacao-H03-R47-CAD-NAO-EXECUTAR'
R46=ROOT/'outputs/Intercambio-H03-R46-BIM-NAO-EXECUTAR'
P=ROOT/'outputs/Alternativa-H03-R43-ESTUDO-NAO-EXECUTAR/H03-R43-proposta.json'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,o:p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
at=datetime.now(timezone.utc).isoformat()
protected=[]
transient=[]
def verify(path,expected,group):
    p=Path(path); actual=sha(p)
    protected.append(dict(path=str(p),expected=expected,observed=actual,group=group,unchanged=actual==expected.lower()))
for r in load(R46/'R46-preservacao-origens.json')['sources']:verify(r['path'],r['expected'],'origens R43 e historicas')
for r in load(R46/'R46-manifesto.json')['files']:verify(r['path'],r['sha256'],'manifesto R46')
for r in load(R47/'R47-manifesto.json')['files']:verify(r['path'],r['sha256'],'manifesto R47')
for r in load(R47/'R47-congelamento.json')['files']:
    p=Path(r['source'])
    if p.suffix.lower()=='.errlog' and not p.exists() and r['bytes']==0:
        transient.append(dict(path=str(p),observation='ERRLOG vazio ausente no diretorio de trabalho; copia congelada preservada por manifesto R47.',frozen=r['frozen']))
    else:verify(r['source'],r['sha256'],'nativos R47')
assert all(r['unchanged'] for r in protected),[r for r in protected if not r['unchanged']]
write(OUT/'R48-preservacao.json',dict(atUtc=at,files=protected,allCheckedUnchanged=True,transientFiles=transient))
frozen=[]
for folder in ('Projeto Eberick','_DADOS_'):
    for p in sorted((NATIVE/folder).rglob('*')):
        if not p.is_file() or p.suffix.lower() in ('.bak','.lck','.tmp'):continue
        target=OUT/'congelado'/p.relative_to(NATIVE)
        target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():assert sha(p)==sha(target),target
        else:shutil.copy2(p,target)
        frozen.append(dict(source=str(p),frozen=str(target),sha256=sha(p),bytes=p.stat().st_size))
write(OUT/'R48-congelamento.json',dict(atUtc=at,files=frozen,limits='Preservacao local; sem teste em outra maquina.'))
for script in ('auditar-vigas-h03-r48.py','consolidar-h03-r48.py'):
    shutil.copy2(ROOT/'work'/script,OUT/script)
rules=ROOT/'outputs/Reauditoria-H02-R17-NAO-EXECUTAR/auditar-geometria-h02-r17.py'
shutil.copy2(rules,OUT/'regras-geometria-origem-r17.py')
initial=load(OUT/'R48-auditoria-vigas-inicial.json'); reopen=load(OUT/'R48-auditoria-vigas-reaberto.json')
assert initial['geometryPass'] and reopen['geometryPass'] and reopen['sameGeometryAndGuidsAfterReopen']
native=load(OUT/'R48-geometria-reaberto.json')
native_beams=len({(r['name'],round(r['max'][2],5)) for r in native['geometry'] if r['class']=='IfcBeam'})
with (OUT/'R48-mapa-vigas.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f,delimiter=';'); w.writerow(['id_proposta','nomes_nativos','solidos_IFC','geometria_confere'])
    for b in reopen['beams']:w.writerow([b['sourceId'],' | '.join(b['nativeNames']),b['exportedParts'],all(b['checks'].values())])
timing=load(OUT/'R48-tempo-vigas-CAD.json')
state=dict(atUtc=at,revision='H03/R48',proposalRunId=load(P)['runId'],proposalSha256=sha(P),
    CAD=dict(nativeProject=str(NATIVE/'Projeto Eberick/H03_CAD_R48_VIGAS_NAO_EXECUTAR.prj'),
             columnSegments=22,logicalBeams=29,nativeBeamNamesByLevel=native_beams,beamSolids=32,slabs=0,
             geometryAuditPassed=True,reopenedAndReexported=True,geometryAndGuidsPersisted=True),
    BIM=dict(nativeProject=str(ROOT/'outputs/H03_BIM_R46_IFC_NAO_EXECUTAR/Projeto Eberick/H03_BIM_R46_IFC_NAO_EXECUTAR.prj'),
             unchangedSinceR46=True,columnSegments=22,logicalBeams=29,beamSolids=32,slabs=0),
    stageElapsedMs=timing['elapsedMs'],launchElapsedMs=timing['launchElapsedMs'],wholeFlowRankingAvailable=False,
    nativeSlabsPendingPerBranch=11,calculationPerformed=False,structuralApproval=False,monographEdited=False,
    observedOperations=['13 vigas comuns lancadas em N1 e copiadas para N2 pelo Eberick',
        'V4A-N1 20x16 cm e V15-N1 20x30 cm especificas do nivel N1',
        'V4A-N2 20x30 cm e complemento de V2-N2 20x55 cm lancados separadamente',
        'V2-N2 e representada por dois nomes nativos; conciliada como uma viga logica',
        'comando Unificar aberto por engano e cancelado antes de selecionar',
        'Escape no campo de coordenadas nao encerrou o comando; troca de croqui recuperou o foco',
        'destino IFC herdado apontava R47; alterado para pasta R48 antes de gerar',
        'IFC de trabalho sobrescrito na segunda exportacao depois de arquivar o inicial'],
    limits=['Auditoria geometrica e persistencia nao comprovam conectividade ou dimensionamento.',
            'Oito erros de esquema IFC permanecem nas listas opcionais vazias de identificacao.',
            'Tempo exploratorio assistido com documentacao, recuperacoes e latencias; sem total comparavel.',
            'Nao se copiou o modelo BIM para completar o receptor CAD.'],
    pending=['11 lajes em cada receptor, incluindo contorno especifico da varanda em N1',
             'materiais cobrimentos e parametros nativos harmonizados',
             'cargas vento combinacoes e apoios idealizados',
             'compatibilizacao arquitetonica e conectividade analitica',
             'calculo verificacoes ELU/ELS estabilidade e comparacao em escopos iguais'])
write(OUT/'R48-estado-atual.json',state)
plan=dict(preparedAtUtc=at,proposal=str(P),proposalSha256=sha(P),status='ROTEIRO, NAO LANCADO',
          elements=[e for e in load(P)['elements'] if e['kind']=='slab'],
          instructions=['Nova revisao propria de cada ramo e cronometro antes das acoes.',
                        'Conferir contornos internos de vigas e espessuras; nao tratar o IFC sem lajes como preservacao delas.',
                        'Varanda em balanco requer contorno e verificacao especifica; capacidade nao comprovada.'])
write(OUT/'R49-lajes-a-lancar-proposta.json',plan)
manifest=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='R48-manifesto.json']
write(OUT/'R48-manifesto.json',dict(atUtc=at,files=manifest))
print(json.dumps(dict(protectedFiles=len(protected),frozenFiles=len(frozen),manifestFiles=len(manifest),
                     logicalBeams=29,nativeBeamNames=native_beams,beamSolids=32,geometryAndReopeningPass=True,
                     elapsedMs=timing['elapsedMs']),indent=2))

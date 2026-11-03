"""Auditoria de evidências R175. Não edita PRJ nem executa cálculo estrutural."""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib, importlib.util, json, math, re, shutil, zipfile

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Cargas-H03-R175-A1-A2-BIM-NAO-EXECUTAR')

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

sap = module('sap175', HERE.parent/'h03-r122/consolidar.py')
native = module('native175', HERE.parent/'h03-r174/auditar_apoios.py')
summary_reader = module('summary175', HERE.parent/'h03-r172/consolidar.py')

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path): return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def write(path, value): Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
def multiset(rows): return Counter(json.dumps(r, sort_keys=True) for r in rows)

def audit_models(before, after, plan):
    if before['joints'] != after['joints'] or before['frames'] != after['frames']:
        raise ValueError('Geometria analitica mudou entre as duas analises R175')
    if set(before['tables']) != set(after['tables']):
        raise ValueError('Conjunto de tabelas mudou')
    load_tables = {'JOINT LOADS - FORCE', 'FRAME LOADS - POINT'}
    unchanged = []
    for table in before['tables']:
        if table not in load_tables:
            if multiset(before['tables'][table]) != multiset(after['tables'][table]):
                raise ValueError('Tabela fora do escopo mudou: '+table)
            unchanged.append(table)
    if len(plan) != 13 or len({r['id'] for r in plan}) != 13:
        raise ValueError('Plano deve conter treze pontos unicos')
    checked = []
    for row in plan:
        point = (row['xCm'], row['yCm'], row['zCm'])
        ids = [k for k,v in after['joints'].items() if v == point]
        if len(ids) != 1: raise ValueError('No ausente ou ambiguo: '+row['id'])
        joint = ids[0]
        edges = [k for k,ends in after['frames'].items() if point in ends]
        if len(edges) != 2: raise ValueError('Conectividade inesperada: '+row['id'])
        for action, pattern in [('G','G2'), ('QT','QT')]:
            old = [r for r in before['tables']['JOINT LOADS - FORCE'] if r['Joint']==joint and r['LoadPat']==pattern]
            new = [r for r in after['tables']['JOINT LOADS - FORCE'] if r['Joint']==joint and r['LoadPat']==pattern]
            if old or len(new)!=1 or new[0]['CoordSys']!='GLOBAL':
                raise ValueError('Carga previa, duplicada, ausente ou eixo incorreto: '+row['id']+'/'+action)
            actual = {}
            for ui, field in zip(['Fx','Fy','Fz','Mx','My','Mz'], ['F1','F2','F3','M1','M2','M3']):
                value = sap.number(new[0][field])
                # Relação NUMÉRICA observada entre o campo nativo e esta exportação.
                # Não equivale a calibrar kN/kgf ou kN.m/kgf.cm em unidades físicas.
                expected = row[action][ui]*100
                if not math.isclose(value,expected,abs_tol=.000051,rel_tol=0):
                    raise ValueError('Componente divergente: '+row['id']+'/'+action+'/'+field)
                actual[field] = value
            checked.append(dict(id=row['id'],joint=joint,positionCm=point,action=action,
                loadPattern=pattern,inputVectorNative=row[action],exportedVector=actual,connectedFrames=edges))
    changes = {}
    for table in load_tables:
        a,b = (multiset(m['tables'][table]) for m in [before,after])
        changes[table] = dict(removed=[dict(row=json.loads(r),count=n) for r,n in (a-b).items()],
                             added=[dict(row=json.loads(r),count=n) for r,n in (b-a).items()])
    # Os demais vetores incluem transferência da grelha para o pórtico. Conservar
    # as diferenças, em vez de declarar que só 26 linhas do arquivo mudaram.
    target_ids = {r['joint'] for r in checked}
    changes['jointRowsOutsideTargetNodes'] = {}
    for key in ['removed','added']:
        changes['jointRowsOutsideTargetNodes'][key] = [e for e in changes['JOINT LOADS - FORCE'][key] if e['row']['Joint'] not in target_ids]
    totals = {}
    for key,model in [('before',before),('after',after)]:
        values = defaultdict(float)
        for r in model['tables']['FRAME LOADS - POINT']:
            values[r['LoadPat']+'/'+r['Dir']] += sap.number(r['Force'])
        totals[key] = dict(values)
    return dict(checkedVectors=checked,checkedVectorCount=len(checked),checkedComponents=len(checked)*6,
        jointCount=len(after['joints']),frameCount=len(after['frames']),unchangedTables=unchanged,
        geometryUnchangedDuringLoadEdition=True,rawLoadChanges=changes,
        framePointForceSumsByPatternAndLocalDirection=totals,
        otherExportedLoadRowsUnchanged=False,nativeToExportNumericFactorObserved=100,
        physicalSIConversionCalibrated=False,globalEquilibriumVerified=False)

def main():
    prep=read(OUT/'R175-preparacao-plano.json')
    for e in prep['sourceFiles']:
        if sha(Path(prep['sourceRoot'])/e['relativePath']) != e['sha256']:
            raise ValueError('Fonte R174 alterada')
    paths={k:OUT/f'{folder}/portico_SAP2000_elastico.$2k' for k,folder in [
        ('stale','analitico-nos-sem-cargas'),('before','analitico-apos-regenerar'),('after','analitico-cargas-final')]}
    models={k:sap.parse(p.read_text(encoding='cp1252')) for k,p in paths.items()}
    result=audit_models(models['before'],models['after'],prep['rows'])
    stale=models['stale']
    absent=[r['id'] for r in prep['rows'] if (r['xCm'],r['yCm'],r['zCm']) not in stale['joints'].values()]
    if len(absent)!=13 or len(stale['joints'])!=110 or len(stale['frames'])!=134:
        raise ValueError('Evidencia da exportacao desatualizada inesperada')
    samples=[]
    for id in ['RC03','RC11']:
        row=next(r for r in prep['rows'] if r['id']==id)
        identity=(OUT/f'R175-{id}-identidade-reaberta.txt').read_text(encoding='utf-8')
        if 'R175-BIM-CARGAS-A1-A2-NAO-EXECUTAR' not in identity: raise ValueError('Projeto da amostra incorreto')
        for field,expected in [('X',row['xCm']),('Y',row['yCm'])]:
            values=set(re.findall(r'editar \(settable, string\) '+field+r' Value: (\S+) ID:',identity))
            if len(values)!=1 or float(values.pop())!=expected: raise ValueError('Identidade da amostra divergente')
        for action,label in [('G','Adicional'),('QT','Q_TELHADO_MANUTENCAO')]:
            p=OUT/f'R175-{id}-{action}-reaberto.txt'
            text=p.read_text(encoding='utf-8')
            if 'R175-BIM-CARGAS-A1-A2-NAO-EXECUTAR' not in text:raise ValueError('Projeto incorreto na releitura')
            values=native.extract(text.replace('R175-BIM-CARGAS-A1-A2','R174-BIM-CARGAS-COBERTURA'),label,row[action])
            samples.append(dict(id=id,action=action,displayed=values,evidence=p.name,sha256=sha(p)))
    text=(OUT/'R175-cargas-resumo-resultados.txt').read_text(encoding='utf-8')
    if 'R175-BIM-CARGAS-A1-A2-NAO-EXECUTAR' not in text:raise ValueError('Resumo de outro projeto')
    summary=summary_reader.extract(text.replace('R175-BIM-CARGAS-A1-A2','R172-BIM-DIAGNOSTICO-PARCIAL'),'BIM')
    project=Path(prep['targetRoot'])/'Projeto Eberick/R166-R160-3NIVEIS-CONFIG-CAD-NAO-EXECUTAR.prj'
    if sha(project)!='735ea69b5cbd0c95b92e88f6d25268452e5baf97a0c03ded19b4471a2974f849':
        raise ValueError('PRJ mudou desde a conferencia de persistencia')
    with zipfile.ZipFile(project) as z:
        if z.testzip() is not None:raise ValueError('PRJ corrompido')
    frozen=OUT/'R175-receptor-congelado';frozen.mkdir(exist_ok=True);files=[]
    for p in sorted(Path(prep['targetRoot']).rglob('*')):
        if not p.is_file() or p.suffix.lower() in ('.log','.errlog'):continue
        rel=p.relative_to(prep['targetRoot']);dest=frozen/rel;dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists() and sha(dest)!=sha(p):raise ValueError('Congelado divergente')
        shutil.copy2(p,dest);files.append(dict(relativePath=str(rel),bytes=p.stat().st_size,sha256=sha(p)))
    time=read(OUT/'R175-sessao-com-releitura-tempo.json')
    if time['duracaoMs']!=time['fim']['ms']-time['inicio']['ms']:raise ValueError('Intervalo temporal inconsistente')
    first=read(OUT/'R175-cargas-primeiro-save-tempo.json')
    if first['duracaoMs']!=int(datetime.fromisoformat(first['fim'].replace('Z','+00:00')).timestamp()*1000)-first['inicio']['ms']:
        raise ValueError('Primeiro save temporal inconsistente')
    result.update(revision='H03/R175',recordedAtUtc=datetime.now(timezone.utc).isoformat(),projectPath=str(project),
        projectSha256=sha(project),sourceFilesUnchanged=True,protectedSourceFiles=len(prep['sourceFiles']),
        exports={k:dict(path=str(p),sha256=sha(p)) for k,p in paths.items()},
        rejectedStaleExport=dict(missingTargetNodes=absent,jointCount=110,frameCount=134,accepted=False),
        afterRegenerationTargetNodes=13,afterRegenerationJointCount=123,afterRegenerationFrameCount=147,
        nativeReadbackSamples=samples,nativeReadbackComponents=24,nativeReadbackSampleNotCensus=True,
        savedClosedReopened=True,projectBytesUnchangedDuringReadback=True,summary=summary,
        sessionTime=time,containedTimeUntilFirstSave=first,doNotAddContainedTimes=True,
        staticAnalysisPerformed=True,porticoConfiguredStiffnessDisplacementsPerformed=True,
        dimensioningPerformed=False,slabDeflectionsPerformed=False,stairIntegratedInReceiver=False,
        fullAllLoadEqualityAgainstCadVerified=False,fullPairedFlowTimeMeasured=False,finalRankingAllowed=False,
        structuralApproval=False,frozenFiles=files)
    write(OUT/'R175-resultado.json',result)
    print(json.dumps(dict(vectors=26,components=156,readbackSamples=4,sessionMs=time['duracaoMs'],untilSaveMs=first['duracaoMs'],prj=sha(project))))

if __name__=='__main__':main()

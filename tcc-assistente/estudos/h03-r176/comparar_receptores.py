"""Compara tabelas exportadas por posição, preservando diferenças e precisão."""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import hashlib,importlib.util,json,re,shutil,zipfile

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Analise-H03-R176-COMPARACAO-RECEPTORES-NAO-EXECUTAR')
spec=importlib.util.spec_from_file_location('sap176',HERE.parent/'h03-r122/consolidar.py')
sap=importlib.util.module_from_spec(spec);spec.loader.exec_module(sap)

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def normalize(value):
    if isinstance(value,dict):return {k:normalize(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [normalize(v) for v in value]
    if isinstance(value,str) and re.fullmatch(r'[+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+)(?:[eE][+-]?\d+)?',value):
        return sap.number(value)
    return value

def canonical_table(model,table):
    sections={r['SectionName']:{k:v for k,v in r.items() if k!='SectionName'} for r in model['tables']['FRAME SECTION PROPERTIES 01 - GENERAL']}
    result=[]
    for row in model['tables'][table]:
        item=dict(row)
        if table=='JOINT COORDINATES':item.pop('Joint')
        elif 'Joint' in item:item['Joint']=model['joints'][item['Joint']]
        if table=='CONNECTIVITY - FRAME':
            item={'orderedEndpointsCm':model['frames'][row['Frame']]}
        elif 'Frame' in item:item['Frame']=model['frames'][item['Frame']]
        if 'AnalSect' in item:item['AnalSect']=sections[item['AnalSect']]
        if table=='FRAME SECTION PROPERTIES 01 - GENERAL':item.pop('SectionName')
        result.append(json.dumps(normalize(item),sort_keys=True))
    return Counter(result)

def compare(cad,bim):
    if set(cad['tables'])!=set(bim['tables']):raise ValueError('Tabelas ausentes; comparacao incompleta')
    tables={}
    for table in cad['tables']:
        a,b=(canonical_table(m,table) for m in [cad,bim])
        tables[table]=dict(equal=a==b,cadRows=sum(a.values()),bimRows=sum(b.values()),
            onlyCad=[dict(row=json.loads(r),count=n) for r,n in (a-b).items()],
            onlyBim=[dict(row=json.loads(r),count=n) for r,n in (b-a).items()])
    jointsets=[Counter(m['joints'].values()) for m in [cad,bim]]
    edges=[Counter(tuple(sorted(v)) for v in m['frames'].values()) for m in [cad,bim]]
    # A orientação I-J é conservada na comparação principal. Esta conferência
    # adicional ignora apenas I-J para comparar propriedades de seção por trecho.
    def spatial_sections(model):
        rows=canonical_table(model,'FRAME SECTION ASSIGNMENTS')
        result=Counter()
        for raw,n in rows.items():
            item=json.loads(raw);item['Frame']=sorted(item['Frame'])
            result[json.dumps(item,sort_keys=True)]+=n
        return result
    def nodal_rows(model):
        result={}
        for r in model['tables'].get('JOINT LOADS - FORCE',[]):
            key=(model['joints'][r['Joint']],r['LoadPat'],r['CoordSys'])
            if key in result:raise ValueError('Carga nodal duplicada; nao somar silenciosamente')
            result[key]={f:sap.number(r[f]) for f in ['F1','F2','F3','M1','M2','M3']}
        return result
    a,b=nodal_rows(cad),nodal_rows(bim);nodal=[]
    for key in sorted(a.keys()|b.keys()):
        av,bv=a.get(key),b.get(key)
        if av!=bv:
            nodal.append(dict(positionCm=key[0],pattern=key[1],coordinateSystem=key[2],cad=av,bim=bv,
                bimMinusCad={k:bv[k]-av[k] for k in av} if av is not None and bv is not None else None))
    return dict(jointCoordinateMultisetsEqual=jointsets[0]==jointsets[1],frameUndirectedEndpointMultisetsEqual=edges[0]==edges[1],
        sectionPropertiesByUndirectedSegmentEqual=spatial_sections(cad)==spatial_sections(bim),
        nodalLoadPositionPatternKeysEqual=a.keys()==b.keys(),nodalLoadDifferences=nodal,
        counts={k:dict(joints=len(m['joints']),frames=len(m['frames'])) for k,m in [('CAD',cad),('BIM',bim)]},
        tables=tables,allExportedTablesEqualAfterSpatialNormalization=all(r['equal'] for r in tables.values()),
        comparisonAtExportedPrecision=True,reverseFrameDirectionsNotSilentlyEquated=True,
        unknownMissingInformationNotValidated=True,completeNativeModelEquivalenceVerified=False,structuralApproval=False)

def main():
    prep=read(OUT/'R176-preparacao.json');protected=[]
    for branch,entry in prep['branches'].items():
        for r in entry['sourceFiles']:
            if sha(Path(entry['sourceRoot'])/r['relativePath'])!=r['sha256']:raise ValueError('Fonte alterada')
        if sha(entry['projectPath'])!=entry['projectSha256']:raise ValueError('PRJ de consulta alterado')
        with zipfile.ZipFile(entry['projectPath']) as z:
            if z.testzip() is not None:raise ValueError('PRJ corrompido')
        protected.append(dict(branch=branch,prjSha256=entry['projectSha256'],prjBytesUnchanged=True,sourceFileCount=len(entry['sourceFiles'])))
    source=OUT.parent/'Cargas-H03-R175-A1-A2-BIM-NAO-EXECUTAR/analitico-cargas-final'
    provenance=[]
    for p in source.glob('*.$2k'):
        dest=OUT/'SAP-BIM'/p.name
        if dest.exists() and sha(dest)!=sha(p):raise ValueError('Copia BIM divergente')
        shutil.copy2(p,dest);provenance.append(dict(sourcePath=str(p),destinationPath=str(dest),sha256=sha(p)))
    if len(provenance)!=3:raise ValueError('Exportacao BIM incompleta')
    models={};exports={}
    for branch in ['CAD','BIM']:
        models[branch]={};exports[branch]=[]
        files=list((OUT/f'SAP-{branch}').glob('*.$2k'))
        if len(files)!=3:raise ValueError('Exportacao incompleta: '+branch)
        for p in files:
            kind='portico' if p.name.startswith('portico') else ('N1' if re.search(r'[-_]N1[.]',p.name) else 'N2')
            if kind in models[branch]:raise ValueError('Tipo duplicado')
            models[branch][kind]=sap.parse(p.read_text(encoding='cp1252'))
            exports[branch].append(dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size))
    comparisons={kind:compare(models['CAD'][kind],models['BIM'][kind]) for kind in ['portico','N1','N2']}
    result=dict(revision='H03/R176',recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        scope='Comparacao somente leitura dos receptores corrigidos; CAD R172, BIM R175; SAP2000 nao executado',
        protectedProjects=protected,exports=exports,bimExportReuseProvenance=provenance,
        reusedBimExportNotNewTimedNativeExport=True,comparisons=comparisons,
        cadExportObservationTime=read(OUT/'CAD-exportacao-tempo.json'),newProcessingPerformed=False,
        fullPairedFlowTimeMeasured=False,finalRankingAllowed=False,structuralApproval=False)
    write(OUT/'R176-resultado.json',result)
    print(json.dumps({k:dict(counts=v['counts'],equalTables=[t for t,r in v['tables'].items() if r['equal']],differentTables={t:dict(cadOnly=sum(e['count'] for e in r['onlyCad']),bimOnly=sum(e['count'] for e in r['onlyBim'])) for t,r in v['tables'].items() if not r['equal']}) for k,v in comparisons.items()}))

if __name__=='__main__':main()

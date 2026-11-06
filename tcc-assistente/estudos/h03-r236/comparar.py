"""Compara controles IFC reais de duas recepções independentes, sem editar modelos."""
from collections import Counter
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'h03-r232'))
from auditar_pilares import snapshot, sha

ROOT = Path('D:/TCC/outputs')
OUT = ROOT/'H03-R236-COMPARACAO-GEOMETRICA-CAD-BIM-NAO-EXECUTAR'
CAD = ROOT/'H03-R235-CAD-VIGAS-ESCADA-NAO-EXECUTAR/CAD'
BIM = ROOT/'H03-R231-IFC4-CONTINUIDADE-NAO-EXECUTAR/R231-BIM-SECOES-NOMINAIS-NAO-EXECUTAR'
TOL = .0002


def compare():
    paths=[r/'Arquivos do projeto/Modelo 3D.IFC' for r in (CAD,BIM)]
    paths += [p for r in (CAD,BIM) for p in (r/'Projeto Eberick').glob('*.prj')]
    evidence=[ROOT/(f'H03-{r}-NAO-EXECUTAR')/(r[:4]+'-auditoria.json') for r in
              ('R231-IFC4-CONTINUIDADE','R232-CAD-PILARES','R233-CAD-VIGAS-N2','R234-CAD-VIGAS-N1')]
    evidence.append(CAD.parent/'R235-auditoria.json')
    paths+=evidence
    hashes={str(p):sha(p) for p in paths}
    e231,e232,e233,e234,e235=[json.loads(p.read_text(encoding='utf-8-sig')) for p in evidence]
    if (e231['reportCounts']!={'Vigas':32,'Pilares':23} or e232['sourceColumns']!=23
            or e233['sourceCadBeams']+e234['sourceCadBeams']+e235['addedBeamParts']!=32):
        raise ValueError('Auditorias de origem não sustentam as contagens nominais')
    cad,bim=map(snapshot,paths[:2])
    expected={'IfcColumn':35,'IfcBeam':35}
    if any(dict(Counter(p['cls'] for p in model.values()))!=expected for model in (cad,bim)):
        raise ValueError('Contagem/classes diferentes do marco esperado')
    pairs=[]; consumed=set()
    for guid,p in cad.items():
        candidates=[]
        for bg,q in bim.items():
            if p['cls']!=q['cls']: continue
            delta=max(abs(p['geometry'][s][i]-q['geometry'][s][i])
                      for s in ('minM','maxM') for i in range(3))
            if delta<=TOL: candidates.append((bg,q,delta))
        if len(candidates)!=1 or candidates[0][0] in consumed:
            raise ValueError('Correspondência geométrica ausente, duplicada ou ambígua: '+guid)
        bg,q,delta=candidates[0]; consumed.add(bg)
        props=lambda x:{k:{a:b for a,b in v.items() if a!='id'} for k,v in x['psets'].items()}
        cp,bp=props(p),props(q)
        differences=[]
        for group in sorted(set(cp)|set(bp)):
            for key in sorted(set(cp.get(group,{}))|set(bp.get(group,{}))):
                cv,bv=cp.get(group,{}).get(key),bp.get(group,{}).get(key)
                if cv!=bv: differences.append(dict(group=group,key=key,cad=cv,bim=bv))
        concreteEqual=cp['Pset_ConcreteElementGeneral']==bp['Pset_ConcreteElementGeneral']
        pairs.append(dict(cadGuid=guid,bimGuid=bg,kind=p['cls'],cadName=p['name'],bimName=q['name'],
                          cadLevel=p['level'],bimLevel=q['level'],maxCoordinateDifferenceM=delta,
                          concretePropertiesEqual=concreteEqual,propertyDifferences=differences))
    if len(consumed)!=len(bim): raise ValueError('Elementos BIM sem correspondência')
    level_map={level:sorted({p['bimLevel'] for p in pairs if p['cadLevel']==level})
               for level in sorted({p['cadLevel'] for p in pairs})}
    if any(len(v)!=1 for v in level_map.values()) or len({v[0] for v in level_map.values()})!=4:
        raise ValueError('Correspondência dos pavimentos não é biunívoca')
    if hashes!={str(p):sha(p) for p in paths}: raise ValueError('Modelo modificado durante conferência')
    result=dict(revision='R236',scope='Recepção recomposta de pilares e vigas; exclui lajes, escada, cargas e cálculo',
                cadNativeRevision='R235',bimNativeRevision='R231',partsPerFlow=70,
                classCountsPerFlow=expected,bijectionVerified=True,rectangularMeshesVerified=True,
                sourceIdentitiesPerFlow=dict(columns=23,beams=32),geometryToleranceM=TOL,
                maximumCoordinateDifferenceM=max(p['maxCoordinateDifferenceM'] for p in pairs),
                allConcretePropertiesEqual=all(p['concretePropertiesEqual'] for p in pairs),
                pairsWithPropertyDifferences=sum(bool(p['propertyDifferences']) for p in pairs),
                pairsWithDifferentNames=sum(p['cadName']!=p['bimName'] for p in pairs),
                levels=level_map,hashes=hashes,pairs=pairs,modelsModified=False,
                analyticalConnectivityEquivalent=None,loadsComplete=False,structuralApproval=False,
                timeRankingValid=False,timeRankingReason='Escopos diferentes; CAD contém interrupções; diagnóstico e preparação do BIM não estão integralmente cronometrados.')
    OUT.mkdir(exist_ok=True)
    (OUT/'R236-comparacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    public={k:v for k,v in result.items() if k!='pairs'}
    (Path(__file__).parent/'R236-resultados.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=['# Correspondência geométrica CAD R235 × BIM R231','',
          'Somente vigas e pilares. Os GUIDs completos estão no JSON. Esta tabela não comprova vínculos analíticos.','',
          '| Classe | Nível CAD | Nome CAD | Nível BIM | Nome BIM | Maior diferença (mm) |',
          '|---|---|---|---|---|---:|']
    for p in sorted(pairs,key=lambda p:(p['cadLevel'],p['kind'],p['cadName'])):
        rows.append(f"| {p['kind']} | {p['cadLevel']} | {p['cadName']} | {p['bimLevel']} | {p['bimName']} | {p['maxCoordinateDifferenceM']*1000:.5f} |")
    (OUT/'R236-correspondencia-elementos.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    print(json.dumps(public,ensure_ascii=False,indent=2))
    return result


if __name__=='__main__':
    compare()

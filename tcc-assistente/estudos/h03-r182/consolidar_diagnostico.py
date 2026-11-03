"""Consolida ensaio nativo real; nao confunde resumo de lajes com escadas."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,sys,zipfile,xml.etree.ElementTree as ET,math
from collections import Counter,defaultdict

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Diagnostico-H03-R182-DIMENSIONAMENTO-NAO-EXECUTAR')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def text_docx(p):
    with zipfile.ZipFile(p) as z:
        root=ET.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    return '\n'.join(''.join(t.text or '' for t in q.findall('.//w:t',ns)) for q in root.findall('.//w:p',ns))


def parse_report(text):
    start=text.index('DIMENSIONAMENTO DOS ELEMENTOS')
    end=text.index('Tempo de dimensionamento dos elementos:',start)
    levels={}
    for match in re.finditer(r'Pavimento ([^\r\n]+)\s*([\s\S]*?)(?=Pavimento |\Z)',text[start:end]):
        raw_level=match[1].strip()
        level_match=re.search(r'(N[012])$',raw_level)
        if not level_match:
            raise ValueError('Pavimento nao mapeado: '+raw_level)
        level=level_match[1]
        if level in levels:
            raise ValueError('Pavimento duplicado')
        counts={}
        for line in match[2].splitlines():
            if not line.strip():
                continue
            row=re.fullmatch(r'\s*(Pilares|Vigas|Lajes): (\d+) Com sucesso(?:, (\d+) com erro)?\s*',line)
            if not row or row[1] in counts:
                raise ValueError('Linha de dimensionamento nao reconhecida: '+line)
            counts[row[1]]=dict(reportedSuccess=int(row[2]),reportedError=int(row[3] or 0))
        levels[level]=dict(nativeLevelName=raw_level,reportedCategories=counts,
                           emptyLevelBlockIsNotAZeroCount=not bool(counts))
    total=re.findall(r'Tempo total de processamento:\s*(\d\d:\d\d:\d\d)',text)
    sizing=re.findall(r'Tempo de dimensionamento dos elementos:\s*(\d\d:\d\d:\d\d)',text)
    if len(total)!=1 or len(sizing)!=1:
        raise ValueError('Tempos ausentes ou ambiguos')
    def seconds(s):
        h,m,v=map(int,s.split(':'))
        if m>59 or v>59:
            raise ValueError('Tempo invalido')
        return h*3600+m*60+v
    return dict(levels=levels,nativeTotalSeconds=seconds(total[0]),nativeDimensioningSeconds=seconds(sizing[0]),
        dimensioningTimeIsIncludedInTotal=True,reportedSuccessMayIncludeWarnings=True,
        stairPassCannotBeInferredFromReportedSlabCounts=True)


def prism_signature(vertices,faces):
    """Verifica solido fechado retangular, permitindo trocar diagonais de faces."""
    v=[tuple(map(float,p)) for p in vertices]
    lo=tuple(min(p[k] for p in v) for k in range(3));hi=tuple(max(p[k] for p in v) for k in range(3))
    if len(v)!=8 or len(faces)!=12 or any(b-a<=1e-9 for a,b in zip(lo,hi)):
        raise ValueError('Prisma nao reconhecido')
    expected={(round(x,7),round(y,7),round(z,7)) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])}
    if {tuple(round(x,7) for x in p) for p in v}!=expected:
        raise ValueError('Vertices nao sao os oito cantos')
    edges=Counter();areas=defaultdict(float)
    for tri in faces:
        a,b,c=[v[i] for i in tri]
        u=[b[k]-a[k] for k in range(3)];w=[c[k]-a[k] for k in range(3)]
        cross=[u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0]]
        ta=math.sqrt(sum(x*x for x in cross))/2
        if ta<1e-12:
            raise ValueError('Face degenerada')
        planes=[(k,side) for k in range(3) for side,bound in enumerate((lo[k],hi[k])) if all(abs(p[k]-bound)<1e-9 for p in (a,b,c))]
        if len(planes)!=1:
            raise ValueError('Triangulo fora da face do prisma')
        areas[planes[0]]+=ta
        for i,j in zip(tri,list(tri[1:])+[tri[0]]):
            edges[tuple(sorted((int(i),int(j))))]+=1
    if any(n!=2 for n in edges.values()):
        raise ValueError('Prisma aberto ou duplicado')
    for k in range(3):
        dims=[hi[q]-lo[q] for q in range(3) if q!=k]
        for side in (0,1):
            if not math.isclose(areas[k,side],dims[0]*dims[1],rel_tol=1e-8,abs_tol=1e-10):
                raise ValueError('Face incompleta ou sobreposta')
    return tuple(round(x,7) for x in lo+hi)


def map_baseline_v2(control):
    """Compara prismas fechados dos IFCs R178, anteriores ao diagnostico R182."""
    sys.path.insert(0,'D:/TCC/work/ifc/deps')
    import ifcopenshell,ifcopenshell.geom
    import numpy as np
    models={b:ifcopenshell.open(r['ifcPath']) for b,r in control['branches'].items()}
    settings=ifcopenshell.geom.settings();settings.set(settings.USE_WORLD_COORDS,True)
    meshes={}
    for b,m in models.items():
        rows=[]
        for e in m.by_type('IfcBeam'):
            shape=ifcopenshell.geom.create_shape(settings,e)
            v=np.asarray(shape.geometry.verts).reshape(-1,3)
            f=np.asarray(shape.geometry.faces).reshape(-1,3)
            try:
                signature=prism_signature(v,f)
            except ValueError:
                signature=None
            rows.append(dict(name=e.Name,guid=e.GlobalId,lo=v.min(0).tolist(),hi=v.max(0).tolist(),signature=signature))
        meshes[b]=rows
    result=[]
    for row in meshes['BIM']:
        if row['name']!='V2' or abs(row['hi'][2]-3.2)>1e-7:
            continue
        if row['signature'] is None:
            raise ValueError('Peca V2 nao prismatica')
        matches=[x for x in meshes['CAD'] if x['signature']==row['signature']]
        if len(matches)!=1:
            raise ValueError('Peca correspondente nao identificada de forma unica')
        cad=matches[0]
        result.append(dict(bimName=row['name'],bimGuid=row['guid'],cadName=cad['name'],cadGuid=cad['guid'],
            minM=row['lo'],maxM=row['hi'],closedOrthogonalPrismsEqualAt1eMinus7M=True,
            triangleDiagonalEqualityNotRequiredForSamePrism=True,
            basedOnBaselineR178IfcNotAFreshR182Export=True))
    if len(result)!=2:
        raise ValueError('Esperadas duas pecas fisicas de V2 no N1')
    return result


def main():
    prep=json.loads((OUT/'R182-preparacao.json').read_text(encoding='utf-8'))
    control=json.loads((HERE.parent/'h03-r178/R178-comparacao-CAD-BIM.json').read_text(encoding='utf-8'))
    branches={}
    for b,r in prep['branches'].items():
        for f in r['sourceFiles']:
            if sha(Path(r['sourceRoot'])/f['relativePath'])!=f['sha256']:
                raise ValueError('Fonte R178 alterada: '+b+' '+f['relativePath'])
        if sha(control['branches'][b]['ifcPath'])!=control['branches'][b]['ifcSha256']:
            raise ValueError('IFC de referencia alterado')
        report=OUT/f'{b}-mensagens-analise.docx'
        text=text_docx(report)
        (OUT/f'{b}-mensagens-analise.txt').write_text(text,encoding='utf-8')
        parsed=parse_report(text)
        prj=Path(r['projectPath'])
        with zipfile.ZipFile(prj) as z:
            if z.testzip():
                raise ValueError('PRJ ilegivel')
        start=json.loads((OUT/f'{b}-processamento-inicio.json').read_text(encoding='utf-8'))
        stop=json.loads((OUT/f'{b}-processamento-observacao-final.json').read_text(encoding='utf-8'))
        if 'Estrutura processada com avisos' not in stop['state']:
            raise ValueError('Termino nativo nao confirmado')
        observed=(datetime.fromisoformat(stop['observedAtUtc'])-datetime.fromisoformat(start['startedAtUtc'])).total_seconds()
        branches[b]=dict(projectPath=str(prj),projectSha256=sha(prj),projectZipValid=True,
            sourceR178FilesUnchanged=len(r['sourceFiles']),nativeReportPath=str(report),nativeReportSha256=sha(report),
            nativeDimensioningReport=parsed,observedClickToFirstConfirmedCompletionSeconds=observed,
            observedIntervalIncludesToolAndObservationLatency=True,observedIntervalIsNotNativeProcessingTime=True,
            integrityWarningAtOpening=b=='CAD',nativeIntegrityCheckPerformedBeforeProcessing=b=='CAD',
            sourceNotReplacedByDiagnosticCopy=True,fullFlowTimeMeasured=False,
            staircaseUiObservation=dict(LE1='calculado',LE2='calculado',LE3='Erro D31',
                LE3Message='Erro no calculo da armadura principal (direcao X)',
                LE3DiameterResultsMm={str(d):'Erro A11 - Largura do apoio insuficiente' for d in [6.3,8.,10.,12.5,16.]},
                sourceImages=[f'{b}-LE3-armadura-diagnostico-0.png',f'{b}-LE3-D31-detalhe-0.png'],
                observationMethod='Leitura visual da planilha nativa e do resultado por bitola; nao OCR automatico'),
            postDiagnosticGeometryAndLoadRetentionNotVerifiedByFreshExport=True,structuralApproval=False)
    result=dict(revision='H03/R182',recordedAtUtc=datetime.now(timezone.utc).isoformat(),branches=branches,
        selection=dict(N2=['Vigas','Pilares','Lajes'],N1=['Vigas','Pilares','Lajes','Escadas'],N0=[],
            foundationsExcluded=True),
        options=dict(ELU=True,selectedSuperstructureDimensioning=True,
            frameDeflectionConfiguredRigidity=True,slabDeflection=False,dynamic=False,
            constructionStages=False,semiRigidRedistributionLimitCheck=False),
        BIMV2NativeObservation=dict(level='TCC-7a6267fd-N1',error='D16',nodeNumber=2,nodeName='P5',
            message='Erro na armadura negativa (no 2). Nenhuma bitola configurada pode ser usada.',
            diameterResultsMm={str(d):'Erro A07 - Taxa de armadura maior que a configurada' for d in [8.,10.,12.5,16.,20.]},
            sectionsCm=[[20,16],[20,45]],node2MdKnM=-36.90,
            observationMethod='Leitura visual das planilhas e resultados por bitola',
            sourceImages=['BIM-V2-no2-resultados-armadura-0.png','BIM-V2-no2-bitolas-complemento-0.png','BIM-V2-secoes-0.png'],
            maximumSteelRatioConfigurationNotChanged=True,ratioLimitValueNotRead=True),
        baselineR178V2PhysicalMapping=map_baseline_v2(control),
        beamGroupingDiffersBetweenBranches=True,causalAttributionToGroupingNotProven=True,
        allStructuralElementsSuccessfullyDesigned=False,nativeSummaryIsNotCompleteStairStatus=True,
        fullPairedFlowComparisonFinished=False,completeNativeModelEquivalenceVerified=False,
        finalReinforcementReviewed=False,structuralApproval=False,
        nativeTimingSingleObservationEach=True,nativeTimingCannotRankEntireWorkflows=True,
        references=[dict(title='Erro D16 - Erro na armadura negativa',url='https://suporte.altoqi.com.br/hc/pt-br/articles/360000680694'),
                    dict(title='Erro D31 - Erro no calculo da armadura principal',url='https://suporte.altoqi.com.br/hc/pt-br/articles/360000681913')])
    (OUT/'R182-diagnostico.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({b:dict(nativeTimes=r['nativeDimensioningReport']['nativeTotalSeconds'],
        reportedCategories=r['nativeDimensioningReport']['levels'],stairError=r['staircaseUiObservation']['LE3']) for b,r in branches.items()},indent=2))


if __name__=='__main__':
    main()

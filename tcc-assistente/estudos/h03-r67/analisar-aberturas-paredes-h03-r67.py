"""Sensibilidade geometrica e de massa das 11 aberturas; nao aplica cargas."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter
import json,hashlib,shutil,ast
root=Path('D:/TCC');out=root/'outputs/Paredes-H03-R67-ABERTURAS-NAO-APLICADO'
dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r67')
assert not out.exists() and not dest.exists()
tick=perf_counter();started=datetime.now(timezone.utc).isoformat()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=[root/'outputs/Paredes-H03-R55-ESTUDO-NAO-EXECUTAR/R55-paredes-referencia.json',root/'outputs/Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR/R56-paredes-trechos.json',root/'outputs/Cobertura-H03-R56-ESTUDO-NAO-EXECUTAR/R56-geometria-exportada.json',root/'outputs/Verificacao-H03-R57-NAO-EXECUTAR/R57-resultado.json']
protected=read(root/'outputs/Acoes-H03-R66-Q-TELHADO-NAO-EXECUTAR/R66-manifesto.json')['files']
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
walls=read(paths[0])['walls'];segments=read(paths[1])['segments'];geo=read(paths[2]);audit=read(paths[3])
assert len(walls)==20 and len(segments)==59
assert all(a['superstructureNamesGuidsBoxesTopAreasAndExportedPropertiesPreserved'] for a in audit['audits'].values())
def spatial(rows):return sorted((r['type'],tuple(r['min']+r['max'])) for r in rows if r['type'] in ('IfcBeam','IfcColumn','IfcSlab'))
assert spatial(geo['CAD'])==spatial(geo['BIM'])
def overlap(a,b,c,d):return max(0.,min(b,d)-max(a,c))
surface=1.565
openingrows=[];wallrows=[];sensitivity=[]
for w in walls:
    ss=[s for s in segments if s['wallId']==w['id']]
    assert abs(sum(s['lengthM'] for s in ss)-w['lengthBetweenAxesM'])<1e-5
    axis='x' if abs(w['y']-w['y2'])<1e-8 else 'y'
    gross=sum(s['lengthM']*s['grossHeightReferenceM'] for s in ss if s['route']!='coluna-sem-alvenaria' and s['grossHeightReferenceM'] is not None)
    unknown=[s for s in ss if s['route']!='coluna-sem-alvenaria' and s['grossHeightReferenceM'] is None]
    wallOpenings=[]
    for ref in w['openingReferencesR34']:
        specs=[o for o in w['openings'] if o['tag']==ref['tag']]
        assert len(specs)==1
        o=specs[0];a=min(ref[axis],ref[axis+'2']);rawWidth=abs(ref[axis+'2']-ref[axis]);width=o['widthM'];height=o['heightM']
        assert abs(rawWidth-width)<.002,(ref['id'],rawWidth,width)
        # Centraliza a largura nominal na leitura aproximada, sem ocultar o valor bruto.
        a=(ref[axis]+ref[axis+'2'])/2-width/2;b=a+width;unc=ref['coordinateUncertaintyM']
        tests=[]
        # Extremos e pontos de quebra tornam exata a faixa da intersecao em translacao.
        shifts={-unc,0.,unc}
        for s in ss:
            for cut in (s['fromM'],s['toM']):
                for edge in (a,b):
                    if -unc<=cut-edge<=unc:shifts.add(cut-edge)
        for delta in sorted(shifts):
            cols=sum(overlap(a+delta,b+delta,s['fromM'],s['toM']) for s in ss if s['route']=='coluna-sem-alvenaria')
            mason=sum(overlap(a+delta,b+delta,s['fromM'],s['toM']) for s in ss if s['route']!='coluna-sem-alvenaria')
            known=sum(overlap(a+delta,b+delta,s['fromM'],s['toM']) for s in ss if s['route']!='coluna-sem-alvenaria' and s['grossHeightReferenceM'] is not None)
            assert cols+mason<=width+1e-5
            tests.append(dict(translationM=delta,columnOverlapWidthM=cols,masonryOverlapWidthM=mason,knownHeightMasonryOverlapWidthM=known,conditionalMasonryDeductionM2=known*height))
        nominal=next(t for t in tests if t['translationM']==0)
        hvals=[s['grossHeightReferenceM'] for s in ss if s['grossHeightReferenceM'] is not None and s['route']!='coluna-sem-alvenaria' and overlap(a,b,s['fromM'],s['toM'])>1e-8]
        sill=o.get('sillM')
        verticalFit=(sill+height<=min(hvals)+1e-6) if sill is not None and hvals else None
        if ref['tag'].startswith('P') and hvals:verticalFit=height<=min(hvals)+1e-6
        row=dict(id=ref['id'],wallId=w['id'],tag=ref['tag'],axis=axis,rawStartM=min(ref[axis],ref[axis+'2']),rawWidthM=rawWidth,nominalWidthM=width,heightM=height,nominalStartM=a,nominalEndM=b,positionUncertaintyM=unc,uncertaintyIsStudyNotSurvey=True,nominalFullOpeningAreaM2=width*height,nominalColumnOverlapWidthM=nominal['columnOverlapWidthM'],columnOverlapWidthRangeM=[min(t['columnOverlapWidthM'] for t in tests),max(t['columnOverlapWidthM'] for t in tests)],nominalConditionalMasonryDeductionM2=nominal['conditionalMasonryDeductionM2'],conditionalDeductionRangeM2=[min(t['conditionalMasonryDeductionM2'] for t in tests),max(t['conditionalMasonryDeductionM2'] for t in tests)],sillM=sill,verticalFitFromAvailableData=verticalFit,joineryTareKN=None,lintelLoadsDefined=False,nativeApplied=False,conditionalOnly=True,scenarios=tests)
        openingrows.append(row);wallOpenings.append(row)
    deduction=sum(o['nominalConditionalMasonryDeductionM2'] for o in wallOpenings)
    complete=not unknown
    assert gross>=deduction-1e-6
    wallrows.append(dict(wallId=w['id'],wallName=w['name'],knownGrossMasonryAreaM2=gross if complete else None,partialKnownGrossAreaM2=gross,unknownHeightSegmentCount=len(unknown),conditionalOpeningDeductionM2=deduction,conditionalNetMasonryAreaM2=gross-deduction if complete else None,conditionalNetMasonryWeightKN=(gross-deduction)*surface if complete else None,grossMasonryWeightKN=gross*surface if complete else None,openingIds=[o['id'] for o in wallOpenings],netWeightExcludesJoineryLintelsFinishesOnConcrete=True,readyForNativeApplication=False))
assert len(openingrows)==11 and len({o['id'] for o in openingrows})==11
out.mkdir()
def write(n,v):(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write('R67-protegidos-R66.json',protected)
result=dict(revision='H03/R67',atUtc=datetime.now(timezone.utc).isoformat(),status='11 aberturas analisadas; massa liquida condicional, nao aplicada',sources=[dict(path=str(p),sha256=sha(p)) for p in paths],referenceGeometry='IFC R56 com preservacao da superestrutura verificada em R57; nao nova exportacao R67',areaWeightHypothesisKNm2=surface,openingCount=len(openingrows),walls=wallrows,openings=openingrows,nominalGeometricColumnOverlapOpeningIds=[o['id'] for o in openingrows if o['nominalColumnOverlapWidthM']>1e-6],possibleColumnOverlapUnderStudyUncertainty=[o['id'] for o in openingrows if o['columnOverlapWidthRangeM'][1]>1e-6],unknownWallIds=[w['wallId'] for w in wallrows if w['unknownHeightSegmentCount']],nativeEdited=False,loadsApplied=False,analyticalLoadPathVerified=False,fullBuildingMassCalculated=False,structuralApproval=False)
write('R67-aberturas-e-massas-condicionais.json',result)
table='\n'.join(f'| {o["id"]} | {o["wallId"]} | {o["nominalFullOpeningAreaM2"]:.3f} | {o["nominalColumnOverlapWidthM"]:.3f} | {o["columnOverlapWidthRangeM"][0]:.3f} a {o["columnOverlapWidthRangeM"][1]:.3f} |' for o in openingrows)
mass='\n'.join(f'| {w["wallId"]} | '+('pendente | pendente |' if w['knownGrossMasonryAreaM2'] is None else f'{w["knownGrossMasonryAreaM2"]:.4f} | {w["conditionalNetMasonryAreaM2"]:.4f} |') for w in wallrows)
(out/'LEIA-ME-R67.md').write_text(f'''# H03/R67 — aberturas e massa condicional das paredes superiores

ESTUDO NÃO APLICADO. NÃO EXECUTAR. Analisaram-se as 11 aberturas R34/R55 sobre os59 trechos R56 das20 paredes superiores. A geometria R56 teve preservação da superestrutura verificada em R57. Não se efetuou nova exportação ou edição de PRJ/RVT/DWG. A fonte não representa uma vistoria arquitetônica nova.

## Confronto com os pilares

| Abertura | Parede | Área nominal do vão (m²) | Sobreposição nominal com pilar em planta (m) | Faixa com translação de ±0,05m (m) |
|---|---|---:|---:|---:|
{table}

A sobreposição é uma interseção do intervalo horizontal de um vão aproximado com a caixa de um pilar que atravessa o pavimento. Trata-se de triagem geométrica, não prova de interferência executiva. A margem±0,05m foi herdada do estudo R34 e não é precisão de levantamento nem tolerância normativa. Os extremos da faixa incluem os pontos de quebra geométrica das interseções, não apenas duas amostras extremas. Confirmar faces e posição da abertura antes de alterar pilar ou vão. Não se deslocou nenhum apoio por esse diagnóstico.

Na porta S-P3-01, a leitura vetorial bruta tem largura aproximadamente0,60113m, enquanto a tabela especifica0,60m. Usou-se a largura nominal centralizada no intervalo lido para a análise condicional, preservando ambos os valores no JSON. Não se ocultou a discrepância nem se modificou a arquitetura. S-P3-01/W19 e S-P3-02/W18 continuam identificadores distintos.

## Área de alvenaria, ainda condicional

| Parede | Área bruta conhecida, sem trechos de pilares (m²) | Área líquida condicional de alvenaria (m²) |
|---|---:|---:|
{mass}

A diferença retira apenas a parcela geométrica do vão sobre o intervalo de alvenaria com altura conhecida. Não se desconta novamente uma abertura na parcela de pilar já excluída. A massa condicional multiplica a área por1,565kN/m², composição hipotética herdada da R55 para parede acabada de15cm. Esse coeficiente não foi confirmado por fabricante. Não se apresenta soma final da edificação: falta W08, paredes térreas, encontros, acabamentos sobre concreto e outras parcelas.

O cálculo de área de janela independe da altura do peitoril apenas se o vão couber integralmente na faixa de alvenaria. Os peitoris J1 permanecem desconhecidos e a verificação vertical correspondente é nula/desconhecida no JSON; não foram inventados. J2 tem peitoril de referência1,50m. As portas usam a hipótese de partir do piso, registrada pela checagem de altura. Tara de esquadrias, vergas/contravergas, arremates e transferência das cargas em torno das aberturas não estão incluídos. Por isso a diferença de massa não é redução liberada de carga estrutural, nem uma distribuição linear pronta para aplicar em cada viga.

Paredes apoiadas sobre laje e caminhos analíticos continuam exigindo análise própria. A massa global não permite substituir cargas locais junto aos vãos por uma carga uniforme sem justificar a distribuição. W08 permanece desconhecida, sem valor zero. A folga geométrica ao forro da R56 não foi convertida em aprovação de flecha ou compatibilização completa.

## Continuidade

Usar o diagnóstico para priorizar a confirmação de faces e das aberturas com sobreposição possível. Completar altura/base de W08, dados verticais J1, pesos de esquadrias e vergas; então preparar matriz local de cargas e aplicar a mesma hipótese aos dois ramos em novas cópias. Nenhuma ocorrência foi atribuída a defeito de transferência DWG/IFC. Não houve edição da monografia ou validação ELU/ELS. O tempo do script registrado mede somente execução computacional, não esforço total da IA, trabalho humano ou duração dos fluxos.
''',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name);ast.parse(Path(__file__).read_text(encoding='utf-8'))
write('R67-validacao.json',dict(openingCount=11,uniqueOpeningIds=True,wallPartitionLengthChecksPassed=True,sourceCADBIMBoundingBoxesEqual=True,protectedR66FilesChecked=len(protected),nativeApplicationPerformed=False,startedUtc=started,endUtc=datetime.now(timezone.utc).isoformat(),scriptElapsedSeconds=perf_counter()-tick,scriptDurationIsFlowTime=False))
write('R67-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file()]))
dest.mkdir()
for p in out.iterdir():shutil.copy2(p,dest/p.name);assert sha(p)==sha(dest/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
guide.write_text('''# Atualizacao R67 — diagnostico de aberturas, sem aplicacao

Analisadas11 aberturas em20 paredes/59trechos R56, com sensibilidade de posicao±5cm herdada R34. Areas e pesos liquidos condicionais de alvenaria calculados por parede; nao sao cargas liberadas e nao incluem tara/vergas/acabamentos sobre concreto. W08 continua desconhecida e J1 sem peitoril confirmado. Conferir sobreposicoes geometricas com pilares no relatorio antes de alterar apoios. Ler outputs/Paredes-H03-R67-ABERTURAS-NAO-APLICADO/LEIA-ME-R67.md. Ultimo nativo de engenharia permanece R64; R65Q nao aplicado, R66configuracao cancelada. Sem monografia/origens alteradas. NAO EXECUTAR.

---
Historico anterior:

'''+old,encoding='utf-8')
print(json.dumps(dict(status=result['status'],nominalColumnOverlaps=result['nominalGeometricColumnOverlapOpeningIds'],possibleColumnOverlaps=result['possibleColumnOverlapUnderStudyUncertainty'],unknownWalls=result['unknownWallIds']),ensure_ascii=False))

"""Ponto único de consulta dos resultados parciais, sem preencher resultados finais ausentes."""
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path

HERE=Path(__file__).parent
ROOT=HERE.parent
OUT=Path('D:/TCC/outputs/Resultados-H03-R128-PARCIAIS-NAO-EXECUTAR')
FILES={72:'R72-resultados-parciais.json',116:'R116-resultado.json',119:'R119-resultado.json',
       121:'R121-resultado.json',122:'R122-resultado.json',123:'R123-orientacao.json',
       124:'R124-resumo.json',125:'R125-resultado.json',126:'R126-resultado.json',127:'R127-resultado.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fmt(value):return f'{value:.2f}'.replace('.',',')
def duration(value):
    seconds=value/1000
    return f'{int(seconds//60)} min {seconds%60:06.3f} s'.replace('.',',')

def main():
    if OUT.exists():raise FileExistsError('Não substituir consolidação existente')
    sources=[];data={}
    for rev,name in FILES.items():
        p=ROOT/f'h03-r{rev}'/name
        sources.append({'revision':f'R{rev}','path':str(p),'sha256':sha(p)})
        data[rev]=json.loads(p.read_text(encoding='utf-8'))
    if data[121]['finalWallLoadApplicationAccepted'] or data[126]['loadsApplied']:
        raise ValueError('Estado das paredes mudou; reavaliar consolidação')
    if data[124]['finalRankingAllowed'] or data[127]['structuralSectionApproved']:
        raise ValueError('Estado de aceite mudou; reavaliar consolidação')
    initial=data[72]['initialTypedAvailability']
    den=sum(row['denominator'] for row in initial)
    native={b:sum(row[f'{b}_initialNative'] for row in initial) for b in ['CAD','BIM']}
    if den!=62 or native!={'CAD':0,'BIM':51}:raise ValueError('Denominador histórico diferente')
    slabs=data[119]['branches']
    if any(len(slabs[b]['readings'])!=11 for b in ['CAD','BIM']):raise ValueError('Leituras incompletas')
    pairs=sum(slabs['CAD']['readings'][i]['values'][k]==slabs['BIM']['readings'][i]['values'][k]
              for i in range(11) for k in ['QkNm2','G2kNm2','thicknessCm','elevationCm'])
    if pairs!=44:raise ValueError('Lajes divergentes; não publicar igualdade')
    summary={rev:{b:data[rev]['branches'][b]['summary']['verticalLoadsDisplayedTf'] for b in ['CAD','BIM']} for rev in [116,121]}
    if any(summary[rev]['CAD']!=summary[rev]['BIM'] for rev in [116,121]):raise ValueError('Cargas verticais divergentes')
    new_times=[{'revision':'R125','branch':'BIM','purpose':'Consulta de unidades: segmento retomado',**data[125]['timing']},
               {'revision':'R126','branch':'CAD','purpose':'Tentativa de delimitação não aceita',**data[126]['timing']},
               *[{'revision':'R127','branch':b,'purpose':'Consulta da seção do apoio W17',**data[127]['times'][b]} for b in ['CAD','BIM']]]
    pending=[
      {'id':'F01','task':'Delimitar ações nas faixas reais de paredes','status':'pendente','evidence':'R122/R126','doneWhen':'Extremos e intensidade preservados após salvar/reabrir e conferidos na representação analítica dos dois ramos.'},
      {'id':'F02','task':'Completar paredes, aberturas, vergas e caminho de carga W08','status':'parcial','evidence':'R120/R127','doneWhen':'Todas as parcelas e apoios definidos, lançados e relidos sem duplicar concreto ou cargas existentes.'},
      {'id':'F03','task':'Resolver reservatório de 1.000 L, posição/base/acesso e cargas cheio/vazio','status':'pendente','evidence':'R112/R113','doneWhen':'Compatibilização física e apoio definidos com pesos documentados e casos nativos verificados.'},
      {'id':'F04','task':'Completar escada, guarda-corpo e cargas remanescentes','status':'pendente','evidence':'Matriz de fechamento R72','doneWhen':'Modelo/reação documentados e parcelas aplicadas sem duplicar ações de lajes.'},
      {'id':'F05','task':'Validar vento local, manutenção localizada e conjunto completo de combinações','status':'parcial','evidence':'Registros de ações e análises parciais; não encerrados pela R128','doneWhen':'Parâmetros e todos os casos/combinações justificados e conferidos nos dois receptores.'},
      {'id':'F06','task':'Concluir ELU/ELS e revisar seções preservando alturas arquitetônicas','status':'pendente','evidence':'R116/R121/R127','doneWhen':'Entradas completas, esforços/resistência/flechas/fissuração/estabilidade verificados e revisões relidas.'},
      {'id':'F07','task':'Sincronizar Revit/AutoCAD com a hipótese técnica aceita','status':'pendente','evidence':'Autoria e receptores em checkpoints distintos','doneWhen':'Nova transferência de fontes congeladas, com geometria/propriedades e ocorrências auditadas.'},
      {'id':'F08','task':'Executar comparação prospectiva de tempos e fechar pacote de resultados','status':'pendente','evidence':'R124 mais intervalos R125–R127','doneWhen':'Mesmo escopo inicial/final, pausas e esforço humano/IA/interface registrados; tabelas finais vinculadas às evidências.'}]
    result={'revision':'H03/R128','createdAtUtc':datetime.now(timezone.utc).isoformat(),
      'scope':'Síntese rastreável de checkpoints históricos e consultas recentes; não é nova importação, cálculo, atualização de fontes ou edição da monografia.',
      'sources':sources,'initialTypedAvailabilityHistoricalR45R46':{'rows':initial,'denominator':den,'native':native,
        'percent':{b:100*n/den for b,n in native.items()},'BIMInputTreatment':data[72]['bimInputTreatment'],
        'complementedLogicalUnits':data[72]['complementedLogicalElements'],'notDefectOrInterfaceActionCount':True},
      'currentChecks':{'slabPairedFieldsR119':pairs,'exportGeometryR122':data[122]['geometryOnlyComparison'],
        'orientationR123':{k:v['counts'] for k,v in data[123]['models'].items()},'W17R127':data[127]['readings']},
      'partialVerticalSummariesTf':summary,
      'wallExperiment':{'acceptedAsFinal':False,'R122Representation':data[122]['reconciliation'],
        'R125ObservedDisplayRatio':data[125]['observedDisplayedRatioKgfPerKN'],
        'R126AttemptAccepted':data[126]['partialWallLoadRepresentationAccepted'],
        'BIMNodeAttemptPerformedInR126':data[126]['BIMAttempted']},
      'timingSnapshotR124':{k:data[124][k] for k in ['files','counts','overlappingPairs','fullFlowTotals','isolatedAIWorkOnMainBuilding']},
      'additionalMeasuredIntervalsAfterR124':new_times,'noSumOfExploratoryHistory':True,
      'pendingWorkstreams':pending,'closedFinalFlow':False,'structuralApproval':False,'finalRankingAllowed':False,
      'isolatedAIEffort':{'inferenceSeconds':None,'tokens':None,'cost':None},
      'humanAndAIContribution':{'AI':'Programação, preparação/auditoria de artefatos, pesquisa técnica, operação de interface e registro; sem inferir tempo isolado ou tokens.',
        'human':'Premissas e decisões registradas sobre escopo, materiais, arquitetura, cobertura/reservatório e intervenções nos aplicativos; tempo ativo não reconstruído retrospectivamente.'},
      'notExecutedInThisConsolidation':['Importação','Cálculo estrutural','Edição de RVT/DWG/PRJ','Edição da monografia','Atualização do banco central de tempos']}
    initial_rows='\n'.join(f"| {r['element'].replace('logica','lógica')} | {r['denominator']} | {r['CAD_initialNative']} | {r['BIM_initialNative']} |" for r in initial)
    vertical_rows='\n'.join(f"| {rev} | {fmt(summary[rev]['CAD']['Adicional'])} | {fmt(summary[rev]['CAD']['Total'])} |" for rev in [116,121])
    time_rows='\n'.join(f"| {r['revision']} | {r['branch']} | {r['purpose']} | {duration(r['durationMs'])} |" for r in new_times)
    pending_rows='\n'.join(f"| {r['id']} | {r['task']} | {r['status']} | {r['doneWhen']} |" for r in pending)
    md=f'''# H03/R128 — resultados parciais e roteiro de fechamento

Esta síntese reúne evidências verificadas, sem alterar a monografia ou os modelos. O estudo permanece parcial e sem dimensionamento final aprovado. As diferenças de unidades lógicas, sólidos e barras analíticas são mantidas; nenhuma contagem vira automaticamente número de erros ou ações de interface.

## Chegada inicial ao Eberick — evidência histórica R45/R46, consolidada na R72

| Unidade lógica | Proposta comum | CAD nativo inicial | BIM nativo inicial |
|---|---:|---:|---:|
{initial_rows}

Havia 0/62 unidades tipadas no CAD e 51/62 no BIM (82,26%). O CAD preservou 62/62 contornos e 66/66 conteúdos textuais, como referência gráfica. A reconstrução posterior abrangeu 62 unidades no CAD e 11 no BIM. Esses números são unidades lógicas complementadas, não operações de interface, correções ou defeitos. O fluxo BIM incluiu tratamento explícito de 17 registros de geometria nominal e retirada de 2 pavimentos vazios; esse esforço permanece parte do fluxo.

## Conferências posteriores

R119: 11 lajes por ramo, 44 campos pareados iguais (cargas Q/G2, espessura e elevação). R122: coordenadas e conexões geométricas coincidem no pórtico e nas grelhas exportadas. R123: há inversão da ordem I/J em 68 pares únicos do pórtico, 76 da grelha N1 e 159 da N2; isso não é contagem de erros nem prova da causa da direção relativa Y−/Y+. Propriedades/cargas locais não foram transformadas para declarar equivalência mecânica completa.

R127: apoio W17, CAD V14/BIM V2, com seção de 20 × 16 cm, elevação 0 e carga de parede/soma extra exibidas 0. A seção coincide, mas sua capacidade sob o conjunto completo de ações não foi aprovada. A opção de edição “Manter seção constante” difere visualmente e foi preservada.

## Análise parcial e ensaio de parede

| Revisão | Adicional exibido, ambos ramos (tf) | Total vertical exibido, ambos ramos (tf) |
|---|---:|---:|
{vertical_rows}

A R116 é a referência parcial anterior. A R121 é um ensaio da W03 não aceito como lançamento definitivo. O aumento exibido de 1,95 tf é coerente com 1,9536 tf na exportação R122, que aplica a carga em 4,40 m entre eixos; a faixa livre tem 4,20 m. A consulta R125 confirmou 444 kgf/m ↔ 4,44 kN/m na exibição nativa, sem editar a carga, e restaurou a unidade original. Isso identifica a convenção observada, sem afirmar conversão SI exata ou calibração universal.

Na R126, tentativas de nós junto à face do pilar foram recusadas; um controle no meio do vão foi descartado ao fechar sem salvar. Não houve aplicação de carga ou tentativa BIM equivalente. A delimitação continua pendente. Não se adotou a intensidade reduzida ou a viga inteira para forçar igualdade do resumo.

O Gama-Z X+ exibido na R121 chegou a 1,10, igual ao limite mostrado. Valor arredondado no limite não é aprovação. Permanecem a indicação relativa CAD Y−/BIM Y+ e a necessidade de esclarecer sua causa. As análises parciais não abrangem resistência completa, flechas de lajes, fissuração e todos os carregamentos.

## Tempos e esforço

O inventário R124 reúne 203 candidatos: 162 com duração, 26 sem duração principal e 15 contêineres, com 23 pares sobrepostos. É a fotografia até aquela revisão. A tabela abaixo acrescenta quatro intervalos observados posteriormente, sem refazer a contagem de candidatos ou somar o histórico:

| Revisão | Ramo | Escopo | Intervalo observado |
|---|---|---|---:|
{time_rows}

Os intervalos incluem navegação, leitura, pesquisa, erro de interface ou evidências, conforme cada JSON. A retomada R125 exclui a consulta preliminar e espera da ajuda. A tentativa R126 não foi concluída como lançamento e não possui medição BIM correspondente. As consultas R127 tiveram caminhos de seleção distintos. Não sustentam ranking, tempo final de fluxo ou economia percentual. Intervalos de processamento contidos nas sessões não são somados novamente.

A atuação da IA compreende código, artefatos, pesquisa, operação e auditoria. A intervenção humana compreende premissas, decisões e ações registradas nos aplicativos. Tempo ativo humano, inferência isolada, tokens e custo não foram reconstruídos por quantidade de mensagens ou arquivos. **Tempo final CAD/BIM, esforço isolado da IA e ranking continuam desconhecidos.**

## Frentes para fechar o estudo

| ID | Frente | Estado | Critério para encerrar |
|---|---|---|---|
{pending_rows}

As oito frentes são agrupamentos de trabalho, não erros por ramo. Uma conferência parcial concluída não encerra toda a frente. Fundações permanecem fora do escopo pela ausência de sondagem; apoios idealizados devem continuar explicitados.

O JSON conserva os hashes das fontes e os limites. Não se executou nova importação, cálculo, alteração de arquivos nativos ou edição acadêmica nesta consolidação. Saída local: `{OUT}`.
'''
    for row in sources:
        if sha(Path(row['path']))!=row['sha256']:raise ValueError('Fonte alterada durante consolidação')
    OUT.mkdir()
    (OUT/'R128-resultados-parciais.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'LEIA-ME-R128.md').write_text(md,encoding='utf-8')
    print(json.dumps({'sourcesVerified':len(sources),'newIntervals':len(new_times),'pendingWorkstreams':len(pending),'finalRankingAllowed':False}))

if __name__=='__main__':main()

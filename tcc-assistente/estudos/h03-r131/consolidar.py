"""Consolida análise W15 preservando arredondamentos, avisos e divergências."""
import importlib.util
import json
import shutil
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Analise-W15-H03-R131-ESTUDO-NAO-EXECUTAR')
spec=importlib.util.spec_from_file_location('r116',HERE.parent/'h03-r116/consolidar.py')
r116=importlib.util.module_from_spec(spec)
spec.loader.exec_module(r116)
sha=r116.sha

def main():
    if (OUT/'R131-resultado.json').exists():raise FileExistsError('Resultado existente')
    prep=json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected=[]
    for row in prep['files']:
        digest=sha(Path(row['source']))
        if digest!=row['sha256Before']:raise ValueError('Fonte R130 alterada')
        protected.append({'path':row['source'],'sha256':digest})
    baselinepath=HERE.parent/'h03-r116/R116-resultado.json'
    baseline=json.loads(baselinepath.read_text(encoding='utf-8'))
    inputpath=HERE.parent/'h03-r130/R130-resultado.json'
    inputdata=json.loads(inputpath.read_text(encoding='utf-8'))
    expected=Decimal(str(inputdata['wallReference']['forceMagnitudeKN']))/Decimal(10)
    branches={}
    frozen=OUT/'congelados-apos-processamento'
    if frozen.exists():raise FileExistsError(frozen)
    for b,prefix in [('CAD','46'),('BIM','47')]:
        name=f'{prefix}-H03-R131-{b}-W15-ANALISE-NAO-EXECUTAR'
        text=(OUT/f'{b}-resumo-analise-UI.txt').read_text(encoding='utf-8')
        status=(OUT/f'{b}-processamento-estado-UI.txt').read_text(encoding='utf-8')
        if name not in text or name not in status or 'Estrutura processada com avisos' not in status:
            raise ValueError('Projeto ou conclusão sem comprovação')
        summary=r116.extract(text)
        session=json.loads((OUT/f'{b}-sessao-tempo.json').read_text(encoding='utf-8'))
        command=json.loads((OUT/f'{b}-processamento-tempo.json').read_text(encoding='utf-8'))
        r116.check_time(session,command)
        prev=baseline['branches'][b]['summary']['verticalLoadsDisplayedTf']
        delta={k:float(Decimal(str(v))-Decimal(str(prev[k]))) for k,v in summary['verticalLoadsDisplayedTf'].items()}
        # Cada resumo tem duas casas: diferença de dois arredondamentos tem erro até 0,01 tf.
        coherent={k:abs(Decimal(str(delta[k]))-expected)<=Decimal('0.01') for k in ['Adicional','Total']}
        if not all(coherent.values()):raise ValueError('Acréscimo incompatível com intervalo de arredondamento')
        source=OUT.parent/name
        prjs=list((source/'Projeto Eberick').glob('*.prj'))
        if len(prjs)!=1:raise ValueError('PRJ ambíguo')
        shutil.copytree(source,frozen/b)
        files=[{'path':p.relative_to(source).as_posix(),'sha256':sha(p)} for p in sorted(source.rglob('*')) if p.is_file()]
        if not all(sha(frozen/b/r['path'])==r['sha256'] for r in files):raise ValueError('Cópia congelada divergente')
        branches[b]={'projectPath':str(prjs[0]),'projectSha256':sha(prjs[0]),'summary':summary,
          'deltaDisplayedVerticalTfFromR116':delta,'incrementCompatibleWithDisplayRounding':coherent,
          'sessionTime':session,'processingTimeObservation':command,'frozenFiles':files}
    cad,bim=[branches[b]['summary'] for b in ['CAD','BIM']]
    diffs=[]
    for case,fields in cad['topDisplacementsRawUnitNotExplicit'].items():
        for key,a in fields.items():
            v=bim['topDisplacementsRawUnitNotExplicit'][case][key]
            if a!=v:diffs.append({'case':case,'field':key,'CAD':a,'BIM':v,'deltaBIMminusCAD':round(v-a,6)})
    comparison={**r116.r111.r106.comparison(cad,bim),
      'verticalDisplayedValuesEqual':cad['verticalLoadsDisplayedTf']==bim['verticalLoadsDisplayedTf'],
      'gammaZDisplayedValuesAndLimitsEqual':cad['gammaZDisplayed']==bim['gammaZDisplayed'],
      'topDisplayedDifferences':diffs}
    result={'revision':'H03/R131','createdAtUtc':datetime.now(timezone.utc).isoformat(),
      'scope':'Sensibilidade isolada W15 em cópias R130 derivadas R116: estática e ELS-DEF do pórtico com rigidez configurada.',
      'branches':branches,'comparison':comparison,'protectedR130Files':protected,'sourceFilesUnchanged':True,
      'baselineR116':{'path':str(baselinepath),'sha256':sha(baselinepath)},
      'inputR130':{'path':str(inputpath),'sha256':sha(inputpath)},
      'incrementCheck':{'wallHypothesisForceKN':4.46025,'expectedDisplayedTfUnderObservedR125Convention':float(expected),
        'observedDisplayConventionKNPerTf':10,'differenceOfTwoRoundedNumbersErrorBoundTf':0.01,
        'exactSIConversionOrFullEquilibriumAudit':False},
      'processingPerformed':True,'dimensioningPerformed':False,'slabDeflectionPerformed':False,
      'crackedStiffnessCalculationPerformed':False,'finalWallLoadSetCompleted':False,
      'analyticalSlabLoadDistributionIndividuallyVerified':False,'finalStructuralApproval':False,
      'finalProductivityRankingAllowed':False,'monographEdited':False,
      'nextStep':'Conferir a distribuição local da W15 e aplicar demais parcelas em checkpoints pareados, mantendo W03 e outras pendências explicitadas.'}
    (OUT/'R131-resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    rows='\n'.join(f"| {b} | {v['sessionTime']['wallMs']/60000:.3f} min | {v['processingTimeObservation']['durationMs']/1000:.3f} s |" for b,v in branches.items())
    (OUT/'LEIA-ME-R131.md').write_text(f'''# H03/R131 — análise isolada com a linha W15

Processaram-se cópias CAD 46 e BIM 47, derivadas da R130. A única nova parcela em relação à referência R116 é a linha W15, 4,695 kN/m por 0,95 m, na laje L4/N1. O ensaio W03 em toda a viga da R121 não foi incorporado.

| Parcela exibida | CAD | BIM |
|---|---:|---:|
| Peso próprio | 75,69 tf | 75,69 tf |
| Adicional | 11,00 tf | 11,00 tf |
| Acidental | 17,11 tf | 17,11 tf |
| Q_TELHADO_MANUTENCAO | 1,78 tf | 1,78 tf |
| Total | 105,59 tf | 105,59 tf |

Ante a própria R116, o total exibido aumentou 0,45 tf e a ação Adicional aumentou 0,44 tf. Essa diferença de 0,01 tf entre os deltas é conservada: os dois resumos são arredondados. A integral nominal é 4,46025 kN; pela convenção de exibição observada R125, o acréscimo esperado é 0,446025 tf. Ambos os deltas cabem no intervalo de erro de até 0,01 tf da subtração de duas leituras com duas casas. Isso não é conversão SI exata nem auditoria completa de equilíbrio ou das reações locais.

**Ambos terminaram com avisos**, inclusive relação de carga por área não usual para edifícios. Não se considerou esse aviso resolvido por concluir a análise. As demais cargas da edificação continuam incompletas.

Os deslocamentos horizontais exibidos permanecem 0,20 cm nas quatro direções; o relativo é 0,17 cm. A direção relativa continua CAD N1/Y− e BIM TCC-cdd31967-N1/Y+. Gama-Z exibido: 1,09 X+; 1,08 X−; 1,06 Y+; 1,05 Y−. Limites mostrados no software não representam aprovação normativa.

No acréscimo percentual de topo por Desaprumo X+, registrou-se CAD 14,41% e BIM 14,40%, diferença −0,01 ponto percentual. Os outros campos de topo comparados coincidem na precisão exibida. Não se comprovou a causa ou um defeito de transferência.

| Ramo | Sessão observada | Comando até observação do término |
|---|---:|---:|
{rows}

O intervalo do comando está contido na sessão e não deve ser somado novamente. Inclui espera e latência de captura; não mede solver isolado, inferência da IA ou produtividade final. A navegação e o aprendizado diferem entre sessões. Tempos finais CAD/BIM e ranking continuam abertos.

Executou-se estática linear e ELS-DEF do pórtico com rigidez configurada. Não houve dimensionamento, flechas de lajes, cálculo de rigidez fissurada ou análise dinâmica. A distribuição local da linha na grelha e as reações individuais ainda não foram auditadas. A etapa não encerra ELU/ELS nem aprova seções.

Preservaram-se {len(protected)} arquivos das fontes R130 e congelaram-se os arquivos calculados, com hashes verificados, em `congelados-apos-processamento/CAD` e `BIM`, neste diretório local. Monografia e arquivos de autoria Revit/AutoCAD não foram alterados.
''',encoding='utf-8')
    print(json.dumps({'comparison':comparison,'protectedSources':len(protected),'frozen':{b:len(v['frozenFiles']) for b,v in branches.items()}}))

if __name__=='__main__':main()

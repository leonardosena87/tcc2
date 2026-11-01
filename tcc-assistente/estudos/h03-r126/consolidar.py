"""Registra tentativa não aceita; não promove controle de interface a solução estrutural."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Trecho-W03-H03-R126-ESTUDO-NAO-EXECUTAR')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if (OUT/'R126-resultado.json').exists():raise FileExistsError('Resultado existente')
    prep=json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    sources=[];prjs=[]
    for r in prep['files']:
        after=sha(Path(r['source']))
        if after!=r['sha256Before']:raise ValueError('Fonte R116 alterada')
        sources.append({'path':r['source'],'sha256':after})
        if r['copy'].endswith('.prj'):
            copied=sha(Path(r['copy']))
            if copied!=r['sha256Before']:raise ValueError('Nó de controle foi gravado ou PRJ alterado')
            prjs.append({'branch':r['branch'],'path':r['copy'],'sha256':copied,'unchangedSincePreparation':True})
    messages=[]
    for file,typed in [('CAD-no-limite-mensagem-existente-UI.txt','10,705'),('CAD-no-teste-10p1-mensagem-existente-UI.txt','10.1,705')]:
        text=(OUT/file).read_text(encoding='utf-8')
        if '40-H03-R126-CAD' not in text or 'Já existe um nó nesta posição no pavimento.' not in text:
            raise ValueError('Mensagem ou projeto não comprovados')
        if 'Value: '+typed not in text:raise ValueError('Coordenada não conservada')
        messages.append({'typedCoordinateText':typed,'message':'Já existe um nó nesta posição no pavimento.','evidence':file})
    result={'revision':'H03/R126','createdAtUtc':datetime.now(timezone.utc).isoformat(),
      'scope':'Tentativa exploratória no CAD de delimitar a carga W03; controle em memória descartado ao fechar sem salvar.',
      'protectedR116Files':sources,'copyPrjs':prjs,'sourceFilesUnchanged':True,
      'CADAttempted':True,'BIMAttempted':False,'messages':messages,
      'midspanControl':{'typedCoordinateText':'220,705','newDivisionVisibleInCroqui':True,
                        'exactRetainedNodePositionIndependentlyVerified':False,'saved':False},
      'inputObservations':['Uma tentativa de clique por índice UIA retornou elemento indisponível.',
        'Entrada por type_text não apareceu em tentativas de coordenadas; usou-se digitação direta por teclas com releitura.',
        'Dois cliques em controles visíveis da barra de captura foram ensaiados; não se comprovou o estado efetivo dessas opções ou a causa da recusa.',
        'O texto de comando Nó-Centro não foi interpretado como prova de uma opção de captura ativa.'],
      'loadsApplied':False,'partialWallLoadRepresentationAccepted':False,'processingPerformed':False,
      'controlDiscardedByClosingWithoutSaving':True,'modelEditPersisted':False,'monographEdited':False,
      'normativeValidationPerformed':False,'finalProductivityRankingAllowed':False,
      'timing':json.loads((OUT/'CAD-tentativa-tempo.json').read_text(encoding='utf-8')),
      'technicalSource':'https://suporte.altoqi.com.br/hc/pt-br/articles/360046158854',
      'nextStep':'Pular ampliação das paredes dependente desta delimitação e conferir a seção nativa do apoio W17; retomar nós sem remover vínculos de pilares ou inventar tolerância.'}
    (OUT/'R126-resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'protectedFiles':len(sources),'prjsUnchanged':len(prjs),'wallLoadApplied':False,'BIMAttempted':False}))

if __name__=='__main__':main()

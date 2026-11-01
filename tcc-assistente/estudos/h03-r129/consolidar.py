"""Conserva tentativa de captura sem convertê-la em lançamento aceito."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('D:/TCC/outputs/Faixa-W03-H03-R129-ESTUDO-NAO-EXECUTAR')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    target = OUT / 'R129-resultado.json'
    if target.exists():
        raise FileExistsError(target)
    prep = json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    sources, copies = [], []
    for row in prep['files']:
        digest = sha(row['source'])
        if digest != row['sha256Before']:
            raise ValueError('Fonte R116 alterada')
        sources.append({'path': row['source'], 'sha256': digest})
        if row['copy'].endswith('.prj'):
            if sha(row['copy']) != digest:
                raise ValueError('PRJ experimental alterado')
            copies.append({'branch':row['branch'],'path':row['copy'],'sha256':digest})
    evidence = []
    for name in ['CAD-no-ampliado-recusa-UI.txt','CAD-no-captura-alterada-resposta-UI.txt']:
        text = (OUT/name).read_text(encoding='utf-8')
        if not all(s in text for s in ['42-H03-R129-CAD','Já existe um nó nesta posição no pavimento.','Value: 10,705']):
            raise ValueError('Resposta ou coordenada sem evidência')
        evidence.append(name)
    timing = json.loads((OUT/'CAD-tempo-sessao.json').read_text(encoding='utf-8'))
    result = {'revision':'H03/R129','createdAtUtc':datetime.now(timezone.utc).isoformat(),
      'scope':'Tentativas CAD de inserir limite W03 em vista ampliada e após clique no controle de captura; fechadas sem salvar.',
      'sourceFiles':sources,'copyPrjs':copies,'sourceFilesUnchanged':True,'copyPrjsUnchanged':True,
      'CADAttempted':True,'BIMAttempted':False,'typedCoordinateText':'10,705','evidence':evidence,
      'observedMessage':'Já existe um nó nesta posição no pavimento.',
      'effectiveCaptureStateIndependentlyVerified':False,'causeOfRejectionProven':False,
      'loadsApplied':False,'processingPerformed':False,'partialWallLoadAccepted':False,
      'saved':False,'closedWithoutSaving':True,'monographEdited':False,'timing':timing,
      'finalProductivityRankingAllowed':False,
      'nextStep':'Ensaiar linha de parede W15 sobre laje em cópias independentes, sem ampliar a carga W03 ao eixo dos pilares.'}
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    minutes=timing['duracao_ms']/60000
    (OUT/'LEIA-ME-R129.md').write_text(f'''# H03/R129 — tentativa de faixa W03

Em cópia CAD derivada da R116, ampliou-se a região do pilar e digitou-se o limite `10,705` cm. O aplicativo recusou a inserção com a mensagem de nó existente. Após um clique no controle de captura, sem comprovação independente do estado efetivo dessa opção, a mesma coordenada recebeu a mesma resposta. A causa da recusa continua desconhecida.

Não houve aplicação de carga, processamento ou tentativa BIM. A cópia foi fechada sem salvar. Os hashes de {len(sources)} arquivos de referência e dos dois PRJs de cópias foram preservados. Nenhuma alteração da monografia.

Sessão CAD: {minutes:.3f} min, com navegação, ampliação, tentativas, pesquisa e capturas; não é tempo puro de processamento nem comparação controlada CAD/BIM. Não somar a tempos que a contenham.

O ensaio W03 em toda a viga da R121 continua sem aceite como carga definitiva. A próxima frente independente é a parede W15 sobre laje. Não se retirou conexão de pilar nem se ajustou artificialmente a intensidade para compensar o comprimento.
''',encoding='utf-8')
    print(json.dumps({'protectedFiles':len(sources),'copyPrjsUnchanged':len(copies),'loadsApplied':False}))

if __name__=='__main__':
    main()

"""Audita persistência e extensão gráfica W20; não calcula a estrutura."""
import hashlib
import importlib.util
import json
import re
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

HERE = Path(__file__).parent
OUT = Path('D:/TCC/outputs/Linha-W20-H03-R135-ESTUDO-NAO-EXECUTAR')
spec = importlib.util.spec_from_file_location('r130dxf', HERE.parent/'h03-r130/ler_dxf.py')
dxf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dxf)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def geometry(path):
    row = dxf.wall_line(path)
    es = dxf.entities(path)
    centers = [tuple(D(dxf.one(e,c)) for c in [10,20]) for e in es
               if dxf.values(e,8) == ['CR-Pilares'] and dxf.one(e,0) == 'CIRCLE']
    anchors = [(D(0),D(0)),(D('8.8'),D('14.1')),(D('19.3'),D('7.8'))]
    eps = D('1e-9')
    for anchor in anchors:
        if sum(max(abs(a-b) for a,b in zip(anchor,p)) <= eps for p in centers) != 1:
            raise ValueError('Escala/origem sem três âncoras únicas')
    start = [D(v)*50 for v in row['startRaw']]
    end = [D(v)*50 for v in row['endRaw']]
    if any(abs(a-b) > eps*50 for a,b in zip(start,[810,10,0])) or any(
            abs(a-b) > eps*50 for a,b in zip(end,[810,380,0])):
        raise ValueError('Extremos W20 diferentes do intervalo previsto')
    if row['label'] != '4.71':
        raise ValueError('Rótulo gráfico inesperado')
    return {**row,'startModelCm':[str(v) for v in start],
            'endModelCm':[str(v) for v in end],
            'lengthM':str(((end[0]-start[0])**2+(end[1]-start[1])**2).sqrt()/100),
            'plotScale':50,'anchorModelCm':[[0,0],[440,705],[965,390]],
            'rawTolerance':str(eps),'zIsDrawingPlaneNotPhysicalLevel':True}


def readback(text, branch):
    if f'R135-{branch}-W20' not in text or not re.search(
            r'Carga extra Value: 4\.71065\b',text) or 'text 0.00 kN/m' not in text:
        raise ValueError('Releitura nativa insuficiente ou de outra cópia')
    return {'extraKNm':'4.71065','wallKNm':'0','method':'Texto nativo de acessibilidade após reabrir, com imagem correspondente'}


def main():
    target = OUT/'R135-resultado.json'
    if target.exists():
        raise FileExistsError(target)
    prep = json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected = []
    for r in prep['files']:
        digest = sha(r['source'])
        if digest != r['sha256Before']:
            raise ValueError('Fonte R116 alterada')
        protected.append({'path':r['source'],'sha256':digest})
    matrixpath = HERE.parent/'h03-r120/R120-matriz.json'
    matrix = json.loads(matrixpath.read_text(encoding='utf-8'))
    seg = next(s for s in matrix['segments'] if s['segmentId']=='R120-S58')
    if seg['wallId']!='W20' or seg['route']!='laje' or seg['openingDeductions']:
        raise ValueError('Premissa de referência mudou')
    branches = {}
    for b in ['CAD','BIM']:
        r = next(r for r in prep['files'] if r['branch']==b and r['copy'].endswith('.prj'))
        saved = json.loads((OUT/f'{b}-prj-salvo-hash.json').read_text(encoding='utf-8'))
        if sha(r['copy']) != saved['sha256'] or saved['sha256'] == r['sha256Before']:
            raise ValueError('PRJ não preserva lançamento salvo durante consultas')
        native = readback((OUT/f'{b}-recuperado-W20-UI.txt').read_text(encoding='utf-8'),b)
        graphic = OUT/f'{b}-N1-W20-reaberto.dxf'
        branches[b] = {'project':r['copy'],'projectSha256':sha(r['copy']),
            'nativeReadback':native,'drawing':geometry(graphic),'drawingSha256':sha(graphic),
            'session':json.loads((OUT/f'{b}-tempo-sessao.json').read_text(encoding='utf-8')),
            'actionGridVisual':{'Adicional':'4.71','Solo':'0.00','Acidental':'0.00','Agua':'0.00',
                'Subpressao':'0.00','Q_TELHADO_MANUTENCAO':'0.00',
                'method':'Transcrição visual pela IA; duas casas, distinta da releitura textual exata'},
            'readbackDidNotChangeSavedProject':True}
    # Quarentena é rastreabilidade do erro de captura, nunca evidência da tela nomeada.
    invalid = [{'path':p.name,'sha256':sha(p)} for p in sorted((OUT/'capturas-invalidas-repetidas').iterdir())]
    result = {'revision':'H03/R135','createdAtUtc':datetime.now(timezone.utc).isoformat(),
        'scope':'W20/S58 isolada sobre L3/N1 em cópias R116, sem W15 ou ensaio W03',
        'reference':{'path':str(matrixpath),'sha256':sha(matrixpath),'segment':seg,
            'geometry':'R56/R57 histórica; sem nova exportação de autoria nesta etapa',
            'loadHypothesisKNm':'4.71065','lineLengthM':'3.70','integralMagnitudeKN':'17.429405',
            'compositionKNm2':'1.565','heightM':'3.01','manufacturerConfirmed':False,
            'currentUpperSoffitRevalidated':False},
        'protectedR116Files':protected,'sourceFilesUnchanged':True,'branches':branches,
        'nativeInputPersistenceVerified':True,'graphicalExtentVerified':True,
        'pairedNativeExtraAndWallEqual':True,'processingPerformed':False,
        'analyticalLoadDistributionVerified':False,'structuralApproval':False,
        'finalWallLoadSetCompleted':False,'finalProductivityRankingAllowed':False,
        'monographEdited':False,'authorshipRVTorDWGEdited':False,
        'captureRecovery':{'invalidFiles':invalid,'invalidCount':len(invalid),
            'reason':'Função de salvamento reteve estado antigo por fechamento léxico entre células; 24 grupos repetiram imagem inicial.',
            'fix':'Estado observado passado explicitamente; novas capturas de croqui, intensidade e ações em ambos os ramos.',
            'initialInputScreenshotsRecovered':False,
            'slabPropertiesInitialLiveInspection':'Maciça, ambiente Externo, h14cm, elevação0, Q1.5 e revestimento1 nos dois ramos; imagem inicial inválida não comprova essa leitura.',
            'slabPropertiesRecovery':'Não recuperada: seleção do rótulo BIM sobreposto à carga abriu a linha; sem alteração.',
            'time':json.loads((OUT/'recuperacao-capturas-tempo.json').read_text(encoding='utf-8'))},
        'timingLimit':'Sessões exploratórias distintas, incluem raciocínio e interface; recuperação separada. Sem inferência IA, tokens, custos ou total final conhecido.',
        'nextStep':'Processar cópias derivadas, comparar a grelha e distribuição contra controle de mesma malha; verificar integral, momentos e caminho de carga antes de aceitação.',
        'technicalProcedure':'https://suporte.altoqi.com.br/hc/pt-br/articles/360058309854'}
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'protected':len(protected),'nativeKNm':'4.71065','lengthM':branches['CAD']['drawing']['lengthM'],
        'sessionsMin':{b:branches[b]['session']['duracao_ms']/60000 for b in branches},
        'captureRecoveryMin':result['captureRecovery']['time']['duracao_ms']/60000}))


if __name__=='__main__':
    main()

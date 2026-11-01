"""Confronta releitura nativa e geometria gráfica da W15 nas cópias pareadas."""
import hashlib
import json
import re
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
from ler_dxf import entities,values,one,wall_line

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Linha-W15-H03-R130-ESTUDO-NAO-EXECUTAR')
D=Decimal

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def drawing(path):
    row=wall_line(path)
    centers=[tuple(D(one(e,c)) for c in [10,20]) for e in entities(path)
             if values(e,8)==['CR-Pilares'] and one(e,0)=='CIRCLE']
    # Escala gráfica 1:50: centímetros do modelo / 50 = unidade do DXF.
    # Três eixos conhecidos conferem escala e origem; epsilon só para resíduos de escrita.
    anchors=[(D(0),D(0)),(D('8.8'),D('14.1')),(D('19.3'),D('7.8'))]
    if not all(sum(max(abs(a-b) for a,b in zip(anchor,center))<=D('1e-9') for center in centers)==1 for anchor in anchors):
        raise ValueError('Âncoras gráficas não confirmam escala/origem esperadas')
    start=[D(v)*50 for v in row['startRaw']]
    end=[D(v)*50 for v in row['endRaw']]
    if start!=[450,495,0] or end!=[545,495,0] or row['label']!='4.70':
        raise ValueError('Faixa W15 ou rótulo diferente do previsto')
    return {**row,'startModelXYCm':[float(v) for v in start[:2]],
      'endModelXYCm':[float(v) for v in end[:2]],'lengthM':float((end[0]-start[0])/100),
      'plotScale':50,'rawUnitPerModelCm':0.02,'anchorToleranceRawUnits':1e-9,
      'anchorModelXYCm':[[0,0],[440,705],[965,390]],'checkedAnchors':3,
      'rawZIsDrawingPlaneNotBuildingLevel':True,'analyticalLoadDistributionVerified':False}

def main():
    if (OUT/'R130-resultado.json').exists():raise FileExistsError('Resultado existente')
    prep=json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected=[];copies={}
    for row in prep['files']:
        digest=sha(row['source'])
        if digest!=row['sha256Before']:raise ValueError('Fonte R116 alterada')
        protected.append({'path':row['source'],'sha256':digest})
        if row['copy'].endswith('.prj'):copies[row['branch']]=row
    matrixpath=HERE.parent/'h03-r120/R120-matriz.json'
    matrix=json.loads(matrixpath.read_text(encoding='utf-8'))
    w15=[s for s in matrix['segments'] if s['wallId']=='W15' and s['route']=='laje']
    if len(w15)!=1 or w15[0]['openingDeductions'] or w15[0]['lengthM']!=0.95:
        raise ValueError('Premissa W15 mudou')
    branches={}
    for b in ['CAD','BIM']:
        p=OUT/f'{b}-W15-reaberto-UI.txt'
        text=p.read_text(encoding='utf-8')
        if f'R130-{b}-W15' not in text or not re.search(r'Carga extra Value: 4\.695\b',text) or 'text 0.00 kN/m' not in text:
            raise ValueError('Releitura nativa incompleta')
        saved=json.loads((OUT/f'{b}-prj-salvo-hash.json').read_text(encoding='utf-8-sig'))
        copy=Path(copies[b]['copy']);digest=sha(copy)
        if digest.lower()!=saved['Hash'].lower():raise ValueError('PRJ mudou durante consulta')
        if digest==copies[b]['sha256Before']:raise ValueError('Não há alteração persistida no PRJ')
        dxf=OUT/f'{b}-N1-W15-reaberto.dxf'
        branches[b]={'projectPath':str(copy),'savedProjectSha256':digest,'readbackPreservedProjectBytes':True,
          'sourceR116Sha256':copies[b]['sha256Before'],'extraLoadNativeKNm':4.695,'wallLoadNativeKNm':0,
          'actionVisualReading':{'Adicional':4.70,'Solo':0,'Acidental':0,'Agua':0,'Subpressao':0,'Q_TELHADO_MANUTENCAO':0,
            'method':'Leitura visual da grade antes de salvar, com duas casas; total exato da linha relido após reabrir.'},
          'nativeReadbackFile':p.name,'drawingFile':dxf.name,'drawingSha256':sha(dxf),'drawing':drawing(dxf),
          'timing':json.loads((OUT/f'{b}-tempo-sessao.json').read_text(encoding='utf-8'))}
    if branches['CAD']['drawing']['startRaw']!=branches['BIM']['drawing']['startRaw'] or branches['CAD']['drawing']['endRaw']!=branches['BIM']['drawing']['endRaw']:
        raise ValueError('Geometria diverge entre ramos')
    result={'revision':'H03/R130','createdAtUtc':datetime.now(timezone.utc).isoformat(),
      'scope':'Ensaio isolado da parede W15 sobre laje L4/N1, em cópias derivadas R116, com salvar/fechar/reabrir e exportação gráfica DXF.',
      'wallReference':{'path':str(matrixpath),'sha256':sha(matrixpath),'segmentId':w15[0]['segmentId'],
        'geometryReference':'R56/R57; sem nova exportação dos arquivos de autoria nesta etapa',
        'areaWeightHypothesisKNm2':1.565,'grossHeightM':3,'lengthM':0.95,'lineMagnitudeKNm':4.695,
        'forceMagnitudeKN':4.46025,'compositionManufacturerConfirmed':False},
      'protectedR116Files':protected,'sourceFilesUnchanged':True,'branches':branches,
      'pairedExtraAndWallLoadsEqual':True,'pairedDrawingEndpointsEqual':True,
      'nativeInputPersistenceVerified':True,'graphicalExtentVerified':True,
      'loadsAppliedInExperimentalCopies':True,'processingPerformed':False,'analyticalLoadDistributionVerified':False,
      'structuralApproval':False,'finalWallLoadSetCompleted':False,'finalProductivityRankingAllowed':False,
      'monographEdited':False,'authorshipRVTorDWGEdited':False,
      'technicalSource':'https://suporte.altoqi.com.br/hc/pt-br/articles/360058309854',
      'nextStep':'Conferir reação/distribuição da W15 em análise isolada dos dois ramos; resolver demais paredes e ações antes de ELU/ELS completo.'}
    (OUT/'R130-resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    times={b:branches[b]['timing']['duracao_ms']/60000 for b in branches}
    (OUT/'LEIA-ME-R130.md').write_text(f'''# H03/R130 — linha W15 sobre laje

A hipótese W15 foi lançada em cópias independentes dos dois ramos: CAD 44 e BIM 45, derivadas da R116. Trata-se de complementação no receptor Eberick, e não de carga transferida automaticamente de DWG/IFC.

| Item | CAD | BIM |
|---|---:|---:|
| Carga extra relida após salvar/fechar/reabrir | 4,695 kN/m | 4,695 kN/m |
| Carga de parede adicional do comando | 0 | 0 |
| Início gráfico em coordenadas do modelo | (450;495) cm | (450;495) cm |
| Término gráfico em coordenadas do modelo | (545;495) cm | (545;495) cm |
| Extensão | 0,95 m | 0,95 m |
| Sessão exploratória | {times['CAD']:.3f} min | {times['BIM']:.3f} min |

A intensidade resulta da hipótese 1,565 kN/m² × 3,00 m. A integral prevista é 4,46025 kN; **não é reação calculada**. A composição da vedação continua hipótese sem confirmação de fabricante. Não há vão na faixa W15 da matriz R120.

O comando foi configurado com Parede desmarcado, ação Adicional e definição por dois pontos. O total exato 4,695 foi relido nativamente após reabertura. A grade de ações, inspecionada antes de salvar, exibiu Adicional 4,70 e outras cinco ações 0,00, na precisão de duas casas.

Os DXFs de croqui reaberto contêm uma única linha e um único rótulo no nível CR-Paredes. Os extremos brutos coincidem em (9;9,9) e (10,9;9,9). A escala gráfica 1:50 foi conferida por três centros de pilares de referência, com tolerância de 10⁻⁹ unidade gráfica apenas para resíduos numéricos da escrita. A coordenada Z=0 do DXF pertence ao desenho plano, não ao nível físico N1. O rótulo 4,70 é arredondado; o valor nativo permanece 4,695.

Preservaram-se os hashes de {len(protected)} arquivos R116. Os PRJs experimentais foram alterados pelo lançamento e permaneceram iguais aos hashes capturados após salvar durante a consulta e exportação. Não se editou monografia, RVT ou DWG de autoria.

**Não houve processamento nesta etapa.** A geometria gráfica e o valor persistido não comprovam a distribuição analítica na grelha, as reações, a capacidade resistente ou o atendimento a ELU/ELS. A R130 não incorpora o ensaio W03 de viga inteira da R121. A referência R116 continua preservada; as cópias R130 são ensaios parciais.

Os tempos incluem abertura, configuração, entrada, releitura, salvamento, reabertura, exportação e capturas. O CAD incluiu pesquisa e consulta extra de desenho; o BIM reutilizou o procedimento aprendido. Não constituem ranking nem economia percentual; os tempos finais dos fluxos permanecem abertos.

Próximo passo: análise isolada da W15 nos dois ramos, com conferência de integral e caminho de carga, antes de ampliar o lançamento às outras paredes. Procedimento consultado: [AltoQi — carga linear](https://suporte.altoqi.com.br/hc/pt-br/articles/360058309854).
''',encoding='utf-8')
    print(json.dumps({'protectedFiles':len(protected),'nativeExtraKNm':4.695,'pairedGraphicLengthM':0.95,'processed':False}))

if __name__=='__main__':main()

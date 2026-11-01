"""Conserva alternância reversível de unidade e identidade da carga consultada."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Unidades-H03-R125-CONSULTA-NAO-EXECUTAR')
SOURCE=HERE.parent/'h03-r122'


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def field(text, pattern):
    values=set(re.findall(pattern,text))
    if len(values)!=1: raise ValueError('Campo ausente ou conflitante: '+pattern)
    return values.pop()


def system_units(text):
    return {str(i):field(text,r'caixa de combinação \(settable, string\) [^\n]*? Value: ([^\n]*?) ID: '+str(i)+r'\b') for i in range(101,114)}


def beam(text, unit):
    if '39-H03-R122-BIM' not in text or 'Croqui-TCC-cdd31967-N1' not in text:
        raise ValueError('Projeto/pavimento diferente')
    name=field(text,r'editar \(settable, string\) Nome Value: (\S+) ID: 801')
    if name!='V1' or not re.search(r'text '+re.escape(unit)+r' ID: 567',text):
        raise ValueError('Peça ou unidade diferente')
    return {'name':name,'extraDisplayed':float(field(text,r'editar \(disabled, settable, string\) Carga extra Value: (\S+) ID: 564')),
            'unit':unit,'bwCm':float(field(text,r'editar \(settable, string\) bw Value: (\S+) ID: 810')),
            'hCm':float(field(text,r'editar \(settable, string\) h Value: (\S+) ID: 811')),
            'elevationCm':float(field(text,r'editar \(settable, string\) / Value: (\S+) ID: 507'))}


def main():
    if (OUT/'R125-resultado.json').exists(): raise FileExistsError('Resultado já existente')
    read=lambda name:(OUT/name).read_text(encoding='utf-8')
    units={name:system_units(read(file)) for name,file in [('before','Sistema-SI-retomada-UI.txt'),('temporary','Sistema-linear-kgfm-UI.txt'),('restoreSelected','Sistema-SI-restaurar-UI.txt')]}
    if units['before']!=units['restoreSelected']: raise ValueError('Configuração de restauração diferente')
    expected={**units['before'],'102':'kgf/m'}
    if units['temporary']!=expected: raise ValueError('Outra unidade alterada')
    kgf=beam(read('BIM-primeiro-V1-carga-kgfm-UI.txt'),'kgf/m')
    kn=beam(read('BIM-primeiro-V1-carga-SI-restaurada-UI.txt'),'kN/m')
    if kgf['extraDisplayed']!=444 or kn['extraDisplayed']!=4.44: raise ValueError('Leitura diferente do observado')
    if any(kgf[k]!=kn[k] for k in ['bwCm','hCm','elevationCm']): raise ValueError('Seção/elevação diferentes')
    preparation=json.loads((SOURCE/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected=[]
    for row in preparation['files']:
        after=sha(Path(row['source']))
        if after!=row['sha256Before']: raise ValueError('Fonte R121 alterada')
        protected.append({'path':row['source'],'sha256':after})
    prjs=[]
    for row in preparation['files']:
        if row['copy'].endswith('.prj'):
            after=sha(Path(row['copy']))
            if after!=row['sha256Before']: raise ValueError('PRJ de consulta alterado')
            prjs.append({'path':row['copy'],'sha256':after,'unchangedSinceR122Preparation':True})
    result={'revision':'H03/R125','createdAtUtc':datetime.now(timezone.utc).isoformat(),
      'scope':'Alternância temporária apenas da exibição de carga linear, consulta do primeiro trecho BIM V1/N1, cancelamento e fechamento sem salvar.',
      'units':units,'readings':{'kgfPerM':kgf,'restoredKNPerM':kn},
      'observedDisplayedRatioKgfPerKN':kgf['extraDisplayed']/kn['extraDisplayed'],
      'exportedMagnitudeKgfPerCmR122':4.44,'exportConsistentWithNativeKgfDisplay':True,
      'nativeDisplayConventionIdentifiedForThisReading':True,'universalUnitCalibrationProved':False,
      'exactSIConversionAsserted':False,'internalStoragePrecisionProved':False,
      'nativeLoadsEdited':False,'nativeGeometryEdited':False,'processingPerformed':False,
      'displayUnitRestoredByApplyAndBeamReadback':True,'protectedR121Files':protected,
      'copyPrjs':prjs,'monographEdited':False,'finalStructuralApproval':False,'finalProductivityRankingAllowed':False,
      'timing':json.loads(read('BIM-retomada-tempo.json')),
      'limits':['Relação observada 4,44 kN/m ↔444 kgf/m no aplicativo; não é conversão metrológica exata nem calibração universal.',
                'A consulta usou o primeiro trecho V1, identificado por posição na imagem, pavimento e seção20x45; nomes repetidos não identificam sozinhos a barra.',
                '13 seletores de unidade foram comparados antes e na configuração de restauração; retorno efetivo confirmado pela releitura da viga em kN/m.',
                'PRJs e fontes mantiveram hashes; isso não garante igualdade de todos os arquivos auxiliares do aplicativo.',
                'Tempo cobre só segmento retomado, sem consulta preliminar/espera do navegador e sem ranking.'],
      'nextStep':'Ensaiar delimitação geométrica da carga entre X10 e430cm em novas cópias independentes; não ajustar q apenas para forçar resumo.'}
    (OUT/'R125-resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'protectedSourceFiles':len(protected),'prjsUnchanged':len(prjs),'ratio':result['observedDisplayedRatioKgfPerKN']}))


if __name__=='__main__':main()

"""Empacota leituras manuais da UI; nao edita os projetos do Eberick."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
OUT = Path('D:/TCC/outputs/Escada-H03-R183-LEITURA-APOIOS-NAO-EXECUTAR')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    start = json.loads((OUT / 'R183-inicio.json').read_text(encoding='utf-8-sig'))
    sources = start['sourceProjects']
    for branch, source in sources.items():
        source['sha256AfterRead'] = sha(source['path'])
        source['unchanged'] = source['sha256AfterRead'] == source['sha256']
        if not source['unchanged']:
            raise ValueError('Projeto fonte alterado: ' + branch)
    values = dict(lowerBoundaryOrdinaryBarWidthCm=0, slabAnchorageOption='reta',
        slabMinimumPositiveMomentForAnchorageKgfM=100,
        slabMinimumTensionForAnchorageKgfPerM=100,
        allowAnchorageInAdjacentSlab=False, waiveSlabShearVerification=True,
        beamMaximumReinforcementRatioPercent=2)
    result = dict(revision='H03/R183', recordedAtUtc=datetime.now(timezone.utc).isoformat(),
        scope='Consulta nativa de apoios e parametros; sem processamento ou correcao',
        sourceProjects=sources, observations={b: dict(values) for b in sources},
        observationMethod='Leitura manual das telas nativas; capturas anexas. Nao e OCR automatizado.',
        lowerBoundaryLocation='N0, barra horizontal entre AE1A e AE1B na extremidade inferior de LE3',
        conclusions=dict(selectedSettingsMatch=True, zeroWidthIsNotByItselfInvalid=True,
            exactFailingAnchorageEdgeIdentified=False, causalTestCompleted=False,
            shearVerificationRequiresReview=True, fullSizingApproved=False,
            newPhysicalBeamOrColumnCreated=False),
        timing=dict(newNativeProcessing=False, nativeSeconds=None, fullFlowMeasured=False,
            auditSessionIsNotActiveWorkflowTime=True),
        sources=[dict(title='Erro A11 - Largura do apoio insuficiente em lajes',
            url='https://suporte.altoqi.com.br/hc/pt-br/articles/115003202014'),
            dict(title='Como inserir os lances da escada?',
            url='https://suporte.altoqi.com.br/hc/pt-br/articles/115002312454')])
    write(OUT / 'R183-leitura-apoios.json', result)
    pointer = Path('D:/TCC/dados-pesquisa/escada-h03-atual.json')
    backup = OUT / 'R183-ponteiro-anterior.json'
    if not backup.exists():
        shutil.copy2(pointer, backup)
    current = json.loads(pointer.read_text(encoding='utf-8-sig'))
    current.update(latestSupportSettingsReadRevision='H03/R183',
        latestSupportSettingsReadPath=str(OUT / 'R183-leitura-apoios.json'),
        latestSupportSettingsReadSha256=sha(OUT / 'R183-leitura-apoios.json'),
        lowerStairBoundaryOrdinaryBarWidthCmBoth=0,
        slabAnchorageTypeBoth='reta', slabShearVerificationWaivedBothObserved=True,
        allStructuralElementsSuccessfullyDesigned=False, finalReinforcementReviewed=False)
    write(pointer, current)
    write(OUT / 'R183-ponteiro-atualizado.json', current)
    for p in OUT.glob('*-0.png'):
        shutil.copy2(p, HERE / p.name)
    for name in ('R183-inicio.json', 'R183-leitura-apoios.json', 'R183-ponteiro-atualizado.json',
                 'CAD-N0-barra-inferior-AX.txt', 'BIM-N0-barra-inferior-AX.txt'):
        shutil.copy2(OUT / name, HERE / name)
    shutil.copy2(HERE / 'LEIA-ME-R183.md', OUT / 'LEIA-ME-R183.md')
    files = [p for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'R183-manifesto.json']
    manifest = dict(revision='H03/R183', files=[dict(relativePath=p.name,
        bytes=p.stat().st_size, sha256=sha(p)) for p in files])
    write(HERE / 'R183-manifesto.json', manifest)
    shutil.copy2(HERE / 'R183-manifesto.json', OUT / 'R183-manifesto.json')
    print(json.dumps(dict(files=len(files), sourceProjectsUnchanged=True)))


if __name__ == '__main__':
    main()

"""Auditoria e backup das copias R218 apos gravacao pela interface nativa."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime, timezone
import argparse


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(root, backup):
    if backup.exists():
        raise FileExistsError(backup)
    original=root.parent/'H03-R217-V1-VERIFICACAO-NAO-EXECUTAR'
    expected={'CAD':'1bb22b8316417a11f53d9506483910593aad11f26d8db2548c72c969d651ca53',
              'BIM':'84ce9482e16afdeac95c3301fbbae63c52dc2555e069c3c7b4a239b0618348b2'}
    projects=[]
    for branch in expected:
        before,= (original/branch/'Projeto Eberick').glob('*.prj')
        after,= (root/branch/'Projeto Eberick').glob('*.prj')
        assert sha(before)==expected[branch], 'Original R217 alterado'
        with ZipFile(after) as z:
            assert z.testzip() is None, 'PRJ com CRC divergente'
        drawings=list((root/branch/'Desenhos').rglob('R218-V1-COMPLEMENTO-EXTERNO.cad'))
        native=list((root/branch/'Desenhos').rglob('R218-V1-NATIVO-C15-REFERENCIA.cad'))
        assert len(drawings)==len(native)==1
        projects.append(dict(branch=branch,path=str(after.relative_to(root)),sha256=sha(after),
            originalSha256=sha(before),originalPreserved=True,crc='OK',
            skinBarsReadBackAfterReopen='2x2 fi8',
            complementaryDrawing=str(drawings[0].relative_to(root)),drawingSha256=sha(drawings[0])))
    audit=dict(recordedAt=datetime.now(timezone.utc).isoformat(),revision='R218',
      nativeProjects=projects,fullVerificationComplete=False,globalStirrupLimitChanged=False,
      nativeStirrupSpacingCm=15,externalMaximumSpacingCm=9,
      externalSkinBars=4,externalCrossTiesPerPosition=2,
      nativeSkinSettingAppliedToV1=True,externalDetailImportedAndSavedBoth=True,
      steelScheduleUpdatedForExternalDetail=False,pending=['Aviso 19','Aviso 98 em ambas as extremidades da pele',
        'Verificacao das ancoragens longitudinais, dobras, montagem e ligacao aos apoios'],
      timing=dict(pairedExperiment=False,durationSeconds=None,tokens=None,inferenceSeconds=None,
        reason='Revisao interrompida entre sessoes; sem cronometro continuo confiavel. CAD exigiu recuperacao e processamento global; BIM teve recalculo individual da V1. Nao comparar os intervalos como ensaio pareado.'),
      files=[dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=sha(p))
             for p in sorted(root.rglob('*')) if p.is_file() and not p.name.endswith(('-tmp','.tmp'))])
    (root/'R218-integridade.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with ZipFile(backup,'x',ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file() and not p.name.endswith(('-tmp','.tmp')):
                z.write(p,p.relative_to(root).as_posix())
    with ZipFile(backup) as z:
        assert z.testzip() is None
        for project in projects:
            name=project['path'].replace('\\','/')
            assert hashlib.sha256(z.read(name)).hexdigest()==project['sha256']
    result=dict(path=str(backup),sha256=sha(backup),bytes=backup.stat().st_size,crc='OK',projectHashesVerified=True)
    (root/'R218-backup.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('backup',type=Path)
    args=p.parse_args();main(args.root,args.backup)

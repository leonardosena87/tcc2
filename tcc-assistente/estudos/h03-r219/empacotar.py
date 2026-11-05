"""Monta entrega academica identificada; preserva fontes e valida copias/ZIP."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import csv
import hashlib
import json
import shutil
import argparse


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output):
    here=Path(__file__).resolve().parent
    studies=here.parent
    local=Path('D:/TCC/outputs')
    if output.exists() or output.with_suffix('.zip').exists():
        raise FileExistsError('Nao substituir pacote existente')
    output.mkdir(parents=True)
    copied=[]
    def copy(source,target):
        destination=output/target
        destination.parent.mkdir(parents=True,exist_ok=True)
        before=sha(source)
        shutil.copy2(source,destination)
        assert sha(destination)==sha(source)==before
        copied.append(dict(path=str(target),source=str(source),bytes=destination.stat().st_size,sha256=before))
    for name in ('LEIA-PRIMEIRO.md','RESULTADOS-PARA-O-TCC.md'):
        copy(here/name,Path(name))
    backup=local/'Salvamento-R218-2026-11-05.zip'
    expected=json.loads((studies/'h03-r218/R218-backup.json').read_text(encoding='utf-8-sig'))
    assert sha(backup)==expected['sha256']
    with ZipFile(backup) as z:
        assert z.testzip() is None
    copy(backup,Path('Eberick')/backup.name)
    for name in ('H03-R195-SEM-J4.rvt','R160-CAD-PATAMAR-FORMA-CANDIDATA.dwg'):
        copy(local/'W08-H03-R207-ENSAIO/Autoria-salva'/name,Path('Autoria-referencia')/name)
    for revision,name in (('r90','LEIA-ME-R90.md'),('r212','README.md'),('r214','README.md'),
                          ('r216','README.md'),('r217','README.md'),('r218','README.md')):
        copy(studies/('h03-'+revision)/name,Path('Evidencias')/(revision.upper()+'-'+name))
    for name in ('R218-resumo.json','R218-validacao.json','R218-backup.json'):
        copy(studies/'h03-r218'/name,Path('Evidencias')/name)
    rows=[
        ('R196','W08 integral',7,7,'Uma execucao por fluxo','h03-r206/tempos-recentes-por-cenario.json'),
        ('R201','ELS fissurado; dimensionamento selecionado herdado',9,9,'Escopo diferente do integral','h03-r206/tempos-recentes-por-cenario.json'),
        ('R205','ELS fissurado; dimensionamento integral',10,10,'Uma execucao por fluxo','h03-r206/tempos-recentes-por-cenario.json'),
        ('R207','W08 corrigida',10,11,'Estados finais diferentes; BIM com D16','h03-r207/README.md'),
        ('R211 CAD / R210 BIM','Revisao de concepcao',9,9,'Revisoes distintas; agrupamento diferente','h03-r216/README.md'),
        ('R215','Controle apos recuperacao','',10,'CAD nao registrado; BIM apenas','h03-r216/README.md')]
    with (output/'tempos-nativos.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f,delimiter=';')
        writer.writerow(('Revisao','Cenario','CAD_s','BIM_s','Limite','Fonte'))
        writer.writerows(rows)
    data=dict(revision='R219',classification='Entrega academica preliminar; nao executar',
       structuralApproval=False,fullWorkflowComparisonComplete=False,authoringSynchronized=False,
       nativeTotalTimingComparisonAvailable=False,files=copied)
    (output/'manifesto.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    all_files=[p for p in sorted(output.rglob('*')) if p.is_file()]
    zipped=output.with_suffix('.zip')
    with ZipFile(zipped,'x',ZIP_DEFLATED) as z:
        for p in all_files:z.write(p,p.relative_to(output).as_posix())
    with ZipFile(zipped) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(all_files)
        for p in all_files:
            assert hashlib.sha256(z.read(p.relative_to(output).as_posix())).hexdigest()==sha(p)
    result=dict(package=str(output),zip=str(zipped),bytes=zipped.stat().st_size,sha256=sha(zipped),
                crc='OK',everyFileHashVerified=True,fileCount=len(all_files),structuralApproval=False)
    (output.parent/(output.name+'-verificacao.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output',type=Path)
    main(p.parse_args().output)

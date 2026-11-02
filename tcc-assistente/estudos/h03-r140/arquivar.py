"""Arquiva evidência concluída por lista explícita; exclui capturas transitórias."""
import json
import shutil
from auditar import HERE, OUT, sha

def main():
    stems=['CAD-W20-G2-fletores-finalizado','CAD-W20-G2-deslocamentos',
        'CAD-grelha-duplo-clique-abre-edicao-nao-rotacoes']
    stems += [f'{b}-{c}-reacoes-lajes-N1-G2' for b in ['CAD','BIM'] for c in ['W20','controle']]
    names={'R140-preparacao.json','R140-resultado.json','LEIA-ME-R140.md'}
    for label in ['CAD','BIM','CAD-controle','BIM-controle']:
        names.update([f'{label}-consulta-inicio.json',f'{label}-consulta-fim.json'])
    for b in ['CAD','BIM']:
        for c in ['W20','controle']:
            names.add(f'{b}-{c}-reacoes-N1-G2.dxf')
    for stem in stems:
        names.update(p.name for p in OUT.glob(stem+'-*'))
    for name in names:
        src,dst=OUT/name,HERE/name
        if not src.is_file():raise FileNotFoundError(src)
        if dst.exists() and sha(src) != sha(dst):raise ValueError('Evidência arquivada divergente')
        shutil.copyfile(src,dst)
    (HERE/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    files=[{'path':p.relative_to(HERE).as_posix(),'sha256':sha(p)} for p in sorted(HERE.rglob('*'))
        if p.is_file() and '__pycache__' not in p.parts and 'manifesto' not in p.name]
    for base in [HERE,OUT]:
        (base/'R140-manifesto.json').write_text(json.dumps({'revision':'H03/R140','publicFiles':files},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'manifestedFiles':len(files)}))

if __name__ == '__main__':
    main()

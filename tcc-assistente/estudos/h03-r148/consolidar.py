"""Inventaria a triagem nativa sem confundir peças com trechos geométricos."""
import hashlib
import importlib.util
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).parent
OUT=Path('D:/TCC/outputs/Dimensionamento-H03-R148-PARCIAL-NAO-EXECUTAR')
spec=importlib.util.spec_from_file_location('r146',HERE.parent/'h03-r146/consolidar.py')
r146=importlib.util.module_from_spec(spec);spec.loader.exec_module(r146)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def parse_status(text,branch):
    prefix={'CAD':'74-H03-R148-CAD','BIM':'75-H03-R148-BIM'}[branch]
    if prefix not in text or 'janela Status dos elementos' not in text:
        raise ValueError('Projeto/status incorreto')
    floor=kind=None;rows={}
    for line in text.splitlines():
        if 'item da árvore (selectable) ' not in line:continue
        label=line.split('item da árvore (selectable) ',1)[1].strip()
        if re.fullmatch(r'(?:TCC-cdd31967-)?N[012]',label):
            floor=label[-2:];kind=None
        elif label in {'Viga(s)','Laje(s)','Pilar(es)','Sapata(s)'}:kind=label
        else:
            m=re.fullmatch(r'(\d+) (Viga\(s\)|Laje\(s\)|Pilar\(es\)) (dimensionad[ao]\(s\)|com aviso\(s\)|com erro\(s\))',label)
            if m and floor and kind:
                key=(floor,kind,m[3]);count=int(m[1])
                if key in rows and rows[key]!=count:raise ValueError('Contagem contraditória')
                rows[key]=count
    return rows


def main():
    target=OUT/'R148-resultado.json'
    if target.exists():raise FileExistsError(target)
    prep=json.loads((OUT/'R102-preparacao.json').read_text(encoding='utf-8'))
    protected=[{**r,'sha256After':sha(Path(r['source']))} for r in prep['files']]
    assert all(r['sha256After']==r['sha256Before'] for r in protected)
    branches={}
    for branch in ('CAD','BIM'):
        counts={};warnings=set()
        evidence=[]
        for p in sorted(OUT.glob(branch+'-*-UI.txt')):
            text=p.read_text(encoding='utf-8')
            if 'janela Status dos elementos' in text:
                for key,value in parse_status(text,branch).items():
                    if key in counts and counts[key]!=value:raise ValueError('Contagens entre capturas divergentes')
                    counts[key]=value
                warnings.update(re.findall(r'item da árvore \(selectable\) ((?:Aviso|Erro) [^\r\n]+)',text))
                evidence.append(dict(path=p.name,sha256=sha(p)))
        assert all(any(k[0]==floor and k[1]==kind for k in counts) for floor in ('N1','N2') for kind in ('Viga(s)','Laje(s)','Pilar(es)'))
        prj=Path(next(r['copy'] for r in protected if r['branch']==branch and r['copy'].endswith('.prj')))
        with zipfile.ZipFile(prj) as z:assert z.testzip() is None
        session=json.loads((OUT/f'{branch}-sessao-tempo.json').read_text(encoding='utf-8'))
        command=json.loads((OUT/f'{branch}-processamento-tempo.json').read_text(encoding='utf-8'))
        r146.check_time(session,command)
        text=(OUT/f'{branch}-resumo-analise-UI.txt').read_text(encoding='utf-8')
        summary=r146.extract(text)
        src=prj.parent.parent;frozen=OUT/'congelados-apos-triagem'/branch
        if frozen.exists():raise FileExistsError(frozen)
        shutil.copytree(src,frozen)
        files=[]
        for p in sorted(src.rglob('*')):
            if p.is_file():
                rel=p.relative_to(src);assert sha(p)==sha(frozen/rel)
                files.append(dict(path=rel.as_posix(),sha256=sha(p)))
        branches[branch]=dict(projectPath=str(prj),projectSha256=sha(prj),summary=summary,
            displayedStatusCounts=[dict(floor=k[0],kind=k[1],status=k[2],count=v) for k,v in sorted(counts.items())],
            expandedMessageTexts=sorted(warnings),statusEvidence=evidence,
            sessionTime=session,processingObservation=command,frozenPath=str(frozen),frozenFiles=files)
    result=dict(revision='H03/R148',createdAtUtc=datetime.now(timezone.utc).isoformat(),branches=branches,
        protectedR146Files=protected,sourcesUnchanged=True,dimensioningAttempted=True,
        selection='Vigas, pilares e lajes N1/N2; N0 e fundacoes desmarcados',
        slabDeflectionPerformed=False,crackedStiffnessPerformed=False,
        finalStructuralApproval=False,finalRankingAllowed=False,
        identifiedBimError=dict(floor='N1',nativeBeam='V2',code='D16',node=2,
            text='Erro na armadura negativa',specificDiameterFailureCause=None,transferDefectDemonstrated=False),
        vendorDiagnostic='https://suporte.altoqi.com.br/hc/pt-br/articles/360000680694',
        limits=['Cargas e verificacoes incompletas; triagem nao aprova armaduras ou estabilidade final.',
                'Categorias dimensionadas, com avisos e com erros sao estados exibidos; nao somar como defeitos do IFC/DWG.',
                'CAD mostra 15 pecas de viga em cada nivel; BIM 12 em N1 e 8 em N2. Identidade de agrupamento/detalhamento ainda nao equalizada.',
                'Mensagem de erro BIM nao demonstra causa de transferencia; requer verificar vao/no e resultados por bitola.',
                'Somente avisos expandidos foram identificados por texto; nao se inferiu o codigo de todas as onze lajes.',
                'Sessao BIM inclui longa interrupcao entre turnos e a retomada; nao mede trabalho continuo ou tempo ativo. A resposta sobre escada nao foi intervencao de operacao no Eberick.',
                'Salvar/fechar e integridade ZIP foram conferidos; nao houve releitura de todas as armaduras apos reabrir.',
                'Sem alteracoes de seções, criterios, autoria RVT/DWG ou monografia.'])
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({b:dict(counts=r['displayedStatusCounts'],messages=r['expandedMessageTexts']) for b,r in branches.items()},ensure_ascii=True))


if __name__=='__main__':main()

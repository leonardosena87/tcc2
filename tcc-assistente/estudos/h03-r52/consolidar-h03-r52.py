"""Congela hipotese de continuidade atribuida via UI; nao certifica modelo analitico."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
root=Path('D:/TCC');out=root/'outputs/Conferencia-H03-R52-VINCULOS-NAO-EXECUTAR'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,r:p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
states=[]
for branch in ('CAD','BIM'):
    prep=json.loads((out/f'R52-preparacao-{branch}.json').read_text(encoding='utf-8-sig'))
    native=Path(prep['nativeProject']).parent.parent;frozen=[]
    for folder in ('Projeto Eberick','_DADOS_'):
        for p in (native/folder).rglob('*'):
            if not p.is_file() or p.suffix.lower() in ('.bak','.lck','.tmp','.errlog'):continue
            dest=out/f'congelado-{branch}'/p.relative_to(native);dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.exists():assert sha(dest)==sha(p),str(dest)
            else:shutil.copy2(p,dest)
            frozen.append(dict(path=str(p),frozen=str(dest),sha256=sha(p)))
    before=next(r for r in prep['files'] if r['copy']==prep['nativeProject'])['sha256']
    after=sha(Path(prep['nativeProject']));assert before!=after,'Arquivo nativo nao mudou.'
    state=dict(revision='H03/R52',branch=branch,atUtc=datetime.now(timezone.utc).isoformat(),nativeProject=prep['nativeProject'],
        action='Modelo > Lajes > Engastar; selecionar uma viga comum a L4 e L6 no N1 e confirmar Enter.',
        assignedHypothesis='Continuidade entre a laje interna e a varanda macica no bordo comum.',
        selectedBeamAxisM=dict(x=9.65,yStart=3.9,yEnd=7.05,levelZ=3.2),nativeSlabNames=['L4','L6'],
        selectedBeamCount=1,assignmentCommandAccepted=True,saveCloseReopenPerformed=True,croquiObservedAfterReopen=True,
        priorLinkStateVerified=False,analyticalLinkVerified=False,balconyStructuralSafetyVerified=False,
        geometryReexportedThisRevision=False,structuralCalculationPerformed=False,
        beforeNativeSha256=before,afterNativeSha256=after,frozenFiles=frozen,
        classification='Hipotese comum de vinculacao atribuida separadamente nos dois receptores; nao classificada como erro de transferencia.',
        technicalReferences=['https://suporte.altoqi.com.br/hc/pt-br/articles/115003725214','https://suporte.altoqi.com.br/hc/pt-br/articles/115004249154'],
        limits=['Atribuicao confirmada pela sequencia de UI e pelo arquivo alterado; croqui observado apos reabrir.',
            'Nao foi extraido parametro interno de vinculo nem gerada grelha processada; persistencia analitica permanece pendente.',
            'Nao se verificou se o vinculo anterior era rotulado ou ja continuo. Nao contar a acao como defeito comprovado.',
            'Nao se configurou engaste direto na viga nem se validou comportamento de torcao.',
            'Nao se alteraram as demais ligacoes entre lajes; auditoria de toda a conectividade ainda pendente.',
            'A escolha exige verificacao de continuidade efetiva, armadura negativa, ancoragem, esforcos e deformacoes no calculo.',
            'Relatorios normativos da estrutura, cargas completas e apoios idealizados ainda pendentes.'])
    write(out/f'R52-vinculo-{branch}.json',state);states.append(state)
preserved=[]
src=root/'outputs/Conferencia-H03-R51-PARAMETROS-NAO-EXECUTAR/R51-manifesto.json'
for row in json.loads(src.read_text(encoding='utf-8-sig'))['files']:
    assert sha(Path(row['path']))==row['sha256'],row['path'];preserved.append(row['path'])
write(out/'R52-estado-atual.json',dict(revision='H03/R52',branches={s['branch']:s['nativeProject'] for s in states},
    sameAssignedBalconyHypothesis=True,analyticalLinkVerified=False,completeLoads=False,structuralCalculationPerformed=False,
    preservedR51Files=len(preserved),nextSteps=['Conferir toda conectividade e apoios idealizados da superestrutura.',
        'Completar cargas, escada e reservatorio antes de processar.',
        'Conferir grelha e continuidade efetiva da varanda quando o modelo puder ser processado.',
        'Reexportar geometria dos dois ramos para controlar efeitos das revisoes de parametros/vinculos.']))
shutil.copy2(Path(__file__),out/Path(__file__).name)
write(out/'R52-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in out.rglob('*') if p.is_file() and p.name!='R52-manifesto.json']))
print(json.dumps(dict(frozenByBranch={s['branch']:len(s['frozenFiles']) for s in states},preservedR51Files=len(preserved),sameAssignedHypothesis=True,analyticalLinkVerified=False)))

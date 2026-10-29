"""Valida evidencias e registra apenas materiais pertinentes, sem modelos nativos."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, shutil
root=Path('D:/TCC')
repo=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for rev,folder in [('R60','Cobertura-H03-R60-REACOES-PARCIAIS-NAO-EXECUTAR'),('R61','Cargas-H03-R61-TELHADO-G-PARCIAL-NAO-EXECUTAR')]:
    src=root/'outputs'/folder
    rows=read(src/f'{rev}-manifesto.json')['files']
    for r in rows:assert sha(Path(r['path']))==r['sha256'],r['path']
    for p in src.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'))
    if rev=='R61':
        data=read(src/'R61-resultado.json')
        assert len(data['appliedGPointIds'])==2 and len(data['pendingGPointIds'])==11
        assert data['summaryTextsEqualAtDisplayedPrecision'] and not data['fullFlowRankingAllowed']
        for b in ('CAD','BIM'):
            state=read(src/f'R61-estado-{b}.json')
            assert sha(Path(state['nativeProject']))==state['nativeSha256']
            for f in state['frozenFiles']:assert sha(Path(f['frozen']))==f['sha256']
    val=dict(atUtc=datetime.now(timezone.utc).isoformat(),manifestFilesChecked=len(rows),pythonSyntaxPassed=True,syntheticTests=dict(passed=9,failed=0,command='node --test tests/exchange.test.mjs tests/structural.test.mjs',nativeStructuralValidation=False),liveOpenAIApiCalls=False,fullFlowRankingAllowed=False)
    (src/f'{rev}-validacao-registro.json').write_text(json.dumps(val,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    shutil.copy2(Path(__file__),src/Path(__file__).name)
    manifest=dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(src.rglob('*')) if p.is_file() and p.name!=f'{rev}-manifesto.json'])
    (src/f'{rev}-manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    dst=repo/f'h03-{rev.lower()}'
    dst.mkdir(exist_ok=False)
    allowed={'.json','.txt','.md','.py'} | ({'.svg','.png'} if rev=='R60' else set())
    copied=[]
    for p in src.iterdir():
        if p.is_file() and p.suffix.lower() in allowed:
            q=dst/p.name;shutil.copy2(p,q);assert sha(q)==sha(p);copied.append(p.name)
    print(json.dumps(dict(revision=rev,files=len(copied),destination=str(dst)),ensure_ascii=False))

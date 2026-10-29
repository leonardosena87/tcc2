"""Consolida 26 leituras reais; nao calcula ou certifica a estrutura."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, re, shutil, zipfile

ROOT = Path('D:/TCC')
OUT = ROOT/'outputs/Cargas-H03-R64-CONFERENCIA-INDIVIDUAL-NAO-EXECUTAR'
DEST = Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r64')
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v): (OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def fmt(ms): return f'{ms//60000} min {ms%60000/1000:.3f} s'
assert not DEST.exists() and not (OUT/'R64-manifesto.json').exists()
protected=read(OUT/'R64-protegidos-R63.json')
for row in protected: assert sha(Path(row['path']))==row['sha256'],row['path']
plan=read(OUT/'R64-plano.json')
assert len(plan)==13 and len({p['id'] for p in plan})==13
tol=.0000051
results={}
states={}
for branch in ('CAD','BIM'):
    rows=[]
    for p in plan:
        file=OUT/f'{branch}-{p["id"]}-leitura-UI.txt'
        t=file.read_text(encoding='utf-8-sig')
        vals={k:float(re.search(r'\b'+k+r' Value: (-?[0-9.]+)',t).group(1)) for k in ('X','Y','Fx','Fy','Fz','Mx','My','Mz')}
        assert vals['X']==p['xCm'] and vals['Y']==p['yCm'],file
        assert abs(vals['Fz']-p['fzKN'])<=tol,file
        assert all(vals[k]==0 for k in ('Fx','Fy','Mx','My','Mz')),file
        assert 'Ação Value: Adicional' in t and 'text kN ID: 107' in t,file
        rows.append(dict(id=p['id'],expected=p,observed=vals,passed=True,evidence=file.name))
    results[branch]=rows
    write(f'R64-leituras-{branch}.json',dict(branch=branch,count=len(rows),loadEntryPrecisionToleranceKN=tol,engineeringEdited=False,rows=rows))
    prep=read(OUT/f'R64-preparacao-{branch}.json')
    native=Path(prep['nativeProject'])
    old=read(Path(prep['sourceState']))
    identical=sha(native)==old['nativeSha256']
    with zipfile.ZipFile(native) as z: assert z.testzip() is None
    oldnative=next(Path(r['frozen']) for r in old['frozenFiles'] if Path(r['path']).suffix.lower()=='.prj')
    with zipfile.ZipFile(native) as a, zipfile.ZipFile(oldnative) as b:
        contentsEqual=set(a.namelist())==set(b.namelist()) and all(a.read(n)==b.read(n) for n in a.namelist())
    frozen=OUT/f'congelado-{branch}'
    assert not frozen.exists()
    files=[]
    for source in sorted(native.parent.parent.rglob('*')):
        if not source.is_file() or source.suffix.lower() in ('.bak','.bak-g2','.bak-g3','.tmp'): continue
        target=frozen/source.relative_to(native.parent.parent)
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
        assert sha(source)==sha(target)
        files.append(dict(path=str(source),frozen=str(target),sha256=sha(target)))
    states[branch]=dict(nativeProject=str(native),nativeSha256=sha(native),frozenFiles=files,closedBeforeFreeze=True,zipIntegrityPassed=True,nativeByteIdenticalToR63=identical,nativeZipContentsIdenticalToR63=contentsEqual,engineeringEditsPerformed=False,recalculationPerformed=False,all13RoofGPointsIndividuallyRead=True,eluElsApproved=False)
    write(f'R64-estado-{branch}.json',states[branch])
comparison=[dict(id=a['id'],equalDisplayedComponentsAndCoordinates=a['observed']==b['observed']) for a,b in zip(results['CAD'],results['BIM'])]
assert all(r['equalDisplayedComponentsAndCoordinates'] for r in comparison)
times={b:read(OUT/f'R64-tempo-{b}.json') for b in ('CAD','BIM')}
assert all(t['durationMs']>0 and t['rankingAllowed'] is False for t in times.values())
result=dict(revision='H03/R64',atUtc=datetime.now(timezone.utc).isoformat(),status='26 leituras individuais validadas: 13 pontos G A1/A2 em cada ramo',protectedR63FilesChecked=len(protected),readCount=26,roofGPointsPerBranch=13,displayPrecisionToleranceKN=tol,intendedRoundedRoofGDownKN=-sum(p['fzKN'] for p in plan),comparison=comparison,allExpectedReadingsPassed=True,engineeringEditsPerformed=False,recalculationPerformed=False,fullTransferEquivalenceProven=False,roofLoadCaseComplete=False,eluElsApproved=False,sourceRvtDwgEdited=False,monographEdited=False,fullFlowRankingAllowed=False,isolatedAIEffortMeasured=False,prospectiveAssistedAuditTimes=times,excludedDiagnosticCaptures=sorted(p.name for p in OUT.glob('*INVALIDA.txt')))
write('R64-resultado.json',result)
table='\n'.join(f'| {p["id"]} | {p["xCm"]:g} | {p["yCm"]:g} | {p["fzKN"]:.6f} | {results["CAD"][i]["observed"]["Fz"]:g} | {results["BIM"][i]["observed"]["Fz"]:g} |' for i,p in enumerate(plan))
report=f'''# H03/R64 — conferência individual das cargas permanentes da cobertura

ESTUDO PARCIAL — NÃO EXECUTAR. Conferiram-se 13 pontos em cada ramo no Eberick 2025 Infinity, em cópias independentes dos congelados R63. As 26 leituras confirmaram coordenadas X/Y, ação Adicional, Fz negativo e Fx/Fy/Mx/My/Mz nulos. Todas corresponderam ao plano e as leituras CAD/BIM coincidiram entre si.

## Resultado verificável

| Ponto | X (cm) | Y (cm) | Fz pretendido (kN) | CAD exibido (kN) | BIM exibido (kN) |
|---|---:|---:|---:|---:|---:|
{table}

A soma das forças pretendidas arredondadas é 18,511247 kN, descendente, somente nos trechos A1/A2 da R60. A tolerância de 0,0000051 kN atende à precisão da janela observada; por exemplo, -1,120503 aparece como -1,1205. Não se concluiu que o valor interno foi truncado nem se alteraram forças para reproduzir a janela. Não houve edição de engenharia, novo processamento, mudança de unidade ou correção nesta revisão. As consultas foram encerradas por Escape, inclusive o diálogo do nó.

Os pontos CAD RC07/RC08/RC13 corrigidos na R63 e RC12 corrigido na R62 persistiram. A conclusão se limita ao lançamento G consultado; não comprova equivalência integral da transferência DWG/IFC ou de esforços, armaduras, combinações e demais cargas. Não se atribuem correções anteriores a defeito DWG. A genealogia é AutoCAD 2027/DWG2D e Revit 2027.2/IFC adaptado; não se operaram esses dois programas nesta auditoria.

## Qualidade dos registros

Cada leitura válida possui arquivo próprio *-leitura-UI.txt e linha estruturada em R64-leituras-CAD/BIM.json. Comparou-se por coordenadas, sem depender apenas da posição visual ou do nome de uma viga. Preservaram-se três capturas iniciais BIM com sufixo INVALIDA: um vínculo de estado do runtime apontava a observação anterior e registrou a árvore incorreta. Foram excluídas da análise e substituídas por consultas reais posteriores com estado global explícito; não se contaram como divergências estruturais ou defeitos IFC. Essa recuperação é esforço de instrumentação da IA/interface.

Verificaram-se por SHA-256 {len(protected)} arquivos R63 protegidos. Após fechar cada projeto, verificou-se a integridade ZIP dos PRJ e congelou-se o conjunto com seus arquivos associados. Igualdade binária do PRJ em relação à R63: CAD={states['CAD']['nativeByteIdenticalToR63']}, BIM={states['BIM']['nativeByteIdenticalToR63']}; igualdade dos conteúdos descompactados: CAD={states['CAD']['nativeZipContentsIdenticalToR63']}, BIM={states['BIM']['nativeZipContentsIdenticalToR63']}. Arquivos auxiliares de interface podem ser gravados pelo Eberick; não se afirmou que todo arquivo nativo permaneceu idêntico. Nenhuma monografia, RVT ou DWG foi editada.

## Tempos prospectivos e esforço assistido

CAD: {fmt(times['CAD']['durationMs'])}, de {times['CAD']['startUtc']} a {times['CAD']['endUtc']}. BIM: {fmt(times['BIM']['durationMs'])}, de {times['BIM']['startUtc']} a {times['BIM']['endUtc']}. Os JSON preservam início/fim UTC e duração bruta. São intervalos de auditoria assistida, incluindo navegação, raciocínio, latência, recuperação de captura e continuidade entre mensagens; não medem tempo de transferência ou solver. O BIM incluiu a recuperação das capturas iniciais inválidas. Não se isolou tempo humano ativo, esforço cognitivo da IA, tokens ou custo. Não se calcula vantagem percentual nem vencedor dos fluxos com esses intervalos. O ensaio final exige tarefas pareadas, entradas congeladas, mesmos critérios de início/fim e separação entre transferência, reconstrução, correções, verificação, espera e intervenção humana.

## Continuidade e limites

A pendência de leitura individual dos 13 pontos G dos dois ramos foi encerrada. Segue pendente a ação variável do telhado, sem duplicar a sobrecarga das lajes, além de P1/varanda, P2/abrigo e sua altimetria, perfis/apoios/ancoragens metálicas, paredes/aberturas, reservatório de 1.000 L/tara/base, escada/bordas, vento/combinações, ELU/ELS e sincronização das origens RVT/DWG. Os avisos e resumos de processamento R63 permanecem históricos; não foram reprocessados nesta revisão. Mantém-se o recorte da superestrutura com apoios idealizados e sem fundações reais dimensionadas. A auditoria de dados não equivale à aprovação da segurança estrutural.
'''
(OUT/'LEIA-ME-R64.md').write_text(report,encoding='utf-8')
shutil.copy2(Path(__file__),OUT/Path(__file__).name)
for p in OUT.glob('*.py'): ast.parse(p.read_text(encoding='utf-8'))
write('R64-validacao.json',dict(all26ReadingsPassed=True,bothBranchesClosedBeforeFreeze=True,zipIntegrityPassed=True,protectedFilesPassed=len(protected),scriptSyntaxPassed=True,structuralDesignValidated=False,liveOpenAIApiCalls=False,assistantCodeChanged=False))
write('R64-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='R64-manifesto.json']))
guide=ROOT/'CONTINUAR-AQUI-H03-2026-10-29.md'
old=guide.read_text(encoding='utf-8-sig')
assert not old.startswith('# Atualizacao R64')
guide.write_text(f'''# Atualizacao R64 — 29/10/2026

Conferencia concluida: 26 leituras reais, 13 pontos G A1/A2 por ramo; coordenadas, acao Adicional e componentes coincidentes CAD/BIM dentro da precisao exibida. Soma pretendida18,511247kN. Sem edicao de engenharia ou novo processamento. NAO EXECUTAR: cargas ainda incompletas, sem ELU/ELS aprovados.

Nativos: outputs/H03_CAD_R64_CONFERENCIA_INDIVIDUAL_NAO_EXECUTAR e H03_BIM_R64_CONFERENCIA_INDIVIDUAL_NAO_EXECUTAR. Evidencia/congelados: outputs/Cargas-H03-R64-CONFERENCIA-INDIVIDUAL-NAO-EXECUTAR. Ler LEIA-ME-R64.md e R64-resultado.json. Capturas INVALIDA sao diagnostico de instrumentacao excluido; usar somente *-leitura-UI.txt. R63 preservada com {len(protected)} hashes conferidos.

Tempos brutos de auditoria CAD {fmt(times['CAD']['durationMs'])}; BIM {fmt(times['BIM']['durationMs'])}, com latencia/raciocinio/recuperacao/intervalos, SEM ranking de fluxo. PROXIMO: fechar Q telhado sem duplicacao e P1/P2; demais cargas, vento/combinacoes, ELU/ELS, sincronizacao RVT/DWG e ensaio final pareado. Monografia preservada.

---
Historico anterior:

'''+old,encoding='utf-8')
DEST.mkdir()
for p in OUT.iterdir():
    if p.is_file() and p.suffix.lower() in ('.json','.txt','.md','.py'):
        shutil.copy2(p,DEST/p.name)
        assert sha(p)==sha(DEST/p.name)
print(json.dumps(dict(status=result['status'],protected=len(protected),states={b:{k:v for k,v in s.items() if k!='frozenFiles'} for b,s in states.items()},times={b:fmt(t['durationMs']) for b,t in times.items()}),ensure_ascii=False))

"""Preserva e confere o piloto nativo de duas cargas, sem inferir adequacao estrutural."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, re, shutil, zipfile

root = Path('D:/TCC')
out = root/'outputs/Cargas-H03-R61-TELHADO-G-PARCIAL-NAO-EXECUTAR'
r60dir = root/'outputs/Cobertura-H03-R60-REACOES-PARCIAIS-NAO-EXECUTAR'
r58dir = root/'outputs/Processamento-H03-R58-DIAGNOSTICO-PARCIAL-NAO-EXECUTAR'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def write(name, data):
    (out/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def check(rows):
    for row in rows:
        assert sha(Path(row['path'])) == row['sha256'], row['path']
    return len(rows)
protected = check(read(out/'R61-protegidos-R58.json'))
r60checked = check(read(r60dir/'R60-manifesto.json')['files'])
r59checked = check(read(r60dir/'R60-protegidos-R59.json'))
arr = read(r60dir/'R60-arranjo-reacoes.json')
nodes = arr['reactionNodes']
assert len(nodes) == 13 and arr['equilibrium']['verticalAndFirstMomentsPassed']
pilot = [n for n in nodes if n['id'] in ('RC01', 'RC02')]
assert len(pilot) == 2
typed = [-round(n['gDownKN'], 6) for n in pilot]
assert typed == [-1.419551, -1.419551]
expected_kn = -sum(typed)
expected_tf = expected_kn/9.80665
states, summaries, times, solve = {}, {}, {}, {}
for b, sample in [('CAD', 'RC01'), ('BIM', 'RC02')]:
    text = (out/f'{b}-resultados-texto.txt').read_text(encoding='utf-8')
    full = (out/f'{b}-resultados-UI.txt').read_text(encoding='utf-8')
    reopened = (out/f'{b}-resultados-reaberto-UI.txt').read_text(encoding='utf-8')
    assert text in full and text in reopened
    assert f'H03_{b}_R61_TELHADO_G_PARCIAL_NAO_EXECUTAR' in reopened
    assert 'Estrutura processada com avisos' in (out/f'{b}-conclusao-UI.txt').read_text(encoding='utf-8')
    sampletext = (out/f'{b}-{sample}-forca-lida-UI.txt').read_text(encoding='utf-8')
    assert 'Fz Value: -1.41955' in sampletext and 'Ação Value: Adicional' in sampletext
    assert 'Detectou-se que ocorreu um erro' not in (out/f'{b}-reabertura-UI.txt').read_text(encoding='utf-8')
    def number(pattern):
        m = re.search(pattern, text)
        assert m, pattern
        return float(m[1])
    loads = dict(selfWeightTf=number(r'Peso próprio = ([\d.]+) tf'), additionalTf=number(r'Adicional = ([\d.]+) tf'), liveTf=number(r'Acidental = ([\d.]+) tf'), totalTf=number(r'Total = ([\d.]+) tf'), approxAreaM2=number(r'Área aproximada = ([\d.]+) m²'), ratioKgfM2=number(r'Relação = ([\d.]+) kgf/m²'))
    old = read(r58dir/f'R58-resumo-{b}.json')['loads']
    assert all(loads[k] == old[k] for k in ('selfWeightTf', 'liveTf', 'approxAreaM2'))
    delta = loads['additionalTf']-old['additionalTf']
    assert abs(delta-expected_tf) <= .010001
    assert abs(loads['totalTf']-old['totalTf']-expected_tf) <= .010001
    summaries[b] = dict(loads=loads, displayedAdditionalDeltaTf=delta, expectedDeltaKN=expected_kn, expectedDeltaTfUsingStandardGravity=expected_tf, roundingCompatibilityToleranceTf=.01, summaryPreservedAfterReopen=True, individualSampleRead=sample, allNodesReadIndividually=False, structuralAdequacyApproved=False)
    times[b] = read(out/f'R61-tempo-{b}.json')
    solve[b] = read(out/f'R61-tempo-processamento-{b}.json')
    native = Path(read(out/f'R61-preparacao-{b}.json')['nativeProject'])
    with zipfile.ZipFile(native) as z:
        assert z.testzip() is None
    base, frozen = native.parent.parent, out/f'congelado-{b}'
    assert not frozen.exists(), 'Congelamento ja existe; preservar e usar revisao nova'
    files = []
    for p in sorted(base.rglob('*')):
        if not p.is_file() or p.suffix.lower() in ('.bak', '.bak-g2', '.bak-g3', '.tmp'):
            continue
        q = frozen/p.relative_to(base)
        q.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, q)
        assert sha(p) == sha(q)
        files.append(dict(path=str(p), frozen=str(q), sha256=sha(q)))
    states[b] = dict(nativeProject=str(native), nativeSha256=sha(native), frozenFiles=files, closedNormallyBeforeFreeze=True, summaryReopenedWithoutReprocessing=True, zipIntegrityPassed=True, newIFCExportPerformed=False)
    write(f'R61-estado-{b}.json', states[b])
    write(f'R61-resumo-{b}.json', summaries[b])
assert (out/'CAD-resultados-texto.txt').read_bytes() == (out/'BIM-resultados-texto.txt').read_bytes()
result = dict(revision='H03/R61', atUtc=datetime.now(timezone.utc).isoformat(), scope='Piloto nativo apenas RC01 e RC02 de 13 pontos G do arranjo parcial R60', appliedGPointIds=[n['id'] for n in pilot], pendingGPointIds=[n['id'] for n in nodes if n not in pilot], typedFzKN=typed, expectedAppliedGDownKN=expected_kn, roofVariableLoadsApplied=False, summaries=summaries, summaryTextsEqualAtDisplayedPrecision=True, protectedR58FilesChecked=protected, r60ManifestFilesChecked=r60checked, protectedR59FilesChecked=r59checked, prospectiveAssistedTimes=times, observedProcessingTimes=solve, fullFlowRankingAllowed=False, elementDesignPerformed=False, elsVerified=False, windAndCombinationsComplete=False, postPilotIFCAudited=False, monographEdited=False, sourceRvtDwgEdited=False)
write('R61-resultado.json', result)
fmt = lambda ms: f'{int(ms//60000)} min {(ms%60000)/1000:.3f} s'
report = f'''# H03/R61 — piloto de duas cargas da cobertura

ESTUDO PARCIAL, SEM DIMENSIONAMENTO — NAO EXECUTAR. Criaram-se copias independentes dos conjuntos CAD e BIM R58 no Eberick 2025 Infinity. Inseriram-se apenas RC01 e RC02 do arranjo proposto R60, no pavimento N2, em (110;0) e (330;0) cm. Aplicou-se em ambos Fz=-1,419551 kN por no, acao Adicional, demais componentes nulas. A unidade kN foi conferida no dialogo instalado. O comando mostrou selecao de dois nos em cada ramo. Consultou-se individualmente RC01 no CAD e RC02 no BIM: coordenadas e Fz=-1,41955 kN na precisao exibida. Nao se releram todos os nos individualmente.

O plano inicial previa 13 pontos; limitou-se o ensaio a dois para conferir unidade, sinal, posicao e acrescimo global antes de ampliar. Restam RC03 a RC13. A soma digitada foi {expected_kn:.6f} kN descendentes, enquanto a soma dos 13 pontos propostos R60 e 18,511248 kN. Nenhuma reacao variavel Q_telhado foi aplicada. Preservaram-se G2 do forro e Q das lajes. A discretizacao por nos pertence a concepcao comum, sem classificar essa operacao como defeito de transferencia.

## Resultado observado e persistencia

Processou-se apenas a opcao Analise estatica linear, com Processo P-Delta indicado no resumo; dimensionamento, ELS e dinamica desmarcados. Ambos retornaram Estrutura processada com avisos. O texto completo do resumo e igual na precisao exibida, inclusive apos salvar, fechar, reabrir e consultar resultados armazenados sem reprocessar.

| Grandeza | R58 em ambos | R61 em ambos |
|---|---:|---:|
| Peso proprio (tf) | 75,69 | 75,69 |
| Adicional (tf) | 8,20 | 8,49 |
| Acidental (tf) | 17,11 | 17,11 |
| Total (tf) | 101,00 | 101,29 |
| Area aproximada (m2) | 132,81 | 132,81 |
| Relacao (kgf/m2) | 760,52 | 762,66 |

Usando explicitamente 9,80665 kN/tf, o acrescimo esperado das duas forcas e {expected_tf:.9f} tf. O incremento exibido de 0,29 tf e compativel com a diferenca de dois valores arredondados a 0,01 tf (tolerancia combinada 0,01 tf). Isso nao demonstra precisao interna do programa nem verifica distribuicao local dos esforcos. Gama-Z permaneceu X+1,09/X-1,08/Y+1,06/Y-1,05. A variacao P-Delta passou a 8,85% no caso acidental, 13,97% em vento X, 7,94% em vento Y, 13,76% em desaprumo X e 7,78% em desaprumo Y. Os textos integrais preservam os valores.

Persistem os avisos Relacao de carga por area nao usual para edificios e Os deslocamentos horizontais nao foram verificados. Igualdade de resumos nao certifica equivalencia integral ou atendimento normativo. Nao se compararam esforcos por elemento, nem se verificaram ELU, flechas ELS, vento completo ou fundacoes reais. Nao houve exportacao IFC posterior ao piloto; a geometria atual apos os nos adicionais nao foi auditada por IFC. Os arquivos de origem RVT/DWG e a monografia ficaram intactos.

## Tempos prospectivos assistidos

| Ramo | Piloto ate salvamento | Intervalo observado de processamento |
|---|---:|---:|
| CAD | {fmt(times['CAD']['durationMs'])} | {fmt(solve['CAD']['durationMs'])} |
| BIM | {fmt(times['BIM']['durationMs'])} | {fmt(solve['BIM']['durationMs'])} |

O escopo inclui abertura, dois nos, cargas, consulta amostral, processamento, leitura e salvamento; inclui raciocinio, latencia e aprendizado da interface. O BIM inclui interrupcao de contexto antes do salvamento final. A ordem foi CAD primeiro, BIM depois. O intervalo de processamento termina na leitura da conclusao, nao isola o solver. A verificacao de persistencia ocorreu depois desses cronometros. Nao se mediram tempo humano ativo, tokens ou inferencia isolada da IA. Nao houve chamada direta a API OpenAI nesta rodada. Estes intervalos exploratorios nao autorizam ranking, economia percentual ou tempo total dos fluxos.

## Preservacao e continuidade

Os dois projetos foram salvos, reabertos sem aviso de integridade e fechados normalmente antes do congelamento. Preservaram-se {protected} arquivos protegidos R58 e {r59checked} arquivos R59; conferiram-se {r60checked} entradas do manifesto R60. Os PRJ passaram na integridade ZIP. O conjunto nativo congelado inclui auxiliares/resultados e permanece em D:/TCC; o repositorio recebe apenas memoria, scripts e evidencias textuais pertinentes.

Proximo: ampliar em copias novas para RC03..RC13, com mesmos pontos e acoes nos dois ramos, conferir soma e posicoes; resolver P1/varanda e P2/abrigo elevado, perfis/altimetria/apoios/ancoragens, paredes, tanque1000L/tara/base, escada, bordas, vento/combinacoes e ELU/ELS. A hipotese metalica sem empuxo horizontal exige apoios e contraventamento ainda nao dimensionados. A reserva metalica0,15kN/m2 segue como hipotese. Nao extrapolar os 55,9425m2 nominais parciais para toda a cobertura.

Referencia operacional para sinal e insercao de nos: [AltoQi — cargas concentradas](https://suporte.altoqi.com.br/hc/pt-br/articles/115003467013). A evidencia do piloto provem da interface nativa preservada.
'''
(out/'LEIA-ME-R61.md').write_text(report, encoding='utf-8')
shutil.copy2(Path(__file__), out/Path(__file__).name)
for p in out.glob('*.py'):
    ast.parse(p.read_text(encoding='utf-8'))
write('R61-validacao.json', dict(summaryEquality=True, persistenceBoth=True, pilotLoadIncrementCompatible=True, protectedR58=protected, protectedR59=r59checked, r60Manifest=r60checked, zipIntegrityBoth=True, pythonSyntaxPassed=True, syntheticAssistantTests='registrados separadamente antes do commit', nativeModelCompleted=False))
write('R61-manifesto.json', dict(files=[dict(path=str(p), sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'R61-manifesto.json']))
guide = root/'CONTINUAR-AQUI-H03-2026-10-29.md'
old = guide.read_text(encoding='utf-8-sig')
assert not old.startswith('# Atualizacao R61')
guide.write_text(f'''# Atualizacao R61/R60 - 29/10/2026

R60: arranjo PROPOSTO de8barras metalicas/13reacoes em duas areas nominais parciais55,9425m2; equilibrio vertical e momentos conferidos, P1varanda/P2abrigo e demais pendencias separados. Ver outputs/Cobertura-H03-R60-REACOES-PARCIAIS-NAO-EXECUTAR/LEIA-ME-R60.md e figura R60-arranjo-reacoes.png. Nao dimensionado.

R61: aplicado SOMENTE G de RC01 e RC02, 2de13, em novas copias CAD/BIM R58. N2(110;0)/(330;0)cm, Fz=-1,419551kN cada, Adicional. Consulta amostral CADRC01/BIMRC02. Total digitado2,839102kN. Q_telhado nao aplicado; RC03..RC13 ainda pendentes. Resumos processados iguais e persistentes apos salvar/fechar/reabrir: proprio75,69/adicional8,49/acidental17,11/total101,29tf. Avisos e limitacoes em outputs/Cargas-H03-R61-TELHADO-G-PARCIAL-NAO-EXECUTAR/LEIA-ME-R61.md. So analise estatica linear/PDelta; sem dimensionamento/ELS/vento completo. Sem IFC pos-piloto.

Nativos atuais: outputs/H03_CAD_R61_TELHADO_G_PARCIAL_NAO_EXECUTAR e H03_BIM_R61_TELHADO_G_PARCIAL_NAO_EXECUTAR; congelados R61 com auxiliares, ambos fechados normalmente. R58/R59 preservados. Eberick aberto sem projeto/dialogo. Tempos exploratorios CAD {fmt(times['CAD']['durationMs'])}, BIM {fmt(times['BIM']['durationMs'])}; incluem latencia/raciocinio, BIM interrupcao de contexto; nao ranking. Reabertura QA posterior separada desses intervalos.

Proximo: outras11G em copias novas com conferencia, completar cobertura/acoes e ELU/ELS; sincronizar RVT/DWG somente apos escolher concepcao. Nao alterar monografia. Apoios idealizados, superestrutura apenas, sem fundacoes reais. NAO EXECUTAR.

---
Historico anterior:

'''+old, encoding='utf-8')
print(json.dumps(dict(pilotPoints=2, remainingPoints=11, protectedR58=protected, r60Checked=r60checked, frozenFiles={b:len(s['frozenFiles']) for b,s in states.items()}, summaryEquality=True, expectedDeltaTf=expected_tf), ensure_ascii=False))

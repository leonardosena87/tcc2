"""Consolida auditoria real R63 sem certificar dimensionamento ou ranking."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import re
import shutil
import zipfile

ROOT = Path('D:/TCC')
OUT = ROOT / 'outputs/Cargas-H03-R63-AUDITORIA-G-NAO-EXECUTAR'
DEST = Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r63')


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text(name):
    return (OUT / name).read_text(encoding='utf-8-sig')


def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def summary_from_ui(name):
    return re.search(r'editar Value: (Cargas verticais:[^\n]+)', text(name)).group(1)


def fmt(ms):
    return f'{int(ms // 60000)} min {(ms % 60000) / 1000:.3f} s'


assert not DEST.exists(), 'Preservar evidencia ja versionada'
assert not (OUT / 'R63-manifesto.json').exists(), 'Nao substituir revisao consolidada'
protected = read(OUT / 'R63-protegidos-R62.json')
for row in protected:
    assert sha(Path(row['path'])) == row['sha256'], row['path']

summaries = {}
for branch in ('CAD', 'BIM'):
    value = text(f'{branch}-resultados-texto.txt').strip()
    assert value == summary_from_ui(f'{branch}-resultados-UI.txt')
    assert value == summary_from_ui(f'{branch}-resultados-reaberto-UI.txt')
    assert 'Adicional = 10.05 tf' in value and 'Total = 102.86 tf' in value
    assert 'Estrutura processada com avisos' in text(f'{branch}-conclusao-UI.txt')
    summaries[branch] = value
assert summaries['CAD'] == summaries['BIM']

for node in ('RC07', 'RC08', 'RC13'):
    assert 'Fz Value: 0 ID: 108' in text(f'CAD-{node}-antes-UI.txt')
    assert 'Fz Value: -0.807804' in text(f'CAD-{node}-corrigido-UI.txt')
assert 'Fz Value: -0.807804' in text('CAD-RC12-reaberto-UI.txt')
assert 'Fz Value: -0.0807804' in text('CAD-RC12-unidade-tf-UI.txt')
assert 'Fz Value: -0.807804' in text('BIM-RC07-leitura-UI.txt')
assert 'X Value: 732.5' in text('BIM-RC07-leitura-UI.txt')
assert 'Y Value: 390' in text('BIM-RC07-leitura-UI.txt')

groups = [('RC03', 1.387289, 1), ('RC04-RC05', 2.566112, 2),
          ('RC06', 2.507791, 1), ('RC07-RC08-RC12-RC13', .807804, 4),
          ('RC09-RC10', 1.146561, 2), ('RC11', 1.120503, 1)]
for name, force, count in groups:
    assert f'Fz Value: -{force}' in text(f'BIM-{name}-config-UI.txt')
    assert f'({count} sel.)' in text(f'BIM-{name}-selecao-UI.txt')
new_g = sum(force * count for _, force, count in groups)
full_g = new_g + 2 * 1.419551
assert abs(full_g - 18.511247) < 1e-9
native_factor = .807804 / .0807804
assert abs(native_factor - 10) < 1e-10
assert abs((10.05 - 8.20) - full_g / native_factor) < .010001
assert abs((102.86 - 101.00) - full_g / native_factor) < .010001

states = {}
for branch in ('CAD', 'BIM'):
    pre = read(OUT / f'R63-preparacao-{branch}.json')
    native = Path(pre['nativeProject'])
    base = native.parent.parent
    frozen = OUT / f'congelado-{branch}'
    assert not frozen.exists(), 'Preservar congelamento anterior'
    with zipfile.ZipFile(native) as archive:
        assert archive.testzip() is None
    files = []
    for source in sorted(base.rglob('*')):
        if not source.is_file() or source.suffix.lower() in ('.bak', '.bak-g2', '.bak-g3', '.tmp'):
            continue
        target = frozen / source.relative_to(base)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        assert sha(source) == sha(target)
        files.append(dict(path=str(source), frozen=str(target), sha256=sha(target)))
    states[branch] = dict(nativeProject=str(native), nativeSha256=sha(native), frozenFiles=files,
                          closedBeforeFreeze=True, zipIntegrityPassed=True,
                          summaryReprocessed=True, summaryPersistedAfterReopen=True,
                          all13LoadsIndividuallyRead=False, newIFCExportPerformed=False,
                          designOrServiceabilityApproved=False)
    write(f'R63-estado-{branch}.json', states[branch])

cad_time = read(OUT / 'R63-tempo-CAD.json')
bim_time = read(OUT / 'R63-tempo-BIM.json')
cad_solve = read(OUT / 'R63-tempo-processamento-CAD.json')
bim_solve = read(OUT / 'R63-tempo-processamento-BIM.json')
result = dict(
    revision='H03/R63', atUtc=datetime.now(timezone.utc).isoformat(),
    status='Resumos parciais CAD/BIM coincidentes e persistentes; auditoria individual incompleta',
    protectedR62FilesChecked=len(protected),
    intendedRoofGReactionNodes=13, intendedRoundedRoofGDownKN=full_g,
    addedBimGDownKN=new_g, cadCorrectionsThisRevision=['RC07', 'RC08', 'RC13'],
    cadRC12CorrectionFromR62Persisted=True,
    sampledBimRC07=dict(xCm=732.5, yCm=390, fzKN=-.807804),
    nativeDisplayCalibration=dict(node='RC12', fzKN=-.807804, fzDisplayedTf=-.0807804,
                                  observedKNPerDisplayedTf=native_factor,
                                  physicalStandardKNPerTf=9.80665,
                                  inputUnitsRestoredToKN=True, forcesRescaledToFitSummary=False),
    displayedSummary=dict(ownTf=75.69, additionalTf=10.05, accidentalTf=17.11,
                          totalTf=102.86, areaM2=132.81, ratioKgfM2=774.46),
    displayedSummaryTextIdentical=True, bothSummariesPersistedAfterReopen=True,
    all13LoadsIndividuallyRead=False, aggregateEqualityProvesAllForcesAndPositions=False,
    fullTransferEquivalenceProven=False, roofLoadCaseComplete=False,
    missingLoadTechnicalRootCauseProven=False, cadDwgTransferDefectProven=False,
    prospectiveAssistedTimeCAD=cad_time, prospectiveAssistedTimeBIM=bim_time,
    observedProcessingTimeCAD=cad_solve, observedProcessingTimeBIM=bim_solve,
    fullFlowRankingAllowed=False, isolatedAIEffortMeasured=False,
    newIFCExportPerformed=False, sourceRvtDwgEdited=False, monographEdited=False,
    eluElsApproved=False, foundationDesigned=False)
write('R63-resultado.json', result)

report = f'''# H03/R63 — auditoria e ampliação das cargas permanentes da cobertura

ESTUDO PARCIAL, NÃO EXECUTAR. Os dois ramos apresentaram o mesmo texto de resumo de análise e o conservaram após salvar, fechar e reabrir. Isso comprova coincidência dos valores exibidos neste estado parcial. Não comprova igualdade de todos os esforços, posições, armaduras, combinações ou conformidade normativa integral.

## Desenvolvimento real no Eberick

Utilizou-se o AltoQi Eberick 2025 Infinity instalado. A genealogia permanece AutoCAD 2027/DWG2D e Revit 2027.2/IFC adaptado, conforme os registros anteriores. Nesta revisão não houve nova operação no AutoCAD ou Revit, exportação IFC, alteração dos arquivos de origem ou edição da monografia. Criaram-se cópias independentes dos congelados R62. O CAD partiu do lançamento R62 já ampliado; o BIM partiu da cópia R62 ainda equivalente ao piloto R61.

No CAD, a consulta individual revelou Fz=0 na ação Adicional em RC07, RC08 e RC13. Corrigiu-se cada ponto para -0,807804 kN, confirmando o diálogo de carga e o diálogo do nó. RC12 já continha -0,807804 kN após reabrir, confirmando a correção salva na R62. O resumo R62 de 9,73 tf era anterior à correção de RC12 e permanece histórico. Não se demonstrou a causa técnica da falta de gravação do grupo; classificou-se a ocorrência como correção de lançamento/operação, sem atribuí-la a defeito DWG.

No BIM inseriram-se onze nós RC03..RC13 por coordenadas em centímetros e aplicaram-se seis grupos de Fz, ação Adicional, com seleção 1/2/1/4/2/1. RC01 e RC02 vieram do piloto R61 e não foram duplicados. Conferiu-se o retorno a Comando após cada aplicação. A leitura posterior de RC07 confirmou X732,5 cm/Y390 cm e Fz=-0,807804 kN. Os registros de seleção e a soma global não substituem a leitura individual de todos os treze pontos, ainda pendente.

O conjunto pretendido contém RC01/RC02=1,419551 kN cada; RC03=1,387289; RC04/RC05=2,566112 cada; RC06=2,507791; RC07/RC08/RC12/RC13=0,807804 cada; RC09/RC10=1,146561 cada; RC11=1,120503 kN. Adotou-se sinal Fz negativo para gravidade. A soma dos valores arredondados digitados é {full_g:.6f} kN; trata-se apenas da ação permanente dos trechos A1/A2 do mapa R60, e não da cobertura integral ou do carregamento total do edifício.

## Calibração de unidades e esclarecimento da R62

Na mesma carga RC12, sem alterar a força, mudou-se temporariamente apenas Sistema/Cargas/Concentrada de kN para tf. Leu-se -0,807804 kN e depois -0,0807804 tf. A relação observada nesta interface instalada é 10 kN por tf exibida. Restaurou-se a unidade de entrada para kN. Não se modificaram as forças para ajustar o resumo.

Essa relação observada é uma convenção da interface verificada neste exemplar; não redefine a conversão física de 1 tf=9,80665 kN. A R62 empregara 9,80665 kN/tf na estimativa sem ter confirmado a conversão nativa. A R63 esclarece essa limitação e preserva o relatório anterior. A comparação com os resumos nativos utiliza agora a relação medida, explicitamente identificada.

Os 18,511247 kN correspondem a 1,8511247 tf nessa exibição. O aumento adicional R58→R63 de 8,20 para 10,05 tf é compatível dentro do arredondamento de 0,01 tf de dois resumos. A diferença total 101,00→102,86 tf também é compatível com essa tolerância. O acréscimo R62→R63 de aproximadamente 0,32 tf é compatível com quatro cargas de 0,807804 kN: RC12 corrigida na R62, mais três corrigidas nesta revisão. A compatibilidade global apoia a reconciliação, sem provar todas as posições e forças individualmente.

## Resultados exibidos e qualidade da informação

Nos dois ramos: peso próprio75,69 tf; adicional10,05 tf; acidental17,11 tf; total102,86 tf; área aproximada132,81 m²; relação774,46 kgf/m². O total utiliza a precisão interna do programa e pode diferir da soma de parcelas já arredondadas. O texto completo dos resumos CAD/BIM coincidiu, incluindo Gama-Z X+/X-/Y+/Y-=1,09/1,08/1,06/1,05 e Processo P-Delta. Conferiu-se a persistência de cada resumo após fechamento/reabertura, sem novo processamento nessa consulta.

Processou-se somente a análise estática linear; o resumo indicou P-Delta. Dimensionamento, deslocamentos ELS e análise dinâmica ficaram desmarcados. O Eberick retornou Estrutura processada com avisos, relação carga/área não usual e deslocamentos horizontais não verificados. Gama-Z abaixo do limite exibido não constitui aprovação estrutural ou verificação completa de vento/serviço. A coincidência do resumo não certifica segurança ou equivalência integral dos modelos.

## Tempos e esforço assistido

CAD: {fmt(cad_time['durationMs'])}. Escopo: leitura/correção de três pontos, conferência de RC12, investigação de unidades, recálculo, salvamento e fechamento; inclui raciocínio, latência e intervalo entre mensagens. BIM: {fmt(bim_time['elapsedMs'])}. Escopo: inserção dos onze nós, seis grupos de carga, amostra RC07, processamento, salvamento e primeiro fechamento; inclui raciocínio, latência e continuidade entre mensagens. As verificações adicionais após reabrir ficaram fora desses dois intervalos principais.

Intervalos observados de processamento: CAD {fmt(cad_solve['durationMs'])}; BIM {fmt(bim_solve['elapsedMs'])}. Ambos incluem captura e latência até registro da conclusão; não representam tempo puro do solver. No BIM a primeira captura retornou acessibilidade nula e exigiu atualização, sem repetir o comando de processamento. Houve ainda uma tentativa de clique UIA indisponível no diálogo de RC06, recuperada por observação e clique visual, sem alterar a carga.

Os escopos são diferentes: o CAD realizou correção/auditoria de uma tentativa anterior; o BIM realizou ampliação. Não calcular economia percentual ou declarar vencedor com esses intervalos. A IA apoiou análise, preparação de scripts, operação pela interface e organização das evidências; não se mediu separadamente tempo cognitivo, tokens, custo ou trabalho humano ativo. Os testes automatizados não fizeram chamadas reais à API OpenAI e não substituem validação nativa. Para o ensaio final, usar entradas comuns congeladas, critérios de início/fim iguais e registrar separadamente transferência, reconstrução, correções, cálculo, conferência, espera e intervenção humana.

## Preservação e continuidade

Verificaram-se {len(protected)} arquivos protegidos R62 por SHA-256. Congelaram-se os conjuntos CAD/BIM após fechar os projetos; verificou-se a integridade ZIP de ambos os PRJ e a igualdade dos hashes entre cópias. Evidência textual da interface, tempos, scripts, estados e manifesto acompanham esta revisão. O congelamento preserva PRJ e seus arquivos associados; não distribuir somente o PRJ sem conferir dependências.

Próxima etapa: completar a auditoria individual dos treze pontos nos dois ramos, conferindo coordenadas, ação e força após reabrir. Depois fechar a ação variável do telhado sem duplicar a sobrecarga já existente nas lajes e resolver P1/varanda e P2/abrigo/altimetria. Permanecem perfis/apoios/ancoragens metálicas, paredes e aberturas, reservatório1000 L/tara/base, escada/bordas, vento/combinações, ELU/ELS e compatibilização das origens RVT/DWG. O estudo continua restrito à superestrutura com apoios idealizados, sem fundações reais dimensionadas. A viga20x30 cm e a folga geométrica ao forro continuam sem aprovação de flecha/execução.
'''
(OUT / 'LEIA-ME-R63.md').write_text(report, encoding='utf-8')
shutil.copy2(Path(__file__), OUT / Path(__file__).name)
for source in OUT.glob('*.py'):
    ast.parse(source.read_text(encoding='utf-8'))
write('R63-validacao.json', dict(evidenceSyntaxAndHashesPassed=True, protectedR62Files=len(protected),
                                bothBranchesProcessedAndReopened=True,
                                displayedSummariesIdentical=True, all13LoadsIndividuallyRead=False,
                                syntheticAssistantTestsThisTurn=dict(passed=9, failed=0,
                                                                    nativeStructuralValidation=False),
                                liveOpenAIApiCalls=False))
write('R63-manifesto.json', dict(files=[dict(path=str(p), sha256=sha(p))
                                      for p in sorted(OUT.rglob('*'))
                                      if p.is_file() and p.name != 'R63-manifesto.json']))
guide = ROOT / 'CONTINUAR-AQUI-H03-2026-10-29.md'
old = guide.read_text(encoding='utf-8-sig')
assert not old.startswith('# Atualizacao R63')
guide.write_text(f'''# Atualizacao R63 — 29/10/2026

R63: resumos CAD/BIM parciais coincidentes e persistentes apos salvar/fechar/reabrir. Adicional10,05tf/total102,86tf. NAO EXECUTAR: sem dimensionamento/ELS aprovados ou cargas completas. Nativos: outputs/H03_CAD_R63_AUDITORIA_G_NAO_EXECUTAR e H03_BIM_R63_AUDITORIA_G_NAO_EXECUTAR; congelados/evidencias: outputs/Cargas-H03-R63-AUDITORIA-G-NAO-EXECUTAR. Ler LEIA-ME-R63.md e R63-resultado.json.

CAD: RC07/08/13 lidos zerados, corrigidos individualmente; RC12 corrigida na R62 persistiu. BIM: onze nos RC03..RC13 e seis grupos G aplicados; RC01/02 herdados sem duplicacao; RC07 relido e confirmado. Nao foram relidos todos os treze pontos individualmente. Resumos iguais nao comprovam posicoes/esforcos/armaduras integrais.

Unidades: mesma carga RC12 mostrou -0,807804kN/-0,0807804tf apos mudar somente exibicao. Relacao nativa observada10kN/tf, distinta da conversao fisica9,80665kN/tf usada sem calibracao na R62. Entrada restaurada a kN; nenhuma forca reajustada para caber no resumo. Total G pretendido18,511247kN apenas A1/A2. R62 preservada; nao atribuir suas faltas a DWG.

Tempos assistidos CAD {fmt(cad_time['durationMs'])}; BIM {fmt(bim_time['elapsedMs'])}, escopos diferentes e intervalos/latencia incluidos, SEM ranking. Programas fechados antes do congelamento, ambos PRJ integro e {len(protected)} arquivos R62 preservados. Nao houve edicao da monografia ou origens RVT/DWG.

PROXIMO: auditoria individual das treze cargas e coordenadas nos dois ramos; Q telhado sem duplicacao, P1/P2 e demais cargas; vento/combinacoes; ELU/ELS e compatibilizacao. Ensaio final de tempos exige entradas/escopos pareados e separacao de correcao, transferencia e espera. Superestrutura com apoios idealizados.

---
Historico anterior:

''' + old, encoding='utf-8')
DEST.mkdir()
for source in OUT.iterdir():
    if source.is_file() and source.suffix.lower() in ('.json', '.md', '.txt', '.py'):
        shutil.copy2(source, DEST / source.name)
        assert sha(source) == sha(DEST / source.name)
print(json.dumps(dict(status=result['status'], protectedR62=len(protected),
                      frozen={b: len(s['frozenFiles']) for b, s in states.items()},
                      cadTime=fmt(cad_time['durationMs']), bimTime=fmt(bim_time['elapsedMs'])), ensure_ascii=False))

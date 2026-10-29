"""Inventario rastreavel dos tempos; nao soma intervalos de escopos distintos."""
from pathlib import Path
from datetime import datetime,timezone
from time import perf_counter
from collections import Counter
import json,hashlib,re,shutil,ast
root=Path('D:/TCC');out=root/'outputs/Resultados-H03-R69-TEMPOS-EXPLORATORIOS'
dest=Path('C:/Users/leona/OneDrive/Documentos/FTC/10º Semestre/TCC2/tcc-assistente/estudos/h03-r69')
assert not out.exists() and not dest.exists()
tick=perf_counter();started=datetime.now(timezone.utc).isoformat()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(root/'outputs/Compatibilizacao-H03-R68-PORTA-P3-ESTUDO/R68-manifesto.json')['files']
for r in protected:assert sha(Path(r['path']))==r['sha256'],r['path']
def endpoint(v):
    if isinstance(v,dict):
        for k in ('utc','iso','atUtc','startedAt','startUtc'):
            if k in v:return endpoint(v[k])
        return None
    if not isinstance(v,str):return None
    try:
        t=datetime.fromisoformat(v.replace('Z','+00:00'))
        return t if t.tzinfo is not None else None
    except ValueError:return None
rows=[]
for directory in sorted((root/'outputs').iterdir()):
    if not directory.is_dir():continue
    for file in sorted(directory.glob('*tempo*.json')):
        a=read(file)
        assert isinstance(a,dict),file
        keys=[k for k in ('durationMs','elapsedMs','elapsedWallMs') if isinstance(a.get(k),(float,int))]
        starts=[(k,endpoint(a.get(k))) for k in ('startUtc','startedAt','startedAtUtc','started','start') if k in a]
        ends=[(k,endpoint(a.get(k))) for k in ('endUtc','endedAt','finishedAtUtc','finish','end','utc') if k in a]
        start=next((t for k,t in starts if t is not None),None);end=next((t for k,t in ends if t is not None),None)
        value=a[keys[0]] if keys else None
        assert value is None or value>=0,file
        nested=any(k in a for k in ('records','sessions','session','events'))
        kind='intervalo-com-duracao' if value is not None else 'container-consolidado-nao-somar' if nested else 'inicio-ou-registro-sem-duracao'
        branch=a.get('branch',a.get('flow'))
        if branch is None:
            match=re.search(r'(?i)(CAD|BIM|REVIT|COMUM)',file.name)
            branch=match.group(1).upper() if match else 'nao-identificado'
        row=dict(id=f'T{len(rows)+1:03}',path=str(file),sha256=sha(file),sourceDirectory=directory.name,sourceName=file.name,classification=kind,branch=str(branch),durationMs=value,durationField=keys[0] if keys else None,otherDurationFields={k:a[k] for k in keys[1:]},startUtc=start.isoformat() if start else None,endUtc=end.isoformat() if end else None,utcDifferenceMs=(end-start).total_seconds()*1000 if start and end else None,scope=a.get('actualScope',a.get('scope',a.get('stage',a.get('meaning','Consultar fonte')))),containsNestedRecords=nested,sourceRankingDeclarations={k:v for k,v in a.items() if any(s.lower() in k.lower() for s in ('rank','compar','totalFlow','wholeFlow','wholeWorkflow'))},recordIncludedInFinalRanking=False,aggregateTotalComputed=False)
        if row['utcDifferenceMs'] is not None and value is not None:row['durationMinusUTCms']=value-row['utcDifferenceMs']
        rows.append(row)
assert rows and len({r['path'] for r in rows})==len(rows)
# Subintervalos podem estar contidos nos intervalos de operacao: jamais somar ambos.
overlaps=[]
for i,a in enumerate(rows):
    if a['durationMs'] is None or not a['startUtc'] or not a['endUtc']:continue
    aa=endpoint(a['startUtc']);ab=endpoint(a['endUtc'])
    for b in rows[i+1:]:
        if b['durationMs'] is None or not b['startUtc'] or not b['endUtc']:continue
        ba=endpoint(b['startUtc']);bb=endpoint(b['endUtc']);seconds=(min(ab,bb)-max(aa,ba)).total_seconds()
        if seconds>0:overlaps.append(dict(a=a['id'],b=b['id'],overlapSeconds=seconds,meaning='Sobreposicao temporal dos intervalos declarados; nao prova duplicacao indevida ou trabalho paralelo real'))
counts=dict(Counter(r['classification'] for r in rows))
out.mkdir()
def write(n,v):(out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write('R69-protegidos-R68.json',protected)
write('R69-inventario-tempos.json',dict(revision='H03/R69',atUtc=datetime.now(timezone.utc).isoformat(),searchScope='Somente arquivos *tempo*.json diretamente dentro de cada pasta filha de D:/TCC/outputs; nao e auditoria de todo log/API/servidor',counts=counts,files=len(rows),records=rows,overlappingDeclaredIntervals=overlaps,flowGrandTotalsComputed=False,finalRankingComputed=False,aiInferenceOrHumanActiveTimeComputed=False))
chosen=[]
for revision in (53,54,56,57,58,61,62,63,64):
    pair=[]
    for b in ('CAD','BIM'):
        candidates=[r for r in rows if r['sourceName']==f'R{revision}-tempo-{b}.json' and 'H03' in r['sourceDirectory']]
        if len(candidates)!=1 or candidates[0]['durationMs'] is None:break
        pair.append(candidates[0])
    if len(pair)==2:chosen.append((revision,*pair))
def fmt(ms):return f'{int(ms//60000)} min {ms%60000/1000:.3f} s'
table='\n'.join(f'| R{rev} | {fmt(a["durationMs"])} | {fmt(b["durationMs"])} | Exploratória; consultar escopos individuais |' for rev,a,b in chosen)
(out/'LEIA-ME-R69.md').write_text(f'''# H03/R69 — inventário dos tempos e preparação dos resultados

Inventariaram-se {len(rows)} arquivos de tempos nas pastas de primeiro nível de outputs. Foram classificados {counts.get('intervalo-com-duracao',0)} arquivos com duração principal explícita, {counts.get('container-consolidado-nao-somar',0)} contêineres/consolidados e {counts.get('inicio-ou-registro-sem-duracao',0)} registros sem duração principal. A cobertura da busca é explícita: não inclui tempos em work, pacote de entrega, congelados, banco do painel ou logs de API não chamados *tempo*.json. Não se criou uma contagem de todo o esforço do TCC.

Preservaram-se caminho, hash, campo original da duração, limites UTC quando disponíveis, escopo e declarações de comparabilidade. Os campos ausentes são nulos, nunca zero. Datas sem fuso não foram adivinhadas. Não se expandiram contêineres históricos para evitar recontar registros que também existem em arquivos separados. Não se somaram duração geral, exportação e processamento, pois podem representar intervalos sobrepostos. O JSON aponta{len(overlaps)} pares com sobreposição temporal dos limites declarados, que são candidatos a revisão, não erros comprovados.

## Intervalos exploratórios recentes H03

| Revisão | CAD, duração assistida declarada | BIM, duração assistida declarada | Uso nos resultados |
|---|---:|---:|---|
{table}

Os números acima permanecem resultados operacionais parciais. Os escopos não são necessariamente iguais: por exemplo, na R63 o CAD corrigiu pontos anteriores e o BIM inseriu onze nós; na R64 ambos leram13 pontos, mas o BIM incluiu recuperação da captura e os intervalos incorporaram latência/continuidade. O inventário não transforma uma sequência exploratória em ensaio controlado. Não se calculou percentual de economia, tempo total por fluxo ou vencedor. R66 sem intervalo completo recuperável foi mantida como ausência de dado, não como0s; ela é documentada no relatório próprio e não apareceu artificialmente nesta tabela.

## Como esses dados entram no TCC

Apresentar o histórico como desenvolvimento e aperfeiçoamento do protótipo: duração, escopo, produto entregue, ocorrência e evidência. Distinguir três origens de correção: interpretação da arquitetura/concepção comum; representação ou transferência demonstrada; operação/instrumentação. Uma falta de carga após aplicação nativa ou perda de foco não é automaticamente erro DWG/IFC. A correção de referência da porta na R68 é interpretação geométrica comum; não é vantagem comprovada de um programa.

O comparativo principal deve ser o ensaio pareado definido no protocolo separado. Informar explicitamente que o teste de uma edificação e de versões/configurações determinadas não permite generalização estatística para todos os projetos. Não reconstruir tempo ativo humano por tempo de conversa nem inferência da IA por duração de script. Quando houver log real de chamada IA, tempo, tokens e custo devem ter fonte/ID e ser apresentados em campos próprios, sem duplicar um subintervalo já incluído no tempo total.

## Preservação

Conferiram-se os hashes de{len(protected)} arquivos R68. Nenhum registro histórico, nativo, monografia ou arquivo de origem foi alterado. Os testes do instrumento de tempos, quando executados, são simulados e não produzem medições empíricas dos programas. A última configuração de engenharia conferida permanece R64; R65Q e R66ações continuam pendentes.
''',encoding='utf-8')
(out/'PROTOCOLO-ENSAIO-PAREADO.md').write_text('''# Protocolo do ensaio final — dois fluxos com automação

Este protocolo define atividades futuras, não declara execução concluída. Fluxos: AutoCAD2027→DWG2D→Eberick2025Infinity e Revit2027.2→IFC adaptado→Eberick2025Infinity. Registrar os números exatos instalados e versões do suplemento/adaptador na abertura de cada ensaio. Os dois fluxos incluem automação. Não apresentar CAD como desenho manual se foi gerado por rotina.

## Condição para começar

Congelar a mesma arquitetura, referência comum de coordenadas/unidades, hipótese estrutural e matriz de propriedades/cargas, com hashes. Fechar antes os níveis, seções, cargas, critérios de apoios idealizados e configuração normativa comum; guardar pendências que impeçam uma conclusão. Não usar uma alternativa ainda em revisão como se fosse uma solução final aprovada. Guardar cópias independentes, sem transferir o PRJ pronto de um ramo ao outro.

Separar desenvolvimento comum do protótipo e treinamento das medições finais. Definir antes do primeiro ensaio os entregáveis e a tolerância por grandeza. Tolerância computacional de caixa IFC, precisão exibida pela UI e tolerância de execução são conceitos distintos. Não selecionar tolerância depois de observar uma divergência para fazê-la desaparecer.

## Unidades de tempo e limites iguais

Usar tempo decorrido prospectivo e iniciar o registro persistente ANTES do comando. Salvar imediatamente início UTC, relógio monotônico quando suportado, identificador da sessão, fluxo, etapa, revisão/hashes e operador. Ao concluir, persistir fim, duração e evidência de término. Se o runtime/servidor cair, preservar o intervalo como interrompido, sem estimar o trecho ausente ou continuar o mesmo relógio monotônico em outro processo.

Etapas para ambos os ramos:

1. Geração nativa: começar com arquitetura/matriz comum já congeladas e aplicativo aberto no estado definido; terminar com esboço nativo salvo e exportação de controle disponível. Incluir seleção/configuração e execução da rotina; registrar falhas/repetições.
2. Preparação do intercâmbio: começar no comando de exportação; terminar no arquivo aceito pelo receptor, incluindo adaptação IFC ou preparação DWG necessárias. Manter subintervalos identificados sem somá-los novamente ao intervalo maior.
3. Transferência e reconstrução no Eberick: começar ao escolher a entrada; terminar quando houver elementos nativos e dados exigidos para a auditoria. Reconstrução prevista no fluxo CAD é trabalho do fluxo, não automaticamente defeito de transferência. A adaptação necessária no BIM também integra o fluxo completo.
4. Auditoria e correções: começar ao confrontar a matriz esperada com o receptor; terminar após corrigir e verificar novamente todos os itens do escopo. Medir o esforço e classificar a causa, preservando valores antes/depois e evidência. Ajustes comuns devem ser aplicados aos dois ramos e separados das perdas de transferência.
5. Processamento e conferência: usar os mesmos critérios de análise/dimensionamento e saída esperada. Separar intervalo observado entre comando e conclusão de tempo puro do solver, se o programa fornecer este último. Resultado com aviso, erro ou verificação incompleta não recebe status de aprovação só porque o processamento terminou.
6. Documentação/compatibilização: verificar mesma lista de produtos e atualização após uma alteração comum predefinida; terminar com nativos salvos, reabertos, produtos e relatórios conferidos. Não contar texto manual desatualizado como dado estrutural corrente.

Manter fora do relógio de produtividade as esperas pessoais, indisponibilidade de licença ou intervenção humana não executada; preservá-las no tempo bruto com motivo e limites reais. Se não houver início/fim da espera, não descontar duração estimada: marcar intervalo contaminado e repetir o ensaio. Navegação e correção normalmente necessárias à tarefa permanecem incluídas. Não excluir uma tentativa simplesmente porque foi lenta ou falhou.

## Repetição e aprendizagem

Planejar pelo menos3 pares completos, com ordem alternada: CAD/BIM, BIM/CAD, CAD/BIM. Manter hardware, versões, arquivos e condições de inicialização. Identificar condição fria/quente e cache sem afirmar limpeza se não foi verificada. Executar familiarização separada e registrar sua duração. Os três pares não tornam a amostra de uma edificação representativa de toda a Engenharia Civil; reportar aprendizagem e limitações. Se não for possível repetir, apresentar um estudo pareado descritivo sem inferência estatística.

## Qualidade da informação e contagem de correções

Antes do ensaio, definir a matriz esperada por classe/elemento e campo: unidade/origem, posição/nível/seção, material, classificação estrutural, carga/ação, identificação e ligação analítica verificável. Atribuir nulo ao não verificado; ausência e valor zero não são equivalentes. Conferir por posição e identidade de origem quando disponível, sem exigir que a numeração nativa CAD/BIM seja igual.

Calcular completude apenas com denominador explícito: campos exigidos presentes e semanticamente válidos/campos exigidos inspecionados; informar separadamente campos não inspecionados. Geometria coincidente de caixas envolventes não prova identidade de malha, conexão analítica ou segurança. Para retenção de atributos, restringir o denominador aos atributos que de fato existiam na origem e estavam no escopo contratado de intercâmbio. Atributo criado só no receptor é complementação, não perda comprovada na exportação.

Contar cada ocorrência uma vez por elemento/campo/regra violada. Separar quantidade de ocorrências, quantidade de operações para corrigi-las e duração. Um comando que corrige10elementos não equivale a uma única perda; dez cliques para corrigir um campo não equivalem a dez defeitos. Classificação mínima: concepção/interpretação comum; transferência/formato demonstrada; representação esperada; operação/instrumentação; causa indeterminada. Guardar justificativa e evidência. Não forçar a categoria para explicar um ranking.

Na compatibilização, confrontar portas/janelas/circulação, faces de paredes, forro, pisos, escada, reservatório e cobertura. Manter ocorrência aberta até a verificação correspondente; corrigir uma referência aproximada não significa alterar a arquitetura original. Verificações ELU/ELS e compatibilidade geométrica têm critérios próprios e precisam ser relatadas separadamente.

## Análise final

Para cada par completo, informar T_CAD, T_BIM e diferença T_CAD−T_BIM, com escopo idêntico e soma de intervalos não sobrepostos. A diferença percentual em relação ao CAD é100×(T_CAD−T_BIM)/T_CAD; calcular somente com T_CAD>0 e ambos concluídos e comparáveis. Valor positivo indica menor duração BIM naquele par; negativo indica maior duração. Não atribuir causalidade ao programa isoladamente quando o fluxo também envolve rotinas, adaptador e operação assistida.

Com repetições válidas, apresentar mediana e faixa mín–máx por etapa e total, além dos valores individuais; manter tentativas inválidas/interrompidas em quadro próprio com motivo. Informar completude, perdas verificadas, complementações e correções ao lado dos tempos. Não produzir um índice único de qualidade com pesos arbitrários. Um fluxo rápido com campos pendentes não é equivalente ao fluxo concluído.

Separar esforço assistido da IA (tarefas e intervenções observadas) de inferência efetivamente medida por log/API, tokens/custo registrados e trabalho humano ativo. Sem fonte, usar “não medido”. Preparação comum não deve ser duplicada no total CAD e BIM. Simulações/testes automatizados validam o instrumento, não constituem uma rodada real em Revit/AutoCAD/Eberick.

## Pacote de evidências

Entregar manifesto, arquitetura/matriz comum referenciadas por hash, versões, sessões/intervalos, ocorrências/correções, nativos com dependências, exportações, relatórios e verificações de reabertura. Preservar os originais e separar o estudo exploratório das rodadas finais. Na ausência de sondagem, manter explícita a delimitação à superestrutura e os apoios idealizados. Este protocolo não altera a monografia ou aprova execução.
''',encoding='utf-8')
shutil.copy2(Path(__file__),out/Path(__file__).name);ast.parse(Path(__file__).read_text(encoding='utf-8'))
write('R69-validacao.json',dict(sourceHashCount=len(rows),uniquePaths=True,negativeDurationsFound=False,protectedR68FilesChecked=len(protected),historicalFilesEdited=False,flowGrandTotalsComputed=False,startedUtc=started,endUtc=datetime.now(timezone.utc).isoformat(),scriptElapsedSeconds=perf_counter()-tick,scriptDurationIsFlowTime=False))
write('R69-manifesto.json',dict(files=[dict(path=str(p),sha256=sha(p)) for p in sorted(out.iterdir()) if p.is_file()]))
dest.mkdir()
for p in out.iterdir():shutil.copy2(p,dest/p.name);assert sha(p)==sha(dest/p.name)
guide=root/'CONTINUAR-AQUI-H03-2026-10-29.md';old=guide.read_text(encoding='utf-8-sig')
guide.write_text('''# Atualizacao R69 — tempos historicos e protocolo final

Inventario rastreavel dos arquivos*tempo*.json de primeiro nivel de outputs, com duracoes/escopos/hashes e deteccao de sobreposicoes; SEM soma geral ou ranking. Protocolo do ensaio pareado define dois fluxos automatizados, etapas, tempos persistidos, correcao/completude e3pares com ordem alternada. Rodadas futuras ainda NAO executadas. Ler outputs/Resultados-H03-R69-TEMPOS-EXPLORATORIOS/LEIA-ME-R69.md e PROTOCOLO-ENSAIO-PAREADO.md. Sem monografia/nativos alterados. Engenharia permaneceR64; Q_R65 e acoesR66pendentes; referenciaP3R68 deve prevalecer sobre aproximacaoR34/R67.

---
Historico anterior:

'''+old,encoding='utf-8')
print(json.dumps(dict(files=len(rows),counts=counts,declaredOverlaps=len(overlaps),recentPairs=len(chosen),ranking=False),ensure_ascii=False))

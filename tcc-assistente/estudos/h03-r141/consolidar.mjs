import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {utc} from '../h03-r86/inventariar-tempos.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const phases={125:'Consulta de unidades, segmento retomado',126:'Tentativa de faixa de parede descartada',127:'Consulta do apoio W17',129:'Tentativa W15 sem lançamento salvo',130:'Lançamento isolado W15 e releitura',131:'Análise parcial W15 e releitura',132:'Exportação analítica W15 e controle',133:'Refinamento L4/W15 e análise parcial',134:'Controle L4 de mesma malha sem W15',135:'Lançamento isolado W20 e recuperação de evidências',136:'Análise parcial W20, malha inicial',137:'Refinamento L3/W20 e análise parcial',138:'Controle L3 de mesma malha sem W20',139:'Consulta de processo de análise e vínculos',140:'Consulta gráfica G2 com W20 e controle'};
const sha=b=>createHash('sha256').update(b).digest('hex');

export function normalize(v,{revision,name,source,sha256}) {
  const dates=keys=>keys.map(k=>utc(v[k])).find(Boolean)??null;
  let startUtc=dates(['inicio_utc','startUtc','startedAtUtc','startedAt','start']);
  if(!startUtc&&v.endUtc&&v.elapsedSeconds!==undefined)startUtc=utc(v.utc);
  const endUtc=dates(['fim_utc','fim_primeira_observacao_utc','endUtc','endedAtUtc','endedAt','end','endFirstFinishRecorded']);
  const durationCandidates=[];
  for(const k of ['duracao_ms','durationMs','elapsedMs','wallMs','elapsedWallMs','commandToRecordedFinishMs','commandToFirstObservedFinishMs']) {
    if(v[k]!==undefined){if(typeof v[k]!=='number'||!Number.isFinite(v[k])||v[k]<0)throw Error('Duração inválida: '+k);durationCandidates.push({field:k,ms:v[k]});}
  }
  if(v.elapsedSeconds!==undefined){if(typeof v.elapsedSeconds!=='number'||!Number.isFinite(v.elapsedSeconds)||v.elapsedSeconds<0)throw Error('Duração inválida: elapsedSeconds');durationCandidates.push({field:'elapsedSeconds',ms:v.elapsedSeconds*1000});}
  const utcDifferenceMs=startUtc&&endUtc?Date.parse(endUtc)-Date.parse(startUtc):null;
  if(utcDifferenceMs!==null&&utcDifferenceMs<0)throw Error('Fim anterior ao início');
  const durationMs=durationCandidates[0]?.ms??utcDifferenceMs;
  const inferredBranch=/^CAD(?:-|\.)/.test(name)?'CAD':/^BIM(?:-|\.)/.test(name)?'BIM':null;
  const category=/processamento/.test(name)?'comando_ate_observacao_de_termino':/recuperacao/.test(name)?'recuperacao_de_evidencia':name.endsWith('consulta-fim.json')?'consulta_de_resultados':/tentativa/.test(name)||revision===129?'tentativa_descartada':'sessao_exploratoria';
  return {id:`R${revision}/${name}`,revision,name,source,sha256,branch:inferredBranch,
    branchOrigin:inferredBranch?'prefixo do arquivo':'não atribuída: atividade compartilhada ou escopo não inequívoco',
    category,phase:phases[revision]??'Escopo não classificado',
    scope:v.scope??v.tipo??v.limit??v.escopo??null,startUtc,endUtc,durationMs,
    durationOrigin:durationCandidates.length?'campo explícito do registro':utcDifferenceMs!==null?'diferença de horários UTC, sem medição monotônica declarada':'não disponível',
    durationCandidates,utcDifferenceMs,durationMinusUtcMs:durationCandidates.length&&utcDifferenceMs!==null?durationCandidates[0].ms-utcDifferenceMs:null,
    parentIntervalIds:[],eligibleForFinalFlowRanking:false,pureSolverTime:false,
    isolatedAIInferenceMs:null,humanActiveMs:null,tokens:null,cost:null};
}

export function relate(rows) {
  const overlaps=[];
  for(let i=0;i<rows.length;i++) {
    const a=rows[i];if(!a.startUtc||!a.endUtc||a.durationMs===null)continue;
    for(const b of rows.slice(i+1)) {
      if(!b.startUtc||!b.endUtc||b.durationMs===null)continue;
      const ms=Math.min(Date.parse(a.endUtc),Date.parse(b.endUtc))-Math.max(Date.parse(a.startUtc),Date.parse(b.startUtc));
      if(ms<=0)continue;
      overlaps.push({a:a.id,b:b.id,overlapMs:ms,parallelExecutionProven:false});
    }
    if(a.category==='comando_ate_observacao_de_termino') {
      a.parentIntervalIds=rows.filter(b=>b!==a&&b.revision===a.revision&&b.branch===a.branch&&b.category==='sessao_exploratoria'&&b.startUtc&&b.endUtc&&Date.parse(b.startUtc)<=Date.parse(a.startUtc)&&Date.parse(b.endUtc)>=Date.parse(a.endUtc)).map(b=>b.id);
    }
  }
  return overlaps;
}

export async function consolidate(output) {
  const rows=[];const recordsRoot=path.dirname(here);
  for(let revision=125;revision<=140;revision++) {
    const dir=path.join(recordsRoot,`h03-r${revision}`);
    for(const name of (await fs.readdir(dir)).sort()) {
      if(!/\.json$/.test(name)||!(/tempo/i.test(name)||name.endsWith('consulta-fim.json')))continue;
      const file=path.join(dir,name),bytes=await fs.readFile(file),v=JSON.parse(bytes.toString('utf8').replace(/^\uFEFF/,''));
      rows.push(normalize(v,{revision,name,source:path.relative(path.resolve(here,'../../..'),file).replaceAll('\\','/'),sha256:sha(bytes)}));
    }
  }
  const overlaps=relate(rows);
  const legacyFile=path.join(recordsRoot,'h03-r124/R124-resumo.json'),legacyBytes=await fs.readFile(legacyFile),legacy=JSON.parse(legacyBytes.toString('utf8'));
  const result={revision:'H03/R141',createdAtUtc:new Date().toISOString(),
    scope:'Adendo de arquivos temporais diretos arquivados nas revisões R125–R140; não é inventário de todo o tempo da pesquisa',
    sourceUniverse:'Um exemplar versionado por arquivo; não relê cópias equivalentes em D:/TCC nem expande resultados/manifestos/contêineres.',
    legacySnapshot:{revision:'H03/R124',source:path.relative(path.resolve(here,'../../..'),legacyFile).replaceAll('\\','/'),sha256:sha(legacyBytes),files:legacy.files,counts:legacy.counts,notAddedToCurrentCounts:true},
    counts:{records:rows.length,withDuration:rows.filter(r=>r.durationMs!==null).length,derivedFromUTC:rows.filter(r=>r.durationOrigin.startsWith('diferença')).length,
      withoutDuration:rows.filter(r=>r.durationMs===null).length,processingObservationIntervals:rows.filter(r=>r.category==='comando_ate_observacao_de_termino').length,
      processingWithParent:rows.filter(r=>r.category==='comando_ate_observacao_de_termino'&&r.parentIntervalIds.length).length,
      sharedOrUnassigned:rows.filter(r=>r.branch===null).length,overlappingPairs:overlaps.length},
    records:rows,overlaps,fullFlowTotals:{CAD:null,BIM:null},finalProductivityRankingAllowed:false,
    isolatedAIWork:{inferenceMs:null,tokens:null,cost:null},humanActiveMs:null,monographEdited:false,nativeProjectsEdited:false,
    limits:[
      'As sessões incluem navegação, pesquisa, raciocínio e falhas/retomadas diferentes; não são tempos ativos humanos ou tempos puros de software.',
      'A duração explícita é preservada mesmo quando difere do relógio UTC; diferença UTC não substitui silenciosamente o registro.',
      'As quatro consultas R140 não declaram duração monotônica: o intervalo é derivado dos horários UTC e identificado como tal.',
      'Os intervalos comando→observação contidos nas sessões não são somados novamente; não há soma geral ou porcentagem de vantagem.',
      'Intervalos de recuperação compartilhados permanecem sem rateio arbitrário CAD/BIM.',
      'Código, documentação e decisões fora dos limites registrados não são preenchidos como zero nem estimados a partir de mensagens.',
      'O recorte anterior R124 e este adendo usam universos diferentes; a soma das contagens não representa total atualizado de atividades.',
      'Um campo de duração ou uma conclusão de sessão não demonstra escopo técnico completo ou aprovação estrutural.']};
  await fs.mkdir(output,{recursive:false});
  await fs.writeFile(path.join(output,'R141-adendo-tempos.json'),JSON.stringify(result,null,2)+'\n');
  const sec=ms=>ms===null?'não disponível':(ms/1000).toFixed(3);
  const table=rows.map(r=>`| R${r.revision} | ${r.branch??'compartilhado/não atribuído'} | ${r.name} | ${sec(r.durationMs)} | ${r.durationOrigin.startsWith('diferença')?'UTC derivado':'registrado'} | ${r.parentIntervalIds.length?'contido na sessão':'—'} |`).join('\n');
  const text=`# H03/R141 — adendo de tempos R125–R140\n\nForam consolidados **${rows.length} registros** de arquivos já arquivados, sem alterar os modelos ou a monografia. Há ${result.counts.withDuration} intervalos com duração utilizável neste recorte, dos quais ${result.counts.derivedFromUTC} derivados de limites UTC. Os ${result.counts.processingObservationIntervals} intervalos comando→observação estão contidos nas respectivas sessões e não devem ser adicionados novamente. Identificaram-se ${overlaps.length} pares com limites sobrepostos; isso não prova execução paralela.\n\nO inventário R124 permanece uma fotografia histórica separada (${legacy.files} candidatos naquele recorte). Este adendo não atualiza todo o universo do R124, não soma seus registros e não transforma contagens de arquivos em horas completas do projeto. Os arquivos de início, os resultados consolidados e as cópias locais de evidências não são contados novamente.\n\n| Revisão | Ramo | Registro | Segundos | Origem | Relação temporal |\n|---|---|---|---:|---|---|\n${table}\n\n## Uso nos resultados\n\nAs sessões são exploratórias e preservam tentativas descartadas, recuperação de capturas e consulta de controles. A R137 CAD inclui descoberta/retomada da seleção; a R140 CAD inclui descoberta do caminho de consulta, enquanto as seguintes usam o caminho aprendido. A R135 tem recuperação conjunta de capturas e a R133 tem consulta adicional, ambas sem rateio arbitrário entre CAD e BIM. O estado de cada ensaio deve ser lido em seu relatório técnico.\n\nA duração explícita e a diferença dos limites UTC estão preservadas em campos distintos no JSON. Nenhuma duração ausente vira zero. Os quatro intervalos R140 são derivados de UTC, sem precisão monotônica declarada. As diferenças entre relógios não foram ocultadas.\n\n**Não há tempo final comparável CAD/BIM, ranking ou economia percentual.** Também não há inferência isolada da IA, tempo ativo humano, tokens ou custo medidos para a edificação principal. O banco central e as demonstrações da palestra não foram alterados nem incorporados a este adendo.\n\n## Procedimento para o ensaio final\n\nCongelar primeiro uma proposta comum tecnicamente revisada e os arquivos de partida de cada ramo. Usar o mesmo conjunto de elementos, ações e entregáveis como critério de término. Registrar geração/autoria, intercâmbio, conferência, complementos no Eberick, correções, reprocessamento e documentação em intervalos identificados por ramo/etapa, mantendo a preparação comum separada.\n\nIniciar cada intervalo antes do comando da etapa e encerrá-lo após o critério de término observado. Pausas fora da tarefa exigem parada e novo intervalo na retomada. Falha/retrabalho dentro da tarefa permanece registrado com sua ocorrência e resultado; não se retira tempo para favorecer um ramo. Medidas internas de API/solver são subconjuntos: registrar seus limites e não adicioná-las ao intervalo que as contém. Tempo de raciocínio e operação da IA dentro da sessão não equivale a tempo isolado de inferência.\n\nO cronômetro existente distingue trabalho manual e processamento automático; o registro de evidências deve esclarecer se houve operação pela IA ou pelo usuário, pois a categoria manual do instrumento não comprova autoria humana. Como o instrumento existente também exige um cenário de alteração arquitetônica para permitir comparação final, definir e executar a mesma alteração nos dois ramos ou revisar formalmente esse protocolo antes de usar sua saída como resultado final. Não marcar cenários inexistentes como concluídos.\n\nAlternar a ordem CAD/BIM em repetições, conservar os mesmos critérios de inspeção e arquivar início/fim, proposta, versões, arquivos e ocorrências. Medir tempo junto com retenção de informação, complementos e compatibilização. Um resultado rápido sem o mesmo estado final aceito permanece parcial.\n\nOs números desta tabela são observações históricas, não previsão de duração futura. A consolidação de dados e a redação deste adendo não estão incluídas nos intervalos da tabela.\n`;
  await fs.writeFile(path.join(output,'LEIA-ME-R141.md'),text);
  console.log(JSON.stringify(result.counts));
  return result;
}

if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) {
  const [output]=process.argv.slice(2);if(!output)throw Error('Uso: node consolidar.mjs <pasta nova>');
  await consolidate(output);
}

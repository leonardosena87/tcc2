import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {normalize,relate} from '../h03-r141/consolidar.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const sha=b=>createHash('sha256').update(b).digest('hex');

export function normalizeRecent(value,meta) {
  const v={...value};
  v.startUtc??=v.inicioUtc??v.inicio??v.clocks?.['Revit-inicio.json'];
  v.endUtc??=v.fim_observado_utc??v.fimObservadoUtc??v.fimUtc??v.fim??v.savedObservation??v.saved??v.observationRecorded??v.observation??v.clocks?.['Revit-fim.json'];
  const extra=['duracaoMs','duracao_observacao_ms','intervaloObservacionalMs','decorridoMs','scriptDurationMs','scriptMs','elapsedMonotonicMs','sessionElapsedMonotonicMs'];
  const candidates=extra.filter(k=>v[k]!==undefined).map(k=>({field:k,ms:v[k]}));
  for(const c of candidates)if(typeof c.ms!=='number'||!Number.isFinite(c.ms)||c.ms<0)throw Error('Duracao invalida: '+c.field);
  const row=normalize(v,meta);
  if(!row.durationCandidates.length&&candidates.length){row.durationMs=candidates[0].ms;row.durationOrigin='campo explicito do registro';}
  row.durationCandidates.push(...candidates);
  row.durationMinusUtcMs=row.durationCandidates.length&&row.utcDifferenceMs!==null?row.durationCandidates[0].ms-row.utcDifferenceMs:null;
  row.phase='Consultar o escopo original do registro';
  row.scope??=v.nota??v.limitacao??null;
  if(/script/i.test(meta.name))row.category='execucao_de_script_sem_tempo_total_da_etapa';
  row.humanInterventionOriginal=v.humanIntervention??null;
  row.originalKnownLimits=Object.fromEntries(Object.entries(value).filter(([k])=>/includes|unknown|notFlow|not.*Effort|limit|ranking|Waiting|doNotSum/i.test(k)));
  row.explicitSourceFieldsPreserved=true;
  return row;
}

export async function consolidate(output) {
  const rows=[],sources=[],excluded=[];
  for(let revision=142;revision<=178;revision++){
    const dir=path.join(path.dirname(here),`h03-r${revision}`);
    for(const name of (await fs.readdir(dir)).sort()){
      if(!/\.json$/i.test(name)||!/(tempo|timing|observacao|correcao-primeiro-save)/i.test(name))continue;
      if(/inicio|primeiro-save\.json$/.test(name)){excluded.push({revision,name,reason:'marco de inicio ou fim isolado; usar intervalo consolidado'});continue;}
      const file=path.join(dir,name),bytes=await fs.readFile(file),v=JSON.parse(bytes.toString('utf8').replace(/^\uFEFF/,''));
      const meta={revision,name,source:path.relative(path.resolve(here,'../../..'),file).replaceAll('\\','/'),sha256:sha(bytes)};
      sources.push({source:meta.source,sha256:meta.sha256});
      if(revision===178&&name==='R178-tempos.json'){
        for(const branch of ['CAD','BIM']){
          const r=normalizeRecent({start:v[branch].start.startedAt,end:v[branch].firstSave.savedAt,scope:v[branch].start.scope},{...meta,name:`${branch}-correcao-intervalo`});
          r.sourceFragment=`${branch}`;r.includesConversationPause=branch==='BIM';r.scopeBoundariesUnequal=true;rows.push(r);
          rows.push({...normalizeRecent({durationMs:v.nativePartialProcessingSeconds[branch]*1000,scope:'Tempo interno do relatorio nativo de analise parcial R178'},{...meta,name:`${branch}-processamento-nativo`}),sourceFragment:`nativePartialProcessingSeconds.${branch}`,nativeSoftwareProcessingMeasure:true,pureSolverTime:false});
        }
      }else rows.push(normalizeRecent(v,meta));
    }
  }
  const overlaps=relate(rows);
  const result={revision:'H03/R180',createdAtUtc:new Date().toISOString(),
    scope:'Adendo de arquivos temporais diretos versionados R142-R178; sem somar o historico R124/R141 ou calcular total de fluxo',
    sourceUniverse:'Um exemplar local do repositorio por arquivo de tempo/observacao; sem varredura de copias em D:/TCC e sem expansao arbitraria de resultados',
    counts:{sourceFiles:sources.length,records:rows.length,withDuration:rows.filter(r=>r.durationMs!==null).length,
      withoutDuration:rows.filter(r=>r.durationMs===null).length,unassignedBranch:rows.filter(r=>!r.branch).length,
      nativeSoftwareProcessingMeasures:rows.filter(r=>r.nativeSoftwareProcessingMeasure).length,overlappingPairs:overlaps.length},
    sources,excluded,records:rows,overlaps,finalPairedFlowTotalCalculated:false,rankingsAllowed:false,
    isolatedAIInferenceMeasured:false,humanActiveTimeMeasured:false,tokensMeasured:false,costMeasured:false,
    centralTimingDatabaseModified:false,monographModified:false};
  await fs.mkdir(output,{recursive:true});
  await fs.writeFile(path.join(output,'R180-adendo-tempos.json'),JSON.stringify(result,null,2)+'\n');
  const table=rows.map(r=>`| R${r.revision} | ${r.branch??'nao atribuido'} | ${r.name} | ${r.durationMs===null?'ausente':(r.durationMs/1000).toFixed(3)} | ${r.nativeSoftwareProcessingMeasure?'interno do software':r.category} |`).join('\n');
  await fs.writeFile(path.join(output,'LEIA-ME-R180.md'),`# H03/R180 — adendo dos registros de tempo R142–R178\n\nConsolidaram-se ${sources.length} arquivos-fonte e ${rows.length} registros, com ${result.counts.withDuration} duracoes disponiveis e ${result.counts.withoutDuration} registros sem duracao. Existem ${overlaps.length} pares de limites sobrepostos; isso nao comprova trabalho paralelo. A ausencia de duracao nao foi convertida em zero. O inventario R124 e o adendo R141 permanecem separados e nao foram somados.\n\n| Revisao | Ramo | Registro | Segundos | Natureza |\n| --- | --- | --- | ---: | --- |\n${table}\n\n## Limites de uso nos resultados\n\nTrata-se de um inventario historico de observacoes parciais e exploratorias. A descricao completa, os campos de duracao originais, a diferenca dos limites UTC e as limitacoes declaradas ficam no JSON. Registros sem ramo inequivoco permanecem nao atribuidos; nao houve rateio entre CAD e BIM. Os nomes de arquivo nao demonstram equivalencia de escopo tecnico. O tempo de um script nao equivale a toda a etapa ou ao esforco integral da IA.\n\nTempos comando-ate-observacao podem incluir latencia e estar contidos em sessoes maiores. O arquivo registra esses vinculos quando os limites permitem, mas nao soma intervalos. Os dois valores internos da R178 sao 5 s CAD e 6 s BIM, com uma execucao documentada por ramo; os intervalos de correcao sao parciais e desiguais, incluindo pausa no BIM. Nenhum desses registros foi promovido a total comparavel.\n\nNao se calculou economia percentual ou vencedor. Nao se mediram separadamente inferencia da IA, tempo ativo humano, tokens ou custo. O banco central de tempos, os modelos e a monografia nao foram modificados por este inventario. Os hashes das fontes sao preservados para reproducao.\n\n## Ensaio final\n\nConcluir e congelar a concepcao comum e os criterios de aceitacao. Medir as mesmas fronteiras de autoria, intercambio, conferencia, complementacao, correcao e documentacao nos dois ramos, registrando pausas e intervencoes. Alternar a ordem nas repeticoes e tratar tempos internos como subconjuntos dos intervalos observados. O protocolo detalhado da R141 continua aplicavel; cenarios e repeticoes ainda nao executados nao devem ser declarados concluidos.\n\nExecutar node --test tcc-assistente/estudos/h03-r180/test_tempos.mjs e node tcc-assistente/estudos/h03-r180/consolidar_tempos.mjs <pasta-de-saida>. A consolidacao atual nao mede novas operacoes dos aplicativos.\n`);
  console.log(JSON.stringify(result.counts));return result;
}

if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href){
  if(!process.argv[2])throw Error('Informe uma pasta de saida');
  await consolidate(process.argv[2]);
}

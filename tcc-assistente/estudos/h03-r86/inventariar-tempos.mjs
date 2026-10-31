import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';

export function utc(value) {
  if(value&&typeof value==='object')for(const key of ['utc','iso','atUtc','startedAt','startUtc'])if(key in value)return utc(value[key]);
  if(typeof value!=='string'||!/(?:Z|[+-]\d{2}:\d{2})$/i.test(value))return null;
  const ms=Date.parse(value);return Number.isFinite(ms)?new Date(ms).toISOString():null;
}

export function classify(value) {
  if(!value||Array.isArray(value)||typeof value!=='object')throw Error('Registro de tempo nao e objeto.');
  const fields=['durationMs','elapsedMs','elapsedWallMs'].filter(k=>typeof value[k]==='number'&&Number.isFinite(value[k]));
  if(fields.some(k=>value[k]<0))throw Error('Duracao negativa.');
  const start=['startUtc','startedAt','startedAtUtc','started','start'].map(k=>utc(value[k])).find(Boolean)??null;
  const end=['endUtc','endedAt','endedAtUtc','finishedAtUtc','finish','end','utc'].map(k=>utc(value[k])).find(Boolean)??null;
  const nested=['records','sessions','session','events'].some(k=>k in value);
  const durationMs=fields.length?value[fields[0]]:null;
  const utcDifferenceMs=start&&end?Date.parse(end)-Date.parse(start):null;
  return {classification:durationMs!==null?'intervalo_com_duracao':nested?'container_nao_expandido':'registro_sem_duracao_principal',durationMs,durationField:fields[0]??null,otherDurationFields:Object.fromEntries(fields.slice(1).map(k=>[k,value[k]])),startUtc:start,endUtc:end,utcDifferenceMs,durationMinusUtcMs:durationMs!==null&&utcDifferenceMs!==null?durationMs-utcDifferenceMs:null,containsNestedRecords:nested,scope:value.actualScope??value.scope??value.stage??value.meaning??null,branch:value.branch??value.flow??null,status:value.status??null,knownInterruption:value.includesConversationInterruptionAndResume===true||value.includesHumanEntryAndWait===true||value.includesHumanWindowRepositionAndWait===true||/interromp|cancelad/i.test(value.status??''),eligibleForFinalFlowRanking:false};
}

export function overlaps(rows) {
  const out=[];
  for(let i=0;i<rows.length;i++) {
    const a=rows[i];if(a.durationMs===null||!a.startUtc||!a.endUtc)continue;
    for(const b of rows.slice(i+1)) {
      if(b.durationMs===null||!b.startUtc||!b.endUtc)continue;
      const durationMs=Math.min(Date.parse(a.endUtc),Date.parse(b.endUtc))-Math.max(Date.parse(a.startUtc),Date.parse(b.startUtc));
      if(durationMs>0)out.push({a:a.id,b:b.id,overlapMs:durationMs,meaning:'Sobreposicao dos limites declarados; nao prova trabalho paralelo nem duplicacao indevida.'});
    }
  }
  return out;
}

export async function inventory(root,output) {
  const rows=[],sha=b=>createHash('sha256').update(b).digest('hex'),read=async p=>JSON.parse((await fs.readFile(p,'utf8')).replace(/^\uFEFF/,''));
  const outputs=path.join(root,'outputs'),dirs=await fs.readdir(outputs,{withFileTypes:true});
  const candidates=[];
  for(const d of dirs.filter(d=>d.isDirectory()).sort((a,b)=>a.name.localeCompare(b.name))) {
    const dir=path.join(outputs,d.name);
    for(const f of await fs.readdir(dir,{withFileTypes:true}))if(f.isFile()&&/tempo.*\.json$/i.test(f.name))candidates.push({file:path.join(dir,f.name),group:'historico_exploratorio'});
  }
  const r84=path.join(outputs,'Autoria-H03-R84-AUDITORIA-NAO-EXECUTAR');
  for(const name of ['R84-CAD-N1-conversao.json','R84-CAD-N1-reabertura.json','R84-CAD-N2-conversao.json','R84-CAD-N2-reabertura.json'])candidates.push({file:path.join(r84,name),group:'processo_tecnico_CAD_R84'});
  for(const item of candidates) {
    const b=await fs.readFile(item.file),v=JSON.parse(b.toString('utf8').replace(/^\uFEFF/,''));
    rows.push({id:'T'+String(rows.length+1).padStart(3,'0'),source:path.relative(root,item.file).replaceAll('\\','/'),sha256:sha(b),group:item.group,...classify(v)});
  }
  const demos=[],demoRoot=path.join(root,'palestra-IA-engenharia/demonstracao/execucoes');
  for(const d of await fs.readdir(demoRoot,{withFileTypes:true})) {
    if(!d.isDirectory())continue;
    const dir=path.join(demoRoot,d.name);let result,request;
    try{result=await read(path.join(dir,'resultado.json'));request=await read(path.join(dir,'pedido-e-previa.json'));}catch(e){if(e.code==='ENOENT')continue;throw e;}
    demos.push({runId:result.runId,status:result.status,mode:result.mode,geometrySeconds:result.apiGeometrySeconds,dialogSeconds:result.dialogSeconds,commandTotalSeconds:result.commandTotalSeconds,aiSeconds:request.ai?.elapsedMs===undefined?null:request.ai.elapsedMs/1000,usage:request.ai?.usage??null,model:request.ai?.responseModel??null,source:path.relative(root,path.join(dir,'resultado.json')).replaceAll('\\','/'),sourceSha256:sha(await fs.readFile(path.join(dir,'resultado.json'))),belongsToMainBuildingExperiment:false,eligibleForFinalFlowRanking:false});
  }
  const centralPath=path.join(root,'dados-pesquisa/tempos.json'),central=await read(centralPath);
  const centralSummary={source:path.relative(root,centralPath).replaceAll('\\','/'),sha256:sha(await fs.readFile(centralPath)),sessions:central.sessions.map(s=>({id:s.id,name:s.name,mode:s.mode,entries:s.entries.length,statusCounts:Object.fromEntries([...new Set(s.entries.map(e=>e.status))].map(k=>[k,s.entries.filter(e=>e.status===k).length])),proposals:s.proposals,flowCompletedFlags:s.completed})),expandedOrAddedToOtherRecords:false};
  const counts=Object.fromEntries([...new Set(rows.map(r=>r.classification))].map(c=>[c,rows.filter(r=>r.classification===c).length]));
  const result={revision:'H03/R86',createdAtUtc:new Date().toISOString(),scope:'Arquivos *tempo*.json diretamente em cada pasta filha de outputs, quatro processos tecnicos R84, banco central resumido sem somar e demonstracoes separadas. Nao e inventario de todo o esforco da pesquisa.',counts,files:rows.length,records:rows,overlaps:overlaps(rows),centralTimingDatabase:centralSummary,presentationDemos:demos,fullFlowTotals:{CAD:null,BIM:null},isolatedAIWorkOnMainBuilding:{inferenceSeconds:null,tokens:null,cost:null},finalRankingAllowed:false,mainBuildingApproval:false};
  await fs.mkdir(output,{recursive:false});
  await fs.writeFile(path.join(output,'R86-inventario-tempos.json'),JSON.stringify(result,null,2)+'\n');
  return result;
}

if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) {
  const [root,output]=process.argv.slice(2);if(!root||!output)throw Error('Uso: node inventariar-tempos.mjs <D:/TCC> <nova pasta de resultados>');
  const r=await inventory(root,output);console.log(JSON.stringify({files:r.files,counts:r.counts,overlappingPairs:r.overlaps.length,demos:r.presentationDemos.length,centralSessions:r.centralTimingDatabase.sessions.length,finalRankingAllowed:false}));
}

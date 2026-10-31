import fs from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';

// Leitura de DXF ASCII: nunca abre ou modifica o arquivo nativo.
export function entities(text) {
  const lines=text.replace(/^\uFEFF/,'').replace(/\r/g,'').split('\n'), pairs=[];
  for(let i=0;i+1<lines.length;i+=2) {
    const code=Number(lines[i].trim());
    if(!Number.isInteger(code))throw Error('Codigo DXF invalido.');
    pairs.push([code,lines[i+1].trim()]);
  }
  const all=[];let active=false,current=null;
  for(let i=0;i<pairs.length;i++) {
    const [code,value]=pairs[i];
    if(code===0&&value==='SECTION'&&pairs[i+1]?.[0]===2&&pairs[i+1][1]==='ENTITIES'){active=true;i++;continue;}
    if(active&&code===0&&value==='ENDSEC'){if(current)all.push(current);return all;}
    if(!active)continue;
    if(code===0){if(current)all.push(current);current={type:value,pairs:[]};}
    else current?.pairs.push([code,value]);
  }
  throw Error('Secao ENTITIES completa nao encontrada.');
}

export function signature(e) {
  const vals=c=>e.pairs.filter(p=>p[0]===c).map(p=>p[1]);
  const n=v=>{const x=Number(v);if(!Number.isFinite(x))throw Error('Coordenada nao finita.');return Number(x.toFixed(6));};
  const layer=vals(8)[0]||'0';
  if(vals(38).some(v=>n(v)!==0)||vals(30).some(v=>n(v)!==0))throw Error('Geometria fora do plano XY.');
  if(vals(210).some(v=>n(v)!==0)||vals(220).some(v=>n(v)!==0)||vals(230).some(v=>n(v)!==1))throw Error('Extrusao nao suportada.');
  if(e.type==='LWPOLYLINE') {
    if([40,41,42,43].some(c=>vals(c).some(v=>n(v)!==0)))throw Error('Arco ou largura especial nao suportados.');
    const x=vals(10).map(n),y=vals(20).map(n);
    if(x.length!==y.length||x.length!==Number(vals(90)[0]))throw Error('Vertices inconsistentes.');
    return JSON.stringify({type:e.type,layer,closed:Number(vals(70)[0]||0)&1,x,y});
  }
  if(e.type!=='TEXT')throw Error('Entidade nao suportada: '+e.type);
  const hj=Number(vals(72)[0]||0),vj=Number(vals(73)[0]||0),aligned=hj!==0||vj!==0;
  return JSON.stringify({type:e.type,layer,text:vals(1),x:vals(aligned?11:10).map(n),y:vals(aligned?21:20).map(n),height:vals(40).map(n),angle:n((Number(vals(50)[0]||0)%360+360)%360),hJust:hj,vJust:vj});
}

export function compareDxf(before,after) {
  const a=entities(before),b=entities(after),sa=a.map(signature).sort(),sb=b.map(signature).sort();
  const differences=[];
  for(let i=0;i<Math.max(sa.length,sb.length);i++)if(sa[i]!==sb[i])differences.push({index:i,before:sa[i]??null,after:sb[i]??null});
  return {equal:differences.length===0,sourceEntities:a.length,reopenedEntities:b.length,polylines:b.filter(e=>e.type==='LWPOLYLINE').length,texts:b.filter(e=>e.type==='TEXT').length,differences};
}

export async function audit(sourceRoot,outputRoot) {
  const startedAtUtc=new Date().toISOString(),tick=performance.now();
  const hash=b=>createHash('sha256').update(b).digest('hex'),files=[];
  const bytes=async name=>{const p=path.join(sourceRoot,name),b=await fs.readFile(p);files.push({name,bytes:b.length,sha256:hash(b)});return b;};
  const json=async name=>JSON.parse((await bytes(name)).toString('utf8').replace(/^\uFEFF/,''));
  const proposal=await json('H03-R83-proposta.json');
  const creation=await json('R83-Revit-criacao-nativa.json');
  const readback=await json('R83-Revit-leitura-apos-reabrir.json');
  const mapping=new Map(creation.elements.map(e=>[e.id,e]));
  const native=new Map(readback.elements.map(e=>[e.uniqueId,e]));
  if(mapping.size!==62||native.size!==62||proposal.elements.length!==62)throw Error('Contagem ou identificadores divergentes.');
  const rows=proposal.elements.map(e=>{
    const id=mapping.get(e.id),r=id&&native.get(id.uniqueId);if(!r||String(id.revitId)!==r.id)throw Error('Elemento nativo nao associado: '+e.id);
    const category={column:'Pilares estruturais',beam:'Quadro estrutural',slab:'Pisos'}[e.kind];
    const expected=e.kind==='beam'?Math.hypot(e.x2-e.x,e.y2-e.y):e.kind==='slab'?(e.x2-e.x)*(e.y2-e.y):null;
    const observed=e.kind==='beam'?r.lengthM:e.kind==='slab'?r.areaM2:null;
    const measurement=e.kind==='beam'?'curveLengthM':e.kind==='slab'?'slabAreaM2':null;
    return {sourceId:e.id,kind:e.kind,revitId:r.id,uniqueId:r.uniqueId,categoryMatches:r.category===category,measurement,expected,observed,measurementMatches:expected===null?null:observed!==null&&Math.abs(expected-observed)<=1e-6};
  });
  const sourceDxf=(await bytes('H03-R83-AutoCAD.dxf')).toString('utf8');
  const cad=compareDxf(sourceDxf,(await bytes('H03-R83-AutoCAD-releitura.dxf')).toString('utf8'));
  const dwg=await bytes('H03-R83-AutoCAD.dwg');
  const rvt=await bytes('H03-R83-Revit.rvt');
  if(dwg.subarray(0,6).toString()!=='AC1032')throw Error('Cabecalho DWG inesperado.');
  const counts=Object.fromEntries(['column','beam','slab'].map(k=>[k,rows.filter(r=>r.kind===k).length]));
  const result={revision:'H03/R84',sourceRevision:'H03/R83',startedAtUtc,endedAtUtc:new Date().toISOString(),auditScriptMs:performance.now()-tick,counts,revit:{allIdsMatched:true,allCategoriesMatch:rows.every(r=>r.categoryMatches),measuredItems:rows.filter(r=>r.measurement).length,allAvailableLengthsAndAreasMatch:rows.every(r=>r.measurementMatches!==false),rows,limits:'Exportacao de leitura nao contem b/h, eixos XYZ, vinculos, cargas ou armaduras. Nao e auditoria completa das secoes nem do modelo analitico.'},cad,files,sourceFilesPreserved:true,flowTotal:false,rankingAllowed:false,structuralApproval:false,rvtBytes:rvt.length};
  const passed=result.revit.allCategoriesMatch&&result.revit.allAvailableLengthsAndAreasMatch&&cad.equal&&cad.polylines===62;
  result.status=passed?'audited_with_explicit_limits':'differences_require_review';
  await fs.mkdir(outputRoot,{recursive:true});
  await fs.writeFile(path.join(outputRoot,'R84-auditoria-autoria.json'),JSON.stringify(result,null,2)+'\n');
  for(const f of files)if(hash(await fs.readFile(path.join(sourceRoot,f.name)))!==f.sha256)throw Error('Fonte alterada durante a auditoria: '+f.name);
  return result;
}

if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) {
  const [source,output]=process.argv.slice(2);if(!source||!output)throw Error('Uso: node auditar-autoria.mjs <pasta R83> <pasta de saida nova>');
  const r=await audit(source,output);
  console.log(JSON.stringify({status:r.status,counts:r.counts,cad:r.cad.equal,revit:r.revit.allAvailableLengthsAndAreasMatch,cadDifferences:r.cad.differences.length}));
}

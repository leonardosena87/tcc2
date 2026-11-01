import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const out='D:/TCC/outputs/Tempos-H03-R124-INVENTARIO-NAO-EXECUTAR';
const sha=b=>createHash('sha256').update(b).digest('hex');
for(const name of ['R86-inventario-tempos.json','R124-resumo.json']) {
  const bytes=await fs.readFile(path.join(out,name));
  try {if(sha(await fs.readFile(path.join(here,name)))!==sha(bytes))throw Error('Evidencia divergente');}
  catch(e){if(e.code!=='ENOENT')throw e;}
  await fs.writeFile(path.join(here,name),bytes);
}
await fs.copyFile(path.join(here,'LEIA-ME-R124.md'),path.join(out,'LEIA-ME-R124.md'));
const files=[];
for(const entry of (await fs.readdir(here,{withFileTypes:true})).filter(e=>e.isFile()&&!e.name.includes('manifesto')).sort((a,b)=>a.name.localeCompare(b.name))) {
  files.push({path:entry.name,sha256:sha(await fs.readFile(path.join(here,entry.name)))});
}
const manifest={revision:'H03/R124',publicFiles:files};
for(const base of [here,out])await fs.writeFile(path.join(base,'R124-manifesto.json'),JSON.stringify(manifest,null,2)+'\n');
console.log(JSON.stringify({publicFiles:files.length}));

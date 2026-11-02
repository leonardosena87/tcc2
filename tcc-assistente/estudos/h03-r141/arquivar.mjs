import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../../..');
const out='D:/TCC/outputs/Tempos-H03-R141-ADENDO-NAO-EXECUTAR';
const sha=b=>createHash('sha256').update(b).digest('hex');
const result=JSON.parse(await fs.readFile(path.join(out,'R141-adendo-tempos.json'),'utf8'));
for(const r of [...result.records,result.legacySnapshot]) {
  if(sha(await fs.readFile(path.join(root,r.source)))!==r.sha256)throw Error('Fonte temporal alterada: '+r.source);
}
for(const name of ['R141-adendo-tempos.json','LEIA-ME-R141.md']) {
  const source=await fs.readFile(path.join(out,name));
  try{if(sha(await fs.readFile(path.join(here,name)))!==sha(source))throw Error('Arquivo já existe divergente');}
  catch(e){if(e.code!=='ENOENT')throw e;}
  await fs.writeFile(path.join(here,name),source);
}
await fs.writeFile(path.join(here,'.gitattributes'),'* -text\n');
const publicFiles=[];
for(const name of (await fs.readdir(here)).sort()) {
  if(name==='R141-manifesto.json')continue;
  const p=path.join(here,name);if(!(await fs.stat(p)).isFile())continue;
  publicFiles.push({path:name,sha256:sha(await fs.readFile(p))});
}
const manifest=JSON.stringify({revision:'H03/R141',sourceRecordsVerified:result.records.length,publicFiles},null,2)+'\n';
for(const base of [here,out])await fs.writeFile(path.join(base,'R141-manifesto.json'),manifest);
console.log(JSON.stringify({sourceRecordsVerified:result.records.length,manifestedFiles:publicFiles.length}));

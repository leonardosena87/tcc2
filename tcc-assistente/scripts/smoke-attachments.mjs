import https from 'node:https';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {createDownload} from '../server/downloads.mjs';
const ca=await readFile(path.join(os.homedir(),'.office-addin-dev-certs/ca.crt'));
function request(route,token,body){return new Promise((resolve,reject)=>{const req=https.request('https://localhost:3443'+route,{ca,method:body?'POST':'GET',headers:{'Content-Type':'application/json',...(token?{'X-TCC-Token':token}:{})}},res=>{const chunks=[];res.on('data',c=>chunks.push(c));res.on('end',()=>{try{const data=JSON.parse(Buffer.concat(chunks));if(res.statusCode!==200)reject(new Error(data.error));else resolve(data);}catch(e){reject(e);}});});req.on('error',reject);req.end(body?JSON.stringify(body):undefined);});}
// Synthetic PDF with a real cross-reference table, no user content.
function pdf(){const stream='BT /F1 12 Tf 50 750 Td (Codigo PDF: AMOSTRA-73) Tj ET';const objects=['<< /Type /Catalog /Pages 2 0 R >>','<< /Type /Pages /Kids [3 0 R] /Count 1 >>','<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>','<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',`<< /Length ${stream.length} >>\nstream\n${stream}\nendstream`];let text='%PDF-1.4\n';const offsets=[0];for(let i=0;i<objects.length;i++){offsets.push(Buffer.byteLength(text));text+=`${i+1} 0 obj\n${objects[i]}\nendobj\n`;}const xref=Buffer.byteLength(text);text+=`xref\n0 6\n0000000000 65535 f \n${offsets.slice(1).map(n=>String(n).padStart(10,'0')+' 00000 n \n').join('')}trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF`;return Buffer.from(text);}
const docs=[{name:'amostra.pdf',base64:pdf().toString('base64')},createDownload({format:'docx',text:'Codigo Word: AMOSTRA-84'}),createDownload({format:'xlsx',table:{columns:['Item','Quantidade'],rows:[['AMOSTRA-95','17']]}})];
const directory=new URL('../.runtime/fixtures/',import.meta.url);await mkdir(directory,{recursive:true});for(const file of docs)await writeFile(new URL(file.name,directory),Buffer.from(file.base64,'base64'));
const session=await request('/api/session');
const result=await request('/api/chat',session.token,{prompt:'Teste de leitura. Informe o codigo presente em cada um dos tres arquivos e a quantidade na planilha. Retorne uma tabela com colunas Arquivo, Codigo, Quantidade. Nao invente dados.',attachments:docs.map(({name,base64})=>({name,base64}))});
const all=JSON.stringify(result);
for(const expected of ['AMOSTRA-73','AMOSTRA-84','AMOSTRA-95','17'])if(!all.includes(expected))throw new Error(`Leitura não confirmou ${expected}`);
console.log(JSON.stringify({status:'Leitura real dos 3 formatos confirmada',answer:result.answer,table:result.table},null,2));

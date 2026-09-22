import test from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import {once} from 'node:events';
import {mkdtemp,writeFile,rm} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {createHandler} from '../server/app.mjs';
async function fixture(t,options={}){
  const exportDir=await mkdtemp(path.join(os.tmpdir(),'tcc-test-'));
  const server=http.createServer(createHandler({exportDir,...options}));server.listen(0,'127.0.0.1');await once(server,'listening');
  t.after(async()=>{await new Promise(resolve=>server.close(resolve));await rm(exportDir,{recursive:true,force:true});});
  const url=`http://127.0.0.1:${server.address().port}`;
  const request=(route,opts={})=>new Promise((resolve,reject)=>{
    const req=http.request(url+route,{method:opts.method??'GET',headers:{host:'localhost:3443',...opts.headers}},res=>{
      const chunks=[];res.on('data',chunk=>chunks.push(chunk));res.on('end',()=>resolve(new Response(Buffer.concat(chunks),{status:res.statusCode,headers:res.headers})));
    });req.on('error',reject);req.end(opts.body);
  });
  const {token}=await (await request('/api/session')).json();
  const call=(route,body)=>request(route,{method:body?'POST':'GET',headers:{'x-tcc-token':token,'content-type':'application/json'},body:body?JSON.stringify(body):undefined});
  return {request,call,exportDir};
}
test('API bloqueia origem externa, DNS rebinding e chamadas sem token',async t=>{
  const {request}=await fixture(t);
  assert.equal((await request('/api/exports')).status,401);
  assert.equal((await request('/api/session',{headers:{origin:'https://example.org'}})).status,403);
  assert.equal((await request('/api/session',{headers:{host:'evil.test'}})).status,403);
  assert.equal((await request('/api/session',{headers:{'sec-fetch-site':'cross-site'}})).status,403);
  assert.equal((await request('/',{headers:{'sec-fetch-site':'cross-site'}})).status,200);
});
test('chave não aparece nas respostas e pode ser removida',async t=>{
  const {request,call}=await fixture(t);
  assert.equal((await call('/api/chat',{prompt:'oi'})).status,503);
  const r=await call('/api/settings',{apiKey:'sk-test-only',model:'model-test'});assert.equal(r.status,200);assert.equal((await r.text()).includes('sk-test-only'),false);
  assert.equal((await (await request('/api/session')).json()).configured,true);
  await call('/api/settings',{clearKey:true,model:'model-test'});
  assert.equal((await (await request('/api/session')).json()).configured,false);
  assert.equal((await request('/server/main.mjs')).status,404);
});
test('exportações não permitem ler caminhos arbitrários',async t=>{
  const {call,exportDir}=await fixture(t);
  await writeFile(path.join(exportDir,'revit-test.json'),JSON.stringify({schemaVersion:1,application:'Revit',scope:'selection',document:'Teste',exportedAt:new Date().toISOString(),elements:[]}));
  assert.equal((await call('/api/export?name=../../secret.json')).status,400);
  assert.equal((await call('/api/export?name=revit-test.json')).status,200);
  assert.equal((await (await call('/api/exports')).json()).files.length,1);
});
test('contrato Responses API e leitura de resposta completos, sem chamada paga',async t=>{
  let captured;
  const {call}=await fixture(t,{apiKey:'sk-test-only',fetchImpl:async(url,options)=>{captured={url,body:JSON.parse(options.body)};return new Response(JSON.stringify({status:'completed',output:[{type:'message',content:[{type:'output_text',text:'{"answer":"Revisto","replacement":"Texto final"}'}]}]}),{status:200});}});
  const result=await call('/api/chat',{prompt:'Revisar',mode:'rewrite',selection:'Texto original'});
  assert.equal(result.status,200);assert.equal((await result.json()).replacement,'Texto final');
  assert.equal(captured.url,'https://api.openai.com/v1/responses');assert.equal(captured.body.store,false);
});
test('falhas upstream não expõem payloads ou credenciais',async t=>{
  const {call}=await fixture(t,{apiKey:'sk-test-only',fetchImpl:async()=>new Response('private upstream details',{status:401})});
  const response=await call('/api/chat',{prompt:'oi'});assert.equal(response.status,502);assert.match((await response.json()).error,/não foi aceita/);
});

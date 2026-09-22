import test from 'node:test';
import assert from 'node:assert/strict';
import {setWordReady,capture,applyReplacement,discardTarget,insertAtCursor} from '../public/word.js';
function host(){
  const first={text:'Original',xml:'<w:p><w:r><w:t>Original</w:t></w:r></w:p>',load(){},getOoxml(){return {value:this.xml};},track(){},untrack(){},insertText(text,where){this.inserted={text,where};}};
  const second={...first,text:'Outra seleção'};
  let current=first;
  const context={document:{getSelection:()=>current,body:{text:'Documento',load(){}}},sync:async()=>{}};
  globalThis.Word={RequestContext:function(){return context;},InsertLocation:{replace:'Replace',end:'End'},run:fn=>fn(context)};
  setWordReady(true);return {first,second,move:()=>current=second};
}
test('aplica ao trecho capturado mesmo se seleção do cursor mudar',async()=>{
  const h=host();await capture({rewrite:true});h.move();await applyReplacement('Novo');
  assert.deepEqual(h.first.inserted,{text:'Novo',where:'Replace'});assert.equal(h.second.inserted,undefined);
});
test('bloqueia proposta se texto original foi alterado',async()=>{
  const h=host();await capture({rewrite:true});h.first.text='Alterado pelo usuário';
  await assert.rejects(applyReplacement('Novo'),/trecho mudou/);assert.equal(h.first.inserted,undefined);await discardTarget();
});
test('conteúdo com tabelas ou campos não é substituído',async()=>{
  const h=host();h.first.xml='<w:tbl><w:tr/></w:tbl>';
  await assert.rejects(capture({rewrite:true}),/tabelas/);assert.equal(h.first.inserted,undefined);
});
test('inserção de resposta não substitui a seleção atual',async()=>{
  const h=host();await insertAtCursor('Resposta');assert.equal(h.first.inserted.where,'End');
});
test('fora do Word falha claramente; conversa sem contexto continua disponível',async()=>{
  setWordReady(false);await assert.rejects(capture({selection:true}),/dentro do Word/);
  assert.deepEqual(await capture({selection:false,document:false,rewrite:false}),{selection:'',document:''});
});

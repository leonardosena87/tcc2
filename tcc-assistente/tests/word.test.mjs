import test from 'node:test';
import assert from 'node:assert/strict';
import {setWordReady,capture,applyReplacement,discardTarget,insertAtCursor,releaseSuggestions,applySuggestionsInWord,clearSuggestionHighlights} from '../public/word.js';
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
test('limpeza de sugestões tolera ranges invalidados após aplicação',async()=>{
  const snapshot={items:[{range:{untrack(){throw new Error('ItemNotFound');}}}],context:{sync:async()=>{}}};
  await releaseSuggestions(snapshot);
});
test('captura seleção dentro de Word.run e mantém índices do documento',async()=>{
  const order=[];const selection={text:'Trecho selecionado',load(){}};
  const makeParagraph=(text,relation)=>({text,getRange(){return {text,load(){},getOoxml(){return {value:'<w:p/>'};},compareLocationWith(){return {value:relation};},insertText(value){this.inserted=value;return {font:{}};}};}});
  const body={paragraphs:{items:[makeParagraph('Antes','Before'),makeParagraph('Trecho selecionado','Equal'),makeParagraph('Depois','After')],load(){}}};
  const context={document:{getSelection(){order.push('getSelection');return selection;},body},sync:async()=>{order.push('sync');}};
  globalThis.Word={run:fn=>fn(context)};setWordReady(true);
  let requestData;
  const result=await applySuggestionsInWord('selection',async paragraphs=>{order.push('request');requestData=paragraphs;return [{index:1,original:'Trecho selecionado',revised:'Texto revisado'}];},async(snapshot)=>{order.push('apply');assert.equal(snapshot.context,context);return 1;});
  assert.deepEqual(order.slice(0,2),['getSelection','sync']);
  assert.deepEqual(requestData,[{index:1,text:'Trecho selecionado'}]);
  assert.equal(result.count,1);
});
test('captura o documento inteiro sem tentar ler uma seleção inexistente',async()=>{
  const paragraph={getRange(){return {text:'Parágrafo',load(){},getOoxml(){return {value:'<w:p/>'};}};}};
  const context={document:{getSelection(){throw new Error('não deveria obter seleção');},body:{paragraphs:{items:[paragraph],load(){}}}},sync:async()=>{}};
  globalThis.Word={run:fn=>fn(context)};setWordReady(true);
  const result=await applySuggestionsInWord('document',async values=>{assert.deepEqual(values,[{index:0,text:'Parágrafo'}]);return [];},async()=>0);
  assert.equal(result.count,0);
});
test('remove destaques em novo Word.run usando índices e texto revisado',async()=>{
  const range={font:{highlightColor:null}};
  const paragraph={text:'Revisado',load(){},getRange(){return range;}};
  const paragraphs={items:[paragraph],load(){}};const context={document:{body:{paragraphs}},sync:async()=>{}};
  globalThis.Word={run:fn=>fn(context)};setWordReady(true);
  assert.equal(await clearSuggestionHighlights([{index:0,revised:'Revisado'}]),1);
  assert.equal(range.font.highlightColor,'None');
});
test('fora do Word falha claramente; conversa sem contexto continua disponível',async()=>{
  setWordReady(false);await assert.rejects(capture({selection:true}),/dentro do Word/);
  assert.deepEqual(await capture({selection:false,document:false,rewrite:false}),{selection:'',document:''});
});

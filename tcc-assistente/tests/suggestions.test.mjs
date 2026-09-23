import test from 'node:test';
import assert from 'node:assert/strict';
import {validateEdits,applyEdits,clearSuggestionHighlights} from '../public/suggestions.js';
import {buildRequest} from '../server/core.mjs';
const paragraphs=[{index:0,text:'Texto original'},{index:2,text:'Outro parágrafo'}];
const edit={index:0,original:'Texto original',revised:'Texto revisado'};
function snapshot(){const items=paragraphs.map(p=>({index:p.index,original:p.text,xml:'<w:p/>',range:{text:p.text,load(){},getOoxml(){return {value:'<w:p/>'};},insertText(text){this.written=text;}}}));return {items,paragraphs,context:{sync:async()=>{}}};}
test('plano recusa original errado, índices protegidos, duplicações e exclusões',()=>{
  assert.deepEqual(validateEdits([edit],paragraphs),[edit]);
  for(const edits of [[{...edit,original:'Inventado'}],[{...edit,index:1}],[edit,edit],[{...edit,revised:''}]])assert.throws(()=>validateEdits(edits,paragraphs));
});
test('verifica todo o escopo antes de escrever qualquer parágrafo',async()=>{
  const captured=snapshot();captured.items[1].range.text='Mudança durante a análise';
  await assert.rejects(applyEdits(captured,[edit]),/documento mudou/);
  assert.ok(captured.items.every(x=>!x.range.written));
});
test('aplica somente mudanças válidas e preserva outros parágrafos',async()=>{
  const captured=snapshot();assert.equal(await applyEdits(captured,[edit]),1);
  assert.equal(captured.items[0].range.written,'Texto revisado');assert.equal(captured.items[1].range.written,undefined);
});
test('remove destaques sem falhar se um range já foi invalidado',async()=>{
  const range={font:{highlightColor:'#FFFF00'},untrack(){throw new Error('ItemNotFound');}};
  const snapshot={highlights:[range],context:{sync:async()=>{}}};
  await clearSuggestionHighlights(snapshot);assert.equal(range.font.highlightColor,'None');assert.deepEqual(snapshot.highlights,[]);
});
test('modo apply solicita mudanças estruturadas com fonte exata',()=>{
  const result=buildRequest({mode:'apply',prompt:'Aplicar',suggestions:'Melhorar clareza',paragraphs},'test');
  assert.ok(result.text.format.schema.required.includes('edits'));assert.match(result.input[0].content,/Texto original/);
  assert.throws(()=>buildRequest({mode:'apply',prompt:'Aplicar',suggestions:'Melhorar',paragraphs:[paragraphs[0],paragraphs[0]]},'test'),/inválidos/);
});

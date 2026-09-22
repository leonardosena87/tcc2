import test from 'node:test';
import assert from 'node:assert/strict';
import AdmZip from 'adm-zip';
import {validateAttachments,FILE_LIMIT} from '../server/attachments.mjs';
import {buildRequest} from '../server/core.mjs';
import {createDownload} from '../server/downloads.mjs';
const pdf={name:'referencia.pdf',base64:Buffer.from('%PDF-1.4\nexample').toString('base64')};
test('anexos entram como input_file e não como instruções',()=>{
  const request=buildRequest({prompt:'Compare',attachments:[pdf]},'test');
  assert.equal(request.input.at(-1).content[1].type,'input_file');
  assert.equal(request.input.at(-1).content[1].filename,pdf.name);
  assert.match(request.input.at(-1).content[1].file_data,/^data:application\/pdf;base64,/);
  assert.match(request.instructions,/1.000 linhas/);
});
test('valida tipo, assinatura, base64 e limites dos arquivos',()=>{
  assert.equal(validateAttachments([pdf]).length,1);
  for(const invalid of [{...pdf,name:'../../file.pdf'},{...pdf,name:'programa.exe'},{...pdf,base64:'broken'},{...pdf,base64:Buffer.from('not PDF').toString('base64')}])assert.throws(()=>validateAttachments([invalid]));
  assert.throws(()=>validateAttachments(Array(6).fill(pdf)),/5 arquivos/);
  const big=Buffer.alloc(FILE_LIMIT+1);big.write('%PDF-');assert.throws(()=>validateAttachments([{name:'grande.pdf',base64:big.toString('base64')}]));
  const regular=Buffer.alloc(8*1024*1024);regular.write('%PDF-');assert.throws(()=>validateAttachments(Array(3).fill({name:'teste.pdf',base64:regular.toString('base64')})),/20 MB/);
});
test('formatos Word e Excel gerados são pacotes OOXML válidos e texto é escapado',()=>{
  const doc=createDownload({format:'docx',text:'Teste <seguro> & referência'});
  const zip=new AdmZip(Buffer.from(doc.base64,'base64'));
  assert.match(zip.readAsText('word/document.xml'),/Teste &lt;seguro&gt; &amp; referência/);
  assert.ok(zip.getEntry('_rels/.rels'));
  assert.equal(validateAttachments([{name:doc.name,base64:doc.base64}])[0].mime,doc.mime);
  const sheet=createDownload({format:'xlsx',table:{columns:['Nome','Valor'],rows:[['Item A','42'],['=HYPERLINK("https://example.org")','<texto>']]}});
  const xlsx=new AdmZip(Buffer.from(sheet.base64,'base64'));const xml=xlsx.readAsText('xl/worksheets/sheet1.xml');
  assert.match(xml,/inlineStr/);assert.doesNotMatch(xml,/<f>/);assert.match(xml,/&lt;texto&gt;/);
  assert.equal(validateAttachments([{name:sheet.name,base64:sheet.base64}])[0].mime,sheet.mime);
});
test('exportação rejeita tabela irregular e formatos não autorizados',()=>{
  assert.throws(()=>createDownload({format:'xlsx',table:{columns:['A'],rows:[['1','2']]}}),/Tabela inválida/);
  assert.throws(()=>createDownload({format:'exe',text:'code'}),/Formato/);
  assert.throws(()=>createDownload({format:'docx',text:''}),/vazio/);
});

import test,{after} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import AdmZip from 'adm-zip';
import {ADDIN_ID,configureTemplateFile} from '../scripts/word-autoopen-template.mjs';

const sandbox=fs.mkdtempSync(path.join(os.tmpdir(),'tcc-autoopen-test-'));
after(()=>fs.rmSync(sandbox,{recursive:true,force:true}));
function makeTemplate(name){
  const file=path.join(sandbox,name);const zip=new AdmZip();
  zip.addFile('[Content_Types].xml',Buffer.from('<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'));
  zip.addFile('_rels/.rels',Buffer.from('<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'));
  zip.addFile('word/document.xml',Buffer.from('<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body/></w:document>'));
  zip.writeZip(file);return file;
}
test('marca o modelo padrão e remove somente a marcação do TCC Assistente',()=>{
  const input=makeTemplate('Normal.dotm');const enabled=path.join(sandbox,'enabled.dotm');const disabled=path.join(sandbox,'disabled.dotm');
  assert.equal(configureTemplateFile(input,enabled,true),true);
  const zip=new AdmZip(enabled);const relationships=zip.readAsText('_rels/.rels');
  assert.match(relationships,/webextensiontaskpanes/);
  assert.match(zip.readAsText('word/webextensions/webextension.xml'),new RegExp(`id="\\{${ADDIN_ID}\\}"`));
  assert.match(zip.readAsText('word/webextensions/webextension.xml'),/Office\.AutoShowTaskpaneWithDocument" value="true/);
  assert.match(zip.readAsText('word/webextensions/taskpanes.xml'),/visibility="0"/);
  assert.equal(configureTemplateFile(enabled,disabled,false),true);
  const cleaned=new AdmZip(disabled);
  assert.doesNotMatch(cleaned.readAsText('_rels/.rels'),/webextensiontaskpanes/);
  assert.equal(cleaned.getEntry('word/webextensions/taskpanes.xml'),null);
  assert.equal(cleaned.getEntry('word/webextensions/webextension.xml'),null);
  assert.match(cleaned.readAsText('[Content_Types].xml'),/word\/document\.xml/);
});
test('não substitui uma configuração de suplemento já existente no modelo',()=>{
  const input=makeTemplate('Existing.dotm');const zip=new AdmZip(input);
  zip.addFile('_rels/.rels',Buffer.from('<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.microsoft.com/office/2011/relationships/webextensiontaskpanes" Target="word/webextensions/taskpanes.xml"/></Relationships>'));
  zip.addFile('word/webextensions/taskpanes.xml',Buffer.from('<wetp:taskpanes/>'));
  zip.writeZip(input);
  assert.throws(()=>configureTemplateFile(input,path.join(sandbox,'must-not-exist.dotm'),true),/já contém.*configuração/);
});

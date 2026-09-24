import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import AdmZip from 'adm-zip';

export const ADDIN_ID='03d9d533-ff12-4e95-bd27-f35dc9c4d678';
const TASKPANES='word/webextensions/taskpanes.xml';
const TASKPANES_RELS='word/webextensions/_rels/taskpanes.xml.rels';
const WEBEXTENSION='word/webextensions/webextension.xml';
const TASKPANES_TYPE='http://schemas.microsoft.com/office/2011/relationships/webextensiontaskpanes';
const WEBEXTENSION_TYPE='http://schemas.microsoft.com/office/2011/relationships/webextension';
const RELS_NS='http://schemas.openxmlformats.org/package/2006/relationships';
const WEBEXTENSION_NS='http://schemas.microsoft.com/office/webextensions/webextension/2010/11';
const TASKPANES_NS='http://schemas.microsoft.com/office/webextensions/taskpanes/2010/11';
const OFFICE_REL_NS='http://schemas.openxmlformats.org/officeDocument/2006/relationships';

function read(zip,path){const entry=zip.getEntry(path);if(!entry)throw new Error(`O modelo do Word não contém ${path}.`);return entry.getData().toString('utf8');}
function write(zip,path,value){zip.addFile(path,Buffer.from(value,'utf8'));}
function contentTypesWith(zip,overrides){
  let xml=read(zip,'[Content_Types].xml');
  for(const [partName,contentType] of overrides){
    if(xml.includes(`PartName="${partName}"`))continue;
    xml=xml.replace(/<\/Types>\s*$/,`<Override PartName="${partName}" ContentType="${contentType}"/></Types>`);
  }
  write(zip,'[Content_Types].xml',xml);
}
function contentTypesWithout(zip,partNames){
  let xml=read(zip,'[Content_Types].xml');
  for(const partName of partNames){
    const escaped=partName.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
    xml=xml.replace(new RegExp(`<Override\\b(?=[^>]*\\bPartName=["']${escaped}["'])[^>]*/>`,'g'),'');
  }
  write(zip,'[Content_Types].xml',xml);
}
function relationshipEntries(xml){return [...xml.matchAll(/<Relationship\b[^>]*\/>/g)].map(match=>({xml:match[0],id:/\bId="([^"]+)"/.exec(match[0])?.[1],type:/\bType="([^"]+)"/.exec(match[0])?.[1],target:/\bTarget="([^"]+)"/.exec(match[0])?.[1]}));}
function nextRelationshipId(entries){const used=new Set(entries.map(entry=>entry.id));let n=1;while(used.has(`rId${n}`))n++;return `rId${n}`;}
function addTaskpane(zip){
  const rootRels=read(zip,'_rels/.rels');
  const entries=relationshipEntries(rootRels);
  const current=entries.find(entry=>entry.type===TASKPANES_TYPE);
  if(current){
    const target=current.target?.replace(/^\//,'');
    if(!target||!zip.getEntry(target))throw new Error('O Normal.dotm já contém uma configuração de painel desconhecida. Nenhuma alteração foi feita para preservá-la.');
    const taskpaneRelsPath=target?`${target.slice(0,target.lastIndexOf('/'))}/_rels/${target.slice(target.lastIndexOf('/')+1)}.rels`:'';
    if(!zip.getEntry(taskpaneRelsPath))throw new Error('O Normal.dotm já contém uma configuração de painel desconhecida. Nenhuma alteração foi feita para preservá-la.');
    const relXml=taskpaneRelsPath?read(zip,taskpaneRelsPath):'';
    const extRel=relationshipEntries(relXml).find(entry=>entry.type===WEBEXTENSION_TYPE);
    const extPath=extRel&&`${target.slice(0,target.lastIndexOf('/'))}/${extRel.target}`;
    if(!extPath||!zip.getEntry(extPath))throw new Error('O Normal.dotm já contém uma configuração de painel desconhecida. Nenhuma alteração foi feita para preservá-la.');
    if(extPath&&read(zip,extPath).includes(`id="{${ADDIN_ID}}"`)&&read(zip,extPath).includes('name="Office.AutoShowTaskpaneWithDocument" value="true"'))return false;
    throw new Error('O Normal.dotm já contém configuração de painel de suplemento. Nenhuma alteração foi feita para preservar essa configuração.');
  }
  for(const path of [TASKPANES,TASKPANES_RELS,WEBEXTENSION])if(zip.getEntry(path))throw new Error(`O arquivo ${path} já existe; interrompi para preservar o modelo.`);
  const rootId=nextRelationshipId(entries);
  const rootRelationship=`<Relationship Id="${rootId}" Type="${TASKPANES_TYPE}" Target="${TASKPANES}"/>`;
  if(!/<\/Relationships>\s*$/.test(rootRels))throw new Error('Não consegui atualizar as relações internas do Normal.dotm.');
  write(zip,'_rels/.rels',rootRels.replace(/<\/Relationships>\s*$/,`${rootRelationship}</Relationships>`));
  write(zip,TASKPANES,`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><wetp:taskpanes xmlns:wetp="${TASKPANES_NS}"><wetp:taskpane dockstate="right" visibility="0" width="350" row="4"><wetp:webextensionref xmlns:r="${OFFICE_REL_NS}" r:id="rId1"/></wetp:taskpane></wetp:taskpanes>`);
  write(zip,TASKPANES_RELS,`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="${RELS_NS}"><Relationship Id="rId1" Type="${WEBEXTENSION_TYPE}" Target="webextension.xml"/></Relationships>`);
  write(zip,WEBEXTENSION,`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><we:webextension xmlns:we="${WEBEXTENSION_NS}" id="{${ADDIN_ID}}"><we:reference id="${ADDIN_ID}" version="1.0.0.2" store="developer" storeType="Registry"/><we:alternateReferences/><we:properties><we:property name="Office.AutoShowTaskpaneWithDocument" value="true"/></we:properties><we:bindings/><we:snapshot xmlns:r="${OFFICE_REL_NS}"/></we:webextension>`);
  contentTypesWith(zip,[
    [`/${TASKPANES}`,'application/vnd.ms-office.webextensiontaskpanes+xml'],
    [`/${WEBEXTENSION}`,'application/vnd.ms-office.webextension+xml'],
  ]);
  return true;
}
function removeTaskpane(zip){
  const rootRels=read(zip,'_rels/.rels');
  const entries=relationshipEntries(rootRels);
  const current=entries.find(entry=>entry.type===TASKPANES_TYPE);
  if(!current)return false;
  const target=current.target?.replace(/^\//,'');
  if(target!==TASKPANES)throw new Error('A relação do painel não corresponde ao suplemento TCC Assistente. Nada foi removido.');
  const taskpaneXml=read(zip,TASKPANES);
  const relsXml=read(zip,TASKPANES_RELS);
  const webExtension=read(zip,WEBEXTENSION);
  if(!webExtension.includes(`id="{${ADDIN_ID}}"`))throw new Error('O painel do Normal.dotm pertence a outro suplemento. Nada foi removido.');
  if((taskpaneXml.match(/<wetp:taskpane\b/g)??[]).length!==1||relationshipEntries(relsXml).length!==1)throw new Error('O Normal.dotm contém outros painéis. Nada foi removido para preservá-los.');
  const escaped=current.id.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
  const withoutRelationship=rootRels.replace(new RegExp(`<Relationship\\b(?=[^>]*\\bId="${escaped}")(?=[^>]*\\bType="${TASKPANES_TYPE}")[^>]*/>`),'');
  if(withoutRelationship===rootRels)throw new Error('Não consegui remover a relação do suplemento com segurança.');
  write(zip,'_rels/.rels',withoutRelationship);
  for(const path of [TASKPANES,TASKPANES_RELS,WEBEXTENSION])zip.deleteFile(path);
  contentTypesWithout(zip,[`/${TASKPANES}`,`/${WEBEXTENSION}`]);
  return true;
}

export function configureTemplateFile(inputPath,outputPath,enabled){
  const zip=new AdmZip(inputPath);
  const changed=enabled?addTaskpane(zip):removeTaskpane(zip);
  if(changed)zip.writeZip(outputPath);else fs.copyFileSync(inputPath,outputPath);
  return changed;
}

if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href){
  const [operation,inputPath,outputPath]=process.argv.slice(2);
  if(!['enable','disable'].includes(operation)||!inputPath||!outputPath){
    console.error('Uso: node word-autoopen-template.mjs <enable|disable> <Normal.dotm> <arquivo-temporario>');process.exit(2);
  }
  try{
    const changed=configureTemplateFile(inputPath,outputPath,operation==='enable');
    console.log(changed?'Abertura automática configurada no modelo.':'O modelo já estava no estado solicitado.');
  }catch(error){console.error(error.message);process.exit(1);}
}

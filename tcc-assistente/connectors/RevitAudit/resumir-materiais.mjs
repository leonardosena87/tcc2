import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const key=value=>{
  if(value==null)return null;
  if(typeof value==='number'&&!Number.isSafeInteger(value))throw Error('ID numerico sem precisao segura; exportar como texto');
  if(!['string','number'].includes(typeof value))throw Error('ID em formato invalido');
  return String(value);
};
function unique(rows,field,label){
  const map=new Map();
  for(const row of rows){const id=key(row[field]);if(!id||map.has(id))throw Error(`${label}: identificador ausente ou duplicado`);map.set(id,row);}
  return map;
}
function compression(material){
  const r=material?.asset?.concreteCompression;
  return material?.status==='asset_read'&&material.asset?.class==='Concrete'&&r?.status==='read'&&typeof r.converted==='number'&&Number.isFinite(r.converted)?r.converted:null;
}

export function summarizeMaterials(audit,mapping){
  if(audit?.schema!=='tcc-revit-material-audit/1'||audit.status!=='native_read_with_explicit_limits'||!Array.isArray(audit.elements)||!Array.isArray(audit.materials)||!Array.isArray(mapping?.elements)||mapping.elements.length===0)throw Error('Formato ou mapeamento de origem invalido');
  if(audit.count!==audit.elements.length||audit.transactionsStarted!==0||audit.nativeDocumentSaved!==false)throw Error('Escopo de leitura inconsistente');
  const native=unique(audit.elements,'uniqueId','Leitura nativa'),expected=unique(mapping.elements,'uniqueId','Mapa de autoria'),materials=unique(audit.materials,'id','Materiais');
  unique(audit.elements,'id','IDs nativos');unique(mapping.elements,'id','IDs logicos');
  const rows=[...expected].map(([uid,source])=>{
    const e=native.get(uid);
    if(!e)return {sourceId:source.id,uniqueId:uid,status:'native_element_absent',structuralMaterialId:null,concreteCompressionMPa:null};
    if(key(source.revitId)!==key(e.id))return {sourceId:source.id,uniqueId:uid,status:'native_id_mismatch',structuralMaterialId:null,concreteCompressionMPa:null};
    if(!Object.hasOwn(e,'structuralMaterialId'))throw Error('Campo de atribuicao estrutural ausente');
    const id=key(e.structuralMaterialId),m=id===null?null:materials.get(id);
    return {sourceId:source.id,uniqueId:uid,status:'identity_matched',structuralMaterialId:id,assignmentStatus:e.assignmentStatus,
      materialName:m?.name??null,materialCatalogStatus:m?.status??(id===null?'not_assigned':'catalog_entry_missing'),
      concreteCompressionMPa:compression(m)};
  });
  const matched=rows.filter(r=>r.status==='identity_matched');
  return {schema:'tcc-revit-material-summary/1',expectedLogicalUnits:expected.size,nativeCandidates:native.size,
    extraNativeCandidates:[...native.keys()].filter(uid=>!expected.has(uid)),
    identityMatchedUnits:matched.length,assignmentObservedUnits:matched.filter(r=>r.structuralMaterialId!==null).length,
    concreteCompressionReadUnits:matched.filter(r=>r.concreteCompressionMPa!==null).length,rows,
    savedSnapshotObserved:audit.document?.modifiedBefore===false&&audit.document?.modifiedAfter===false,
    sourceMappingCompleted:matched.length===expected.size,
    transferLossProven:false,structuralApproval:false,ca50MechanicalPropertiesVerified:false,
    limits:'Somente identidade e propriedades disponiveis no autor. Nomes, materiais geometricos e dados ausentes nao substituem atribuicao estrutural. Sem receptor nao ha diagnostico de perda. Compressao da API nao e automaticamente fck da NBR.'};
}

if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href){
  const[auditFile,mappingFile,outputFile]=process.argv.slice(2);if(!auditFile||!mappingFile||!outputFile)throw Error('Uso: node resumir-materiais.mjs <leitura.json> <criacao-nativa.json> <novo-resumo.json>');
  const bytes=await Promise.all([auditFile,mappingFile].map(f=>fs.readFile(f)));
  const result=summarizeMaterials(...bytes.map(b=>JSON.parse(b.toString('utf8').replace(/^\uFEFF/,''))));
  result.sources=[auditFile,mappingFile].map((file,i)=>({path:file,sha256:createHash('sha256').update(bytes[i]).digest('hex')}));
  await fs.writeFile(outputFile,JSON.stringify(result,null,2)+'\n',{flag:'wx'});console.log(JSON.stringify({expected:result.expectedLogicalUnits,matched:result.identityMatchedUnits,compressionRead:result.concreteCompressionReadUnits,structuralApproval:false}));
}

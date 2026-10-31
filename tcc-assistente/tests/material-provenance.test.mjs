import test from 'node:test';
import assert from 'node:assert/strict';
import {summarizeMaterials} from '../connectors/RevitAudit/resumir-materiais.mjs';

function fixture(){return {
  mapping:{elements:[{id:'P1',revitId:10,uniqueId:'uid-10'},{id:'V1',revitId:20,uniqueId:'uid-20'}]},
  audit:{schema:'tcc-revit-material-audit/1',status:'native_read_with_explicit_limits',count:2,transactionsStarted:0,nativeDocumentSaved:false,
    document:{modifiedBefore:false,modifiedAfter:false},elements:[
      {id:10,uniqueId:'uid-10',structuralMaterialId:30,assignmentStatus:'FamilyInstance.StructuralMaterialId'},
      {id:20,uniqueId:'uid-20',structuralMaterialId:null,geometryMaterialIds:[30],assignmentStatus:'unassigned'}],
    materials:[{id:30,name:'C25',status:'asset_read',asset:{class:'Concrete',concreteCompression:{status:'read',converted:25}}}]}
};}

test('associa UniqueId e ID, sem promover material geometrico a atribuicao estrutural',()=>{
  const {audit,mapping}=fixture(),r=summarizeMaterials(audit,mapping);
  assert.equal(r.identityMatchedUnits,2);assert.equal(r.assignmentObservedUnits,1);assert.equal(r.concreteCompressionReadUnits,1);
  assert.equal(r.rows[1].concreteCompressionMPa,null);assert.equal(r.transferLossProven,false);assert.equal(r.structuralApproval,false);
});

test('nome C25 nao preenche compressao ausente e ausencia nao vira zero',()=>{
  const {audit,mapping}=fixture();audit.materials[0].asset.concreteCompression={status:'unavailable',converted:null};
  const r=summarizeMaterials(audit,mapping);assert.equal(r.concreteCompressionReadUnits,0);assert.equal(r.rows[0].materialName,'C25');assert.equal(r.rows[0].concreteCompressionMPa,null);
});

test('ID numerico divergente e UniqueId ausente impedem associacao, sem usar nome como substituto',()=>{
  const {audit,mapping}=fixture();audit.elements[0].id=999;audit.elements[1].uniqueId='other';
  const r=summarizeMaterials(audit,mapping);assert.equal(r.identityMatchedUnits,0);assert.equal(r.sourceMappingCompleted,false);
  assert.deepEqual(r.rows.map(x=>x.status),['native_id_mismatch','native_element_absent']);assert.deepEqual(r.extraNativeCandidates,['other']);
});

test('duplicidades e campo de atribuicao ausente sao recusados; documento sujo fica identificado',()=>{
  const {audit,mapping}=fixture();audit.document.modifiedBefore=true;audit.document.modifiedAfter=true;
  assert.equal(summarizeMaterials(audit,mapping).savedSnapshotObserved,false);
  delete audit.elements[1].structuralMaterialId;assert.throws(()=>summarizeMaterials(audit,mapping),/atribuicao/);
  const f=fixture();f.audit.elements[1].uniqueId=f.audit.elements[0].uniqueId;assert.throws(()=>summarizeMaterials(f.audit,f.mapping),/duplicado/);
});

test('recusa IDs numericos fora da precisao segura do JSON/JavaScript',()=>{
  const {audit,mapping}=fixture();audit.elements[0].id=Number.MAX_SAFE_INTEGER+1;
  assert.throws(()=>summarizeMaterials(audit,mapping),/precisao segura/);
});

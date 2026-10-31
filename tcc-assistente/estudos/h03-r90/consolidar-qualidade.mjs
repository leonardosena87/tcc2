import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';

export async function consolidateQuality(root,output) {
  const sourceNames={
    initial:'outputs/Resultados-H03-R72-PARCIAIS-NAO-FINAIS/R72-resultados-parciais.json',
    materialCAD:'outputs/Conferencia-H03-R51-PARAMETROS-NAO-EXECUTAR/R51-parametros-CAD.json',
    materialBIM:'outputs/Conferencia-H03-R51-PARAMETROS-NAO-EXECUTAR/R51-parametros-BIM.json',
    grouping:'outputs/Agrupamento-H03-R81-TESTE-NAO-EXECUTAR/R81-resultado.json',
    authoring:'outputs/Autoria-H03-R84-AUDITORIA-NAO-EXECUTAR/R84-auditoria-autoria.json',
    failedUI:'outputs/Cargas-H03-R85-RETOMADA-NAO-EXECUTAR/R85-resultado.json',
    premises:'outputs/Premissas-H03-R87-CONSOLIDACAO-NAO-EXECUTAR/R87-matriz-premissas-comuns.json',
    volumes:'outputs/Quantidades-H03-R88-UNIAO-GEOMETRICA-NAO-EXECUTAR/verificacao-rigorosa/R88-quantidades-geometricas.json'};
  const s={},sources={};const sha=b=>createHash('sha256').update(b).digest('hex');
  for(const [key,name]of Object.entries(sourceNames)){const bytes=await fs.readFile(path.join(root,name));s[key]=JSON.parse(bytes.toString('utf8').replace(/^\uFEFF/,''));sources[key]={path:name,sha256:sha(bytes)};}
  const initial=s.initial.initialTypedAggregate,complement=s.initial.complementedLogicalElements;
  if(initial.denominatorLogicalElements!==62||initial.CAD_native!==0||initial.BIM_native!==51)throw Error('Denominador inicial requer nova analise.');
  if(s.initial.cadDrawingContent.contoursReceived!==62||s.initial.cadDrawingContent.textContentsReceived!==66)throw Error('Retencao grafica nao confirmada.');
  if(s.materialCAD.changedFieldCount!==4||s.materialBIM.changedFieldCount!==4)throw Error('Alteracoes comuns nao confirmadas.');
  if(!s.grouping.nativeDivisionCausallyRemovedD16InThisTrial||s.grouping.adoptedAsFinalDesign)throw Error('Escopo do teste de agrupamento mudou.');
  if(s.failedUI.nativeLoadApplied||!s.authoring.cad.equal)throw Error('Estado nativo ou auditoria de autoria requer revisao.');
  const comparisons=Object.values(s.volumes.ifcCheckpoints);
  if(comparisons.length!==4||!comparisons.every(v=>v.nominalSourceComparison.sameOccupiedVolumeWithinDeclaredCriterion))throw Error('Dominios geometricos nao conferiram.');
  const observations=[
    {id:'O01',phase:'chegada_inicial_CAD',category:'representacao_prevista_e_complementacao',finding:'Contornos e conteudos de texto chegaram; nao eram elementos estruturais nativos.',evidence:['initial'],numbers:{contours:62,textContents:66,initialNativeLogicalUnits:0,denominator:62,laterComplementedLogicalUnits:complement.CAD},notDefectCount:true,notOperationCount:true},
    {id:'O02',phase:'chegada_inicial_BIM',category:'disponibilidade_nativa_e_complementacao',finding:'Chegaram pilares e vigas logicas tipados apos tratamento do IFC; as lajes exigiram complemento.',evidence:['initial'],numbers:{columns:22,logicalBeams:29,nativeSlabs:0,initialNativeLogicalUnits:51,denominator:62,laterComplementedLogicalUnits:complement.BIM},notDefectCount:true,notOperationCount:true},
    {id:'O03',phase:'preparacao_intercambio_BIM',category:'normalizacao_do_formato',finding:'O tratamento do IFC integra o esforco BIM; nao pode desaparecer da metodologia.',evidence:['initial'],numbers:s.initial.bimInputTreatment,provenNativeDefectCount:null},
    {id:'O04',phase:'retencao_grafica_CAD',category:'diferenca_de_representacao',finding:'Conteudo preservado nao comprova tipografia ou classe TEXT/MTEXT identica.',evidence:['initial'],numbers:s.initial.cadDrawingContent,provenNativeDefectCount:null},
    {id:'O05',phase:'materiais_no_receptor',category:'adequacao_comum_das_premissas',finding:'Quatro campos foram ajustados em cada ramo; a origem desses valores por IFC/DWG nao foi demonstrada.',evidence:['materialCAD','materialBIM'],numbers:{changedFieldsPerBranch:4},transferDefectProven:false},
    {id:'O06',phase:'concepcao_e_autoria',category:'concepcao_comum',finding:'A altura N2 foi harmonizada entre a proposta de autoria e o estudo do receptor; isso nao e correcao exclusiva de um fluxo.',evidence:['authoring','premises'],numbers:{authoringLogicalBeams:29,roofBeamHeightM:0.30,authoringUnits:62},structuralApproval:false},
    {id:'O07',phase:'teste_local_de_agrupamento_BIM',category:'efeito_operacional_local_observado',finding:'Uma divisao de viga eliminou a mensagem D16 naquele teste, sem provar que o IFC originou o agrupamento.',evidence:['grouping'],numbers:{groupsBefore:20,groupsAfter:s.grouping.after.nativeBeamGroups,beamErrorsAfter:s.grouping.after.beamErrorMessages},originalImportCauseProven:false,adoptedAsFinalDesign:false,globalErrorCount:null},
    {id:'O08',phase:'quantitativo_geometrico',category:'particionamento_e_intersecoes',finding:'Os quatro IFCs conservam o dominio ocupado; somas de partes incluem encontros contados mais de uma vez.',evidence:['volumes'],numbers:{unionM3:s.volumes.sourceNominalUnionVolumeM3,sourceSeparatePieceSumM3:s.volumes.sourceNominalSeparateVolumeM3,IFCIndividualMeshSumM3:comparisons[0].sumIndividualMeshVolumesM3,IFCOverlapM3:comparisons[0].internalOverlapM3,IFCIntersectionPairs:comparisons[0].intersectionPairs.length},transferDefectProven:false,structuralApproval:false},
    {id:'O09',phase:'automacao_da_interface',category:'instrumentacao',finding:'A tentativa R85 foi interrompida sem aplicar cargas; nao deve ser atribuida a defeito DWG/IFC.',evidence:['failedUI'],numbers:{nativeLoadsApplied:0,newProcessing:0},provenTransferDefectCount:null},
    {id:'O10',phase:'procedencia_das_entradas',category:'consistencia_documental_comum',finding:'Metadados antigos de unidade, reservatorio, secao padrao e versao foram identificados sem reescrever o historico.',evidence:['premises'],numbers:{metadataReviewItems:s.premises.staleMetadataFound.length},notNativeErrorCount:true}
  ];
  const result={schema:'tcc-quality-evidence-register/1',revision:'H03/R90',createdAtUtc:new Date().toISOString(),case:'H03; uma edificacao; checkpoints distintos identificados',sources,observations,
    metrics:{initialNativeAvailability:{checkpoint:'R45/R46 apos tratamento do IFC',unit:'unidades logicas da proposta, nao solidos ou grupos de detalhamento',denominator:62,CAD:0,BIM:51,BIMPercent:51/62*100,notErrorRate:true,notOverallQualityIndex:true},subsequentComplementation:{CAD:complement.CAD,BIM:complement.BIM,unit:'unidades logicas atendidas; nao numero de cliques ou defeitos'},geometricUnionAudit:{fourIFCCheckpoints:4,sameOccupiedDomain:true,volumetricSymmetricDifferencesM3:comparisons.map(v=>v.nominalSourceComparison.symmetricDifferenceM3),criteriaAreComputationalNotNormative:true},finalCorrectionTotals:{CAD:null,BIM:null},finalFlowTimeTotals:{CAD:null,BIM:null}},
    finalAssessmentCompleted:false,finalWinner:null,structuralApproval:false,monographChanged:false,
    interpretation:'Dez observacoes metodologicas nao sao dez erros por projeto. Nao somar unidades, campos, mensagens, operacoes, partes IFC e itens de metadados. Nem toda complementacao e perda de informacao.'};
  for(const [key,name]of Object.entries(sourceNames))if(sha(await fs.readFile(path.join(root,name)))!==sources[key].sha256)throw Error('Fonte alterada: '+key);
  await fs.mkdir(output,{recursive:false});await fs.writeFile(path.join(output,'R90-registro-qualidade.json'),JSON.stringify(result,null,2)+'\n');
  return result;
}

if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href){const[root,output]=process.argv.slice(2);if(!root||!output)throw Error('Uso: node consolidar-qualidade.mjs <D:/TCC> <nova pasta>');const r=await consolidateQuality(root,output);console.log(JSON.stringify({observations:r.observations.length,initialTypedNative:r.metrics.initialNativeAvailability,finalCorrectionTotals:r.metrics.finalCorrectionTotals,finalWinner:null}));}

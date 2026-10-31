import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';

// Decisoes ja confirmadas na conversa; nao sao escolhas novas de engenharia.
export const confirmedDecisions=Object.freeze({municipality:'Vitória da Conquista',state:'BA',wallFinishedThicknessM:0.15,slumpUnit:'cm',tankCapacityL:1000,superstructureOnly:true,roofAccess:'apenas manutencao',ceiling:'gesso acartonado',roofSheetThicknessMM:6,roofSlope:0.10,roofSupport:'estrutura metalica leve',preserveArchitecturalHeights:true});

export function consolidate(proposal,cad,bim,tank) {
  const study=proposal.parameters?.study;
  if(proposal.schema!=='tcc-esboco/1'||proposal.elements?.length!==62||!study)throw Error('Proposta comum H03 nao reconhecida.');
  if(study.concreto.fckMPa!==25||study.aco.fykMPa!==500)throw Error('Premissas de material divergentes da decisao registrada.');
  const receivers={CAD:cad.observedAfterReopen,BIM:bim.observedAfterReopen};
  if(!receivers.CAD||!receivers.BIM)throw Error('Leituras historicas de materiais incompletas.');
  const covers=study.cobrimentosNominaisMm;
  const concrete={class:'C25',fckMPa:25,gammaCInformed:study.concreto.gammaCInformado,EciGPaInformed:study.concreto.EciGPaInformado,EcsGPaInformed:study.concreto.EcsGPaInformado,receiverEcsGPaObservedR51:{CAD:receivers.CAD.EcsMpaDisplayed/1000,BIM:receivers.BIM.EcsMpaDisplayed/1000},differenceMeaning:'24,1 GPa informado e 24,150 GPa exibido sao mantidos separadamente; nao se substitui a entrada silenciosamente.',aggregateMaxMM:25,aggregatePetrographyConfirmedByUser:null,receiverAggregateHypothesisR51:{CAD:receivers.CAD.aggregateType,BIM:receivers.BIM.aggregateType},petrographyMeaning:'Granito foi observado como hipotese no cadastro R51, sem caracterizacao de material real.',cementRequested:'CP II-E',receiverCementFamilyObservedR51:{CAD:receivers.CAD.cementFamily,BIM:receivers.BIM.cementFamily},cementSubtypeEVerifiedInNativeUI:false};
  const beamSections=proposal.elements.filter(e=>e.kind==='beam').map(e=>({sourceId:e.id,level:e.level,bM:e.b,hM:e.h,topM:e.z}));
  const roofBeams=beamSections.filter(e=>e.level===1);
  if(!roofBeams.length||roofBeams.some(e=>e.hM!==0.30))throw Error('As vigas N2 nao correspondem a R83.');
  return {
    schema:'tcc-common-input-ledger/1',revision:'H03/R87',status:'MATRIZ COMUM PARCIAL; NAO LIBERADA PARA ENSAIO FINAL',
    confirmedUserDecisions:{...confirmedDecisions},geometrySourceRunId:proposal.runId,
    location:{municipality:confirmedDecisions.municipality,state:confirmedDecisions.state,siteCoordinates:null,windParametersFinalized:false},
    scope:{superstructureOnly:true,geotechnicalReportAvailable:false,realFoundationsDesigned:false,supportIdealization:'Apoios idealizados do estudo; rigidez e vinculacoes ainda exigem conferencia.'},
    wall:{material:'bloco ceramico',finishedThicknessM:0.15,blockBodyThicknessM:null,finishThicknessPerFaceM:null,unitSurfaceWeightKNM2:null,status:'Espessura acabada confirmada; composicao e peso completo nao definidos.',weightAppliedInNativeModel:false},
    concrete,steel:{classRequested:'CA-50',fykMPaInformed:500,receiverClassSeenInActiveRowsR51:{CAD:receivers.CAD.steelClassesInObservedActiveRows,BIM:receivers.BIM.steelClassesInObservedActiveRows},completeMechanicalSteelRegisterVerified:false},
    environment:{class:'II',meaning:'Moderada urbana; premissa do estudo'},nominalCoverMM:{slabs:covers.lajes,beams:covers.vigas,columns:covers.pilares},
    slump:{slabsBeamsColumns:{nominal:10,tolerance:2,unit:'cm'},stairs:{nominal:6,tolerance:2,unit:'cm'},receiverNominalObservedR51:{CAD:receivers.CAD.slumpNominalCm,BIM:receivers.BIM.slumpNominalCm},toleranceStoredInNativeFieldVerified:false},
    slab:{system:'laje macica de concreto armado',nominalThicknessM:0.14,designApproved:false},
    levels:{valuesM:[...proposal.parameters.zs],reference:'Datum do modelo; nao e cota de fundacao real',architecturalHeightsMayBeChanged:false},
    beamSections:{mustUseElementValues:true,globalGeneratorDefaultHeightM:proposal.parameters.beamH,globalDefaultDoesNotDescribeAllCurrentBeams:true,byElement:beamSections},
    roof:{cover:'telha ondulada de fibrocimento',sheetThicknessMM:6,slope:0.10,support:'estrutura metalica leve',access:'apenas manutencao',ceiling:'gesso acartonado',fullReactionMapApplied:false,regionsP1P2Closed:false,metallicSupportDesigned:false},
    tank:{capacityL:1000,capacityConfirmed:true,positionAndSupportFinalized:false,tareKN:null,pedestalKN:null,fullAssemblyWeightKN:tank.fullAssemblyWeightKN??null,modelSelected:tank.modelSelected??null,alternativesRevision:'R71',candidatePositionIsNotAcceptedLocation:true,nativeLoadsApplied:false},
    normative:{localConcreteStandard:'ABNT NBR 6118:2026, exemplar local identificado na R74',sourcePremisesOriginallyMentioned:'2014',genericGeometryCheckerStillMentions:'2023',full2026ImplementationVerified:false,structuralComplianceAttested:false},
    verificationScope:{receiverMaterialsCheckpoint:'R51, leitura depois de salvar/fechar/reabrir; nao e nova leitura R79/R85',qFactorsCheckpoint:'R78, fatores 0,50 / 0,40 / 0,30 conferidos; isso nao aplica Q_TELHADO',authoringGeometryCheckpoint:'R84 sobre R83; IDs/categorias, comprimentos/areas disponiveis e contornos/textos CAD',revitAuthoringMaterialPropertiesReadBack:false,transferCauseForMaterialSettingsProven:false},
    staleMetadataFound:[
      {field:'parameters.study.consistenciaInformada/unidade e pendencias',meaning:'A unidade cm ja foi confirmada pelo usuario; a pendencia historica nao deve ser repetida como pergunta aberta.'},
      {field:'parameters.study.reservatorio',meaning:'Capacidade de 1.000L confirmada; posicao, tara e apoio continuam pendentes.'},
      {field:'parameters.study.agregado.naturezaPetrografica',meaning:'Usuario nao confirmou petrografia; granito observado no Eberick e hipotese, nao ensaio de material.'},
      {field:'parameters.beamH',meaning:'0,55m e um valor padrao do gerador; os elementos atuais possuem secoes proprias, com N2 em 0,30m.'},
      {field:'studyHypothesis.id',meaning:'Identificacao H02-R12 e historica; o arquivo de autoria atual e H03/R83, conforme runId, eventos e hashes.'},
      {field:'metadados de norma',meaning:'Mencionar 2026 no JSON nao comprova que o verificador 2023 ou o Eberick instalado implemente integralmente essa edicao.'}
    ],
    approvedForFinalComparison:false,loadsComplete:false,eluElsApproved:false,nativeModelsChanged:false,monographChanged:false
  };
}

export async function buildLedger(root,output) {
  const files={proposal:'outputs/Autoria-H03-R83-SINCRONIZACAO-GEOMETRICA-NAO-EXECUTAR/H03-R83-proposta.json',CAD:'outputs/Conferencia-H03-R51-PARAMETROS-NAO-EXECUTAR/R51-parametros-CAD.json',BIM:'outputs/Conferencia-H03-R51-PARAMETROS-NAO-EXECUTAR/R51-parametros-BIM.json',tank:'outputs/Reservatorio-H03-R71-ALTERNATIVAS-NAO-APLICADO/R71-reservatorio-alternativas.json'};
  const sources={},values={};const sha=b=>createHash('sha256').update(b).digest('hex');
  for(const [id,name] of Object.entries(files)){const b=await fs.readFile(path.join(root,name));sources[id]={path:name,sha256:sha(b)};values[id]=JSON.parse(b.toString('utf8').replace(/^\uFEFF/,''));}
  const result=consolidate(values.proposal,values.CAD,values.BIM,values.tank);result.sources=sources;result.createdAtUtc=new Date().toISOString();
  for(const [id,name] of Object.entries(files))if(sha(await fs.readFile(path.join(root,name)))!==sources[id].sha256)throw Error('Fonte alterada: '+id);
  await fs.mkdir(output,{recursive:false});await fs.writeFile(path.join(output,'R87-matriz-premissas-comuns.json'),JSON.stringify(result,null,2)+'\n');return result;
}

if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href){const[root,output]=process.argv.slice(2);if(!root||!output)throw Error('Uso: node consolidar-premissas.mjs <D:/TCC> <nova pasta>');const r=await buildLedger(root,output);console.log(JSON.stringify({revision:r.revision,beamRows:r.beamSections.byElement.length,wallFinishedM:r.wall.finishedThicknessM,wallBodyM:r.wall.blockBodyThicknessM,tankL:r.tank.capacityL,loadsComplete:r.loadsComplete,nativeModelsChanged:false}));}

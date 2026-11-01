import fs from 'node:fs/promises';
import path from 'node:path';
import {inventory} from '../h03-r86/inventariar-tempos.mjs';

const [root,output]=process.argv.slice(2);
if(!root||!output)throw Error('Uso: node inventariar.mjs <raiz TCC> <pasta nova>');
const result=await inventory(root,output);
const recent=result.records.filter(r=>/R11[89]|R12[0-3]/.test(r.source));
for(const r of result.records) {
  if(/R116.*CAD-sessao-tempo/.test(r.source)||/R121.*BIM-sessao-tempo/.test(r.source)||/R122.*CAD-sessao-tempo/.test(r.source)) {
    r.knownInterruption=true;
    r.interruptionAnnotation='Anotacao retrospectiva de retomada/pesquisa/interface, sem alterar limites nem estimar tempo ativo.';
  }
  if(/R121.*CAD-processamento-tempo/.test(r.source)) {
    r.observationBoundaryNote='Termino registrado apos inspecao da captura de estrutura ja processada; inclui atraso de registro, nao tempo puro do solver.';
  }
}
const summary={revision:'H03/R124',createdAtUtc:result.createdAtUtc,files:result.files,counts:result.counts,
  overlappingPairs:result.overlaps.length,recentRecords:recent,
  fullFlowTotals:result.fullFlowTotals,isolatedAIWorkOnMainBuilding:result.isolatedAIWorkOnMainBuilding,
  finalRankingAllowed:false,
  limits:['Fotografia de arquivos diretos *tempo*.json ate as consultas R122; scripts R123 com tempo embutido nao sao expandidos.',
    'Banco central e demonstracoes ficam separados do experimento principal.',
    'Ausencia de duracao nao equivale a zero; sessoes exploratorias nao representam so tempo ativo.',
    'Intervalos de processamento sao contidos nas sessoes e nao devem ser somados novamente.',
    'Sessao CAD R121 inclui pesquisa e tentativa de no; BIM R121 inclui retomada. Escopos diferentes, sem ranking.',
    'R122 inclui consulta e exportacao com pesquisa/interface; nao mede duracao pura de exportacao.',
    'Tempo de script nao mede esforco de autoria, inferencia, tokens ou custo da IA.',
    'Totais completos e comparaveis CAD/BIM e esforco isolado da IA permanecem desconhecidos.']};
await fs.writeFile(path.join(output,'R124-resumo.json'),JSON.stringify(summary,null,2)+'\n');
await fs.writeFile(path.join(output,'R86-inventario-tempos.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({files:summary.files,counts:summary.counts,overlaps:summary.overlappingPairs,recentRecords:recent.length,finalRankingAllowed:false}));

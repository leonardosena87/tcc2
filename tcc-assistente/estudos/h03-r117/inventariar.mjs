import fs from 'node:fs/promises';
import path from 'node:path';
import {inventory} from '../h03-r86/inventariar-tempos.mjs';

const [root,output]=process.argv.slice(2);
if(!root||!output)throw Error('Uso: node inventariar.mjs <raiz TCC> <pasta nova>');
const result=await inventory(root,output);
const recent=result.records.filter(r=>/R11[1-6]/.test(r.source));
// A anotacao retrospectiva nao altera os limites nem inventa tempo ativo.
for(const r of recent)if(/R116.*CAD-sessao-tempo/.test(r.source)) {
  r.knownInterruption=true;
  r.interruptionAnnotation='Sessao inclui intervalo de retomada entre a configuracao e continuacao do usuario; tempo ativo nao medido.';
}
const summary={revision:'H03/R117',createdAtUtc:result.createdAtUtc,
  files:result.files,counts:result.counts,overlappingPairs:result.overlaps.length,
  recentRecords:recent,fullFlowTotals:result.fullFlowTotals,
  isolatedAIWorkOnMainBuilding:result.isolatedAIWorkOnMainBuilding,
  finalRankingAllowed:false,
  limits:['Fotografia de arquivos diretos *tempo*.json ate a R116, processos R84, banco central e demos separados.',
    'Nao e todo o esforco do projeto; duracao ausente nao e zero.',
    'R107 e R116 CAD contem intervalos de retomada; nao representam tempo ativo.',
    'Intervalos de processamento estao contidos nas sessoes; nao somar recortes sobrepostos.',
    'Tempos de scripts nao medem autoria, inferencia ou tokens da IA.',
    'Totais completos e comparaveis CAD/BIM continuam desconhecidos; sem ranking.']};
await fs.writeFile(path.join(output,'R117-resumo.json'),JSON.stringify(summary,null,2)+'\n');
await fs.writeFile(path.join(output,'R86-inventario-tempos.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({files:summary.files,counts:summary.counts,overlaps:summary.overlappingPairs,recentRecords:recent.length,finalRankingAllowed:false}));

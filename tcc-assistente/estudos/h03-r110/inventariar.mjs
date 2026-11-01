import fs from 'node:fs/promises';
import path from 'node:path';
import {inventory} from '../h03-r86/inventariar-tempos.mjs';

const [root,output]=process.argv.slice(2);
if(!root||!output)throw Error('Uso: node inventariar.mjs <raiz TCC> <pasta nova>');
const result=await inventory(root,output);
const recent=result.records.filter(r=>/R10[6-9]/.test(r.source));
const summary={revision:'H03/R110',createdAtUtc:result.createdAtUtc,
  files:result.files,counts:result.counts,overlappingPairs:result.overlaps.length,
  recentRecords:recent,fullFlowTotals:result.fullFlowTotals,
  isolatedAIWorkOnMainBuilding:result.isolatedAIWorkOnMainBuilding,
  finalRankingAllowed:false,
  limits:['Inventario de arquivos diretos *tempo*.json e quatro processos R84; nao e todo o esforco.',
    'Duracoes de sessao podem conter interrupcoes e incluem observacao/interface.',
    'R107 CAD inclui lacuna de conversa de varias horas; nao classificar como tempo ativo.',
    'Intervalos de processamento estao contidos nas sessoes; nao somar recortes sobrepostos.',
    'Registro R108 mede somente script aritmetico, nao autoria ou inferencia IA.',
    'Nao ha registro completo elegivel para classificacao dos dois fluxos finais.']};
await fs.writeFile(path.join(output,'R110-resumo.json'),JSON.stringify(summary,null,2)+'\n');
console.log(JSON.stringify({files:summary.files,counts:summary.counts,overlaps:summary.overlappingPairs,recentRecords:recent.length,finalRankingAllowed:false}));

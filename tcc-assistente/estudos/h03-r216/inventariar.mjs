import fs from 'node:fs/promises';
import path from 'node:path';
import {inventory} from '../h03-r86/inventariar-tempos.mjs';

const [root,output]=process.argv.slice(2);
if(!root||!output)throw Error('Uso: node inventariar.mjs <raiz TCC> <pasta nova>');
const r=await inventory(root,output);
r.revision='H03/R216';
r.schemaNote='Duracoes em segundos de wallSeconds/intervalo_observado_s sao normalizadas para ms, preservando valor e unidade originais. Inventario superficial: nao expande conteineres nem infere tempos ausentes.';
const serialized=JSON.stringify(r,null,2)+'\n';
await fs.writeFile(path.join(output,'R86-inventario-tempos.json'),serialized);
await fs.rename(path.join(output,'R86-inventario-tempos.json'),path.join(output,'R216-inventario-tempos.json'));
const recent=r.records.filter(x=>/R(?:20\d|21[0-5])[^\d]/i.test(x.source));
const summary={revision:r.revision,createdAtUtc:r.createdAtUtc,files:r.files,counts:r.counts,overlappingPairs:r.overlaps.length,recentRecords:recent,
 fullFlowTotals:r.fullFlowTotals,isolatedAIWorkOnMainBuilding:r.isolatedAIWorkOnMainBuilding,finalRankingAllowed:false,
 limitations:['Arquivos diretos tempo*.json: relatorios nativos DOCX/TXT e tempos embutidos em README nao sao varridos por este inventario.',
 'Intervalos observados incluem navegacao, raciocinio, capturas e possiveis interrupcoes; nao sao tempo ativo puro.',
 'Nao somar registros sobrepostos, revisoes exploratorias, demonstracoes ou tempo interno de calculo ao intervalo que ja o contem.',
 'Nao ha pares completos de autoria, intercambio, complementacao e verificacao final para classificar CAD/BIM.']};
await fs.writeFile(path.join(output,'R216-resumo-tempos.json'),JSON.stringify(summary,null,2)+'\n');
console.log(JSON.stringify({files:r.files,counts:r.counts,overlaps:r.overlaps.length,recent:recent.length,finalRankingAllowed:false}));

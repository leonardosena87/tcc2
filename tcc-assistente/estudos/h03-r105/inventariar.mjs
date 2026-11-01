import {inventory} from '../h03-r86/inventariar-tempos.mjs';
const [root,output]=process.argv.slice(2);
if(!root||!output)throw Error('Uso: node inventariar.mjs <raiz TCC> <pasta nova>');
const r=await inventory(root,output);
console.log(JSON.stringify({files:r.files,counts:r.counts,overlaps:r.overlaps.length,finalRankingAllowed:r.finalRankingAllowed}));

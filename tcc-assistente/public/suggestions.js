export function validateEdits(edits, paragraphs) {
  if(!Array.isArray(edits)||edits.length>500)throw new Error('A IA devolveu alterações inválidas.');
  const originals=new Map(paragraphs.map(p=>[p.index,p.text]));const seen=new Set();
  return edits.map(edit=>{
    if(!edit||!Number.isInteger(edit.index)||seen.has(edit.index)||!originals.has(edit.index)||typeof edit.original!=='string'||edit.original!==originals.get(edit.index)||typeof edit.revised!=='string'||!edit.revised.trim()||edit.revised.length>20000)throw new Error('Uma alteração não corresponde ao texto original. Nada foi aplicado.');
    seen.add(edit.index);return edit;
  }).filter(edit=>edit.original!==edit.revised);
}
export function normalizeWordText(value) {
  return String(value??'')
    .normalize('NFC')
    .replace(/\r\n?/g,'\n')
    .replace(/[\v\u000b]/g,'\n')
    .replace(/\u00a0/g,' ')
    .replace(/[\u200b-\u200d\u2060\ufeff]/g,'')
    .replace(/[\u0007\n]+$/g,'')
    .replace(/\s+/g,' ')
    .trim();
}
export async function applyEdits(snapshot, edits) {
  const valid=validateEdits(edits,snapshot.paragraphs);
  snapshot.appliedTargets??=[];
  snapshot.complexSkipped=0;
  if(!valid.length)return 0;
  for(const edit of valid){
    const item=snapshot.items.find(candidate=>candidate.index===edit.index);
    if(!item)throw new Error('Não encontrei todos os parágrafos da proposta. Nada foi aplicado.');
    if(item.range.text?.includes('\u0007')||item.result?.value&&/<w:(?:tbl|drawing|pict|fldSimple|fldChar|footnoteReference|endnoteReference|hyperlink|sdt|object)(?:\s|\/?>)/.test(item.result.value))item.complex=true;
    if(!item.complex&&normalizeWordText(item.range.text)!==normalizeWordText(item.original))throw new Error('O documento mudou durante a análise. Nada foi aplicado; tente novamente.');
  }
  const safe=valid.filter(edit=>!snapshot.items.find(item=>item.index===edit.index).complex);
  snapshot.complexSkipped=valid.length-safe.length;
  for(const edit of safe){
    const item=snapshot.items.find(candidate=>candidate.index===edit.index);
    const changed=item.range.insertText(edit.revised,'Replace');
    if(changed?.font)changed.font.highlightColor='#FFFF00';
    snapshot.appliedTargets.push({index:item.wordIndex??edit.index,revised:edit.revised});
  }
  if(safe.length)await snapshot.context.sync();return safe.length;
}

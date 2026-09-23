export function validateEdits(edits, paragraphs) {
  if(!Array.isArray(edits)||edits.length>500)throw new Error('A IA devolveu alterações inválidas.');
  const originals=new Map(paragraphs.map(p=>[p.index,p.text]));const seen=new Set();
  return edits.map(edit=>{
    if(!edit||!Number.isInteger(edit.index)||seen.has(edit.index)||!originals.has(edit.index)||typeof edit.original!=='string'||edit.original!==originals.get(edit.index)||typeof edit.revised!=='string'||!edit.revised.trim()||edit.revised.length>20000)throw new Error('Uma alteração não corresponde ao texto original. Nada foi aplicado.');
    seen.add(edit.index);return edit;
  }).filter(edit=>edit.original!==edit.revised);
}
export async function applyEdits(snapshot, edits) {
  const valid=validateEdits(edits,snapshot.paragraphs);
  snapshot.appliedTargets??=[];
  // Preflight the complete scope before queuing any mutation.
  for(const item of snapshot.items)item.range.load('text');
  const xml=snapshot.items.map(item=>item.range.getOoxml());
  await snapshot.context.sync();
  for(let i=0;i<snapshot.items.length;i++){
    const item=snapshot.items[i];
    if(item.range.text!==item.original||xml[i].value!==item.xml)throw new Error('O documento mudou durante a análise. Nada foi aplicado; tente novamente.');
  }
  for(const edit of valid){
    const changed=snapshot.items.find(item=>item.index===edit.index).range.insertText(edit.revised,'Replace');
    if(changed?.font)changed.font.highlightColor='#FFFF00';
    snapshot.appliedTargets.push({index:edit.index,revised:edit.revised});
  }
  await snapshot.context.sync();return valid.length;
}

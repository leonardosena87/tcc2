let ready = false;
let target = null;
const LIMIT = 120000;
const complex = /<w:(?:tbl|drawing|pict|fldSimple|fldChar|footnoteReference|endnoteReference|hyperlink|sdt|object)(?:\s|\/?>)/;
export function setWordReady(value) {ready=value;}
function requireWord() {if(!ready) throw new Error('Abra este suplemento dentro do Word para acessar o documento.');}
function wordFailure(stage,error){
  if(error?.code==='GeneralException'||error?.name==='OfficeExtension.Error')return new Error(`O Word falhou ao ${stage} (erro ${error.code??error.name}). Feche e reabra o documento e tente novamente.`);
  return error;
}
export async function discardTarget() {
  if(target) {const old=target;target=null;try{old.range.untrack();await old.context.sync();}catch{/* Documento pode ter sido fechado. */}}
}
export async function capture({selection,document,rewrite}) {
  if(!selection && !document && !rewrite) return {selection:'',document:''};
  requireWord();
  const context=new Word.RequestContext();
  const range=context.document.getSelection();
  const body=context.document.body;
  if(selection || rewrite) range.load('text');
  if(document) body.load('text');
  const xml=rewrite ? range.getOoxml() : null;
  await context.sync();
  const selected=selection||rewrite ? range.text : '';
  const content=document?body.text:'';
  if(selected.length>LIMIT || content.length>LIMIT) throw new Error('O contexto ultrapassa 120.000 caracteres. Desmarque o documento inteiro ou selecione um trecho menor.');
  if(rewrite) {
    if(!selected.trim()) throw new Error('Selecione no Word o texto que deseja revisar.');
    if(complex.test(xml.value)) throw new Error('O trecho contém tabelas, campos, links, notas ou imagens. Selecione apenas texto corrido para substituir; use Conversar para analisar conteúdo complexo.');
    range.track(); await context.sync(); target={context,range,original:selected};
  }
  return {selection:selected,document:content};
}
export async function applyReplacement(text) {
  requireWord();
  if(!target) throw new Error('Capture o trecho novamente para preparar uma revisão.');
  if(!text.trim()) throw new Error('O texto proposto está vazio.');
  const {context,range,original}=target;
  range.load('text'); const xml=range.getOoxml(); await context.sync();
  if(range.text!==original || complex.test(xml.value)) throw new Error('O trecho mudou desde o pedido. Prepare uma nova revisão antes de substituir.');
  range.insertText(text,Word.InsertLocation.replace);
  await context.sync(); await discardTarget();
}
export async function insertAtCursor(text) {
  requireWord();
  if(!text.trim()) throw new Error('Não há texto para inserir.');
  await Word.run(async context=>{
    // Insert after the current selection, never replace whatever is now selected.
    context.document.getSelection().insertText(text,Word.InsertLocation.end);
    await context.sync();
  });
}
export async function applySuggestionsInWord(scope, requestEdits, applyEdits) {
  requireWord();
  let stage='ler os parágrafos do documento';
  let captured;
  try{captured=await Word.run(async context=>{
    // Resolve the selection first and return only plain values from this batch.
    const selection=scope==='selection'?context.document.getSelection():null;
    if(selection)selection.load('text');
    const paragraphs=context.document.body.paragraphs;paragraphs.load('items');await context.sync();
    if(selection&&!selection.text.trim())throw new Error('Selecione os parágrafos no documento antes de clicar no botão.');
    if(!selection&&paragraphs.items.length===0)throw new Error('O documento está vazio. Insira um texto antes de aplicar sugestões.');
    if(!selection&&paragraphs.items.length>500)throw new Error('O documento tem mais de 500 parágrafos. Selecione uma seção menor.');
    const items=paragraphs.items.map((paragraph,index)=>{
      const range=paragraph.getRange('Content');
      return {index,range,relation:selection?range.compareLocationWith(selection):null};
    });
    for(let start=0;start<items.length;start+=50){
      const batch=items.slice(start,start+50);for(const item of batch)item.range.load('text');await context.sync();
      if(selection)for(const item of batch)item.inSelection=['Contains','ContainsStart','ContainsEnd','Inside','InsideStart','InsideEnd','Equal','OverlapsBefore','OverlapsAfter'].includes(item.relation.value);
    }
    const scoped=selection?items.filter(item=>item.inSelection):items;
    if(scoped.length>500||(selection?.text?.length??0)>LIMIT)throw new Error('O escopo excede o limite de revisão. Selecione uma seção menor.');
    const result=scoped.filter(item=>item.range.text?.trim()).map(item=>({index:item.index,text:item.range.text}));
    if(!result.length)throw new Error('Não há parágrafos com texto para revisar.');
    if(result.reduce((n,item)=>n+item.text.length,0)>LIMIT)throw new Error('O documento excede o limite de revisão. Selecione uma seção menor.');
    return {paragraphs:result,items:result,skipped:scoped.length-result.length};
  });}catch(error){throw wordFailure(stage,error);}
  // The network request runs with no live Word proxies. Reopen a fresh batch
  // afterwards and verify the exact paragraphs before making any change.
  const edits=await requestEdits(captured.paragraphs);
  stage='revalidar e aplicar as alterações';
  try{return await Word.run(async context=>{
    const indexes=new Set(Array.isArray(edits)?edits.map(edit=>edit?.index).filter(Number.isInteger):[]);
    if(!indexes.size)return {count:0,skipped:captured.skipped,complexSkipped:0,targets:[]};
    const paragraphs=context.document.body.paragraphs;paragraphs.load('items');await context.sync();
    const source=new Map(captured.items.map(item=>[item.index,item]));
    const items=[...indexes].map(index=>{
      const item=source.get(index);const paragraph=paragraphs.items[index];
      if(!item||!paragraph)throw new Error('O documento mudou durante a análise. Refaça a aplicação das sugestões.');
      const range=paragraph.getRange('Content');range.load('text');return {...item,range,result:range.getOoxml()};
    });
    await context.sync();
    const snapshot={context,items,paragraphs:captured.paragraphs,skipped:captured.skipped,appliedTargets:[],complexSkipped:0};
    const count=await applyEdits(snapshot,edits);
    return {count,skipped:snapshot.skipped,complexSkipped:snapshot.complexSkipped,targets:snapshot.appliedTargets};
  });}catch(error){throw wordFailure(stage,error);}
}
export async function clearSuggestionHighlights(targets){
  if(!targets?.length)return 0;
  return Word.run(async context=>{
    const paragraphs=context.document.body.paragraphs;paragraphs.load('items');await context.sync();
    const cleared=[];
    for(const target of targets){
      const paragraph=paragraphs.items[target.index];if(!paragraph)continue;
      paragraph.load('text');await context.sync();
      if(paragraph.text!==target.revised)continue;
      paragraph.getRange('Content').font.highlightColor='None';cleared.push(target);
    }
    await context.sync();return cleared.length;
  });
}
export async function releaseSuggestions(snapshot){
  if(!snapshot)return;
  // A substituição pode invalidar os ranges rastreados. Nesse caso o Word
  // retorna ItemNotFound ao chamar untrack; a limpeza é apenas best-effort.
  for(const item of snapshot.items){try{item.range.untrack();}catch{/* Range já invalidado após a aplicação. */}}
  try{await snapshot.context.sync();}catch{/* O documento pode ter sido fechado ou alterado. */}
}

let ready = false;
let target = null;
const LIMIT = 120000;
const complex = /<w:(?:tbl|drawing|pict|fldSimple|fldChar|footnoteReference|endnoteReference|hyperlink|sdt|object)(?:\s|\/?>)/;
export function setWordReady(value) {ready=value;}
function requireWord() {if(!ready) throw new Error('Abra este suplemento dentro do Word para acessar o documento.');}
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
  return Word.run(async context=>{
    // Resolve the selection first, then map intersecting paragraphs to stable
    // document-wide indexes. This also avoids holding a transient selection
    // proxy after the pane takes focus.
    const selection=scope==='selection'?context.document.getSelection():null;
    if(selection)selection.load('text');
    const paragraphs=context.document.body.paragraphs;paragraphs.load('items');await context.sync();
    if(selection&&!selection.text.trim())throw new Error('Selecione os parágrafos no documento antes de clicar no botão.');
    if(!selection&&paragraphs.items.length===0)throw new Error('O documento está vazio. Insira um texto antes de aplicar sugestões.');
    const items=paragraphs.items.map((paragraph,index)=>{
      const range=paragraph.getRange('Content');
      return {index,range,relation:selection?range.compareLocationWith(selection):null};
    });
    if(selection){await context.sync();for(const item of items)item.inSelection=['Contains','ContainsStart','ContainsEnd','Inside','InsideStart','InsideEnd','Equal','OverlapsBefore','OverlapsAfter'].includes(item.relation.value);}
    const scoped=selection?items.filter(item=>item.inSelection):items;
    if(scoped.length>500||selection.text?.length>LIMIT)throw new Error('O escopo excede o limite de revisão. Selecione uma seção menor.');
    for(const item of scoped){item.range.load('text');item.result=item.range.getOoxml();}await context.sync();
    const eligible=scoped.filter(item=>item.range.text.trim()&&!complex.test(item.result.value));
    if(!eligible.length)throw new Error('Não há parágrafos de texto simples para alterar. Tabelas, campos, notas, links e imagens são preservados.');
    for(const item of eligible){item.original=item.range.text;item.xml=item.result.value;}
    const snapshot={context,items:eligible,paragraphs:eligible.map(item=>({index:item.index,text:item.original})),skipped:scoped.length-eligible.length,appliedTargets:[]};
    const edits=await requestEdits(snapshot.paragraphs);
    const count=await applyEdits(snapshot,edits);
    return {count,skipped:snapshot.skipped,targets:snapshot.appliedTargets};
  });
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

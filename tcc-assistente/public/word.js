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

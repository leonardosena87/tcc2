import {setWordReady,capture,discardTarget,applyReplacement,insertAtCursor,applySuggestionsInWord,clearSuggestionHighlights} from './word.js';
import {applyEdits} from './suggestions.js';
const $=id=>document.getElementById(id);
let token='',history=[],dataset=null,busy=false,wordReady=false,attachments=[];
function status(message,error=false){$('status').textContent=message;$('status').classList.toggle('error',error);}
function lock(value){busy=value;document.querySelectorAll('button,input,select,textarea').forEach(x=>x.disabled=value||x.dataset.applied==='true');if(!value){$('insert-dataset').disabled=!dataset;$('apply').disabled=$('proposal').hidden;}}
async function api(url,body,retry=true){const r=await fetch(url,{method:body?'POST':'GET',headers:{'X-TCC-Token':token,...(body?{'Content-Type':'application/json'}:{})},body:body?JSON.stringify(body):undefined});if(r.status===401&&retry){const session=await fetch('/api/session');if(session.ok){const data=await session.json();token=data.token;connection(data);return api(url,body,false);}}const data=await r.json();if(!r.ok)throw new Error(data.error??'Falha no serviço local.');return data;}
async function action(fn){if(busy)return;lock(true);try{await fn();}catch(e){status(e.message??'Não foi possível concluir a ação.',true);}finally{lock(false);}}
function connection(data){$('connection-state').textContent=data.configured?'· chave configurada':'· configurar';$('model').value=data.model;if(!data.configured)$('connection').open=true;}
function addMessage(role,text,table){const div=document.createElement('div');div.className=`message ${role}`;const label=document.createElement('strong');label.textContent=role==='user'?'Você':'Assistente';div.append(label,document.createTextNode(text));if(role==='assistant'){const button=document.createElement('button');button.className='secondary';button.textContent='Inserir resposta após a seleção';button.addEventListener('click',()=>action(async()=>{await insertAtCursor(text);status('Texto inserido no Word. Ctrl+Z desfaz a inserção.');}));div.append(button);const word=document.createElement('button');word.className='secondary';word.textContent='Baixar resposta em Word';word.onclick=()=>action(()=>download({format:'docx',text}));div.append(word);if(validTable(table)){const wrapper=document.createElement('div');wrapper.className='table-scroll';const element=document.createElement('table');for(const [index,row] of [table.columns,...table.rows].entries()){const tr=document.createElement('tr');for(const cell of row){const td=document.createElement(index===0?'th':'td');td.textContent=cell;tr.append(td);}element.append(tr);}wrapper.append(element);div.append(wrapper);const excel=document.createElement('button');excel.className='secondary';excel.textContent='Baixar tabela em Excel';excel.onclick=()=>action(()=>download({format:'xlsx',table}));div.append(excel);}} $('conversation').append(div);}
function validTable(table){return table&&Array.isArray(table.columns)&&table.columns.length>0&&table.columns.length<=20&&table.columns.every(x=>typeof x==='string')&&Array.isArray(table.rows)&&table.rows.length<=200&&table.rows.every(r=>Array.isArray(r)&&r.length===table.columns.length&&r.every(x=>typeof x==='string'));}
function addSuggestionAction(suggestions){
  const message=$('conversation').lastElementChild;
  const box=document.createElement('div');box.className='apply-suggestions';
  const label=document.createElement('label');label.textContent='Onde aplicar estas sugestões?';
  const scope=document.createElement('select');scope.setAttribute('aria-label','Onde aplicar estas sugestões');scope.append(new Option('Documento Word aberto','document'),new Option('Parágrafos da seleção atual','selection'));label.append(scope);
  const hint=document.createElement('p');hint.className='hint';hint.textContent='Revisa os parágrafos de texto do Word aberto com estas sugestões. Não altera os anexos. Formatação interna pode mudar; Ctrl+Z desfaz no Word.';
  const button=document.createElement('button');button.className='primary';button.textContent='Aplicar sugestões no Word';
  const done=document.createElement('button');done.className='secondary';done.textContent='Concluído — remover destaques';done.hidden=true;
  const outcome=document.createElement('p');outcome.className='hint';outcome.setAttribute('role','status');
  let appliedTargets=null;
  button.onclick=()=>action(async()=>{
    try{
      status('Lendo e revisando os parágrafos no Word…');outcome.textContent='Lendo o documento…';
      let answer='';
      const result=await applySuggestionsInWord(scope.value,async paragraphs=>{
        outcome.textContent='Enviando os parágrafos para revisão…';
        const response=await api('/api/chat',{mode:'apply',prompt:'Aplique as sugestões acadêmicas pertinentes ao texto, preservando as informações existentes.',suggestions,paragraphs});
        answer=response.answer;return response.edits;
      },applyEdits);
      const count=result.count;appliedTargets=result.targets;
      if(count){button.dataset.applied='true';button.textContent='Sugestões aplicadas';scope.dataset.applied='true';done.hidden=false;}
      outcome.textContent=count?`${count} parágrafo(s) alterado(s) e destacados em amarelo. ${result.skipped?`${result.skipped} parágrafo(s) vazio(s) ou com conteúdo complexo preservado(s). `:''}`:`Nenhum parágrafo alterado. ${answer}`;
      status(outcome.textContent);
    }catch(e){outcome.textContent=e.message;throw e;}
  });
  done.onclick=()=>action(async()=>{const count=await clearSuggestionHighlights(appliedTargets);appliedTargets=null;done.hidden=true;status(`${count} destaque(s) removido(s). As alterações permanecem no documento.`);});
  box.append(label,hint,button,done,outcome);message.insertBefore(box,message.querySelector('button'));
}
async function download(body){const data=await api('/api/download',body);const bytes=Uint8Array.from(atob(data.base64),x=>x.charCodeAt(0));const url=URL.createObjectURL(new Blob([bytes],{type:data.mime}));const link=document.createElement('a');link.href=url;link.download=data.name;document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),60000);status('Arquivo gerado. Confira o download solicitado ao Word/navegador.');}
function renderAttachments(){const list=$('attachment-list');list.replaceChildren();for(const item of attachments){const row=document.createElement('div');row.className='attachment';const label=document.createElement('label');label.className='check';const check=document.createElement('input');check.type='checkbox';check.checked=item.selected;check.onchange=()=>item.selected=check.checked;label.append(check,document.createTextNode(`${item.name} · ${(item.size/1024/1024).toFixed(2)} MB`));const remove=document.createElement('button');remove.className='text-button';remove.textContent='Remover';remove.onclick=()=>{if(busy)return;attachments=attachments.filter(x=>x!==item);renderAttachments();};row.append(label,remove);list.append(row);}}
async function addFiles(files){const incoming=Array.from(files);if(!incoming.length)return;if(attachments.length+incoming.length>5)throw new Error('Anexe no máximo 5 arquivos.');let total=attachments.reduce((n,f)=>n+f.size,0);const names=new Set(attachments.map(f=>f.name));for(const file of incoming){if(!/\.(pdf|docx?|xlsx?)$/i.test(file.name))throw new Error('Use PDF, Word (.doc/.docx) ou Excel (.xls/.xlsx).');if(!file.size||file.size>10*1024*1024)throw new Error(`${file.name}: limite de 10 MB por arquivo.`);if(names.has(file.name))throw new Error(`Já existe um anexo chamado ${file.name}. Remova-o antes de substituir.`);names.add(file.name);total+=file.size;}if(total>20*1024*1024)throw new Error('O total de anexos não pode exceder 20 MB.');const added=[];for(const file of incoming){const base64=await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(String(reader.result).split(',')[1]);reader.onerror=()=>reject(new Error(`Não foi possível ler ${file.name}.`));reader.readAsDataURL(file);});added.push({name:file.name,size:file.size,base64,selected:true});}attachments.push(...added);renderAttachments();status('Arquivos anexados. Escreva seu pedido e clique em Enviar.');}
$('attachments').onchange=()=>action(async()=>{try{await addFiles($('attachments').files);}finally{$('attachments').value='';}});
for(const event of ['dragenter','dragover'])$('dropzone').addEventListener(event,e=>{e.preventDefault();if(!busy)$('dropzone').classList.add('drag-over');});
$('dropzone').addEventListener('dragleave',()=>{$('dropzone').classList.remove('drag-over');});
$('dropzone').addEventListener('drop',e=>{e.preventDefault();$('dropzone').classList.remove('drag-over');if(!busy)action(()=>addFiles(e.dataTransfer.files));});
async function clearProposal(){await discardTarget();$('proposal').hidden=true;$('replacement').value='';$('original').textContent='';}
$('save-settings').onclick=()=>action(async()=>{const data=await api('/api/settings',{apiKey:$('key').value.trim(),model:$('model').value.trim()});$('key').value='';connection(data);if(data.configured)$('connection').open=false;status(data.configured?'Chave configurada nesta sessão. Faça um pedido para testar a conexão com a OpenAI.':'Informe uma chave da API para usar a IA.');});
$('clear-key').onclick=()=>action(async()=>{connection(await api('/api/settings',{clearKey:true,model:$('model').value.trim()}));$('key').value='';status('Chave removida da memória do serviço.');});
document.querySelectorAll('[data-prompt]').forEach(button=>button.onclick=()=>{$('prompt').value=button.dataset.prompt;$('prompt').focus();if(button.textContent==='Revisar escrita')$('mode').value='rewrite';else $('mode').value='chat';});
$('clear-chat').onclick=()=>action(async()=>{history=[];attachments=[];renderAttachments();$('conversation').replaceChildren();await clearProposal();status('Nova conversa iniciada. Histórico e anexos removidos deste painel.');});
$('discard').onclick=()=>action(async()=>{await clearProposal();status('Proposta descartada.');});
$('send').onclick=()=>action(async()=>{
  const prompt=$('prompt').value.trim();if(!prompt)throw new Error('Escreva o que deseja fazer.');
  const mode=$('mode').value;
  if($('include-dataset').checked&&!dataset)throw new Error('Carregue uma exportação Autodesk ou desmarque o envio desses dados.');
  await clearProposal();
  const context=await capture({selection:$('include-selection').checked,document:$('include-document').checked,rewrite:mode==='rewrite'});
  status('Consultando a OpenAI…');
  try {
    const selectedFiles=attachments.filter(f=>f.selected).map(({name,base64})=>({name,base64}));
    const result=await api('/api/chat',{prompt,mode,...context,history,dataset:$('include-dataset').checked?dataset:null,attachments:selectedFiles});
    const promptWithFiles=prompt+(selectedFiles.length?'\n\nAnexos enviados: '+selectedFiles.map(f=>f.name).join(', '):'');
    addMessage('user',promptWithFiles);addMessage('assistant',result.answer,result.table);addSuggestionAction(result.answer);
    history=[...history,{role:'user',content:promptWithFiles},{role:'assistant',content:result.answer.slice(0,20000)}].slice(-12);
    if(mode==='rewrite'&&result.replacement.trim()){$('original').textContent=context.selection;$('replacement').value=result.replacement;$('proposal').hidden=false;}else await discardTarget();
    $('prompt').value='';status(mode==='rewrite'&&!$('proposal').hidden?'Revisão pronta. Confira o texto proposto antes de aplicar.':'Resposta recebida.');
  }catch(e){await discardTarget();throw e;}
});
$('apply').onclick=()=>action(async()=>{await applyReplacement($('replacement').value);$('proposal').hidden=true;status('Trecho substituído no Word. Use Ctrl+Z para desfazer.');});
function datasetSummary(data){const counts={};for(const e of data.elements)counts[e.category]=(counts[e.category]??0)+1;return `${data.application} — ${data.document}\nExportado em: ${new Date(data.exportedAt).toLocaleString('pt-BR')}\nEscopo: somente elementos selecionados (${data.elements.length})\n${Object.entries(counts).map(([k,v])=>`${k}: ${v}`).join('\n')}\n\nUnidades e medições: ${data.units??'consulte cada elemento'}\nNão representa o quantitativo completo do projeto.`;}
async function refreshExports(){const data=await api('/api/exports');$('exports').replaceChildren(new Option('Escolha uma exportação',''));for(const f of data.files)$('exports').append(new Option(`${f.name} · ${new Date(f.modified).toLocaleString('pt-BR')}`,f.name));dataset=null;$('include-dataset').checked=false;$('dataset-preview').textContent='Escolha uma exportação para conferir os dados.';}
$('refresh-exports').onclick=()=>action(refreshExports);
$('exports').onchange=()=>action(async()=>{dataset=null;$('include-dataset').checked=false;if(!$('exports').value){$('dataset-preview').textContent='Nenhuma exportação carregada.';return;}dataset=await api(`/api/export?name=${encodeURIComponent($('exports').value)}`);$('dataset-preview').textContent=datasetSummary(dataset)+'\n\nAmostra dos primeiros 5 elementos:\n'+JSON.stringify(dataset.elements.slice(0,5),null,2);status('Exportação carregada. Marque o envio dos dados se quiser usá-los na conversa.');});
$('insert-dataset').onclick=()=>action(async()=>{if(!dataset)throw new Error('Selecione uma exportação.');await insertAtCursor(datasetSummary(dataset));status('Resumo da seleção Autodesk inserido no Word.');});
async function boot(){try{const r=await fetch('/api/session');if(!r.ok)throw new Error();const data=await r.json();token=data.token;connection(data);status('Serviço local conectado. Abra no Word para ler e editar documentos.');await refreshExports();lock(false);}catch{status('Não foi possível conectar. Execute Iniciar.cmd e reabra o painel.',true);}}
if(window.Office){Office.onReady(info=>{wordReady=info.host===Office.HostType.Word;setWordReady(wordReady);if(wordReady){
  status('Conectado ao Word. Este documento abrirá o painel automaticamente nas próximas vezes.');
  Office.context.document.settings.set('Office.AutoShowTaskpaneWithDocument',true);
  Office.context.document.settings.saveAsync(result=>{if(result.status!==Office.AsyncResultStatus.Succeeded)status('Não foi possível gravar a abertura automática neste documento. Salve-o e tente novamente.',true);});
}});}
boot();

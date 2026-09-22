import { randomBytes, timingSafeEqual } from 'node:crypto';
import { readFile, readdir, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PublicError, buildRequest, parseResponse, validateDataset } from './core.mjs';
import {createDownload} from './downloads.mjs';
const publicDir = fileURLToPath(new URL('../public/', import.meta.url));
const mime = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml','.png':'image/png'};
const staticFiles = new Set(['index.html','app.js','word.js','style.css','files.css','icon-16.png','icon-32.png','icon-80.png']);
export function createHandler({origin = 'https://localhost:3443', exportDir, apiKey = '', model = 'gpt-6-astra', fetchImpl = fetch} = {}) {
  const token = randomBytes(32).toString('hex');
  let busy = false;
  const send = (res,status,data) => { res.writeHead(status,{'Content-Type':'application/json; charset=utf-8'}); res.end(JSON.stringify(data)); };
  async function json(req,limit=1600000) {
    if (!req.headers['content-type']?.startsWith('application/json')) throw new PublicError('Use JSON.',415);
    let size=0; const chunks=[];
    for await (const chunk of req) { size+=chunk.length; if(size>limit) throw new PublicError('Pedido muito grande.',413); chunks.push(chunk); }
    try { return JSON.parse(Buffer.concat(chunks).toString()); } catch {throw new PublicError('JSON inválido.');}
  }
  return async (req,res) => {
    res.setHeader('Cache-Control','no-store'); res.setHeader('X-Content-Type-Options','nosniff');
    res.setHeader('Referrer-Policy','no-referrer');
    try {
      if(req.headers.host !== new URL(origin).host) throw new PublicError('Origem não autorizada.',403);
      const url = new URL(req.url,origin);
      if(url.pathname.startsWith('/api/') && ((req.headers.origin && req.headers.origin !== origin) || req.headers['sec-fetch-site'] === 'cross-site')) throw new PublicError('Origem não autorizada.',403);
      if(url.pathname === '/api/session' && req.method === 'GET') return send(res,200,{token,configured:!!apiKey,model,version:'0.1.0'});
      if(url.pathname.startsWith('/api/')) {
        const provided = Buffer.from(String(req.headers['x-tcc-token'] ?? '')); const expected=Buffer.from(token);
        if(provided.length !== expected.length || !timingSafeEqual(provided,expected)) throw new PublicError('Reabra o painel para conectar ao serviço local.',401);
        if(url.pathname === '/api/settings' && req.method === 'POST') {
          if(busy) throw new PublicError('Aguarde a solicitação atual.',409);
          const body=await json(req);
          if(typeof body.model !== 'string' || !/^[a-zA-Z0-9._:-]{1,100}$/.test(body.model)) throw new PublicError('Informe um modelo válido.');
          if(body.apiKey !== undefined && (typeof body.apiKey !== 'string' || body.apiKey.length>500 || (body.apiKey && !/^sk-[\x21-\x7E]+$/.test(body.apiKey)))) throw new PublicError('Chave da API inválida.');
          if(body.apiKey) apiKey=body.apiKey;
          if(body.clearKey === true) apiKey='';
          model=body.model;
          return send(res,200,{configured:!!apiKey,model});
        }
        if(url.pathname === '/api/exports' && req.method === 'GET') {
          const names = await readdir(exportDir).catch(e => {if(e.code==='ENOENT') return []; throw e;});
          const files = [];
          for(const name of names.filter(n => /^(revit|autocad)-[a-zA-Z0-9-]+\.json$/.test(n))) {
            const info=await stat(path.join(exportDir,name)); if(info.isFile() && info.size <= 1000000) files.push({name,modified:info.mtime.toISOString()});
          }
          return send(res,200,{files:files.sort((a,b)=>b.modified.localeCompare(a.modified)).slice(0,30)});
        }
        if(url.pathname === '/api/export' && req.method === 'GET') {
          const name=url.searchParams.get('name')??'';
          if(!/^(revit|autocad)-[a-zA-Z0-9-]+\.json$/.test(name)) throw new PublicError('Nome de exportação inválido.');
          const filename=path.join(exportDir,name); const info=await stat(filename).catch(()=>{throw new PublicError('Exportação não encontrada.',404);});
          if(info.size>1000000) throw new PublicError('Seleção muito grande. Exporte menos elementos.');
          return send(res,200,validateDataset(JSON.parse(await readFile(filename,'utf8'))));
        }
        if(url.pathname === '/api/download' && req.method === 'POST') {
          const body=await json(req);try{return send(res,200,createDownload(body));}catch(e){throw new PublicError(e.message);}
        }
        if(url.pathname === '/api/chat' && req.method === 'POST') {
          const body=await json(req,30*1024*1024); const request=buildRequest(body,model);
          if(!apiKey) throw new PublicError('Configure sua chave da API OpenAI em Conexão.',503);
          if(busy) throw new PublicError('Já existe um pedido em andamento.',429);
          busy=true;
          try {
            const response=await fetchImpl('https://api.openai.com/v1/responses',{method:'POST',headers:{Authorization:`Bearer ${apiKey}`,'Content-Type':'application/json'},body:JSON.stringify(request),signal:AbortSignal.timeout(120000)});
            if(!response.ok) {
              const messages={400:'A OpenAI não conseguiu processar o pedido ou um anexo. Confira se os arquivos abrem normalmente e não têm senha; tente um arquivo menor ou exportado novamente.',401:'A chave OpenAI não foi aceita. Confira em Conexão.',403:'A conta não tem acesso a esse recurso.',404:'Modelo não encontrado ou indisponível para sua conta.',429:'Limite ou saldo da API atingido. Confira sua conta OpenAI.'};
              throw new PublicError(messages[response.status]??`A OpenAI retornou erro HTTP ${response.status}. Tente novamente.`,502);
            }
            return send(res,200,parseResponse(await response.json()));
          } finally {busy=false;}
        }
        throw new PublicError('Rota não encontrada.',404);
      }
      if(req.method !== 'GET') throw new PublicError('Método não permitido.',405);
      const name=url.pathname === '/' ? 'index.html' : url.pathname.slice(1);
      if(!staticFiles.has(name)) throw new PublicError('Arquivo não encontrado.',404);
      const file=await readFile(path.join(publicDir,name)); res.writeHead(200,{'Content-Type':mime[path.extname(name)]}); res.end(file);
    } catch(e) {
      const message=e instanceof PublicError ? e.message : ['TimeoutError','AbortError'].includes(e.name) ? 'A solicitação demorou demais. Tente um trecho menor.' : 'Falha no serviço local. Verifique a conexão e reinicie se necessário.';
      if(!res.headersSent) send(res,e.status??500,{error:message}); else res.end();
    }
  };
}

import https from 'node:https';
import path from 'node:path';
import os from 'node:os';
import {readFile} from 'node:fs/promises';
import {createHandler} from './app.mjs';
const certDir=path.join(os.homedir(),'.office-addin-dev-certs');
try {
  const options={key:await readFile(path.join(certDir,'localhost.key')),cert:await readFile(path.join(certDir,'localhost.crt'))};
  const exportDir=path.join(process.env.LOCALAPPDATA ?? os.homedir(),'TccAssistente','exports');
  const server=https.createServer(options,createHandler({exportDir,apiKey:process.env.OPENAI_API_KEY??'',model:process.env.OPENAI_MODEL??'gpt-6-astra'}));
  server.requestTimeout=150000;
  server.on('error',e=>{console.error(e.code==='EADDRINUSE'?'A porta 3443 já está em uso. Verifique se o assistente já está aberto.':`Erro ao iniciar: ${e.code}`);process.exitCode=1;});
  server.listen(3443,'127.0.0.1',()=>console.log('TCC Assistente disponível em https://localhost:3443'));
} catch(e) {console.error('Certificado local ausente. Execute npm run certs antes de iniciar.');process.exitCode=1;}

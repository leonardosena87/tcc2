# TCC Assistente — primeira versão, 0.1

**Configuração atual: Sena Imóveis.** O serviço usa a credencial `OPENAI_API_KEY` do projeto Firebase `senaimoveisvca-d8b7e` e o modelo `gpt-5.6-sol`, padrão do suplemento de contratos Sena. A credencial foi armazenada com proteção DPAPI do Windows em `%LOCALAPPDATA%\TccAssistente\credentials\openai.xml`, fora do OneDrive, e só pode ser recuperada pelo mesmo usuário Windows. Iniciar.cmd a carrega na memória do serviço; não é necessário digitar a chave no painel. O uso é cobrado no projeto OpenAI dessa credencial. As instruções continuam específicas para TCC, sem incluir os dados imobiliários.

Para atualizar a credencial após uma rotação, execute `scripts/configure-sena.ps1` com a sessão Firebase autorizada e reinicie o serviço. Remover chave no painel limpa apenas a sessão: para remover a configuração persistente, encerre o serviço e remova o arquivo `openai.xml` indicado acima. Os parágrafos abaixo sobre chave apenas em memória se referem às chaves digitadas manualmente no painel.

Suplemento para Word no Windows, com painel de redação conectado à API OpenAI e conectores locais para **Revit 2027 e AutoCAD 2027**. O código está nesta pasta e pode ser ampliado conforme o seu TCC.

## Aplicar sugestões no documento

Cada resposta da IA agora oferece **Aplicar sugestões no Word**. Escolha **Documento Word aberto** ou **Parágrafos da seleção atual** e clique para gerar e aplicar as revisões. O clique autoriza uma nova chamada à IA e a alteração dos parágrafos correspondentes. O resultado informa quantos parágrafos foram alterados; Ctrl+Z desfaz no Word. A seleção atua nos parágrafos que ela abrange, inclusive quando apenas parte de um parágrafo estiver selecionada.

O sistema confere o texto original e o conteúdo capturado antes de escrever. Se o documento mudar durante a análise, a aplicação é bloqueada. Parágrafos com tabelas, campos, imagens, notas e links são preservados. A formatação interna de parágrafos substituídos pode mudar. O limite é de 500 parágrafos e 120.000 caracteres; para textos maiores, aplique por seção. O botão atua somente no documento Word aberto, não nos arquivos anexados nem na geometria Autodesk. O comando antigo **Inserir resposta após a seleção** continua disponível para inserir os comentários da IA como texto.

## Trabalhar com os anexos

No painel, use **Anexar PDF, Word ou Excel** ou arraste os arquivos para essa área. São aceitos `.pdf`, `.doc`, `.docx`, `.xls` e `.xlsx`: até 5 arquivos, 10 MB por arquivo e 20 MB no total. Os arquivos marcados são enviados à OpenAI junto com cada novo pedido, para manter o contexto durante a conversa. Desmarque para excluir de um pedido; Remover libera o anexo do painel. Nova conversa remove histórico e anexos. Fechar/recarregar o painel também perde os anexos locais.

Exemplos: “Resuma este artigo e destaque o que serve para minha fundamentação”, “Compare os dois documentos”, “Analise os dados e monte uma tabela”, “Proponha uma nova redação para a introdução do arquivo Word”. A resposta pode ser inserida no documento aberto ou baixada em um **novo DOCX**. Quando houver uma tabela estruturada na resposta, ela pode ser baixada em um **novo XLSX**. As células exportadas são texto, inclusive números, para evitar executar fórmulas recebidas da IA. As tabelas têm limite de 200 linhas e 20 colunas.

Os anexos originais não são alterados. Os arquivos baixados contêm a resposta/tabela; não são cópias com toda a formatação, imagens, fórmulas ou abas dos anexos preservadas. A substituição de texto no Word aberto continua usando o trecho selecionado e a prévia de revisão.

PDF é enviado com texto e páginas para a IA. Documentos Word são lidos como texto; imagens e gráficos internos podem não ser considerados. Para Excel, a API analisa até as **primeiras 1.000 linhas por aba**, sem garantia de recálculo das fórmulas. Para gráficos ou layout importantes, envie também uma versão PDF. Arquivos ilegíveis, protegidos por senha ou incompatíveis podem ser recusados. O painel informa essa falha sem afirmar que leu o arquivo.

Selecionar um arquivo só o lê na memória do painel. O envio acontece ao clicar em Enviar. Esta implementação usa `input_file.file_data` na Responses API, não cria uploads persistentes na Files API e não grava os anexos em disco. A política de dados da API continua aplicável. O histórico guarda nomes dos anexos enviados, não seus bytes.

Testes: `npm test` inclui limites, assinaturas dos formatos, envio de anexos e exportação OOXML. `node scripts/smoke-attachments.mjs` faz uma chamada real cobrada com três arquivos sintéticos; não usa seus documentos de TCC.

Verificação realizada: os 22 testes passaram e uma chamada real com PDF, DOCX e XLSX sintéticos identificou os três códigos de teste e a quantidade da planilha corretamente, retornando uma tabela por arquivo. `.doc` e `.xls` são aceitos pela integração conforme a documentação da API, mas não foram exercitados nesse teste real. A exportação foi verificada estruturalmente; o download pelo WebView do Word ainda depende do comportamento da versão instalada.

## Começar

1. Execute **Instalar.cmd** na primeira instalação. Ele instala as dependências, solicita o certificado HTTPS de desenvolvimento da Microsoft, registra o suplemento e abre um documento de teste no Word. Se aparecer a confirmação do certificado “Developer CA for Microsoft Office Add-ins”, confirme no Windows. Não é necessário habilitar macros ou desabilitar proteções do Office.
2. Nas próximas vezes, execute **Iniciar.cmd**. Ele inicia o servidor, atualiza o registro do manifesto e abre o Word com o suplemento carregado. Para abrir também o documento de teste com o painel, use **Abrir-no-Word.cmd**.
3. No documento em que pretende trabalhar, abra **Página Inicial → Suplementos → Mais suplementos / Meus suplementos → TCC Assistente**. Em algumas versões do Word ele aparece na área de suplementos de desenvolvedor. Uma vez adicionado ao documento, use **Página Inicial → TCC Assistente → Abrir assistente**. Se não aparecer na sessão já aberta, salve seu trabalho e reabra o Word.
4. A instalação do projeto Sena já pode carregar a credencial local configurada por `scripts/configure-sena.ps1`. Se preferir uma chave própria, abra **Conexão com a OpenAI**, informe a chave e clique em **Conectar**. O modelo é configurável; o padrão do suplemento é `gpt-5.6-sol`.
5. Selecione um parágrafo, clique em **Revisar escrita** e depois em **Enviar para a IA**. Confira a proposta, edite se necessário e clique em **Substituir trecho**.

O botão Conectar configura a chave; a primeira solicitação é que verifica efetivamente o acesso ao modelo. A chave permanece apenas na memória do processo local e precisa ser informada de novo após encerrar o serviço. Alternativamente, o serviço aceita as variáveis de ambiente `OPENAI_API_KEY` e `OPENAI_MODEL`. Não coloque chaves no código ou em arquivos desta pasta sincronizada pelo OneDrive.

A assinatura do ChatGPT não configura automaticamente a API. Use uma chave de um projeto da plataforma OpenAI com acesso e saldo/limite disponíveis. O uso da API pode gerar cobrança na conta correspondente.

## O que já está implementado

- Conversa em português sobre o TCC, com histórico limitado às últimas 12 mensagens.
- Revisão de clareza, coesão e linguagem acadêmica, identificação de lacunas e apoio a objetivos/metodologia.
- Leitura do trecho selecionado e, opcionalmente, do corpo do documento aberto.
- Prévia editável da substituição. A aplicação usa o trecho capturado, mesmo se o cursor mudar de lugar. Se o trecho for editado enquanto a IA responde, a proposta antiga não é aplicada.
- Inserção da resposta após a seleção atual, sem substituir essa seleção.
- Importação das exportações locais dos conectores Autodesk, resumo por categoria e envio opcional dos dados à IA.
- Orientações à IA para não inventar referências, normas ou medições e marcar informações faltantes. Essas orientações não substituem a conferência humana das fontes.

**Limites de edição:** substituição em texto simples. Seleções com tabelas, imagens, campos, links, notas ou controles de conteúdo são rejeitadas para evitar sua perda. Formatação interna mista pode ser perdida. O comando não formata automaticamente todo o documento segundo ABNT e não cria referências verificadas. Use Ctrl+Z para desfazer alterações aplicadas no Word. O suplemento não salva o documento automaticamente.

**Contexto:** no máximo 120.000 caracteres por trecho/corpo. Textos maiores são recusados explicitamente, sem truncamento silencioso. Cabeçalhos, rodapés, notas e imagens não são extraídos como contexto nesta versão. Nova conversa limpa o histórico no painel. O serviço não grava a conversa em disco.

## Revit 2027

O conector foi compilado para a API instalada em `C:\Program Files\Autodesk\Revit 2027`, com .NET 10.

1. Após a instalação do conector, salve seu trabalho e reabra o Revit quando for conveniente.
2. No modelo, selecione de 1 a 2.000 elementos.
3. Na guia **Suplementos**, painel **TCC Assistente**, clique em **Exportar para o TCC**.
4. No Word, expanda **Dados do Revit e AutoCAD**, clique em **Atualizar exportações** e escolha o arquivo.

São exportados ID, ID único, categoria, nome, tipo, nível e parâmetros disponíveis de comprimento, área e volume. Os valores são convertidos para m, m² e m³. Valores indisponíveis são `null`, não zero. Modelos vinculados não são percorridos. Não se deve somar áreas de paredes, pisos e ambientes como se representassem a mesma grandeza.

## AutoCAD 2027

1. No AutoCAD, use **NETLOAD** e carregue `%LOCALAPPDATA%\TccAssistente\connectors\TccAssistente.AutoCAD.dll` (expanda o caminho no Explorador se o seletor não expandir variáveis).
2. Se o AutoCAD solicitar confirmação para carregar o conector local, confira o nome e confirme na interface. Não desabilite SECURELOAD.
3. Abra um desenho e execute **TCCEXPORTAR**. Se já houver uma seleção, ela será utilizada; caso contrário, o comando solicitará a seleção.
4. Atualize e escolha a exportação no painel do Word.

São exportados identificador/handle, tipo de entidade, camada, texto, nome do bloco e comprimento/área quando aplicáveis. **As medidas permanecem nas unidades do desenho.** O valor INSUNITS é incluído como referência, mas não comprova a escala usada na geometria. Curvas abertas não recebem área; blocos não são explodidos. Limite de 2.000 entidades e 1 MB por exportação.

Os conectores desta primeira versão **leem seleções**. Criação/modificação de geometria, sincronização contínua e comandos da IA sobre os modelos são possibilidades para próximas versões, ainda não implementadas.

## Dados, funcionamento local e privacidade

O servidor escuta somente em `127.0.0.1:3443`, com HTTPS em `https://localhost:3443`. A API local verifica Host, origem e token de sessão. A chave não é enviada ao JavaScript do painel após a configuração, não é exposta em respostas e não é registrada em logs. Ela é usada pelo servidor para chamar `https://api.openai.com/v1/responses` com `store: false`.

Isso não equivale a uma garantia de retenção zero na plataforma: aplicam-se as políticas da conta/API. Ao clicar em Enviar, o pedido, histórico e contextos marcados são enviados à OpenAI. As exportações Autodesk ficam em `%LOCALAPPDATA%\TccAssistente\exports`, fora desta pasta do OneDrive, até serem removidas manualmente. Atualizar a lista não envia esses arquivos à OpenAI.

Use **Parar.cmd** para encerrar o serviço iniciado por Iniciar.cmd. O script verifica se o PID ainda corresponde a este servidor antes de encerrá-lo. O serviço não inicia automaticamente com o Windows.

## Desenvolvimento

Requisitos: Node.js 22+, Word com WordApi 1.3 e acesso a Office.js; .NET 10 SDK e instalações completas do Revit/AutoCAD 2027 para compilar os conectores.

```powershell
npm ci
npm test
npm run validate
./scripts/build-connectors.ps1
./scripts/install-connectors.ps1
```

Os diretórios Autodesk podem ser alterados nos parâmetros `-RevitDir` e `-AutoCADDir` do script de compilação. Outras versões dos produtos exigem recompilação e avaliação de compatibilidade. O manifesto Office usa versão 1.0.0.0, conforme exigência do validador; a versão do produto ainda é 0.1.

Arquivos principais: `public/` contém o painel e integração Word; `server/` contém a API local; `connectors/` contém os conectores .NET; `tests/` contém os testes; `scripts/` contém instalação, início e compilação.

## Verificação desta entrega

- 14 testes automatizados passaram: validação do contexto, contrato Responses API com resposta simulada, erros upstream, proteção da API local, leitura de exportações e comportamento de edição com host Word simulado.
- Manifesto validado pela ferramenta oficial `office-addin-manifest`.
- DLLs de Revit e AutoCAD compiladas contra as APIs 2027 locais e copiadas para `%LOCALAPPDATA%\TccAssistente\connectors`; manifesto Revit instalado no perfil do usuário.
- O SDK local é uma versão preview do .NET 10. A compilação indicou conflitos de referências transitivas Autodesk/Microsoft. A execução nos programas precisa ser confirmada; compilação não prova exportação real.
- Certificado HTTPS instalado e serviço local verificado com validação TLS. Painel aberto em uma nova instância real do Word, com status “Conectado ao Word” e botão “Abrir assistente” na faixa de opções.
- Chamada real à OpenAI confirmada usando a credencial Sena e `gpt-5.6-sol`, com mensagem técnica sem conteúdo do TCC. Os testes de substituição foram realizados com host simulado; ainda não houve substituição real pela IA. Nenhum TCC existente foi alterado nos testes.

## Desinstalar

Execute `npm run unregister` nesta pasta para remover o registro de desenvolvimento do Word. Encerre o servidor com Parar.cmd. Com o Revit fechado, remova somente `%APPDATA%\Autodesk\Revit\Addins\2027\TccAssistente.addin` e os arquivos TccAssistente da pasta local de conectores. O AutoCAD descarrega a DLL ao ser encerrado. Exportações podem ser mantidas ou removidas pelo usuário. O certificado Office de desenvolvimento pode ser compartilhado com outros suplementos; não o remova sem verificar esse uso.

## Documentação de referência

- [OpenAI Responses API — início rápido](https://developers.openai.com/api/docs/quickstart)
- [Word Range — API de leitura e edição](https://learn.microsoft.com/en-us/javascript/api/word/word.range?view=word-js-preview)
- [Revit 2027 e .NET 10](https://help.autodesk.com/cloudhelp/2027/ENU/Revit-WhatsNew/files/GUID-8D7A4715-EAF8-4BD1-BE78-061F900D0BCE.htm)
- [AutoCAD — compatibilidade .NET](https://help.autodesk.com/cloudhelp/2027/ENU/AutoCAD-Customization/files/GUID-A6C680F2-DE2E-418A-A182-E4884073338A.htm)

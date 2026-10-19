# Instalar o TCC Assistente em outro computador

Repositório: [leonardosena87/tcc2](https://github.com/leonardosena87/tcc2). A pasta `tcc-assistente` contém o suplemento do Word, o servidor local, os instaladores e os conectores Autodesk.

O GitHub distribui os arquivos do projeto. Cada computador executa seu próprio serviço local e precisa da instalação abaixo para usar o suplemento no Word.

## Requisitos

- Windows 10 ou 11;
- Node.js 22 ou superior, com npm;
- Microsoft Word 365 ou Word 2019 ou superior.

Revit e AutoCAD são opcionais. Os conectores Autodesk só são usados quando os produtos 2027 estão instalados.

## 1. Baixar o projeto

**Por ZIP, sem precisar instalar Git:**

1. [Baixe o projeto em ZIP](https://github.com/leonardosena87/tcc2/archive/refs/heads/main.zip).
2. Extraia os arquivos para uma pasta onde o projeto ficará instalado. Não execute os comandos dentro do ZIP.
3. Abra a pasta extraída e entre em `tcc-assistente`.

**Por Git:** instale Git e execute no PowerShell:

```powershell
git clone https://github.com/leonardosena87/tcc2.git
cd tcc2\tcc-assistente
```

## 2. Instalar no Word

Na pasta `tcc-assistente`, dê dois cliques em **Instalar.cmd**. Ele instala as dependências, solicita o certificado HTTPS local, registra o suplemento, configura o início do serviço com o Windows e abre o Word com o painel.

Quando o Windows solicitar, confirme o certificado **Developer CA for Microsoft Office Add-ins**. Aguarde a instalação terminar.

Para que novos documentos em branco abram o painel automaticamente:

1. Salve seus documentos e feche todas as janelas do Word.
2. Execute **Configurar-Abertura-Automatica.cmd** na pasta `tcc-assistente`.
3. Abra o Word normalmente e crie um documento em branco.

Essa configuração precisa ser feita uma vez em cada computador. Ela atualiza o modelo `Normal.dotm` e cria uma cópia de segurança em `%LOCALAPPDATA%\TccAssistente\backups`. Para reverter, feche o Word e execute **Desativar-Abertura-Automatica.cmd**.

Em documentos antigos, abra **Página Inicial → TCC Assistente → Abrir assistente** uma vez e salve o documento para guardar a preferência de abertura do painel.

## 3. Configurar a mesma IA do Sena Imóveis

A chave não acompanha o download. A configuração deste computador usa proteção DPAPI e não deve ser copiada para outra máquina.

No novo computador, abra o PowerShell **dentro da pasta `tcc-assistente`** e execute:

```powershell
npm install -g firebase-tools
firebase login
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\configure-sena.ps1
.\Parar.cmd
.\Iniciar.cmd
```

Faça login com a conta Firebase que tem permissão para ler o segredo `OPENAI_API_KEY` do projeto `senaimoveisvca-d8b7e`. O script recupera a credencial localmente e a armazena protegida pelo usuário Windows, em `%LOCALAPPDATA%\TccAssistente\credentials`, fora do repositório. Parar e iniciar o serviço faz com que ele carregue a nova configuração.

No painel do Word, confira **Conexão com a OpenAI · chave configurada**. Esse status confirma o carregamento da credencial; faça um pedido para verificar o acesso à IA. As chamadas usam a API OpenAI da conta configurada e podem gerar cobrança.

Como alternativa, informe uma chave OpenAI própria em **Conexão com a OpenAI** no painel. A chave digitada no painel vale somente enquanto o serviço estiver em execução.

## Usar depois da instalação

Abra o Word normalmente. O serviço inicia quando você entra no Windows e os novos documentos em branco abrem o painel se o passo 2 foi concluído. Para iniciá-lo imediatamente sem sair do Windows, execute **Iniciar.cmd**.

Se o painel mostrar erro de rede, ou se você mover a pasta do projeto, execute **Configurar-Inicio-Automatico.cmd** e clique em **Repetir** no painel do Word. O comando corrige o caminho usado pelo Agendador do Windows e inicia o serviço. Se o botão do suplemento não aparecer na faixa, execute **Abrir-no-Word.cmd**.

O painel aceita PDF, DOC, DOCX, XLS e XLSX. O botão **Aplicar sugestões no Word** aplica as revisões ao documento aberto; as alterações recebem destaque amarelo, removido pelo botão de conclusão.

## Atualizar uma instalação

Salve seus documentos e feche o Word antes de atualizar. Se instalou por Git, execute a partir da pasta do repositório:

```powershell
cd tcc-assistente
.\Parar.cmd
git pull --ff-only
npm ci
.\Configurar-Inicio-Automatico.cmd
.\Iniciar.cmd
```

Se instalou por ZIP, baixe e extraia a nova versão em uma pasta própria e execute **Instalar.cmd** nela. Use os novos scripts a partir dessa pasta. A credencial existente, armazenada fora do projeto, continua no perfil Windows desse computador.

Não copie `node_modules`, certificados privados ou credenciais entre computadores e não coloque esses arquivos no GitHub. Instalar em outra máquina exige recriar o certificado e configurar a credencial naquele Windows.

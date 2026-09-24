# TCC Assistente em outro computador

Este repositório contém todo o código necessário para abrir o suplemento do TCC em outro Windows. Segredos, certificados privados e dependências geradas ficam fora do Git por segurança e são recriados durante a instalação.

## Requisitos

- Windows 10 ou 11;
- Git;
- Node.js 22 ou superior, com npm;
- Microsoft Word 365 ou Word 2019 ou superior.

Revit e AutoCAD são opcionais. Os conectores Autodesk só são usados quando os produtos 2027 estão instalados.

## Instalação inicial

Abra o PowerShell e execute:

```powershell
git clone https://github.com/leonardosena87/tcc2.git
cd tcc2\tcc-assistente
.\Instalar.cmd
```

Durante a instalação, aceite o certificado **Developer CA for Microsoft Office Add-ins** quando o Windows perguntar. O instalador instala as dependências, gera o certificado local, registra o suplemento no Word e inicia o servidor local.

Se quiser que documentos em branco novos também abram o painel automaticamente, salve e feche todas as janelas do Word e execute `Configurar-Abertura-Automatica.cmd` uma vez. Ele atualiza `Normal.dotm` com a configuração e guarda o modelo anterior em `%LOCALAPPDATA%\TccAssistente\backups`. Para desfazer, feche o Word e execute `Desativar-Abertura-Automatica.cmd`. Essa configuração é local e precisa ser feita em cada computador.

Depois, abra o Word pelo script:

```powershell
.\Abrir-no-Word.cmd
```

O instalador configura o servidor local para iniciar automaticamente quando você entrar no Windows. Para iniciar imediatamente após a instalação, use `.\Iniciar.cmd`.

Se não configurar `Normal.dotm`, abra o TCC Assistente uma primeira vez em cada documento pelo grupo **TCC Assistente** na faixa **Página Inicial**. O Word salva essa preferência dentro do arquivo e abre o painel automaticamente quando aquele documento for aberto novamente. Documentos existentes sem essa preferência precisam ser ativados uma vez.

Se o painel não aparecer, feche o Word completamente, execute `.\Iniciar.cmd` e abra novamente um documento em branco.

Se o Word for aberto pelo ícone normal, entre em **Página Inicial → Suplementos → Meus suplementos**, selecione **TCC Assistente** e clique em **Adicionar**. O carregamento automático ocorre no documento aberto pelos scripts do projeto.

## Configurar a IA do Sena Imóveis

As credenciais não são versionadas. Para usar a mesma IA do projeto Sena, faça login na conta Firebase que tem acesso ao projeto e execute:

```powershell
firebase login
cd tcc-assistente
.\scripts\configure-sena.ps1
```

O script recupera o segredo de forma local e o protege com o armazenamento de credenciais do Windows. Alternativamente, é possível informar uma chave OpenAI própria pelo painel de Configuração.

## Atualizar depois

Para trazer a versão mais recente para esse computador:

```powershell
cd tcc2
git pull
cd tcc-assistente
npm ci
.\Iniciar.cmd
```

Não copie `node_modules`, certificados ou arquivos de credenciais entre computadores. Eles são específicos de cada instalação.

## Arquivos aceitos

O painel permite anexar PDF, DOC, DOCX, XLS e XLSX. As sugestões podem ser revisadas e aplicadas diretamente no documento Word aberto pelo botão **Aplicar sugestões no Word**.

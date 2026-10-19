# TCC2

Materiais do TCC e desenvolvimento do suplemento **TCC Assistente** para Word, com integração à API OpenAI e conectores para Revit e AutoCAD 2027.

## Organização

- `tcc-assistente/`: código do suplemento, conectores, testes e scripts de instalação.
- Arquivos PDF, apresentação e roteiro na raiz: materiais de trabalho do TCC.

## Usar o suplemento

Consulte [as instruções do TCC Assistente](tcc-assistente/LEIA-ME.md). No Windows, execute `tcc-assistente/Instalar.cmd` para instalar ou `tcc-assistente/Iniciar.cmd` para iniciar uma instalação existente.

O suplemento roda localmente; versionar no GitHub não publica nem hospeda o serviço. A configuração OpenAI precisa ser fornecida separadamente. Chaves, certificados privados, arquivos temporários e dependências instaladas não fazem parte do repositório.

### Instalar em outro computador

O suplemento completo está na pasta [`tcc-assistente`](tcc-assistente). Você pode [baixar o projeto em ZIP](https://github.com/leonardosena87/tcc2/archive/refs/heads/main.zip), extrair os arquivos e executar `tcc-assistente/Instalar.cmd`. O novo computador precisa de Windows, Node.js 22 ou superior e Microsoft Word 365/2019 ou superior.

Se preferir usar Git, execute no PowerShell:

```powershell
git clone https://github.com/leonardosena87/tcc2.git
cd tcc2\tcc-assistente
.\Instalar.cmd
```

Confirme o certificado local quando o Windows solicitar. Para abrir o painel automaticamente em documentos em branco novos, salve e feche o Word e execute `tcc-assistente/Configurar-Abertura-Automatica.cmd` uma vez. O instalador já configura o início do serviço com o Windows; `Configurar-Inicio-Automatico.cmd` repara essa configuração se a pasta mudar de lugar.

A chave da IA precisa ser configurada no novo computador. Para usar a mesma IA do Sena Imóveis, siga [o guia de instalação e configuração da IA](INSTALAR-EM-OUTRO-COMPUTADOR.md). Chaves, certificados privados e dependências não são enviados ao GitHub.

## Desenvolvimento

```powershell
cd tcc-assistente
npm ci
npm test
```

Os conectores Autodesk exigem os produtos 2027 e o SDK .NET 10 para recompilação. Os caminhos podem ser configurados no script de build.

Repositório: https://github.com/leonardosena87/tcc2

O arquivo local `TCC 2 - Leonardo, Danyela e Arthur.pdf` estava vazio na importação inicial e foi excluído do versionamento até ser substituído por um PDF válido. Remova sua entrada específica do `.gitignore` quando houver conteúdo para versionar.

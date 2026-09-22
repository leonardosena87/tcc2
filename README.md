# TCC2

Materiais do TCC e desenvolvimento do suplemento **TCC Assistente** para Word, com integração à API OpenAI e conectores para Revit e AutoCAD 2027.

## Organização

- `tcc-assistente/`: código do suplemento, conectores, testes e scripts de instalação.
- Arquivos PDF, apresentação e roteiro na raiz: materiais de trabalho do TCC.

## Usar o suplemento

Consulte [as instruções do TCC Assistente](tcc-assistente/LEIA-ME.md). No Windows, execute `tcc-assistente/Instalar.cmd` para instalar ou `tcc-assistente/Iniciar.cmd` para iniciar uma instalação existente.

O suplemento roda localmente; versionar no GitHub não publica nem hospeda o serviço. A configuração OpenAI precisa ser fornecida separadamente. Chaves, certificados privados, arquivos temporários e dependências instaladas não fazem parte do repositório.

## Desenvolvimento

```powershell
cd tcc-assistente
npm ci
npm test
```

Os conectores Autodesk exigem os produtos 2027 e o SDK .NET 10 para recompilação. Os caminhos podem ser configurados no script de build.

Repositório: https://github.com/leonardosena87/tcc2

O arquivo local `TCC 2 - Leonardo, Danyela e Arthur.pdf` estava vazio na importação inicial e foi excluído do versionamento até ser substituído por um PDF válido. Remova sua entrada específica do `.gitignore` quando houver conteúdo para versionar.

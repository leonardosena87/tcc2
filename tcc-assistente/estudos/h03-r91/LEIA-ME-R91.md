# H03/R91 — preparação da auditoria de materiais do autor

Preparou-se um comando externo independente de leitura de propriedades para o Revit 2027. A lacuna R87 permanece aberta: o novo comando foi compilado, mas ainda não foi executado no modelo do estudo. Nenhum valor de material novo foi observado ou presumido.

## O que está pronto

- Código `connectors/RevitAudit`, sem modificar os conectores existentes.
- Compilação contra os DLLs da instalação Revit 2027: zero avisos e zero erros após incluir a referência de desktop exigida pelas dependências do host.
- Identificação de material estrutural de famílias e camada estrutural de pisos, mantendo materiais geométricos separados.
- Leitura de ativo físico e conversões explícitas, com dados ausentes nulos. IDs de 64 bits são gravados como texto.
- Associador por UniqueId e ID, com cinco testes simulados sobre ausência, identidade, atribuição e precisão numérica.
- Conjunto Node do ambiente atual: 78 testes aprovados. Os sete testes geométricos R88 continuam sendo um conjunto separado.

## Próxima operação nativa

Na próxima abertura do Revit, permitir o carregamento do comando local somente após conferir o aviso de confiança, se apresentado. Abrir uma cópia do RVT do estudo e executar **Complementos → Ferramentas externas → TCC - auditar materiais**. Essa etapa foi pulada durante a ausência do usuário; não se lançou o Revit para responder a avisos de segurança.

O pacote local está em `D:/TCC/ferramentas/RevitAudit-R91`. O registro usa manifesto próprio e não substitui TCC Assistente ou TCC Demonstração IA. O comprovante local identifica o manifesto, DLL, documentação de API e fonte compilada.

O comando exporta para `D:/TCC/outputs/Propriedades-Revit-*`. Associar o JSON ao mapa de criação R83 com `resumir-materiais.mjs`. Conferir se o documento já estava salvo e se os 62 IDs esperados foram associados. Um piso extra de arquitetura não deve entrar automaticamente no denominador dos 62 elementos do estudo.

Para a transferência final, registrar essa leitura no autor imediatamente antes da exportação e preservar o par de arquivos. Uma leitura atual não prova retroativamente quais propriedades existiam na importação histórica R45/R46.

## Limites

O auditor não atribui material, não inicia transações, não salva o RVT, não muda normas, não verifica aço CA-50, cobrimentos, cargas, conexões analíticas ou ELU/ELS. Compressão e módulo do ativo não são automaticamente fck/Eci/Ecs da norma brasileira. A procedência de uma propriedade no Revit não prova sua retenção no receptor: ainda é necessário inspecionar o arquivo exportado e a recepção do Eberick.

Não há resultado real de propriedades na R91. O tempo da futura leitura será instrumentação específica, separado do tempo total dos fluxos. O texto acadêmico permanece preservado e nenhum item P08 foi encerrado por causa da compilação.

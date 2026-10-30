# Botão Demonstração IA no Revit 2027

Complemento separado do conector TCC Assistente existente. Na guia **Complementos**, cria o painel **IA • Palestra TCC**, com o botão **Demonstração IA**.

A janela recebe um pedido em português e oferece dois caminhos:

- **Gerar prévia com IA** envia somente o texto do pedido para o serviço local HTTPS do TCC Assistente, que consulta a OpenAI. O serviço retorna parâmetros em um contrato JSON restrito. O botão não executa código produzido pelo modelo. A API utiliza a chave e o modelo já configurados no assistente e pode gerar cobrança na conta da API.
- **Exemplo ensaiado** carrega as dimensões locais conhecidas. A janela e o registro identificam explicitamente que não ocorreu uma nova consulta à IA. Esse caminho não depende da rede.

Depois de conferir a prévia, **Criar no Revit** cria uma nova cópia da base reservada, gera a geometria, abre uma vista 3D sombreada e salva o RVT. Editar o pedido invalida a prévia anterior. Um pedido incompleto ou fora do escopo não habilita a criação.

## Escopo da demonstração

Um pórtico retangular de um pavimento, quatro pilares nos cantos, quatro vigas de borda e uma laje maciça retangular. São nove elementos. O pedido precisa informar os dois vãos entre eixos, a altura/cotas, as seções dos pilares e vigas e a espessura da laje.

As dimensões e os limites numéricos são entradas didáticas e limites operacionais do protótipo. O complemento não dimensiona elementos, aplica cargas ou armaduras, produz modelo analítico ou atesta conformidade integral com a NBR 6118. As propriedades de materiais são herdadas da base.

## Compilação e instalação

Requisitos: Revit 2027, SDK .NET 10 com suporte Windows Desktop e famílias da base do estudo. As DLLs Autodesk são referências locais e não são distribuídas neste repositório.

```powershell
dotnet build .\TccAssistente.RevitDemo.csproj -c Release
# Com todos os documentos salvos e o Revit fechado:
.\Instalar.ps1
```

O instalador usa como origem padrão `D:\TCC\palestra-IA-engenharia\demonstracao\DEMO-AO-VIVO-BASE-VAZIA.rvt`, copia uma base própria para `%LOCALAPPDATA%\TccAssistente\revit-demo`, confere seu SHA-256 a cada execução e instala `TccAssistente.Demo.addin` no diretório de suplementos do usuário. O complemento anterior não é substituído. Configurações e backup são locais.

Na abertura do Revit, uma decisão de confiança de suplemento pode ser necessária. Essa escolha deve ser feita pelo usuário. O botão não modifica a política de segurança do Revit.

## Uso na palestra

1. Abrir o Revit e clicar em **Complementos > IA • Palestra TCC > Demonstração IA**.
2. Colar o pedido ou usar o texto inicial.
3. Clicar em **Gerar prévia com IA** e aguardar a interpretação, ou escolher **Exemplo ensaiado**.
4. Conferir as dimensões e o modo indicado na janela.
5. Clicar em **Criar no Revit** e apresentar o modelo 3D.

O projeto aberto anteriormente permanece aberto e não recebe os elementos. Cada execução ganha uma pasta nova em `D:\TCC\palestra-IA-engenharia\demonstracao\execucoes`. Nenhum arquivo de resultado existente é substituído.

## Registros e tempos

Cada execução salva `pedido-e-previa.json`, `resultado.json` e `DEMO-IA-RESULTADO.rvt`. Uma execução parcial pode produzir `falha.json`, sem declaração de sucesso. O registro diferencia o tempo da janela, o tempo geométrico da API, o salvamento e o comando completo. O tempo de interpretação e o uso de tokens constam da resposta real da API quando disponíveis. Não se estima custo sem informação de preço. Os intervalos são identificados pelo escopo e não devem ser somados novamente quando já incluídos no total do comando.

Esses tempos da palestra não substituem os ensaios pareados completos CAD/BIM do TCC. O antigo valor de 0,53 s pertence ao ensaio pelo importador anterior, não ao novo botão.

## Segunda demonstração: variação geométrica

O mesmo botão foi ensaiado com uma alternativa de 8 × 3 m, mantendo os 24 m² do exemplo de 6 × 4 m. Os dois caminhos usaram consulta real à IA e criaram arquivos independentes; uma exportação posterior conferiu os nove elementos físicos, a área da laje e os comprimentos das vigas. O [roteiro e os pedidos completos](../../estudos/palestra-ia-engenharia-20min/demonstracao-2/ROTEIRO.md) registram os ensaios e seus tempos. Não há edição do modelo anterior nem avaliação de equivalência estrutural.

## Serviço de IA

A rota `POST /api/revit-demo/plan` usa as mesmas verificações de host, origem, sessão e concorrência do serviço existente em `https://localhost:3443`. Nenhuma chave fica no Revit, nos arquivos RVT ou nos registros de execução. O cliente valida normalmente o certificado HTTPS. Se o certificado local vencer, deve-se renová-lo pelo instalador oficial já utilizado pelo TCC Assistente. Não se deve desabilitar a verificação TLS.

O modo ensaiado permanece disponível se o serviço, a credencial, a conexão ou o modelo estiverem indisponíveis. Uma prévia gerada por IA exige revisão antes da criação, mesmo quando seu formato é válido.

## Verificação de código

```powershell
# Na pasta tcc-assistente:
node --test tests/*.test.mjs
dotnet run --project tests/RevitDemoPlan/RevitDemoPlan.csproj -c Release
```

Os testes HTTP usam respostas simuladas. O teste C# valida o plano e não carrega o Revit. Compilação, instalação, chamada real à IA e criação no aplicativo são verificações separadas e devem ser registradas separadamente.

Referências de implementação: [Structured Outputs na Responses API](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses), [abertura de documento pela API Revit](https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API-MainReference/files/html/3b3d671d-47ec-2ed8-1818-a7c19d01884b.htm). A compilação utiliza as bibliotecas locais da versão 2027 instalada.

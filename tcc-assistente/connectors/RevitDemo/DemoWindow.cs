using System.Diagnostics;
using System.IO;
using System.Net.Http;
using System.Net.Http.Json;
using System.Text.Json;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace TccAssistente.RevitDemo;

public sealed class DemoWindow:Window
{
    readonly TextBox prompt=new(){Text=DemoPlan.PromptExample,AcceptsReturn=true,TextWrapping=TextWrapping.Wrap,VerticalScrollBarVisibility=ScrollBarVisibility.Auto,Height=138,FontSize=16,Padding=new Thickness(10),MaxLength=6000};
    readonly TextBox preview=new(){IsReadOnly=true,TextWrapping=TextWrapping.Wrap,VerticalScrollBarVisibility=ScrollBarVisibility.Auto,Height=216,FontSize=16,Padding=new Thickness(10)};
    readonly TextBlock status=new(){Text="Escreva o pedido e gere a prévia, ou carregue o exemplo ensaiado.",TextWrapping=TextWrapping.Wrap,Margin=new Thickness(0,10,0,10)};
    readonly Button generate=new(){Content="Gerar prévia com IA",MinWidth=190,Height=38};
    readonly Button example=new(){Content="Exemplo ensaiado",MinWidth=175,Height=38,Margin=new Thickness(12,0,0,0)};
    readonly Button create=new(){Content="Criar no Revit",MinWidth=190,Height=42,IsEnabled=false};
    readonly CancellationTokenSource cancel=new();
    bool busy,closed;
    string? approvedPrompt;
    public DemoPlan? Plan{get;private set;}
    public string Mode{get;private set;}="";
    public string SubmittedPrompt{get;private set;}="";
    public string? AiTraceJson{get;private set;}
    public double DialogSeconds{get;private set;}
    readonly Stopwatch timer=Stopwatch.StartNew();
    public DemoWindow()
    {
        Title="Demonstração IA • TCC Assistente";Width=810;Height=780;MinWidth=720;MinHeight=700;ResizeMode=ResizeMode.CanResize;WindowStartupLocation=WindowStartupLocation.CenterOwner;FontFamily=new FontFamily("Segoe UI");FontSize=14;Background=new SolidColorBrush(Color.FromRgb(246,248,250));
        var stack=new StackPanel{Margin=new Thickness(26)};
        stack.Children.Add(new TextBlock{Text="Um pedido. Uma prévia. Um modelo 3D.",FontSize=25,FontWeight=FontWeights.SemiBold,Margin=new Thickness(0,0,0,10)});
        stack.Children.Add(new TextBlock{Text="Exemplo didático: quatro pilares, quatro vigas e uma laje. A criação usa uma nova cópia da base e preserva o documento atual.",TextWrapping=TextWrapping.Wrap,Margin=new Thickness(0,0,0,14)});
        stack.Children.Add(prompt);
        var buttons=new StackPanel{Orientation=Orientation.Horizontal,Margin=new Thickness(0,12,0,4)};buttons.Children.Add(generate);buttons.Children.Add(example);stack.Children.Add(buttons);
        stack.Children.Add(new TextBlock{Text="Gerar com IA envia apenas este texto à OpenAI pelo serviço local TCC Assistente e utiliza a API configurada. Exemplo ensaiado funciona sem consulta à IA.",FontSize=12,TextWrapping=TextWrapping.Wrap,Margin=new Thickness(0,6,0,0)});
        stack.Children.Add(status);stack.Children.Add(preview);
        var bottom=new StackPanel{Orientation=Orientation.Horizontal,Margin=new Thickness(0,15,0,0)};bottom.Children.Add(create);var close=new Button{Content="Fechar",MinWidth=120,Height=42,Margin=new Thickness(12,0,0,0),IsCancel=true};bottom.Children.Add(close);stack.Children.Add(bottom);
        Content=new ScrollViewer{Content=stack,VerticalScrollBarVisibility=ScrollBarVisibility.Auto};
        prompt.TextChanged+=(_,_)=>Invalidate();
        example.Click+=(_,_)=>{prompt.Text=DemoPlan.PromptExample;Accept(DemoPlan.Example(),"local_prepared",null);status.Text="Modo: exemplo ensaiado. Sem nova consulta à IA.";};
        generate.Click+=async(_,_)=>await Generate();
        create.Click+=(_,_)=>{if(busy||Plan?.Status!="ready"||prompt.Text!=approvedPrompt)return;Plan.RequireReady();SubmittedPrompt=approvedPrompt;DialogSeconds=timer.Elapsed.TotalSeconds;DialogResult=true;};
        Closed+=(_,_)=>{closed=true;cancel.Cancel();};
    }
    void Invalidate(){Plan=null;approvedPrompt=null;AiTraceJson=null;create.IsEnabled=false;preview.Clear();status.Text="Pedido alterado. Gere uma nova prévia antes de criar.";}
    void Accept(DemoPlan plan,string mode,string? trace){plan.Validate();Plan=plan;Mode=mode;AiTraceJson=trace;approvedPrompt=prompt.Text;preview.Text=plan.Preview();create.IsEnabled=plan.Status=="ready";}
    async Task Generate()
    {
        if(busy)return;Invalidate();var input=prompt.Text;if(string.IsNullOrWhiteSpace(input)){status.Text="Escreva o pedido.";return;}
        busy=true;generate.IsEnabled=false;example.IsEnabled=false;prompt.IsReadOnly=true;status.Text="A IA está interpretando o pedido. Nenhum elemento foi criado.";
        try
        {
            using var client=new HttpClient{BaseAddress=new Uri("https://localhost:3443"),Timeout=TimeSpan.FromSeconds(100)};
            using var session=await client.GetAsync("/api/session",cancel.Token);session.EnsureSuccessStatusCode();
            using var sj=JsonDocument.Parse(await session.Content.ReadAsStringAsync(cancel.Token));
            if(!sj.RootElement.GetProperty("configured").GetBoolean())throw new InvalidOperationException("Configure a API no TCC Assistente. O exemplo ensaiado continua disponível.");
            client.DefaultRequestHeaders.Add("x-tcc-token",sj.RootElement.GetProperty("token").GetString());
            using var response=await client.PostAsJsonAsync("/api/revit-demo/plan",new{prompt=input},cancel.Token);
            var raw=await response.Content.ReadAsStringAsync(cancel.Token);if(raw.Length>64000)throw new InvalidDataException("Resposta acima do limite.");
            using var json=JsonDocument.Parse(raw);
            if(!response.IsSuccessStatusCode)throw new InvalidOperationException(json.RootElement.TryGetProperty("error",out var error)?error.GetString():"Serviço indisponível.");
            var plan=DemoPlan.Parse(json.RootElement.GetProperty("plan").GetRawText());if(closed)return;
            Accept(plan,"openai",raw);status.Text=plan.Status=="ready"?"Modo: consulta real à IA. Confira as dimensões e clique em Criar no Revit.":"A prévia precisa de esclarecimento. Nenhum elemento será criado.";
        }
        catch(Exception e){if(!closed)status.Text=e is HttpRequestException?"Não foi possível conectar ao serviço local. Inicie o TCC Assistente ou use Exemplo ensaiado.":e is OperationCanceledException?"Solicitação cancelada ou tempo esgotado. Use o exemplo ensaiado se necessário.":e.Message;}
        finally{busy=false;if(!closed){generate.IsEnabled=true;example.IsEnabled=true;prompt.IsReadOnly=false;}}
    }
}

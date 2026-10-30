using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;
using System.Text.Json;
using System.Windows.Interop;

namespace TccAssistente.RevitDemo;

public class App:IExternalApplication
{
    public Result OnStartup(UIControlledApplication app)
    {
        var panel=app.CreateRibbonPanel("IA • Palestra TCC");
        var button=(PushButton)panel.AddItem(new PushButtonData("TccLectureDemo","Demonstração\nIA",typeof(App).Assembly.Location,typeof(Command).FullName!){AvailabilityClassName=typeof(Available).FullName});
        button.ToolTip="Escreva um pedido, confira a prévia e crie um pórtico didático em uma cópia separada.";
        button.LongDescription="Demonstração geométrica com quatro pilares, quatro vigas e uma laje. Consulta real à IA ou exemplo ensaiado, identificados na janela. Preserva o documento atual. Não dimensiona a estrutura.";
        return Result.Succeeded;
    }
    public Result OnShutdown(UIControlledApplication app)=>Result.Succeeded;
}
public class Available:IExternalCommandAvailability{public bool IsCommandAvailable(UIApplication app,CategorySet categories)=>true;}
public sealed record DemoConfig(string BasePath,string BaseSha256,string OutputRoot);

[Transaction(TransactionMode.Manual)]
public class Command:IExternalCommand
{
    public Result Execute(ExternalCommandData data,ref string message,ElementSet failed)
    {
        var started=DateTimeOffset.UtcNow;var total=Stopwatch.StartNew();string? folder=null;
        try
        {
            var window=new DemoWindow();var owner=new WindowInteropHelper(window){Owner=data.Application.MainWindowHandle};
            if(window.ShowDialog()!=true)return Result.Cancelled;
            var plan=window.Plan??throw new InvalidOperationException("Prévia ausente.");plan.RequireReady();
            var configPath=System.IO.Path.Combine(System.IO.Path.GetDirectoryName(typeof(Command).Assembly.Location)!,"demo.config.json");
            var config=JsonSerializer.Deserialize<DemoConfig>(File.ReadAllText(configPath),DemoPlan.JsonOptions)??throw new InvalidDataException("Configuração ausente.");
            var basePath=System.IO.Path.GetFullPath(config.BasePath);var output=System.IO.Path.GetFullPath(config.OutputRoot);
            if(!File.Exists(basePath)||!Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(basePath))).Equals(config.BaseSha256,StringComparison.OrdinalIgnoreCase))throw new InvalidDataException("A base de demonstração mudou ou não está disponível. Reinstale a base preparada.");
            var runId=Guid.NewGuid().ToString();folder=System.IO.Path.Combine(output,"execucoes",DateTime.Now.ToString("yyyyMMdd-HHmmss")+"-"+runId[..8]);Directory.CreateDirectory(folder);
            var resultPath=System.IO.Path.Combine(folder,"DEMO-IA-RESULTADO.rvt");File.Copy(basePath,resultPath,false);
            File.WriteAllText(System.IO.Path.Combine(folder,"pedido-e-previa.json"),JsonSerializer.Serialize(new{runId,mode=window.Mode,prompt=window.SubmittedPrompt,plan,startedAtUtc=started,ai=window.AiTraceJson is null?(JsonElement?)null:JsonSerializer.Deserialize<JsonElement>(window.AiTraceJson)},new JsonSerializerOptions(DemoPlan.JsonOptions){WriteIndented=true}));
            var ui=data.Application.OpenAndActivateDocument(resultPath);
            var result=DemoGeometry.Create(ui,plan,runId);
            ui.ActiveView=result.View;
            ui.GetOpenUIViews().FirstOrDefault(v=>v.ViewId==result.View.Id)?.ZoomToFit();
            var save=Stopwatch.StartNew();ui.Document.Save();save.Stop();total.Stop();
            File.WriteAllText(System.IO.Path.Combine(folder,"resultado.json"),JsonSerializer.Serialize(new{runId,status="created_saved",mode=window.Mode,software="Revit",version=data.Application.Application.VersionNumber,build=data.Application.Application.VersionBuild,createdAtUtc=DateTimeOffset.UtcNow,rvtPath=resultPath,counts=new{columns=4,beams=4,slabs=1,total=9},apiGeometrySeconds=result.Seconds,dialogSeconds=window.DialogSeconds,saveSeconds=save.Elapsed.TotalSeconds,commandTotalSeconds=total.Elapsed.TotalSeconds,timeScope="Comando inclui janela, consulta/revisao, abertura de copia, geometria, vista e salvamento; nao e tempo total do fluxo TCC",elements=result.Elements,normativeApproval=false},new JsonSerializerOptions(DemoPlan.JsonOptions){WriteIndented=true}));
            TaskDialog.Show("Demonstração concluída",$"9 elementos criados e salvos em uma nova cópia.\nModo: {(window.Mode=="openai"?"consulta real à IA":"exemplo ensaiado, sem chamada à IA")}\nEscrita geométrica pela API: {result.Seconds:F2} s\nComando completo: {total.Elapsed.TotalSeconds:F2} s\n\n{resultPath}\n\nGeometria didática. Sem dimensionamento estrutural.");
            return Result.Succeeded;
        }
        catch(Exception e)
        {
            if(folder is not null)try{File.WriteAllText(System.IO.Path.Combine(folder,"falha.json"),JsonSerializer.Serialize(new{status="failed_or_partial",atUtc=DateTimeOffset.UtcNow,message=e.Message,note="Confira a copia da demonstracao; nao ha atestado de conclusao ou salvamento."}));}catch{}
            message=e.Message;TaskDialog.Show("Demonstração não concluída",e.Message+"\nO documento original não foi usado como destino. Se uma cópia abriu, confira seu estado antes de repetir.");return Result.Failed;
        }
    }
}

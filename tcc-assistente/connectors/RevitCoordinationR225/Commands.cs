using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;
using Autodesk.Revit.UI;
using System.Diagnostics;
using System.Text.Json;
using S = TccAssistente.RevitStairSupport.Study;

namespace TccAssistente.RevitCoordinationR225;

public static class Revision
{
    public const string Out = @"D:\TCC\outputs\H03-R225-AUTORIA-COORDENACAO-NAO-EXECUTAR";
    public static JsonElement Read(string file) => JsonDocument.Parse(File.ReadAllText(Path.Combine(Out,file))).RootElement;
    public static void Write(string file, object value) => File.WriteAllText(Path.Combine(Out,file),JsonSerializer.Serialize(value,S.Json));
    public static void Guard(Document doc)
    {
        var cfg=Read("R225-config.json");
        if(doc.IsFamilyDocument || !string.Equals(Path.GetFullPath(doc.PathName),cfg.GetProperty("CopyPath").GetString(),StringComparison.OrdinalIgnoreCase))
            throw new InvalidOperationException("Abrir somente a copia Revit R225 preparada.");
        if(!string.Equals(S.Hash(cfg.GetProperty("CandidatePath").GetString()!),cfg.GetProperty("CandidateSha256").GetString(),StringComparison.OrdinalIgnoreCase))
            throw new InvalidOperationException("O candidato R225 mudou.");
    }
    public static object Readback(Document doc, JsonElement plan) => new {
        Elements=S.ReadElements(doc,S.Entries(plan)), Stair=S.ReadStair(doc),
        Count=66, StructuralApproval=false, NativeEberickOrReinforcementUpdated=false,
        LowerStairInterfaceResolved=false, FullAuthoringAnalyticalEquivalenceVerified=false
    };
}

[Transaction(TransactionMode.Manual)]
public class ApplyRevision : IExternalCommand
{
    public Result Execute(ExternalCommandData data,ref string message,ElementSet elements)
    {
        var timer=Stopwatch.StartNew(); var started=DateTimeOffset.UtcNow;
        bool assimilated=false,saved=false;var failures=new TccAssistente.RevitStairSupport.Failures();
        try
        {
            var ui=data.Application.ActiveUIDocument ?? throw new InvalidOperationException("Abrir a copia R225.");
            var doc=ui.Document; Revision.Guard(doc);var cfg=Revision.Read("R225-config.json");
            if(doc.IsModified || !string.Equals(S.Hash(doc.PathName),cfg.GetProperty("CopySha256Before").GetString(),StringComparison.OrdinalIgnoreCase))
                throw new InvalidOperationException("Copia R225 alterada ou com edicoes nao salvas.");
            var old=JsonDocument.Parse(File.ReadAllText(@"D:\TCC\outputs\Escada-H03-R160-SOMENTE-VIGA-NAO-EXECUTAR\R160-candidato-comum.json")).RootElement;
            // Confere as 63 identidades geometricas e o C25 antes de editar.
            S.ReadElements(doc,S.Entries(old)); var stairBefore=JsonSerializer.Serialize(S.ReadStair(doc),S.Json);
            var plan=Revision.Read("R225-candidato-comum.json"); var map=S.Elements(doc);
            if(S.Entries(plan).Length!=66 || plan.GetProperty("changedExistingElements").GetArrayLength()!=4 || plan.GetProperty("addedElements").GetArrayLength()!=3)
                throw new InvalidOperationException("Contagens do candidato divergentes.");
            var retained=plan.GetProperty("retainedExistingElements").EnumerateArray().ToArray();
            var before=S.LogicalHash(doc,retained);var created=new List<long>();object? readback=null;View3D? view=null;
            using(var group=new TransactionGroup(doc,"TCC R225 - retorno geometrico da hipotese Eberick"))
            {
                group.Start();
                using(var tx=new Transaction(doc,"P11, P12, secoes N1 e viga inferior da escada"))
                {
                    tx.Start();var options=tx.GetFailureHandlingOptions();options.SetFailuresPreprocessor(failures);tx.SetFailureHandlingOptions(options);
                    var symbols=new Dictionary<string,FamilySymbol>();
                    FamilySymbol Symbol(FamilySymbol source,JsonElement e)
                    {
                        var b=S.N(e,"b");var h=S.N(e,"h");var key=$"{source.Id.Value}-{b:R}-{h:R}";
                        if(symbols.TryGetValue(key,out var existing))return existing;
                        var s=(FamilySymbol)source.Duplicate("TCC-R225-"+symbols.Count);
                        if(!S.Dim(s,"b").Set(S.Ft(b)) || !S.Dim(s,"h").Set(S.Ft(h)))throw new InvalidOperationException("Tipo nao aceitou secao.");
                        if(!s.IsActive)s.Activate();doc.Regenerate();symbols[key]=s;return s;
                    }
                    void BeamParameters(FamilyInstance fi)
                    {
                        fi.get_Parameter(BuiltInParameter.YZ_JUSTIFICATION).Set(0);
                        fi.get_Parameter(BuiltInParameter.Y_JUSTIFICATION).Set((int)YJustification.Center);
                        fi.get_Parameter(BuiltInParameter.Z_JUSTIFICATION).Set((int)ZJustification.Top);
                        S.Set(fi,BuiltInParameter.Y_OFFSET_VALUE,0);S.Set(fi,BuiltInParameter.Z_OFFSET_VALUE,0);
                    }
                    void Comment(Element e) => e.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)?.Set(
                        "R225: retorno geometrico das correcoes comuns R210/R211/R223 Eberick. NAO EXECUTAR. Ligacoes, avisos e interfaces pendentes; sem armadura/modelo analitico atualizado.");
                    foreach(var e in plan.GetProperty("changedExistingElements").EnumerateArray())
                    {
                        var fi=(FamilyInstance)map[e.GetProperty("id").GetString()!];fi.Symbol=Symbol(fi.Symbol,e);
                        if(e.GetProperty("kind").GetString()=="beam")
                        {
                            ((LocationCurve)fi.Location).Curve=Line.CreateBound(S.P(S.N(e,"x"),S.N(e,"y"),S.N(e,"z")),S.P(S.N(e,"x2"),S.N(e,"y2"),S.N(e,"z")));
                            BeamParameters(fi);
                        }
                        Comment(fi);
                    }
                    foreach(var e in plan.GetProperty("addedElements").EnumerateArray())
                    {
                        FamilyInstance fi;
                        if(e.GetProperty("kind").GetString()=="column")
                        {
                            fi=doc.Create.NewFamilyInstance(S.P(S.N(e,"x"),S.N(e,"y"),S.N(e,"z0")),Symbol(((FamilyInstance)map["P1-N1"]).Symbol,e),S.LevelAt(doc,S.N(e,"z0")),StructuralType.Column);
                            S.SetId(fi,BuiltInParameter.FAMILY_TOP_LEVEL_PARAM,S.LevelAt(doc,S.N(e,"z1")).Id);
                            S.Set(fi,BuiltInParameter.FAMILY_BASE_LEVEL_OFFSET_PARAM,0);S.Set(fi,BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM,0);
                        }
                        else
                        {
                            var line=Line.CreateBound(S.P(S.N(e,"x"),S.N(e,"y"),S.N(e,"z")),S.P(S.N(e,"x2"),S.N(e,"y2"),S.N(e,"z")));
                            fi=doc.Create.NewFamilyInstance(line,Symbol(((FamilyInstance)map["V1-N1"]).Symbol,e),S.LevelAt(doc,S.N(e,"z")),StructuralType.Beam);
                            BeamParameters(fi);
                        }
                        fi.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).Set(e.GetProperty("id").GetString());Comment(fi);created.Add(fi.Id.Value);
                    }
                    doc.Regenerate();if(tx.Commit()!=TransactionStatus.Committed)throw new InvalidOperationException("Alteracoes revertidas.");
                }
                if(before!=S.LogicalHash(doc,retained))throw new InvalidOperationException("Um dos 59 elementos preservados mudou.");
                if(stairBefore!=JsonSerializer.Serialize(S.ReadStair(doc),S.Json))throw new InvalidOperationException("Geometria da escada mudou.");
                readback=Revision.Readback(doc,plan);
                using(var tx=new Transaction(doc,"Vista R225 para coordenacao"))
                {
                    tx.Start();var t=new FilteredElementCollector(doc).OfClass(typeof(ViewFamilyType)).Cast<ViewFamilyType>().First(t=>t.ViewFamily==ViewFamily.ThreeDimensional);
                    view=View3D.CreateIsometric(doc,t.Id);view.Name="TCC-R225-COORDENACAO-NAO-EXECUTAR";view.Discipline=ViewDiscipline.Coordination;
                    view.DisplayStyle=DisplayStyle.FlatColors;view.DetailLevel=ViewDetailLevel.Fine;
                    view.SetCategoryHidden(new ElementId(BuiltInCategory.OST_Levels),true);view.SetCategoryHidden(new ElementId(BuiltInCategory.OST_Grids),true);tx.Commit();
                }
                group.Assimilate();assimilated=true;ui.ActiveView=view!;doc.Save();saved=true;
            }
            Revision.Write("R225-aplicacao-nativa.json",new {StartedUtc=started,EndedUtc=DateTimeOffset.UtcNow,
                CommandMs=timer.Elapsed.TotalMilliseconds,CommandTimeIsNotFlowTime=true,Document=doc.PathName,
                Saved=saved,CreatedIds=created,Readback=readback,Warnings=failures.Rows,StructuralApproval=false});
            TaskDialog.Show("TCC R225","Salvo: 23 trechos de pilares, 32 vigas e 11 lajes, mais a escada17 preservada.\nRetorno geometrico da hipotese Eberick; ligacoes, avisos e interfaces ainda pendentes. NAO EXECUTAR.");
            return Result.Succeeded;
        }
        catch(Exception ex)
        {
            Revision.Write("R225-falha-"+DateTime.UtcNow.ToString("yyyyMMdd-HHmmss")+".json",new {Error=ex.ToString(),Assimilated=assimilated,Saved=saved,Warnings=failures.Rows});
            message=ex.Message;return Result.Failed;
        }
    }
}

[Transaction(TransactionMode.ReadOnly)]
public class AuditRevision : IExternalCommand
{
    public Result Execute(ExternalCommandData data,ref string message,ElementSet elements)
    {
        try
        {
            var doc=data.Application.ActiveUIDocument.Document;Revision.Guard(doc);
            Revision.Write("R225-releitura-"+DateTime.UtcNow.ToString("yyyyMMdd-HHmmss")+".json",Revision.Readback(doc,Revision.Read("R225-candidato-comum.json")));
            TaskDialog.Show("TCC R225","Releitura das 66 geometrias e da escada salva. Sem aprovacao estrutural.");return Result.Succeeded;
        }
        catch(Exception ex){message=ex.Message;return Result.Failed;}
    }
}

[Transaction(TransactionMode.Manual)]
public class ExportRevision : IExternalCommand
{
    public Result Execute(ExternalCommandData data,ref string message,ElementSet elements)
    {
        var timer=Stopwatch.StartNew();var started=DateTimeOffset.UtcNow;
        try
        {
            var doc=data.Application.ActiveUIDocument.Document;Revision.Guard(doc);
            if(doc.IsModified)throw new InvalidOperationException("Salvar a copia antes da exportacao.");
            var readback=Revision.Readback(doc,Revision.Read("R225-candidato-comum.json"));
            var name="H03-R225-Revit-COORDENACAO-NAO-EXECUTAR";
            var path=Path.Combine(Revision.Out,name+".ifc");
            if(File.Exists(path))throw new InvalidOperationException("O IFC R225 ja existe; preservar a primeira exportacao.");
            using var options=new IFCExportOptions {FileVersion=IFCVersion.IFC4};
            options.AddOption("ExportBaseQuantities","true");
            options.AddOption("ExportInternalRevitPropertySets","true");
            options.AddOption("ExportIFCCommonPropertySets","true");
            options.AddOption("ExportMaterialPsets","true");
            bool exported;
            using(var tx=new Transaction(doc,"TCC R225 - exportar IFC de controle"))
            {
                tx.Start();exported=doc.Export(Revision.Out,name,options);
                // Preserva o RVT salvo; dados transitorios de exportacao nao ficam no modelo.
                tx.RollBack();
            }
            if(!exported || !File.Exists(path))throw new InvalidOperationException("O exportador nao produziu IFC.");
            Revision.Write("R225-exportacao-ifc.json",new {StartedUtc=started,EndedUtc=DateTimeOffset.UtcNow,
                CommandMs=timer.Elapsed.TotalMilliseconds,CommandTimeIsNotFlowTime=true,
                File=path,Sha256=S.Hash(path),Bytes=new FileInfo(path).Length,FileVersion="IFC4",
                ExporterReturnedSuccess=exported,RvtModifiedAfterExport=doc.IsModified,
                Readback=readback,ExportedPropertiesAudited=false,StructuralApproval=false});
            TaskDialog.Show("TCC R225","IFC4 de controle salvo. Conferir geometria e propriedades no arquivo; exportacao nao comprova aprovacao estrutural.");
            return Result.Succeeded;
        }
        catch(Exception ex){message=ex.Message;return Result.Failed;}
    }
}

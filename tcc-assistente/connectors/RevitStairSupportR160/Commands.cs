using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;
using Autodesk.Revit.UI;
using System.Diagnostics;
using System.Text.Json;
using S=TccAssistente.RevitStairSupport.Study;

namespace TccAssistente.RevitStairSupportR160;

public static class Revision
{
    public const string Out=@"D:\TCC\outputs\Escada-H03-R160-SOMENTE-VIGA-NAO-EXECUTAR";
    public const string Copy=Out+@"\H03-R160-Revit-SOMENTE-VIGA-PATAMAR-NAO-EXECUTAR.rvt";
    public static JsonElement Read(string name)=>JsonDocument.Parse(File.ReadAllText(Path.Combine(Out,name))).RootElement;
    public static void Write(string name,object value)=>File.WriteAllText(Path.Combine(Out,name),JsonSerializer.Serialize(value,S.Json));
    public static void Guard(Document d)
    {
        if(d.IsFamilyDocument||!string.Equals(Path.GetFullPath(d.PathName),Copy,StringComparison.OrdinalIgnoreCase))throw new InvalidOperationException("Abrir apenas a cópia R160: "+Copy);
    }
    public static JsonElement Plan()
    {
        var config=Read("R160-config.json");var file=Path.Combine(Out,"R160-candidato-comum.json");
        if(!string.Equals(S.Hash(file),config.GetProperty("CandidateSha256").GetString(),StringComparison.OrdinalIgnoreCase))throw new InvalidOperationException("Candidato alterado após preparação.");
        return Read("R160-candidato-comum.json");
    }
    public static JsonElement[] Unchanged(JsonElement p)=>p.GetProperty("retainedExistingElements").EnumerateArray().Concat(p.GetProperty("changedExistingElements").EnumerateArray()).ToArray();
    public static object Readback(Document d,JsonElement plan)=>new{Elements=S.ReadElements(d,S.Entries(plan)),Stair=S.ReadStair(d),UnchangedLogicalHash=S.LogicalHash(d,Unchanged(plan)),UnchangedCount=62,Count=63,StructuralApproval=false,AnalyticalModelOrEberickUpdated=false};
}

[Transaction(TransactionMode.Manual)]
public class ApplyRevision:IExternalCommand
{
    public Result Execute(ExternalCommandData data,ref string message,ElementSet failed)
    {
        var watch=Stopwatch.StartNew();bool assimilated=false,saved=false;
        var warnings=new TccAssistente.RevitStairSupport.Failures();
        try
        {
            var ui=data.Application.ActiveUIDocument??throw new InvalidOperationException("Abrir a cópia R160.");var doc=ui.Document;Revision.Guard(doc);
            var config=Revision.Read("R160-config.json");var plan=Revision.Plan();var map=S.Elements(doc);
            if(doc.IsModified||!string.Equals(S.Hash(doc.PathName),config.GetProperty("CopySha256Before").GetString(),StringComparison.OrdinalIgnoreCase))throw new InvalidOperationException("Cópia mudou ou tem alterações não salvas.");
            if(map.Count!=65||S.Entries(plan).Length!=63||Revision.Unchanged(plan).Length!=62)throw new InvalidOperationException("Contagem inicial/final inesperada ou revisão já aplicada.");
            // Verifica todo o cadastro inicial, não somente as três marcas editadas.
            S.ReadElements(doc,S.Entries(S.Plan()));
            var remove=new[]{map["P12-ESC-N1"],map["P13-ESC-N1"]};
            if(remove[0].Id.Value!=473797||remove[1].Id.Value!=473798||map["V16-ESC-PAT"].Id.Value!=473802)throw new InvalidOperationException("Identidades dos elementos diferentes da R159 conferida.");
            var kept=Revision.Unchanged(plan);var before=S.LogicalHash(doc,kept);var stairsBefore=JsonSerializer.Serialize(S.ReadStair(doc),S.Json);
            var protectedIds=map.Values.Except(remove).Select(e=>e.Id.Value).Append(S.Stair(doc).Id.Value).ToHashSet();
            var deletedIds=new List<long>();View3D? view=null;object? result=null;
            using(var group=new TransactionGroup(doc,"TCC R160 - retirar 2 pilares e reposicionar somente a viga"))
            {
                group.Start();
                using(var tx=new Transaction(doc,"Somente viga no local marcado pelo usuário"))
                {
                    tx.Start();var options=tx.GetFailureHandlingOptions();options.SetFailuresPreprocessor(warnings);tx.SetFailureHandlingOptions(options);
                    foreach(var e in remove)
                    {
                        var deleted=doc.Delete(e.Id);if(deleted.Any(id=>protectedIds.Contains(id.Value)))throw new InvalidOperationException("Remoção afetaria outro elemento protegido.");
                        deletedIds.AddRange(deleted.Select(id=>id.Value));
                    }
                    var beam=(FamilyInstance)map["V16-ESC-PAT"];var curve=((LocationCurve)beam.Location).Curve;
                    S.Near(S.M(curve.GetEndPoint(0).Y),.8757833333333321,"Y inicial da viga");
                    ElementTransformUtils.MoveElement(doc,beam.Id,S.P(0,-.8757833333333321,0));
                    beam.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)?.Set("R160: somente viga entre P4/P10 em Y=0, conforme marcação do usuário. P12/P13 retirados. Conflito com faixa J4 da arquitetura registrado; seção, apoios e ligações sem dimensionamento. NÃO EXECUTAR.");
                    doc.Regenerate();
                    if(tx.Commit()!=TransactionStatus.Committed)throw new InvalidOperationException("Alteração revertida.");
                }
                if(S.LogicalHash(doc,kept)!=before)throw new InvalidOperationException("Um dos 62 elementos preservados mudou de identidade, eixo, perfil, seção ou material.");
                if(JsonSerializer.Serialize(S.ReadStair(doc),S.Json)!=stairsBefore)throw new InvalidOperationException("A escada mudou durante a revisão.");
                result=Revision.Readback(doc,plan);
                using(var tx=new Transaction(doc,"Vista R160 de conferência"))
                {
                    tx.Start();var t=new FilteredElementCollector(doc).OfClass(typeof(ViewFamilyType)).Cast<ViewFamilyType>().First(x=>x.ViewFamily==ViewFamily.ThreeDimensional);
                    view=View3D.CreateIsometric(doc,t.Id);view.Name="TCC-R160-SOMENTE-VIGA-PATAMAR";view.Discipline=ViewDiscipline.Coordination;view.DisplayStyle=DisplayStyle.FlatColors;view.DetailLevel=ViewDetailLevel.Fine;
                    if(ui.ActiveView is View3D old)view.SetOrientation(old.GetOrientation());
                    view.SetSectionBox(new BoundingBoxXYZ{Min=S.P(4.1,-.25,-.1),Max=S.P(6.9,3.7,3.7)});view.IsSectionBoxActive=true;
                    view.SetCategoryHidden(new ElementId(BuiltInCategory.OST_Levels),true);view.SetCategoryHidden(new ElementId(BuiltInCategory.OST_Grids),true);tx.Commit();
                }
                group.Assimilate();assimilated=true;ui.ActiveView=view!;doc.Save();saved=true;
            }
            Revision.Write("R160-criacao-nativa.json",new{StartedUtc=DateTimeOffset.UtcNow.Subtract(watch.Elapsed),EndedUtc=DateTimeOffset.UtcNow,CommandMs=watch.Elapsed.TotalMilliseconds,CommandTimeIsNotFlowTime=true,Document=doc.PathName,Readback=result,DeletedIds=deletedIds,BeamIdPreserved=473802,Warnings=warnings.Rows,WindowJ4ConflictUnderRecordedArchitectureInterpretation=true,StructuralApproval=false,EberickUpdated=false});
            TaskDialog.Show("TCC R160","Salvo: 2 pilares adicionais retirados; somente a viga reposicionada entre P4/P10.\n63 elementos: 22 pilares,30 vigas,11 lajes + escada17.\nConflito com J4 registrado. Seção/apoios/ligações não dimensionados. NÃO EXECUTAR.");return Result.Succeeded;
        }
        catch(Exception ex)
        {
            Revision.Write("R160-falha-"+DateTime.UtcNow.ToString("yyyyMMdd-HHmmss")+".json",new{Error=ex.ToString(),Assimilated=assimilated,Saved=saved,CommandMs=watch.Elapsed.TotalMilliseconds,Warnings=warnings.Rows});message=ex.Message;return Result.Failed;
        }
    }
}

[Transaction(TransactionMode.ReadOnly)]
public class AuditRevision:IExternalCommand
{
    public Result Execute(ExternalCommandData data,ref string message,ElementSet failed)
    {
        try
        {
            var doc=data.Application.ActiveUIDocument.Document;Revision.Guard(doc);var plan=Revision.Plan();
            Revision.Write("R160-releitura-nativa-"+DateTime.UtcNow.ToString("yyyyMMdd-HHmmss")+".json",Revision.Readback(doc,plan));
            TaskDialog.Show("TCC R160","Releitura salva: 63 elementos + escada17; sem os 2 pilares adicionais. Não é aprovação estrutural.");return Result.Succeeded;
        }
        catch(Exception ex){message=ex.Message;return Result.Failed;}
    }
}

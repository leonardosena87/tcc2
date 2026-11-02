using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Architecture;
using Autodesk.Revit.UI;
using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;
using System.Text.Json;

namespace TccAssistente.RevitStairs;

public static class Data
{
    public const string Output = @"D:\TCC\outputs\Escada-H03-R155-Revit-17-NAO-EXECUTAR";
    public const string Copy = Output + @"\H03-R155-Revit-ESCADA17-NAO-EXECUTAR.rvt";
    public const string Mark = "TCC-H03-ESCADA17";
    public static readonly JsonSerializerOptions Json = new() { WriteIndented=true };
    public static double Ft(double m)=>UnitUtils.ConvertToInternalUnits(m,UnitTypeId.Meters);
    public static double M(double ft)=>UnitUtils.ConvertFromInternalUnits(ft,UnitTypeId.Meters);
    public static void Write(string name,object value)=>File.WriteAllText(Path.Combine(Output,name),JsonSerializer.Serialize(value,Json));
    public static void Guard(Document doc)
    {
        if(doc.IsFamilyDocument||!string.Equals(Path.GetFullPath(doc.PathName),Copy,StringComparison.OrdinalIgnoreCase))
            throw new InvalidOperationException("Abra apenas a cópia R155: "+Copy);
    }
    public static string ProtectedGeometry(Document doc)
    {
        var cats=new[]{BuiltInCategory.OST_StructuralColumns,BuiltInCategory.OST_StructuralFraming,BuiltInCategory.OST_Floors};
        var rows=cats.SelectMany(c=>new FilteredElementCollector(doc).OfCategory(c).WhereElementIsNotElementType().ToElements())
            .OrderBy(e=>e.Id.Value).Select(e=>
            {
                var b=e.get_BoundingBox(null);
                return new {Id=e.Id.Value,e.UniqueId,Type=e.GetTypeId().Value,
                    Bounds=b==null?null:new[]{b.Min.X,b.Min.Y,b.Min.Z,b.Max.X,b.Max.Y,b.Max.Z},
                    Volume=e.get_Parameter(BuiltInParameter.HOST_VOLUME_COMPUTED)?.AsDouble()};
            }).ToArray();
        if(rows.Length!=62)throw new InvalidOperationException("Esperados62elementos preexistentes; encontrados"+rows.Length);
        return Convert.ToHexString(SHA256.HashData(System.Text.Encoding.UTF8.GetBytes(JsonSerializer.Serialize(rows,Json))));
    }
    public static Level LevelAt(Document doc,double m)=>new FilteredElementCollector(doc).OfClass(typeof(Level)).Cast<Level>()
        .Single(l=>Math.Abs(M(l.Elevation)-m)<1e-7);
    public static void Set(Element e,BuiltInParameter key,double value)
    {
        var p=e.get_Parameter(key)??throw new InvalidOperationException("Parâmetro ausente:"+key);
        if(p.IsReadOnly||!p.Set(value)||Math.Abs(p.AsDouble()-value)>1e-8)throw new InvalidOperationException("Falha no parâmetro:"+key);
    }
    public static Stairs Find(Document doc)=>new FilteredElementCollector(doc).OfClass(typeof(Stairs)).Cast<Stairs>()
        .Single(s=>s.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)?.AsString()==Mark);
    public static object Read(Document doc,Stairs stairs)
    {
        var runs=stairs.GetStairsRuns().Select(id=>(StairsRun)doc.GetElement(id)).OrderBy(r=>r.BaseElevation).ToArray();
        var landings=stairs.GetStairsLandings().Select(id=>(StairsLanding)doc.GetElement(id)).ToArray();
        if(stairs.ActualRisersNumber!=17||runs.Length!=2||runs[0].ActualRisersNumber!=9||runs[1].ActualRisersNumber!=8||landings.Length!=1)
            throw new InvalidOperationException("A geometria nativa não confirmou17espelhos,9+8 e1patamar.");
        if(Math.Abs(M(stairs.BaseElevation)-.22)>1e-6||Math.Abs(M(stairs.TopElevation)-3.25)>1e-6||Math.Abs(M(stairs.ActualRiserHeight)-3.03/17)>1e-6||Math.Abs(M(stairs.ActualTreadDepth)-.28)>1e-6)
            throw new InvalidOperationException($"Cotas/dimensões divergentes: base={M(stairs.BaseElevation):R};topo={M(stairs.TopElevation):R};espelho={M(stairs.ActualRiserHeight):R};pisada={M(stairs.ActualTreadDepth):R}.");
        if(Math.Abs(M(stairs.BaseElevation+landings[0].BaseElevation)-(.22+9*3.03/17))>1e-6)
            throw new InvalidOperationException("Patamar nativo em cota inesperada.");
        return new {Status="ESBOCO ACADEMICO - NAO DIMENSIONADO - NAO EXECUTAR",Id=stairs.Id.Value,stairs.UniqueId,
            TotalRisers=stairs.ActualRisersNumber,BaseM=M(stairs.BaseElevation),TopM=M(stairs.TopElevation),
            RiserM=M(stairs.ActualRiserHeight),TreadM=M(stairs.ActualTreadDepth),
            Runs=runs.Select(r=>new{Id=r.Id.Value,r.UniqueId,Risers=r.ActualRisersNumber,Treads=r.ActualTreadsNumber,
                BaseRelativeM=M(r.BaseElevation),TopRelativeM=M(r.TopElevation),r.BeginsWithRiser,r.EndsWithRiser,TypeId=r.GetTypeId().Value}),
            Landings=landings.Select(l=>new{Id=l.Id.Value,l.UniqueId,FinishedM=M(stairs.BaseElevation+l.BaseElevation),ThicknessM=M(l.Thickness)}),
            Railings=stairs.GetAssociatedRailings().Select(id=>id.Value).ToArray(),
            ProtectedGeometryHash=ProtectedGeometry(doc),StructuralApproval=false,SupportAndGuardDesignCompleted=false};
    }
}

public class Failures:IFailuresPreprocessor
{
    public List<object> Rows {get;}=[];
    public FailureProcessingResult PreprocessFailures(FailuresAccessor a)
    {
        bool error=false;
        foreach(var f in a.GetFailureMessages())
        {
            Rows.Add(new{Id=f.GetFailureDefinitionId().Guid,Severity=f.GetSeverity().ToString(),Description=f.GetDescriptionText(),Elements=f.GetFailingElementIds().Select(i=>i.Value).ToArray()});
            if(f.GetSeverity()==FailureSeverity.Warning)a.DeleteWarning(f);else error=true;
        }
        return error?FailureProcessingResult.ProceedWithRollBack:FailureProcessingResult.Continue;
    }
}

[Transaction(TransactionMode.Manual)]
public class CreateStair:IExternalCommand
{
    public Result Execute(ExternalCommandData data,ref string message,ElementSet failed)
    {
        var watch=Stopwatch.StartNew();var failures=new Failures();bool saved=false;
        try
        {
            var ui=data.Application.ActiveUIDocument??throw new InvalidOperationException("Abra a cópia R155.");var doc=ui.Document;Data.Guard(doc);
            if(new FilteredElementCollector(doc).OfClass(typeof(Stairs)).Any())throw new InvalidOperationException("Já existe escada; não criar duplicata.");
            var before=Data.ProtectedGeometry(doc);
            var config=JsonDocument.Parse(File.ReadAllText(Path.Combine(Data.Output,"R155-config.json"))).RootElement;
            var planPath=config.GetProperty("PlanPath").GetString()!;var expected=config.GetProperty("PlanSha256").GetString()!;
            if(!string.Equals(Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(planPath))),expected,StringComparison.OrdinalIgnoreCase))throw new InvalidDataException("Definição geométrica mudou.");
            var plan=JsonDocument.Parse(File.ReadAllText(planPath)).RootElement;var e=plan.GetProperty("clearEnvelope");
            var g=plan.GetProperty("geometry");
            if(g.GetProperty("totalRisers").GetInt32()!=17||g.GetProperty("lowerFlightRisers").GetInt32()!=9)throw new InvalidDataException("Configuração diferente de17/9+8.");
            double xl=e.GetProperty("xMinM").GetDouble(),xr=e.GetProperty("xMaxM").GetDouble(),w=e.GetProperty("flightWidthGraphicalM").GetDouble();
            double ys=e.GetProperty("ySouthM").GetDouble(),yn=e.GetProperty("landingNorthM").GetDouble(),start=e.GetProperty("lowerStartYM").GetDouble(),end=e.GetProperty("upperArrivalYM").GetDouble();
            _=Data.LevelAt(doc,.20);_=Data.LevelAt(doc,3.20);
            ElementId stairId;View3D? view=null;
            using(var group=new TransactionGroup(doc,"TCC R155 - escada17 de estudo"))
            {
                group.Start();
                Level bottom,top;
                using(var levelsTx=new Transaction(doc,"Referências dos pisos acabados da escada"))
                {
                    levelsTx.Start();bottom=Level.Create(doc,Data.Ft(.22));bottom.Name="TCC-R155-PISO-ACABADO-022";
                    top=Level.Create(doc,Data.Ft(3.25));top.Name="TCC-R155-PISO-ACABADO-325";levelsTx.Commit();
                }
                using(var scope=new StairsEditScope(doc,"Escada17 -9+8 - não executar"))
                {
                    stairId=scope.Start(bottom.Id,top.Id);
                    using(var tx=new Transaction(doc,"Geometria de estudo e tipos independentes"))
                    {
                        tx.Start();var opt=tx.GetFailureHandlingOptions();opt.SetFailuresPreprocessor(failures);tx.SetFailureHandlingOptions(opt);
                        var stairs=(Stairs)doc.GetElement(stairId);
                        var source=new FilteredElementCollector(doc).OfClass(typeof(StairsType)).Cast<StairsType>().Where(t=>t.ConstructionMethod==StairsConstructionMethod.CastInPlace).OrderBy(t=>t.Name).FirstOrDefault()??throw new InvalidOperationException("Tipo de escada moldada no local ausente.");
                        var type=(StairsType)source.Duplicate("TCC-R155-ESCADA17-ESTUDO-NAO-EXECUTAR");
                        var rt=(StairsRunType)((StairsRunType)doc.GetElement(type.RunType)).Duplicate("TCC-R155-LANCE-14cm-HIPOTESE");
                        var lt=(StairsLandingType)((StairsLandingType)doc.GetElement(type.LandingType)).Duplicate("TCC-R155-PATAMAR-14cm-HIPOTESE");
                        if(!rt.IsMonolithic||!lt.IsMonolithic)throw new InvalidOperationException("Tipos não monolíticos.");
                        rt.StructuralDepth=Data.Ft(.14);lt.Thickness=Data.Ft(.14);
                        var material=(Material)doc.GetElement(new ElementId(70123));
                        var materialAsset=(PropertySetElement)doc.GetElement(material.StructuralAssetId);
                        using(var asset=materialAsset.GetStructuralAsset())
                        {
                            if(asset.StructuralAssetClass!=StructuralAssetClass.Concrete||Math.Abs(UnitUtils.ConvertFromInternalUnits(asset.ConcreteCompression,UnitTypeId.Megapascals)-25)>1e-5)
                                throw new InvalidOperationException("Material da cópia não confirmou25MPa; não atribuir à escada.");
                        }
                        rt.MaterialId=material.Id;
                        var lm=lt.get_Parameter(BuiltInParameter.STAIRS_LANDINGTYPE_LANDING_MATERIAL);
                        if(lm==null||lm.IsReadOnly||!lm.Set(material.Id))throw new InvalidOperationException("Material do patamar não configurável.");
                        type.RunType=rt.Id;type.LandingType=lt.Id;stairs.ChangeTypeId(type.Id);
                        Data.Set(stairs,BuiltInParameter.STAIRS_BASE_OFFSET,0);Data.Set(stairs,BuiltInParameter.STAIRS_TOP_OFFSET,0);
                        doc.Regenerate();stairs.DesiredRisersNumber=17;doc.Regenerate();stairs.ActualTreadDepth=Data.Ft(.28);doc.Regenerate();
                        XYZ P(double x,double y)=>new(Data.Ft(x),Data.Ft(y),0);
                        StairsRun Run(double x1,double x2,double y1,double y2,int count,double baseRel)
                        {
                            var boundaries=new List<Curve>{Line.CreateBound(P(x1,y1),P(x1,y2)),Line.CreateBound(P(x2,y1),P(x2,y2))};
                            var risers=Enumerable.Range(0,count).Select(i=>(Curve)Line.CreateBound(P(x1,y1+(y2-y1)*i/(count-1)),P(x2,y1+(y2-y1)*i/(count-1)))).ToList();
                            var path=new List<Curve>{Line.CreateBound(P((x1+x2)/2,y1),P((x1+x2)/2,y2))};
                            return StairsRun.CreateSketchedRun(doc,stairId,Data.Ft(baseRel),boundaries,risers,path);
                        }
                        var lower=Run(xl,xl+w,start,yn,9,0);var upper=Run(xr-w,xr,yn,end,8,9*3.03/17);
                        var loop=CurveLoop.Create(new List<Curve>{Line.CreateBound(P(xl,ys),P(xr,ys)),Line.CreateBound(P(xr,ys),P(xr,yn)),Line.CreateBound(P(xr,yn),P(xl,yn)),Line.CreateBound(P(xl,yn),P(xl,ys))});
                        var landing=StairsLanding.CreateSketchedLanding(doc,stairId,loop,Data.Ft(9*3.03/17));
                        foreach(var el in new Element[]{stairs,lower,upper,landing})
                        {
                            el.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)?.Set("H03 R155 -17 espelhos - h14cm hipótese geométrica, não dimensionada; apoios/guardas/ELU/ELS pendentes. NÃO EXECUTAR.");
                        }
                        stairs.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)?.Set(Data.Mark);
                        if(tx.Commit()!=TransactionStatus.Committed)throw new InvalidOperationException("Transação revertida.");
                    }
                    scope.Commit(failures);
                }
                var created=(Stairs)doc.GetElement(stairId);
                Data.Write("R155-tentativa-leitura-"+DateTime.UtcNow.ToString("yyyyMMdd-HHmmss")+".json",new{BaseM=Data.M(created.BaseElevation),TopM=Data.M(created.TopElevation),RiserM=Data.M(created.ActualRiserHeight),TreadM=Data.M(created.ActualTreadDepth),Desired=created.DesiredRisersNumber,Actual=created.ActualRisersNumber});
                var read=Data.Read(doc,created);
                if(Data.ProtectedGeometry(doc)!=before)throw new InvalidOperationException("Geometria dos62elementos preexistentes mudou; reverter.");
                using(var tx=new Transaction(doc,"Vista de conferência da escada"))
                {
                    tx.Start();var vft=new FilteredElementCollector(doc).OfClass(typeof(ViewFamilyType)).Cast<ViewFamilyType>().First(v=>v.ViewFamily==ViewFamily.ThreeDimensional);
                    view=View3D.CreateIsometric(doc,vft.Id);view.Name="TCC-R155-ESCADA17-NAO-EXECUTAR";
                    view.SetSectionBox(new BoundingBoxXYZ{Min=new XYZ(Data.Ft(xl-.2),Data.Ft(ys-.2),Data.Ft(0)),Max=new XYZ(Data.Ft(xr+.2),Data.Ft(start+.5),Data.Ft(3.7))});view.IsSectionBoxActive=true;view.DisplayStyle=DisplayStyle.FlatColors;view.DetailLevel=ViewDetailLevel.Fine;
                    tx.Commit();
                }
                group.Assimilate();
                doc.Save();saved=true;
                Data.Write("R155-criacao-nativa.json",new{StartedUtc=DateTimeOffset.UtcNow.Subtract(watch.Elapsed),EndedUtc=DateTimeOffset.UtcNow,CommandMs=watch.Elapsed.TotalMilliseconds,CommandTimeIsNotFlowTime=true,Document=doc.PathName,BeforeProtectedHash=before,Readback=read,WarningsAndErrors=failures.Rows,StructuralDepthHypothesisM=.14,StructuralApproval=false});
                ui.ActiveView=view!;ui.Selection.SetElementIds(new List<ElementId>{stairId});ui.ShowElements(stairId);
            }
            TaskDialog.Show("TCC - escada17","Escada nativa criada e salva na cópia R155.\n17 espelhos,9+8; patamar acabado+1,824118m.\n14cm é hipótese geométrica, não dimensionamento.\nAvisos registrados:"+failures.Rows.Count+".\nConferir apoios, guardas e compatibilidade antes de calcular.");
            return Result.Succeeded;
        }
        catch(Exception ex){Data.Write("R155-falha-"+DateTime.UtcNow.ToString("yyyyMMdd-HHmmss")+".json",new{Error=ex.ToString(),Saved=saved,CommandMs=watch.Elapsed.TotalMilliseconds,Failures=failures.Rows});message=ex.Message;return Result.Failed;}
    }
}

[Transaction(TransactionMode.ReadOnly)]
public class AuditStair:IExternalCommand
{
    public Result Execute(ExternalCommandData data,ref string message,ElementSet failed)
    {
        try{var doc=data.Application.ActiveUIDocument.Document;Data.Guard(doc);var result=Data.Read(doc,Data.Find(doc));Data.Write("R155-releitura-nativa-"+DateTime.UtcNow.ToString("yyyyMMdd-HHmmss")+".json",result);TaskDialog.Show("TCC - conferir escada17","Leitura nativa confirmou17espelhos,9+8, pisos+.22/+3.25 e patamar+1.824118m.\nRelatório salvo; não é aprovação estrutural.");return Result.Succeeded;}
        catch(Exception ex){message=ex.Message;return Result.Failed;}
    }
}

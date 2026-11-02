using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Architecture;
using Autodesk.Revit.DB.Structure;
using Autodesk.Revit.UI;
using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;
using System.Text.Json;

namespace TccAssistente.RevitStairSupport;

public static class Study
{
    public const string Output=@"D:\TCC\outputs\Escada-H03-R159-IMPLANTACAO-NAO-EXECUTAR";
    public const string Copy=Output+@"\H03-R159-Revit-VIGA-PATAMAR-NAO-EXECUTAR.rvt";
    public const string Mark="TCC-H03-ESCADA17-R159-CONCRETO";
    public static readonly JsonSerializerOptions Json=new(){WriteIndented=true};
    public static double Ft(double m)=>UnitUtils.ConvertToInternalUnits(m,UnitTypeId.Meters);
    public static double M(double ft)=>UnitUtils.ConvertFromInternalUnits(ft,UnitTypeId.Meters);
    public static string Hash(string path)
    {
        // O Revit mantém o RVT aberto para escrita; esta leitura não altera o arquivo.
        using var stream=new FileStream(path,FileMode.Open,FileAccess.Read,FileShare.ReadWrite|FileShare.Delete);
        return Convert.ToHexString(SHA256.HashData(stream));
    }
    public static void Write(string name,object value)=>File.WriteAllText(Path.Combine(Output,name),JsonSerializer.Serialize(value,Json));
    public static void Guard(Document doc)
    {
        if(doc.IsFamilyDocument||!string.Equals(Path.GetFullPath(doc.PathName),Copy,StringComparison.OrdinalIgnoreCase))throw new InvalidOperationException("Use somente a cópia R159: "+Copy);
    }
    public static JsonElement Config()=>JsonDocument.Parse(File.ReadAllText(Path.Combine(Output,"R159-config.json"))).RootElement;
    public static JsonElement Plan()
    {
        var c=Config();var path=c.GetProperty("CandidatePath").GetString()!;
        if(!string.Equals(Hash(path),c.GetProperty("CandidateSha256").GetString(),StringComparison.OrdinalIgnoreCase))throw new InvalidDataException("O candidato mudou.");
        var j=JsonDocument.Parse(File.ReadAllText(path)).RootElement;
        if(j.GetProperty("schema").GetString()!="tcc-stair-compatibility/1"||j.GetProperty("units").GetString()!="m")throw new InvalidDataException("Contrato ou unidade diferente.");
        return j;
    }
    public static double N(JsonElement e,string k)
    {
        double x=e.GetProperty(k).GetDouble();if(!double.IsFinite(x)||Math.Abs(x)>100)throw new InvalidDataException("Número inválido:"+k);return x;
    }
    public static JsonElement[] Entries(JsonElement p)=>new[]{"retainedExistingElements","changedExistingElements","addedElements"}.SelectMany(k=>p.GetProperty(k).EnumerateArray()).ToArray();
    public static string Tag(Element e)=>e.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)?.AsString()??"";
    public static Dictionary<string,Element> Elements(Document doc)
    {
        var cats=new[]{BuiltInCategory.OST_StructuralColumns,BuiltInCategory.OST_StructuralFraming,BuiltInCategory.OST_Floors};
        return cats.SelectMany(c=>new FilteredElementCollector(doc).OfCategory(c).WhereElementIsNotElementType().ToElements()).ToDictionary(Tag);
    }
    public static Level LevelAt(Document doc,double z)=>new FilteredElementCollector(doc).OfClass(typeof(Level)).Cast<Level>().Single(l=>Math.Abs(M(l.Elevation)-z)<1e-7);
    public static XYZ P(double x,double y,double z=0)=>new(Ft(x),Ft(y),Ft(z));
    public static Parameter Dim(FamilySymbol s,string axis)
    {
        var names=axis=="b"?new[]{"b","Width","Largura"}:new[]{"h","Height","Altura","Depth"};
        foreach(var n in names){var p=s.LookupParameter(n);if(p is{StorageType:StorageType.Double}&&p.Definition.GetDataType()==SpecTypeId.Length)return p;}
        throw new InvalidOperationException("Dimensão ausente "+axis+" em "+s.Name);
    }
    public static void Set(Element e,BuiltInParameter key,double value)
    {
        var p=e.get_Parameter(key)??throw new InvalidOperationException("Parâmetro ausente:"+key);
        if(Math.Abs(p.AsDouble()-value)<1e-9)return;
        if(p.IsReadOnly||!p.Set(value)||Math.Abs(p.AsDouble()-value)>1e-8)throw new InvalidOperationException("Falha ao alterar:"+key);
    }
    public static void SetId(Element e,BuiltInParameter key,ElementId id)
    {
        var p=e.get_Parameter(key)??throw new InvalidOperationException("Parâmetro ausente:"+key);
        if(p.AsElementId()==id)return;if(p.IsReadOnly||!p.Set(id)||p.AsElementId()!=id)throw new InvalidOperationException("Falha:"+key);
    }
    public static void Near(double value,double expected,string label)
    {
        if(!double.IsFinite(value)||Math.Abs(value-expected)>1e-6)throw new InvalidOperationException($"{label}: {value:R} != {expected:R}");
    }
    public static double Material25(Document doc,Element e)
    {
        var mid=e is FamilyInstance fi?fi.StructuralMaterialId:((FloorType)doc.GetElement(e.GetTypeId())).StructuralMaterialId;
        return Material25Id(doc,mid,Tag(e));
    }
    public static double Material25Id(Document doc,ElementId mid,string label)
    {
        var mat=doc.GetElement(mid) as Material??throw new InvalidOperationException("Material estrutural ausente:"+label);
        var prop=doc.GetElement(mat.StructuralAssetId) as PropertySetElement??throw new InvalidOperationException("Ativo ausente:"+label);
        using var a=prop.GetStructuralAsset();if(a.StructuralAssetClass!=StructuralAssetClass.Concrete)throw new InvalidOperationException("Material não é concreto.");
        var mpa=UnitUtils.ConvertFromInternalUnits(a.ConcreteCompression,UnitTypeId.Megapascals);Near(mpa,25,"fck "+label);return mpa;
    }
    public static double[][] Profile(Document doc,Floor f)
    {
        var s=(Sketch)doc.GetElement(f.SketchId);
        return s.Profile.Cast<CurveArray>().SelectMany(a=>a.Cast<Curve>()).Select(c=>c.GetEndPoint(0)).Select(p=>new[]{M(p.X),M(p.Y),M(p.Z)}).OrderBy(p=>p[0]).ThenBy(p=>p[1]).ToArray();
    }
    public static object ReadElement(Document doc,Element element,JsonElement expected)
    {
        string kind=expected.GetProperty("kind").GetString()!,tag=expected.GetProperty("id").GetString()!;
        if(Tag(element)!=tag)throw new InvalidOperationException("Marca divergente");
        double[] axis;double b=0,h,rotation=0;double[][]? profile=null;
        if(kind=="column")
        {
            var fi=(FamilyInstance)element;var pt=((LocationPoint)fi.Location).Point;
            rotation=((LocationPoint)fi.Location).Rotation;Near(rotation,0,tag+" rotação");
            var baseL=(Level)doc.GetElement(fi.get_Parameter(BuiltInParameter.FAMILY_BASE_LEVEL_PARAM).AsElementId());
            var topL=(Level)doc.GetElement(fi.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_PARAM).AsElementId());
            axis=new[]{M(pt.X),M(pt.Y),M(baseL.Elevation+fi.get_Parameter(BuiltInParameter.FAMILY_BASE_LEVEL_OFFSET_PARAM).AsDouble()),M(topL.Elevation+fi.get_Parameter(BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM).AsDouble())};
            Near(axis[0],N(expected,"x"),tag+" X");Near(axis[1],N(expected,"y"),tag+" Y");Near(axis[2],N(expected,"z0"),tag+" Z0");Near(axis[3],N(expected,"z1"),tag+" Z1");
            b=M(Dim(fi.Symbol,"b").AsDouble());h=M(Dim(fi.Symbol,"h").AsDouble());Near(b,N(expected,"b"),tag+" b");
        }
        else if(kind=="beam")
        {
            var fi=(FamilyInstance)element;var curve=((LocationCurve)fi.Location).Curve;var p=curve.GetEndPoint(0);var q=curve.GetEndPoint(1);
            var want=new[]{P(N(expected,"x"),N(expected,"y"),N(expected,"z")),P(N(expected,"x2"),N(expected,"y2"),N(expected,"z"))};
            if(p.DistanceTo(want[0])+q.DistanceTo(want[1])>p.DistanceTo(want[1])+q.DistanceTo(want[0]))(p,q)=(q,p);
            Near(M(p.DistanceTo(want[0])),0,tag+" início");Near(M(q.DistanceTo(want[1])),0,tag+" fim");
            axis=new[]{M(p.X),M(p.Y),M(p.Z),M(q.X),M(q.Y),M(q.Z)};
            b=M(Dim(fi.Symbol,"b").AsDouble());h=M(Dim(fi.Symbol,"h").AsDouble());Near(b,N(expected,"b"),tag+" b");
            Near(fi.get_Parameter(BuiltInParameter.Z_JUSTIFICATION).AsInteger(),(int)ZJustification.Top,tag+" justificação topo");
            Near(M(fi.get_Parameter(BuiltInParameter.Y_OFFSET_VALUE).AsDouble()),0,tag+" offsetY");Near(M(fi.get_Parameter(BuiltInParameter.Z_OFFSET_VALUE).AsDouble()),0,tag+" offsetZ");
        }
        else if(kind=="slab")
        {
            var f=(Floor)element;profile=Profile(doc,f);var lev=(Level)doc.GetElement(f.LevelId);double z=M(lev.Elevation+f.get_Parameter(BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM).AsDouble());
            if(profile.Length!=4)throw new InvalidOperationException("Perfil não retangular:"+tag);
            var want=new[]{new[]{N(expected,"x"),N(expected,"y")},new[]{N(expected,"x2"),N(expected,"y")},new[]{N(expected,"x2"),N(expected,"y2")},new[]{N(expected,"x"),N(expected,"y2")}}.OrderBy(p=>p[0]).ThenBy(p=>p[1]).ToArray();
            for(int i=0;i<4;i++){Near(profile[i][0],want[i][0],tag+" perfilX");Near(profile[i][1],want[i][1],tag+" perfilY");}
            Near(z,N(expected,"z"),tag+" topo");axis=new[]{z};h=M(((FloorType)doc.GetElement(f.GetTypeId())).GetCompoundStructure().GetWidth());
        }
        else throw new InvalidDataException("Tipo desconhecido:"+kind);
        Near(h,N(expected,"h"),tag+" h");var fck=Material25(doc,element);
        var materialId=element is FamilyInstance family?family.StructuralMaterialId.Value:((FloorType)doc.GetElement(element.GetTypeId())).StructuralMaterialId.Value;
        return new{Mark=tag,Id=element.Id.Value,element.UniqueId,TypeId=element.GetTypeId().Value,Kind=kind,AxisM=axis,BM=b,HM=h,RotationRad=rotation,ProfileM=profile,MaterialId=materialId,MaterialFckMPa=fck};
    }
    public static object[] ReadElements(Document doc,JsonElement[] entries)
    {
        var map=Elements(doc);if(map.Count!=entries.Length)throw new InvalidOperationException("Contagem estrutural divergente.");
        return entries.OrderBy(e=>e.GetProperty("id").GetString()).Select(e=>ReadElement(doc,map[e.GetProperty("id").GetString()!],e)).ToArray();
    }
    public static string LogicalHash(Document doc,JsonElement[] retained)
    {
        var map=Elements(doc);var rows=retained.OrderBy(e=>e.GetProperty("id").GetString()).Select(e=>ReadElement(doc,map[e.GetProperty("id").GetString()!],e)).ToArray();
        return Convert.ToHexString(SHA256.HashData(System.Text.Encoding.UTF8.GetBytes(JsonSerializer.Serialize(rows,Json))));
    }
    public static Stairs Stair(Document doc)=>new FilteredElementCollector(doc).OfClass(typeof(Stairs)).Cast<Stairs>().Single(s=>Tag(s)==Mark);
    public static object ReadStair(Document doc)
    {
        var s=Stair(doc);var runs=s.GetStairsRuns().Select(id=>(StairsRun)doc.GetElement(id)).OrderBy(r=>r.BaseElevation).ToArray();var lands=s.GetStairsLandings().Select(id=>(StairsLanding)doc.GetElement(id)).ToArray();
        if(s.ActualRisersNumber!=17||runs.Length!=2||runs[0].ActualRisersNumber!=9||runs[1].ActualRisersNumber!=8||lands.Length!=1)throw new InvalidOperationException("Escada não confirmou17/9+8.");
        Near(M(s.BaseElevation),.17,"base virtual concreto");Near(M(s.TopElevation),3.20,"topo concreto");Near(M(s.ActualRiserHeight),3.03/17,"espelho");Near(M(s.ActualTreadDepth),.28,"pisada");
        Near(M(s.BaseElevation+lands[0].BaseElevation),.22+9*3.03/17-.05,"patamar concreto");
        double[][] Footprint(CurveLoop loop)=>loop.SelectMany(c=>new[]{c.GetEndPoint(0),c.GetEndPoint(1)}).Select(p=>new[]{M(p.X),M(p.Y),M(p.Z)}).ToArray();
        var plan=Plan();var landing=plan.GetProperty("concreteTopSurfaces").EnumerateArray().Single(f=>f.GetProperty("kind").GetString()=="landing");
        var vertices=landing.GetProperty("vertices").EnumerateArray().Select(v=>v.EnumerateArray().Select(x=>x.GetDouble()).ToArray()).ToArray();
        double xl=vertices.Min(p=>p[0]),xr=vertices.Max(p=>p[0]),ys=vertices.Min(p=>p[1]),yn=vertices.Max(p=>p[1]);
        void CheckBounds(double[][] points,double xmin,double xmax,double ymin,double ymax,string label)
        {
            Near(points.Min(p=>p[0]),xmin,label+" Xmin");Near(points.Max(p=>p[0]),xmax,label+" Xmax");
            Near(points.Min(p=>p[1]),ymin,label+" Ymin");Near(points.Max(p=>p[1]),ymax,label+" Ymax");
        }
        var runDetails=runs.Select((r,i)=>
        {
            var type=(StairsRunType)doc.GetElement(r.GetTypeId());Near(M(type.StructuralDepth),.14,"espessura hipotetica lance");
            var fck=Material25Id(doc,type.MaterialId,"lance "+r.Id.Value);
            var footprint=Footprint(r.GetFootprintBoundary());
            // ActualRunWidth é documentado como zero para lances por croqui; medir o contorno destes lances retos.
            CheckBounds(footprint,i==0?xl:xr-.90,i==0?xl+.90:xr,yn,yn+(i==0?8:7)*.28,"lance "+i);
            double width=footprint.Max(p=>p[0])-footprint.Min(p=>p[0]);Near(width,.90,"largura nominal pelo contorno");
            return new{Id=r.Id.Value,Risers=r.ActualRisersNumber,Treads=r.ActualTreadsNumber,WidthM=width,ApiActualRunWidthM=M(r.ActualRunWidth),WidthMeasuredFromFootprint=true,BaseRelativeM=M(r.BaseElevation),TopRelativeM=M(r.TopElevation),
                StructuralDepthM=M(type.StructuralDepth),MaterialFckMPa=fck,FootprintProjectedToBaseLevelM=footprint};
        }).ToArray();
        Near(M(lands[0].Thickness),.14,"espessura hipotetica patamar");
        var landingType=(StairsLandingType)doc.GetElement(lands[0].GetTypeId());
        var landingFck=Material25Id(doc,landingType.get_Parameter(BuiltInParameter.STAIRS_LANDINGTYPE_LANDING_MATERIAL).AsElementId(),"patamar");
        var landingFootprint=Footprint(lands[0].GetFootprintBoundary());CheckBounds(landingFootprint,xl,xr,ys,yn,"patamar");
        return new{Id=s.Id.Value,s.UniqueId,TotalRisers=s.ActualRisersNumber,BaseVirtualConcreteM=M(s.BaseElevation),TopConcreteM=M(s.TopElevation),RiserM=M(s.ActualRiserHeight),TreadM=M(s.ActualTreadDepth),
            Runs=runDetails,LandingFootprintProjectedM=landingFootprint,LandingMaterialFckMPa=landingFck,
            ConcreteLandingM=M(s.BaseElevation+lands[0].BaseElevation),LandingThicknessM=M(lands[0].Thickness),Railings=s.GetAssociatedRailings().Select(id=>id.Value),
            FinishHypothesisM=.05,LowerSupportUnresolved=true,StructuralApproval=false};
    }
}

public class Failures:IFailuresPreprocessor
{
    public readonly List<object> Rows=[];
    public FailureProcessingResult PreprocessFailures(FailuresAccessor a)
    {
        bool error=false;
        foreach(var f in a.GetFailureMessages())
        {
            Rows.Add(new{Id=f.GetFailureDefinitionId().Guid,Severity=f.GetSeverity().ToString(),Description=f.GetDescriptionText(),ElementIds=f.GetFailingElementIds().Select(id=>id.Value).ToArray()});
            if(f.GetSeverity()==FailureSeverity.Warning)a.DeleteWarning(f);else error=true;
        }
        return error?FailureProcessingResult.ProceedWithRollBack:FailureProcessingResult.Continue;
    }
}

[Transaction(TransactionMode.Manual)]
public class ApplyCandidate:IExternalCommand
{
    public Result Execute(ExternalCommandData data,ref string message,ElementSet failed)
    {
        var watch=Stopwatch.StartNew();var warnings=new Failures();bool saved=false,assimilated=false;string phase="guard";
        try
        {
            var ui=data.Application.ActiveUIDocument??throw new InvalidOperationException("Abra a cópia R159.");var doc=ui.Document;Study.Guard(doc);
            var config=Study.Config();
            if(doc.IsModified||!string.Equals(Study.Hash(doc.PathName),config.GetProperty("CopySha256Before").GetString(),StringComparison.OrdinalIgnoreCase))throw new InvalidOperationException("Cópia modificada desde a preparação; não aplicar sobre alterações pendentes.");
            var plan=Study.Plan();var entries=Study.Entries(plan);var retained=plan.GetProperty("retainedExistingElements").EnumerateArray().ToArray();
            if(entries.Length!=65||retained.Length!=60||entries.Select(e=>e.GetProperty("id").GetString()).Distinct().Count()!=65)throw new InvalidDataException("Esperados65elementos e60retidos.");
            var map=Study.Elements(doc);if(map.Count!=62||map.ContainsKey("V16-ESC-PAT"))throw new InvalidOperationException("Cópia não está na base62ou já foi aplicada.");
            var before=Study.LogicalHash(doc,retained);var oldStairs=new FilteredElementCollector(doc).OfClass(typeof(Stairs)).Cast<Stairs>().Single();
            if(Study.Tag(oldStairs)!="TCC-H03-ESCADA17")throw new InvalidOperationException("Escada de origem inesperada.");
            if(new FilteredElementCollector(doc).OfClass(typeof(RevitLinkInstance)).Any())throw new InvalidOperationException("Cópia com vínculo não previsto.");
            var columnBase=((FamilyInstance)map["P4-N1"]).Symbol;var beamBase=((FamilyInstance)map["V13-N1"]).Symbol;
            var oldIds=map.Values.Select(e=>e.Id.Value).ToHashSet();
            View3D? view=null;object read;
            using(var group=new TransactionGroup(doc,"TCC R159 - candidato com viga no patamar"))
            {
                group.Start();
                using(var tx=new Transaction(doc,"Apoios e viga de chegada - hipótese comum"))
                {
                    tx.Start();var opts=tx.GetFailureHandlingOptions();opts.SetFailuresPreprocessor(warnings);tx.SetFailureHandlingOptions(opts);
                    var deleted=doc.Delete(oldStairs.Id);if(deleted.Any(id=>oldIds.Contains(id.Value)))throw new InvalidOperationException("Remoção da escada afetaria elemento estrutural preexistente.");
                    FamilySymbol Symbol(double b,double h,string name)
                    {
                        var s=(FamilySymbol)beamBase.Duplicate(name);Study.Dim(s,"b").Set(Study.Ft(b));Study.Dim(s,"h").Set(Study.Ft(h));if(!s.IsActive)s.Activate();return s;
                    }
                    var beam=(FamilyInstance)map["V15-N1"];var spec=plan.GetProperty("changedExistingElements").EnumerateArray().Single(e=>e.GetProperty("id").GetString()=="V15-N1");
                    beam.Symbol=Symbol(.20,.16,"TCC-R159-V15-20x16-HIPOTESE");
                    var curve=((LocationCurve)beam.Location).Curve;double dy=Study.N(spec,"y")-Study.M(curve.GetEndPoint(0).Y);
                    ElementTransformUtils.MoveElement(doc,beam.Id,new XYZ(0,Study.Ft(dy),0));
                    foreach(var e in plan.GetProperty("addedElements").EnumerateArray())
                    {
                        string tag=e.GetProperty("id").GetString()!;Element element;
                        if(e.GetProperty("kind").GetString()=="column")
                        {
                            Study.Near(Study.M(Study.Dim(columnBase,"b").AsDouble()),.20,"pilar base b");Study.Near(Study.M(Study.Dim(columnBase,"h").AsDouble()),.30,"pilar base h");
                            var c=doc.Create.NewFamilyInstance(Study.P(Study.N(e,"x"),Study.N(e,"y"),.20),columnBase,Study.LevelAt(doc,.20),StructuralType.Column);
                            Study.SetId(c,BuiltInParameter.FAMILY_TOP_LEVEL_PARAM,Study.LevelAt(doc,3.20).Id);Study.Set(c,BuiltInParameter.FAMILY_BASE_LEVEL_OFFSET_PARAM,0);Study.Set(c,BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM,0);element=c;
                        }
                        else
                        {
                            double z=Study.N(e,"z");var level=Level.Create(doc,Study.Ft(z));level.Name="TCC-R159-PATAMAR-CONCRETO";
                            var line=Line.CreateBound(Study.P(Study.N(e,"x"),Study.N(e,"y"),z),Study.P(Study.N(e,"x2"),Study.N(e,"y2"),z));
                            var b=doc.Create.NewFamilyInstance(line,Symbol(.20,.30,"TCC-R159-V16-20x30-HIPOTESE"),level,StructuralType.Beam);
                            b.get_Parameter(BuiltInParameter.YZ_JUSTIFICATION).Set(0);b.get_Parameter(BuiltInParameter.Y_JUSTIFICATION).Set((int)YJustification.Center);b.get_Parameter(BuiltInParameter.Z_JUSTIFICATION).Set((int)ZJustification.Top);
                            Study.Set(b,BuiltInParameter.Y_OFFSET_VALUE,0);Study.Set(b,BuiltInParameter.Z_OFFSET_VALUE,0);element=b;
                        }
                        element.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).Set(tag);element.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)?.Set("R159 candidato comum; seção não dimensionada; apoios N0 idealizados, sem projeto de fundações. NÃO EXECUTAR.");
                    }
                    doc.Regenerate();if(tx.Commit()!=TransactionStatus.Committed)throw new InvalidOperationException("Transação dos apoios revertida.");
                }
                var floor=(Floor)map["L6-N1"];var floorSpec=plan.GetProperty("changedExistingElements").EnumerateArray().Single(e=>e.GetProperty("id").GetString()=="L6-N1");
                using(var scope=new SketchEditScope(doc,"R159 borda de L6"))
                {
                    scope.Start(floor.SketchId);
                    using(var tx=new Transaction(doc,"Atualizar borda preservando a laje"))
                    {
                        tx.Start();var sketch=(Sketch)doc.GetElement(floor.SketchId);
                        // A API documenta o vínculo entre o perfil e sua curva por Reference.ElementId.
                        // GetAllElements inclui elementos auxiliares e não define os quatro lados do perfil.
                        var curves=sketch.Profile.Cast<CurveArray>().SelectMany(a=>a.Cast<Curve>()).Select(c=>doc.GetElement(c.Reference.ElementId) as CurveElement??throw new InvalidOperationException("Curva do perfil L6 sem elemento associado.")).ToArray();
                        if(curves.Length!=4||curves.Select(c=>c.Id.Value).Distinct().Count()!=4)throw new InvalidOperationException("L6 sem os4lados distintos previstos no perfil.");
                        int count=0;
                        foreach(var mc in curves)
                        {
                            var c=mc.GeometryCurve;var a=c.GetEndPoint(0);var b=c.GetEndPoint(1);
                            XYZ Move(XYZ p)=>Math.Abs(Study.M(p.Y)-2.85)<1e-6?new XYZ(p.X,Study.Ft(Study.N(floorSpec,"y")),p.Z):p;
                            var aa=Move(a);var bb=Move(b);if(aa.DistanceTo(a)+bb.DistanceTo(b)>1e-8){mc.SetGeometryCurve(Line.CreateBound(aa,bb),true);count++;}
                        }
                        if(count!=3)throw new InvalidOperationException("L6 não confirmou3lados afetados.");tx.Commit();
                    }
                    scope.Commit(warnings);
                }
                CreateStair(doc,plan,warnings);
                phase="read-elements";var nativeElements=Study.ReadElements(doc,entries);phase="read-stair";var nativeStair=Study.ReadStair(doc);
                if(Study.LogicalHash(doc,retained)!=before)throw new InvalidOperationException("Um dos60elementos retidos mudou de identidade, tipo, eixo/perfil ou material.");
                using(var tx=new Transaction(doc,"Vista R159 de conferência"))
                {
                    tx.Start();var type=new FilteredElementCollector(doc).OfClass(typeof(ViewFamilyType)).Cast<ViewFamilyType>().First(t=>t.ViewFamily==ViewFamily.ThreeDimensional);
                    view=View3D.CreateIsometric(doc,type.Id);view.Name="TCC-R159-VIGA-PATAMAR-NAO-EXECUTAR";view.Discipline=ViewDiscipline.Coordination;
                    view.SetSectionBox(new BoundingBoxXYZ{Min=Study.P(4.1,-.25,-.1),Max=Study.P(6.9,3.7,3.7)});view.IsSectionBoxActive=true;view.DisplayStyle=DisplayStyle.FlatColors;view.DetailLevel=ViewDetailLevel.Fine;
                    view.SetCategoryHidden(new ElementId(BuiltInCategory.OST_Stairs),false);view.SetCategoryHidden(new ElementId(BuiltInCategory.OST_Levels),true);view.SetCategoryHidden(new ElementId(BuiltInCategory.OST_Grids),true);tx.Commit();
                }
                read=new{Elements=nativeElements,Stair=nativeStair,RetainedLogicalHash=before,RetainedCount=60,Count=65,StructuralApproval=false,AnalyticalModelOrEberickUpdated=false};
                phase="assimilate";group.Assimilate();assimilated=true;phase="save";ui.ActiveView=view!;doc.Save();saved=true;
                Study.Write("R159-criacao-nativa.json",new{StartedUtc=DateTimeOffset.UtcNow.Subtract(watch.Elapsed),EndedUtc=DateTimeOffset.UtcNow,CommandMs=watch.Elapsed.TotalMilliseconds,CommandTimeIsNotFlowTime=true,Document=doc.PathName,Readback=read,Warnings=warnings.Rows,FullSolidClashAndStructuralDesignCompleted=false});
            }
            TaskDialog.Show("TCC R159","Candidato salvo:65elementos estruturais + escada17.\nViga no patamar e2pilares laterais criados.\nSeções, ancoragem, apoio inferior, ELU/ELS e interferências ainda em estudo. NÃO EXECUTAR.");return Result.Succeeded;
        }
        catch(Exception ex){Study.Write("R159-falha-"+DateTime.UtcNow.ToString("yyyyMMdd-HHmmss")+".json",new{Error=ex.ToString(),Phase=phase,Assimilated=assimilated,Saved=saved,DocumentModifiedAfterFailure=data.Application.ActiveUIDocument?.Document.IsModified,CommandMs=watch.Elapsed.TotalMilliseconds,Warnings=warnings.Rows});message=ex.Message;return Result.Failed;}
    }
    static void CreateStair(Document doc,JsonElement plan,Failures warnings)
    {
        var faces=plan.GetProperty("concreteTopSurfaces").EnumerateArray().ToArray();var landing=faces.Single(f=>f.GetProperty("kind").GetString()=="landing");var vs=landing.GetProperty("vertices").EnumerateArray().Select(v=>v.EnumerateArray().Select(x=>x.GetDouble()).ToArray()).ToArray();
        double xl=vs.Min(p=>p[0]),xr=vs.Max(p=>p[0]),ys=vs.Min(p=>p[1]),yn=vs.Max(p=>p[1]);
        var bottom=default(Level);
        using(var tx=new Transaction(doc,"Referência virtual inferior do concreto")){tx.Start();bottom=Level.Create(doc,Study.Ft(.17));bottom.Name="TCC-R159-BASE-VIRTUAL-017-APOIO-PENDENTE";tx.Commit();}
        using(var scope=new StairsEditScope(doc,"R159 escada17 em concreto"))
        {
            var id=scope.Start(bottom.Id,Study.LevelAt(doc,3.20).Id);
            using(var tx=new Transaction(doc,"R159 lances e patamar"))
            {
                tx.Start();var stairs=(Stairs)doc.GetElement(id);var baseType=new FilteredElementCollector(doc).OfClass(typeof(StairsType)).Cast<StairsType>().Where(t=>t.ConstructionMethod==StairsConstructionMethod.CastInPlace).OrderBy(t=>t.Name).First();
                var type=(StairsType)baseType.Duplicate("TCC-R159-ESCADA17-HIPOTESE");var rt=(StairsRunType)((StairsRunType)doc.GetElement(type.RunType)).Duplicate("TCC-R159-LANCE-14cm-HIPOTESE");var lt=(StairsLandingType)((StairsLandingType)doc.GetElement(type.LandingType)).Duplicate("TCC-R159-PATAMAR-14cm-HIPOTESE");
                if(!rt.IsMonolithic||!lt.IsMonolithic)throw new InvalidOperationException("Tipos não monolíticos");rt.StructuralDepth=Study.Ft(.14);lt.Thickness=Study.Ft(.14);rt.MaterialId=new ElementId(70123);lt.get_Parameter(BuiltInParameter.STAIRS_LANDINGTYPE_LANDING_MATERIAL).Set(new ElementId(70123));
                type.RunType=rt.Id;type.LandingType=lt.Id;stairs.ChangeTypeId(type.Id);Study.Set(stairs,BuiltInParameter.STAIRS_BASE_OFFSET,0);Study.Set(stairs,BuiltInParameter.STAIRS_TOP_OFFSET,0);doc.Regenerate();stairs.DesiredRisersNumber=17;doc.Regenerate();stairs.ActualTreadDepth=Study.Ft(.28);doc.Regenerate();
                StairsRun Run(double x1,double x2,double y1,double y2,int n,double z)
                {
                    var bounds=new List<Curve>{Line.CreateBound(Study.P(x1,y1),Study.P(x1,y2)),Line.CreateBound(Study.P(x2,y1),Study.P(x2,y2))};
                    var risers=Enumerable.Range(0,n).Select(i=>(Curve)Line.CreateBound(Study.P(x1,y1+(y2-y1)*i/(n-1)),Study.P(x2,y1+(y2-y1)*i/(n-1)))).ToList();
                    return StairsRun.CreateSketchedRun(doc,id,Study.Ft(z),bounds,risers,new List<Curve>{Line.CreateBound(Study.P((x1+x2)/2,y1),Study.P((x1+x2)/2,y2))});
                }
                Run(xl,xl+.90,yn+8*.28,yn,9,0);Run(xr-.90,xr,yn,yn+7*.28,8,9*3.03/17);
                var pts=new[]{Study.P(xl,ys),Study.P(xr,ys),Study.P(xr,yn),Study.P(xl,yn)};var loop=new CurveLoop();for(int i=0;i<4;i++)loop.Append(Line.CreateBound(pts[i],pts[(i+1)%4]));StairsLanding.CreateSketchedLanding(doc,id,loop,Study.Ft(9*3.03/17));
                stairs.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).Set(Study.Mark);stairs.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)?.Set("Concreto descontado de5cm de acabamento hipotético; basevirtual+.17,apoio inferior pendente;14cm não dimensionados. NÃO EXECUTAR.");
                if(tx.Commit()!=TransactionStatus.Committed)throw new InvalidOperationException("Escada revertida");
            }
            scope.Commit(warnings);
        }
    }
}

[Transaction(TransactionMode.ReadOnly)]
public class AuditCandidate:IExternalCommand
{
    public Result Execute(ExternalCommandData data,ref string message,ElementSet failed)
    {
        try
        {
            var doc=data.Application.ActiveUIDocument.Document;Study.Guard(doc);var plan=Study.Plan();var entries=Study.Entries(plan);var retained=plan.GetProperty("retainedExistingElements").EnumerateArray().ToArray();
            Study.Write("R159-releitura-nativa-"+DateTime.UtcNow.ToString("yyyyMMdd-HHmmss")+".json",new{Elements=Study.ReadElements(doc,entries),Stair=Study.ReadStair(doc),RetainedLogicalHash=Study.LogicalHash(doc,retained),RetainedCount=60,Count=65,StructuralApproval=false,AnalyticalModelOrEberickUpdated=false});
            TaskDialog.Show("TCC R159","Releitura confirmou65elementos e escada17/9+8. Relatório salvo. Não é aprovação estrutural.");return Result.Succeeded;
        }
        catch(Exception ex){message=ex.Message;return Result.Failed;}
    }
}

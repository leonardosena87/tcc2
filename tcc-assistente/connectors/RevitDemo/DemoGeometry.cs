using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;
using Autodesk.Revit.UI;
using System.Diagnostics;

namespace TccAssistente.RevitDemo;

public sealed record CreatedElement(string SourceId,long RevitId,string UniqueId,string Kind,double? BM,double HM);
public sealed record GeometryResult(View3D View,double Seconds,List<CreatedElement> Elements);
public static class DemoGeometry
{
    static double Ft(double m)=>UnitUtils.ConvertToInternalUnits(m,UnitTypeId.Meters);
    static Parameter Dim(FamilySymbol s,string name)=>s.LookupParameter(name) is {IsReadOnly:false,StorageType:StorageType.Double} p&&p.Definition.GetDataType()==SpecTypeId.Length?p:throw new InvalidOperationException("Tipo base sem dimensão editável: "+name);
    static FamilySymbol Base(Document doc,BuiltInCategory category,string name)=>new FilteredElementCollector(doc).OfClass(typeof(FamilySymbol)).OfCategory(category).Cast<FamilySymbol>().SingleOrDefault(s=>s.Name==name)??throw new InvalidOperationException("Tipo base ausente: "+name);
    static void Set(Element e,BuiltInParameter key,double value){var p=e.get_Parameter(key)??throw new InvalidOperationException("Parâmetro ausente: "+key);if(Math.Abs(p.AsDouble()-value)<1e-9)return;if(p.IsReadOnly||!p.Set(value)||Math.Abs(p.AsDouble()-value)>1e-8)throw new InvalidOperationException("Falha ao ajustar "+key);}
    static void Set(Element e,BuiltInParameter key,ElementId value){var p=e.get_Parameter(key)??throw new InvalidOperationException("Parâmetro ausente: "+key);if(p.AsElementId()==value)return;if(p.IsReadOnly||!p.Set(value)||p.AsElementId()!=value)throw new InvalidOperationException("Falha ao ajustar "+key);}
    static void Set(Element e,BuiltInParameter key,int value){var p=e.get_Parameter(key)??throw new InvalidOperationException("Parâmetro ausente: "+key);if(p.AsInteger()==value)return;if(p.IsReadOnly||!p.Set(value)||p.AsInteger()!=value)throw new InvalidOperationException("Falha ao ajustar "+key);}
    public static GeometryResult Create(UIDocument ui,DemoPlan plan,string runId)
    {
        plan.RequireReady();var doc=ui.Document;
        var categories=new[]{BuiltInCategory.OST_StructuralColumns,BuiltInCategory.OST_StructuralFraming,BuiltInCategory.OST_Floors};
        if(doc.IsFamilyDocument||categories.Any(c=>new FilteredElementCollector(doc).OfCategory(c).WhereElementIsNotElementType().Any()))throw new InvalidOperationException("A cópia da base precisa estar vazia de pilares, vigas e pisos.");
        var cb=Base(doc,categories[0],"TCC-Pilar-Base");var bb=Base(doc,categories[1],"TCC-Viga-Base");
        var fb=new FilteredElementCollector(doc).OfClass(typeof(FloorType)).Cast<FloorType>().SingleOrDefault(s=>s.Name=="TCC-Laje-Base")??throw new InvalidOperationException("Tipo TCC-Laje-Base ausente.");
        if(fb.GetCompoundStructure()?.LayerCount!=1)throw new InvalidOperationException("A laje base deve ter uma camada.");
        var x=plan.SpanXM!.Value;var y=plan.SpanYM!.Value;var z0=plan.BaseZM!.Value;var z1=z0+plan.StoreyHeightM!.Value;var records=new List<CreatedElement>();var prefix="DEMO-"+runId[..8];
        var watch=Stopwatch.StartNew();
        using(var tx=new Transaction(doc,"Demonstração didática - 9 elementos"))
        {
            tx.Start();
            Level L(double z,string suffix){var level=Level.Create(doc,Ft(z));level.Name=prefix+suffix;return level;}
            var bottom=L(z0,"-BASE");var top=L(z1,"-TOPO");
            FamilySymbol Type(FamilySymbol source,double b,double h,string suffix){var type=(FamilySymbol)source.Duplicate(prefix+suffix);Dim(type,"b").Set(Ft(b));Dim(type,"h").Set(Ft(h));type.Activate();doc.Regenerate();if(Math.Abs(UnitUtils.ConvertFromInternalUnits(Dim(type,"b").AsDouble(),UnitTypeId.Meters)-b)>1e-8||Math.Abs(UnitUtils.ConvertFromInternalUnits(Dim(type,"h").AsDouble(),UnitTypeId.Meters)-h)>1e-8)throw new InvalidOperationException("Seção não aplicada.");return type;}
            var ct=Type(cb,plan.ColumnBM!.Value,plan.ColumnHM!.Value,"-P");var bt=Type(bb,plan.BeamBM!.Value,plan.BeamHM!.Value,"-V");
            void Record(Element e,string id,string kind,double? b,double h){e.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)?.Set(id);e.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)?.Set("DEMONSTRAÇÃO DIDÁTICA - NÃO DIMENSIONADO - NÃO EXECUTAR | "+runId);records.Add(new(id,e.Id.Value,e.UniqueId,kind,b,h));}
            var points=new[]{(0d,0d),(x,0d),(x,y),(0d,y)};
            for(int i=0;i<4;i++){var(px,py)=points[i];var c=doc.Create.NewFamilyInstance(new XYZ(Ft(px),Ft(py),Ft(z0)),ct,bottom,StructuralType.Column);Set(c,BuiltInParameter.FAMILY_TOP_LEVEL_PARAM,top.Id);Set(c,BuiltInParameter.FAMILY_BASE_LEVEL_OFFSET_PARAM,0.0);Set(c,BuiltInParameter.FAMILY_TOP_LEVEL_OFFSET_PARAM,0.0);Record(c,"DEMO-P"+(i+1),"column",plan.ColumnBM,plan.ColumnHM.Value);}
            for(int i=0;i<4;i++){var(ax,ay)=points[i];var(bx,by)=points[(i+1)%4];var line=Line.CreateBound(new XYZ(Ft(ax),Ft(ay),Ft(z1)),new XYZ(Ft(bx),Ft(by),Ft(z1)));var b=doc.Create.NewFamilyInstance(line,bt,top,StructuralType.Beam);Set(b,BuiltInParameter.YZ_JUSTIFICATION,0);Set(b,BuiltInParameter.Y_JUSTIFICATION,(int)YJustification.Center);Set(b,BuiltInParameter.Z_JUSTIFICATION,(int)ZJustification.Top);Set(b,BuiltInParameter.Y_OFFSET_VALUE,0.0);Set(b,BuiltInParameter.Z_OFFSET_VALUE,0.0);Record(b,"DEMO-V"+(i+1),"beam",plan.BeamBM,plan.BeamHM.Value);}
            var floorType=(FloorType)fb.Duplicate(prefix+"-L");var cs=floorType.GetCompoundStructure();cs.SetLayerWidth(0,Ft(plan.SlabHM!.Value));cs.StructuralMaterialIndex=0;floorType.SetCompoundStructure(cs);
            var loop=new CurveLoop();for(int i=0;i<4;i++){var(ax,ay)=points[i];var(bx,by)=points[(i+1)%4];loop.Append(Line.CreateBound(new XYZ(Ft(ax),Ft(ay),Ft(z1)),new XYZ(Ft(bx),Ft(by),Ft(z1))));}
            var slab=Floor.Create(doc,new List<CurveLoop>{loop},floorType.Id,top.Id,true,null,0);Set(slab,BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM,0.0);Record(slab,"DEMO-L1","slab",null,plan.SlabHM.Value);
            doc.Regenerate();if(records.Count!=9||categories.Select(c=>new FilteredElementCollector(doc).OfCategory(c).WhereElementIsNotElementType().GetElementCount()).Sum()!=9)throw new InvalidOperationException("Contagem de criação divergente.");
            if(tx.Commit()!=TransactionStatus.Committed)throw new InvalidOperationException("A transação de criação não concluiu.");
        }
        watch.Stop();View3D view;
        using(var tx=new Transaction(doc,"Vista 3D da demonstração"))
        {
            tx.Start();var type=new FilteredElementCollector(doc).OfClass(typeof(ViewFamilyType)).Cast<ViewFamilyType>().First(v=>v.ViewFamily==ViewFamily.ThreeDimensional);view=View3D.CreateIsometric(doc,type.Id);view.Name=prefix+" - 3D";view.DisplayStyle=DisplayStyle.Shading;view.DetailLevel=ViewDetailLevel.Medium;
            var levelCategory=new ElementId(BuiltInCategory.OST_Levels);if(view.CanCategoryBeHidden(levelCategory))view.SetCategoryHidden(levelCategory,true);
            var margin=1d;view.SetSectionBox(new BoundingBoxXYZ{Min=new XYZ(Ft(-margin),Ft(-margin),Ft(z0-margin)),Max=new XYZ(Ft(x+margin),Ft(y+margin),Ft(z1+margin))});view.IsSectionBoxActive=true;
            if(tx.Commit()!=TransactionStatus.Committed)throw new InvalidOperationException("Vista 3D não concluída.");
        }
        return new(view,watch.Elapsed.TotalSeconds,records);
    }
}

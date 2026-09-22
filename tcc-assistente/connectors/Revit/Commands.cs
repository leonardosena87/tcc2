using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace TccAssistente.Revit;

public class App : IExternalApplication
{
    public Result OnStartup(UIControlledApplication app)
    {
        var panel = app.CreateRibbonPanel("TCC Assistente");
        panel.AddItem(new PushButtonData("TccExport", "Exportar para\no TCC", typeof(App).Assembly.Location, typeof(ExportSelection).FullName!));
        return Result.Succeeded;
    }
    public Result OnShutdown(UIControlledApplication app) => Result.Succeeded;
}

[Transaction(TransactionMode.ReadOnly)]
public class ExportSelection : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        var ui = commandData.Application.ActiveUIDocument;
        if (ui == null) { TaskDialog.Show("TCC Assistente", "Abra um modelo e selecione os elementos para exportar."); return Result.Cancelled; }
        var ids = ui.Selection.GetElementIds();
        if (ids.Count == 0 || ids.Count > 2000) { TaskDialog.Show("TCC Assistente", "Selecione de 1 a 2.000 elementos do modelo e execute novamente."); return Result.Cancelled; }
        try
        {
            var rows = new List<object>();
            foreach (var id in ids)
            {
                var e = ui.Document.GetElement(id);
                if (e == null) continue;
                var type = ui.Document.GetElement(e.GetTypeId());
                rows.Add(new {
                    id = e.Id.Value.ToString(), uniqueId = e.UniqueId,
                    category = e.Category?.Name ?? "Sem categoria", name = e.Name,
                    type = type?.Name, level = ui.Document.GetElement(e.LevelId)?.Name,
                    lengthM = Measurement(e, BuiltInParameter.CURVE_ELEM_LENGTH, UnitTypeId.Meters),
                    areaM2 = Measurement(e, BuiltInParameter.HOST_AREA_COMPUTED, UnitTypeId.SquareMeters),
                    volumeM3 = Measurement(e, BuiltInParameter.HOST_VOLUME_COMPUTED, UnitTypeId.CubicMeters),
                    roomAreaM2 = Measurement(e, BuiltInParameter.ROOM_AREA, UnitTypeId.SquareMeters),
                    roomVolumeM3 = Measurement(e, BuiltInParameter.ROOM_VOLUME, UnitTypeId.CubicMeters)
                });
            }
            var filename = Export.Write("Revit", ui.Document.Title, "Comprimentos em m; áreas em m²; volumes em m³. Valores ausentes são null, não zero. Somente parâmetros disponíveis nos elementos selecionados. Modelos vinculados não são percorridos.", rows);
            TaskDialog.Show("TCC Assistente", $"{rows.Count} elementos exportados.\nNo Word, use Dados do Revit e AutoCAD > Atualizar exportações.\n\n{filename}");
            return Result.Succeeded;
        }
        catch (Exception e) { message = e.Message; return Result.Failed; }
    }
    private static double? Measurement(Element element, BuiltInParameter parameter, ForgeTypeId unit)
    {
        var value = element.get_Parameter(parameter);
        if (value == null || !value.HasValue || value.StorageType != StorageType.Double) return null;
        var number = UnitUtils.ConvertFromInternalUnits(value.AsDouble(), unit);
        return double.IsFinite(number) ? Math.Round(number, 6) : null;
    }
}

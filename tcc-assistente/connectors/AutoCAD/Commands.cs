using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.Runtime;
using AcApp = Autodesk.AutoCAD.ApplicationServices.Core.Application;

[assembly: CommandClass(typeof(TccAssistente.AutoCAD.Commands))]
namespace TccAssistente.AutoCAD;
public class Commands
{
    [CommandMethod("TCCEXPORTAR", CommandFlags.Modal | CommandFlags.UsePickSet)]
    public void ExportSelection()
    {
        Document? doc = AcApp.DocumentManager.MdiActiveDocument;
        if (doc == null) return;
        var selection = doc.Editor.SelectImplied();
        if (selection.Status != PromptStatus.OK) selection = doc.Editor.GetSelection(new PromptSelectionOptions { MessageForAdding = "\nSelecione os elementos para o TCC: " });
        if (selection.Status != PromptStatus.OK) return;
        if (selection.Value.Count > 2000) { doc.Editor.WriteMessage("\nSelecione no máximo 2.000 elementos."); return; }
        try
        {
            using var transaction = doc.Database.TransactionManager.StartTransaction();
            var rows = new List<object>();
            foreach (var id in selection.Value.GetObjectIds())
            {
                if (transaction.GetObject(id, OpenMode.ForRead) is not Entity entity) continue;
                double? length = null, area = null;
                string? measurementNote = null;
                if (entity is Curve curve)
                {
                    try { length = curve.GetDistanceAtParameter(curve.EndParam) - curve.GetDistanceAtParameter(curve.StartParam); }
                    catch (Autodesk.AutoCAD.Runtime.Exception) { measurementNote = "Comprimento indisponível."; }
                    if (curve.Closed) { try { area = curve.Area; } catch (Autodesk.AutoCAD.Runtime.Exception) { measurementNote = "Área indisponível."; } }
                }
                if (entity is Hatch hatch) { try { area = hatch.Area; } catch (Autodesk.AutoCAD.Runtime.Exception) { measurementNote = "Área de hachura indisponível."; } }
                rows.Add(new { id = entity.Handle.ToString(), category = entity.GetRXClass().DxfName, layer = entity.Layer,
                    text = entity is DBText text ? text.TextString : entity is MText mtext ? mtext.Text : null,
                    block = entity is BlockReference block ? ((BlockTableRecord)transaction.GetObject(block.IsDynamicBlock ? block.DynamicBlockTableRecord : block.BlockTableRecord, OpenMode.ForRead)).Name : null,
                    lengthDrawingUnits = Finite(length), areaDrawingUnits2 = Finite(area), measurementNote });
            }
            var filename = Export.Write("AutoCAD", Path.GetFileName(doc.Name), $"INSUNITS={doc.Database.Insunits}. Medidas em unidades de desenho e unidades de desenho ao quadrado; não convertidas. INSUNITS é metadado, confirme a escala efetiva. Blocos não são explodidos. Curvas abertas não têm área exportada.", rows);
            doc.Editor.WriteMessage($"\n{rows.Count} elementos exportados para o TCC. No Word, atualize as exportações.\n{filename}\n");
        }
        catch (System.Exception e) { doc.Editor.WriteMessage($"\nFalha ao exportar: {e.Message}\n"); }
    }
    private static double? Finite(double? value) => value.HasValue && double.IsFinite(value.Value) ? Math.Round(value.Value, 6) : null;
}

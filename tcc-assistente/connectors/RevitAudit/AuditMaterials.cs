using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System.Diagnostics;
using System.Globalization;
using System.Text.Json;

namespace TccAssistente.RevitAudit;

// No Transaction, material assignment, native save, HTTP request or inference.
[Transaction(TransactionMode.ReadOnly)]
public class AuditMaterials : IExternalCommand
{
    private sealed record NumberReading(double? Raw, double? Converted, string Status, string? Error = null);
    private sealed record VectorReading(double[]? Raw, double[]? Converted, string Status, string? Error = null);
    private static readonly JsonSerializerOptions JsonOptions = new() { WriteIndented = true, PropertyNamingPolicy = JsonNamingPolicy.CamelCase };

    private static NumberReading Number(Func<double> get, ForgeTypeId unit)
    {
        try
        {
            var raw = get();
            var converted = UnitUtils.ConvertFromInternalUnits(raw, unit);
            return double.IsFinite(raw) && double.IsFinite(converted)
                ? new(raw, converted, "read") : new(null, null, "non_finite");
        }
        catch (Exception ex) { return new(null, null, "unavailable", ex.GetType().Name + ": " + ex.Message); }
    }

    private static VectorReading Vector(Func<XYZ> get, ForgeTypeId? unit)
    {
        try
        {
            var v = get();
            var raw = new[] { v.X, v.Y, v.Z };
            var converted = unit is null ? raw.ToArray() : raw.Select(x => UnitUtils.ConvertFromInternalUnits(x, unit)).ToArray();
            return raw.All(double.IsFinite) && converted.All(double.IsFinite)
                ? new(raw, converted, "read") : new(null, null, "non_finite");
        }
        catch (Exception ex) { return new(null, null, "unavailable", ex.GetType().Name + ": " + ex.Message); }
    }

    private static long? Id(ElementId? id) => id is not null && id.Value > 0 ? id.Value : null;
    private static string IdText(long id) => id.ToString(CultureInfo.InvariantCulture);

    private static object ReadMaterial(Document doc, long id)
    {
        if (doc.GetElement(new ElementId(id)) is not Material m)
            return new { id = IdText(id), status = "material_not_found" };
        var ps = doc.GetElement(m.StructuralAssetId) as PropertySetElement;
        object? assetData = null;
        string status = "structural_asset_absent";
        string? error = null;
        if (ps is not null)
        {
            try
            {
                using var asset = ps.GetStructuralAsset();
                assetData = new
                {
                    id = IdText(ps.Id.Value), uniqueId = ps.UniqueId, ps.Name,
                    @class = asset.StructuralAssetClass.ToString(), behavior = asset.Behavior.ToString(),
                    density = Number(() => asset.Density, UnitTypeId.KilogramsPerCubicMeter),
                    densityRawUnit = "kg/ft3", densityConvertedUnit = "kg/m3",
                    concreteCompression = asset.StructuralAssetClass == StructuralAssetClass.Concrete
                        ? Number(() => asset.ConcreteCompression, UnitTypeId.Megapascals) : null,
                    compressionRawUnit = "N/(ft*m)", compressionConvertedUnit = "MPa",
                    compressionInterpretation = "API concrete compression strength; not automatically the adopted NBR fck",
                    youngModulus = Vector(() => asset.YoungModulus, UnitTypeId.Megapascals),
                    youngModulusRawUnit = "N/(ft*m)", youngModulusConvertedUnit = "MPa",
                    youngModulusInterpretation = "API XYZ components; not automatically NBR Eci or Ecs",
                    poissonRatio = Vector(() => asset.PoissonRatio, null), poissonUnit = "dimensionless"
                };
                status = "asset_read";
            }
            catch (Exception ex) { status = "asset_unavailable"; error = ex.GetType().Name + ": " + ex.Message; }
        }
        return new { id = IdText(id), uniqueId = m.UniqueId, m.Name, m.MaterialClass, structuralAssetId = Id(m.StructuralAssetId)?.ToString(CultureInfo.InvariantCulture), status, error, asset = assetData };
    }

    private static object ReadElement(Document doc, Element e, HashSet<long> materials)
    {
        long? structuralMaterialId = null;
        string assignmentStatus = "not_resolved";
        string? assignmentError = null;
        object? floorLayers = null;
        try
        {
            if (e is FamilyInstance family)
            {
                structuralMaterialId = Id(family.StructuralMaterialId);
                assignmentStatus = structuralMaterialId.HasValue ? "FamilyInstance.StructuralMaterialId" : "family_structural_material_unassigned";
            }
            else if (e is Floor && doc.GetElement(e.GetTypeId()) is FloorType floorType)
            {
                var structure = floorType.GetCompoundStructure();
                if (structure is not null)
                {
                    var layers = structure.GetLayers();
                    var index = structure.StructuralMaterialIndex;
                    if (index >= 0 && index < layers.Count) structuralMaterialId = Id(layers[index].MaterialId);
                    floorLayers = layers.Select((layer, i) => new {
                        index = i, structural = i == index, materialId = Id(layer.MaterialId)?.ToString(CultureInfo.InvariantCulture), rawMaterialId = IdText(layer.MaterialId.Value),
                        widthM = UnitUtils.ConvertFromInternalUnits(layer.Width, UnitTypeId.Meters), function = layer.Function.ToString()
                    }).ToArray();
                    foreach (var layer in layers) if (Id(layer.MaterialId) is long layerId) materials.Add(layerId);
                    assignmentStatus = structuralMaterialId.HasValue ? "FloorType.CompoundStructure.StructuralMaterialIndex" : "floor_structural_layer_or_material_unassigned";
                }
                else assignmentStatus = "floor_compound_structure_absent";
            }
        }
        catch (Exception ex) { assignmentStatus = "assignment_unavailable"; assignmentError = ex.GetType().Name + ": " + ex.Message; }
        if (structuralMaterialId is long materialId) materials.Add(materialId);
        long[]? geometryMaterialIds = null;
        string? geometryMaterialsError = null;
        try
        {
            geometryMaterialIds = e.GetMaterialIds(false).Select(x => x.Value).Where(x => x > 0).Distinct().Order().ToArray();
            foreach (var gid in geometryMaterialIds) materials.Add(gid);
        }
        catch (Exception ex) { geometryMaterialsError = ex.GetType().Name + ": " + ex.Message; }
        return new
        {
            id = IdText(e.Id.Value), uniqueId = e.UniqueId, category = e.Category?.Name, categoryId = e.Category?.Id.Value.ToString(CultureInfo.InvariantCulture),
            e.Name, typeId = Id(e.GetTypeId())?.ToString(CultureInfo.InvariantCulture), typeName = doc.GetElement(e.GetTypeId())?.Name,
            structuralMaterialId = structuralMaterialId?.ToString(CultureInfo.InvariantCulture), assignmentStatus, assignmentError, floorLayers,
            geometryMaterialIds = geometryMaterialIds?.Select(IdText).ToArray(), geometryMaterialsError,
            geometryMaterialIdsAreNotAssumedToBeStructuralAssignment = true
        };
    }

    public Result Execute(ExternalCommandData data, ref string message, ElementSet errors)
    {
        var ui = data.Application.ActiveUIDocument;
        if (ui is null) { TaskDialog.Show("TCC - materiais", "Abra o arquivo do estudo antes de executar a auditoria."); return Result.Cancelled; }
        try
        {
            var start = DateTimeOffset.UtcNow;
            var clock = Stopwatch.StartNew();
            var doc = ui.Document;
            var modifiedBefore = doc.IsModified;
            var categories = new[] { BuiltInCategory.OST_StructuralColumns, BuiltInCategory.OST_StructuralFraming, BuiltInCategory.OST_Floors };
            var filter = new LogicalOrFilter(categories.Select(c => (ElementFilter)new ElementCategoryFilter(c)).ToList());
            var native = new FilteredElementCollector(doc).WhereElementIsNotElementType().WherePasses(filter).OrderBy(e => e.Id.Value).ToArray();
            if (native.Length == 0 || native.Length > 2000)
            { TaskDialog.Show("TCC - materiais", "O modelo deve conter entre 1 e 2.000 candidatos de pilares estruturais, estruturas ou pisos. Nenhum arquivo foi exportado."); return Result.Cancelled; }
            var materialIds = new HashSet<long>();
            var rows = native.Select(e => ReadElement(doc, e, materialIds)).ToArray();
            var materials = materialIds.Order().Select(id => ReadMaterial(doc, id)).ToArray();
            var modifiedAfter = doc.IsModified;
            if (modifiedBefore != modifiedAfter) throw new InvalidOperationException("O estado de modificacao do documento mudou durante a leitura. A auditoria deve ser repetida.");
            clock.Stop();
            var result = new
            {
                schema = "tcc-revit-material-audit/1", status = "native_read_with_explicit_limits",
                startedAtUtc = start, endedAtUtc = DateTimeOffset.UtcNow, auditReadMs = clock.Elapsed.TotalMilliseconds,
                revit = new { version = data.Application.Application.VersionNumber, build = data.Application.Application.VersionBuild },
                document = new { doc.Title, doc.PathName, modifiedBefore, modifiedAfter },
                scope = "Current document only; all non-type structural columns, structural framing and floors. Floor structural role must be interpreted; linked models are not traversed.",
                count = rows.Length, elements = rows, materials,
                nativeDocumentSaved = false, transactionsStarted = 0, inferenceCalls = 0,
                sourceMappingCompleted = false, transferLossProven = false,
                ca50MechanicalPropertiesVerified = false, structuralApproval = false, flowTotalTime = false,
                limits = new[] {
                    "Element UniqueIds must be matched to the authoring mapping before comparing the 62 source units.",
                    "A named material does not prove physical properties or transfer. Missing data remain null with status.",
                    "Concrete compression and Young modulus are API properties, not automatic interpretations as NBR fck/Eci/Ecs.",
                    "No loads, supports, analytical connections, cover, reinforcement or ELU/ELS have been checked.",
                    "The recorded time covers this native read only, not the complete authoring/interchange workflow."
                }
            };
            var folder = Path.Combine("D:\\TCC\\outputs", "Propriedades-Revit-" + start.ToString("yyyyMMdd-HHmmss-fff") + "-" + Guid.NewGuid().ToString("N")[..8]);
            Directory.CreateDirectory(folder);
            var file = Path.Combine(folder, "materiais-revit.json");
            using (var stream = new FileStream(file, FileMode.CreateNew, FileAccess.Write, FileShare.Read))
                JsonSerializer.Serialize(stream, result, JsonOptions);
            TaskDialog.Show("TCC - materiais", $"Leitura de {rows.Length} candidatos concluida. Sem alterar ou salvar o modelo.\n\n{file}\n\nO resultado precisa ser associado aos IDs da autoria; nao constitui verificacao estrutural.");
            return Result.Succeeded;
        }
        catch (Exception ex) { message = ex.GetType().Name + ": " + ex.Message; return Result.Failed; }
    }
}

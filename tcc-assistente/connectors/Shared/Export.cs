using System;
using System.IO;
using System.Text.Json;
using System.Collections.Generic;

namespace TccAssistente;
public static class Export
{
    public static string Write(string application, string document, string units, List<object> elements)
    {
        var directory = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "TccAssistente", "exports");
        Directory.CreateDirectory(directory);
        var filename = Path.Combine(directory, $"{application.ToLowerInvariant()}-{DateTime.UtcNow:yyyyMMdd-HHmmss}-{Guid.NewGuid():N}.json");
        var data = new { schemaVersion = 1, application, document, exportedAt = DateTime.UtcNow.ToString("O"), scope = "selection", units, elements };
        var json = JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true });
        if (System.Text.Encoding.UTF8.GetByteCount(json) > 1000000)
            throw new InvalidOperationException("Seleção excede 1 MB. Selecione menos elementos e exporte novamente.");
        var temporary = filename + ".tmp";
        File.WriteAllText(temporary, json, new System.Text.UTF8Encoding(false));
        File.Move(temporary, filename);
        return filename;
    }
}

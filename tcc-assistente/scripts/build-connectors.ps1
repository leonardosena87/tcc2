param([string]$RevitDir = 'C:\Program Files\Autodesk\Revit 2027', [string]$AutoCADDir = 'D:\AutoCAD 2027')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
& dotnet build (Join-Path $projectRoot 'connectors/Revit/TccAssistente.Revit.csproj') -c Release "-p:RevitDir=$RevitDir" --nologo
if ($LASTEXITCODE -ne 0) { throw 'Falha na compilação do conector Revit.' }
& dotnet build (Join-Path $projectRoot 'connectors/AutoCAD/TccAssistente.AutoCAD.csproj') -c Release "-p:AutoCADDir=$AutoCADDir" --nologo
if ($LASTEXITCODE -ne 0) { throw 'Falha na compilação do conector AutoCAD.' }

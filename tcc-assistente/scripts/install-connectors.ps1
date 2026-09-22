$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$installRoot = Join-Path $env:LOCALAPPDATA 'TccAssistente/connectors'
$revitSource = Join-Path $projectRoot 'connectors/Revit/bin/Release/net10.0-windows/TccAssistente.Revit.dll'
$acadSource = Join-Path $projectRoot 'connectors/AutoCAD/bin/Release/net10.0-windows/TccAssistente.AutoCAD.dll'
if (!(Test-Path -LiteralPath $revitSource) -or !(Test-Path -LiteralPath $acadSource)) { throw 'Compile os conectores primeiro: scripts/build-connectors.ps1' }
New-Item -ItemType Directory -Force -Path $installRoot | Out-Null
Copy-Item -LiteralPath $revitSource -Destination $installRoot -Force
Copy-Item -LiteralPath $acadSource -Destination $installRoot -Force
$revitAddins = Join-Path $env:APPDATA 'Autodesk/Revit/Addins/2027'
New-Item -ItemType Directory -Force -Path $revitAddins | Out-Null
$assemblyPath = [System.Security.SecurityElement]::Escape((Join-Path $installRoot 'TccAssistente.Revit.dll'))
$manifest = @"
<?xml version="1.0" encoding="utf-8"?>
<RevitAddIns><AddIn Type="Application"><Name>TCC Assistente</Name><Assembly>$assemblyPath</Assembly><AddInId>6CE69B22-D64C-4A8B-A0CE-A58D17E35C04</AddInId><FullClassName>TccAssistente.Revit.App</FullClassName><VendorId>TCCA</VendorId><VendorDescription>Assistente local para TCC</VendorDescription></AddIn></RevitAddIns>
"@
[IO.File]::WriteAllText((Join-Path $revitAddins 'TccAssistente.addin'), $manifest, [Text.UTF8Encoding]::new($false))
Write-Host 'Conector Revit instalado. Ele será carregado na próxima abertura do Revit.'
Write-Host 'No AutoCAD, use NETLOAD e escolha:'
Write-Host (Join-Path $installRoot 'TccAssistente.AutoCAD.dll')
Write-Host 'Depois execute TCCEXPORTAR. A primeira carga pode pedir confirmação de confiança do AutoCAD.'

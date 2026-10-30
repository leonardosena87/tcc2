param(
    [string]$BasePath='D:\TCC\palestra-IA-engenharia\demonstracao\DEMO-AO-VIVO-BASE-VAZIA.rvt',
    [string]$OutputRoot='D:\TCC\palestra-IA-engenharia\demonstracao'
)
$ErrorActionPreference='Stop'
$source=Join-Path $PSScriptRoot 'bin\Release\net10.0-windows\TccAssistente.RevitDemo.dll'
if (!(Test-Path -LiteralPath $source)) {throw 'Compile TccAssistente.RevitDemo.csproj antes de instalar.'}
if (!(Test-Path -LiteralPath $BasePath)) {throw 'Base vazia da palestra ausente.'}
if (Get-Process Revit -ErrorAction SilentlyContinue) {throw 'Feche o Revit antes de instalar. Os documentos precisam estar salvos.'}
$installRoot=Join-Path $env:LOCALAPPDATA 'TccAssistente\revit-demo'
$addins=Join-Path $env:APPDATA 'Autodesk\Revit\Addins\2027'
New-Item -ItemType Directory -Force -Path $installRoot,$addins,$OutputRoot | Out-Null
$backup=Join-Path $env:LOCALAPPDATA ('TccAssistente\backups\revit-demo-'+(Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Force -Path $backup | Out-Null
$manifest=Join-Path $addins 'TccAssistente.Demo.addin'
foreach ($name in @('TccAssistente.RevitDemo.dll','DEMO-BASE.rvt','demo.config.json')) {
    $existing=Join-Path $installRoot $name
    if (Test-Path -LiteralPath $existing) {Copy-Item -LiteralPath $existing -Destination $backup}
}
if (Test-Path -LiteralPath $manifest) {Copy-Item -LiteralPath $manifest -Destination $backup}
$dll=Join-Path $installRoot 'TccAssistente.RevitDemo.dll'
$installedBase=Join-Path $installRoot 'DEMO-BASE.rvt'
Copy-Item -LiteralPath $source -Destination $dll -Force
Copy-Item -LiteralPath $BasePath -Destination $installedBase -Force
$settings=@{basePath=$installedBase;baseSha256=(Get-FileHash -LiteralPath $installedBase -Algorithm SHA256).Hash;outputRoot=[IO.Path]::GetFullPath($OutputRoot)}
[IO.File]::WriteAllText((Join-Path $installRoot 'demo.config.json'),($settings | ConvertTo-Json),[Text.UTF8Encoding]::new($false))
$escaped=[Security.SecurityElement]::Escape($dll)
$xml=@"
<?xml version="1.0" encoding="utf-8"?>
<RevitAddIns><AddIn Type="Application"><Name>TCC Demonstração IA</Name><Assembly>$escaped</Assembly><AddInId>5E4E4C0A-4DA3-4D5C-A918-A3467456A243</AddInId><FullClassName>TccAssistente.RevitDemo.App</FullClassName><VendorId>TCCA</VendorId><VendorDescription>Demonstração didática de modelagem</VendorDescription></AddIn></RevitAddIns>
"@
[IO.File]::WriteAllText($manifest,$xml,[Text.UTF8Encoding]::new($false))
Write-Host 'Complemento separado instalado. O complemento TCC Assistente anterior foi preservado.'
Write-Host 'Abra o Revit e confira Complementos > IA - Palestra TCC > Demonstração IA.'
Write-Host 'A instalação não comprova a execução dentro do Revit.'

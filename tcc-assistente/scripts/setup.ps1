$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Push-Location $projectRoot
try {
    if (!(Get-Command node.exe -ErrorAction SilentlyContinue)) { throw 'Instale Node.js 22 ou superior antes de continuar.' }
    & npm.cmd ci --no-audit --no-fund
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar dependencias.' }
    & npm.cmd run certs
    if ($LASTEXITCODE -ne 0) { throw 'Certificado local nao instalado. Confirme a solicitacao do Windows e tente novamente.' }
    & npm.cmd run register
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao registrar o suplemento no Word.' }
    & (Join-Path $PSScriptRoot 'start.ps1')
    & npx.cmd office-addin-dev-settings sideload manifest.xml desktop --app Word
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao abrir o suplemento. Consulte LEIA-ME.md.' }
} finally { Pop-Location }

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$runtimeRoot = Join-Path $env:LOCALAPPDATA 'TccAssistente/runtime'
New-Item -ItemType Directory -Path $runtimeRoot -Force | Out-Null
$existing = Get-NetTCPConnection -LocalPort 3443 -State Listen -ErrorAction SilentlyContinue
if ($existing) { Write-Host 'Já há um serviço na porta 3443. Abra o painel TCC Assistente no Word.'; exit 0 }
$nodePath = (Get-Command node.exe).Source
$serverPath = Join-Path $projectRoot 'server/main.mjs'
$credentialDir = Join-Path $env:LOCALAPPDATA 'TccAssistente/credentials'
$credentialFile = Join-Path $credentialDir 'openai.xml'
$previousKey = $env:OPENAI_API_KEY
$previousModel = $env:OPENAI_MODEL
try {
if (Test-Path -LiteralPath $credentialFile) {
    $secure = Import-Clixml -LiteralPath $credentialFile
    $env:OPENAI_API_KEY = [System.Net.NetworkCredential]::new('', $secure).Password
    $settings = Get-Content -LiteralPath (Join-Path $credentialDir 'settings.json') -Raw | ConvertFrom-Json
    $env:OPENAI_MODEL = $settings.model
}
$serverProcess = Start-Process -FilePath $nodePath -ArgumentList @('"' + $serverPath + '"') -WorkingDirectory $projectRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runtimeRoot 'server.log') -RedirectStandardError (Join-Path $runtimeRoot 'error.log') -PassThru
} finally {
    $env:OPENAI_API_KEY = $previousKey
    $env:OPENAI_MODEL = $previousModel
}
Start-Sleep -Seconds 2
$serverProcess.Refresh()
if ($serverProcess.HasExited) { throw ('Falha ao iniciar. Consulte ' + (Join-Path $runtimeRoot 'error.log')) }
$serverProcess.Id | Set-Content (Join-Path $runtimeRoot 'server.pid')
Write-Host 'TCC Assistente iniciado. Abra o suplemento no Word.'

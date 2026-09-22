$ErrorActionPreference = 'Stop'
$pidPath = Join-Path $env:LOCALAPPDATA 'TccAssistente/runtime/server.pid'
if (!(Test-Path -LiteralPath $pidPath)) { Write-Host 'Nenhum processo registrado.'; exit 0 }
$serverId = [int](Get-Content -LiteralPath $pidPath)
$serverProcess = Get-CimInstance Win32_Process -Filter "ProcessId = $serverId"
$expectedScript = Join-Path (Split-Path $PSScriptRoot -Parent) 'server/main.mjs'
if ($serverProcess -and $serverProcess.Name -eq 'node.exe' -and $serverProcess.CommandLine.Contains($expectedScript)) { Stop-Process -Id $serverId; Write-Host 'Assistente encerrado. A chave em memória foi removida.' } else { Write-Host 'O processo registrado já foi encerrado ou não pertence a este assistente.' }

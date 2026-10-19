$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).ProviderPath
$startScript = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot 'start.ps1')).ProviderPath
$powershellPath = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
if (!(Test-Path -LiteralPath $powershellPath -PathType Leaf)) { throw 'Windows PowerShell nao encontrado.' }

$taskName = 'TCC Assistente - iniciar serviço'
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    $backupRoot = Join-Path $env:LOCALAPPDATA 'TccAssistente\backups'
    New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
    $backupPath = Join-Path $backupRoot ('startup-task.' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '.xml')
    Export-ScheduledTask -TaskName $taskName | Set-Content -LiteralPath $backupPath -Encoding Unicode
}

$identity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$action = New-ScheduledTaskAction -Execute $powershellPath -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$startScript`"" -WorkingDirectory $projectRoot
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $identity
$principal = New-ScheduledTaskPrincipal -UserId $identity -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description 'Inicia o servidor local do TCC Assistente ao entrar no Windows.' -Force | Out-Null
Write-Host 'Inicio automatico configurado para esta pasta do projeto.'

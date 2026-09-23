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
    $identity = "$env:USERDOMAIN\$env:USERNAME"
    $startScript = Join-Path $PSScriptRoot 'start.ps1'
    $action = New-ScheduledTaskAction -Execute "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$startScript`"" -WorkingDirectory $projectRoot
    $trigger = New-ScheduledTaskTrigger -AtLogOn -User $identity
    $principal = New-ScheduledTaskPrincipal -UserId $identity -LogonType Interactive -RunLevel Limited
    Register-ScheduledTask -TaskName 'TCC Assistente - iniciar serviço' -Action $action -Trigger $trigger -Principal $principal -Description 'Inicia o servidor local do TCC Assistente ao entrar no Windows.' -Force | Out-Null
    & (Join-Path $PSScriptRoot 'start.ps1')
    & npx.cmd office-addin-dev-settings sideload manifest.xml desktop --app Word
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao abrir o suplemento. Consulte LEIA-ME.md.' }
} finally { Pop-Location }

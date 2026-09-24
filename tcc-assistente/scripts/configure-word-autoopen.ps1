param([ValidateSet('enable','disable')][string]$Action='enable')
$ErrorActionPreference = 'Stop'
$normalPath = Join-Path $env:APPDATA 'Microsoft\Templates\Normal.dotm'

if (Get-Process -Name WINWORD -ErrorAction SilentlyContinue) {
    Write-Error 'Salve seus documentos e feche todas as janelas do Word. Depois execute este comando novamente.'
}
if (!(Test-Path -LiteralPath $normalPath -PathType Leaf)) {
    Write-Error "Não encontrei o modelo padrão do Word: $normalPath"
}
$nodePath = (Get-Command node.exe -ErrorAction Stop).Source
$backupRoot = Join-Path $env:LOCALAPPDATA 'TccAssistente\backups'
New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
$backupPath = Join-Path $backupRoot "Normal.$stamp.dotm.bak"
$stagedPath = Join-Path (Split-Path $normalPath -Parent) "Normal.$stamp.tcc-assistente.tmp"
$toolPath = Join-Path $PSScriptRoot 'word-autoopen-template.mjs'

try {
    & $nodePath $toolPath $Action $normalPath $stagedPath
    if ($LASTEXITCODE -ne 0) { throw 'A configuração do modelo do Word falhou; o Normal.dotm original foi preservado.' }
    [System.IO.File]::Replace($stagedPath, $normalPath, $backupPath, $true)
    if ($Action -eq 'enable') {
        Write-Host 'Concluído. Os novos documentos em branco do Word abrirão o TCC Assistente automaticamente.'
    } else {
        Write-Host 'Concluído. Os novos documentos em branco do Word não abrirão mais o TCC Assistente automaticamente.'
    }
    Write-Host "Cópia de segurança: $backupPath"
} finally {
    if (Test-Path -LiteralPath $stagedPath) { Remove-Item -LiteralPath $stagedPath -Force }
}

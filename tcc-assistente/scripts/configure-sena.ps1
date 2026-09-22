$ErrorActionPreference = 'Stop'
$credentialDir = Join-Path $env:LOCALAPPDATA 'TccAssistente/credentials'
New-Item -ItemType Directory -Path $credentialDir -Force | Out-Null
# Capture secret output in memory only. Never print the CLI result.
$secretOutput = & firebase.cmd functions:secrets:access OPENAI_API_KEY --project senaimoveisvca-d8b7e --non-interactive 2>$null
if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel acessar a credencial OpenAI do projeto Sena com a sessao Firebase atual.' }
$secret = ($secretOutput -join "`n").Trim()
if ($secret -notmatch '^sk-[\x21-\x7E]+$') { throw 'A credencial retornada nao tem o formato esperado. Nenhum valor foi salvo.' }
$secure = ConvertTo-SecureString $secret -AsPlainText -Force
$secure | Export-Clixml -LiteralPath (Join-Path $credentialDir 'openai.xml')
[IO.File]::WriteAllText((Join-Path $credentialDir 'settings.json'), '{"model":"gpt-5.6-sol","source":"Sena Imoveis"}')
$secret = $null
$secretOutput = $null
Write-Host 'Credencial do projeto Sena configurada e protegida pelo Windows para este usuario.'

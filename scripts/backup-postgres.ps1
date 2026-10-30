param(
    [string]$BackupDirectory = (Join-Path $PSScriptRoot "..\backups")
)

$ErrorActionPreference = "Stop"
if ($PSVersionTable.PSVersion.Major -lt 7) {
    throw "El respaldo binario requiere PowerShell 7 o superior."
}

$backupRoot = [System.IO.Path]::GetFullPath($BackupDirectory)
New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupPath = Join-Path $backupRoot "cibersegura-$timestamp.dump"

$databaseUser = (& docker compose exec -T db printenv POSTGRES_USER).Trim()
$databaseName = (& docker compose exec -T db printenv POSTGRES_DB).Trim()
if ($LASTEXITCODE -ne 0 -or -not $databaseUser -or -not $databaseName) {
    throw "No se pudo consultar la configuración del contenedor PostgreSQL."
}

& docker compose exec -T db pg_dump `
    --username=$databaseUser `
    --dbname=$databaseName `
    --format=custom `
    --no-owner `
    --no-acl > $backupPath
if ($LASTEXITCODE -ne 0) {
    throw "pg_dump no pudo crear el respaldo."
}

$hash = (Get-FileHash -LiteralPath $backupPath -Algorithm SHA256).Hash.ToLowerInvariant()
"$hash  $([System.IO.Path]::GetFileName($backupPath))" |
    Set-Content -LiteralPath "$backupPath.sha256" -Encoding ascii

Write-Host "Respaldo creado: $backupPath"
Write-Host "Integridad SHA-256: $hash"

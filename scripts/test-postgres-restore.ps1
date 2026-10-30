param(
    [Parameter(Mandatory = $true)]
    [string]$BackupPath
)

$ErrorActionPreference = "Stop"
$resolvedBackup = (Resolve-Path -LiteralPath $BackupPath).Path
$checksumPath = "$resolvedBackup.sha256"
if (-not (Test-Path -LiteralPath $checksumPath -PathType Leaf)) {
    throw "Falta el archivo de integridad: $checksumPath"
}

$expectedHash = ((Get-Content -LiteralPath $checksumPath -Raw).Trim() -split "\s+")[0]
$actualHash = (Get-FileHash -LiteralPath $resolvedBackup -Algorithm SHA256).Hash.ToLowerInvariant()
if ($expectedHash -ne $actualHash) {
    throw "El respaldo no coincide con su checksum SHA-256."
}

$databaseUser = (& docker compose exec -T db printenv POSTGRES_USER).Trim()
$temporaryDatabase = "cibersegura_restore_check_$PID"
if ($temporaryDatabase -notmatch '^cibersegura_restore_check_[0-9]+$') {
    throw "El nombre de la base temporal no es seguro."
}
$containerBackup = "/tmp/$([System.IO.Path]::GetFileName($resolvedBackup))"

try {
    & docker compose cp $resolvedBackup "db:$containerBackup"
    if ($LASTEXITCODE -ne 0) { throw "No se pudo copiar el respaldo al contenedor." }

    & docker compose exec -T db createdb --username=$databaseUser $temporaryDatabase
    if ($LASTEXITCODE -ne 0) { throw "No se pudo crear la base temporal." }

    & docker compose exec -T db pg_restore --username=$databaseUser --dbname=$temporaryDatabase --exit-on-error $containerBackup
    if ($LASTEXITCODE -ne 0) { throw "La restauración de comprobación falló." }

    $migrationCount = (& docker compose exec -T db psql --username=$databaseUser --dbname=$temporaryDatabase --tuples-only --no-align --command="SELECT COUNT(*) FROM django_migrations;").Trim()
    if ($LASTEXITCODE -ne 0 -or [int]$migrationCount -lt 1) {
        throw "La base restaurada no contiene migraciones verificables."
    }
    Write-Host "Restauración comprobada en una base temporal ($migrationCount migraciones)."
}
finally {
    & docker compose exec -T db dropdb --username=$databaseUser --if-exists $temporaryDatabase | Out-Null
    & docker compose exec -T db rm -f -- $containerBackup | Out-Null
}

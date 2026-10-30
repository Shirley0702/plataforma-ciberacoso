$ErrorActionPreference = "Stop"

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Command,
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "El comando '$Command $($Arguments -join ' ')' terminó con código $LASTEXITCODE."
    }
}

Write-Host "[1/5] Validando la configuración de Docker Compose..."
Invoke-Checked docker compose config --quiet

Write-Host "[2/5] Construyendo imágenes reproducibles..."
Invoke-Checked docker compose build

Write-Host "[3/5] Comprobando configuración y migraciones..."
Invoke-Checked docker compose run --rm backend python manage.py makemigrations --check --dry-run

Write-Host "[4/5] Ejecutando pruebas backend con PostgreSQL..."
Invoke-Checked docker compose run --rm backend python manage.py test

Write-Host "[5/5] Validando pruebas y compilación frontend dentro de Docker..."
Invoke-Checked docker compose build frontend

Write-Host "Línea base verificada correctamente."

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

Write-Host "[1/4] Validando la configuración de Docker Compose..."
Invoke-Checked docker compose config --quiet

Write-Host "[2/4] Construyendo imágenes reproducibles..."
Invoke-Checked docker compose build

Write-Host "[3/4] Ejecutando pruebas backend con PostgreSQL..."
Invoke-Checked docker compose run --rm backend python manage.py test

Write-Host "[4/4] Validando compilación frontend dentro de Docker..."
Invoke-Checked docker compose build frontend

Write-Host "Línea base verificada correctamente."

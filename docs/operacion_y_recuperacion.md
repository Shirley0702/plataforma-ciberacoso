# Operación, monitoreo y recuperación

## Salud y registros

- `GET /api/health/` comprueba la aplicación y una consulta real a PostgreSQL. Responde `503` si la base no está disponible.
- Backend y frontend tienen `healthcheck` en Docker Compose.
- Cada respuesta incluye `X-Request-ID`; el backend registra ruta, método, estado y duración en JSON.
- No se registran cuerpos, parámetros de consulta, correos, tokens ni textos escritos por participantes.

En un entorno de pruebas o producción, la plataforma de monitoreo debe consultar `/api/health/`, alertar por respuestas distintas de 200 y recopilar la salida estándar de los contenedores. Los umbrales y destinatarios dependen del servicio de alojamiento y deben configurarse allí.

## Respaldo

Con Docker Compose en ejecución y PowerShell 7:

```powershell
.\scripts\backup-postgres.ps1
```

En Linux:

```bash
./scripts/backup-postgres.sh
```

El resultado usa el formato personalizado de `pg_dump` y genera un checksum SHA-256. El directorio `backups/` está excluido de Git porque puede contener información privada.

## Comprobación de restauración

La comprobación restaura el archivo en una base temporal cuyo nombre empieza por `cibersegura_restore_check_`; nunca sobrescribe la base principal. Verifica el checksum y la tabla de migraciones, y elimina la base temporal al finalizar.

```powershell
.\scripts\test-postgres-restore.ps1 -BackupPath .\backups\cibersegura-AAAAmmdd-HHMMSS.dump
```

```bash
./scripts/test-postgres-restore.sh ./backups/cibersegura-AAAAmmdd-HHMMSS.dump
```

Antes de cada liberación se debe conservar en un almacenamiento cifrado el respaldo, su checksum, la fecha de la prueba de restauración y el resultado. Las credenciales y los respaldos nunca se suben al repositorio.

## Entorno de pruebas

`.env.staging.example` y `docker-compose.staging.yml` endurecen Django y utilizan las imágenes publicadas en GitHub Container Registry. En el servidor de pruebas:

```bash
docker compose --env-file .env.staging -f docker-compose.yml -f docker-compose.staging.yml pull
docker compose --env-file .env.staging -f docker-compose.yml -f docker-compose.staging.yml up -d --no-build
```

El servidor debe terminar TLS, restringir los puertos internos mediante firewall, mantener secretos fuera de Git y ejecutar la comprobación de salud. El repositorio prepara el despliegue; la publicación efectiva requiere un servidor y credenciales del entorno de pruebas.

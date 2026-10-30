#!/usr/bin/env sh
set -eu

backup_directory="${1:-./backups}"
mkdir -p "$backup_directory"
timestamp="$(date -u +%Y%m%d-%H%M%S)"
backup_path="$backup_directory/cibersegura-$timestamp.dump"
database_user="$(docker compose exec -T db printenv POSTGRES_USER)"
database_name="$(docker compose exec -T db printenv POSTGRES_DB)"

docker compose exec -T db pg_dump \
  --username="$database_user" \
  --dbname="$database_name" \
  --format=custom \
  --no-owner \
  --no-acl > "$backup_path"

(cd "$backup_directory" && sha256sum "$(basename "$backup_path")" > "$(basename "$backup_path").sha256")
printf 'Respaldo creado: %s\n' "$backup_path"

#!/usr/bin/env sh
set -eu

backup_path="${1:?Indica el archivo .dump que se comprobará}"
test -f "$backup_path"
test -f "$backup_path.sha256"
backup_directory="$(CDPATH='' cd -- "$(dirname -- "$backup_path")" && pwd)"
backup_filename="$(basename -- "$backup_path")"
(cd "$backup_directory" && sha256sum -c "$backup_filename.sha256")

database_user="$(docker compose exec -T db printenv POSTGRES_USER)"
temporary_database="cibersegura_restore_check_$$"
container_backup="/tmp/$backup_filename"

cleanup() {
  docker compose exec -T db dropdb --username="$database_user" --if-exists "$temporary_database" >/dev/null 2>&1 || true
  docker compose exec -T db rm -f -- "$container_backup" >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

docker compose cp "$backup_path" "db:$container_backup"
docker compose exec -T db createdb --username="$database_user" "$temporary_database"
docker compose exec -T db pg_restore --username="$database_user" --dbname="$temporary_database" --exit-on-error "$container_backup"
migration_count="$(docker compose exec -T db psql --username="$database_user" --dbname="$temporary_database" --tuples-only --no-align --command='SELECT COUNT(*) FROM django_migrations;')"
test "$migration_count" -gt 0
printf 'Restauración comprobada en una base temporal (%s migraciones).\n' "$migration_count"

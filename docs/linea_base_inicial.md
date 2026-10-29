# Entregable inicial: línea base y planificación técnica

**Periodo:** 5–11 de octubre de 2026  
**Unidad:** 1  
**Objetivo Scrum:** Línea base y planificación técnica aprobada.

## Resultado entregable

La línea base del MVP queda compuesta por:

1. Backlog de 16 semanas y tres unidades configurado en Jira.
2. Alcance, requisitos y arquitectura inicial documentados en `docs/`.
3. Matriz de trazabilidad entre requisitos, evidencia y semana de cierre.
4. Versiones de Python, Node, pnpm y dependencias backend registradas.
5. Procedimiento único de verificación mediante `verify-baseline.ps1`.
6. Evidencia de compilación frontend y pruebas backend sobre PostgreSQL.
7. Correcciones anticipadas de seguridad, configuración y progreso del curso.

## Auditoría técnica del 6 de octubre de 2026

| Componente | Verificación | Resultado | Observación |
|---|---|---|---|
| Docker Compose | `docker compose config --quiet` | Aprobado | Configuración válida |
| Backend | `docker compose run --rm backend python manage.py test` | Aprobado | 28 de 28 pruebas; PostgreSQL |
| Frontend | `pnpm --dir frontend build` | Aprobado con advertencia | El equipo local usa Node 20.15; el proyecto exige 22.12+ |
| Seguridad Django | `python manage.py check --deploy` con configuración de producción | Aprobado | 0 advertencias |
| Migraciones | `python manage.py makemigrations --check --dry-run` | Aprobado | No existen cambios sin migración |

## Versiones de referencia

- Python 3.12.14.
- Node.js 22.12.0 o superior y menor que 25.
- pnpm 11.19.0.
- PostgreSQL 16.
- Dependencias Python fijadas en `backend/constraints.txt`.
- Dependencias frontend fijadas en `frontend/pnpm-lock.yaml`.

## Definition of Ready

Una historia puede entrar al sprint cuando tiene valor para el usuario, descripción, criterios de aceptación verificables, dependencias, riesgos de privacidad/seguridad, diseño o contrato suficiente y estimación acordada.

## Definition of Done

Una historia está terminada cuando el código compila, las pruebas relacionadas pasan, los criterios de aceptación tienen evidencia, no se incluyen secretos ni datos personales reales y la documentación afectada queda actualizada. Los cambios de datos requieren migración reversible; los cambios de interfaz deben revisar accesibilidad y respuesta móvil.

## Criterios de aceptación de la Semana 1

- [x] Existen exactamente 16 sprints semanales en Jira, agrupados en tres unidades.
- [x] Cada semana tiene un entregable evaluable.
- [x] El alcance y los requisitos están inventariados.
- [x] La matriz de trazabilidad relaciona requisitos con semanas y evidencia.
- [x] Docker Compose tiene configuración válida.
- [x] Las 28 pruebas backend pasan con PostgreSQL.
- [x] El frontend genera una compilación de producción.
- [x] Las versiones requeridas y los riesgos conocidos están documentados.
- [x] DoR y DoD están definidos.

## Riesgos abiertos para los siguientes sprints

1. Cobertura backend insuficiente y ausencia de pruebas frontend/E2E.
2. Credenciales y valores de demostración que deben prohibirse en producción.
3. Falta de política implementada de retención y eliminación de resultados de evaluación.
4. Falta de CI/CD, observabilidad, backup y restauración probada.

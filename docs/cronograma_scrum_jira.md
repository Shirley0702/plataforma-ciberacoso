# Cronograma Scrum para finalizar CiberSegura

## Horizonte y supuesto de capacidad

- Periodo: 5 de octubre de 2026 al 20 de enero de 2027.
- Cadencia: 16 semanas académicas. La semana 16 es parcial y termina el 20 de enero con la entrega final.
- Evaluación: 3 unidades académicas. Unidad 1: semanas 1–5. Unidad 2: semanas 6–10. Unidad 3: semanas 11–16.
- Capacidad de referencia: 10 puntos por semana para una persona con dedicación parcial de 15 a 20 horas. Ajustar los puntos, no las fechas finales, si participa más de una persona.
- Las semanas de Navidad (21–27 de diciembre) y Año Nuevo (28 de diciembre–3 de enero) cuentan dentro del cronograma y tienen entregables obligatorios de alcance reducido.
- Objetivo de producto: publicar una versión verificable, segura, accesible y documentada de CiberSegura, centrada en cursos y evaluaciones preventivas.

## Diagnóstico del estado actual

La revisión técnica confirmó que el MVP implementa registro universitario internacional con verificación, cuentas iniciales `demo` y `admin` con roles separados, evaluación de ocho escenarios, filtrado por pesos, dashboard y curso personalizados, recursos y administración. El frontend compila correctamente dentro de Docker y las 28 pruebas backend existentes pasan.

Pendientes y riesgos que justifican el backlog:

- Existen 28 pruebas backend y todavía no hay pruebas automatizadas del frontend ni E2E persistentes.
- Las evaluaciones y el curso requieren mayor profundidad pedagógica, historial, comparación y seguimiento.
- Faltan límites de frecuencia, auditoría, cabeceras de seguridad, monitoreo y pipeline CI/CD.
- Hay secretos y credenciales de demostración por defecto que deben quedar prohibidos en producción.
- El enlace de administración está fijado a `localhost` y la configuración por ambiente debe completarse.
- La validación de registro y la verificación de correo ya están implementadas; todavía faltan recuperación de contraseña y pruebas más amplias de permisos/aislamiento entre usuarios.
- Los contenidos y recursos oficiales deben ser revisados por una persona responsable antes de publicar.

## Épicas de Jira

1. `EP-01` Gestión y arquitectura.
2. `EP-02` Identidad y API backend.
3. `EP-03` Base de datos y gobierno de datos.
4. `EP-04` Frontend, UX y accesibilidad.
5. `EP-05` Seguimiento y reportes de evaluación.
6. `EP-06` Calidad, seguridad y privacidad.
7. `EP-07` DevOps, despliegue y observabilidad.
8. `EP-08` Validación, documentación y entrega.

## Cronograma semanal de entregables evaluables

Cada semana termina con un producto que puede revisarse mediante una demostración, evidencia de pruebas, documento versionado o despliegue. Las actividades internas no sustituyen al entregable.

| Unidad | Semana | Fechas | Entregable semanal que se revisa | Evidencia mínima de aceptación | Puntos |
|---|---:|---|---|---|---:|
| Unidad 1 | 1 | 5–11 oct | Línea base y planificación técnica aprobada | Backlog priorizado, matriz de requisitos, arquitectura, entorno Docker reproducible y DoR/DoD | 8 |
| Unidad 1 | 2 | 12–18 oct | Módulo de identidad endurecido | Demo de registro, separación administrador/participante, inicio/cierre, renovación JWT y recuperación; pruebas positivas y negativas | 10 |
| Unidad 1 | 3 | 19–25 oct | Base de datos y política de privacidad implementadas | Diagrama actualizado, migraciones PostgreSQL reversibles, índices y prueba de eliminación/retención | 10 |
| Unidad 1 | 4 | 26 oct–1 nov | Diagnóstico backend validado | API documentada, cálculo corregido, permisos de historial y reporte de pruebas de borde | 10 |
| Unidad 1 | 5 | 2–8 nov | Incremento evaluable de la Unidad 1 | Diagnóstico completo frontend-backend, responsive y accesible; demo, informe y evidencias de pruebas | 10 |
| Unidad 2 | 6 | 9–15 nov | Curso y progreso funcionales | Administración de contenidos, avance reversible/idempotente y pruebas de API | 10 |
| Unidad 2 | 7 | 16–22 nov | Experiencia formativa terminada | Navegación, reanudación, contenido pedagógico revisado y evidencia responsive/accesible | 8 |
| Unidad 2 | 8 | 23–29 nov | Historial de evaluaciones funcional | Resultados aislados por usuario, comparación temporal, filtros y controles de privacidad | 10 |
| Unidad 2 | 9 | 30 nov–6 dic | Evaluaciones configurables y validadas | Versionado de cuestionarios, banco de preguntas y contenido revisado por responsables | 8 |
| Unidad 2 | 10 | 7–13 dic | Incremento evaluable de la Unidad 2 | Curso y evaluaciones ampliados, integrados, probados y demostrables | 10 |
| Unidad 3 | 11 | 14–20 dic | Panel y reportes de progreso integrados | Indicadores de curso y evaluaciones, exportación y pruebas de permisos | 10 |
| Unidad 3 | 12 | 21–27 dic | Paquete navideño de validación de contenido | Ruta formativa y enlaces oficiales revisados, acta de validación y correcciones documentadas | 5 |
| Unidad 3 | 13 | 28 dic–3 ene | Paquete de Año Nuevo de cobertura automatizada | Reporte ejecutable de pruebas de usuarios, permisos, dashboard, curso y recursos | 5 |
| Unidad 3 | 14 | 4–10 ene | Calidad frontend y accesibilidad verificadas | Suite E2E de flujos críticos, auditoría WCAG 2.2 y registro de correcciones | 5 |
| Unidad 3 | 15 | 11–17 ene | Candidato de liberación seguro y recuperable | Informe OWASP, prueba de rendimiento, backup/restauración y despliegue en staging con monitoreo | 10 |
| Unidad 3 | 16 | 18–20 ene | Entrega final de la Unidad 3 | UAT cerrada, versión liberada, cero defectos críticos, manual técnico, manual de usuario, evidencias y retrospectiva final | 15 |

Total planificado: 144 puntos.

## Entregables de cierre por unidad

- Unidad 1, semana 5: incremento funcional de identidad, datos y diagnóstico; informe técnico y demostración.
- Unidad 2, semana 10: curso y evaluaciones ampliados e integrados; informe de resultados y demostración.
- Unidad 3, semana 16: sistema desplegado, probado y documentado; release final, manuales y evidencias académicas.

## Flujo Scrum en Jira

Estados recomendados: `Backlog` → `Seleccionado` → `En progreso` → `Revisión` → `Pruebas` → `Hecho`.

Ceremonias:

- Planificación: primer día de cada sprint, 30 a 45 minutos.
- Daily: 10 a 15 minutos; registrar bloqueos en la incidencia, no como una tarea separada.
- Refinamiento: miércoles, 30 minutos, para dejar preparado el siguiente sprint.
- Revisión y retrospectiva: último día, 30 minutos cada una.
- En la semana 16: revisión final de la Unidad 3 y retrospectiva global el 20 de enero.

## Definition of Ready

Una historia puede entrar a un sprint cuando tiene descripción, valor para el usuario, criterios de aceptación comprobables, dependencias identificadas, diseño o contrato API suficiente y estimación acordada.

## Definition of Done

Una historia se considera terminada cuando:

- El código compila y las pruebas relacionadas pasan.
- Incluye pruebas nuevas proporcionales al cambio y no reduce la cobertura acordada.
- Se revisaron seguridad, privacidad, accesibilidad y tratamiento de errores cuando aplican.
- Las migraciones son reversibles y se probaron con PostgreSQL cuando hay cambios de datos.
- La documentación y los criterios de aceptación están actualizados.
- Está desplegada y verificada en staging para los cambios de los sprints 15 y 16.
- No contiene secretos, credenciales de demostración ni datos personales reales.

## Criterios de liberación del 20 de enero

- Flujos completos de registro, acceso por rol, evaluación, ruta personalizada, curso, recursos y cierre de sesión aprobados en E2E.
- Cero defectos críticos o altos abiertos; los medios aceptados deben tener responsable y fecha.
- Backend, frontend y migraciones validados en PostgreSQL mediante CI.
- Historial y reportes de evaluación aislados por usuario, con advertencia orientativa visible.
- Política de privacidad/retención de resultados aplicada y procedimiento de eliminación probado.
- Backup restaurado exitosamente en un entorno limpio.
- Manual técnico, manual de usuario, matriz de trazabilidad y evidencias académicas entregados.

## Importación a Jira

El archivo `docs/jira_backlog_import.csv` contiene las épicas e historias. En el importador CSV de Jira se deben mapear `Issue ID`, `Parent ID`, `Issue Type`, `Summary`, `Description`, `Priority`, `Labels`, `Story Points`, `Sprint`, `Start Date` y `Due Date`. Si Jira no permite crear sprints durante la importación, crear primero los 16 sprints con los nombres exactos del CSV y repetir la importación o asignarlos después mediante el label `sprint-XX`.

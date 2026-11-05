# Matriz de trazabilidad del MVP

Esta matriz relaciona los requisitos con su implementación actual, la evidencia verificable y la semana Scrum que completa o fortalece cada capacidad. Se revisó como parte del entregable de la Semana 1, el 6 de octubre de 2026.

## Requisitos funcionales

| ID | Resultado esperado | Implementación actual | Evidencia mínima | Semana de cierre | Estado de línea base |
|---|---|---|---|---:|---|
| RF-01 | Registro universitario verificado y acceso separado de `admin` | `apps.users`, catálogo internacional de dominios universitarios, código temporal, permisos por rol, JWT y Django Admin | Aceptación de distintos dominios universitarios, rechazo de correos personales y claves débiles, activación por código, login participante y rechazo admin en API | 2 | Implementado y probado |
| RF-02 | Completar ocho escenarios diagnósticos | `apps.diagnostics` y `DiagnosticPage` | Envío completo, incompleto y opciones válidas | 4–5 | Implementado y probado |
| RF-03 | Priorizar módulo por suma de pesos | `SubmitDiagnosticView` y `DiagnosticResult` | Mayor puntuación y salida neutral preventiva | 4–5 | Implementado y probado |
| RF-04 | Dashboard y curso personalizados | `DashboardView`, `CourseUnitListView` y páginas React | Solo se muestra el módulo asignado | 5–7 | Implementado y probado |
| RF-05 | Progreso limitado a la ruta asignada | `CompleteLessonView` | Rechazo de lecciones pertenecientes a otros módulos | 6–7 | Implementado y probado |
| RF-06 | Completar actividad y cuestionario del módulo | `CompleteLessonView`, `SubmitModuleQuizView` y `CoursePage` | Bloqueo previo, respuesta válida, cálculo de puntuación e intentos | 6–7 | Implementado y probado |
| RF-07 | Obtener certificado con 80 % o más | `Certificate`, descarga PDF y verificación pública | Aprobación al 80 %, PDF autenticado y código verificable | 7 | Implementado y probado |
| RF-08 | Recursos de orientación | `apps.resources` | Enlaces, teléfonos y vigencia revisados | 12 | Implementado; requiere revisión periódica externa |
| RF-09 | Administración de contenidos | Django Admin | Permisos, auditoría y reversibilidad | 9–12 | Implementado para contenidos y evidencia de calidad |
| RF-10 | Recoger validación del producto | `apps.product_validation` y `ProductFeedbackPage` | Acceso después de certificar el curso, cinco métricas por versión, consentimiento, agregados y matriz ISO/IEC 25010 | 14–15 | Instrumento implementado; resultados dependen de participantes reales |

## Requisitos no funcionales

| ID | Resultado esperado | Evidencia mínima | Semana de cierre | Estado de línea base |
|---|---|---|---:|---|
| RNF-01 | Interfaz responsiva | Pruebas en móvil, tableta y escritorio | 5, 7 y 14 | Cubierto por E2E en escritorio y móvil; completar evidencia en dispositivos físicos |
| RNF-02 | Accesibilidad WCAG 2.2 | Teclado, foco, contraste, lector y auditoría | 5 y 14 | Auditoría automática transversal; lector de pantalla y dispositivos físicos requieren evidencia manual |
| RNF-03 | Contraseñas protegidas | Hash Django, validadores y pruebas de autenticación | 2 | Implementado; ampliar pruebas |
| RNF-04 | Uso únicamente orientativo | Aviso visible y consistente en API/UI | 7 y 12 | Implementado; revisar contenidos |

## Cobertura de la línea base

- Backend: 49 pruebas automatizadas en PostgreSQL para autenticación, roles, diagnóstico, personalización, curso, certificación, clasificación de texto, validación del producto y salud operativa.
- Frontend: 11 pruebas de componentes y accesibilidad, compilación TypeScript de producción y 2 recorridos E2E completos con Chromium (escritorio y móvil), incluida auditoría WCAG en navegador real.
- Datos: migraciones iniciales disponibles para todos los módulos.
- Operación: Docker Compose levanta PostgreSQL, backend y frontend con comprobaciones de salud; GitHub Actions ejecuta CI/E2E, publica imágenes y verifica respaldo/restauración en una base temporal.

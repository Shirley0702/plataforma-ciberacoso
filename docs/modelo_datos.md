# Modelo de datos inicial

```mermaid
erDiagram
    USER ||--|| USER_PROFILE : tiene
    USER ||--o{ DIAGNOSTIC_ATTEMPT : realiza
    DIAGNOSTIC_ATTEMPT ||--o{ DIAGNOSTIC_ANSWER : contiene
    DIAGNOSTIC_ATTEMPT ||--|| DIAGNOSTIC_RESULT : produce
    DIAGNOSTIC_QUESTION ||--o{ DIAGNOSTIC_OPTION : ofrece
    DIAGNOSTIC_QUESTION ||--o{ DIAGNOSTIC_ANSWER : responde
    DIAGNOSTIC_OPTION ||--o{ DIAGNOSTIC_ANSWER : selecciona
    COURSE_UNIT ||--o{ DIAGNOSTIC_QUESTION : contextualiza
    COURSE_UNIT ||--o{ DIAGNOSTIC_OPTION : recibe_peso
    COURSE_UNIT ||--o{ DIAGNOSTIC_RESULT : es_sugerido
    COURSE_UNIT ||--o{ LESSON : contiene
    COURSE_UNIT ||--o{ MODULE_QUIZ_QUESTION : evalua
    MODULE_QUIZ_QUESTION ||--o{ MODULE_QUIZ_OPTION : ofrece
    USER ||--o{ COURSE_PROGRESS : registra
    LESSON ||--o{ COURSE_PROGRESS : recibe
    USER ||--o{ MODULE_QUIZ_ATTEMPT : realiza
    COURSE_UNIT ||--o{ MODULE_QUIZ_ATTEMPT : recibe
    USER ||--o{ CERTIFICATE : obtiene
    COURSE_UNIT ||--o{ CERTIFICATE : acredita
```

`DiagnosticOption.destination_unit` y `DiagnosticOption.weight` implementan el filtrado. `DiagnosticResult` conserva el módulo sugerido, la puntuación máxima y los totales por módulo. Cada módulo tiene cuatro lecciones y una actividad; `CourseProgress.activity_response` conserva la decisión tomada. El cuestionario final registra intentos y puntuación sin exponer las respuestas correctas. `Certificate` acredita una sola vez la combinación usuario-módulo, almacena un código público único y permite generar el PDF bajo demanda. Se reutiliza el usuario autenticado de Django en lugar de duplicar una tabla de credenciales. `OrientationResource` permanece como catálogo independiente.

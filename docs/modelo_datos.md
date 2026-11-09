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
    COURSE_UNIT ||--o{ DIAGNOSTIC_OPTION : recibe_valor_ordinal
    COURSE_UNIT ||--o{ DIAGNOSTIC_RESULT : es_prioridad_principal
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

`DiagnosticOption.destination_unit` y `DiagnosticOption.weight` conservan la dimensión y el valor ordinal uniforme de cada alternativa. `DiagnosticResult.profile` guarda la versión del instrumento, las cuatro dimensiones, sus porcentajes, los niveles de prioridad, los empates y todas las unidades recomendadas; `suggested_unit` se mantiene como referencia a la primera unidad para compatibilidad. Cada módulo tiene exploración guiada, decisión, lista interactiva, práctica y plan personal. `CourseProgress.interaction_response` guarda exclusivamente identificadores de opciones o pasos, nunca relatos ni datos personales. El cuestionario final registra intentos y puntuación sin exponer las respuestas correctas. `Certificate` acredita una sola vez la combinación usuario-módulo, almacena un código público único y permite generar el PDF bajo demanda. Se reutiliza el usuario autenticado de Django en lugar de duplicar una tabla de credenciales. `OrientationResource` permanece como catálogo independiente.

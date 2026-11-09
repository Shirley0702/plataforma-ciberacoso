# Mapa de pantallas

```mermaid
flowchart LR
    R["Registro / Login de participante"] --> D["Evaluación de 16 escenarios"]
    D --> A["Perfil multidimensional y prioridades"]
    A --> P["Dashboard personalizado"]
    P --> C["Curso: unidades recomendadas"]
    C --> L["1 unidad visible y 6 experiencias secuenciales"]
    L --> I["Ver · comprender · explorar · decidir · revisar · practicar · planificar"]
    I --> Q["Cuestionario final obligatorio"]
    Q -->|"80 % o más"| CE["Certificado PDF verificable"]
    Q -->|"Menos de 80 %"| RE["Retroalimentación y nuevo intento"]
    P --> O["Recursos de orientación"]
    P --> S["Cerrar sesión"]
    ADM["Inicio de sesión: admin"] --> DA["Django Admin"]
```

El sistema mantiene separados los roles: los participantes registrados y `demo` recorren la experiencia educativa; `admin` solo gestiona el sistema mediante Django Admin. La evaluación es obligatoria antes de mostrar el panel y el curso. Los empates conservan el mismo nivel de prioridad. Si todas las respuestas son neutrales, se asigna la ruta general de Convivencia y Autocuidado Preventivo. El curso muestra una sola unidad y una sola experiencia cada vez; la unidad siguiente requiere el certificado de la anterior. El cuestionario se habilita al completar sus seis experiencias y el certificado requiere al menos 80 %.

# Mapa de pantallas

```mermaid
flowchart LR
    R["Registro / Login de participante"] --> D["Evaluación de 8 escenarios"]
    D --> A["Algoritmo: suma de pesos por módulo"]
    A --> P["Dashboard personalizado"]
    P --> C["Curso: módulo priorizado"]
    C --> L["4 lecciones de microaprendizaje"]
    L --> I["Actividad interactiva"]
    I --> Q["Cuestionario final obligatorio"]
    Q -->|"80 % o más"| CE["Certificado PDF verificable"]
    Q -->|"Menos de 80 %"| RE["Retroalimentación y nuevo intento"]
    P --> O["Recursos de orientación"]
    P --> S["Cerrar sesión"]
    ADM["Inicio de sesión: admin"] --> DA["Django Admin"]
```

El sistema mantiene separados los roles: los participantes registrados y `demo` recorren la experiencia educativa; `admin` solo gestiona el sistema mediante Django Admin. La evaluación es obligatoria antes de mostrar el panel y el curso. Si todas las respuestas son neutrales, se asigna la ruta preventiva de bienestar y seguridad digital. El cuestionario se habilita al completar los cinco microcontenidos y el certificado requiere al menos 80 %.

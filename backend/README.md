# Guía del backend

El backend usa una estructura **por dominio** y el patrón de capas de Django:

```text
backend/
|-- manage.py                 Entrada oficial de comandos Django
|-- config/                   Configuración global del servidor
|-- initial_data/             Catálogo inicial idempotente de la plataforma
`-- apps/
    |-- users/                Cuenta, perfil, autenticación y dashboard
    |-- diagnostics/          Test por escenarios y filtrado de ruta
    |-- courses/              Curso, progreso, cuestionario y certificado
    `-- resources/            Recursos oficiales de orientación
```

## Cómo leer una aplicación

Los archivos que parecen estar "sueltos" dentro de cada aplicación son puntos de
entrada que Django reconoce por convención. No son archivos basura:

| Archivo o carpeta | Responsabilidad única |
|---|---|
| `models.py` | Tablas y relaciones de la base de datos |
| `serializers.py` | Validación y formato de entrada/salida de la API |
| `views.py` | Recibir HTTP, delegar el caso de uso y devolver HTTP |
| `urls.py` | Rutas HTTP del dominio |
| `admin.py` | Registro de modelos en el panel administrativo |
| `apps.py` | Identidad y configuración de la aplicación Django |
| `use_cases/` | Reglas de negocio, separadas por acción del usuario |
| `documents/` | Generación de archivos descargables |
| `tests.py` | Pruebas automáticas del dominio |
| `migrations/` | Historial inmutable del esquema de base de datos |

`__init__.py` indica que una carpeta es un paquete Python. Puede estar vacío y es
necesario para que los imports sean predecibles.

## Casos de uso

```text
apps/courses/use_cases/
|-- course_assignment.py     Obtiene la ruta asignada y su estado
|-- lesson_progress.py       Valida y completa experiencias interactivas
`-- module_quiz.py           Califica y emite el certificado

apps/diagnostics/use_cases/
`-- submit_diagnostic.py     Puntúa respuestas y selecciona la ruta

apps/users/use_cases/
|-- dashboard_summary.py     Construye el resumen personalizado
|-- email_verification.py    Emite, reenvía y valida el código institucional
`-- username_generation.py   Genera el identificador interno único

apps/users/
|-- university_email.py      Consulta segura del catálogo universitario local
`-- data/                     Catálogo internacional, atribución y licencia

apps/courses/documents/
`-- certificate.py           Genera el certificado PDF
```

Las vistas no contienen el algoritmo del negocio. Este reparto sigue una
arquitectura por capas: **API → caso de uso → modelos**.

## Archivos globales

| Archivo | Función |
|---|---|
| `config/settings.py` | Base de datos, seguridad, idioma y configuración REST |
| `config/urls.py` | Agrupa las rutas de todas las aplicaciones |
| `config/wsgi.py` | Punto de entrada del servidor web en producción |
| `initial_data/seed_catalog.py` | Carga usuarios opcionales y contenido inicial |
| `requirements.txt` | Dependencias directas declaradas por el proyecto |
| `constraints.txt` | Versiones exactas reproducibles de dependencias |
| `Dockerfile` | Construcción del contenedor del backend |

## Regla para código nuevo

Una regla que calcula, decide o cambia estado pertenece en un archivo con nombre
explícito dentro de `use_cases/`. Una vista solo debe validar la petición,
ejecutar ese caso de uso y construir la respuesta.

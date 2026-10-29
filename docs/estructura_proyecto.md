# Estructura del proyecto

La aplicación está organizada por dominio. Cada carpeta debe tener una sola razón principal para cambiar.

## Backend

```text
backend/
|-- config/                  Configuración global de Django y rutas principales
|-- initial_data/            Catálogo inicial cargado de forma idempotente
`-- apps/
    |-- users/               Registro, autenticación, roles, perfil y panel
    |-- diagnostics/         Escenarios, respuestas y asignación de la ruta
    |-- courses/             Microcontenidos, progreso, cuestionario y certificado
    `-- resources/           Directorio oficial de orientación
```

En cada aplicación Django:

- `models.py`: estructura persistente de la base de datos.
- `serializers.py`: entrada y salida de la API.
- `views.py`: adaptación HTTP; no contiene reglas de negocio complejas.
- `use_cases/`: reglas de negocio separadas por acción del usuario.
- `urls.py`: rutas públicas de la aplicación.
- `admin.py`: configuración del panel administrativo.
- `tests.py`: pruebas automatizadas.
- `migrations/`: historial ordenado de cambios de la base de datos.

Paquetes especializados:

- `courses/documents/certificate.py`: representación PDF del certificado.
- `initial_data/seed_catalog.py`: carga idempotente de los contenidos iniciales.
- `users/management/commands/seed_initial_data.py`: adaptador requerido para exponer el comando a Django.

Los archivos `models.py`, `views.py`, `serializers.py`, `urls.py`, `admin.py` y
`apps.py` permanecen en la raíz de cada aplicación porque Django los reconoce por
convención. Su función exacta está documentada en `backend/README.md`.

## Frontend

```text
frontend/src/
|-- app/                    Rutas, layout y páginas globales
|-- features/
|   |-- auth/                Registro, inicio de sesión y estado de autenticación
|   |-- diagnostic/          Evaluación por escenarios
|   |-- dashboard/           Resumen personalizado
|   |-- course/              Curso, actividad, cuestionario y certificado
|   `-- resources/           Recursos de ayuda
|-- shared/
|   |-- api/                 Cliente HTTP
|   |-- components/          Componentes usados por varias funcionalidades
|   |-- styles/              Variables y estilos globales
|   `-- types/               Contratos compartidos mínimos
|-- main.tsx                 Punto de entrada requerido por React/Vite
`-- vite-env.d.ts            Tipos automáticos requeridos por Vite
```

La funcionalidad del curso se divide además en:

- `pages/CoursePage.tsx`: composición visual de la pantalla.
- `hooks/useCourse.ts`: estado, carga y acciones del curso.
- `components/LearningItemCard.tsx`: lección o actividad interactiva.
- `components/ModuleAssessment.tsx`: cuestionario, resultado y certificado.

## Flujo principal

```text
Registro de participante
    -> Verificación del correo institucional
    -> Login de participante
    -> Diagnóstico por escenarios
    -> Servicio de puntuación y filtrado
    -> Dashboard personalizado
    -> Curso del módulo asignado
    -> Cuestionario final
    -> Certificado verificable
```

La cuenta `demo` sigue este flujo como usuario de prueba. La cuenta `admin` queda fuera y accede exclusivamente a Django Admin.

## Reglas de organización

1. Una vista HTTP no debe contener el algoritmo del dominio.
2. Una página React no debe implementar directamente todas las peticiones y reglas de estado.
3. El código exclusivo de una funcionalidad permanece dentro de `features/<funcionalidad>`.
4. `shared` solo contiene elementos utilizados por dos o más funcionalidades.
5. No se guardan compilaciones, cachés, secretos ni configuraciones personales del editor.
6. Las migraciones no se renombran ni eliminan después de aplicarse.

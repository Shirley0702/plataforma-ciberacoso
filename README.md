# CiberSegura

Plataforma educativa de prevención y orientación frente al ciberacoso en jóvenes. Implementa autenticación, diagnóstico por escenarios, filtrado adaptativo, microaprendizaje, evaluación final, certificación, recursos y administración de contenidos.

Flujo educativo obligatorio: **Registro/Login → Verificación del correo → Evaluación de escenarios → Algoritmo de filtrado → Dashboard y curso personalizados**. La cuenta `admin` utiliza un acceso separado y no participa en ese recorrido; `demo` es una cuenta de participante preparada para pruebas.

> Las evaluaciones son orientativas. No reemplazan una evaluación profesional, una denuncia ni la atención de una emergencia.

## Qué incluye

- React 19 + TypeScript + Vite + Bootstrap 5.
- Django 5.2 LTS + Django REST Framework + JWT.
- PostgreSQL en Docker y SQLite como opción local de inicio rápido.
- Datos iniciales, usuario de demostración, pruebas backend y documentación del alcance.
- Banco de ocho escenarios con opciones indirectas y pesos no expuestos al frontend.
- Selección del módulo con mayor puntuación y curso limitado a la ruta asignada.
- Ruta de microaprendizaje con cuatro lecciones, una actividad de decisión y un cuestionario final por módulo.
- Certificado individual al obtener al menos 80 %, descargable en PDF y verificable mediante código público.
- Interfaz responsiva, navegación por teclado, etiquetas accesibles y mensajes claros.

## Inicio rápido con Docker

Requisitos: Docker Desktop con Docker Compose. El entorno de contenedores es la vía recomendada y no depende de las versiones locales de Python o Node.

1. Copia `.env.example` como `.env` y cambia las contraseñas.
2. Ejecuta:

   ```bash
   docker compose up --build
   ```

3. Abre `http://localhost:8080`.

La administración local está disponible en `http://localhost:8000/admin/`. El sistema sincroniza dos cuentas iniciales: `admin`, para el panel administrativo, y `demo`, como participante de prueba. Además, el registro público permite crear participantes normales sin privilegios administrativos. Las contraseñas iniciales deben definirse en `DEMO_ADMIN_PASSWORD` y `DEMO_USER_PASSWORD`; el proyecto no incluye contraseñas predecibles.

El registro público contrasta el dominio contra un catálogo local de más de
10.000 dominios de universidades de distintos países y admite sus subdominios.
Esto incluye instituciones que usan `.edu`, `.edu.ec`, `.ac.uk` o dominios
propios como `.cl` y `.fr`; no se intenta decidir por el texto del sufijo. Los
dominios nuevos pueden incorporarse mediante
`ADDITIONAL_UNIVERSITY_EMAIL_DOMAINS`. La cuenta se crea desactivada y solo se
habilita al ingresar el código de seis dígitos enviado al correo; el código
vence, limita intentos y permite reenvío con espera. Para entrega real configura en `.env`
`DJANGO_EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`,
`EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS` y `DEFAULT_FROM_EMAIL`. Sin credenciales
SMTP, el entorno Docker de desarrollo imprime el mensaje en el registro del
backend y no puede enviarlo a una bandeja real.

El participante registra su nombre completo, correo y contraseña. El nombre
solo admite letras y debe incluir nombre y apellido. El identificador técnico se
genera automáticamente y nunca se solicita en el formulario; el inicio de sesión
normal se realiza con el correo institucional. `demo` conserva su nombre de
usuario por ser una cuenta inicial de pruebas.

En producción configura `DJANGO_DEBUG=False`, una `DJANGO_SECRET_KEY` propia, hosts y orígenes permitidos reales. Las opciones HTTPS, cookies seguras y HSTS se activan automáticamente al deshabilitar el modo de depuración y pueden ajustarse con las variables documentadas en `.env.example`.

## Inicio local sin Docker

Versiones de referencia: Python 3.12.14, Node.js 22.12 o superior (menor que 25) y pnpm 11.19.0. Los archivos `.python-version`, `.nvmrc`, `backend/constraints.txt` y `frontend/pnpm-lock.yaml` conservan la línea base validada.

### Backend

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -c backend/constraints.txt -r backend/requirements.txt
cd backend
python manage.py migrate
python manage.py seed_initial_data
python manage.py runserver
```

Por defecto usa SQLite. Para PostgreSQL, configura `DATABASE_ENGINE=postgresql` y las variables `POSTGRES_*` del archivo de ejemplo.

### Frontend

En otra terminal:

```bash
cd frontend
pnpm install
pnpm dev
```

Abre `http://localhost:5173`.

## Pruebas y compilación

```bash
cd backend
python manage.py test

cd ../frontend
pnpm build
```

En Windows también puede validarse toda la línea base desde la raíz:

```powershell
.\verify-baseline.ps1
```

La organización de carpetas y la responsabilidad de cada archivo están explicadas en `docs/estructura_proyecto.md`. La evidencia y los riesgos de la primera semana están en `docs/linea_base_inicial.md`; la relación entre requisitos y sprints está en `docs/matriz_trazabilidad.md`.

## API principal

- `POST /api/auth/register/`
- `POST /api/auth/verify-email/`
- `POST /api/auth/resend-verification/`
- `POST /api/auth/token/`
- `POST /api/auth/token/refresh/`
- `POST /api/auth/logout/`
- `GET /api/users/me/`
- `GET /api/users/dashboard/`
- `GET /api/diagnostics/questions/`
- `POST /api/diagnostics/submit/`
- `GET /api/courses/units/`
- `POST /api/courses/lessons/{id}/complete/`
- `POST /api/courses/quiz/submit/`
- `GET /api/courses/certificates/{code}/download/`
- `GET /api/courses/certificates/verify/{code}/`
- `GET /api/resources/`

## Estructura

```text
plataforma-ciberacoso/
|-- frontend/              # React organizado por funcionalidades
|-- backend/               # Django REST organizado por dominios y servicios
|-- docs/                  # Alcance, requisitos y diagramas
|-- docker-compose.yml
|-- .env.example
`-- README.md
```

## Decisiones de seguridad y privacidad

- Django aplica hash seguro a las contraseñas; nunca se guardan en texto plano.
- Los tokens de acceso vencen en 15 minutos y los de renovación se rotan.
- La ruta inicial siempre muestra el acceso y los tokens solo persisten durante la sesión actual del navegador.
- CORS y hosts permitidos se configuran por entorno.
- Los resultados de las evaluaciones siempre muestran una advertencia de uso orientativo.

Consulta `docs/` para el alcance, requisitos, navegación y modelo de datos.

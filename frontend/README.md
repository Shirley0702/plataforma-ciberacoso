# Organización del frontend

## Archivos de la raíz

- `Dockerfile`: construye la imagen de producción.
- `index.html`: documento HTML donde React se monta.
- `nginx.conf`: sirve la compilación y redirige la API al backend.
- `package.json`: dependencias y comandos del frontend.
- `pnpm-lock.yaml`: versiones exactas instaladas.
- `vite.config.ts`: configuración del compilador Vite.
- `tsconfig*.json`: reglas de TypeScript.

Estos archivos permanecen en la raíz porque Docker, Vite, pnpm y TypeScript los buscan allí.

## Código fuente

```text
src/
|-- app/                    Arranque visual, rutas y layout principal
|-- features/               Funcionalidades independientes del producto
|   |-- auth/               Registro, verificación, acceso y sesión de participantes
|   |                        (`admin` se dirige al panel Django separado)
|   |-- diagnostic/         Evaluación por escenarios
|   |-- dashboard/          Panel personalizado
|   |-- course/             Microcontenidos, cuestionario y certificado
|   `-- resources/          Recursos oficiales
|-- shared/                 Código compartido entre funcionalidades
|   |-- api/                Cliente HTTP
|   |-- components/         Componentes visuales reutilizables
|   |-- styles/             Estilos generales de la aplicación
|   `-- types/              Tipos compartidos
|-- main.tsx                Punto de entrada requerido por React/Vite
`-- vite-env.d.ts           Tipos automáticos requeridos por Vite
```

Cada funcionalidad puede contener:

- `pages/`: composición completa de una pantalla.
- `components/`: piezas visuales exclusivas de esa funcionalidad.
- `hooks/`: estado, efectos y operaciones reutilizables.
- `context/`: estado compartido por varias pantallas de la funcionalidad.
- `types.ts`: contratos exclusivos de esa funcionalidad.

En `features/auth`, `registrationValidation.ts` concentra las reglas del
formulario y `verificationStorage.ts` conserva únicamente el correo pendiente
durante la sesión del navegador. `VerifyEmailPage.tsx` controla la activación de
la cuenta mediante el código recibido.

`main.tsx` y `vite-env.d.ts` son los únicos archivos sueltos dentro de `src` porque constituyen puntos técnicos de entrada exigidos por las herramientas.

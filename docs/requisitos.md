# Requisitos del MVP

## Funcionales

- **RF-01:** registrar e iniciar sesión de usuarios.
- **RF-02:** completar una evaluación diagnóstica formada por escenarios y opciones indirectas.
- **RF-03:** sumar los pesos seleccionados por módulo y elegir de forma determinista el módulo con mayor puntuación.
- **RF-04:** mostrar en el panel la ruta asignada y filtrar el curso al módulo sugerido.
- **RF-05:** registrar el progreso únicamente sobre las lecciones de la ruta asignada.
- **RF-06:** consultar recursos de orientación.
- **RF-07:** administrar escenarios, opciones, módulos, lecciones y recursos.

## No funcionales

- **RNF-01:** interfaz responsiva para computadora y teléfono.
- **RNF-02:** contraste, teclado, etiquetas y mensajes claros según criterios básicos de WCAG 2.2.
- **RNF-03:** contraseñas administradas por el sistema de hash de Django.
- **RNF-04:** resultados presentados como orientación, nunca como diagnóstico definitivo.

## Casos de uso principales

1. El usuario crea una cuenta e inicia sesión.
2. Responde los ocho escenarios sin conocer los pesos internos.
3. El algoritmo agrupa los pesos por módulo y prioriza el total más alto.
4. El panel presenta el módulo sugerido y el acceso al curso personalizado.
5. El usuario recorre las lecciones asignadas y registra su progreso.
6. El usuario consulta recursos de orientación.
7. El administrador modifica contenidos desde Django Admin.

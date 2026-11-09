# Requisitos del MVP

## Funcionales

- **RF-01:** registrar e iniciar sesión de usuarios.
- **RF-02:** completar una evaluación diagnóstica formada por escenarios y opciones indirectas.
- **RF-03:** construir un perfil de cuatro dimensiones mediante una escala ordinal uniforme, conservar empates y seleccionar hasta los dos niveles positivos con mayor prioridad.
- **RF-04:** asignar una ruta preventiva general cuando todas las dimensiones sean neutrales y mostrar en el panel todas las unidades recomendadas.
- **RF-05:** registrar el progreso únicamente sobre las lecciones de las unidades recomendadas.
- **RF-06:** consultar recursos de orientación.
- **RF-07:** administrar escenarios, opciones, módulos, lecciones y recursos.

## No funcionales

- **RNF-01:** interfaz responsiva para computadora y teléfono.
- **RNF-02:** contraste, teclado, etiquetas y mensajes claros según criterios básicos de WCAG 2.2.
- **RNF-03:** contraseñas administradas por el sistema de hash de Django.
- **RNF-04:** resultados presentados como orientación, nunca como diagnóstico definitivo.

## Casos de uso principales

1. El usuario crea una cuenta e inicia sesión.
2. Responde los 16 escenarios sin conocer la escala ordinal interna.
3. El algoritmo construye el perfil multidimensional, conserva empates y selecciona los dos primeros niveles positivos.
4. Si todo es neutral, el sistema asigna la ruta preventiva general.
5. El panel presenta todas las unidades sugeridas y el acceso al curso personalizado.
6. El usuario recorre las lecciones asignadas y registra su progreso.
7. El usuario consulta recursos de orientación.
8. El administrador modifica contenidos desde Django Admin.

# Alcance del software

## Problema

Los jóvenes pueden experimentar o presenciar conductas de hostigamiento digital sin reconocer señales, conservar evidencia ni saber a quién acudir. CiberSegura ofrece educación preventiva y orientación inicial en un entorno privado y comprensible.

## Usuarios

- Participantes registrados que completan el recorrido educativo; `demo` es la cuenta de prueba inicial.
- Administrador que mantiene preguntas, contenidos y recursos mediante la cuenta `admin`.

## Incluido en el MVP

- Registro, inicio y cierre de sesión de participantes con JWT.
- Acceso separado de la cuenta `admin` mediante Django Admin.
- Evaluación diagnóstica de ocho escenarios universitarios.
- Algoritmo de filtrado que suma pesos por módulo y prioriza la mayor puntuación.
- Panel personal con la ruta educativa asignada.
- Curso filtrado al módulo sugerido con tres lecciones, una actividad interactiva y avance registrado.
- Cuestionario final obligatorio y certificado del módulo al alcanzar al menos 80 %.
- Recursos oficiales de orientación.
- Administración mediante Django Admin.

## Fuera del MVP

Chat en tiempo real, aplicación móvil nativa, lectura directa de redes sociales, gamificación avanzada, notificaciones y modelos generativos.

## Criterio de éxito

Una persona puede registrarse como participante, completar la evaluación por escenarios, recibir un módulo priorizado, terminar sus microcontenidos, aprobar el cuestionario con al menos 80 %, descargar un certificado verificable, consultar orientación y cerrar sesión. `demo` permite probar ese mismo recorrido. La cuenta `admin` puede actualizar los contenidos desde un panel protegido, pero no puede utilizar las API educativas.

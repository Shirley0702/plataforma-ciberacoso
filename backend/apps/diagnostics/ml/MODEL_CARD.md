# Modelo de recomendación de rutas

## Propósito

Clasificar el patrón agregado de respuestas de una evaluación por escenarios y recomendar una ruta educativa. No diagnostica, no determina si una persona es víctima y no reemplaza una valoración profesional.

## Versión inicial

- Algoritmo: regresión logística multiclase con estandarización.
- Implementación: scikit-learn.
- Versión del modelo: `route-logistic-regression-v1`.
- Variables: puntuaciones agregadas de cuatro categorías internas.
- Salida: identificador interno de la ruta y probabilidad de confianza.

## Datos de entrenamiento

La primera versión usa patrones sintéticos reproducibles construidos con criterios expertos. Sirven para verificar la arquitectura de Machine Learning, pero no demuestran validez pedagógica ni generalización sobre estudiantes reales.

## Uso responsable

Antes de presentar el modelo como validado se requiere un conjunto anonimizado de respuestas reales, etiquetas revisadas por especialistas, consentimiento y evaluación de precisión, sesgo, calibración y desempeño por subgrupos. Las respuestas neutrales, las predicciones con confianza menor a 0.55 y cualquier fallo técnico utilizan una ruta preventiva de respaldo basada en reglas.

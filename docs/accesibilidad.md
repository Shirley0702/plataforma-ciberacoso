# Accesibilidad de CiberSegura

## Objetivo

La interfaz se desarrolla tomando WCAG 2.2 nivel AA como referencia. Las comprobaciones automáticas son una barrera de calidad, no sustituyen las pruebas manuales ni la participación de personas que utilizan tecnologías de asistencia.

## Controles implementados

- estructura semántica con encabezados, regiones `main`, navegación y formularios etiquetados;
- enlace para saltar directamente al contenido principal;
- foco visible y traslado del foco al contenido cuando cambia la ruta;
- nombre de página actualizado en cada navegación;
- mensajes de validación asociados programáticamente con cada campo;
- controles operables con teclado, incluidos el menú y la visualización temporal de contraseña;
- alternativa de movimiento reducido mediante `prefers-reduced-motion`;
- diseño adaptable para pantallas pequeñas y contenido con zoom;
- auditorías automáticas con `axe` sobre acceso, registro, navegación autenticada, evaluación, recursos y revisión de texto, sin excluir la regla de contraste.

## Protocolo manual antes de cada liberación

Registrar fecha, versión, navegador, dispositivo, persona evaluadora y evidencia de cada resultado.

| Comprobación | Criterio de aceptación |
| --- | --- |
| Teclado | Todo el recorrido puede completarse con Tab, Shift+Tab, Enter, Espacio y Escape; no hay trampas de foco. |
| Foco | El orden es lógico, el indicador siempre es visible y los cambios de vista se anuncian desde el contenido principal. |
| Lector de pantalla | NVDA con Firefox o Chrome anuncia títulos, regiones, etiquetas, errores, estados, progreso y botones con nombres comprensibles. |
| Zoom | A 200 % y 400 % no se pierde información ni se requiere desplazamiento horizontal a 320 CSS px, salvo contenido que lo necesite. |
| Contraste | Texto, controles, estados y foco cumplen los mínimos AA medidos en el navegador real. |
| Movimiento | Con “reducir movimiento” activo no existen animaciones indispensables ni transiciones molestas. |
| Dispositivos | Acceso, registro, evaluación, panel, curso, revisión, recursos y cuenta funcionan en escritorio y móvil. |
| Mensajes | Errores y confirmaciones se perciben visualmente y mediante tecnología de asistencia, sin depender solo del color. |

## Evidencia y límites

`pnpm test` ejecuta la auditoría automática en cada cambio. El contraste debe verificarse también en un navegador real porque JSDOM no calcula estilos y píxeles como un motor gráfico completo. Las pruebas manuales y con estudiantes deben registrar resultados reales; no se consideran aprobadas hasta que exista esa evidencia.

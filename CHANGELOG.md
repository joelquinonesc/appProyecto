# Registro de Cambios — ANXRISK

Todos los cambios notables del proyecto serán documentados en este archivo.

---

## [1.2.0] — 2026-03-09

### Mejorado
- **Metodología del Modelo en Resultados y PDF**: nueva sección explicativa sobre la Red Neuronal MLP, la Curva ROC y las métricas de validación (AUC-ROC, Sensibilidad, Especificidad, Precisión, F1-Score, Índice de Youden)
- **PDF sección 7 expandida** con 4 subsecciones: arquitectura MLP, Curva ROC, clasificación triclásica con umbrales, y resultado de la predicción
- **Página de inicio**: estadísticas reemplazadas por descriptores del modelo (MLP / SHAP / ROC)
- **Datos del profesional evaluador** movidos a la página de Demográficos (antes estaban en Resultados)
- **Análisis Masivo** ahora incluye campos del profesional evaluador
- **Documentación del proyecto** completamente reorganizada y actualizada en español

### Eliminado
- Archivos obsoletos: resúmenes de proceso interno, scripts vacíos, screenshots sin usar
- Referencia a exportación HTML (solo PDF)
- Estadísticas genéricas de la página de inicio (0.954 AUC, N=234, 3 Niveles)

---

## [1.1.0] — 2026-03-08

### Mejorado
- **Edad y educación**: campos sin valor por defecto, con placeholder "Ingrese la edad" / "Ingrese los años"
- Manejo de `None` en comparaciones de educación
- Despliegue exitoso en Streamlit Community Cloud

---

## [1.0.5] — 2026-03-07

### Mejorado
- **Radio buttons centrados** en todas las escalas (LTE-12, SF-12, HADS, ZSAS) mediante `st.columns()`
- Solución definitiva después de 5 intentos con CSS que no funcionaron con Streamlit 1.51

---

## [1.0.4] — 2026-03-06

### Mejorado
- **PDF completo reescrito** con 9 secciones clínicas, explicaciones clínicas por escala, puntos de viñeta para eventos, y bloque de firma
- **Datos del profesional evaluador**: sección visible como tarjeta (no expander)
- **Nombre del paciente** en el nombre del archivo PDF descargado
- **Recomendaciones clínicas** por nivel de riesgo en el PDF

### Eliminado
- Exportación HTML (solo PDF)

---

## [1.0.3] — 2026-03-05

### Mejorado
- **Tipografía**: cambio a Figtree (Google Fonts) en toda la aplicación
- **Logo**: monograma "A" con SVG en la página de inicio
- **SF-12**: unificación de estilos entre componente físico y mental
- **LTE-12**: corrección de bug con `enumerate()` vs `.items()`
- **PDF**: explicaciones clínicas añadidas en todas las secciones

---

## [1.0.2] — 2026-03-04

### Mejorado
- **Rediseño estético completo** de 12 archivos con paleta ámbar/carbón
- Colores: primario `#D4911D`, superficie `#F0EDEA`, texto `#2D2D2D`
- Navegación mejorada con botones de avance/retroceso
- Corrección de datos demográficos y layout centrado
- Unificación de fuentes tipográficas

---

## [1.0.0] — 2025-11-28

### Lanzamiento Inicial
- Sistema completo de evaluación con cuestionarios LTE-12, SF-12, HADS, ZSAS
- Modelos MLP y LightGBM entrenados
- Análisis SHAP integrado con visualizaciones
- Análisis masivo por lotes CSV
- Interfaz profesional con Streamlit
- Documentación completa y scripts de instalación

---

**© 2025 Breyner Joel Quiñones Castro. Todos los derechos reservados.**

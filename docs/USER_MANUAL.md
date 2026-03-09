# Manual de Usuario — ANXRISK

## ¿Qué es ANXRISK?

ANXRISK es una herramienta profesional de evaluación psicológica que evalúa el riesgo de trastornos de ansiedad mediante cuestionarios clínicos validados, datos demográficos y análisis genético opcional. Genera predicciones de riesgo utilizando una Red Neuronal MLP con interpretabilidad SHAP.

> **Importante:** Esta herramienta es de apoyo a la decisión clínica. Los resultados no constituyen un diagnóstico definitivo y deben ser interpretados por un profesional de salud mental.

---

## Acceso a la Aplicación

### En línea (producción)
Acceda directamente desde: [appproyecto.streamlit.app](https://appproyecto.streamlit.app)

### Local (desarrollo)
```bash
streamlit run app.py
```
Se abrirá en su navegador en `http://localhost:8501`.

---

## Proceso de Evaluación Paso a Paso

### 1. Página de Inicio

Al abrir ANXRISK verá la página de bienvenida con:
- Descripción del sistema
- Características principales
- Botón **"Comenzar Evaluación"** para iniciar
- Botón **"Análisis Masivo"** para procesar múltiples pacientes

### 2. Datos Demográficos

Complete la información obligatoria del paciente:
- **Nombre completo** (campo de texto)
- **Edad** (sin valor por defecto, ingrese manualmente)
- **Género** (Masculino / Femenino)
- **Años de educación formal** (máximo calculado automáticamente: edad – 5)

En esta misma página, complete los **datos del profesional evaluador**:
- Nombre del profesional
- Cargo / Especialidad
- Institución
- Registro profesional

Estos datos aparecerán en el reporte PDF con espacio para firma.

Presione **"Guardar datos"** para continuar.

### 3. Eventos Vitales — LTE-12

Responda **Sí** o **No** a 12 eventos vitales estresantes experimentados recientemente:
- Enfermedad grave personal o de familiar cercano
- Muerte de un familiar o amigo cercano
- Separación o divorcio
- Problemas laborales serios
- Dificultades financieras graves
- Y otros eventos significativos

Los radio buttons están centrados en la pantalla para facilitar la lectura.

### 4. Salud Física — SF-12

5 preguntas sobre su salud física en las últimas 4 semanas:
- Percepción general de salud
- Limitaciones en actividades moderadas
- Limitaciones subiendo escaleras
- Interferencia con trabajo por problemas físicos
- Dolor corporal

### 5. Salud Mental — SF-12

2 preguntas sobre su bienestar emocional:
- Energía y vitalidad
- Estado de ánimo (tranquilidad vs. desánimo)

### 6. HADS — Escala de Ansiedad Hospitalaria

7 preguntas sobre síntomas de ansiedad en la última semana:
- Tensión y nerviosismo
- Sensación de miedo
- Inquietud
- Malestar estomacal
- Y otros síntomas

Cada pregunta tiene 4 opciones de respuesta (0–3 puntos).

**Interpretación del puntaje total (0–21):**
| Rango | Nivel |
|-------|-------|
| 0–7 | Normal |
| 8–10 | Ansiedad leve |
| 11–14 | Ansiedad moderada |
| 15–21 | Ansiedad severa |

### 7. ZSAS — Escala de Ansiedad de Zung

20 preguntas sobre síntomas de ansiedad con escala de frecuencia:
- Nunca o casi nunca
- A veces
- Con bastante frecuencia
- Siempre o casi siempre

**Nota:** Los ítems 5, 9, 13, 17 y 19 tienen puntuación invertida (son preguntas formuladas en sentido positivo).

---

## Resultados

### Predicción de Riesgo

Después de completar todos los cuestionarios, la página de Resultados muestra:

1. **Resumen clínico** con todos los puntajes
2. **Panel genético** (opcional) — active el toggle para incluir genotipos
3. **Botón "Calcular Predicción"** — ejecuta el modelo MLP

El resultado muestra:
- **Nivel de riesgo** (Bajo / Moderado / Alto) con código de color
- **Probabilidad** expresada como porcentaje
- **Barra de riesgo** visual

### Metodología del Modelo

Después del resultado aparece una sección explicativa con:
- **Qué es la Red Neuronal MLP** y cómo funciona
- **Qué es la Curva ROC** y el AUC-ROC
- **Tabla de métricas** con definiciones y relevancia clínica
- **Umbrales de clasificación** (Bajo < 0.30, Moderado 0.30–0.59, Alto ≥ 0.60)

### Análisis SHAP

Debajo del resultado se genera automáticamente:
- **Gráfico de barras** con las características más influyentes
  - 🔴 Barras rojas: factores que **aumentan** el riesgo
  - 🟢 Barras verdes: factores que **disminuyen** el riesgo
- **Tabla detallada** con valores SHAP, efecto e interpretación

### Descargar Reporte PDF

Una vez calculada la predicción, aparece el botón **"Descargar Reporte PDF Completo"**.

El PDF incluye 9 secciones:
1. Datos Demográficos
2. Eventos Vitales (LTE-12)
3. Salud Física y Mental (SF-12)
4. Ansiedad HADS
5. Ansiedad ZSAS
6. Perfil Genético
7. Metodología del Modelo y Predicción (MLP, ROC, métricas, umbrales, resultado)
8. Análisis SHAP (gráfico + tabla)
9. Resumen Clínico Integrado + firma del profesional

El nombre del archivo incluye el nombre del paciente.

---

## Análisis Masivo

Para procesar múltiples pacientes simultáneamente:

1. Desde la página de inicio, presione **"Análisis Masivo"**
2. Complete los **datos del profesional evaluador**
3. Descargue la **plantilla CSV** como referencia
4. Cargue su archivo CSV con las columnas requeridas:

| Columna | Descripción |
|---------|-------------|
| `nombre` | Nombre completo |
| `edad` | Edad en años |
| `genero` | Masculino o Femenino |
| `años_educacion` | Años de educación formal |
| `hads_score` | Puntuación HADS (0–42) |
| `zsas_score` | Puntuación ZSAS (20–80) |
| `sf12_fisica` | Puntuación SF-12 Física |
| `sf12_mental` | Puntuación SF-12 Mental |
| `lte12_count` | Número de eventos vitales (0–12) |
| `prkca` | *(opcional)* Genotipo PRKCA |
| `tcf4` | *(opcional)* Genotipo TCF4 |
| `cdh20` | *(opcional)* Genotipo CDH20 |

5. Presione **"Procesar y Generar Reportes"**
6. Descargue los resultados en CSV o Excel

---

## Privacidad y Seguridad

- Los datos se procesan localmente en su navegador/servidor
- No se almacenan en bases de datos externas
- La sesión se elimina al cerrar el navegador
- Cumple con principios de Habeas Data

---

## Solución de Problemas

| Problema | Solución |
|----------|----------|
| La aplicación no carga | Verifique que el servidor Streamlit esté ejecutándose |
| Error "módulo no encontrado" | Ejecute `pip install -r requirements.txt` |
| Puerto 8501 en uso | Use `streamlit run app.py --server.port 8502` |
| PDF no se genera | Verifique que calculó la predicción primero |
| Radio buttons no aparecen | Actualice el navegador o limpie la caché |

---

## Situaciones de Crisis

Si durante la evaluación el paciente experimenta crisis de ansiedad severa o pensamientos de autolesión, contacte inmediatamente los servicios de emergencia o la línea de crisis de salud mental de su localidad.

---

**© 2025 Breyner Joel Quiñones Castro. Todos los derechos reservados.**

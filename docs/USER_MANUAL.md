# Manual de Usuario Completo — ANXRISK

## Tabla de Contenido

1. [¿Qué es ANXRISK?](#qué-es-anxrisk)
2. [Acceso a la Aplicación](#acceso-a-la-aplicación)
3. [Interfaz General y Navegación](#interfaz-general-y-navegación)
4. [Evaluación Individual — Paso a Paso](#evaluación-individual--paso-a-paso)
   - 4.1 [Página de Inicio](#41-página-de-inicio)
   - 4.2 [Datos Demográficos](#42-datos-demográficos)
   - 4.3 [Eventos Vitales — LTE-12](#43-eventos-vitales--lte-12)
   - 4.4 [Salud Física — SF-12 PCS](#44-salud-física--sf-12-pcs)
   - 4.5 [Salud Mental — SF-12 MCS](#45-salud-mental--sf-12-mcs)
   - 4.6 [Ansiedad — HADS](#46-ansiedad--hads)
   - 4.7 [Ansiedad — ZSAS (Zung)](#47-ansiedad--zsas-zung)
   - 4.8 [Resultados y Predicción](#48-resultados-y-predicción)
5. [Análisis Masivo (CSV)](#5-análisis-masivo-csv)
6. [Reporte PDF](#6-reporte-pdf)
7. [Privacidad, Seguridad y Habeas Data](#7-privacidad-seguridad-y-habeas-data)
8. [Solución de Problemas](#8-solución-de-problemas)
9. [Situaciones de Crisis](#9-situaciones-de-crisis)

---

## ¿Qué es ANXRISK?

ANXRISK es un **Sistema de Estratificación del Riesgo de Trastornos de Ansiedad** diseñado como herramienta de apoyo a la decisión clínica para profesionales de salud mental.

El sistema integra múltiples fuentes de información:

- **Datos demográficos** del paciente (edad, género, educación)
- **Eventos vitales estresantes** mediante la escala LTE-12
- **Calidad de vida** mediante el SF-12 (componentes físico y mental)
- **Síntomas de ansiedad** mediante las escalas HADS y ZSAS
- **Marcadores genéticos** (opcional) — polimorfismos PRKCA, TCF4 y CDH20

A partir de estas variables, una **Red Neuronal MLP (Perceptrón Multicapa)** predice la probabilidad de riesgo de ansiedad y la clasifica en tres niveles: **Bajo**, **Moderado** o **Alto**. La interpretabilidad individual se logra mediante el método **SHAP** (SHapley Additive exPlanations), que muestra la contribución específica de cada factor a la predicción del paciente.

> **⚠️ Aviso clínico:** Esta herramienta es de **apoyo** a la decisión clínica. Los resultados **no constituyen un diagnóstico definitivo** y deben ser interpretados por un profesional de salud mental calificado, en el contexto clínico completo del paciente.

---

## Acceso a la Aplicación

### En línea (producción)

La aplicación está desplegada en Streamlit Community Cloud y se accede directamente desde el navegador:

🔗 **[appproyecto.streamlit.app](https://appproyecto.streamlit.app)**

No requiere instalación. Compatible con cualquier navegador moderno (Chrome, Firefox, Edge, Safari).

### Ejecución local (desarrollo)

Si dispone del código fuente, puede ejecutar la aplicación localmente:

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la aplicación
streamlit run app.py
```

La aplicación se abrirá automáticamente en su navegador en `http://localhost:8501`. Si el puerto 8501 está ocupado, puede especificar otro:

```bash
streamlit run app.py --server.port 8502
```

---

## Interfaz General y Navegación

### Diseño visual

ANXRISK utiliza un diseño profesional con:
- **Tipografía:** Fuente Figtree (importada de Google Fonts)
- **Paleta de colores:** Ámbar dorado (#D4911D) como color primario, con fondo claro (#F0EDEA) y texto oscuro (#2D2D2D)
- **Disposición:** Layout ancho (`wide`) que aprovecha toda la pantalla

### Barra lateral (sidebar)

En la parte izquierda de la pantalla, la barra lateral muestra:

1. **Logo de ANXRISK** — Monograma "A" con pulso neuronal en SVG
2. **Nombre del sistema** — "ANXRISK" y subtítulo
3. **Stepper de progreso** — Visible durante la evaluación individual, muestra las 6 secciones con indicadores visuales:
   - ⚫ Punto gris: sección pendiente
   - 🟡 Punto dorado: sección actual
   - ✅ Punto verde con check: sección completada
4. **Barra de progreso** — Porcentaje visual de avance (ej. "3 / 6 secciones")
5. **Aviso legal** — Recordatorio de que es una herramienta de apoyo clínico

### Flujo de navegación

El sistema sigue un flujo secuencial obligatorio. No es posible saltar secciones:

```
Inicio → Datos Demográficos → LTE-12 → SF-12 Física → SF-12 Mental → HADS → ZSAS → Resultados
```

Si intenta acceder a una sección sin haber completado la anterior, el sistema lo redirige automáticamente a la sección pendiente.

---

## Evaluación Individual — Paso a Paso

### 4.1 Página de Inicio

Al abrir ANXRISK, la pantalla principal muestra:

#### Sección hero
- **Logo SVG animado** — Monograma "A" con línea de pulso neuronal y puntos de acento en ámbar dorado
- **Título:** "ANXRISK"
- **Subtítulo:** "Sistema de Estratificación del Riesgo de Trastornos de Ansiedad"
- **Descripción:** "Evaluación multimodal con interpretabilidad individual basada en aprendizaje automático. Calibrado en población colombiana adulta."

#### Botones de acción principales
Dos botones centrados en la pantalla:
- **"Iniciar Evaluación Individual"** (botón primario, color ámbar) — Lleva a Datos Demográficos
- **"Análisis Masivo (CSV)"** (botón secundario) — Lleva al módulo de procesamiento por lotes

#### Tarjetas de características
Tres tarjetas informativas en fila:

| Tarjeta | Ícono | Descripción |
|---------|-------|-------------|
| **Evaluación Clínica** | ✔ Check | LTE-12, SF-12, HADS y ZSAS integrados en flujo secuencial validado |
| **Panel Genético** | 🧪 Matraz | SNPs *PRKCA*, *TCF4*, *CDH20* como módulo opcional |
| **Interpretabilidad** | 📊 Barras | Análisis SHAP individual con reportes exportables en PDF |

#### Barra de estadísticas del modelo
Tres indicadores descriptivos:
- **MLP** — Red Neuronal Multicapa
- **SHAP** — Interpretabilidad Individual
- **ROC** — Validación Clínica

#### Guía de uso integrada
- Botón **"Ver Guía de Uso"** que abre un panel expandible con:
  - Introducción al sistema
  - Tabla del flujo de evaluación (6 pasos con instrumentos y referencias bibliográficas)
  - Tabla de interpretación de resultados (Bajo / Moderado / Alto con recomendaciones)
  - Explicación del análisis SHAP
  - Nota de privacidad y protección de datos

#### Sección de privacidad
- **Tarjeta con candado** — Texto sobre la Ley 1581 de 2012 y Decreto 1377 de 2013 (Habeas Data)
- **Expansor "Ver Política de Tratamiento de Datos Personales"** — Documento completo con 7 secciones: Responsable, Finalidad, Datos Recopilados, Tratamiento y Seguridad, Derechos del Titular, Marco Legal y Consentimiento

---

### 4.2 Datos Demográficos

#### Encabezado
- **Título:** "Datos Demográficos"
- **Subtítulo:** "Información base del paciente para la estratificación de riesgo"

#### Campos del paciente (todos obligatorios)

| Campo | Tipo de control | Detalles |
|-------|----------------|----------|
| **Nombre completo** | Campo de texto | Placeholder: "Nombre completo *". Campo libre. |
| **Edad** | Campo numérico | Sin valor por defecto (aparece vacío). Placeholder: "Ingrese la edad". Mínimo: 0, máximo: 120. Debe ser mayor a 0 para ser válido. |
| **Género** | Lista desplegable | Opciones: "Seleccionar" (por defecto, no válido), "Masculino", "Femenino". |
| **Años de educación formal** | Campo numérico | Sin valor por defecto (aparece vacío). Placeholder: "Ingrese los años". El máximo se calcula automáticamente como **edad – 5**. Si la edad no se ha ingresado o es menor a 5, este campo aparece deshabilitado con el mensaje "Ingrese primero la edad del paciente". |

#### Datos del profesional evaluador (opcionales pero recomendados)

Debajo de una línea divisora, aparece una tarjeta con borde dorado a la izquierda titulada **"👨‍⚕️ Datos del Profesional Evaluador"** con la instrucción: "Complete estos datos para que aparezcan en el reporte PDF con espacio para su firma."

| Campo | Placeholder de ejemplo |
|-------|----------------------|
| **Nombre del profesional** | "Dr(a). Nombre Apellido" |
| **Cargo / Especialidad** | "Psiquiatra / Psicólogo clínico" |
| **Institución** | "Hospital / Consultorio / IPS" |
| **Registro profesional** | "TP-XXXXX" |

Estos datos se almacenan en la sesión y aparecerán en el bloque de firma del PDF.

#### Botón "Guardar datos"
Al presionar, el sistema valida:
- Nombre no vacío
- Género seleccionado (no "Seleccionar")
- Edad mayor a 0
- Años de educación ingresados y no superiores al máximo permitido

Si hay errores, se muestran en una lista con viñetas rojas. Si todo es válido, aparece "Datos guardados correctamente" y la página muestra un resumen con métricas de los datos ingresados.

#### Vista de confirmación
Cuando los datos ya están guardados, la pantalla muestra:
- ✅ "Datos demográficos registrados correctamente"
- Métricas del paciente en dos columnas: Nombre, Edad, Género, Educación
- Si se ingresaron datos del profesional: sección **"👨‍⚕️ Profesional Evaluador"** con los datos en métricas
- Botón **"Editar datos"** — Vuelve al formulario
- Botón **"Siguiente"** (primario) — Avanza a LTE-12

---

### 4.3 Eventos Vitales — LTE-12

#### Encabezado
- **Título:** "Eventos Vitales Estresantes (LTE-12)"
- **Subtítulo:** "Evalúa experiencias recientes con impacto potencial en la salud mental"

#### Tarjeta de contexto clínico
Explica el modelo diathesis-stress, la Lista de Experiencias Amenazantes y la referencia bibliográfica:
> *Brugha, T., Bebbington, P., Tennant, C., & Hurry, J. (1985). Psychological Medicine, 15(1), 189-194.*

Instrucción: *"Todas las preguntas son obligatorias — Seleccione 'Sí' para los eventos experimentados recientemente"*

#### Las 12 preguntas

Cada pregunta se presenta en una tarjeta individual con número ("Pregunta X de 12") y texto. Las opciones **"No" / "Sí"** aparecen como **radio buttons horizontales centrados** en la pantalla (usando `st.columns([1, 2, 1])`).

| # | Pregunta |
|---|----------|
| 1 | ¿Ha sufrido usted mismo(a) una enfermedad, lesión o agresión grave? |
| 2 | ¿Algún familiar cercano ha sufrido una enfermedad, lesión o agresión grave? |
| 3 | ¿Ha muerto uno de sus padres, hijos o su pareja/cónyuge? |
| 4 | ¿Ha muerto un amigo cercano a la familia o algún otro familiar? |
| 5 | ¿Se ha separado a causa de problemas en su matrimonio? |
| 6 | ¿Ha roto una relación estable? |
| 7 | ¿Ha tenido un problema grave con algún amigo cercano, vecino o familiar? |
| 8 | ¿Se ha quedado sin empleo o ha buscado empleo durante más de un mes sin éxito? |
| 9 | ¿Le han despedido de su trabajo? |
| 10 | ¿Ha tenido una crisis económica grave? |
| 11 | ¿Ha tenido problemas con la policía o ha comparecido ante un tribunal? |
| 12 | ¿Le han robado o ha perdido algún objeto de valor? |

Ninguna pregunta tiene respuesta preseleccionada (index=None). Si alguna queda sin responder, aparece el mensaje de error:
> ❌ "Responda todas las preguntas antes de continuar."

Cuando todas están respondidas:
> ✅ "Todas las preguntas completadas"

#### Clasificación interna (no visible al usuario)
El total de respuestas "Sí" (0–12) se transforma:
- 0 eventos → clase 0 (LTE12_0 = 1)
- 1 evento → clase 1 (LTE12_1 = 1)
- 2 o más eventos → clase 2 (LTE12_2 = 1)

El botón **"Siguiente"** lleva a SF-12 Física.

---

### 4.4 Salud Física — SF-12 PCS

#### Encabezado
- **Título:** "SF-12 — Componente Física (PCS)"
- **Subtítulo:** "Evalúa la percepción de salud física del paciente mediante 6 ítems"

#### Tarjeta de contexto
Explica el SF-12 como cuestionario de calidad de vida validado internacionalmente. Referencia:
> *Ware, J. E., Kosinski, M., & Keller, S. D. (1996). Medical Care, 34(3), 220-233.*

#### Las 6 preguntas

**Pregunta 1 de 6** — "En general, ¿diría que su salud es?"
- Tipo: **Lista desplegable** (selectbox)
- Opciones: Excelente (5 pts), Muy buena (4 pts), Buena (3 pts), Regular (2 pts), Mala (1 pt)
- Placeholder: "Seleccione una opción"

**Pregunta 2 de 6** — "Esfuerzos moderados (mover una mesa, caminar más de 1 hora)"
- Tipo: **Radio buttons horizontales centrados** (st.columns [1, 3, 1])
- Opciones: "Sí, limitado mucho" (1 pt), "Sí, limitado un poco" (2 pts), "No, no limitado en absoluto" (3 pts)

**Pregunta 3 de 6** — "Subir varios pisos por la escalera"
- Tipo: **Radio buttons horizontales centrados**
- Mismas opciones que la pregunta 2

*Texto introductorio:* "Durante las 4 últimas semanas, ¿ha tenido alguno de los siguientes problemas en su trabajo o en sus actividades cotidianas, a causa de su salud física?"

**Pregunta 4 de 6** — "¿Hizo menos de lo que hubiera querido hacer?"
- Tipo: **Radio buttons horizontales centrados** (st.columns [1, 2, 1])
- Opciones: "Sí" (1 pt), "No" (2 pts)

**Pregunta 5 de 6** — "¿Tuvo que dejar de hacer algunas tareas en su trabajo o en sus actividades cotidianas?"
- Tipo: **Radio buttons horizontales centrados**
- Opciones: "Sí" (1 pt), "No" (2 pts)

**Pregunta 6 de 6** — "¿Hasta qué punto el dolor le ha dificultado su trabajo habitual?"
- Tipo: **Radio buttons horizontales centrados**
- Opciones: "Nada" (5 pts), "Un poco" (4 pts), "Regular" (3 pts), "Bastante" (2 pts), "Mucho" (1 pt)

#### Validación
Si falta alguna respuesta:
> ❌ "Responda todas las preguntas de la sección física antes de continuar."

Cuando todo está completo:
> ✅ "Componente física completada"

El botón **"Siguiente"** lleva a SF-12 Mental. El puntaje bruto se transforma internamente a un **cuartil** (Q1–Q4) según estos umbrales:

| Puntaje | Cuartil |
|---------|---------|
| ≤ 15 | Q1 — Salud física muy baja |
| 16–17 | Q2 — Salud física baja |
| 18–19 | Q3 — Salud física moderada |
| ≥ 20 | Q4 — Salud física excelente |

---

### 4.5 Salud Mental — SF-12 MCS

#### Encabezado
- **Título:** "SF-12 — Componente Mental (MCS)"
- **Subtítulo:** "Evalúa el bienestar emocional y mental del paciente mediante 6 ítems"

#### Tarjeta de contexto
Explica el componente mental del SF-12 con la misma referencia bibliográfica (Ware et al., 1996).

#### Las 6 preguntas

**Pregunta 1 de 6** — "¿Hizo menos de lo que hubiera querido hacer, por algún problema emocional?"
- Tipo: **Radio buttons horizontales centrados** (st.columns [1, 2, 1])
- Opciones: "Sí" (1 pt), "No" (2 pts)

**Pregunta 2 de 6** — "¿No hizo su trabajo o sus actividades cotidianas tan cuidadosamente como de costumbre, por algún problema emocional?"
- Tipo: **Radio buttons horizontales centrados**
- Opciones: "Sí" (1 pt), "No" (2 pts)

**Pregunta 3 de 6** — "¿Con qué frecuencia la salud física o los problemas emocionales le han dificultado sus actividades sociales?"
- Tipo: **Lista desplegable** (selectbox)
- Opciones: Siempre (1 pt), Casi siempre (2 pts), Algunas veces (3 pts), Sólo alguna vez (4 pts), Nunca (5 pts)

**Pregunta 4 de 6** — "¿Se sintió calmado y tranquilo? ¿Cuánto tiempo?"
- Tipo: **Lista desplegable**
- Opciones: Siempre (6 pts), Casi siempre (5 pts), Muchas veces (4 pts), Algunas veces (3 pts), Sólo una vez (2 pts), Nunca (1 pt)

**Pregunta 5 de 6** — "¿Tuvo mucha energía? ¿Cuánto tiempo?"
- Tipo: **Lista desplegable**
- Mismas opciones y puntuación que la pregunta 4

**Pregunta 6 de 6** — "¿Se ha sentido desanimado(a) y triste? ¿Cuánto tiempo?"
- Tipo: **Lista desplegable**
- Opciones: Siempre (1 pt), Casi siempre (2 pts), Muchas veces (3 pts), Algunas veces (4 pts), Sólo una vez (5 pts), Nunca (6 pts)

#### Validación
Si falta alguna respuesta:
> ❌ "Responda todas las preguntas de la sección mental antes de continuar."

Cuando todo está completo:
> ✅ "Componente mental completada"

El botón **"Finalizar SF-12"** calcula ambos componentes y lleva a HADS. El puntaje mental se transforma a cuartil:

| Puntaje | Cuartil |
|---------|---------|
| ≤ 15 | Q1 — Salud mental muy baja |
| 16–18 | Q2 — Salud mental baja |
| 19–21 | Q3 — Salud mental moderada |
| ≥ 22 | Q4 — Salud mental excelente |

---

### 4.6 Ansiedad — HADS

#### Encabezado
- **Título:** "Escala HADS de Ansiedad"
- **Subtítulo:** "Evaluación de síntomas de ansiedad en la última semana"

#### Tarjeta de contexto clínico
Explica la HADS como herramienta validada internacionalmente para evaluar la presencia y severidad de síntomas de ansiedad. Referencia:
> *Zigmond, A. S., & Snaith, R. P. (1983). The hospital anxiety and depression scale. Acta Psychiatrica Scandinavica, 67(6), 361-370.*

Instrucción: *"Todas las preguntas son obligatorias — Responda pensando en la última semana"*

#### Las 7 preguntas

Cada pregunta se presenta en tarjeta individual con 4 opciones como **radio buttons horizontales centrados** (st.columns [1, 3, 1]). Puntuación: 0 a 3 puntos por ítem.

| # | Pregunta | Opciones (0–3 pts) |
|---|----------|--------------------|
| 1 | Me siento tenso(a) o nervioso(a) | Nunca / A veces / Muchas veces / Todos los días |
| 2 | Todavía disfruto con lo que me ha gustado hacer | Nada / Sólo un poco / No mucho / Como siempre |
| 3 | Tengo una sensación de miedo, como si algo horrible fuera a suceder | Nada / Un poco, pero no me preocupa / Si, pero no es muy fuerte / Definitivamente y es muy fuerte |
| 4 | Puedo estar sentado(a) tranquilamente y sentirme relajado(a) | Nunca / No muy seguido / Generalmente / Siempre |
| 5 | Tengo una sensación extraña, como de aleteo o vacío en el estómago | Nunca / En ciertas ocasiones / Con bastante frecuencia / Muy seguido |
| 6 | Me siento inquieto(a), como si no pudiera parar de moverme | Nunca / No mucho / Mucho / Bastante |
| 7 | Presento una sensación de miedo muy intenso de un momento a otro | Nunca / No muy seguido / Muy frecuentemente / Bastante seguido |

#### Interpretación del puntaje total (0–21)

| Rango | Clasificación | Significado clínico |
|-------|--------------|-------------------|
| 0–7 | ✅ Riesgo Bajo | Sin indicadores significativos de ansiedad clínica |
| 8–21 | ⚠️ Riesgo de Ansiedad | Presencia de síntomas que ameritan evaluación clínica |

**Nota:** HADS no alimenta directamente al modelo predictivo MLP, pero complementa el informe clínico.

El botón **"Siguiente"** lleva a Ansiedad (ZSAS).

---

### 4.7 Ansiedad — ZSAS (Zung)

#### Encabezado
- **Título:** "Escala de Ansiedad de Zung (ZSAS)"
- **Subtítulo:** "Evaluación detallada de síntomas afectivos y somáticos de ansiedad — 20 ítems"

#### Tarjeta de contexto clínico
Explica que la ZSAS evalúa aspectos afectivos y somáticos de la ansiedad con 20 ítems. Referencia:
> *Zung, W. W. (1971). Psychosomatics, 12(6), 371-379.*

Instrucción: *"Todas las preguntas son obligatorias — Responda pensando en la última semana"*

#### Las 20 preguntas

Cada pregunta se presenta con **radio buttons horizontales centrados** (st.columns [1, 3, 1]). Las preguntas regulares (directas) se puntúan de 1 a 4. Las preguntas invertidas (formuladas en sentido positivo) invierten el orden de las opciones.

**Opciones para preguntas directas:**
1. Nunca o casi nunca (1 pt)
2. A veces (2 pts)
3. Con bastante frecuencia (3 pts)
4. Siempre o casi siempre (4 pts)

**Opciones para preguntas invertidas** (ítems 5, 9, 13, 17, 19) — las opciones aparecen en orden invertido:
1. Siempre o casi siempre (1 pt)
2. Con bastante frecuencia (2 pts)
3. A veces (3 pts)
4. Nunca o casi nunca (4 pts)

| # | Pregunta | Tipo |
|---|----------|------|
| 1 | Me siento más nervioso y ansioso de lo habitual | Directa |
| 2 | Me siento con temor sin razón | Directa |
| 3 | Me irrito con facilidad o siento pánico | Directa |
| 4 | Me siento como si fuera a reventar y partirme en pedazos | Directa |
| **5** | **Siento que todo está bien y nada malo pasará** | **Invertida** |
| 6 | Mis brazos y piernas tiemblan | Directa |
| 7 | Me mortifican los dolores de la cabeza, cuello o cintura | Directa |
| 8 | Me siento débil y me canso fácilmente | Directa |
| **9** | **Me siento tranquilo(a) y puedo permanecer en calma fácilmente** | **Invertida** |
| 10 | Puedo sentir que me late muy rápido el corazón | Directa |
| 11 | Sufro de mareos | Directa |
| 12 | Sufro de desmayos o siento que me voy a desmayar | Directa |
| **13** | **Puedo inspirar y expirar fácilmente** | **Invertida** |
| 14 | Siento hormigueo/falta de sensibilidad en los dedos de las manos y pies | Directa |
| 15 | Sufro de molestias estomacales o indigestión | Directa |
| 16 | Orino con mucha frecuencia | Directa |
| **17** | **Generalmente mis manos están secas y calientes** | **Invertida** |
| 18 | Siento bochornos / me he ruborizado con frecuencia | Directa |
| **19** | **Me quedo dormido con facilidad y descanso durante la noche** | **Invertida** |
| 20 | Tengo pesadillas | Directa |

#### Cálculo del puntaje
- **Puntaje bruto:** Suma de los 20 ítems (rango: 20–80)
- **Puntaje normalizado:** Puntaje bruto × 1.25 (rango: 25–100)

#### Interpretación

| Puntaje normalizado | Clasificación |
|--------------------|--------------|
| < 36 | ✅ Riesgo Bajo |
| ≥ 36 | ⚠️ Riesgo de Ansiedad |

**Nota:** ZSAS no alimenta directamente al modelo predictivo MLP, pero complementa el informe clínico.

El botón **"Siguiente"** lleva a la página de Resultados.

---

### 4.8 Resultados y Predicción

#### Encabezado
- **Título:** "Resultados de la Evaluación"
- **Subtítulo:** "Análisis completo del riesgo de ansiedad con interpretabilidad individual"

#### Sección 1: Resumen Clínico

La página presenta un resumen completo de todos los datos recolectados:

##### Datos Demográficos
- Métricas: Edad, Género, Educación (en columnas de 3)

##### Eventos Vitales (LTE-12)
- Métrica: Número de eventos estresantes (ej. "3")

##### Salud Física y Mental (SF-12)
- Dos columnas:
  - Componente Físico: puntaje numérico + mensaje interpretativo según cuartil
  - Componente Mental: puntaje numérico + mensaje interpretativo según cuartil
- Mensajes de ejemplo: "Salud Física Moderada (Q3): Nivel intermedio, oportunidades de mejora con ejercicio."

##### Ansiedad HADS
- Dos métricas: Puntaje y Nivel (ej. "12" y "⚠️ Riesgo de Ansiedad")

##### Ansiedad de Zung (ZSAS)
- Dos métricas: Puntaje bruto y Nivel

##### Perfil Genético
- Si se usó: tags con genotipos (ej. "PRKCA: C/T", "TCF4: A/A", "CDH20: G/G")
- Si no se usó: nota indicando "Módulo genético no utilizado en esta evaluación"

##### DataFrame Completo
- Tabla con todos los datos transformados del registro actual

#### Sección 2: Predicción de Riesgo

##### Panel genético (toggle)
- **Toggle:** "Incluir panel genético (modelo extendido, 22 features)"
  - **Desactivado (por defecto):** Se usa el modelo estándar con 13 features
  - **Activado:** Aparecen 3 selectbox para seleccionar genotipos:
    - PRKCA: C/C, C/T, T/T
    - TCF4: A/A, A/T, T/T
    - CDH20: A/A, A/G, G/G

##### Botón de cálculo
- **"Calcular Predicción (Modo Estándar)"** o **"Calcular Predicción con Panel Genético"** (botón primario, ancho completo)

Al presionar, el sistema:
1. Transforma todas las variables al formato one-hot requerido por el modelo
2. Muestra una tabla con las **features transformadas** y sus valores
3. Ejecuta la predicción con el modelo MLP correspondiente
4. Calcula la probabilidad de riesgo

##### Resultado de riesgo
Se muestra un panel destacado con:
- **Nivel de riesgo** en letras grandes: "BAJO", "MODERADO" o "ALTO" con color correspondiente:
  - 🟢 Verde para Bajo
  - 🟡 Ámbar/naranja para Moderado
  - 🔴 Rojo para Alto
- **Probabilidad:** Porcentaje exacto (ej. "23.4%")
- **Barra de riesgo visual (gauge):** Degradado verde→amarillo→rojo con marcador en la posición correspondiente
- **Modelo usado:** "Estándar (13 features)" o "Extendido (22 features)"

##### Umbrales de clasificación

| Probabilidad | Nivel | Color |
|-------------|-------|-------|
| 0.00 – 0.29 | **Bajo** | Verde |
| 0.30 – 0.59 | **Moderado** | Ámbar |
| 0.60 – 1.00 | **Alto** | Rojo |

#### Sección 3: Metodología del Modelo Predictivo

Dos tarjetas en columnas paralelas:

**Columna izquierda — 🧠 Red Neuronal MLP (Perceptrón Multicapa):**
Explica que el MLP procesa variables clínicas, demográficas y genéticas a través de múltiples capas de neuronas interconectadas, capturando relaciones no lineales complejas entre factores de riesgo. Indica el modo actual del modelo.

**Columna derecha — 📈 Curva ROC y Validación:**
Explica la Curva ROC como herramienta estándar de evaluación, la relación Sensibilidad vs. 1-Especificidad, y el AUC-ROC como métrica resumen (0.5 = azar, 1.0 = perfecto).

**Expansor "📊 Métricas de Rendimiento del Modelo":**
Tabla con métricas, descripciones e interpretaciones:

| Métrica | Descripción | Interpretación |
|---------|-------------|----------------|
| AUC-ROC | Área bajo la curva ROC | Capacidad global de discriminación |
| Sensibilidad | Positivos correctamente detectados | ¿Cuántos de alto riesgo identifica? |
| Especificidad | Negativos correctamente clasificados | ¿Cuántos sanos clasifica bien? |
| Precisión | Positivos entre todas las predicciones positivas | Fiabilidad del nivel alto |
| F1-Score | Media armónica de Precisión y Sensibilidad | Balance entre métricas |
| Exactitud | Predicciones correctas / total | Rendimiento general |
| Índice de Youden | Sensibilidad + Especificidad – 1 | Umbral óptimo binario |

#### Sección 4: Análisis SHAP

Se genera automáticamente tras la predicción:

- **Gráfico de barras horizontales** ordenado por magnitud:
  - 🔴 **Barras rojas** (hacia la derecha): Factores que **aumentan** el riesgo
  - 🟢 **Barras verdes** (hacia la izquierda): Factores que **disminuyen** el riesgo
  - La longitud de la barra indica la magnitud del impacto

- **Tabla detallada** con:
  - Nombre de la feature
  - Valor SHAP numérico
  - Efecto (Aumenta riesgo / Disminuye riesgo)
  - Interpretación clínica

#### Sección 5: Descargar Reporte PDF

Botón centrado **"📄 Descargar Reporte PDF Completo"** (primario, ancho completo). Solo aparece después de calcular la predicción.

El nombre del archivo se genera automáticamente usando el nombre del paciente:
```
NombreApellido_resultadoansiedad.pdf
```

#### Navegación
- **"Volver a Ansiedad (ZSAS)"** — Permite corregir la última sección
- **"Nueva Evaluación"** — Borra todos los datos de la sesión y vuelve al inicio

#### Nota clínica final
Aviso permanente al pie de la página:
> "Esta herramienta proporciona un análisis preliminar basado en modelos de aprendizaje automático supervisado. Los resultados deben ser interpretados en el contexto clínico completo del paciente."

---

## 5. Análisis Masivo (CSV)

El módulo de análisis masivo permite procesar **múltiples pacientes simultáneamente** cargando un archivo CSV.

### Acceso
- Desde la página de inicio: botón **"Análisis Masivo (CSV)"**
- Desde la barra lateral cuando está en modo masivo: botón **"Volver al Inicio"**

### Paso 1: Descargar Plantilla CSV

Se ofrece un botón **"Descargar Plantilla CSV"** que descarga un archivo con 3 filas de ejemplo y todas las columnas requeridas. Debajo, un expansor **"Descripción de columnas"** muestra la tabla completa:

| Columna | Tipo | Descripción | Rango válido |
|---------|------|-------------|-------------|
| `nombre` | Texto | Nombre completo del paciente | — |
| `edad` | Numérico | Edad en años | 1–120 |
| `genero` | Texto | Género del paciente | "Masculino" o "Femenino" |
| `años_educacion` | Numérico | Años de educación formal | 0–(edad-5) |
| `hads_score` | Numérico | Puntuación total HADS | 0–42 (>8 indica riesgo) |
| `zsas_score` | Numérico | Puntuación total ZSAS | 20–80 (>36 indica riesgo) |
| `sf12_fisica` | Numérico | Puntuación SF-12 Física | 0–100 |
| `sf12_mental` | Numérico | Puntuación SF-12 Mental | 0–100 |
| `lte12_count` | Numérico | Número de eventos vitales | 0–12 |
| `prkca` | Texto | *(Opcional)* Genotipo PRKCA | T/T, C/T, C/C |
| `tcf4` | Texto | *(Opcional)* Genotipo TCF4 | A/A, A/T, T/T |
| `cdh20` | Texto | *(Opcional)* Genotipo CDH20 | A/A, A/G, G/G |

Si las columnas genéticas están vacías o contienen "N/A", se usa automáticamente el **modelo estándar (13 features)**. Si contienen valores válidos, se usa el **modelo extendido (22 features)**.

### Paso 2: Datos del Profesional Evaluador

Campos opcionales idénticos a los de la evaluación individual:
- Nombre del profesional, Cargo, Institución, Registro profesional
- Claves de sesión independientes (`masivo_prof_nombre`, etc.)

### Paso 3: Cargar Archivo CSV

- **Componente de carga:** `st.file_uploader` que acepta archivos `.csv`
- El sistema valida: presencia de columnas obligatorias, tipos de datos, rangos válidos
- Si hay errores, muestra una lista detallada de problemas encontrados

### Paso 4: Procesamiento

- Cada fila se procesa individualmente:
  1. Transformación de variables (edad→EDAD24, educación→AEFGROUPS, LTE12→one-hot, SF12→cuartiles→one-hot, genotipos→one-hot)
  2. Predicción con el modelo MLP correspondiente
  3. Clasificación triclásica (Bajo/Moderado/Alto)
  4. Cálculo SHAP (si disponible)

### Paso 5: Resultados

- **Tabla resumen:** Nombre, probabilidad, nivel de riesgo, modelo usado
- **Descarga:** Botones para descargar resultados en **CSV** o **Excel** (.xlsx)

---

## 6. Reporte PDF

El reporte PDF se genera con la librería **ReportLab** y contiene 9 secciones profesionales:

| Sección | Contenido |
|---------|-----------|
| **1. Datos Demográficos** | Tabla con nombre, edad, género, años de educación |
| **2. Eventos Vitales (LTE-12)** | Lista con viñetas de los 12 eventos, marcando cuáles fueron afirmativos. Incluye explicación clínica del modelo diathesis-stress |
| **3. Salud Física y Mental (SF-12)** | Tabla con puntajes brutos, cuartiles y mensajes interpretativos para ambos componentes |
| **4. Ansiedad HADS** | Tabla con puntaje, nivel de riesgo y explicación clínica de la escala |
| **5. Ansiedad ZSAS** | Tabla con puntaje bruto, puntaje normalizado, nivel y explicación clínica |
| **6. Perfil Genético** | Tabla de genotipos (PRKCA, TCF4, CDH20) o nota de "no utilizado" |
| **7. Metodología y Predicción** | 4 subsecciones: 7.1 Arquitectura MLP, 7.2 Curva ROC y tabla de métricas, 7.3 Tabla de umbrales triclásicos, 7.4 Resultado de predicción con probabilidad y recomendación clínica |
| **8. Análisis SHAP** | Gráfico de barras embebido como imagen PNG + tabla detallada de contribuciones |
| **9. Resumen Clínico Integrado** | Síntesis de hallazgos + nota clínica legal + bloque de firma del profesional (línea de firma, nombre, cargo, institución, registro) |

### Características del PDF
- **Tamaño:** Carta (Letter)
- **Fuentes:** Helvetica y Helvetica-Bold
- **Colores:** Alineados con la paleta de la app (encabezados en ámbar dorado)
- **Textos largos:** Usa `Paragraph()` de ReportLab para evitar desbordamiento
- **Nombre del archivo:** `NombrePaciente_resultadoansiedad.pdf`

---

## 7. Privacidad, Seguridad y Habeas Data

### Tratamiento de datos
- Todos los datos se procesan **exclusivamente en la sesión del navegador**
- **No se almacenan** datos en servidores externos ni bases de datos permanentes
- Al cerrar la sesión del navegador, todos los datos se eliminan automáticamente
- Los reportes descargados (PDF) quedan bajo la custodia del profesional responsable

### Marco legal
El sistema cumple con:
- **Ley 1581 de 2012** — Régimen General de Protección de Datos Personales (Colombia)
- **Decreto 1377 de 2013** — Reglamentario de la Ley 1581 de 2012
- **Ley 1266 de 2008** — Habeas Data
- **Resolución 8430 de 1993** — Investigación en salud

### Derechos del titular
Conforme a la Ley 1581 de 2012, el titular tiene derecho a:
- Conocer, actualizar y rectificar sus datos personales
- Solicitar prueba de la autorización otorgada
- Ser informado sobre el uso de sus datos
- Revocar la autorización y/o solicitar la supresión de datos
- Acceder gratuitamente a sus datos personales

### Consentimiento
El profesional de salud que utiliza la herramienta declara que cuenta con la autorización previa, expresa e informada del paciente para el tratamiento de sus datos personales y de salud.

---

## 8. Solución de Problemas

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| La aplicación no carga en el navegador | Servidor Streamlit no ejecutándose | Ejecute `streamlit run app.py` y verifique que el terminal muestra "You can now view your Streamlit app in your browser" |
| Error "módulo no encontrado" (ModuleNotFoundError) | Dependencias no instaladas | Ejecute `pip install -r requirements.txt` |
| Puerto 8501 ocupado | Otra instancia de Streamlit activa | Use `streamlit run app.py --server.port 8502` o cierre la otra instancia |
| El botón de PDF no aparece | No se ha calculado la predicción | Presione primero el botón "Calcular Predicción" en la página de Resultados |
| Error al generar PDF | Modelo no encontrado o datos incompletos | Verifique que los archivos `.joblib` existen en `src/models/` y que todos los cuestionarios están completos |
| Los radio buttons aparecen desalineados | Caché del navegador con CSS antiguo | Presione Ctrl+Shift+R (recarga forzada) para limpiar la caché |
| El sistema redirige a una sección anterior | Falta completar una sección obligatoria | Complete todas las secciones en orden secuencial; no es posible saltar pasos |
| Error al cargar CSV en análisis masivo | Formato incorrecto o columnas faltantes | Descargue la plantilla CSV y úsela como referencia para la estructura del archivo |
| Los campos de edad y educación aparecen vacíos | Diseño intencional (sin valor por defecto) | Ingrese manualmente los valores; los campos usan placeholder en lugar de valor 0 |
| Error "Modelo no encontrado" | Archivo .joblib faltante o ruta incorrecta | Verifique que `src/models/anxrisk_mlp_model_standard.joblib` y `anxrisk_mlp_model_extended.joblib` están presentes |

---

## 9. Situaciones de Crisis

> **⚠️ Si durante la evaluación el paciente experimenta una crisis de ansiedad severa, ideación suicida o pensamientos de autolesión, suspenda la evaluación inmediatamente y contacte los servicios de emergencia o la línea de crisis de salud mental de su localidad.**

### Recursos de emergencia (Colombia)
- **Línea 106** — Línea de orientación y atención en crisis
- **Línea 123** — Emergencias
- **Línea 141** — ICBF (menores de edad)

---

**© 2025 Breyner Joel Quiñones Castro. Todos los derechos reservados.**

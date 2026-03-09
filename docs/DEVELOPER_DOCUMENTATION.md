# Documentación Técnica para Desarrolladores — ANXRISK

## Arquitectura General

ANXRISK es una aplicación web construida con **Streamlit** que sigue un patrón de navegación por páginas con estado persistente en `st.session_state`.

### Flujo de datos

```
Formularios (páginas) → st.session_state → Modelo MLP → Predicción + SHAP → PDF
```

1. Cada página recopila datos y los almacena en `st.session_state`
2. La página de Resultados construye el vector de features desde `st.session_state`
3. El modelo MLP genera la probabilidad de riesgo
4. SHAP calcula las contribuciones individuales
5. ReportLab genera el PDF con todos los datos

---

## Estructura del Código Fuente

```
src/
├── config.py                   # Configuración centralizada
├── pages/                      # Módulos de interfaz
│   ├── __init__.py             # Exporta funciones de cada página
│   ├── home.py                 # Página de inicio (logo SVG, guía de uso)
│   ├── demograficos.py         # Datos del paciente + profesional evaluador
│   ├── eventos_vitales.py      # LTE-12 (12 radios centrados con st.columns)
│   ├── sf12_fisica.py          # SF-12 físico (5 preguntas)
│   ├── sf12_mental.py          # SF-12 mental (2 preguntas)
│   ├── hads.py                 # HADS (7 preguntas)
│   ├── zsas.py                 # ZSAS (20 preguntas)
│   ├── resultados.py           # Predicción MLP, SHAP, generación PDF
│   └── analisis_masivo.py      # Procesamiento por lotes CSV
├── utils/
│   ├── calculos.py             # Transformaciones de features
│   └── dataframe_manager.py    # Gestión del registro en session_state
├── models/                     # Archivos .joblib de modelos entrenados
└── assets/
    ├── img/logo.png
    ├── styles/main.css         # ~1100 líneas de CSS personalizado
    └── guia_uso.html           # Guía de uso embebida
```

---

## Configuración Centralizada (`src/config.py`)

```python
# Rutas de modelos
MODEL_STANDARD_PATH = "src/models/anxrisk_mlp_model_standard.joblib"
MODEL_EXTENDED_PATH = "src/models/anxrisk_mlp_model_extended.joblib"

# Orden canónico de features
FEATURES_STANDARD = [  # 13 features
    'EDAD24', 'AEFGROUPS',
    'LTE12_0', 'LTE12_1', 'LTE12_2',
    'SF12F_Q1', 'SF12F_Q2', 'SF12F_Q3', 'SF12F_Q4',
    'SF12M_Q1', 'SF12M_Q2', 'SF12M_Q3', 'SF12M_Q4',
]

FEATURES_EXTENDED = FEATURES_STANDARD + [  # 22 features
    'PRKCA_C/C', 'PRKCA_C/T', 'PRKCA_T/T',
    'TCF4_A/A', 'TCF4_A/T', 'TCF4_T/T',
    'CDH20_A/A', 'CDH20_A/G', 'CDH20_G/G',
]

# Umbrales triclásicos
THRESHOLD_LOW = 0.30
THRESHOLD_HIGH = 0.60
```

---

## Aplicación Principal (`app.py`)

### Responsabilidades
- Configura `st.set_page_config()` con `layout="wide"`
- Carga CSS desde `src/assets/styles/main.css`
- Inyecta CSS inline para centrado de radio buttons
- Gestiona la navegación mediante `st.session_state.pagina_actual`
- Renderiza la barra lateral con progreso y botones de navegación

### CSS para radio buttons

El centrado de radio buttons en Streamlit 1.51 **no funciona con CSS externo** (los estilos emotion de Streamlit no se pueden sobreescribir). La solución es usar `st.columns([1, 2, 1])` o `[1, 3, 1]` en Python para envolver cada `st.radio()` en la columna central.

---

## Páginas del Sistema

### `demograficos.py`

- **Campos del paciente:** nombre (text_input), edad (number_input, value=None), género (selectbox), educación (number_input, value=None)
- **Campos del profesional:** nombre, cargo, institución, registro profesional
- **Validaciones:** campos obligatorios, edad > 0, educación ≤ edad – 5
- **Estado:** guarda en `st.session_state["datos_demograficos"]`
- Los datos del profesional se guardan en claves individuales de session_state (`prof_nombre`, `prof_cargo`, etc.)

### `eventos_vitales.py`

- 12 preguntas Sí/No centradas con `st.columns([1, 2, 1])`
- Guarda total y detalle en `st.session_state.resultados['eventos_vitales']`

### `sf12_fisica.py` y `sf12_mental.py`

- Preguntas con opciones Likert centradas con `st.columns([1, 3, 1])`
- Calcula puntaje bruto y cuartil
- SF-12 físico: 5 preguntas, SF-12 mental: 2 preguntas

### `hads.py`

- 7 preguntas con 4 opciones (0–3 puntos) centradas con `st.columns([1, 3, 1])`
- Puntaje total: 0–21
- Clasifica en: Normal, Leve, Moderada, Severa

### `zsas.py`

- 20 preguntas con 4 opciones (1–4 puntos) centradas con `st.columns([1, 3, 1])`
- Ítems invertidos: 5, 9, 13, 17, 19
- Puntaje bruto: 20–80

### `resultados.py`

Archivo más extenso (~1400 líneas). Contiene:

1. **`mostrar_resultados()`** — Función principal
   - Lee datos profesionales desde session_state
   - Muestra resumen clínico con métricas
   - Toggle para panel genético (modelo extendido)
   - Botón de cálculo de predicción
   - Llama a `_mostrar_resultado_riesgo()`, `_mostrar_explicacion_modelo()`, `mostrar_shap_analysis()`
   - Botón de descarga PDF

2. **`_mostrar_resultado_riesgo()`** — Barra visual de riesgo con CSS

3. **`_mostrar_explicacion_modelo()`** — Sección de metodología MLP y ROC con tabla de métricas

4. **`mostrar_shap_analysis()`** — Gráfico SHAP + tabla de contribuciones

5. **`generar_pdf_resultados()`** — Genera PDF con ReportLab (9 secciones + firma)

### `analisis_masivo.py`

- Descarga de plantilla CSV
- Campos del profesional evaluador (claves `masivo_prof_*`)
- Carga y validación de CSV
- Procesamiento con `calcular_riesgo_paciente()` por fila
- Tabla de features one-hot
- Integración SHAP masiva (si disponible)
- Descarga de resultados en CSV/Excel

---

## Funciones de Cálculo (`src/utils/calculos.py`)

| Función | Descripción |
|---------|-------------|
| `transformar_edad_a_grupo(edad)` | 0 si edad ≤ 24, 1 si > 24 |
| `transformar_educacion_a_binaria(años)` | 0 si ≤ 14 años, 1 si ≥ 15 |
| `transformar_genero_a_binario(genero)` | 0 = Masculino, 1 = Femenino |
| `transformar_lte12_a_clasificacion(total)` | 0, 1, o 2 (≥2 eventos) |
| `transformar_sf12_fisica_a_cuartil(puntaje)` | Cuartil 1–4 según umbrales |
| `transformar_sf12_mental_a_cuartil(puntaje)` | Cuartil 1–4 según umbrales |
| `clasificar_por_youden(proba, umbral)` | Bajo/Moderado/Alto con umbrales fijos |

---

## Generación del PDF

El PDF se genera con **ReportLab** en la función `generar_pdf_resultados()`:

- **Tamaño:** Letter
- **Fuentes:** Helvetica / Helvetica-Bold
- **Colores:** Alineados con la paleta de la app (#D4911D, #2D2D2D, etc.)
- **Tablas:** `Table` con estilos personalizados
- **Texto largo:** Usa `Paragraph()` para evitar desbordamiento
- **Gráfico SHAP:** Generado con matplotlib, embebido como imagen PNG
- **Firma:** Bloque con línea, nombre del profesional, cargo, institución y registro

### Secciones del PDF

1. Datos Demográficos (tabla)
2. Eventos Vitales LTE-12 (viñetas con explicación)
3. SF-12 Física y Mental (tabla + cuartiles + interpretación)
4. HADS (tabla + nivel + explicación clínica)
5. ZSAS (tabla + nivel + explicación clínica)
6. Perfil Genético (tabla de genotipos)
7. Metodología y Predicción (subsecciones 7.1–7.4: MLP, ROC, umbrales, resultado + recomendación)
8. Análisis SHAP (gráfico + tabla detallada)
9. Resumen Clínico Integrado + Nota clínica + Firma

---

## Sistema de Estilos CSS

El archivo `src/assets/styles/main.css` (~1100 líneas) define:

- **Variables CSS:** `--primary`, `--surface`, `--text`, `--border`, etc.
- **Tipografía:** Figtree importada de Google Fonts
- **Componentes:** `.anxrisk-card`, `.anxrisk-result-header`, `.anxrisk-risk-gauge`, `.anxrisk-stats-bar`, etc.
- **Responsive:** Adaptado a diferentes tamaños de pantalla
- **Radio buttons:** Selectores con `data-testid` (efecto limitado, centrado real con st.columns)

---

## Dependencias

Versiones fijadas para reproducibilidad de métricas del modelo (Patente §0022):

```
streamlit==1.29.0
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
joblib==1.3.2
shap==0.44.1
reportlab==4.0.9
matplotlib==3.8.2
openpyxl==3.1.2
scipy==1.11.4
```

> **Nota:** `lightgbm`, `xgboost` y `catboost` NO se incluyen en producción. La app solo usa el modelo MLP pre-entrenado (`.joblib`). Estas librerías solo se necesitan en el pipeline de entrenamiento (Colab).

---

## Despliegue

### Streamlit Community Cloud

El proyecto se despliega desde la rama `main` del repositorio GitHub:
- Repositorio: `github.com/joelquinonesc/appProyecto`
- Rama: `main`
- Archivo principal: `app.py`

Para desplegar cambios: `git push origin main` — Streamlit Cloud reconstruye automáticamente.

---

## Convenciones de Código

- **Variables y funciones:** `snake_case`
- **Clases:** `PascalCase`
- **Constantes:** `UPPER_CASE`
- **Docstrings:** En español, formato Google
- **Session state keys:** descriptivos, sin prefijo (ej. `prof_nombre`, `datos_demograficos`)

---

**© 2025 Breyner Joel Quiñones Castro. Todos los derechos reservados.**

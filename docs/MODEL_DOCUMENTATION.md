# Documentación del Modelo — ANXRISK

## Descripción General

ANXRISK utiliza un **Perceptrón Multicapa (MLP)** de la librería scikit-learn para predecir el riesgo de desarrollar trastornos de ansiedad. El sistema opera con dos variantes del modelo según la disponibilidad de datos genéticos.

---

## Variantes del Modelo

| Variante | Archivo | Features | Uso |
|----------|---------|----------|-----|
| **Estándar** | `anxrisk_mlp_model_standard.joblib` | 13 | Sin datos genéticos |
| **Extendido** | `anxrisk_mlp_model_extended.joblib` | 22 | Con panel genético (3 SNPs) |

Ambos modelos se almacenan en `src/models/` y se cargan con `joblib.load()`.

---

## Arquitectura MLP

El MLP (Multi-Layer Perceptron) es una red neuronal artificial compuesta por capas de neuronas interconectadas:

- **Capa de entrada:** 13 ó 22 neuronas (según variante)
- **Capas ocultas:** Configuración optimizada durante el entrenamiento con búsqueda de hiperparámetros
- **Capa de salida:** 1 neurona con función sigmoide (probabilidad 0–1)
- **Función de activación:** ReLU en capas ocultas
- **Optimizador:** Adam
- **Implementación:** `sklearn.neural_network.MLPClassifier`

### ¿Por qué MLP?

- Captura relaciones no lineales entre factores de riesgo
- Maneja eficientemente combinaciones de variables categóricas y continuas
- Produce probabilidades calibradas útiles para clasificación triclásica
- Balance óptimo entre complejidad y rendimiento para el tamaño del dataset

---

## Features de Entrada

### Modelo Estándar (13 features)

| # | Feature | Tipo | Origen | Descripción |
|---|---------|------|--------|-------------|
| 1 | `EDAD24` | Binaria | Demográficos | 0 = ≤ 24 años, 1 = > 24 años |
| 2 | `AEFGROUPS` | Binaria | Demográficos | 0 = ≤ 14 años educación, 1 = ≥ 15 años |
| 3 | `LTE12_0` | One-hot | LTE-12 | 0 eventos vitales estresantes |
| 4 | `LTE12_1` | One-hot | LTE-12 | 1 evento vital estresante |
| 5 | `LTE12_2` | One-hot | LTE-12 | 2 o más eventos vitales estresantes |
| 6 | `SF12F_Q1` | One-hot | SF-12 Física | Cuartil 1 (puntaje ≤ 15) |
| 7 | `SF12F_Q2` | One-hot | SF-12 Física | Cuartil 2 (puntaje 16–17) |
| 8 | `SF12F_Q3` | One-hot | SF-12 Física | Cuartil 3 (puntaje 18–19) |
| 9 | `SF12F_Q4` | One-hot | SF-12 Física | Cuartil 4 (puntaje ≥ 20) |
| 10 | `SF12M_Q1` | One-hot | SF-12 Mental | Cuartil 1 (puntaje ≤ 15) |
| 11 | `SF12M_Q2` | One-hot | SF-12 Mental | Cuartil 2 (puntaje 16–18) |
| 12 | `SF12M_Q3` | One-hot | SF-12 Mental | Cuartil 3 (puntaje 19–21) |
| 13 | `SF12M_Q4` | One-hot | SF-12 Mental | Cuartil 4 (puntaje ≥ 22) |

### Features Adicionales del Modelo Extendido (+9)

| # | Feature | Tipo | Gen | Descripción |
|---|---------|------|-----|-------------|
| 14 | `PRKCA_C/C` | One-hot | PRKCA | Genotipo homocigoto C/C |
| 15 | `PRKCA_C/T` | One-hot | PRKCA | Genotipo heterocigoto C/T |
| 16 | `PRKCA_T/T` | One-hot | PRKCA | Genotipo homocigoto T/T |
| 17 | `TCF4_A/A` | One-hot | TCF4 | Genotipo homocigoto A/A |
| 18 | `TCF4_A/T` | One-hot | TCF4 | Genotipo heterocigoto A/T |
| 19 | `TCF4_T/T` | One-hot | TCF4 | Genotipo homocigoto T/T |
| 20 | `CDH20_A/A` | One-hot | CDH20 | Genotipo homocigoto A/A |
| 21 | `CDH20_A/G` | One-hot | CDH20 | Genotipo heterocigoto A/G |
| 22 | `CDH20_G/G` | One-hot | CDH20 | Genotipo homocigoto G/G |

---

## Transformación de Variables

### Edad → `EDAD24`

```
edad ≤ 24 → 0
edad > 24 → 1
```

### Educación → `AEFGROUPS`

```
años_educacion ≤ 14 → 0
años_educacion ≥ 15 → 1
```

### LTE-12 → `LTE12_0`, `LTE12_1`, `LTE12_2`

El total de eventos vitales (0–12) se clasifica:

| Total eventos | Clase | LTE12_0 | LTE12_1 | LTE12_2 |
|---------------|-------|---------|---------|---------|
| 0 | 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 1 | 0 |
| 2+ | 2 | 0 | 0 | 1 |

### SF-12 Física → Cuartiles `SF12F_Q1`–`SF12F_Q4`

| Puntaje | Cuartil | Q1 | Q2 | Q3 | Q4 |
|---------|---------|----|----|----|----|
| ≤ 15 | 1 | 1 | 0 | 0 | 0 |
| 16–17 | 2 | 0 | 1 | 0 | 0 |
| 18–19 | 3 | 0 | 0 | 1 | 0 |
| ≥ 20 | 4 | 0 | 0 | 0 | 1 |

### SF-12 Mental → Cuartiles `SF12M_Q1`–`SF12M_Q4`

| Puntaje | Cuartil | Q1 | Q2 | Q3 | Q4 |
|---------|---------|----|----|----|----|
| ≤ 15 | 1 | 1 | 0 | 0 | 0 |
| 16–18 | 2 | 0 | 1 | 0 | 0 |
| 19–21 | 3 | 0 | 0 | 1 | 0 |
| ≥ 22 | 4 | 0 | 0 | 0 | 1 |

### Genotipos → One-Hot

Cada gen (PRKCA, TCF4, CDH20) tiene 3 alelos posibles, codificados en 3 columnas one-hot (solo una es 1, las demás 0).

---

## Clasificación Triclásica

La salida del MLP es una probabilidad continua entre 0 y 1. Se clasifica en tres niveles usando umbrales fijos:

| Nivel | Rango de probabilidad | Color en la app |
|-------|----------------------|-----------------|
| **Bajo** | p < 0.30 | Verde |
| **Moderado** | 0.30 ≤ p < 0.60 | Ámbar/Naranja |
| **Alto** | p ≥ 0.60 | Rojo |

Estos umbrales están definidos en `src/config.py`:

```python
THRESHOLD_LOW = 0.30
THRESHOLD_HIGH = 0.60
```

---

## Curva ROC y Métricas

### Curva ROC (Receiver Operating Characteristic)

La curva ROC representa la capacidad discriminativa del modelo graficando la **Sensibilidad** (tasa de verdaderos positivos) contra **1 – Especificidad** (tasa de falsos positivos) para todos los umbrales de decisión.

- **AUC = 1.0:** Discriminación perfecta
- **AUC = 0.5:** Sin capacidad discriminativa (azar)
- **AUC ≥ 0.90:** Considerado excelente en contexto clínico

### Métricas de Rendimiento

| Métrica | Definición |
|---------|------------|
| **Exactitud (Accuracy)** | Proporción de predicciones correctas sobre el total |
| **Precisión** | Proporción de verdaderos positivos entre todas las predicciones positivas |
| **Sensibilidad (Recall)** | Proporción de positivos correctamente identificados (minimiza falsos negativos) |
| **Especificidad** | Proporción de negativos correctamente identificados (minimiza falsos positivos) |
| **F1-Score** | Media armónica entre Precisión y Sensibilidad |
| **AUC** | Área Bajo la Curva ROC (capacidad discriminativa global) |
| **Índice de Youden** | Sensibilidad + Especificidad – 1 (umbral óptimo para clasificación binaria) |

---

## Interpretabilidad con SHAP

### ¿Qué es SHAP?

SHAP (SHapley Additive exPlanations) es un método basado en la teoría de juegos cooperativos que asigna a cada feature una **contribución marginal** a la predicción individual.

### Implementación en ANXRISK

- **Método:** `shap.KernelExplainer` (compatible con cualquier modelo, incluido MLP)
- **Datos de referencia:** Muestra de background generada a partir de los datos de entrenamiento
- **Salida:** Valor SHAP para cada feature, indicando dirección e intensidad de su efecto

### Interpretación

| Valor SHAP | Significado |
|------------|-------------|
| Positivo alto | La feature **aumenta** significativamente el riesgo predicho |
| Positivo bajo | La feature tiene un efecto **leve** de aumento del riesgo |
| Cercano a 0 | La feature tiene **poco impacto** en esta predicción |
| Negativo bajo | La feature **reduce levemente** el riesgo predicho |
| Negativo alto | La feature **reduce significativamente** el riesgo predicho |

### Visualización

El sistema genera un gráfico de barras horizontales ordenado por magnitud absoluta del valor SHAP, con colores que indican dirección (rojo = aumenta riesgo, verde = reduce riesgo). Este gráfico se incluye tanto en la interfaz web como en el PDF de resultados.

---

## Instrumentos Clínicos Integrados

### LTE-12 (List of Threatening Experiences)

- 12 preguntas Sí/No sobre eventos vitales estresantes
- Evalúa: enfermedad grave, duelo, divorcio, desempleo, etc.
- Rango: 0–12 eventos

### SF-12 (Short Form Health Survey – 12 ítems)

- **Componente físico (PCS):** 5 preguntas sobre salud física general
- **Componente mental (MCS):** 2 preguntas sobre bienestar emocional
- Ambos componentes se transforman a cuartiles para el modelo

### HADS (Hospital Anxiety and Depression Scale)

- 7 preguntas enfocadas en ansiedad
- Escala: 0–3 por ítem, total 0–21
- Clasificación: Normal (0–7), Leve (8–10), Moderada (11–14), Severa (15–21)
- **No se usa como feature del MLP**, pero complementa el informe clínico

### ZSAS (Zung Self-Rating Anxiety Scale)

- 20 preguntas con 4 opciones (1–4 puntos)
- Ítems invertidos: 5, 9, 13, 17, 19
- Puntaje bruto: 20–80
- **No se usa como feature del MLP**, pero complementa el informe clínico

---

## Pipeline de Predicción

```
1. Recolectar datos del paciente (st.session_state)
2. Transformar variables:
   - edad → EDAD24 (binaria)
   - educación → AEFGROUPS (binaria)
   - LTE-12 total → clasificación → one-hot (3 columnas)
   - SF-12 física → cuartil → one-hot (4 columnas)
   - SF-12 mental → cuartil → one-hot (4 columnas)
   - [Opcional] Genotipos → one-hot (9 columnas)
3. Construir vector de features en orden canónico (config.py)
4. Crear DataFrame con nombres de columnas exactos
5. Cargar modelo (.joblib) con joblib.load()
6. Ejecutar model.predict_proba(X)[:, 1] → probabilidad
7. Clasificar: Bajo / Moderado / Alto según umbrales
8. Ejecutar SHAP KernelExplainer para interpretabilidad
9. Generar PDF con todos los resultados
```

---

## Notas Importantes

- **HADS y ZSAS** no alimentan al modelo MLP directamente; se incluyen en el informe como contexto clínico complementario.
- Las features del modelo están codificadas en **one-hot**, lo que significa que cada variable categórica se descompone en columnas binarias mutuamente excluyentes.
- El orden de las features en el vector de entrada debe coincidir **exactamente** con el orden definido en `src/config.py` (`FEATURES_STANDARD` o `FEATURES_EXTENDED`).
- Los modelos fueron entrenados con un dataset de 234 participantes.
- La selección del modelo (estándar vs. extendido) se hace automáticamente según la disponibilidad de datos genéticos.

---

**© 2025 Breyner Joel Quiñones Castro. Todos los derechos reservados.**

## 📊 Integración SHAP en Análisis Masivos

### 🎯 Descripción General

Se ha integrado el análisis SHAP (SHapley Additive exPlanations) directamente en el módulo de análisis masivos. En lugar de generar gráficas separadas, el sistema ahora **muestra las 5 características más importantes con sus valores SHAP directamente en la tabla de resultados**.

---

## ✨ Características Principales

### 1. **Cálculo Automático de SHAP**
- Cuando procesas un lote de pacientes, el sistema calcula automáticamente los valores SHAP
- Identifica las **5 características más importantes** que influyen en el riesgo predicho
- Se realiza de forma eficiente usando solo 30 muestras de background

### 2. **Tabla de Resultados Mejorada**
La tabla de resultados ahora incluye:
- ✅ **nombre**: Nombre del paciente
- ✅ **riesgo_predicho**: Valor numérico de riesgo (0-1)
- ✅ **categoria_riesgo**: Bajo/Moderado/Alto
- ✅ **SHAP_[Característica1]**: Valor SHAP para característica #1
- ✅ **SHAP_[Característica2]**: Valor SHAP para característica #2
- ✅ **SHAP_[Característica3]**: Valor SHAP para característica #3
- ✅ **SHAP_[Característica4]**: Valor SHAP para característica #4
- ✅ **SHAP_[Característica5]**: Valor SHAP para característica #5

### 3. **Panel de Top 5 Características**
Se muestra un panel visual con las 5 características más importantes y su promedio de SHAP:
```
#1: SF12M_Q1      SHAP: 0.1234
#2: LTE12_1       SHAP: 0.1089
#3: HADS_Score    SHAP: 0.0987
#4: SF12F_Q2      SHAP: 0.0876
#5: EDAD24        SHAP: 0.0765
```

---

## 📈 Interpretación de Valores SHAP

### ¿Qué es un valor SHAP?
- **SHAP (SHapley Additive exPlanations)** mide la **contribución de cada característica a la predicción**
- Un valor SHAP **positivo** → empuja la predicción hacia más riesgo
- Un valor SHAP **negativo** → empuja la predicción hacia menos riesgo
- Un valor SHAP **cercano a cero** → poca influencia en la predicción

### Ejemplo de Interpretación
Si para el paciente "Juan Pérez" tenemos:
- `SHAP_SF12M_Q1 = 0.0523`  → SF-12 Mental Q1 contribuye +0.0523 al riesgo
- `SHAP_LTE12_1 = -0.0301`   → LTE12_1 contribuye -0.0301 al riesgo (protector)

---

## 🔧 Integración Técnica

### Componentes Principales

#### 1. **shap_integration_masivo.py**
Script que maneja todo el cálculo de SHAP:
```python
def main_shap_integration(df):
    # Procesa datos
    # Calcula valores SHAP
    # Retorna df con columnas SHAP añadidas
    # Top 5 características
```

#### 2. **Funciones Clave**

**`procesar_datos_para_modelo(df)`**
- Convierte datos raw en 22 features (EDAD24, AEFGROUPS, LTE12_0-2, SF12F_Q1-Q4, SF12M_Q1-Q4, PRKCA, TCF4, CDH20)
- Aplica One-Hot Encoding
- Mantiene orden exacto del modelo Naive Bayes (extendido)

**`calcular_shap_values(model, X_background, X_test)`**
- Usa explainer adaptativo (TreeExplainer si es posible, sino KernelExplainer)
- Usa background reducido (30 muestras) para rapidez
- Retorna valores SHAP para cada paciente

**`crear_columnas_shap_para_resultados(df, X, shap_values, top5_idx)`**
- Agrega 5 nuevas columnas al DataFrame: `SHAP_[Feature]`
- Redondea valores a 4 decimales
- Facilita exportación a CSV/Excel

---

## ⚡ Rendimiento

### Tiempos Estimados
- **10 pacientes**: ~8-12 segundos
- **50 pacientes**: ~15-20 segundos
- **100 pacientes**: ~25-35 segundos
- **500+ pacientes**: ~60-90 segundos

### Optimizaciones
✅ Background reducido (30 muestras vs 100)
✅ Explainer adaptativo (elige el más rápido automáticamente)
✅ Sin gráficas costosas
✅ Cálculos vectorizados en NumPy

---

## 📥 Flujo de Datos

```
CSV con pacientes
    ↓
[analisis_masivo.py - Procesar datos]
    ↓
[shap_integration_masivo.py - Calcular SHAP]
    ↓
Tabla de resultados con 5 SHAP más importantes
    ↓
Exportar CSV/Excel con valores SHAP
```

---

## 💾 Exportación de Resultados

Los resultados incluyen:
1. **CSV**: `resultados_analisis_masivo.csv`
   - Todas las columnas: nombre, riesgo, categoría, y 5 columnas SHAP
   - Fácil de importar en Excel o análisis posterior

2. **Excel**: `resultados_analisis_masivo.xlsx`
   - Mismo formato que CSV
   - Con formato de tabla para mejor visualización

---

## 🔍 Archivos Modificados

### 1. **src/pages/analisis_masivo.py**
- Añadida integración de SHAP después de procesar pacientes
- Nueva sección: "Top 5 Características Más Importantes"
- Tabla de resultados incluye columnas SHAP
- Exportación incluye valores SHAP

### 2. **shap_integration_masivo.py** (NUEVO)
- Script independiente para cálculos SHAP
- Reutilizable desde otros módulos
- Manejo de errores robusto
- Rendimiento optimizado

---

## 🚀 Cómo Usar

### Desde la App Streamlit
1. Ve a **Análisis Masivo**
2. Carga tu CSV con datos
3. Haz clic en **"Procesar y Generar Reportes"**
4. Espera ~30 segundos (se verá barra de progreso SHAP)
5. Verás tabla con riesgo + **Top 5 SHAP**
6. Descargar CSV/Excel con los valores SHAP

### Desde Script Python
```python
from shap_integration_masivo import main_shap_integration
import pandas as pd

df = pd.read_csv('mis_pacientes.csv')
resultado = main_shap_integration(df)

# Acceder a los datos
df_con_shap = resultado['df_with_shap']
top5_nombres = resultado['top5_names']
top5_importancia = resultado['top5_importance']
```

---

## 📊 Ejemplo de Salida

### Tabla de Resultados (primera 5 filas)

| nombre | riesgo_predicho | categoria_riesgo | SHAP: SF12M_Q1 | SHAP: LTE12_1 | SHAP: HADS | SHAP: SF12F_Q2 | SHAP: EDAD24 |
|--------|-----------------|------------------|----------------|---------------|-----------|----------------|-------------|
| Juan Pérez | 0.2341 | Bajo | 0.0523 | -0.0301 | 0.0189 | 0.0156 | 0.0087 |
| María García | 0.5678 | Moderado | 0.1234 | 0.0876 | 0.0654 | 0.0432 | 0.0198 |
| Carlos López | 0.8234 | Alto | 0.2109 | 0.1876 | 0.1543 | 0.1234 | 0.0876 |

### Top 5 Panel

```
🏆 Top 5 Características Más Importantes

#1 SF12M_Q1          SHAP: 0.1456
#2 LTE12_1           SHAP: 0.1209
#3 HADS_Score        SHAP: 0.1087
#4 SF12F_Q2          SHAP: 0.0876
#5 EDAD24            SHAP: 0.0654
```

---

## ⚠️ Notas Importantes

1. **Exactitud del Orden**: Los 22 features se envían al modelo en orden exacto
2. **Background Size**: Se usa 30 muestras de background (balanza entre rapidez y precisión)
3. **Números SHAP**: Valores redondos a 4 decimales para legibilidad
4. **Características Top 5**: Se seleccionan las 5 con mayor |SHAP| promedio

---

## 🔧 Troubleshooting

### Error: "The feature names should match..."
✅ **Solución**: El script ahora normaliza los nombres automáticamente

### Error: "No se puede cargar el modelo"
✅ **Solución**: Verificar que `src/models/anxrisk_best_extended.joblib` existe

### Cálculo muy lento
✅ **Solución**: Es normal para >200 pacientes. Aumentar `background_size` si es necesario en el código

---

## 📚 Referencia de Características

Las 22 características del modelo:

**Demográficas (2)**
- EDAD24: Edad ≥24 años
- AEFGROUPS: Años educación ≥12 años

**Eventos Vitales (3)**
- LTE12_0: 0-2 eventos
- LTE12_1: 3-5 eventos  
- LTE12_2: 6+ eventos

**SF-12 Física (4)**
- SF12F_Q1-Q4: Cuartiles de SF-12 Física

**SF-12 Mental (4)**
- SF12M_Q1-Q4: Cuartiles de SF-12 Mental

**Genotipos (9)**
- PRKCA_C/C, PRKCA_C/T, PRKCA_T/T
- TCF4_A/A, TCF4_A/T, TCF4_T/T
- CDH20_A/A, CDH20_A/G, CDH20_G/G

---

## 📞 Soporte

Para preguntas o problemas:
1. Revisar los mensajes de error en la consola
2. Verificar que todos los archivos estén en su lugar
3. Probar con un dataset pequeño primero (10 pacientes)

---

**Versión**: 1.0  
**Fecha**: Noviembre 2025  
**Autor**: ANXRISK Analytics Team

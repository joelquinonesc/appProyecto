# 🔧 Documentación Técnica para Desarrolladores

## Estructura del Proyecto

### Organización de Directorios

```
ANXRISK/
├── app.py                     # Aplicación principal Streamlit
├── requirements.txt           # Dependencias del proyecto
├── README.md                 # Documentación principal
├── LICENSE                   # Términos de licencia
│
├── src/                      # Código fuente principal
│   ├── pages/               # Páginas de la aplicación
│   │   ├── __init__.py
│   │   ├── home.py          # Página de inicio
│   │   ├── demograficos.py  # Datos demográficos
│   │   ├── datos_geneticos.py # Información genética
│   │   ├── eventos_vitales.py # Cuestionario LTE-12
│   │   ├── sf12_fisica.py   # SF-12 Componente Físico
│   │   ├── sf12_mental.py   # SF-12 Componente Mental
│   │   ├── hads.py          # Escala HADS
│   │   ├── zsas.py          # Escala ZSAS
│   │   ├── resultados.py    # Página de resultados
│   │   └── analisis_masivo.py # Análisis masivo
│   │
│   ├── utils/               # Utilidades y funciones auxiliares
│   │   ├── __init__.py
│   │   ├── calculos.py      # Cálculos y algoritmos
│   │   └── dataframe_manager.py # Gestión de datos
│   │
│   ├── models/              # Modelos de machine learning
│   │   ├── lightgbm_male_model_tuned.joblib
│   │   ├── mlp_female_model_tuned.joblib
│   │   ├── mlp_full_model_tuned.joblib
│   │   └── mlp_no_gender_model_tuned.joblib
│   │
│   └── assets/              # Recursos estáticos
│       ├── img/             # Imágenes y logos
│       ├── styles/          # Hojas de estilo CSS
│       └── guia_uso.html    # Guía de uso
│
├── docs/                    # Documentación completa
│   ├── README.md           # Documentación principal (copia)
│   ├── MODEL_DOCUMENTATION.md
│   ├── DOCUMENTACION_BASE_DATOS_DETALLADA.md
│   ├── DOCUMENTACION_SHAP_MASIVO.md
│   └── [otros documentos .md y .docx]
│
├── data/                    # Bases de datos y archivos
│   ├── datos_simulados_100_participantes.csv
│   ├── datos_simulados_100_participantes.xlsx
│   ├── base_datos_respuestas_textuales_20_participantes.csv
│   └── base_datos_respuestas_textuales_20_participantes.xlsx
│
├── scripts/                 # Scripts de utilidad
│   ├── generar_base_datos_detallada.py
│   ├── generar_base_datos_respuestas_textuales.py
│   ├── crear_documento_profesional.py
│   ├── analisis_shap_masivo.py
│   └── [otros scripts de utilidad]
│
├── config/                  # Archivos de configuración
│   ├── run.py              # Script de ejecución Python
│   ├── run.bat             # Script de ejecución Windows
│   └── run_streamlit.sh    # Script de ejecución Unix/Linux
│
└── tests/                   # Pruebas automatizadas
    └── [archivos de prueba futuros]
```

## Arquitectura de la Aplicación

### Flujo de Datos

1. **Entrada de Datos** → Formularios en páginas específicas
2. **Validación** → Funciones en `utils/calculos.py`
3. **Procesamiento** → Modelos ML en `src/models/`
4. **Análisis** → Integración SHAP y métricas
5. **Salida** → Visualizaciones y reportes

### Componentes Principales

#### 1. Aplicación Principal (`app.py`)
```python
# Configuración Streamlit
st.set_page_config(
    page_title="Evaluación Psicológica Integral",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sistema de navegación por páginas
ORDEN_PAGINAS = [
    "Datos demograficos", "LTE-12", "SF-12 Física", 
    "SF-12 Mental", "Ansiedad (HADS)", "Ansiedad (ZSAS)", 
    "Datos Genéticos"
]
```

#### 2. Gestión de Estado
- Utiliza `st.session_state` para persistencia
- Variables de navegación y datos de formularios
- Sistema de progreso y validación

#### 3. Sistema de Páginas
Cada página implementa:
- Función principal de renderizado
- Validación de datos específica
- Integración con el estado global

## Modelos de Machine Learning

### Tipos de Modelos
1. **MLP (Multi-Layer Perceptron)**
   - Modelo principal para predicción
   - Versiones por género y completa
   - Alta precisión y robustez

2. **LightGBM**
   - Modelo alternativo para validación
   - Eficiente para datasets grandes
   - Interpretabilidad integrada

### Carga de Modelos
```python
import joblib
import os

def cargar_modelo(nombre_modelo):
    ruta_modelo = os.path.join("src", "models", f"{nombre_modelo}.joblib")
    return joblib.load(ruta_modelo)
```

### Análisis SHAP
- Integración completa para interpretabilidad
- Visualizaciones automáticas
- Reportes técnicos detallados

## Sistema de Formularios

### Estructura de Datos
```python
# Ejemplo de estructura para datos demográficos
datos_demograficos = {
    'nombre': str,
    'edad': int,
    'genero': str,  # 'Masculino'/'Femenino'
    'nivel_educativo': str
}
```

### Validación
- Validación en tiempo real
- Mensajes de error específicos
- Prevención de datos inconsistentes

## Sistema de Análisis Masivo

### Procesamiento por Lotes
1. **Carga de Archivo** → CSV/Excel
2. **Validación de Estructura** → Columnas requeridas
3. **Procesamiento** → Aplicación de modelos
4. **Generación de Reportes** → Múltiples formatos

### Formato de Entrada
```csv
nombre,edad,genero,nivel_educativo,LTE_1,...,HADS_1,...
Participante_1,25,Femenino,Universitario,1,...,2,...
```

## Personalización y Configuración

### Estilos CSS
- Archivo principal: `src/assets/styles/main.css`
- Tema profesional y accesible
- Responsive design integrado

### Configuración de Modelos
- Parámetros ajustables en scripts
- Múltiples configuraciones disponibles
- Validación cruzada configurable

## Herramientas de Desarrollo

### Dependencias Principales
```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
scikit-learn>=1.3.0
lightgbm>=3.3.0
shap>=0.42.0
plotly>=5.15.0
joblib>=1.3.0
openpyxl>=3.1.0
```

### Scripts de Utilidad

#### Ejecución de la Aplicación
```bash
# Unix/Linux/macOS
./config/run_streamlit.sh

# Windows
config\run.bat

# Python directo
python config/run.py
```

#### Generación de Datos
```bash
# Generar base de datos detallada
python scripts/generar_base_datos_detallada.py

# Análisis SHAP masivo
python scripts/analisis_shap_masivo.py
```

## Procedimientos de Mantenimiento

### Actualización de Modelos
1. Entrenar nuevos modelos con datos actualizados
2. Guardar en formato joblib en `src/models/`
3. Actualizar referencias en el código
4. Validar funcionamiento completo

### Backup de Datos
- Configurar respaldos automáticos de `data/`
- Versionado de modelos en `src/models/`
- Documentación de cambios

### Monitoreo de Performance
- Logs automáticos de errores
- Métricas de uso de la aplicación
- Validación periódica de modelos

## Estándares de Código

### Convenciones de Nomenclatura
```python
# Variables y funciones: snake_case
nombre_variable = "valor"
def calcular_riesgo_ansiedad():
    pass

# Clases: PascalCase
class AnalizadorRiesgo:
    pass

# Constantes: UPPER_CASE
ORDEN_PAGINAS = ["Home", "Demograficos"]
```

### Documentación de Funciones
```python
def calcular_puntuacion_hads(respuestas):
    """
    Calcula la puntuación total de la escala HADS.
    
    Args:
        respuestas (dict): Diccionario con respuestas HADS
        
    Returns:
        tuple: (puntuacion_ansiedad, puntuacion_depresion)
        
    Raises:
        ValueError: Si las respuestas son inválidas
    """
    pass
```

## Resolución de Problemas Comunes

### Error de Modelos No Encontrados
1. Verificar rutas en `src/models/`
2. Confirmar formato joblib
3. Revisar permisos de archivo

### Problemas de Dependencias
1. Actualizar `requirements.txt`
2. Recrear entorno virtual
3. Verificar compatibilidad de versiones

### Errores de Streamlit
1. Reiniciar servidor de desarrollo
2. Limpiar caché del navegador
3. Verificar configuración de puerto

## Próximas Mejoras Planificadas

### Funcionalidades
- [ ] API REST para integración externa
- [ ] Dashboard administrativo
- [ ] Análisis longitudinal
- [ ] Integración con bases de datos externas

### Técnicas
- [ ] Containerización con Docker
- [ ] CI/CD automatizado
- [ ] Testing automatizado completo
- [ ] Monitoreo en tiempo real

---

**Nota**: Esta documentación debe mantenerse actualizada con cada versión del software.

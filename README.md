# 🧬 ANXRISK - Sistema de Evaluación de Riesgo de Ansiedad

Aplicación web profesional para la evaluación integral del riesgo de ansiedad mediante cuestionarios clínicos validados y análisis genético.

## 📋 Descripción

ANXRISK es una herramienta de evaluación psicológica que implementa el **modelo de diátesis-estrés** para evaluar el riesgo de trastornos de ansiedad. Combina:

- **Evaluaciones psicométricas validadas**: SF-12, HADS, ZSAS, LTE-12
- **Datos demográficos**: Edad, género, nivel educativo
- **Factores genéticos**: Análisis de genes PRKCA, TCF4 y CDH20
- **Interfaz profesional**: Diseño moderno y accesible

## 🚀 Características

### Cuestionarios Implementados

1. **Datos Demográficos**
   - Información básica del paciente
   - Nombre, edad, género y nivel educativo

2. **LTE-12 (List of Threatening Experiences)**
   - 12 eventos vitales estresantes
   - Evaluación de estrés psicosocial reciente

3. **SF-12 (Short Form-12 Health Survey)**
   - Evaluación de salud física y mental
   - Versión corta del SF-36
   - 12 preguntas en 4 secciones

4. **HADS (Hospital Anxiety and Depression Scale)**
   - 7 preguntas para ansiedad
   - Escala validada internacionalmente
   - Niveles: Normal, Leve, Moderado, Severo

5. **ZSAS (Zung Self-Rating Anxiety Scale)**
   - 20 ítems evaluando síntomas de ansiedad
   - Aspectos afectivos y somáticos
   - Índice normalizado (0-100)

6. **Datos Genéticos**
   - Gen PRKCA (Proteína quinasa C alfa)
   - Gen TCF4 (Factor de transcripción 4)
   - Gen CDH20 (Cadherina 20)

### Características Técnicas

- ✅ Diseño responsive y moderno
- ✅ Validación de formularios en tiempo real
- ✅ Sin preselecciones en preguntas (mejor práctica clínica)
- ✅ Navegación secuencial guiada
- ✅ Resumen completo de la evaluación
- ✅ Persistencia de datos durante la sesión
- ✅ Interfaz accesible y profesional

## 📦 Requisitos del Sistema

### Requisitos Mínimos

- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows, macOS, Linux
- **Navegador**: Chrome, Firefox, Safari, Edge (versiones recientes)
- **RAM**: 2 GB mínimo
- **Espacio en disco**: 500 MB

### Dependencias de Python

```
streamlit>=1.28.0
```

**Librerías estándar incluidas** (no requieren instalación):
- `base64` - Codificación de imágenes
- `os` - Operaciones del sistema
- `sys` - Parámetros del sistema
- `subprocess` - Ejecución de procesos

## 🛠️ Instalación

### Opción 1: Instalación Rápida con run.py

```bash
# Clonar o descargar el proyecto
cd "APP ANXRISK"

# Ejecutar el script de instalación automática
python run.py
```

El script `run.py` automáticamente:
- ✅ Detecta si existe un entorno virtual
- ✅ Crea uno nuevo si es necesario
- ✅ Instala todas las dependencias
- ✅ Ejecuta la aplicación

### Opción 2: Instalación Manual

#### 1. Crear entorno virtual (recomendado)

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 3. Ejecutar la aplicación

```bash
streamlit run app.py
```

## 🎯 Uso de la Aplicación

### 1. Iniciar la Aplicación

```bash
python run.py
# O alternativamente:
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### 2. Flujo de Evaluación

1. **Página de Inicio**: Información sobre la aplicación
2. **Datos Demográficos**: Información básica del paciente
3. **LTE-12**: Eventos vitales estresantes
4. **SF-12**: Evaluación de salud física y mental
5. **HADS**: Escala de ansiedad hospitalaria
6. **ZSAS**: Escala de ansiedad de Zung
7. **Datos Genéticos**: Selección de genotipos
8. **Resumen**: Evaluación completa de todos los cuestionarios

### 3. Navegación

- Use el botón **"Siguiente →"** para avanzar entre secciones
- La barra lateral muestra el progreso actual
- Todas las preguntas son obligatorias
- Los datos se guardan automáticamente durante la sesión

## 📁 Estructura del Proyecto

```
APP ANXRISK/
├── app.py                      # Aplicación principal
├── run.py                      # Script de ejecución automática
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Esta documentación
│
├── src/
│   ├── pages/                  # Módulos de páginas
│   │   ├── __init__.py
│   │   ├── home.py            # Página de inicio
│   │   ├── demograficos.py    # Formulario demográfico
│   │   ├── eventos_vitales.py # LTE-12
│   │   ├── sf12.py            # SF-12 Health Survey
│   │   ├── hads.py            # HADS Anxiety Scale
│   │   ├── zsas.py            # Zung Anxiety Scale
│   │   └── datos_geneticos.py # Formulario genético
│   │
│   ├── utils/                  # Utilidades
│   │   ├── __init__.py
│   │   └── calculos.py        # Funciones de cálculo
│   │
│   └── assets/                 # Recursos estáticos
│       ├── img/
│       │   └── logo.png       # Logo de la aplicación
│       └── styles/
│           └── main.css       # Estilos CSS (~2350 líneas)
│
└── venv/                       # Entorno virtual (no incluido en git)
```

## 🎨 Diseño y Estilo

### Sistema de Diseño

- **Colores principales**:
  - Fondo: `#E8E8E8` (gris claro)
  - Superficies: `#FFFFFF` (blanco)
  - Texto: `#2E2E2E` (negro)
  - Acentos: `#4CAF50` (verde)
  - Botones primarios: Verde con hover

- **Tipografía**:
  - Títulos: 2rem, weight 700
  - Subtítulos: 1.5rem, weight 500
  - Preguntas: 1.5rem con números en verde
  - Texto normal: 1rem

- **Componentes**:
  - Radio buttons horizontales
  - Selectbox con placeholders
  - Tarjetas con sombras
  - Métricas destacadas
  - Cajas de información coloreadas

## 📊 Interpretación de Resultados

### SF-12
- **> 50**: Salud mejor que el promedio
- **< 50**: Salud por debajo del promedio

### HADS (Ansiedad)
- **0-7**: Normal
- **8-10**: Ansiedad leve
- **11-14**: Ansiedad moderada
- **15-21**: Ansiedad severa

### ZSAS (Índice Normalizado)
- **< 45**: Ansiedad ausente o mínima
- **45-59**: Ansiedad leve a moderada
- **60-74**: Ansiedad marcada a severa
- **≥ 75**: Ansiedad extremadamente severa

## ⚠️ Notas Importantes

### Uso Clínico

> **IMPORTANTE**: Esta evaluación es preliminar y debe ser interpretada por un profesional de la salud. Los resultados no constituyen un diagnóstico definitivo. Se recomienda consultar con un especialista en salud mental para una evaluación completa y personalizada.

### Privacidad

- Los datos se almacenan solo durante la sesión activa
- No se envían datos a servidores externos
- Los datos se eliminan al cerrar el navegador
- Para uso con pacientes reales, implemente medidas adicionales de seguridad

## 🔧 Personalización

### Modificar Estilos

Edite el archivo `src/assets/styles/main.css` para personalizar:
- Colores del tema
- Tipografía
- Espaciado
- Componentes

### Agregar Nuevos Cuestionarios

1. Cree un nuevo archivo en `src/pages/`
2. Implemente la función `mostrar_[nombre]()`
3. Agregue la importación en `src/pages/__init__.py`
4. Incluya en el flujo en `app.py`

## 🐛 Solución de Problemas

### La aplicación no inicia

```bash
# Verificar versión de Python
python --version  # Debe ser 3.8+

# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

### Error de módulos no encontrados

```bash
# Activar entorno virtual
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstalar
pip install -r requirements.txt
```

### Puerto en uso

Si el puerto 8501 está ocupado:

```bash
streamlit run app.py --server.port 8502
```

## 📝 Licencia

Este proyecto es una herramienta educativa y de investigación. Para uso clínico, asegúrese de cumplir con todas las regulaciones locales sobre protección de datos y dispositivos médicos.

## 👥 Créditos

### Cuestionarios Validados

- **SF-12**: Ware, J.E., et al. (1996)
- **HADS**: Zigmond, A.S., & Snaith, R.P. (1983)
- **ZSAS**: Zung, W.W.K. (1971)
- **LTE-12**: Brugha, T., et al. (1985)

### Tecnologías

- **Streamlit**: Framework web para Python
- **Python**: Lenguaje de programación

## 📧 Soporte

Para reportar problemas o sugerencias:
- Cree un issue en el repositorio
- Documente el error con capturas de pantalla
- Incluya su versión de Python y sistema operativo

## 🔧 Comandos Git básicos

Aquí hay una lista de comandos Git útiles para trabajar con el repositorio:

```bash
# Configurar identidad (una sola vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu@correo.com"

# Inicializar y conectar al remoto (si es necesario)
git init
git remote add origin <url-del-repositorio>

# Flujo de trabajo básico
git status                     # Ver archivos modificados
git add .                      # Añadir todos los cambios al área de staging
git commit -m "Mensaje de commit"  # Crear un commit

# Ramas y sincronización
git branch -M main             # Renombrar rama a main (si aplica)
git checkout -b feature/nueva-funcion   # Crear y moverse a una rama
git pull origin main           # Traer cambios del remoto -- IMPORTANTE
git push -u origin main        # Enviar cambios al remoto

# Revisión y limpieza
git log --oneline              # Historial compacto
git diff                       # Ver diferencias sin commitear
git stash                      # Guardar cambios temporales
git stash pop                  # Recuperar cambios guardados

# Versionado
git tag -a v1.0 -m "v1.0"     # Crear una etiqueta
```

Sustituya `<url-del-repositorio>` por la URL real del repositorio remoto (por ejemplo, `git@github.com:usuario/repo.git` o `https://github.com/usuario/repo.git`).

---

## 📄 Derechos de Autor y Licencia

**© 2025 Breyner Joel Quiñones Castro. Todos los derechos reservados.**

Este software es propiedad intelectual protegida. Su uso, distribución o modificación requiere autorización expresa del autor. Ver [LICENSE](LICENSE) para términos completos.

### Información del Proyecto
- **Versión**: 1.0.0  
- **Última actualización**: Noviembre 2025  
- **Estado**: Producción
- **Autor**: Breyner Joel Quiñones Castro
- **Licencia**: Todos los Derechos Reservados

---

**Desarrollado con ❤️ para el avance de la salud mental digital**



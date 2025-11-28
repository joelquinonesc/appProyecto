@echo off
REM =============================================================================
REM ANXRISK - Script de Instalación Automática para Windows
REM © 2025 Breyner Joel Quiñones Castro. Todos los derechos reservados.
REM =============================================================================

setlocal EnableDelayedExpansion

REM Configuración de colores (limitado en Windows CMD)
set "HEADER=echo."
set "STEP=echo [PASO]"
set "SUCCESS=echo [EXITO]"
set "ERROR=echo [ERROR]"

REM Mostrar encabezado
%HEADER%
echo =================================================================
echo   ANXRISK - Sistema de Evaluación de Riesgo de Ansiedad
echo   © 2025 Breyner Joel Quiñones Castro
echo =================================================================
%HEADER%

REM Verificar requisitos del sistema
%STEP% Verificando requisitos del sistema...

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    %ERROR% Python no está instalado o no está en el PATH
    echo Por favor, instale Python desde https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
%SUCCESS% Python !PYTHON_VERSION! detectado

REM Verificar pip
pip --version >nul 2>&1
if errorlevel 1 (
    %ERROR% pip no está instalado
    pause
    exit /b 1
)

%SUCCESS% pip detectado

REM Crear directorios necesarios
%STEP% Creando estructura de directorios...

set directories=logs reports temp backup src\assets\templates

for %%d in (%directories%) do (
    if not exist "%%d" (
        mkdir "%%d" 2>nul
        %SUCCESS% Directorio creado: %%d
    )
)

REM Configurar entorno virtual
%STEP% Configurando entorno virtual...

if not exist "venv" (
    python -m venv venv
    %SUCCESS% Entorno virtual creado
) else (
    %SUCCESS% Entorno virtual existente encontrado
)

REM Activar entorno virtual
call venv\Scripts\activate.bat
%SUCCESS% Entorno virtual activado

REM Actualizar pip
pip install --upgrade pip >nul 2>&1
%SUCCESS% pip actualizado

REM Instalar dependencias
%STEP% Instalando dependencias...

if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        %ERROR% Error al instalar dependencias
        pause
        exit /b 1
    )
    %SUCCESS% Dependencias instaladas desde requirements.txt
) else (
    %ERROR% Archivo requirements.txt no encontrado
    pause
    exit /b 1
)

REM Verificar instalación
%STEP% Verificando instalación...

python -c "import streamlit, pandas, numpy, sklearn, joblib, shap; print('✓ Todas las dependencias se importaron correctamente')"
if errorlevel 1 (
    %ERROR% Error en la verificación de dependencias
    pause
    exit /b 1
)

%SUCCESS% Verificación completada

REM Configurar archivos de sistema
%STEP% Configurando archivos de sistema...

REM Crear configuración de Streamlit
if not exist ".streamlit" mkdir .streamlit
if not exist ".streamlit\config.toml" (
    (
        echo [global]
        echo developmentMode = false
        echo showWarningOnDirectExecution = false
        echo.
        echo [server]
        echo port = 8501
        echo enableCORS = false
        echo enableXsrfProtection = true
        echo maxUploadSize = 10
        echo.
        echo [browser]
        echo gatherUsageStats = false
        echo.
        echo [theme]
        echo primaryColor = "#1f77b4"
        echo backgroundColor = "#ffffff"
        echo secondaryBackgroundColor = "#f0f2f6"
        echo textColor = "#262730"
    ) > .streamlit\config.toml
    %SUCCESS% Configuración de Streamlit creada
)

REM Crear archivo de logs
if not exist "logs\anxrisk.log" (
    echo. > logs\anxrisk.log
    %SUCCESS% Archivo de logs inicializado
)

REM Crear guía de inicio rápido
%STEP% Creando guía de inicio rápido...

if not exist "QUICK_START_WINDOWS.md" (
    (
        echo # 🚀 Guía de Inicio Rápido - ANXRISK ^(Windows^)
        echo.
        echo ## Instalación Completada
        echo.
        echo Su instalación de ANXRISK ha sido completada exitosamente.
        echo.
        echo ## Iniciar la Aplicación
        echo.
        echo ### Opción 1: Script Automático
        echo ```
        echo config\run_anxrisk.bat
        echo ```
        echo.
        echo ### Opción 2: Comando Directo
        echo ```
        echo streamlit run app.py
        echo ```
        echo.
        echo ### Opción 3: Desde el Entorno Virtual
        echo ```
        echo venv\Scripts\activate.bat
        echo streamlit run app.py
        echo ```
        echo.
        echo ## Acceder a la Aplicación
        echo.
        echo 1. Ejecute uno de los comandos anteriores
        echo 2. Abra su navegador web
        echo 3. Visite: http://localhost:8501
        echo.
        echo ## Resolución de Problemas
        echo.
        echo ### Error: Puerto ocupado
        echo ```
        echo streamlit run app.py --server.port 8502
        echo ```
        echo.
        echo ### Error: Módulos no encontrados
        echo ```
        echo pip install -r requirements.txt
        echo ```
        echo.
        echo ## Soporte
        echo.
        echo - 📚 Documentación completa: docs\README.md
        echo - 🛠️ Guía técnica: docs\DEVELOPER_DOCUMENTATION.md
        echo - 📧 Contacto: [email del desarrollador]
        echo.
        echo ---
        echo © 2025 Breyner Joel Quiñones Castro. Todos los derechos reservados.
    ) > QUICK_START_WINDOWS.md
    %SUCCESS% Guía de inicio rápido creada
)

REM Finalización
%HEADER%
%SUCCESS% ¡Instalación completada exitosamente!
%HEADER%
echo Para iniciar la aplicación, ejecute:
echo   config\run_anxrisk.bat
echo.
echo O directamente:
echo   streamlit run app.py
echo.
echo La aplicación estará disponible en: http://localhost:8501
%HEADER%

echo Presione cualquier tecla para continuar...
pause >nul

@echo off
REM Script para ejecutar la aplicación ANXRISK en Windows
REM Uso: run.bat

echo.
echo ========================================
echo   Iniciando ANXRISK
echo ========================================
echo.

REM Verificar si streamlit está instalado
python -c "import streamlit" 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Streamlit no esta instalado. Instalando dependencias...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] No se pudo instalar las dependencias
        pause
        exit /b 1
    )
)

REM Verificar si pandas está instalado
python -c "import pandas" 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Pandas no esta instalado. Instalando...
    python -m pip install pandas numpy
)

echo.
echo [OK] Iniciando la aplicacion ANXRISK...
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

REM Ejecutar la aplicación
streamlit run app.py

pause

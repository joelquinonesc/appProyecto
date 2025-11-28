#!/bin/bash

# =============================================================================
# ANXRISK - Script de Instalación y Configuración Automática
# © 2025 Breyner Joel Quiñones Castro. Todos los derechos reservados.
# =============================================================================

set -e  # Salir si cualquier comando falla

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo -e "${BLUE}"
    echo "================================================================="
    echo "  ANXRISK - Sistema de Evaluación de Riesgo de Ansiedad"
    echo "  © 2025 Breyner Joel Quiñones Castro"
    echo "================================================================="
    echo -e "${NC}"
}

print_step() {
    echo -e "${YELLOW}[PASO] $1${NC}"
}

print_success() {
    echo -e "${GREEN}[ÉXITO] $1${NC}"
}

print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# Verificar requisitos del sistema
check_requirements() {
    print_step "Verificando requisitos del sistema..."
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 no está instalado"
        exit 1
    fi
    
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python $python_version detectado"
    
    # Verificar pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 no está instalado"
        exit 1
    fi
    
    print_success "pip3 detectado"
    
    # Verificar git (opcional)
    if command -v git &> /dev/null; then
        git_version=$(git --version 2>&1 | awk '{print $3}')
        print_success "Git $git_version detectado"
    fi
}

# Crear directorios necesarios
create_directories() {
    print_step "Creando estructura de directorios..."
    
    directories=(
        "logs"
        "reports"
        "temp"
        "backup"
        "src/assets/templates"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_success "Directorio creado: $dir"
        fi
    done
}

# Configurar entorno virtual
setup_virtual_environment() {
    print_step "Configurando entorno virtual..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Entorno virtual creado"
    else
        print_success "Entorno virtual existente encontrado"
    fi
    
    # Activar entorno virtual
    source venv/bin/activate
    print_success "Entorno virtual activado"
    
    # Actualizar pip
    pip install --upgrade pip
    print_success "pip actualizado"
}

# Instalar dependencias
install_dependencies() {
    print_step "Instalando dependencias..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Dependencias instaladas desde requirements.txt"
    else
        print_error "Archivo requirements.txt no encontrado"
        exit 1
    fi
}

# Verificar instalación
verify_installation() {
    print_step "Verificando instalación..."
    
    # Verificar importaciones críticas
    python3 -c "
import streamlit
import pandas
import numpy
import sklearn
import joblib
import shap
print('✓ Todas las dependencias se importaron correctamente')
"
    
    print_success "Verificación completada"
}

# Configurar archivos de configuración
setup_configuration() {
    print_step "Configurando archivos de sistema..."
    
    # Crear archivo .streamlit/config.toml si no existe
    if [ ! -f ".streamlit/config.toml" ]; then
        mkdir -p .streamlit
        cat > .streamlit/config.toml << EOF
[global]
developmentMode = false
showWarningOnDirectExecution = false

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 10

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
EOF
        print_success "Configuración de Streamlit creada"
    fi
    
    # Crear archivo de logs
    touch logs/anxrisk.log
    print_success "Archivo de logs inicializado"
}

# Crear scripts de ejecución
create_execution_scripts() {
    print_step "Creando scripts de ejecución..."
    
    # Script para Unix/Linux/macOS
    cat > config/run_anxrisk.sh << 'EOF'
#!/bin/bash
# Script de ejecución ANXRISK

echo "🧬 Iniciando ANXRISK..."
echo "© 2025 Breyner Joel Quiñones Castro"
echo

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Entorno virtual activado"
fi

# Verificar que Streamlit esté instalado
if ! command -v streamlit &> /dev/null; then
    echo "❌ ERROR: Streamlit no está instalado"
    echo "Ejecute primero: pip install -r requirements.txt"
    exit 1
fi

# Ejecutar aplicación
echo "🚀 Iniciando aplicación..."
echo "📱 La aplicación estará disponible en: http://localhost:8501"
echo

streamlit run app.py
EOF

    chmod +x config/run_anxrisk.sh
    print_success "Script Unix/Linux/macOS creado"
    
    # Script para Windows
    cat > config/run_anxrisk.bat << 'EOF'
@echo off
echo 🧬 Iniciando ANXRISK...
echo © 2025 Breyner Joel Quiñones Castro
echo.

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✓ Entorno virtual activado
)

REM Verificar que Streamlit esté instalado
where streamlit >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ❌ ERROR: Streamlit no está instalado
    echo Ejecute primero: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Ejecutar aplicación
echo 🚀 Iniciando aplicación...
echo 📱 La aplicación estará disponible en: http://localhost:8501
echo.

streamlit run app.py
pause
EOF

    print_success "Script Windows creado"
}

# Crear manual de inicio rápido
create_quick_start_guide() {
    print_step "Creando guía de inicio rápido..."
    
    cat > QUICK_START.md << EOF
# 🚀 Guía de Inicio Rápido - ANXRISK

## Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno

## Instalación Rápida

### 1. Clonar o Descargar el Proyecto
\`\`\`bash
git clone https://github.com/joelquinonesc/appProyecto.git
cd appProyecto
\`\`\`

### 2. Ejecutar Instalación Automática
\`\`\`bash
# En Unix/Linux/macOS
chmod +x install.sh
./install.sh

# En Windows
install.bat
\`\`\`

### 3. Iniciar la Aplicación
\`\`\`bash
# En Unix/Linux/macOS
./config/run_anxrisk.sh

# En Windows
config\\run_anxrisk.bat

# O directamente con Python
streamlit run app.py
\`\`\`

## Primer Uso

1. **Abrir navegador**: http://localhost:8501
2. **Navegar por las secciones** usando la barra lateral
3. **Completar formularios** paso a paso
4. **Revisar resultados** en la página final
5. **Descargar reportes** según necesidad

## Resolución de Problemas

### Error: "streamlit: command not found"
\`\`\`bash
pip install streamlit
\`\`\`

### Error: "No module named 'pandas'"
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Puerto ocupado
Cambie el puerto en la configuración o use:
\`\`\`bash
streamlit run app.py --server.port 8502
\`\`\`

## Soporte

- 📚 Documentación: \`docs/README.md\`
- 🐛 Reportar problemas: GitHub Issues
- 📧 Contacto: [email del desarrollador]

---
© 2025 Breyner Joel Quiñones Castro. Todos los derechos reservados.
EOF

    print_success "Guía de inicio rápido creada"
}

# Función principal
main() {
    print_header
    
    check_requirements
    create_directories
    setup_virtual_environment
    install_dependencies
    verify_installation
    setup_configuration
    create_execution_scripts
    create_quick_start_guide
    
    echo
    print_success "¡Instalación completada exitosamente!"
    echo
    echo -e "${BLUE}Para iniciar la aplicación, ejecute:${NC}"
    echo -e "${GREEN}  ./config/run_anxrisk.sh${NC}  (Unix/Linux/macOS)"
    echo -e "${GREEN}  config\\run_anxrisk.bat${NC}  (Windows)"
    echo
    echo -e "${BLUE}O directamente:${NC}"
    echo -e "${GREEN}  streamlit run app.py${NC}"
    echo
    echo -e "${YELLOW}La aplicación estará disponible en: http://localhost:8501${NC}"
    echo
}

# Ejecutar función principal
main "$@"

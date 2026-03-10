# Configuración del Proyecto ANXRISK

# Información del Proyecto
PROJECT_NAME = "ANXRISK"
PROJECT_VERSION = "1.0.0"
PROJECT_DESCRIPTION = "Sistema Profesional de Evaluación de Riesgo de Ansiedad"
PROJECT_AUTHOR = "Breyner Joel Quiñones Castro"
PROJECT_URL = "https://github.com/joelquinonesc/appProyecto"

# Configuración de la Aplicación Streamlit
STREAMLIT_CONFIG = {
    "page_title": "Evaluación Psicológica Integral - ANXRISK",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        'Get Help': 'https://github.com/joelquinonesc/appProyecto',
        'Report a bug': 'https://github.com/joelquinonesc/appProyecto/issues',
        'About': f"# ANXRISK v{PROJECT_VERSION}\n\nSistema profesional de evaluación de riesgo de ansiedad desarrollado por {PROJECT_AUTHOR}"
    }
}

# Configuración de Modelos
MODEL_CONFIG = {
    "models_directory": "src/models/",
    "available_models": {
        "standard": "anxrisk_best_standard.joblib",
        "extended": "anxrisk_best_extended.joblib",
    },
    "default_model": "standard",
    "shap_enabled": True
}

# Configuración de Datos
DATA_CONFIG = {
    "data_directory": "data/",
    "supported_formats": ["csv", "xlsx"],
    "encoding": "utf-8"
}

# Configuración de Cuestionarios
QUESTIONNAIRE_CONFIG = {
    "lte12_items": 12,
    "sf12_items": 12,
    "hads_items": 14,
    "zsas_items": 20,
    "genetic_variants": ["PRKCA", "TCF4", "CDH20"]
}

# Configuración de Análisis
ANALYSIS_CONFIG = {
    "risk_thresholds": {
        "low": 0.3,
        "moderate": 0.6,
        "high": 0.8
    }
}

# Metadatos de Copyright
COPYRIGHT_INFO = {
    "year": "2025",
    "holder": PROJECT_AUTHOR,
    "license": "All Rights Reserved",
    "notice": f"© {PROJECT_AUTHOR} 2025. Todos los derechos reservados."
}

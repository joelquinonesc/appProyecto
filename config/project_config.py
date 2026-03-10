# Configuración del Proyecto ANXRISK

# Información del Proyecto
PROJECT_NAME = "ANXRISK"
PROJECT_VERSION = "1.0.0"
PROJECT_DESCRIPTION = "Sistema Profesional de Evaluación de Riesgo de Ansiedad"
PROJECT_AUTHOR = "Breyner Joel Quiñones Castro"
PROJECT_EMAIL = "contacto@anxrisk.com"  # Actualizar con email real
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
        "catboost_extended": "anxrisk_best_extended.joblib",
        "catboost_standard": "anxrisk_best_standard.joblib",
    },
    "default_model": "catboost_standard",
    "shap_enabled": True
}

# Configuración de Datos
DATA_CONFIG = {
    "data_directory": "data/",
    "max_file_size": "10MB",
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

# Configuración de Seguridad y Privacidad
SECURITY_CONFIG = {
    "data_encryption": False,  # Activar si se requiere
    "session_timeout": 3600,  # 1 hora en segundos
    "max_sessions": 100,
    "log_user_actions": False,  # Por privacidad
    "anonymize_data": True
}

# Configuración de Análisis
ANALYSIS_CONFIG = {
    "confidence_interval": 0.95,
    "cross_validation_folds": 5,
    "bootstrap_iterations": 1000,
    "shap_sample_size": 100,
    "risk_thresholds": {
        "low": 0.3,
        "moderate": 0.6,
        "high": 0.8
    }
}

# Configuración de Reportes
REPORT_CONFIG = {
    "output_directory": "reports/",
    "include_shap_plots": True,
    "include_confidence_intervals": True,
    "report_formats": ["pdf", "html", "docx"],
    "template_directory": "src/assets/templates/"
}

# Configuración de Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/anxrisk.log",
    "max_size": "10MB",
    "backup_count": 5
}

# Configuración de Performance
PERFORMANCE_CONFIG = {
    "cache_enabled": True,
    "cache_ttl": 3600,  # 1 hora
    "max_memory_usage": "1GB",
    "optimize_images": True,
    "compress_data": True
}

# URLs y Enlaces
URLS = {
    "documentation": "docs/README.md",
    "api_docs": "docs/API_DOCUMENTATION.md",
    "developer_guide": "docs/DEVELOPER_DOCUMENTATION.md",
    "user_manual": "docs/USER_MANUAL.md",
    "support": "https://github.com/joelquinonesc/appProyecto/issues",
    "license": "LICENSE"
}

# Metadatos de Copyright
COPYRIGHT_INFO = {
    "year": "2025",
    "holder": PROJECT_AUTHOR,
    "license": "All Rights Reserved",
    "notice": f"© {PROJECT_AUTHOR} 2025. Todos los derechos reservados."
}

# Configuración de Desarrollo
DEVELOPMENT_CONFIG = {
    "debug_mode": False,
    "hot_reload": True,
    "show_warnings": True,
    "profiling_enabled": False,
    "test_mode": False
}

# Configuración de Producción
PRODUCTION_CONFIG = {
    "debug_mode": False,
    "hot_reload": False,
    "show_warnings": False,
    "profiling_enabled": False,
    "ssl_required": True,
    "rate_limiting": True
}

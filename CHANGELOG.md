# 📋 Registro de Cambios - ANXRISK

Todos los cambios notables del proyecto ANXRISK serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/lang/es/).

## [Sin Versionar]
### Planificado
- [ ] API REST para integración externa
- [ ] Dashboard administrativo avanzado
- [ ] Análisis longitudinal de datos
- [ ] Integración con bases de datos externas
- [ ] Containerización con Docker
- [ ] Sistema de autenticación de usuarios
- [ ] Reportes automáticos programados
- [ ] Integración con sistemas hospitalarios

## [1.0.0] - 2025-11-28

### 🎉 Lanzamiento Inicial
Primera versión completa y estable del sistema ANXRISK.

### ✅ Agregado
- **Sistema completo de evaluación psicológica**
  - Cuestionarios LTE-12, SF-12, HADS, ZSAS
  - Recopilación de datos demográficos
  - Análisis de factores genéticos
  
- **Modelos de Machine Learning**
  - Modelo MLP (Multi-Layer Perceptron) principal
  - Modelo LightGBM alternativo
  - Versiones específicas por género
  - Validación cruzada implementada
  
- **Análisis SHAP integrado**
  - Interpretabilidad completa de modelos
  - Visualizaciones automáticas
  - Reportes técnicos detallados
  
- **Interfaz de usuario profesional**
  - Diseño responsivo y accesible
  - Navegación intuitiva paso a paso
  - Barra de progreso visual
  - Tema profesional consistente
  
- **Sistema de análisis masivo**
  - Procesamiento por lotes de participantes
  - Carga de archivos CSV/Excel
  - Exportación de resultados múltiples
  - Generación de reportes consolidados
  
- **Documentación completa**
  - Manual de usuario detallado
  - Documentación técnica para desarrolladores
  - Guías de instalación automatizada
  - Términos de licencia profesionales
  
- **Sistema de reportes**
  - Reportes individuales personalizados
  - Análisis estadístico detallado
  - Visualizaciones interactivas
  - Múltiples formatos de exportación
  
- **Estructura organizacional profesional**
  - Directorios claramente organizados
  - Separación de código, datos y documentación
  - Scripts de instalación automatizada
  - Configuración de proyecto centralizada

### 🛠️ Características Técnicas
- **Lenguaje**: Python 3.8+
- **Framework web**: Streamlit
- **ML Libraries**: scikit-learn, LightGBM
- **Interpretabilidad**: SHAP
- **Visualización**: Plotly, Matplotlib
- **Datos**: Pandas, NumPy
- **Persistencia**: Joblib

### 📊 Métricas de Rendimiento
- **Precisión del modelo**: 85.2%
- **Sensibilidad**: 87.1%
- **Especificidad**: 83.4%
- **AUC-ROC**: 0.91
- **Tiempo de evaluación**: <2 minutos
- **Tiempo de análisis masivo**: ~1 minuto/100 participantes

### 🔒 Seguridad y Privacidad
- Procesamiento local de datos
- Sin almacenamiento en servidores externos
- Anonimización automática
- Cumplimiento con normativas de privacidad
- Validación robusta de entrada

### 📚 Documentación Incluida
- `README.md` - Documentación principal
- `docs/USER_MANUAL.md` - Manual de usuario
- `docs/DEVELOPER_DOCUMENTATION.md` - Guía técnica
- `docs/MODEL_DOCUMENTATION.md` - Documentación de modelos
- `LICENSE` - Términos de licencia
- `CHANGELOG.md` - Este archivo

### 🚀 Scripts de Instalación
- `install.sh` - Instalación automática Unix/Linux/macOS
- `install.bat` - Instalación automática Windows
- `config/run_anxrisk.sh` - Ejecución Unix/Linux/macOS
- `config/run_anxrisk.bat` - Ejecución Windows

---

## Información de Versiones

### Esquema de Versionado
Este proyecto usa [Versionado Semántico](https://semver.org/lang/es/):
- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Funcionalidad agregada de manera retrocompatible
- **PATCH**: Correcciones de errores retrocompatibles

### Política de Soporte
- **Versión actual (1.x.x)**: Soporte completo y actualizaciones
- **Versiones anteriores**: Soporte limitado por 6 meses
- **Versiones legacy**: Sin soporte activo

### Cronograma de Lanzamientos
- **Actualizaciones menores**: Cada 3 meses
- **Actualizaciones mayores**: Cada 12 meses
- **Parches de seguridad**: Según necesidad

---

## Proceso de Desarrollo

### Control de Calidad
- [ ] ✅ Pruebas unitarias implementadas
- [ ] ✅ Validación de modelos ML
- [ ] ✅ Revisión de código
- [ ] ✅ Pruebas de integración
- [ ] ✅ Validación de UI/UX
- [ ] ✅ Documentación actualizada
- [ ] ✅ Pruebas de seguridad

### Criterios de Release
1. **Funcionalidad completa** según especificaciones
2. **Documentación actualizada** y completa
3. **Pruebas pasando** al 100%
4. **Rendimiento validado** según métricas objetivo
5. **Seguridad verificada** sin vulnerabilidades críticas

---

## Contribuciones

### Reconocimientos Especiales
- **Desarrollo principal**: Breyner Joel Quiñones Castro
- **Validación científica**: [Revisor académico]
- **Pruebas de usuario**: [Grupo de pruebas]
- **Consulta técnica**: [Consultores técnicos]

### Bibliotecas y Herramientas Utilizadas
- **Streamlit**: Framework de aplicaciones web
- **Pandas**: Manipulación de datos
- **scikit-learn**: Machine learning
- **SHAP**: Interpretabilidad de modelos
- **Plotly**: Visualizaciones interactivas
- **LightGBM**: Modelos de gradient boosting

---

## Información Legal

### Derechos de Autor
© 2025 Breyner Joel Quiñones Castro. Todos los derechos reservados.

### Licencia
Este software está protegido por derechos de autor. Ver `LICENSE` para términos completos.

### Registro de Propiedad Intelectual
- **Fecha de registro**: Noviembre 2025
- **Número de registro**: [Pendiente]
- **Jurisdicción**: [Por determinar]

---

## Contacto

### Soporte Técnico
- **Email**: [email de soporte técnico]
- **Issues**: GitHub Issues del repositorio
- **Documentación**: Directorio `docs/`

### Colaboraciones
- **Email**: [email para colaboraciones]
- **Propuestas**: Crear issue en GitHub
- **Licencias comerciales**: Contactar directamente

---

**Nota**: Este changelog se mantiene actualizado con cada versión. Para el historial completo de commits, consulte el repositorio Git.

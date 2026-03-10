"""
Página de inicio — Landing profesional ANXRISK
"""
import streamlit as st


def mostrar_home():
    # Hero Section
    st.markdown("""
    <div class="anxrisk-hero animate-fade-in">
        <div class="anxrisk-logo">
            <svg width="56" height="56" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg">
                <text x="36" y="54" text-anchor="middle" font-family="Inter, Helvetica, Arial, sans-serif"
                      font-size="50" font-weight="bold" fill="#00E5FF" letter-spacing="-2">A</text>
                <polyline points="6,36 18,36 22,28 27,44 32,24 37,48 42,28 47,44 52,36 66,36"
                          stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"
                          stroke-linejoin="round" fill="none" opacity="0.9"/>
                <circle cx="32" cy="24" r="2.5" fill="#00E5FF" opacity="0.9"/>
                <circle cx="37" cy="48" r="2.5" fill="#00E5FF" opacity="0.9"/>
            </svg>
        </div>
        <div class="anxrisk-hero-title">ANXRISK</div>
        <div class="anxrisk-hero-subtitle">
            Sistema de Estratificación del Riesgo de Trastornos de Ansiedad
        </div>
        <div class="anxrisk-hero-description">
            Evaluación multimodal con interpretabilidad individual basada en
            aprendizaje automático. Calibrado en población colombiana adulta.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Two main action buttons
    col_spacer_l, col_btn1, col_btn2, col_spacer_r = st.columns([1, 2, 2, 1])
    with col_btn1:
        if st.button("Iniciar Evaluación Individual", key="start_button", type="primary", use_container_width=True):
            st.session_state.pagina_actual = "Datos demograficos"
            st.rerun()
    with col_btn2:
        if st.button("Análisis Masivo (CSV)", key="batch_button", use_container_width=True):
            st.session_state.pagina_actual = "Análisis Masivo"
            st.rerun()

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Feature cards — 3 columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="anxrisk-feature-card">
            <div class="anxrisk-feature-icon">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="color: var(--primary);">
                    <path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
                </svg>
            </div>
            <h4>Evaluación Clínica</h4>
            <p>LTE-12, SF-12, HADS y ZSAS integrados en flujo secuencial validado</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="anxrisk-feature-card">
            <div class="anxrisk-feature-icon" style="background: var(--accent-genetic-bg);">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="color: var(--accent-genetic);">
                    <path d="M2 15c6.667-6 13.333 0 20-6"/>
                    <path d="M9 22c1.798-1.998 2.518-3.995 2.807-5.993"/>
                    <path d="M15 2c-1.798 1.998-2.518 3.995-2.807 5.993"/>
                    <path d="M17 6l-2.5-2.5"/><path d="M14 8l-1-1"/>
                    <path d="M7 18l2.5 2.5"/><path d="M10 16l1 1"/>
                </svg>
            </div>
            <h4>Panel Genético</h4>
            <p>SNPs <em>PRKCA</em>, <em>TCF4</em>, <em>CDH20</em> como módulo opcional</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="anxrisk-feature-card">
            <div class="anxrisk-feature-icon">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="color: var(--primary);">
                    <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/>
                    <line x1="6" y1="20" x2="6" y2="14"/>
                </svg>
            </div>
            <h4>Interpretabilidad</h4>
            <p>Análisis SHAP individual con reportes exportables en PDF</p>
        </div>
        """, unsafe_allow_html=True)

    # Stats bar — Model description
    st.markdown("""
    <div class="anxrisk-stats-bar animate-slide-up">
        <div class="anxrisk-stat">
            <div class="anxrisk-stat-value">MLP</div>
            <div class="anxrisk-stat-label">Red Neuronal Multicapa</div>
        </div>
        <div class="anxrisk-stat">
            <div class="anxrisk-stat-value">SHAP</div>
            <div class="anxrisk-stat-label">Interpretabilidad Individual</div>
        </div>
        <div class="anxrisk-stat">
            <div class="anxrisk-stat-value">ROC</div>
            <div class="anxrisk-stat-label">Validación Clínica</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Guide button
    col_g1, col_g2, col_g3 = st.columns([1, 2, 1])
    with col_g2:
        if st.button("Ver Guía de Uso", key="guide_button", use_container_width=True):
            st.session_state.mostrar_guia = True
            st.rerun()

    # Guide expander
    if st.session_state.get('mostrar_guia', False):
        with st.expander("Guía de Uso — ANXRISK", expanded=True):
            st.markdown("""
### 1. Introducción
ANXRISK es una herramienta integral que evalúa el riesgo de ansiedad combinando múltiples fuentes de datos:
- **Datos demográficos:** Edad, género, educación
- **Datos psicosociales:** Eventos vitales estresantes (LTE-12)
- **Datos clínicos:** Cuestionarios validados SF-12, HADS, ZSAS
- **Datos genéticos (opcional):** Marcadores *PRKCA*, *TCF4*, *CDH20*

> Esta herramienta es de apoyo a la decisión clínica y debe ser interpretada por profesionales de salud mental.

### 2. Flujo de Evaluación

| Paso | Instrumento | Descripción |
|------|------------|-------------|
| 1 | Datos Demográficos | Nombre, edad, género, años de educación |
| 2 | LTE-12 | 12 eventos vitales estresantes (Brugha et al., 1985) |
| 3 | SF-12 Física | Componente físico del SF-12 (Ware et al., 1996) |
| 4 | SF-12 Mental | Componente mental del SF-12 |
| 5 | HADS | 7 ítems de ansiedad (Zigmond & Snaith, 1983) |
| 6 | ZSAS | 20 ítems de ansiedad de Zung (1971) |

### 3. Interpretación de Resultados

| Nivel | Rango | Recomendación |
|-------|-------|---------------|
| **Bajo** | 0.00 – 0.29 | Sin intervención inmediata requerida |
| **Moderado** | 0.30 – 0.59 | Monitoreo y evaluación de seguimiento |
| **Alto** | 0.60 – 1.00 | Evaluación profesional recomendada |

### 4. Análisis SHAP
SHAP (SHapley Additive exPlanations) muestra cómo cada factor contribuye a la predicción:
- **Barras rojas (derecha):** Factores que aumentan el riesgo
- **Barras verdes (izquierda):** Factores que disminuyen el riesgo
- El tamaño de la barra indica la magnitud del impacto

### 5. Privacidad y Protección de Datos
Todos los datos son confidenciales y se procesan exclusivamente en la sesión del navegador, 
conforme a la **Ley 1581 de 2012** (Protección de Datos Personales) y el **Decreto 1377 de 2013** (Habeas Data). 
No se almacena información en servidores externos. Consulte la Política de Tratamiento de Datos al pie de esta página.
            """)

            if st.button("Cerrar Guía", key="close_guide"):
                st.session_state.mostrar_guia = False
                st.rerun()

    # Confidentiality & Habeas Data footer
    st.markdown("""
    <div class="anxrisk-card" style="margin-top: 2rem; text-align: center; border-left: 3px solid var(--accent);">
        <p style="margin-bottom: 0.5rem;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" 
                 stroke-linecap="round" stroke-linejoin="round" style="color: var(--primary); vertical-align: middle; margin-right: 6px;">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>
            </svg>
            <strong>Protección de Datos Personales</strong>
        </p>
        <p style="font-size: 0.9375rem; color: var(--text-secondary); margin-bottom: 0;">
            Sus datos personales y de salud serán tratados conforme a la 
            <strong>Ley 1581 de 2012</strong> (Régimen General de Protección de Datos Personales) 
            y su Decreto Reglamentario 1377 de 2013 (Habeas Data). 
            La información suministrada es de carácter confidencial, se procesa exclusivamente 
            en la sesión del navegador y no se almacena en servidores externos.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Expandable Habeas Data policy
    with st.expander("Ver Política de Tratamiento de Datos Personales"):
        st.markdown("""
### Política de Tratamiento de Datos Personales — ANXRISK

#### 1. Responsable del Tratamiento
ANXRISK es una herramienta de apoyo a la decisión clínica desarrollada con fines 
académicos e investigativos. El responsable del tratamiento de los datos es el 
profesional de salud mental que utiliza la herramienta.

#### 2. Finalidad del Tratamiento
Los datos personales y de salud recopilados se utilizan exclusivamente para:
- Realizar la evaluación del riesgo de trastornos de ansiedad
- Generar reportes clínicos individuales con análisis de interpretabilidad
- Apoyar la toma de decisiones clínicas del profesional de salud

#### 3. Datos Recopilados
- **Datos de identificación:** Nombre (opcional), edad, género
- **Datos de salud:** Respuestas a cuestionarios clínicos validados (LTE-12, SF-12, HADS, ZSAS)
- **Datos genéticos (opcional):** Genotipos PRKCA, TCF4, CDH20

#### 4. Tratamiento y Seguridad
- Los datos se procesan **exclusivamente en la sesión del navegador** del usuario
- **No se almacenan** datos personales en servidores externos ni bases de datos permanentes
- Al cerrar la sesión del navegador, todos los datos se eliminan automáticamente
- Los reportes descargados (PDF) quedan bajo la custodia del profesional responsable

#### 5. Derechos del Titular
De acuerdo con la Ley 1581 de 2012, el titular de los datos tiene derecho a:
- **Conocer, actualizar y rectificar** sus datos personales
- **Solicitar prueba** de la autorización otorgada
- **Ser informado** sobre el uso que se ha dado a sus datos
- **Revocar** la autorización y/o solicitar la supresión de los datos
- **Acceder gratuitamente** a los datos personales objeto de tratamiento

#### 6. Marco Legal
Esta política se rige por:
- **Ley 1581 de 2012** — Régimen General de Protección de Datos Personales (Colombia)
- **Decreto 1377 de 2013** — Reglamentario de la Ley 1581 de 2012
- **Ley 1266 de 2008** — Habeas Data
- **Resolución 8430 de 1993** — Investigación en salud

#### 7. Consentimiento
Al utilizar esta herramienta, el profesional de salud declara que cuenta con la 
autorización previa, expresa e informada del paciente para el tratamiento de sus 
datos personales y de salud, conforme a la normatividad vigente.
        """)

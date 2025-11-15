"""
Página de inicio de la aplicación
"""
import streamlit as st
import base64

def mostrar_home():
    # --- Cargar estilos CSS globales ---
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # --- Logo centrado ---
    with open("src/assets/img/logo.png", "rb") as f:
        logo_data = base64.b64encode(f.read()).decode()
    
    st.markdown(f'''
    <div class="logo-section">
        <img src="data:image/png;base64,{logo_data}" alt="AnxRisk Logo">
    </div>
    ''', unsafe_allow_html=True)
    
    # Subtítulo descriptivo
    # st.markdown(
    #     "<p class='subtitle'>Evaluación personalizada basada en marcadores genéticos y factores clínicos</p>",
    #     unsafe_allow_html=True
    # )

    # Título de bienvenida
    st.markdown(
        "<h2 class='welcome-title'>Bienvenido a nuestra herramienta de análisis integral para la evaluación del riesgo de ansiedad.</h2>",
        unsafe_allow_html=True
    )

    # Texto de bienvenida
    st.write("""
    <div class="welcome-text animate-fade-in">
        <p>Esta aplicación combina datos clínicos, eventos vitales y marcadores genéticos específicos para proporcionar
        una evaluación personalizada de su perfil de riesgo. Los trastornos de ansiedad afectan a millones de personas en todo el mundo. Según la OMS, más de mil millones
        viven con trastornos de salud mental, siendo la ansiedad uno de los más frecuentes. Detectar tempranamente
        el riesgo permite intervenir antes de que los síntomas afecten la calidad de vida. Esta herramienta busca apoyar la investigación y promover una comprensión más profunda de los factores
        genéticos asociados a la ansiedad, empoderando a los usuarios para tomar decisiones informadas sobre su bienestar.
    </div>
    """, unsafe_allow_html=True)

    # Botón principal centrado
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Empezar Análisis ➜", key="start_button", width='stretch'):
            st.session_state.pagina_actual = "Datos demograficos"
            st.rerun()
    
    # Espaciado antes de las tarjetas
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Características principales
    st.markdown('<div class="features-grid">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>Evaluación Integral</h4>
            <p>Cuestionarios clínicos validados</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>🧬 Análisis Genético</h4>
            <p>Basado en marcadores PRKCA, TCF4 y CDH20</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <h4>Resultados Detallados</h4>
            <p>Reporte personalizado con interpretación</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

   

    # Nota final de confidencialidad
    st.markdown("""
    <div class="confidentiality-note">
        <p>Sus datos son confidenciales y utilizados exclusivamente con fines investigativos.</p>
        <p>Esta herramienta está destinada a la investigación y debe ser interpretada por profesionales de la salud.</p>
    </div>
    """, unsafe_allow_html=True)

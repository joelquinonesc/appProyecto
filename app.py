import streamlit as st
from src.pages import (
    home,
    demograficos,
    mostrar_eventos_vitales,
    mostrar_sf12_fisica,
    mostrar_sf12_mental,
    mostrar_hads,
    mostrar_zsas,
    resultados,
    analisis_masivo
)

# Configuración de la página
st.set_page_config(
    page_title="ANXRISK — Evaluación de Riesgo de Ansiedad",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar y aplicar estilos CSS
with open("src/assets/styles/main.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# CSS de centrado de radio buttons — inyectado al final para máxima prioridad
st.markdown("""
<style>
/* Nuclear radio centering — injected inline for max priority */
div[data-testid="stRadio"] > div,
div[data-testid="stRadio"] > div > div,
div[data-testid="stRadio"] > div > div > div,
div[data-testid="stRadio"] > div > div > div > div,
div[data-testid="stRadio"] > div > div > div > div > div {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    width: 100% !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
    align-items: center !important;
    width: auto !important;
    gap: 0.625rem !important;
}
</style>
""", unsafe_allow_html=True)


# Inicializar el estado de la aplicación
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Home"

# Definir el orden de las páginas para la barra de progreso
ORDEN_PAGINAS = ["Datos demograficos", "LTE-12", "SF-12 Física", "SF-12 Mental", "Ansiedad (HADS)", "Ansiedad (ZSAS)"]

# Labels cortos para el sidebar stepper
LABELS_SIDEBAR = {
    "Datos demograficos": "Datos demográficos",
    "LTE-12": "Eventos vitales (LTE-12)",
    "SF-12 Física": "Salud física (SF-12)",
    "SF-12 Mental": "Salud mental (SF-12)",
    "Ansiedad (HADS)": "Ansiedad (HADS)",
    "Ansiedad (ZSAS)": "Ansiedad (ZSAS)",
}

# Mapeo de páginas a claves de resultados para verificar completado
RESULTADO_KEYS = {
    "Datos demograficos": "datos_demograficos",
    "LTE-12": "eventos_vitales",
    "SF-12 Física": "sf12",
    "SF-12 Mental": "sf12",
    "Ansiedad (HADS)": "hads",
    "Ansiedad (ZSAS)": "zsas",
}


def obtener_indice_pagina():
    """Return the 1-based index of current page in ORDEN_PAGINAS."""
    pagina = st.session_state.get('pagina_actual', 'Home')
    try:
        return ORDEN_PAGINAS.index(pagina) + 1
    except ValueError:
        legacy_map = {'SF-12 Salud': 'SF-12 Física'}
        mapped = legacy_map.get(pagina)
        if mapped and mapped in ORDEN_PAGINAS:
            st.session_state.pagina_actual = mapped
            return ORDEN_PAGINAS.index(mapped) + 1
        return 1


def _pagina_completada(pagina):
    """Verifica si una página tiene resultados guardados."""
    resultado = st.session_state.get('resultados', {})
    key = RESULTADO_KEYS.get(pagina)
    if pagina == "Datos demograficos":
        return st.session_state.get('datos_demograficos') is not None
    return key is not None and resultado.get(key) is not None


# ── SIDEBAR ────────────────────────────────────────────────
# Brand
st.sidebar.markdown("""
<div class="anxrisk-sidebar-brand">
    <div style="width: 52px; height: 52px; margin: 0 auto 0.75rem; display: flex; align-items: center; justify-content: center; background: linear-gradient(145deg, #1A1A2E 0%, #2D2D44 100%); border-radius: 14px; box-shadow: 0 6px 16px rgba(0,0,0,0.25), 0 0 0 1px rgba(212,145,29,0.12);">
        <svg width="32" height="32" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg">
            <text x="36" y="54" text-anchor="middle" font-family="Helvetica, Arial, sans-serif"
                  font-size="50" font-weight="bold" fill="#E8A832" letter-spacing="-2">A</text>
            <polyline points="6,36 18,36 22,28 27,44 32,24 37,48 42,28 47,44 52,36 66,36"
                      stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"
                      stroke-linejoin="round" fill="none" opacity="0.9"/>
            <circle cx="32" cy="24" r="2" fill="#E8A832" opacity="0.8"/>
            <circle cx="37" cy="48" r="2" fill="#E8A832" opacity="0.8"/>
        </svg>
    </div>
    <h1>ANXRISK</h1>
    <p>Sistema de Evaluación<br>de Riesgo de Ansiedad</p>
</div>
""", unsafe_allow_html=True)

# Stepper (solo visible fuera de Home)
if st.session_state.pagina_actual not in ("Home", "Análisis Masivo"):
    indice_actual = obtener_indice_pagina()

    for i, pagina in enumerate(ORDEN_PAGINAS, 1):
        completada = _pagina_completada(pagina)
        es_actual = (i == indice_actual)

        if completada:
            dot_class = "completed"
            label_class = "completed"
            check = ' <span style="color: var(--success); font-size: 1rem;">&#10003;</span>'
        elif es_actual:
            dot_class = "active"
            label_class = "active"
            check = ""
        else:
            dot_class = ""
            label_class = ""
            check = ""

        label = LABELS_SIDEBAR.get(pagina, pagina)
        st.sidebar.markdown(f"""
        <div class="anxrisk-progress-step">
            <span class="anxrisk-step-dot {dot_class}"></span>
            <span class="anxrisk-step-label {label_class}">{label}{check}</span>
        </div>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # Progress bar
    progress = indice_actual / len(ORDEN_PAGINAS)
    st.sidebar.progress(progress)

    completados = sum(1 for p in ORDEN_PAGINAS if _pagina_completada(p))
    st.sidebar.markdown(f"""
    <div class="anxrisk-sidebar-model">
        Progreso: {completados} / {len(ORDEN_PAGINAS)} secciones
    </div>
    """, unsafe_allow_html=True)

# Navigation when on Análisis Masivo
if st.session_state.pagina_actual == "Análisis Masivo":
    st.sidebar.markdown("---")
    if st.sidebar.button("Volver al Inicio", key="sidebar_volver_home", use_container_width=True):
        st.session_state.pagina_actual = "Home"
        st.rerun()
    if st.sidebar.button("Iniciar Evaluación Individual", key="sidebar_eval_individual", type="primary", use_container_width=True):
        st.session_state.pagina_actual = "Datos demograficos"
        st.rerun()

# Disclaimer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="anxrisk-disclaimer">
    Herramienta de apoyo a la decisión clínica. Los resultados deben ser interpretados
    en el contexto clínico completo del paciente.
</div>
""", unsafe_allow_html=True)


# ── ROUTING ────────────────────────────────────────────────
if st.session_state.pagina_actual == "Home":
    home.mostrar_home()
elif st.session_state.pagina_actual == "Análisis Masivo":
    analisis_masivo.mostrar_analisis_masivo()
elif st.session_state.pagina_actual == "Datos demograficos":
    demograficos.mostrar_demograficos()
elif st.session_state.pagina_actual == "LTE-12":
    if st.session_state.get('datos_demograficos') is None:
        st.session_state.pagina_actual = "Datos demograficos"
        st.rerun()
    mostrar_eventos_vitales()
elif st.session_state.pagina_actual == "SF-12 Física":
    if st.session_state.get('resultados', {}).get('eventos_vitales') is None:
        st.session_state.pagina_actual = "LTE-12"
        st.rerun()
    mostrar_sf12_fisica()
elif st.session_state.pagina_actual == "SF-12 Mental":
    mostrar_sf12_mental()
elif st.session_state.pagina_actual == "Ansiedad (HADS)":
    if st.session_state.get('resultados', {}).get('sf12') is None:
        st.session_state.pagina_actual = "SF-12 Física"
        st.rerun()
    mostrar_hads()
elif st.session_state.pagina_actual == "Ansiedad (ZSAS)":
    if st.session_state.get('resultados', {}).get('hads') is None:
        st.session_state.pagina_actual = "Ansiedad (HADS)"
        st.rerun()
    mostrar_zsas()
elif st.session_state.pagina_actual == "resultados":
    if st.session_state.get('resultados', {}).get('zsas') is None:
        st.session_state.pagina_actual = "Ansiedad (ZSAS)"
        st.rerun()
    resultados.mostrar_resultados()

import streamlit as st
from src.pages import (
    home,
    demograficos,
    datos_geneticos,
    mostrar_eventos_vitales,
    mostrar_sf12_fisica,
    mostrar_sf12_mental,
    mostrar_hads,
    mostrar_zsas,
    resultados
)

# Configuración de la página
st.set_page_config(
    page_title="Evaluación Psicológica Integral",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar y aplicar estilos CSS
with open("src/assets/styles/main.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



# Inicializar el estado de la aplicación
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Home"

# Definir el orden de las páginas para la barra de progreso
ORDEN_PAGINAS = ["Datos demograficos", "LTE-12", "SF-12 Física", "SF-12 Mental", "Ansiedad (HADS)", "Ansiedad (ZSAS)", "Datos Genéticos"]

# Configuración de la barra lateral
st.sidebar.title("Progreso de la Evaluación")

# Función para obtener el índice de la página actual
def obtener_indice_pagina():
    """Return the 1-based index of current page in ORDEN_PAGINAS.

    This is robust to legacy values in `st.session_state.pagina_actual`.
    If the current value isn't in ORDEN_PAGINAS we attempt a small mapping
    (e.g. 'SF-12 Salud' -> 'SF-12 Física'). If still not found, fall back to 1.
    """
    pagina = st.session_state.get('pagina_actual', 'Home')
    try:
        return ORDEN_PAGINAS.index(pagina) + 1
    except ValueError:
        # handle a few known legacy labels
        legacy_map = {
            'SF-12 Salud': 'SF-12 Física',
        }
        mapped = legacy_map.get(pagina)
        if mapped and mapped in ORDEN_PAGINAS:
            # update state to avoid repeating the problem
            st.session_state.pagina_actual = mapped
            return ORDEN_PAGINAS.index(mapped) + 1
        # fallback to 1 (Home / safe default)
        return 1

# Mostrar el progreso actual
if st.session_state.pagina_actual != "Home":
    st.sidebar.markdown(f"### Sección {obtener_indice_pagina()} de {len(ORDEN_PAGINAS)}")
    st.sidebar.markdown(f"**{st.session_state.pagina_actual}**")

# Mostrar el formulario según la página actual
if st.session_state.pagina_actual == "Home":
    home.mostrar_home()
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
    # no obligatorio chequear eventos aquí porque venimos desde SF-12 Física
    mostrar_sf12_mental()
elif st.session_state.pagina_actual == "Ansiedad (HADS)":
    if st.session_state.get('resultados', {}).get('sf12') is None:
        # redirect to start of SF-12 flow
        st.session_state.pagina_actual = "SF-12 Física"
        st.rerun()
    mostrar_hads()
elif st.session_state.pagina_actual == "Ansiedad (ZSAS)":
    if st.session_state.get('resultados', {}).get('hads') is None:
        st.session_state.pagina_actual = "Ansiedad (HADS)"
        st.rerun()
    mostrar_zsas()
elif st.session_state.pagina_actual == "Datos Genéticos":
    if st.session_state.get('resultados', {}).get('zsas') is None:
        st.session_state.pagina_actual = "Ansiedad (ZSAS)"
        st.rerun()
    datos_geneticos.mostrar_datos_geneticos()
elif st.session_state.pagina_actual == "resultados":
    if st.session_state.get('resultados', {}).get('datos_geneticos') is None:
        st.session_state.pagina_actual = "Datos Genéticos"
        st.rerun()
    resultados.mostrar_resultados()

# Mostrar barra de progreso en el sidebar solo si no estamos en Home
if st.session_state.pagina_actual != "Home":
    st.sidebar.markdown("---")
    progress = obtener_indice_pagina() / len(ORDEN_PAGINAS)
    st.sidebar.progress(progress)
    completados = len([k for k, v in st.session_state.get('resultados', {}).items()])
    st.sidebar.markdown(f"**Cuestionarios completados:** {completados} de {len(ORDEN_PAGINAS)}")

# Nota informativa en el sidebar
st.sidebar.markdown("---")
st.sidebar.info("""
**Nota**: Esta es una herramienta de evaluación preliminar.
Los resultados no constituyen un diagnóstico profesional.
Consulta con un profesional de la salud mental para una evaluación completa.
""")

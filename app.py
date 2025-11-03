import streamlit as st
from src.pages import (
    home,
    demograficos,
    datos_geneticos,
    mostrar_eventos_vitales,
    mostrar_sf12,
    mostrar_hads,
    mostrar_zsas
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
ORDEN_PAGINAS = ["Datos demograficos", "LTE-12", "SF-12 Salud", "Ansiedad (HADS)", "Ansiedad (ZSAS)", "Datos Genéticos"]

# Configuración de la barra lateral
st.sidebar.title("Progreso de la Evaluación")

# Función para obtener el índice de la página actual
def obtener_indice_pagina():
    return ORDEN_PAGINAS.index(st.session_state.pagina_actual) + 1

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
elif st.session_state.pagina_actual == "SF-12 Salud":
    if st.session_state.get('resultados', {}).get('eventos_vitales') is None:
        st.session_state.pagina_actual = "LTE-12"
        st.rerun()
    mostrar_sf12()
elif st.session_state.pagina_actual == "Ansiedad (HADS)":
    if st.session_state.get('resultados', {}).get('sf12') is None:
        st.session_state.pagina_actual = "SF-12 Salud"
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

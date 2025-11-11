"""
SF-12 - Componente Física (PCS)
"""
import streamlit as st
from ..utils.calculos import transformar_sf12_fisica_a_cuartil, transformar_sf12_fisica_a_label
from ..utils.dataframe_manager import mostrar_dataframe_actual


def mostrar_sf12_fisica():
    # Cargar estilos
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown(
        "<h1 style='text-align: center; color: #2E2E2E; font-size: 2rem; font-weight: 700;'>📋 SF-12 — Componente Física (PCS)</h1>",
        unsafe_allow_html=True
    )

    st.markdown("#### Responda las preguntas relacionadas con la salud física:")

    # Inicializar respuesta parcial (lista de 12 None)
    if 'sf12_partial' not in st.session_state:
        st.session_state['sf12_partial'] = [None] * 12

    respuestas = st.session_state['sf12_partial']

    # Pregunta 1
    opciones_salud = ["Seleccione una opción", "Excelente", "Muy buena", "Buena", "Regular", "Mala"]
    resp1 = st.selectbox("1. En general, ¿diría que su salud es?", options=opciones_salud, key="sf12_f_salud")
    respuestas[0] = opciones_salud.index(resp1) if resp1 != "Seleccione una opción" else None

    # Pregunta 2
    resp2 = st.radio("2. Esfuerzos moderados (mover una mesa,  caminar más de 1 hora)", ["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"], key="sf12_f_q2", horizontal=True)
    respuestas[1] = ( ["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"].index(resp2) + 1 ) if resp2 is not None else None

    # Pregunta 3
    resp3 = st.radio("3. Subir varios pisos por la escalera", ["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"], key="sf12_f_q3", horizontal=True)
    respuestas[2] = ( ["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"].index(resp3) + 1 ) if resp3 is not None else None

    # Pregunta 4
    resp4 = st.radio("4. ¿Hizo menos de lo que hubiera querido hacer?", ["Sí", "No"], key="sf12_f_q4", horizontal=True)
    respuestas[3] = 1 if resp4 == "Sí" else 2 if resp4 == "No" else None

    # Pregunta 5
    resp5 = st.radio("5. ¿Tuvo que dejar de hacer algunas tareas en su trabajo o en sus actividades cotidianas?", ["Sí", "No"], key="sf12_f_q5", horizontal=True)
    respuestas[4] = 1 if resp5 == "No" else 2 if resp5 == "Sí" else None

    # Pregunta 8 (dolor)
    resp8 = st.radio("8. ¿Hasta qué punto el dolor le ha dificultado su trabajo habitual?", ["Nada", "Un poco", "Regular", "Bastante", "Mucho"], key="sf12_f_q8", horizontal=True)
    respuestas[7] = (["Nada", "Un poco", "Regular", "Bastante", "Mucho"].index(resp8) + 1) if resp8 is not None else None

    # Guardar parcial en session_state
    st.session_state['sf12_partial'] = respuestas

    # Validación: asegurar que las preguntas de esta hoja estén completas
    faltan = any(respuestas[i] is None for i in [0,1,2,3,4,7])
    if faltan:
        st.error("❗ Por favor, responda todas las preguntas de la sección física antes de continuar.")
        disabled = True
    else:
        st.success("✅ Componente física completada")
        disabled = False

    col1, col2 = st.columns([2, 1])
    with col2:
        if st.button("Siguiente →", key="sf12_f_next", disabled=disabled, width='stretch'):
            # Ir a la página mental
            st.session_state.pagina_actual = "SF-12 Mental"
            st.rerun()

    st.markdown("---")
    with st.expander("Ver DataFrame completo"):
        mostrar_dataframe_actual()

    return None

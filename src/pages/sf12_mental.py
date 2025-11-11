"""
SF-12 - Componente Mental (MCS)
"""
import streamlit as st
from ..utils.calculos import calcular_sf12, transformar_sf12_fisica_a_cuartil, transformar_sf12_fisica_a_label
from ..utils.dataframe_manager import mostrar_dataframe_actual, agregar_o_actualizar_registro


def mostrar_sf12_mental():
    # Cargar estilos
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown(
        "<h1 style='text-align: center; color: #2E2E2E; font-size: 2rem; font-weight: 700;'>📋 SF-12 — Componente Mental (MCS)</h1>",
        unsafe_allow_html=True
    )

    st.markdown("#### Responda las preguntas relacionadas con la salud mental:")

    # Cargar parcial existente
    if 'sf12_partial' not in st.session_state:
        st.session_state['sf12_partial'] = [None] * 12
    respuestas = st.session_state['sf12_partial']

    # Preguntas 6 y 7 (problemas emocionales)
    resp6 = st.radio("6. ¿Hizo menos de lo que hubiera querido hacer, por algún problema emocional?", ["Sí", "No"], key="sf12_m_q6", horizontal=True)
    respuestas[5] = 1 if resp6 == "Sí" else 2 if resp6 == "No" else None

    resp7 = st.radio("7. ¿No hizo su trabajo o sus actividades tan cuidadosamente como de costumbre, por algún problema emocional?", ["Sí", "No"], key="sf12_m_q7", horizontal=True)
    respuestas[6] = 1 if resp7 == "Sí" else 2 if resp7 == "No" else None

    # Preguntas 9-11 (estado emocional)
    opciones_emoc = ["Seleccione una opción", "Siempre", "Casi siempre", "Muchas veces", "Algunas veces", "Sólo una vez", "Nunca"]
    resp9 = st.selectbox("9. ¿Se sintió calmado y tranquilo?", options=opciones_emoc, key="sf12_m_q9")
    respuestas[8] = opciones_emoc.index(resp9) if resp9 != "Seleccione una opción" else None

    resp10 = st.selectbox("10. ¿Tuvo mucha energía?", options=opciones_emoc, key="sf12_m_q10")
    respuestas[9] = opciones_emoc.index(resp10) if resp10 != "Seleccione una opción" else None

    resp11 = st.selectbox("11. ¿Se sintió desanimado y triste?", options=opciones_emoc, key="sf12_m_q11")
    respuestas[10] = opciones_emoc.index(resp11) if resp11 != "Seleccione una opción" else None

    # Pregunta 12 (actividades sociales)
    opciones_social = ["Seleccione una opción", "Siempre", "Casi siempre", "Muchas veces", "Algunas veces", "Sólo una vez", "Nunca"]
    resp12 = st.selectbox("12. Durante las 4 últimas semanas, ¿con qué frecuencia la salud física o los problemas emocionales le han dificultado sus actividades sociales?", options=opciones_social, key="sf12_m_q12")
    respuestas[11] = opciones_social.index(resp12) if resp12 != "Seleccione una opción" else None

    # Guardar en session_state
    st.session_state['sf12_partial'] = respuestas

    faltan = any(respuestas[i] is None for i in [5,6,8,9,10,11])
    if faltan:
        st.error("❗ Por favor, responda todas las preguntas de la sección mental antes de continuar.")
        disabled = True
    else:
        st.success("✅ Componente mental completada")
        disabled = False

    col1, col2 = st.columns([2,1])
    with col2:
        if st.button("Finalizar SF-12 →", key="sf12_m_done", disabled=disabled, width='stretch'):
            # Montar respuestas completas y calcular puntuaciones
            resultados = calcular_sf12(respuestas)
            fisica = resultados.get('fisica')
            mental = resultados.get('mental')
            total = resultados.get('total')

            cuartil = transformar_sf12_fisica_a_cuartil(fisica)
            etiqueta = transformar_sf12_fisica_a_label(fisica)

            if 'resultados' not in st.session_state:
                st.session_state.resultados = {}
            st.session_state.resultados['sf12'] = {
                'puntaje_fisico': fisica,
                'puntaje_mental': mental,
                'total': total,
                'cuartil': cuartil,
                'cuartil_label': etiqueta,
                'respuestas': respuestas
            }

            # Persistir en DataFrame
            agregar_o_actualizar_registro(
                {
                    'salud_fisica': fisica,
                    'salud_mental': mental,
                    'sf12_fisica_cuartil': cuartil,
                    'sf12_fisica_cuartil_label': etiqueta
                },
                tipo_datos='sf12'
            )

            # Avanzar a HADS
            st.session_state.pagina_actual = "Ansiedad (HADS)"
            st.rerun()

    st.markdown("---")
    with st.expander("Ver DataFrame completo"):
        mostrar_dataframe_actual()

    return None

"""
SF-12 - Componente Mental (MCS)
"""
import streamlit as st
from ..utils.calculos import (
    calcular_sf12,
    transformar_sf12_fisica_a_cuartil,
    transformar_sf12_fisica_a_label,
    transformar_sf12_mental_a_cuartil,
    transformar_sf12_mental_a_label,
)
from ..utils.dataframe_manager import agregar_o_actualizar_registro


def mostrar_sf12_mental():
    # Page header
    st.markdown("""
    <div class="anxrisk-page-header">
        <h1>SF-12 — Componente Mental (MCS)</h1>
        <p>Evalúa el bienestar emocional y mental del paciente mediante 6 ítems</p>
    </div>
    """, unsafe_allow_html=True)

    # Context card
    st.markdown("""
    <div class="anxrisk-card">
        <h3>Evaluación de la Salud Mental</h3>
        <p style="margin-bottom: 0.75rem;">
            El componente mental (MCS) del <strong>SF-12</strong> evalúa aspectos clave del bienestar
            emocional y mental, incluyendo el estado emocional, la vitalidad, las limitaciones en
            actividades por problemas emocionales y la salud mental percibida.
        </p>
        <p style="font-size: 0.9375rem; color: var(--text-secondary); font-style: italic; text-align: center; margin-bottom: 0.5rem;">
            Todas las preguntas son obligatorias
        </p>
        <p style="font-size: 0.875rem; color: var(--text-secondary); text-align: center; margin: 0;">
            Ware, J. E., Kosinski, M., & Keller, S. D. (1996). <em>Medical Care</em>, 34(3), 220-233.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="anxrisk-question-card section-sf12">
        <div class="anxrisk-question-text">Responda las preguntas relacionadas con la salud mental:</div>
    </div>
    """, unsafe_allow_html=True)

    # --- Ensure the form is NOT pre-filled ---
    if 'sf12_m_cleared' not in st.session_state:
        keys_to_clear = [
            'sf12_partial',
            'sf12_m_q6', 'sf12_m_q7', 'sf12_m_q9', 'sf12_m_q10', 'sf12_m_q11', 'sf12_m_q12',
            'sf12_m_q1', 'sf12_m_q2', 'sf12_m_q3', 'sf12_m_q4', 'sf12_m_q5', 'sf12_m_q6',
        ]
        for k in keys_to_clear:
            if k in st.session_state:
                del st.session_state[k]
        st.session_state['sf12_m_cleared'] = True

    if 'sf12_m_partial' not in st.session_state:
        st.session_state['sf12_m_partial'] = [None] * 6
    m = st.session_state['sf12_m_partial']

    opciones_binario = ["Sí", "No"]
    opciones_frecuencia = ["Siempre", "Casi siempre", "Algunas veces", "Sólo alguna vez", "Nunca"]
    opciones_tiempo = ["Siempre", "Casi siempre", "Muchas veces", "Algunas veces", "Sólo una vez", "Nunca"]

    # Inline progress bar
    sf12m_answered = sum(1 for v in m if v is not None)
    sf12m_pct = (sf12m_answered / 6) * 100
    st.markdown(f"""
    <div class="anxrisk-inline-progress">
        <div class="anxrisk-inline-progress-bar" style="width: {sf12m_pct}%;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Pregunta 1
    st.markdown("""
    <div class="anxrisk-question-card section-sf12">
        <div class="anxrisk-question-number section-sf12">Pregunta 1 de 6</div>
        <div class="anxrisk-question-text">¿Hizo menos de lo que hubiera querido hacer, por algún problema emocional?</div>
    </div>
    """, unsafe_allow_html=True)
    resp1 = None
    _, col_r1, _ = st.columns([1, 2, 1])
    with col_r1:
        resp1 = st.radio("Pregunta 1", options=opciones_binario, key="sf12_m_q1", horizontal=True, index=None, label_visibility="collapsed")
    if resp1 == "Sí":
        m[0] = 1
    elif resp1 == "No":
        m[0] = 2
    else:
        m[0] = None

    # Pregunta 2
    st.markdown("""
    <div class="anxrisk-question-card section-sf12">
        <div class="anxrisk-question-number section-sf12">Pregunta 2 de 6</div>
        <div class="anxrisk-question-text">¿No hizo su trabajo o sus actividades cotidianas tan cuidadosamente como de costumbre, por algún problema emocional?</div>
    </div>
    """, unsafe_allow_html=True)
    resp2 = None
    _, col_r2, _ = st.columns([1, 2, 1])
    with col_r2:
        resp2 = st.radio("Pregunta 2", options=opciones_binario, key="sf12_m_q2", horizontal=True, index=None, label_visibility="collapsed")
    if resp2 == "Sí":
        m[1] = 1
    elif resp2 == "No":
        m[1] = 2
    else:
        m[1] = None

    # Pregunta 3
    st.markdown("""
    <div class="anxrisk-question-card section-sf12">
        <div class="anxrisk-question-number section-sf12">Pregunta 3 de 6</div>
        <div class="anxrisk-question-text">¿Con qué frecuencia la salud física o los problemas emocionales le han dificultado sus actividades sociales?</div>
    </div>
    """, unsafe_allow_html=True)
    resp3 = st.selectbox("Pregunta 3", options=opciones_frecuencia, key="sf12_m_q3", index=None, placeholder="Seleccione una opción", label_visibility="collapsed")
    if resp3 is None:
        m[2] = None
    else:
        opciones_frecuencia_full = ["Seleccione una opción"] + opciones_frecuencia
        m[2] = opciones_frecuencia_full.index(resp3)

    # Pregunta 4
    st.markdown("""
    <div class="anxrisk-question-card section-sf12">
        <div class="anxrisk-question-number section-sf12">Pregunta 4 de 6</div>
        <div class="anxrisk-question-text">¿Se sintió calmado y tranquilo? ¿Cuánto tiempo?</div>
    </div>
    """, unsafe_allow_html=True)
    resp4 = st.selectbox("Pregunta 4", options=opciones_tiempo, key="sf12_m_q4", index=None, placeholder="Seleccione una opción", label_visibility="collapsed")
    if resp4 is None:
        m[3] = None
    else:
        opciones_tiempo_full = ["Seleccione una opción"] + opciones_tiempo
        index = opciones_tiempo_full.index(resp4)
        m[3] = 7 - index

    # Pregunta 5
    st.markdown("""
    <div class="anxrisk-question-card section-sf12">
        <div class="anxrisk-question-number section-sf12">Pregunta 5 de 6</div>
        <div class="anxrisk-question-text">¿Tuvo mucha energía? ¿Cuánto tiempo?</div>
    </div>
    """, unsafe_allow_html=True)
    resp5 = st.selectbox("Pregunta 5", options=opciones_tiempo, key="sf12_m_q5", index=None, placeholder="Seleccione una opción", label_visibility="collapsed")
    if resp5 is None:
        m[4] = None
    else:
        opciones_tiempo_full = ["Seleccione una opción"] + opciones_tiempo
        index = opciones_tiempo_full.index(resp5)
        m[4] = 7 - index

    # Pregunta 6
    st.markdown("""
    <div class="anxrisk-question-card section-sf12">
        <div class="anxrisk-question-number section-sf12">Pregunta 6 de 6</div>
        <div class="anxrisk-question-text">¿Se ha sentido desanimado(a) y triste? ¿Cuánto tiempo?</div>
    </div>
    """, unsafe_allow_html=True)
    resp6 = st.selectbox("Pregunta 6", options=opciones_tiempo, key="sf12_m_q6", index=None, placeholder="Seleccione una opción", label_visibility="collapsed")
    if resp6 is None:
        m[5] = None
    else:
        opciones_tiempo_full = ["Seleccione una opción"] + opciones_tiempo
        m[5] = opciones_tiempo_full.index(resp6)

    st.session_state['sf12_m_partial'] = m

    faltan = any(m[i] is None for i in range(6))
    if faltan:
        st.error("Responda todas las preguntas de la sección mental antes de continuar.")
        disabled = True
    else:
        st.success("Componente mental completada")
        disabled = False

    col1, col2 = st.columns([2, 1])
    with col2:
        if st.button("Finalizar SF-12", key="sf12_m_done", disabled=disabled, type="primary", use_container_width=True):
            full_respuestas = None
            if 'sf12_partial' in st.session_state and isinstance(st.session_state['sf12_partial'], list) and len(st.session_state['sf12_partial']) == 12:
                full_respuestas = st.session_state['sf12_partial'][:]
            else:
                full_respuestas = [None] * 12

            mapping = {0:5, 1:6, 2:8, 3:9, 4:10, 5:11}
            for mi, val in enumerate(m):
                full_respuestas[mapping[mi]] = val

            st.session_state['sf12_partial'] = full_respuestas

            resultados = calcular_sf12(full_respuestas)
            fisica = resultados.get('fisica')
            mental = resultados.get('mental')
            total = resultados.get('total')

            cuartil = transformar_sf12_mental_a_cuartil(mental)
            etiqueta = transformar_sf12_mental_a_label(mental)

            if 'resultados' not in st.session_state:
                st.session_state.resultados = {}
            sf12 = st.session_state.resultados.get('sf12', {})
            sf12.update({
                'puntaje_mental': mental,
                'cuartil_mental': cuartil,
                'cuartil_mental_label': etiqueta,
                'respuestas': full_respuestas
            })
            st.session_state.resultados['sf12'] = sf12

            agregar_o_actualizar_registro(
                {
                    'salud_fisica': fisica,
                    'salud_mental': mental,
                    'sf12_mental_cuartil': cuartil,
                    'sf12_mental_cuartil_label': etiqueta
                },
                tipo_datos='sf12'
            )

            st.session_state.pagina_actual = "Ansiedad (HADS)"
            st.rerun()

    return None

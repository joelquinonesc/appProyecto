"""
SF-12 - Componente Física (PCS)
"""
import streamlit as st
from ..utils.calculos import (
    transformar_sf12_fisica_a_cuartil,
    transformar_sf12_fisica_a_label,
    calcular_sf12,
)
from ..utils.dataframe_manager import agregar_o_actualizar_registro


def mostrar_sf12_fisica():
    # Page header
    st.markdown("""
    <div class="anxrisk-page-header">
        <h1>SF-12 — Componente Física (PCS)</h1>
        <p>Evalúa la percepción de salud física del paciente mediante 6 ítems</p>
    </div>
    """, unsafe_allow_html=True)

    # Context card
    st.markdown("""
    <div class="anxrisk-card">
        <h3>Evaluación de la Salud Física</h3>
        <p style="margin-bottom: 0.75rem; text-align: center;">
            El <strong>SF-12 (Short Form-12)</strong> es un cuestionario de calidad de vida validado
            internacionalmente. El componente físico (PCS) evalúa la percepción sobre el estado de
            salud física, las limitaciones funcionales y el impacto en actividades cotidianas.
        </p>
        <p style="font-size: 0.9375rem; color: var(--text-secondary); font-style: italic; text-align: center; margin-bottom: 0.5rem;">
            Todas las preguntas son obligatorias
        </p>
        <p style="font-size: 0.875rem; color: var(--text-secondary); text-align: center; margin: 0;">
            Ware, J. E., Kosinski, M., & Keller, S. D. (1996). <em>Medical Care</em>, 34(3), 220-233.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- Ensure the form is NOT pre-filled on first visit ---
    keys_to_clear = [
        'sf12_partial',
        'sf12_f_salud',
        'sf12_f_q2',
        'sf12_f_q3',
        'sf12_f_q4',
        'sf12_f_q5',
        'sf12_f_q6',
    ]
    if 'sf12_f_cleared' not in st.session_state:
        for k in keys_to_clear:
            if k in st.session_state:
                del st.session_state[k]
        if 'sf12_partial' not in st.session_state:
            st.session_state['sf12_partial'] = [None] * 12
        st.session_state['sf12_f_partial'] = [None] * 6
        st.session_state['sf12_f_cleared'] = True

    if 'sf12_f_partial' not in st.session_state:
        st.session_state['sf12_f_partial'] = [None] * 6

    m = st.session_state['sf12_f_partial']

    # Pregunta 1
    st.markdown("""
    <div class="anxrisk-question-card">
        <div class="anxrisk-question-number">Pregunta 1 de 6</div>
        <div class="anxrisk-question-text">En general, ¿diría que su salud es?</div>
    </div>
    """, unsafe_allow_html=True)
    opciones_salud = ["Excelente", "Muy buena", "Buena", "Regular", "Mala"]
    resp1 = st.selectbox("Pregunta 1", options=opciones_salud, key="sf12_f_salud", index=None, placeholder="Seleccione una opción", label_visibility="collapsed")
    if resp1 is None:
        m[0] = None
    else:
        scoring = {"Excelente": 5, "Muy buena": 4, "Buena": 3, "Regular": 2, "Mala": 1}
        m[0] = scoring[resp1]

    # Pregunta 2
    st.markdown("""
    <div class="anxrisk-question-card">
        <div class="anxrisk-question-number">Pregunta 2 de 6</div>
        <div class="anxrisk-question-text">Esfuerzos moderados (mover una mesa, caminar más de 1 hora)</div>
    </div>
    """, unsafe_allow_html=True)
    resp2 = None
    _, col_r2, _ = st.columns([1, 3, 1])
    with col_r2:
        resp2 = st.radio("Pregunta 2", ["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"], key="sf12_f_q2", horizontal=True, index=None, label_visibility="collapsed")
    m[1] = (["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"].index(resp2) + 1) if resp2 is not None else None

    # Pregunta 3
    st.markdown("""
    <div class="anxrisk-question-card">
        <div class="anxrisk-question-number">Pregunta 3 de 6</div>
        <div class="anxrisk-question-text">Subir varios pisos por la escalera</div>
    </div>
    """, unsafe_allow_html=True)
    resp3 = None
    _, col_r3, _ = st.columns([1, 3, 1])
    with col_r3:
        resp3 = st.radio("Pregunta 3", ["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"], key="sf12_f_q3", horizontal=True, index=None, label_visibility="collapsed")
    m[2] = (["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"].index(resp3) + 1) if resp3 is not None else None

    st.markdown("""
    <div class="anxrisk-question-card">
        <div class="anxrisk-question-text">Durante las 4 últimas semanas, ¿ha tenido alguno de los siguientes problemas en su trabajo o en sus actividades cotidianas, a causa de su salud física?</div>
    </div>
    """, unsafe_allow_html=True)

    # Pregunta 4
    st.markdown("""
    <div class="anxrisk-question-card">
        <div class="anxrisk-question-number">Pregunta 4 de 6</div>
        <div class="anxrisk-question-text">¿Hizo menos de lo que hubiera querido hacer?</div>
    </div>
    """, unsafe_allow_html=True)
    resp4 = None
    _, col_r4, _ = st.columns([1, 2, 1])
    with col_r4:
        resp4 = st.radio("Pregunta 4", ["Sí", "No"], key="sf12_f_q4", horizontal=True, index=None, label_visibility="collapsed")
    m[3] = 1 if resp4 == "Sí" else 2 if resp4 == "No" else None

    # Pregunta 5
    st.markdown("""
    <div class="anxrisk-question-card">
        <div class="anxrisk-question-number">Pregunta 5 de 6</div>
        <div class="anxrisk-question-text">¿Tuvo que dejar de hacer algunas tareas en su trabajo o en sus actividades cotidianas?</div>
    </div>
    """, unsafe_allow_html=True)
    resp5 = None
    _, col_r5, _ = st.columns([1, 2, 1])
    with col_r5:
        resp5 = st.radio("Pregunta 5", ["Sí", "No"], key="sf12_f_q5", horizontal=True, index=None, label_visibility="collapsed")
    m[4] = 1 if resp5 == "Sí" else 2 if resp5 == "No" else None

    # Pregunta 6
    st.markdown("""
    <div class="anxrisk-question-card">
        <div class="anxrisk-question-number">Pregunta 6 de 6</div>
        <div class="anxrisk-question-text">¿Hasta qué punto el dolor le ha dificultado su trabajo habitual?</div>
    </div>
    """, unsafe_allow_html=True)
    resp6 = None
    _, col_r6, _ = st.columns([1, 3, 1])
    with col_r6:
        resp6 = st.radio("Pregunta 6", ["Nada", "Un poco", "Regular", "Bastante", "Mucho"], key="sf12_f_q6", horizontal=True, index=None, label_visibility="collapsed")
    m[5] = (5 - ["Nada", "Un poco", "Regular", "Bastante", "Mucho"].index(resp6)) if resp6 is not None else None

    st.session_state['sf12_f_partial'] = m

    def _answered(key, placeholder=None):
        if key not in st.session_state:
            return False
        val = st.session_state.get(key)
        if val is None:
            return False
        if placeholder is not None and val == placeholder:
            return False
        return True

    required_keys = [
        ('sf12_f_salud', None),
        ('sf12_f_q2', None),
        ('sf12_f_q3', None),
        ('sf12_f_q4', None),
        ('sf12_f_q5', None),
        ('sf12_f_q6', None),
    ]

    faltan = not all(_answered(k, p) for k, p in required_keys)
    if faltan:
        st.error("Responda todas las preguntas de la sección física antes de continuar.")
        disabled = True
    else:
        st.success("Componente física completada")
        disabled = False

    col1, col2 = st.columns([2, 1])
    with col2:
        if st.button("Siguiente", key="sf12_f_next", disabled=disabled, type="primary", use_container_width=True):
            full_respuestas = None
            if 'sf12_partial' in st.session_state and isinstance(st.session_state['sf12_partial'], list) and len(st.session_state['sf12_partial']) == 12:
                full_respuestas = st.session_state['sf12_partial'][:]
            else:
                full_respuestas = [None] * 12

            mapping = {0:0, 1:1, 2:2, 3:3, 4:4, 5:7}
            for mi, val in enumerate(m):
                full_respuestas[mapping[mi]] = val

            st.session_state['sf12_partial'] = full_respuestas

            resultados = calcular_sf12(full_respuestas)
            fisica = resultados.get('fisica')
            mental = resultados.get('mental')
            total = resultados.get('total')

            cuartil_fis = transformar_sf12_fisica_a_cuartil(fisica)
            etiqueta_fis = transformar_sf12_fisica_a_label(fisica)

            if 'resultados' not in st.session_state:
                st.session_state.resultados = {}
            sf12 = st.session_state.resultados.get('sf12', {})
            sf12.update({
                'puntaje_fisico': fisica,
                'cuartil_fisica': cuartil_fis,
                'cuartil_fisica_label': etiqueta_fis,
                'respuestas': full_respuestas
            })
            st.session_state.resultados['sf12'] = sf12

            agregar_o_actualizar_registro(
                {
                    'salud_fisica': fisica,
                    'sf12_fisica_cuartil': cuartil_fis,
                    'sf12_fisica_cuartil_label': etiqueta_fis
                },
                tipo_datos='sf12'
            )

            st.session_state.pagina_actual = "SF-12 Mental"
            st.rerun()

    return None

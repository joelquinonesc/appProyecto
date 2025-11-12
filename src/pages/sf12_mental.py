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

    # --- Ensure the form is NOT pre-filled ---
    # Remove any previous per-field session keys so the form always starts empty.
    # The mental component of SF-12 maps to item indices [5,6,8,9,10,11] (0-based)
    # Limpiar tanto claves antiguas (6..12) como las nuevas (1..6) UNA SOLA VEZ al entrar
    # (evita borrar las selecciones en cada rerun de Streamlit)
    if 'sf12_m_cleared' not in st.session_state:
        keys_to_clear = [
            'sf12_partial',
            # antiguas
            'sf12_m_q6', 'sf12_m_q7', 'sf12_m_q9', 'sf12_m_q10', 'sf12_m_q11', 'sf12_m_q12',
            # nuevas (formulario independiente): q1..q6
            'sf12_m_q1', 'sf12_m_q2', 'sf12_m_q3', 'sf12_m_q4', 'sf12_m_q5', 'sf12_m_q6',
        ]
        for k in keys_to_clear:
            if k in st.session_state:
                del st.session_state[k]
        st.session_state['sf12_m_cleared'] = True

    # Inicializar respuesta parcial independiente (lista de 6 None) para la sección mental
    if 'sf12_m_partial' not in st.session_state:
        st.session_state['sf12_m_partial'] = [None] * 6
    m = st.session_state['sf12_m_partial']

    # Preguntas 1 y 2 (problemas emocionales) -> corresponden internamente a posiciones 5 y 6
    resp1 = st.radio("1. ¿Hizo menos de lo que hubiera querido hacer, por algún problema emocional?", ["Sí", "No"], key="sf12_m_q1", horizontal=True, index=None)
    # Radios: mapear a 0/1 (Sí=0, No=1)
    m[0] = 0 if resp1 == "Sí" else 1 if resp1 == "No" else None

    resp2 = st.radio("2. ¿No hizo su trabajo o sus actividades tan cuidadosamente como de costumbre, por algún problema emocional?", ["Sí", "No"], key="sf12_m_q2", horizontal=True, index=None)
    m[1] = 0 if resp2 == "Sí" else 1 if resp2 == "No" else None

    # Preguntas 9-11 (estado emocional) -> posiciones 8,9,10
    opciones_emoc = ["Seleccione una opción", "Siempre", "Casi siempre", "Muchas veces", "Algunas veces", "Sólo una vez", "Nunca"]
    # Preguntas 3-5 (estado emocional) -> posiciones 8,9,10
    resp3 = st.selectbox("3. ¿Se sintió calmado y tranquilo?", options=opciones_emoc, key="sf12_m_q3", index=None)
    if resp3 is None or resp3 == "Seleccione una opción":
        m[2] = None
    else:
        # Restar 1 para que las opciones válidas empiecen en 0 (placeholder está en 0)
        m[2] = opciones_emoc.index(resp3) - 1

    resp4 = st.selectbox("4. ¿Tuvo mucha energía?", options=opciones_emoc, key="sf12_m_q4", index=None)
    if resp4 is None or resp4 == "Seleccione una opción":
        m[3] = None
    else:
        m[3] = opciones_emoc.index(resp4) - 1

    resp5 = st.selectbox("5. ¿Se sintió desanimado y triste?", options=opciones_emoc, key="sf12_m_q5", index=None)
    if resp5 is None or resp5 == "Seleccione una opción":
        m[4] = None
    else:
        m[4] = opciones_emoc.index(resp5) - 1

    # Pregunta 12 (actividades sociales) -> posición 11
    opciones_social = ["Seleccione una opción", "Siempre", "Casi siempre", "Muchas veces", "Algunas veces", "Sólo una vez", "Nunca"]
    resp6 = st.selectbox("6. Durante las 4 últimas semanas, ¿con qué frecuencia la salud física o los problemas emocionales le han dificultado sus actividades sociales?", options=opciones_social, key="sf12_m_q6", index=None)
    if resp6 is None or resp6 == "Seleccione una opción":
        m[5] = None
    else:
        m[5] = opciones_social.index(resp6) - 1

    # Guardar parcial mental en session_state
    st.session_state['sf12_m_partial'] = m

    # Validar que los ítems de la sección mental estén todos respondidos (m indices 0..5)
    faltan = any(m[i] is None for i in range(6))
    if faltan:
        st.error("❗ Por favor, responda todas las preguntas de la sección mental antes de continuar.")
        disabled = True
    else:
        st.success("✅ Componente mental completada")
        disabled = False

    col1, col2 = st.columns([2,1])
    with col2:
        if st.button("Finalizar SF-12 →", key="sf12_m_done", disabled=disabled, width='stretch'):
            # Montar respuestas completas: combinar respuestas físicas existentes (si las hay)
            # con las respuestas mentales actuales para formar la lista de 12 ítems requerida
            full_respuestas = None
            if 'sf12_partial' in st.session_state and isinstance(st.session_state['sf12_partial'], list) and len(st.session_state['sf12_partial']) == 12:
                full_respuestas = st.session_state['sf12_partial'][:]  # copiar
            else:
                full_respuestas = [None] * 12

            # Mapear m (0..5) a las posiciones originales [5,6,8,9,10,11]
            mapping = {0:5, 1:6, 2:8, 3:9, 4:10, 5:11}
            for mi, val in enumerate(m):
                full_respuestas[mapping[mi]] = val

            # Guardar parcial combinado en session_state
            st.session_state['sf12_partial'] = full_respuestas

            # Calcular puntuaciones
            resultados = calcular_sf12(full_respuestas)
            fisica = resultados.get('fisica')
            mental = resultados.get('mental')
            total = resultados.get('total')

            # Clasificación mental: usar el puntaje mental para determinar cuartil mental
            cuartil = transformar_sf12_mental_a_cuartil(mental)
            etiqueta = transformar_sf12_mental_a_label(mental)

            if 'resultados' not in st.session_state:
                st.session_state.resultados = {}
            st.session_state.resultados['sf12'] = {
                'puntaje_fisico': fisica,
                'puntaje_mental': mental,
                'total': total,
                'cuartil': cuartil,
                'cuartil_label': etiqueta,
                'respuestas': full_respuestas
            }

            # Persistir en DataFrame
            # Persistir solo los puntajes y el cuartil correspondiente a la componente mental.
            # La columna `sf12_fisica_cuartil` debe ser escrita únicamente por la página física.
            agregar_o_actualizar_registro(
                {
                    'salud_fisica': fisica,
                    'salud_mental': mental,
                    'sf12_mental_cuartil': cuartil,
                    'sf12_mental_cuartil_label': etiqueta
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

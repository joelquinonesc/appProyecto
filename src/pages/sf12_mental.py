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

    # Texto explicativo
    st.markdown("""
    <div style="background: #FFFFFF; padding: 1.25rem; margin: 0.75rem 0 1.5rem 0; border-radius: 8px; border: 1px solid #E0E0E0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <h4 style="color: #2E2E2E; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">
        Evaluación de la Salud Mental
        </h4>
        <p style="color: #2E2E2E; font-size: 1rem; line-height: 1.7; text-align: justify; margin-bottom: 0.75rem;">
        El componente mental (MCS) del <strong>SF-12</strong> evalúa aspectos clave del bienestar emocional y mental, 
        incluyendo el estado emocional, la vitalidad, las limitaciones en actividades por problemas emocionales y la salud mental percibida.
        </p>
        <p style="color: #666666; font-style: italic; text-align: center; margin-top: 1rem; margin-bottom: 0.5rem; font-size: 1.05rem;">
        <strong>⚠️ Todas las preguntas son obligatorias</strong>
        </p>
        <p style="color: #888888; font-size: 0.9rem; text-align: center; margin: 0.5rem 0 0 0;">
        <em>Ware, J. E., Kosinski, M., & Keller, S. D. (1996). A 12-item short-form health survey: construction of scales and preliminary tests of reliability and validity. Medical Care, 34(3), 220-233.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)

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

    # Preguntas del componente mental SF-12
    opciones_binario = ["Seleccione una opción", "Sí", "No"]
    opciones_frecuencia = ["Seleccione una opción", "Siempre", "Casi siempre", "Algunas veces", "Sólo alguna vez", "Nunca"]
    opciones_tiempo = ["Seleccione una opción", "Siempre", "Casi siempre", "Muchas veces", "Algunas veces", "Sólo una vez", "Nunca"]
    
    # Pregunta 1: ¿Hizo menos de lo que hubiera querido hacer, por algún problema emocional?
    resp1 = st.radio("1. ¿Hizo menos de lo que hubiera querido hacer, por algún problema emocional?", options=opciones_binario[1:], key="sf12_m_q1", horizontal=True, index=None)
    if resp1 == "Sí":
        m[0] = 1
    elif resp1 == "No":
        m[0] = 2
    else:
        m[0] = None
    
    # Pregunta 2: ¿No hizo su trabajo o sus actividades cotidianas tan cuidadosamente como de costumbre, por algún problema emocional?
    resp2 = st.radio("2. ¿No hizo su trabajo o sus actividades cotidianas tan cuidadosamente como de costumbre, por algún problema emocional?", options=opciones_binario[1:], key="sf12_m_q2", horizontal=True, index=None)
    if resp2 == "Sí":
        m[1] = 1
    elif resp2 == "No":
        m[1] = 2
    else:
        m[1] = None
    
    # Pregunta 3: ¿Con qué frecuencia la salud física o los problemas emocionales le han dificultado sus actividades sociales?
    resp3 = st.selectbox("3. ¿Con qué frecuencia la salud física o los problemas emocionales le han dificultado sus actividades sociales (como visitar a los amigos o familiares)?", options=opciones_frecuencia, key="sf12_m_q3", index=None)
    if resp3 == "Seleccione una opción" or resp3 is None:
        m[2] = None
    else:
        m[2] = opciones_frecuencia.index(resp3)
    
    # Pregunta 4: ¿Se sintió calmado y tranquilo? ¿Cuánto tiempo?
    resp4 = st.selectbox("4. ¿Se sintió calmado y tranquilo? ¿Cuánto tiempo?", options=opciones_tiempo, key="sf12_m_q4", index=None)
    if resp4 == "Seleccione una opción" or resp4 is None:
        m[3] = None
    else:
        # Siempre (6), Casi siempre (5), ..., Nunca (1)
        index = opciones_tiempo.index(resp4)
        m[3] = 7 - index  # 7-1=6 for Siempre, 7-6=1 for Nunca
    
    # Pregunta 5: ¿Tuvo mucha energía? ¿Cuánto tiempo?
    resp5 = st.selectbox("5. ¿Tuvo mucha energía? ¿Cuánto tiempo?", options=opciones_tiempo, key="sf12_m_q5", index=None)
    if resp5 == "Seleccione una opción" or resp5 is None:
        m[4] = None
    else:
        index = opciones_tiempo.index(resp5)
        m[4] = 7 - index  # Siempre (6), ..., Nunca (1)
    
    # Pregunta 6: ¿Se ha sentido desanimado(a) y triste? ¿Cuánto tiempo?
    resp6 = st.selectbox("6. ¿Se ha sentido desanimado(a) y triste? ¿Cuánto tiempo?", options=opciones_tiempo, key="sf12_m_q6", index=None)
    if resp6 == "Seleccione una opción" or resp6 is None:
        m[5] = None
    else:
        # Siempre (1), Casi siempre (2), ..., Nunca (6)
        m[5] = opciones_tiempo.index(resp6)

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
            # Mantener/merge si ya existe la estructura 'sf12' creada por la otra sección
            sf12 = st.session_state.resultados.get('sf12', {})
            # SOLO actualizar los valores relacionados con MENTAL
            # NO sobrescribir puntaje_fisico que fue calculado en la página física
            sf12.update({
                'puntaje_mental': mental,
                'cuartil_mental': cuartil,
                'cuartil_mental_label': etiqueta,
                'respuestas': full_respuestas
            })
            st.session_state.resultados['sf12'] = sf12

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

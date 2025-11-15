"""
SF-12 - Componente Física (PCS)
"""
import streamlit as st
from ..utils.calculos import (
    transformar_sf12_fisica_a_cuartil,
    transformar_sf12_fisica_a_label,
    calcular_sf12,
)
from ..utils.dataframe_manager import mostrar_dataframe_actual, agregar_o_actualizar_registro


def mostrar_sf12_fisica():
    # Cargar estilos
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown(
        "<h1 style='text-align: center; color: #2E2E2E; font-size: 2rem; font-weight: 700;'>SF-12 — Componente Física (PCS)</h1>",
        unsafe_allow_html=True
    )

    st.markdown("#### Responda las preguntas relacionadas con la salud física:")

    # --- Ensure the form is NOT pre-filled on first visit ---
    # We clear previous per-field session keys only once (first time the page is shown)
    # to avoid wiping user input on every rerun (which would break validation).
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
        # Inicializar parcial global si no existe
        if 'sf12_partial' not in st.session_state:
            st.session_state['sf12_partial'] = [None] * 12
        # Inicializar parcial específico de física (6 items)
        st.session_state['sf12_f_partial'] = [None] * 6
        st.session_state['sf12_f_cleared'] = True

    # Asegurar que existe el parcial físico
    if 'sf12_f_partial' not in st.session_state:
        st.session_state['sf12_f_partial'] = [None] * 6

    m = st.session_state['sf12_f_partial']

    # Pregunta 1
    opciones_salud = ["Seleccione una opción", "Excelente", "Muy buena", "Buena", "Regular", "Mala"]
    resp1 = st.selectbox("1. En general, ¿diría que su salud es?", options=opciones_salud, key="sf12_f_salud", index=None)
    # `resp1` puede ser None cuando no hay selección (index=None). Manejar ambos casos.
    if resp1 is None or resp1 == "Seleccione una opción":
        m[0] = None
    else:
        # Puntuación estándar SF-12: Excelente=5, Muy buena=4, Buena=3, Regular=2, Mala=1
        scoring = {"Excelente": 5, "Muy buena": 4, "Buena": 3, "Regular": 2, "Mala": 1}
        m[0] = scoring[resp1]

    # Pregunta 2
    resp2 = st.radio("2. Esfuerzos moderados (mover una mesa,  caminar más de 1 hora)", ["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"], key="sf12_f_q2", horizontal=True, index=None)
    m[1] = (["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"].index(resp2) + 1) if resp2 is not None else None

    # Pregunta 3
    resp3 = st.radio("3. Subir varios pisos por la escalera", ["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"], key="sf12_f_q3", horizontal=True, index=None)
    m[2] = (["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"].index(resp3) + 1) if resp3 is not None else None

    st.markdown("####  Durante las 4 últimas semanas, ¿ha tenido alguno de los siguientes problemas en su trabajo o en sus actividades cotidianas, a causa de su salud física? :")

    # Pregunta 4
    resp4 = st.radio("4. ¿Hizo menos de lo que hubiera querido hacer?", ["Sí", "No"], key="sf12_f_q4", horizontal=True, index=None)
    # Radios: Sí=1, No=2
    m[3] = 1 if resp4 == "Sí" else 2 if resp4 == "No" else None

    # Pregunta 5
    resp5 = st.radio("5. ¿Tuvo que dejar de hacer algunas tareas en su trabajo o en sus actividades cotidianas?", ["Sí", "No"], key="sf12_f_q5", horizontal=True, index=None)
    # Sí=1, No=2
    m[4] = 1 if resp5 == "Sí" else 2 if resp5 == "No" else None

    # Pregunta 6 (dolor)
    resp6 = st.radio("6. ¿Hasta qué punto el dolor le ha dificultado su trabajo habitual?", ["Nada", "Un poco", "Regular", "Bastante", "Mucho"], key="sf12_f_q6", horizontal=True, index=None)
    m[5] = (5 - ["Nada", "Un poco", "Regular", "Bastante", "Mucho"].index(resp6)) if resp6 is not None else None

    # Guardar parcial físico en session_state
    st.session_state['sf12_f_partial'] = m

    # Validación: asegurar que las preguntas de esta hoja estén completas.
    # Comprobar directamente los valores de los widgets en st.session_state
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
        ('sf12_f_salud', 'Seleccione una opción'),
        ('sf12_f_q2', None),
        ('sf12_f_q3', None),
        ('sf12_f_q4', None),
        ('sf12_f_q5', None),
        ('sf12_f_q6', None),
    ]

    faltan = not all(_answered(k, p) for k, p in required_keys)
    if faltan:
        st.error("❗ Por favor, responda todas las preguntas de la sección física antes de continuar.")
        disabled = True
    else:
        st.success("✅ Componente física completada")
        disabled = False

    col1, col2 = st.columns([2, 1])
    with col2:
        if st.button("Siguiente →", key="sf12_f_next", disabled=disabled, width='stretch'):
            # Montar respuestas completas: combinar parcial global con parcial físico
            full_respuestas = None
            if 'sf12_partial' in st.session_state and isinstance(st.session_state['sf12_partial'], list) and len(st.session_state['sf12_partial']) == 12:
                full_respuestas = st.session_state['sf12_partial'][:]  # copiar
            else:
                full_respuestas = [None] * 12

            # Mapear m (0..5) a las posiciones originales [0,1,2,3,4,7]
            mapping = {0:0, 1:1, 2:2, 3:3, 4:4, 5:7}
            for mi, val in enumerate(m):
                full_respuestas[mapping[mi]] = val

            # Guardar parcial combinado en session_state
            st.session_state['sf12_partial'] = full_respuestas

            # Calcular puntuaciones físicas (si es posible) y persistir cuartil físico
            resultados = calcular_sf12(full_respuestas)
            fisica = resultados.get('fisica')
            mental = resultados.get('mental')
            total = resultados.get('total')

            cuartil_fis = transformar_sf12_fisica_a_cuartil(fisica)
            etiqueta_fis = transformar_sf12_fisica_a_label(fisica)

            if 'resultados' not in st.session_state:
                st.session_state.resultados = {}
            st.session_state.resultados['sf12'] = {
                'puntaje_fisico': fisica,
                'puntaje_mental': mental,
                'total': total,
                'cuartil': cuartil_fis,
                'cuartil_label': etiqueta_fis,
                'respuestas': full_respuestas
            }

            # Persistir únicamente el cuartil físico desde esta página
            agregar_o_actualizar_registro(
                {
                    'salud_fisica': fisica,
                    'sf12_fisica_cuartil': cuartil_fis,
                    'sf12_fisica_cuartil_label': etiqueta_fis
                },
                tipo_datos='sf12'
            )

            # Ir a la página mental
            st.session_state.pagina_actual = "SF-12 Mental"
            st.rerun()

    st.markdown("---")
    with st.expander("Ver DataFrame completo"):
        mostrar_dataframe_actual()

    return None
